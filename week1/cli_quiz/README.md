# CLI Quiz Application

A command-line interface quiz application that tests your knowledge of Linux, Git, and UV commands. The application provides an interactive quiz experience with multiple categories and features.

## Features

- Multiple categories (Linux, Git, UV commands)
- Random question selection
- Multiple attempts per question
- Hint system for incorrect answers
- Score tracking
- Immediate feedback on answers
- YAML/JSON question bank support

## Project Structure

```
cli_quiz/
├── quiz.py          # Main quiz application
├── models.py        # Database models and SQLAlchemy setup
├── populate_db.py   # Script to populate the database
├── questions.yaml   # Question bank in YAML format
├── questions.json   # Question bank in JSON format
└── requirements.txt # Project dependencies
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python populate_db.py
   ```

## Usage

Run the quiz:
```bash
python quiz.py
```

The quiz will:
- Allow you to select a category (Linux, Git, or UV commands)
- Present questions about command-line tools
- Provide hints if you need help
- Track your score
- Give immediate feedback on your answers

## Development

The application is built with:
- Python 3.x
- SQLAlchemy for database management
- SQLite for data storage
- PyYAML for YAML file parsing

## License

MIT License 