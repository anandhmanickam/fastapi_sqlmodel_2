from sqlmodel import SQLModel, Field
from typing import Optional


# Create a Models

class TeamBase(SQLModel):
    name: str = Field(index=True)
    title: str
    players: Optional[int] = Field(default=None, index=True)

class Team(TeamBase, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)

