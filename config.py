import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    TARGET_URL = os.getenv('TARGET_URL', 'https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', './output')
    SCREENSHOTS_DIR = os.getenv('SCREENSHOTS_DIR', './screenshots')
    CHROMADB_PATH = os.getenv('CHROMADB_PATH', './chromadb_storage')
    
    # AI Model Settings
    MODEL_NAME = "claude-3-5-sonnet-20241022"
    MAX_TOKENS = 4096
    TEMPERATURE = 0.7
    
    # MAB Settings
    MAB_ALPHA = 1.0  # Thompson Sampling parameter
    MAB_BETA = 1.0
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.SCREENSHOTS_DIR, exist_ok=True)
        os.makedirs(cls.CHROMADB_PATH, exist_ok=True)