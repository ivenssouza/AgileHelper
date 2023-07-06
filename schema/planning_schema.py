from ninja import Schema, ModelSchema
from datetime import date
from planning.models import Planning, PlanningParticipant, PokerRound, Vote
from typing import List, Optional
from uuid import UUID
from pydantic import Field


#RETURN SCHEMAS
class PlanningSchema(ModelSchema):
    class Config:
        model = Planning
        model_fields = "__all__"

class PlanningParticipantSchema(ModelSchema):
    class Config:
        model = PlanningParticipant
        model_fields = "__all__"

class PokerRoundSchema(ModelSchema):
    class Config:
        model = PokerRound
        model_fields = "__all__"

class VoteSchema(ModelSchema):
    class Config:
        model = Vote
        model_fields = "__all__"

class PlanningPokerRoundsSchema(Schema):
    id: UUID
    sprint_id: UUID
    description: str
    date: date
    poker_round: Optional[List[PokerRoundSchema]]

class PokerRoundVotesSchema(Schema):
    id: UUID
    planning_id: UUID
    story_id: UUID
    votes: Optional[List[VoteSchema]]

class PokerRoundFullSchema(Schema):
    id: UUID
    story_id: UUID
    open: bool
    votes: Optional[List[VoteSchema]]

class PlanningFullSchema(Schema):
    id: UUID
    description: str
    date: date
    poker_rounds: Optional[List[PokerRoundFullSchema]]
    

#IN SCHEMAS (USED FOR POST ENDPOINT)
class PlanningInSchema(ModelSchema):
    class Config:
        model = Planning
        model_exclude = ['id','date']

class PokerRoundInSchema(ModelSchema):
    class Config:
        model = PokerRound
        model_exclude = ['id', 'avg_points']

class VoteInSchema(ModelSchema):
    class Config:
        model = Vote
        model_exclude = ['id', 'participant']


#GET QUERY SCHEMAS
class GetPlanningSchema(Schema):
    sprint: Optional[UUID]

class GetPokerRoundSchema(Schema):
    planning: Optional[UUID]
    story: Optional[UUID]

class GetVoteSchema(Schema):
    poker_round: Optional[UUID]
    #participant: Optional[UUID]
