import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///insomnia_diagnosis.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG  # 在调试模式下显示SQL语句
    
    # 微信公众号配置
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', '')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', '')
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'your_wechat_token')
    WECHAT_ENCODING_AES_KEY = os.getenv('WECHAT_ENCODING_AES_KEY', '')
    
    # 企业微信配置
    WORK_WECHAT_CORP_ID = os.getenv('WORK_WECHAT_CORP_ID', '')
    WORK_WECHAT_CORP_SECRET = os.getenv('WORK_WECHAT_CORP_SECRET', '')
    WORK_WECHAT_AGENT_ID = os.getenv('WORK_WECHAT_AGENT_ID', '')
    WORK_WECHAT_TOKEN = os.getenv('WORK_WECHAT_TOKEN', '')
    WORK_WECHAT_ENCODING_AES_KEY = os.getenv('WORK_WECHAT_ENCODING_AES_KEY', '')
    
    # Redis配置(用于存储用户会话)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # API配置
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
    
    # 中医AI配置
    TCM_AI_MODEL = os.getenv('TCM_AI_MODEL', 'qwen-turbo')
    TCM_AI_API_KEY = os.getenv('TCM_AI_API_KEY', '')
    
    # 系统设置
    MAX_QUESTIONS = 19
    SESSION_TIMEOUT = 3600  # 1小时会话超时