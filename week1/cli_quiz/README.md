# CLI Command Quiz

A command-line quiz application that tests your knowledge of Linux, Git, and UV commands.

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

## Features

- Multiple categories (Linux, Git, UV)
- Random question selection
- Hint system
- Score tracking
- Immediate feedback

## Project Structure

- `quiz.py`: Main quiz application
- `questions.json`: Question bank
- `requirements.txt`: Project dependencies 