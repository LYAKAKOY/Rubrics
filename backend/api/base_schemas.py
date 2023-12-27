from pydantic import BaseModel


class TunedModel(BaseModel):
    class ConfigDict:
        from_attributes = True
