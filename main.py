from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Charity, CharityPhoto, CharityProject, ProjectPhoto, \
    ProjectComment, ProjectCategory, ProjectCategoryMapping

DATABASE_URL = "postgresql://fastapiuser:fastapi@localhost/charity_database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/charities/")
def get_charities(db: Session = Depends(get_db)):
    charities = db.query(Charity).all()
    return charities


@app.get("/charities/{charity_id}")
def get_charity(charity_id: int, db: Session = Depends(get_db)):
    charity = db.query(Charity).filter(
        Charity.charity_id == charity_id).first()
    if charity is None:
        raise HTTPException(status_code=404, detail="Charity not found")
    return charity


@app.post("/charities/")
def create_charity(name: str, description: str, contact_info: str,
                   username: str, password_hash: str,
                   db: Session = Depends(get_db)):
    charity = Charity(name=name, description=description,
                      contact_info=contact_info, username=username,
                      password_hash=password_hash)
    db.add(charity)
    db.commit()
    return charity


@app.get("/charity-photos/")
def get_charity_photos(db: Session = Depends(get_db)):
    charity_photos = db.query(CharityPhoto).all()
    return charity_photos


@app.get("/charity-photos/{photo_id}")
def get_charity_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(CharityPhoto).filter(
        CharityPhoto.photo_id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=404, detail="Charity photo not found")
    return photo


@app.post("/charity-photos/")
def create_charity_photo(charity_id: int, photo_url: str, description: str,
                         db: Session = Depends(get_db)):
    photo = CharityPhoto(charity_id=charity_id, photo_url=photo_url,
                         description=description)
    db.add(photo)
    db.commit()
    return photo


@app.get("/charity-projects/")
def get_charity_projects(db: Session = Depends(get_db)):
    charity_projects = db.query(CharityProject).all()
    return charity_projects


@app.get("/charity-projects/{project_id}")
def get_charity_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(CharityProject).filter(
        CharityProject.project_id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404,
                            detail="Charity project not found")
    return project


@app.post("/charity-projects/")
def create_charity_project(name: str, description: str, start_date: str,
                           end_date: str, charity_id: int,
                           db: Session = Depends(get_db)):
    project = CharityProject(name=name, description=description,
                             start_date=start_date, end_date=end_date,
                             charity_id=charity_id)
    db.add(project)
    db.commit()
    return project


@app.get("/project-photos/")
def get_project_photos(db: Session = Depends(get_db)):
    project_photos = db.query(ProjectPhoto).all()
    return project_photos


@app.get("/project-photos/{photo_id}")
def get_project_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(ProjectPhoto).filter(
        ProjectPhoto.photo_id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=404, detail="Project photo not found")
    return photo


@app.post("/project-photos/")
def create_project_photo(project_id: int, photo_url: str, description: str,
                         db: Session = Depends(get_db)):
    photo = ProjectPhoto(project_id=project_id, photo_url=photo_url,
                         description=description)
    db.add(photo)
    db.commit()
    return photo


@app.get("/project-comments/")
def get_project_comments(db: Session = Depends(get_db)):
    project_comments = db.query(ProjectComment).all()
    return project_comments


@app.get("/project-comments/{comment_id}")
def get_project_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(ProjectComment).filter(
        ProjectComment.comment_id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=404,
                            detail="Project comment not found")
    return comment


@app.post("/project-comments/")
def create_project_comment(comment_text: str, comment_date: str,
                           project_id: int, db: Session = Depends(get_db)):
    comment = ProjectComment(comment_text=comment_text,
                             comment_date=comment_date, project_id=project_id)
    db.add(comment)
    db.commit()
    return comment


@app.get("/project-categories/")
def get_project_categories(db: Session = Depends(get_db)):
    project_categories = db.query(ProjectCategory).all()
    return project_categories


@app.get("/project-categories/{category_id}")
def get_project_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ProjectCategory).filter(
        ProjectCategory.category_id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404,
                            detail="Project category not found")
    return category


@app.post("/project-categories/")
def create_project_category(name: str, db: Session = Depends(get_db)):
    category = ProjectCategory(name=name)
    db.add(category)
    db.commit()
    return category


@app.get("/project-category-mappings/")
def get_project_category_mappings(db: Session = Depends(get_db)):
    mappings = db.query(ProjectCategoryMapping).all()
    return mappings


@app.get("/project-category-mappings/{project_id}/{category_id}")
def get_project_category_mapping(project_id: int, category_id: int,
                                 db: Session = Depends(get_db)):
    mapping = db.query(ProjectCategoryMapping).filter(
        ProjectCategoryMapping.project_id == project_id,
        ProjectCategoryMapping.category_id == category_id).first()
    if mapping is None:
        raise HTTPException(status_code=404,
                            detail="Project category mapping not found")
    return mapping


@app.post("/project-category-mappings/")
def create_project_category_mapping(project_id: int, category_id: int,
                                    db: Session = Depends(get_db)):
    mapping = ProjectCategoryMapping(project_id=project_id,
                                     category_id=category_id)
    db.add(mapping)
    db.commit()
    return mapping


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
