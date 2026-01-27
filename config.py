import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///lang_project.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_TRANSLATE_API_KEY = os.getenv('GOOGLE_TRANSLATE_API_KEY')
