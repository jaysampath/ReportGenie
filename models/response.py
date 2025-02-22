from langchain_core.pydantic_v1 import BaseModel, Field

class Response (BaseModel):
    query: str = Field (description="The SQL query to execute")
    columns: list = Field(description="The columns to include in the result")
    x_axis_column: str = Field(description="The column to use for the 'x-axis")
    y_axis_column: list = Field (description="The columns to use for the y-axis")
