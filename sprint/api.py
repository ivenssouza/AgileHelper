from ninja import Path, Query, Router
from schema.sprint_schema import SprintInSchema, SprintSchema, GetSprintSchema, SprintStoriesSchema, StorySchema, StoryInSchema, GetStorySchema, StoryPointInSchema, SprintFullSchema
from sprint.models import Sprint, Story
from planning.models import Planning, PokerRound, Vote
from schema.http_exceptions import HttpException, BadRequestHttpException, NotFoundHttpException, ConflictHttpException
from uuid import UUID

sprint_router = Router(tags=["Sprint"])
story_router = Router(tags=["Story"])

@sprint_router.post(path="", summary="Create a new Sprint", description="Create a new Sprint", response={201: SprintSchema, 400: BadRequestHttpException, 409: ConflictHttpException, 500: HttpException},)
def createSprint(request, body:SprintInSchema):
    try:
        if campo_vazio(body.type):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Type field is mandatory"
            )
        
        if campo_vazio(str(body.number)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Number field is mandatory"
            )

            
        if Sprint.objects.filter(type=body.type).exists() and Sprint.objects.filter(number=body.number).exists():
            return 409, ConflictHttpException(
                status = 409,
                message = "Sprint " + body.type+'-'+str(body.number) + " already exists.",
            ) 

        sprint = Sprint.objects.create(type=body.type,number=body.number,title=body.type+'-'+str(body.number),description=body.description)
        return 201, sprint
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )

@sprint_router.get(path="", summary="GET all existing Sprints", description="GET all existing Sprints. You can GET the Sprints for a given Type (?type) or Number (?number)", response={200: list[SprintSchema], 500: HttpException},)
def getSprint(request, query: GetSprintSchema = Query(None)):
    try:
        if query.type and not query.number:
            return Sprint.objects.all().filter(type=query.type)

        if query.number and not query.type:
            return Sprint.objects.all().filter(number=query.number)
        
        if query.number and query.type:
            return Sprint.objects.all().filter(title=query.type + "-" + str(query.number))

        return Sprint.objects.all()
    
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )
    
@sprint_router.get(path="/{sprintId}", summary="GET a specific Sprint by ID", description="GET a specific Sprint by ID", response={200: SprintSchema, 404: NotFoundHttpException, 500: HttpException},)
def getSprintId(request, sprintId: UUID):
    try:
        return Sprint.objects.get(pk=sprintId)
    except Sprint.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Sprint matches the given ID."
            )

@sprint_router.get(path="/{sprintId}/stories", summary="GET all Stories from a specific Sprint", description="GET all Stories from a specific Sprint", response={200: SprintStoriesSchema, 404: NotFoundHttpException, 500: HttpException},)
def getSprintStories(request, sprintId: UUID):
    try:
        sprint = Sprint.objects.get(pk=sprintId)

        if sprintId:
            sprint.stories = Story.objects.all().filter(sprint=sprintId)

        return sprint
    
    except Sprint.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Sprint matches the given ID."
            )
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )

@sprint_router.get(path="/{sprintId}/planning", summary="GET all Planning elements related to a specific Sprint", description="GET all Planning elements related to a specific Sprint", response={200: SprintFullSchema, 404: NotFoundHttpException, 500: HttpException},)
def getSprintFull(request, sprintId: UUID):
    try:
        pkr_rnd = []
        sprint = Sprint.objects.get(pk=sprintId)

        if sprintId:
            planning = Planning.objects.get(sprint=sprintId)

            if planning.id:
                poker_rounds = PokerRound.objects.all().filter(planning=planning.id)

                for poker_round in poker_rounds:
                    if poker_round.id:
                        poker_round.votes = Vote.objects.all().filter(poker_round=poker_round.id)
                
                    pkr_rnd.append(poker_round)
                
                planning.poker_rounds = pkr_rnd

        sprint.planning = planning

        return sprint
    
    except Sprint.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Sprint matches the given ID."
            )
    except Exception as e:
        return 500, e


#STORIES
@story_router.post(path="", summary="Create a new Story", description="Create a new Story", response={201: StorySchema, 400: BadRequestHttpException, 404: NotFoundHttpException, 409: ConflictHttpException, 500: HttpException},)
def createStory(request, body:StoryInSchema):
    try:
        if campo_vazio(str(body.sprint)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Sprint field is mandatory"
            )
        else:
            sprint = Sprint.objects.get(pk=body.sprint)
        
        if campo_vazio(str(body.ticket_number)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Ticket Number field is mandatory"
            )
            
        if Story.objects.filter(sprint=body.sprint).exists() and Story.objects.filter(ticket_number=body.ticket_number).exists():
            return 409, ConflictHttpException(
                status = 409,
                message = "Story " + str(body.ticket_number) + " already exists for " + body.sprint,
            ) 

        story = Story.objects.create(sprint=sprint,ticket_number=body.ticket_number,description=body.description)
        return 201, story
    except Sprint.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Sprint matches the given ID."
            )
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e,
        )

@story_router.get(path="", summary="GET all existing Stories", description="GET all existing Stories", response={200: list[StorySchema], 500: HttpException},)
def getStories(request, query: GetStorySchema = Query(None)):
    try:
        if query.sprint and not query.ticket_number:
            return Story.objects.all().filter(sprint=query.sprint)

        if query.ticket_number and not query.sprint:
            return Story.objects.all().filter(ticket_number=query.ticket_number)
        
        if query.sprint and query.ticket_number:
            return Story.objects.all().filter(sprint=query.sprint).filter(ticket_number=query.ticket_number)
        
        return Story.objects.all()
    
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )
    
@story_router.get(path="/{storyId}", summary="GET a specific Story by ID", description="GET a specific Story by ID", response={200: StorySchema, 404: NotFoundHttpException, 500: HttpException},)
def getStoryId(request, storyId: UUID):
    try:
        return Story.objects.get(pk=storyId)
    except Story.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Story matches the given ID."
            )

@story_router.put(path="/{storyId}", summary="Update Story Point", description="Update Story Point", response={200: StorySchema, 400: BadRequestHttpException, 404: NotFoundHttpException, 500: HttpException},)
def putStoryPoint(request, storyId: UUID, body:StoryPointInSchema):
    try:
        if campo_vazio(str(body.story_points)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Story Points field is mandatory"
            )
        
        story = Story.objects.get(pk=storyId)
        story.story_points = body.story_points
        story.save()
        return story
    
    except Story.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Story matches the given ID."
            )
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )




def campo_vazio(campo):
    return not campo.strip()