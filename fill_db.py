from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Charity, CharityPhoto, CharityProject, ProjectPhoto, ProjectComment, ProjectCategory, ProjectCategoryMapping

# Создание соединения с базой данных
DATABASE_URL = "postgresql://postgres:postgres@localhost/charity_database"  # Замените username, password, localhost и charity_database на ваши реальные данные
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание сессии базы данных
db = SessionLocal()

# Добавление данных в таблицу Charity
charity1 = Charity(name="Charity 1", description="Description of Charity 1", contact_info="Contact info of Charity 1", username="charity1", password_hash="hash1")
charity2 = Charity(name="Charity 2", description="Description of Charity 2", contact_info="Contact info of Charity 2", username="charity2", password_hash="hash2")
db.add(charity1)
db.add(charity2)
db.commit()

# Добавление данных в таблицу CharityPhoto
charity_photo1 = CharityPhoto(charity_id=1, photo_url="url1", description="Photo 1 of Charity 1")
charity_photo2 = CharityPhoto(charity_id=2, photo_url="url2", description="Photo 1 of Charity 2")
db.add(charity_photo1)
db.add(charity_photo2)
db.commit()

# Добавление данных в таблицу CharityProject
project1 = CharityProject(name="Project 1", description="Description of Project 1", start_date=datetime.now(), end_date=datetime.now(), charity_id=1)
project2 = CharityProject(name="Project 2", description="Description of Project 2", start_date=datetime.now(), end_date=datetime.now(), charity_id=2)
db.add(project1)
db.add(project2)
db.commit()

# Добавление данных в таблицу ProjectPhoto
project_photo1 = ProjectPhoto(project_id=1, photo_url="url1", description="Photo 1 of Project 1")
project_photo2 = ProjectPhoto(project_id=2, photo_url="url2", description="Photo 1 of Project 2")
db.add(project_photo1)
db.add(project_photo2)
db.commit()

# Добавление данных в таблицу ProjectComment
comment1 = ProjectComment(comment_text="Comment 1 for Project 1", comment_date=datetime.now(), project_id=1)
comment2 = ProjectComment(comment_text="Comment 1 for Project 2", comment_date=datetime.now(), project_id=2)
db.add(comment1)
db.add(comment2)
db.commit()

# Добавление данных в таблицу ProjectCategory
category1 = ProjectCategory(name="Category 1")
category2 = ProjectCategory(name="Category 2")
db.add(category1)
db.add(category2)
db.commit()

# Добавление данных в таблицу ProjectCategoryMapping
mapping1 = ProjectCategoryMapping(project_id=1, category_id=1)
mapping2 = ProjectCategoryMapping(project_id=2, category_id=2)
db.add(mapping1)
db.add(mapping2)
db.commit()

# Закрытие сессии
db.close()
