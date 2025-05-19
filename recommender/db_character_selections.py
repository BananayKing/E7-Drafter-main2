from sqlalchemy.orm import Session
from .models import UserCharacterSelection

def save_user_characters(db: Session, user_id: int, character_ids: list[str]):
    # Remove old selections for user
    db.query(UserCharacterSelection).filter(UserCharacterSelection.user_id == user_id).delete()
    # Add new selections
    for char_id in character_ids:
        db.add(UserCharacterSelection(user_id=user_id, character_id=char_id))
    db.commit()

def get_user_characters(db: Session, user_id: int):
    result = db.query(UserCharacterSelection).filter(UserCharacterSelection.user_id == user_id).all()
    print(f"User {user_id} characters: {[c.character_id for c in result]}")
    return result
