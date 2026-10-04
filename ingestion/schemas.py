from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NewsItem(BaseModel):
    id: int | str = Field(description="Identificador único da notícia")

    # Permite receber campos extras (payload da API) sem quebrar a validação
    model_config = ConfigDict(extra="allow")

    # Adicione aqui outros campos obrigatórios que queira validar estritamente
    # title: str = Field(description="Título da notícia")
