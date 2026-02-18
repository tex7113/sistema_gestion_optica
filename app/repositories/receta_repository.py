from sqlalchemy.orm import Session
from app.models.receta_model import Receta
from app.schemas.receta_schema import RecetaCreate, RecetaUpdate


class RecetaRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Receta).all()

    @staticmethod
    def get_by_id(db: Session, receta_id: int):
        return db.query(Receta).filter(Receta.id == receta_id).first()

    @staticmethod
    def get_by_cliente(db: Session, cliente_id: int):
        return db.query(Receta).filter(Receta.cliente_id == cliente_id).all()

    @staticmethod
    def create(db: Session, receta: RecetaCreate):
        db_receta = Receta(**receta.model_dump())
        db.add(db_receta)
        db.commit()
        db.refresh(db_receta)
        return db_receta

    @staticmethod
    def update(db: Session, receta_id: int, receta: RecetaUpdate):
        db_receta = RecetaRepository.get_by_id(db, receta_id)

        if not db_receta:
            return None

        for key, value in receta.model_dump(exclude_unset=True).items():
            setattr(db_receta, key, value)

        db.commit()
        db.refresh(db_receta)
        return db_receta

    @staticmethod
    def delete(db: Session, receta_id: int):
        db_receta = RecetaRepository.get_by_id(db, receta_id)

        if not db_receta:
            return None

        db.delete(db_receta)
        db.commit()
        return db_receta
