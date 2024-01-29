from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AssistantConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    address: str = Field(validation_alias='viam_address')
    api_key: str = Field(validation_alias='viam_api_key')
    api_key_id: str = Field(validation_alias='viam_api_key_id')
    chat_name: str = Field(validation_alias='chat_service_name', default="llm")
    speech_name: str = Field(validation_alias='speech_service_name', default="speaker")
