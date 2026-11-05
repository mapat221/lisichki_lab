from pydantic import BaseModel, StrictBool


class SuccessResponse(BaseModel):
    success: StrictBool = True
