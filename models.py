from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost/charity_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Charity(Base):
    __tablename__ = "charities"

    charity_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    contact_info = Column(Text)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)

    photos = relationship("CharityPhoto", back_populates="charity")
    projects = relationship("CharityProject", back_populates="charity")


class CharityPhoto(Base):
    __tablename__ = "charity_photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    charity_id = Column(Integer, ForeignKey("charities.charity_id"))
    photo_url = Column(Text)
    description = Column(Text)

    charity = relationship("Charity", back_populates="photos")


class CharityProject(Base):
    __tablename__ = "charity_projects"

    project_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    charity_id = Column(Integer, ForeignKey("charities.charity_id"))

    charity = relationship("Charity", back_populates="projects")
    photos = relationship("ProjectPhoto", back_populates="project")
    comments = relationship("ProjectComment", back_populates="project")
    categories = relationship("ProjectCategory", secondary="project_category_mapping")


class ProjectPhoto(Base):
    __tablename__ = "project_photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("charity_projects.project_id"))
    photo_url = Column(Text)
    description = Column(Text)

    project = relationship("CharityProject", back_populates="photos")


class ProjectComment(Base):
    __tablename__ = "project_comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    comment_text = Column(Text, nullable=False)
    comment_date = Column(Date, nullable=False)
    project_id = Column(Integer, ForeignKey("charity_projects.project_id"))

    project = relationship("CharityProject", back_populates="comments")


class ProjectCategory(Base):
    __tablename__ = "project_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class ProjectCategoryMapping(Base):
    __tablename__ = "project_category_mapping"

    project_id = Column(Integer, ForeignKey("charity_projects.project_id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("project_categories.category_id"), primary_key=True)


# Создание таблиц в базе данных
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
