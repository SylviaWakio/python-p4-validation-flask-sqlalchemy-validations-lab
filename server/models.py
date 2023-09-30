from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    @validates('name')
    def validate_name(self, key, name):
        # Validation: All authors have a name.
        if not name.strip():  # Check for empty or whitespace-only names.
            raise ValueError('Author name cannot be empty.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # Validation: Author phone numbers are exactly ten digits.
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

    @validates('title')
    def validate_title(self, key, title):
        # Validation: All posts have a title.
        if not title.strip():  # Check for empty or whitespace-only titles.
            raise ValueError('Post title cannot be empty.')
        # Validation: Check for clickbait titles.
        clickbait_keywords = ['shocking', 'amazing', 'unbelievable']
        for keyword in clickbait_keywords:
            if keyword in title.lower():
                raise ValueError('Post title is clickbait.')
        return title

    @validates('content')
    def validate_content(self, key, content):
        # Validation: Post content is at least 250 characters long.
        if content and len(content) < 250:
            raise ValueError('Post content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        # Validation: Post summary is a maximum of 250 characters.
        if summary and len(summary) > 250:
            raise ValueError('Post summary cannot exceed 250 characters.')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        # Validation: Post category is either Fiction or Non-Fiction.
        valid_categories = ['Fiction', 'Non-Fiction']
        if category and category not in valid_categories:
            raise ValueError('Post category must be Fiction or Non-Fiction.')
        return category