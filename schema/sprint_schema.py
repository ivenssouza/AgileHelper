from ninja import Schema, ModelSchema
from enum import Enum
from datetime import date
from sprint.models import Sprint, Story
from schema.planning_schema import PlanningFullSchema
from typing import List, Optional
from uuid import UUID
from pydantic import Field

class SprintTypeEnum(str, Enum):
    DEV = 'DEV'
    UX = 'UX'
    SW = 'SW'

#RETURN SCHEMAS
class SprintSchema(ModelSchema):
    class Config:
        model = Sprint
        model_fields = "__all__"

class StorySchema(ModelSchema):
    class Config:
        model = Story
        model_fields = "__all__"

class SprintStoriesSchema(Schema):
    id: UUID
    type: str
    number: int
    title: str
    description: str
    date: date
    stories: Optional[List[StorySchema]]

class SprintFullSchema(Schema):
    id: UUID
    type: str
    number: int
    title: str
    description: str
    date: date
    planning: Optional[PlanningFullSchema]


#IN SCHEMAS (USED FOR POST ENDPOINT)
class SprintInSchema(ModelSchema):
    class Config:
        model = Sprint
        model_exclude = ['id','date','title']

class StoryInSchema(ModelSchema):
    class Config:
        model = Story
        model_exclude = ['id', 'story_points']

class StoryPointInSchema(ModelSchema):
    class Config:
        model = Story
        model_fields = ['story_points']


#GET QUERY SCHEMAS
class GetSprintSchema(Schema):
    type: Optional[SprintTypeEnum] = Field()
    number: Optional[int] = Field()

class GetStorySchema(Schema):
    sprint: Optional[UUID]
    ticket_number: Optional[int]
