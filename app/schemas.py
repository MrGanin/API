from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(URLBase):
    pass

class URLResponse(URLBase):
    short_code: str
    short_url: str
    clicks: int

    class Config:
        from_attributes = True