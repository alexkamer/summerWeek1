import random
from pathlib import Path
from models import get_session, Category, Question, Hint

class Quiz:
    def __init__(self):
        self.session = get_session()
        self.score = 0
        self.current_category = None
        self.current_question = None
        self.questions_asked = 0
        self.total_questions = 0
        self.asked_questions = set()

    def get_categories(self):
        """Return list of available categories."""
        categories = self.session.query(Category).all()
        return [category.name for category in categories]

    def select_category(self, category=None):
        """Select a category. If None or invalid, select random category."""
        if category is None:
            self.current_category = random.choice(self.get_categories())
        else:
            # Check if category exists
            category_obj = self.session.query(Category).filter_by(name=category).first()
            if category_obj:
                self.current_category = category
            else:
                self.current_category = random.choice(self.get_categories())
        return self.current_category

    def get_random_question(self):
        """Get a random question from the current category that hasn't been asked yet."""
        if not self.current_category:
            raise ValueError("No category selected")
        
        # Get category object
        category = self.session.query(Category).filter_by(name=self.current_category).first()
        
        # Get all questions for the category
        available_questions = self.session.query(Question).filter_by(category_id=category.id).all()
        
        # Filter out questions that have already been asked
        unasked_questions = [q for q in available_questions if q.question_text not in self.asked_questions]
        
        # If all questions have been asked, reset the asked questions set
        if not unasked_questions:
            print("\nAll questions in this category have been asked. Resetting question bank...")
            self.asked_questions.clear()
            unasked_questions = available_questions
        
        # Select a random question from unasked questions
        self.current_question = random.choice(unasked_questions)
        self.asked_questions.add(self.current_question.question_text)
        return self.current_question

    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        if not self.current_question:
            raise ValueError("No question selected")
        
        return user_answer.strip().lower() == self.current_question.answer.lower()

    def get_hint(self, hint_index=0):
        """Get a hint for the current question."""
        if not self.current_question:
            raise ValueError("No question selected")
        
        # Get hints for current question
        hints = self.session.query(Hint).filter_by(question_id=self.current_question.id).all()
        if 0 <= hint_index < len(hints):
            return hints[hint_index].hint_text
        return "No more hints available"

    def set_total_questions(self, num_questions):
        """Set the total number of questions to be asked."""
        self.total_questions = num_questions
        self.questions_asked = 0
        self.score = 0
        self.asked_questions.clear()

    def display_score(self):
        """Display current score and progress."""
        print(f"\nCurrent score: {self.score}/{self.questions_asked}")
        if self.total_questions > 0:
            print(f"Progress: {self.questions_asked}/{self.total_questions} questions answered")

    def __del__(self):
        """Close the database session when the quiz object is destroyed."""
        self.session.close()

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
        print(f"\nQuestion: {question.question_text}")
        
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
                    print(f"\nIncorrect! The correct answer was: {question.answer}")
        
        quiz.questions_asked += 1
    
    # Display final score
    quiz.display_score()
    print("\nQuiz completed!")

if __name__ == "__main__":
    main() 