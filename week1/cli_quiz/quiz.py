import json
import random
from pathlib import Path

class Quiz:
    def __init__(self):
        self.questions = self._load_questions()
        self.score = 0
        self.current_category = None
        self.current_question = None
        self.questions_asked = 0
        self.total_questions = 0

    def _load_questions(self):
        """Load questions from the JSON file."""
        json_path = Path(__file__).parent / 'questions.json'
        with open(json_path, 'r') as f:
            return json.load(f)

    def get_categories(self):
        """Return list of available categories."""
        return list(self.questions.keys())

    def select_category(self, category=None):
        """Select a category. If None or invalid, select random category."""
        if category is None or category not in self.questions:
            self.current_category = random.choice(self.get_categories())
        else:
            self.current_category = category
        return self.current_category

    def get_random_question(self):
        """Get a random question from the current category."""
        if not self.current_category:
            raise ValueError("No category selected")
        
        self.current_question = random.choice(self.questions[self.current_category])
        return self.current_question

    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        if not self.current_question:
            raise ValueError("No question selected")
        
        return user_answer.strip().lower() == self.current_question['answer'].lower()

    def get_hint(self, hint_index=0):
        """Get a hint for the current question."""
        if not self.current_question:
            raise ValueError("No question selected")
        
        hints = self.current_question['hints']
        if 0 <= hint_index < len(hints):
            return hints[hint_index]
        return "No more hints available"

    def set_total_questions(self, num_questions):
        """Set the total number of questions to be asked."""
        self.total_questions = num_questions
        self.questions_asked = 0
        self.score = 0

    def display_score(self):
        """Display current score and progress."""
        print(f"\nCurrent score: {self.score}/{self.questions_asked}")
        if self.total_questions > 0:
            print(f"Progress: {self.questions_asked}/{self.total_questions} questions answered")

def check_quit(user_input):
    """Check if user wants to quit."""
    return user_input.strip().lower() in ['q', 'quit', 'exit']

def main():
    quiz = Quiz()
    
    # Display available categories
    print("\nAvailable categories:", ", ".join(quiz.get_categories()))
    print("(Type 'q' or 'quit' at any time to exit)")
    
    # Get category from user
    category = input("\nEnter a category (or press Enter for random): ").strip().lower()
    if check_quit(category):
        print("\nQuiz terminated. No questions were answered.")
        return
    
    selected_category = quiz.select_category(category)
    print(f"\nSelected category: {selected_category}")
    
    # Get number of questions
    while True:
        try:
            num_questions = input("\nHow many questions would you like to answer? ")
            if check_quit(num_questions):
                print("\nQuiz terminated. No questions were answered.")
                return
            num_questions = int(num_questions)
            if num_questions > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    quiz.set_total_questions(num_questions)
    
    # Main quiz loop
    while quiz.questions_asked < quiz.total_questions:
        print(f"\nQuestion {quiz.questions_asked + 1} of {quiz.total_questions}")
        question = quiz.get_random_question()
        print(f"\nQuestion: {question['question']}")
        
        # First attempt
        user_answer = input("Your answer (or 'q' to quit): ")
        if check_quit(user_answer):
            quiz.display_score()
            print("\nQuiz terminated early.")
            return
        
        if quiz.check_answer(user_answer):
            print("Correct! +1 point")
            quiz.score += 1
        else:
            # First hint
            print("\nIncorrect! Here's a hint:")
            print(quiz.get_hint(0))
            
            # Second attempt
            user_answer = input("Try again (or 'q' to quit): ")
            if check_quit(user_answer):
                quiz.display_score()
                print("\nQuiz terminated early.")
                return
            
            if quiz.check_answer(user_answer):
                print("Correct! +1 point")
                quiz.score += 1
            else:
                # Second hint
                print("\nIncorrect! Here's another hint:")
                print(quiz.get_hint(1))
                
                # Final attempt
                user_answer = input("Last try (or 'q' to quit): ")
                if check_quit(user_answer):
                    quiz.display_score()
                    print("\nQuiz terminated early.")
                    return
                
                if quiz.check_answer(user_answer):
                    print("Correct! +1 point")
                    quiz.score += 1
                else:
                    print(f"\nIncorrect! The correct answer was: {question['answer']}")
        
        quiz.questions_asked += 1
    
    # Display final score
    quiz.display_score()
    print("\nQuiz completed!")

if __name__ == "__main__":
    main() 