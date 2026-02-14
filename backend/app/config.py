"""
配置管理（使用环境变量）
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "OpenCode Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://opencode:opencode123@localhost:5432/opencode"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置（必须通过环境变量设置）
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")  # 不提供默认值，强制从环境变量读取
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # opencode配置
    OPENCODE_CLI_PATH: str = "opencode"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# 验证SECRET_KEY
if not settings.SECRET_KEY:
    raise ValueError(
        "SECRET_KEY must be set in environment variables. "
        "Generate one with: openssl rand -hex 32"
    )
