from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Name cannot be null")
        
        # Check if the name already exists in the database
        existing_author = Author.query.filter_by(name=value).first()
        if existing_author:
            raise ValueError(f"Author with name '{value}' already exists.")
        
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        return value
    
    def __repr__(self):
            return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content', 'summary', 'category', 'title')
    def validate_post(self, key, value):
        if key == 'content' and len(value) < 250:
            raise ValueError("Content must be at least 250 characters long")
        if key == 'summary' and len(value) > 250:
            raise ValueError("Summary must be a maximum of 250 characters")
        if key == 'category' and value not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'")
        if key == 'title' and not any(phrase in value for phrase in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
