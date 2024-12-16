from pydantic import BaseModel, Field

class EmailPriorityRequest(BaseModel):
    email_body: str = Field(..., description="The body of the email for priority analysis.")
