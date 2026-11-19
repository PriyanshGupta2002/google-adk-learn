from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field
from typing import Literal

# class Enquiry(BaseModel):
#     name: str
#     email: str
#     interested_in: str
#     budget_int: int

## The schema is way too simple cannnot handle null values
## the course names are not standardized
## If student says about multiple courses , then it will write in string


class Enquiry(BaseModel):
    name: str | None = Field(
        default=None, description="Student's full name, properly capitalized"
    )
    email: str | None = Field(
        default=None, description="Email address exactly as written"
    )
    interested_in: list[
        Literal["GenAI", "Data Science", "MLOps", "Deep Learning", "Other"]
    ] = Field(description="CampusX courses the student is interested in")
    budget_inr: int | None = Field(
        default=None,
        ge=0,
        le=500000,
        description="Total budget in rupees as a plain number. Convert '15k' to 15000",
    )


root_agent = Agent(
    model="gemini-3.8-flash",
    name="root_agent",
    description="Extracts student enquiry details from a message.",
    instruction="Read the student's message and extract their details. "
    "If something is not mentioned, leave it empty. Never guess.",
    output_schema=Enquiry,
    output_key="enquiry",
)
