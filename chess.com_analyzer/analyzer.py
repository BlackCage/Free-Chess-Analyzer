import re
import json
import string
import random
import asyncio
import datetime
import requests
import websockets
from fake_useragent import UserAgent
from chessdotcom import get_player_games_by_month, Client

class ChessAnalyzer:
    CHESSKID_URL     = "https://www.chesskid.com"
    ANALYSIS_WS_URL  = "wss://analysis-va.chess.com/"
    ENGINE_TYPE      = "stockfish16 nnue"
    TALLIES_LIST     = ["brilliant", "greatFind", "best", "excellent", "good", "book", "inaccuracy", "mistake", "miss", "blunder"]

    def __init__(self):
        Client.request_config["headers"]["User-Agent"] = (
            "My Python Application."
            "Contact me at email@example.com"
        )

    def __generate_account(self):
        """
        Generates a random account for chesskid.com registration.

        Returns:
            str: Generated token for authentication.
        """

        user       = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=15))
        passwd     = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))
        PHPSESSID  = requests.get(f'{self.CHESSKID_URL}/register/user-type').cookies["PHPSESSID"]

        json_data = {
            'avatarFilename': 'kid-1459.png',
            'username': user,
            'userType': 'kid',
            'password': passwd,
            'email': f'{user}@gmail.com',
        }
        response = requests.post(f'{self.CHESSKID_URL}/callback/register/account', cookies={'PHPSESSID': PHPSESSID}, headers={'User-Agent': UserAgent().random}, json=json_data)
        if user not in response.json()["user"]["username"]: return "ERROR GENERATING ACCOUNT."

        return self.__fetch_token(response.cookies["PHPSESSID"])
    
    def __fetch_token(self, PHPSESSID):
        """
        Fetches the authentication token for game analysis.

        Args:
            PHPSESSID (str): PHP session ID for authentication.

        Returns:
            str: Authentication token.
        """

        token = requests.get(f'{self.CHESSKID_URL}/callback/auth/service/analysis', cookies={"PHPSESSID": PHPSESSID}).json()["token"]
        return token
    
    def get_game_number(self, username, year=str(datetime.datetime.now().year), month=str(datetime.datetime.now().month)):
        """
        Retrieves the games played by a user in a specified year and month.

        Args:
            username (str): Username of the player.
            year (str): Year of the games (default is current year).
            month (str): Month of the games (default is current month).

        Returns:
            dict: Dictionary containing game numbers and corresponding opponents.
        """

        user_games    = {}
        player_games  = get_player_games_by_month(username, year=year, month=month).json["games"]

        for idx, games in enumerate(player_games):
            user_games.update({idx: {"white": games["white"]["username"], "black": games["black"]["username"]}})
        return user_games

    def analyze_game(self, username: str, game_number: int, year=str(datetime.datetime.now().year), month=str(datetime.datetime.now().month)):
        """
        Analyzes a specific game played by the user.

        Args:
            username (str): Username of the player.
            game_number (int): Index of the game in the player's list of games.
            year (str): Year of the games (default is current year).
            month (str): Month of the games (default is current month).

        Returns:
            dict: Dictionary containing analysis results.
        """

        usernames = {}
        
        player_games  = get_player_games_by_month(username, year=year, month=month).json["games"]
        pgn           = player_games[game_number]["pgn"]
        gameID        = re.search("[0-9].*", player_games[game_number]["url"]).group(0)

        for color in ["white", "black"]:
            usernames[color] = player_games[game_number][color]["username"]

        return self.__get_tallies(asyncio.run(self.__analyze_game_async(pgn, gameID)), usernames)
    
    async def __analyze_game_async(self, pgn: str, gameID: str):
        """
        Asynchronously analyzes a game using websockets.

        Args:
            pgn (str): PGN (Portable Game Notation) of the game.
            gameID (str): ID of the game.

        Returns:
            str: Analysis results in JSON format.
        """

        token = self.__generate_account()

        async with websockets.connect(self.ANALYSIS_WS_URL) as websocket:
            data = {
                "action": "gameAnalysis",
                "game": {"pgn": pgn},
                "options": {
                    "caps2": True,
                    "getNullMove": True,
                    "engineType": self.ENGINE_TYPE,
                    "source": {
                        "gameId": gameID,
                        "gameType": "live",
                        "token": token,
                        "client": "web",
                        "userTimeZone": "Europe/Madrid"
                    },
                    "tep": {
                        "ceeDebug": False,
                        "lang": "en_US",
                        "speechv2": True,
                        "userColor": "white",
                        "classificationv3": True
                    },
                    "strength": "Maximum"
                }
            }
            await websocket.send(json.dumps(data))
            while True:
                game = await websocket.recv()
                if json.loads(game)["action"] == "analyzeGame": return game
                
    def __get_tallies(self, game: str, usernames: dict):
        """
        Parses the analysis results and extracts tallies for each move.

        Args:
            game (str): Analysis results in JSON format.
            usernames (dict): Dictionary containing usernames of players.

        Returns:
            dict: Dictionary containing analysis results including move tallies.
        """

        result = {}
        data = json.loads(game)

        opening = str(data["data"]["book"]["name"]).split(",")[0]
        result["opening"] = opening
        result["engine"] = "StockFish 16 NNUE (Maximum)"

        for color in ["white", "black"]:
            username       = usernames[color]
            effective_elo  = data["data"]["reportCard"][color]["effectiveElo"]
            accuracy       = str(data["data"]["CAPS"][color]["all"])[:4]
            open_acc       = str(data["data"]["CAPS"][color]["gp0"])[:4]
            midd_acc       = str(data["data"]["CAPS"][color]["gp1"])[:4]
            end_acc        = str(data["data"]["CAPS"][color]["gp2"])[:4]

            result[color] = {
                "username": username,
                "effective_elo": effective_elo,
                "accuracy": accuracy,
                "open_acc": open_acc,
                "midd_acc": midd_acc,
                "end_acc": end_acc,
                "move_rating": {move: data["data"]["tallies"][color][move] for move in self.TALLIES_LIST}
            }
        return result