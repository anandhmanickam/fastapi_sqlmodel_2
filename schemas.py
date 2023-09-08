from models import TeamBase
from typing import Optional


# Create Schemas

class TeamCreate(TeamBase):
    pass 

class TeamRead(TeamBase):
    id: int

class TeamUpdate(TeamBase):
    name: Optional[str] = None
    players: Optional[int] = None
