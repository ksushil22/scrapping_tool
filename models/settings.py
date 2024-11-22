from pydantic import BaseModel, Field


class ScraperSettings(BaseModel):
    """Scrapper model to get the request body ."""
    page_limit: int = Field(..., ge=1)  # limit for the pagination
    proxy: None
    url: str = ""  # required web url
