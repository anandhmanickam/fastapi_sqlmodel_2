from sqlmodel import SQLModel, create_engine, Session, select
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from models import Team
from schemas import TeamCreate, TeamRead, TeamUpdate


# Create Engine    
    
url = "mysql://root@127.0.0.1:3306/teams"
engine = create_engine(url, echo=True)


# Create Migrations

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

# Create session

def get_sesion():
    with Session(engine) as session:
        yield session
        
        
# Create Routes

app = FastAPI()

@app.on_event('startup')
def on_startup():
    create_db_and_tables()
    
    
@app.post("/teams/", response_model=TeamRead)
def create_team(*, session: Session = Depends(get_sesion), team: TeamCreate):
    with Session(engine) as session:
        db_team = Team.from_orm(team)

        session.add(db_team)
        session.commit()
        session.refresh(db_team)
        
        return db_team
        
        
@app.get("/teams/", response_model=List[TeamRead])
def read_teams(*, session: Session = Depends(get_sesion)):
    with Session(engine) as session:
        teams = session.exec(select(Team)).all()
        
        if not teams:
            raise HTTPException(status_code=404, detail="No Data")
        
        return teams
    
@app.get("/teams/{team_id}", response_model=TeamRead)
def read_team(*, session: Session = Depends(get_sesion), team_id: int):
    with Session(engine) as session:
        teams  = session.get(Team, team_id)
        
        if not teams:
            raise HTTPException(status_code=404, detail="Team Not Found")
        
        return teams
    
    
@app.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(*, session: Session = Depends(get_sesion), team_id: int, team: TeamUpdate):
    with Session(engine) as session:
        db_team = session.get(Team, team_id)
        
        if not db_team:
            raise HTTPException(status_code=404, detail="Team Not Found")
    
        team_data = team.dict(exclude_unset=True)
        
        for key,value in team_data.items():
            setattr (db_team, key, value)
            
        session.add(db_team)
        session.commit()
        session.refresh(db_team)
        
        return db_team
    
    
@app.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(get_sesion), team_id: int):
    with Session(engine) as session:
        db_team = session.get(Team, team_id)
        
        if not db_team:
            raise HTTPException(status_code=404, detail="Team Not Found")
        
        session.delete(db_team)
        session.commit()
        
        return {"Deleted": True}
