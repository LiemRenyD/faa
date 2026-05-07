from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar, Dict


class Settings(BaseSettings):
    # 静态定义：哪些字段要拼接到 URL 上，以及对应的 URL 参数名
    URL_PARAMS: ClassVar[Dict[str, str]] = {
        "answertimelimit": "answerTimeLimit",
        "questionlimit": "questionLimit",
        # 未来新增参数只需在这里加一行
        # "category_id": "categoryId",
    }

    phone_number: str = Field(alias="PHONE_NUMBER")
    password: str = Field(alias="PASSWORD")
    website_url: str = Field(alias="WEBSITE_URL")
    question_url: str = Field(alias="QUESTION_URL")
    answer_interval: int = Field(default=500, alias="ANSWER_INTERVAL")
    max_rounds: int = Field(default=1, alias="MAX_ROUNDS")
    headless: bool = Field(default=False, alias="HEADLESS")
    end_score: int = Field(default=180, alias="END_SCORE")
    answertimelimit: int = Field(default=20, alias="ANSWERTIMELIMIT")
    questionlimit: int = Field(default=10, alias="QUESTIONLIMIT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @model_validator(mode='after')
    def auto_append_url_params(self):
        base = self.question_url
        connector = "&" if "?" in base else "?"
        # 遍历 URL_PARAMS，动态拼接
        params = []
        for field_name, param_name in self.URL_PARAMS.items():
            value = getattr(self, field_name, None)
            if value is not None:
                params.append(f"{param_name}={value}")
        if params:
            self.question_url = f"{base}{connector}" + "&".join(params)
        return self
        
settings = Settings()