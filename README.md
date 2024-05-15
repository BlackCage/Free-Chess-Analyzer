![ChessDotComLogo](https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/PedroPinhata/phpNgJfyb.png)

`Chess.com Analyzer` is a Python package for analyzing chess games played on Chess.com and retrieving detailed analysis results using the Stockfish 16 NNUE engine. Unlike the Chess.com platform, `Chess Analyzer` is completely free, allowing you to analyze chess games without any cost.

## Features

- 🔍 Analyze chess games played on Chess.com (because who wants to pay for that?).
- 📊 Retrieve game analysis results including move tallies (for the thrifty chess enthusiast).
- 📅 Fetch game numbers and corresponding opponents for a specific user in a given month and year (all without spending a dime!).

## Installation

You can install `Chess.com Analyzer` using pip:

```bash
pip install chess.com-analyzer
```

## Usage

```python
from chess.com_analyzer import ChessAnalyzer

# Initialize a ChessAnalyzer instance
analyzer = ChessAnalyzer()

# Get game numbers and corresponding opponents for a user in a specified month and year
games_info = analyzer.get_game_number("username", year="2024", month="5")

# Analyze a specific game played by the user
game_analysis = analyzer.analyze_game("username", game_number=0, year="2024", month="5")

# Print the analysis results
print(game_analysis)
```

## Contributing

Contributions to `Chess.com Analyzer` are welcome! If you would like to contribute, please follow these guidelines:

- 🛠️ Check if there are any open issues you would like to work on. If not, feel free to open a new issue to discuss your ideas or suggestions.
- 🍴 Fork the repository and create a new branch for your contributions.
- 📝 Make your changes, ensuring adherence to the project's coding style and conventions.
- ✅ Write clear, concise, and well-documented code and commit messages.
- ✔️ Test your changes to ensure they work as expected.
- 🚀 Submit a pull request, explaining the purpose of your changes and referencing any related issues or discussions.

We appreciate your contributions and look forward to making `Chess.com Analyzer` even better together.

## License

This project is licensed under the MIT License. By contributing to this project, you agree to adhere to the terms and conditions outlined in the [LICENSE](https://github.com/BlackCage/free-chess-analyzer/blob/main/LICENSE) file.

## Author

This project is authored by a dedicated developer passionate about chess and software development.

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BlackCage) [![Twitter](https://img.shields.io/badge/Twitter-000000?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/BlackByte_) [![ProtonMail](https://img.shields.io/badge/ProtonMail-8B89CC?style=for-the-badge&logo=protonmail&logoColor=white)](mailto:blackcage_faq@proton.me)

Your feedback and collaboration are greatly appreciated. Thank you for your interest in `Chess.com Analyzer`.