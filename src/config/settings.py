from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    phone_number: str = Field(alias="PHONE_NUMBER")
    password: str = Field(alias="PASSWORD")
    website_url: str = Field(alias="WEBSITE_URL")
    question_url: str = Field(alias="QUESTION_URL")
    answer_interval: int = Field(default=500, alias="ANSWER_INTERVAL")
    max_rounds: int = Field(default=1, alias="MAX_ROUNDS")
    headless: bool = Field(default=False, alias="HEADLESS")

    end_score: int = Field(default=180, alias="END_SCORE")
    answertimelimit: int = Field(default=20, alias="ANSWERTITELIMIT")
    questionlimit: int = Field(default=10, alias="QUESTIONLIMIT")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        # 核心修复：允许环境变量中存在类中未定义的字段，而不会报错
        extra="ignore" 
    )
settings = Settings()