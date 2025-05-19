import yaml
from pathlib import Path
from models import init_db, get_session, Category, Question, Hint

def populate_database():
    """Populate the database with questions from the YAML file."""
    # Initialize database
    init_db()
    session = get_session()
    
    # Load questions from YAML
    yaml_path = Path(__file__).parent / 'questions.yaml'
    with open(yaml_path, 'r') as f:
        questions_data = yaml.safe_load(f)
    
    # Add categories and questions to database
    for category_name, questions in questions_data.items():
        # Create category
        category = Category(name=category_name)
        session.add(category)
        session.flush()  # Get category ID
        
        # Add questions for this category
        for q_data in questions:
            question = Question(
                question_text=q_data['question'],
                answer=q_data['answer'],
                category_id=category.id
            )
            session.add(question)
            session.flush()  # Get question ID
            
            # Add hints for this question
            for hint_text in q_data['hints']:
                hint = Hint(
                    hint_text=hint_text,
                    question_id=question.id
                )
                session.add(hint)
    
    # Commit all changes
    session.commit()
    session.close()

if __name__ == "__main__":
    populate_database() 