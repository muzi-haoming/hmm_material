"""
应用配置模块
"""
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    # 基础配置
    APP_NAME: str = "HMM Material Management"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://postgres:!q2w3e4R@127.0.0.1:5432/hmm_material"

    # AI 配置
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"

    # CORS 配置
    CORS_ORIGINS: List[str] = ["http://localhost:8080", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()
