from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from app.utils.db import get_db

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model_class: T):
        self.model_class = model_class
        self.db: Session = get_db()

    def get_all(self) -> List[T]:
        return self.db.query(self.model_class).all()

    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.query(self.model_class).filter_by(id=id).first()

    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.db.delete(entity)
        self.db.commit()
