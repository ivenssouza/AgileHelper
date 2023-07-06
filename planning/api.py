from ninja import Path, Query, Router

from schema.planning_schema import PlanningSchema, PlanningInSchema, GetPlanningSchema, PlanningFullSchema
from schema.planning_schema import PokerRoundSchema, PokerRoundInSchema, GetPokerRoundSchema, PokerRoundVotesSchema
from schema.planning_schema import VoteSchema, VoteInSchema, GetVoteSchema
from schema.planning_schema import PlanningParticipantSchema

from sprint.models import Sprint, Story
from planning.models import Planning, PokerRound, Vote, PlanningParticipant
from schema.http_exceptions import HttpException, BadRequestHttpException, NotFoundHttpException, ConflictHttpException
from uuid import UUID
import math

planning_router = Router(tags=["Planning"])
poker_round_router = Router(tags=["Poker Round"])
vote_router = Router(tags=["Vote"])

#PLANNING

#FIXME NEED TO DO THE PARTICIPANT PART
@planning_router.post(path="",
    summary="Create a new Planning",
    description="Create a new Planning",
    response={201: PlanningSchema, 400: BadRequestHttpException, 409: ConflictHttpException, 500: HttpException},
)
def createPlanning(request, body:PlanningInSchema):
    try:
        if campo_vazio(str(body.sprint)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Sprint field is mandatory"
            )
        else:
            sprint = Sprint.objects.get(pk=body.sprint)
            
        if Planning.objects.filter(sprint=body.sprint).exists():
            return 409, ConflictHttpException(
                status = 409,
                message = "Planning already exists for Sprint" + str(body.sprint),
            ) 

        planning = Planning.objects.create(sprint=sprint, description=body.description)

        sprint.planning_id = planning.id
        sprint.save()
        
        return 201, planning
    
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

@planning_router.get(path="",
    summary="GET all existing Plannings",
    description="GET all existing Plannings. You can GET the Planning for a given Sprint (?sprint_id).",
    response={200: list[PlanningSchema], 500: HttpException},
)
def getPlanning(request, query: GetPlanningSchema = Query(None)):
    try:
        if query.sprint:
            return Planning.objects.all().filter(sprint=query.sprint)
        
        return Planning.objects.all()
    
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )
    
@planning_router.get(path="/{planningId}",
    summary="GET a specific Planning by ID",
    description="GET a specific Planning by ID",
    response={200: PlanningSchema, 404: NotFoundHttpException, 500: HttpException},
)
def getPlanningById(request, planningId: UUID):
    try:
        return Planning.objects.get(pk=planningId)
    except Planning.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Planning matches the given ID."
            )

@planning_router.get(path="/{planningId}/poker_rounds",
    summary="GET all Poker Rounds from a specific Planning",
    description="GET all Poker Rounds from a specific Planning",
    response={200: PlanningFullSchema, 404: NotFoundHttpException, 500: HttpException},
)
def getPlanningPokerRounds(request, planningId: UUID):
    try:
        pkr_rnd = []
        planning = Planning.objects.get(pk=planningId)

        if planning.id:
            poker_rounds = PokerRound.objects.all().filter(planning=planning.id)

            for poker_round in poker_rounds:
                if poker_round.id:
                    poker_round.votes = Vote.objects.all().filter(poker_round=poker_round.id)
            
                pkr_rnd.append(poker_round)
            
            planning.poker_rounds = pkr_rnd

        return planning
    
    except Planning.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Planning matches the given ID."
            )
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )

#POKER ROUND
@poker_round_router.post(path="",
    summary="Create a new Poker Round",
    description="Create a new Poker Round",
    response={201: PokerRoundSchema, 400: BadRequestHttpException, 404: NotFoundHttpException, 409: ConflictHttpException, 500: HttpException},
)
def createPokerRound(request, body:PokerRoundInSchema):
    try:
        if campo_vazio(str(body.planning)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Planning field is mandatory"
            )
        else:
            planning = Planning.objects.get(pk=body.planning)
        
        if campo_vazio(str(body.story)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Story field is mandatory"
            )
        else:
            story = Story.objects.get(pk=body.story)
            
        if PokerRound.objects.filter(planning=body.planning).exists() and PokerRound.objects.filter(story=body.story).exists():
            return 409, ConflictHttpException(
                status = 409,
                message = "Poker Round already exists for Story " + str(body.story) + " on Planning " + str(body.planning),
            ) 

        poker_round = PokerRound.objects.create(planning=planning,story=story)
        return 201, poker_round
    
    except Planning.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Planning matches the given ID."
            )
    except Story.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Story matches the given ID."
            )
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e,
        )

@poker_round_router.get(path="",
    summary="GET all existing Poker Rounds",
    description="GET all existing Poker Rounds",
    response={200: list[PokerRoundSchema], 500: HttpException},
)
def getPokerRounds(request, query: GetPokerRoundSchema = Query(None)):
    try:
        if query.planning and not query.story:
            return PokerRound.objects.all().filter(planning=query.planning)

        if query.story and not query.planning:
            return PokerRound.objects.all().filter(story=query.story)
        
        if query.planning and query.story:
            return PokerRound.objects.all().filter(planning=query.planning).filter(story=query.story)
        
        return PokerRound.objects.all()
    
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )
    
@poker_round_router.get(path="/{pokerRoundId}",
    summary="GET a specific Poker Round by ID",
    description="GET a specific Poker Round by ID",
    response={200: PokerRoundSchema, 404: NotFoundHttpException, 500: HttpException},
)
def getPokerRoundById(request, pokerRoundId: UUID):
    try:
        return PokerRound.objects.get(pk=pokerRoundId)
    
    except PokerRound.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Poker Round matches the given ID."
            )

@poker_round_router.get(path="/{pokerRoundId}/votes",
    summary="GET all Votes from a specific Poker Round",
    description="GET all Votes from a specific Poker Round",
    response={200: PokerRoundVotesSchema, 404: NotFoundHttpException, 500: HttpException},
)
def getPokerRoundVotes(request, pokerRoundId: UUID):
    try:
        poker_round = PokerRound.objects.get(pk=pokerRoundId)

        if pokerRoundId:
            poker_round.votes = Vote.objects.all().filter(poker_round=pokerRoundId)

        return poker_round
    
    except PokerRound.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Planning matches the given ID."
            )
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )

@poker_round_router.put(path="/{pokerRoundId}/finish",
    summary="Finish Poker Round and cal AVG Story Point",
    description="Finish Poker Round and cal AVG Story Point",
    response={200: PokerRoundSchema, 400: BadRequestHttpException, 404: NotFoundHttpException, 500: HttpException},
)
def putFinishPokerRound(request, pokerRoundId: UUID):
    try:
        if pokerRoundId:
            votes = Vote.objects.all().filter(poker_round=pokerRoundId)
            sum_points = 0

            for vote in votes:
                sum_points = sum_points + vote.estimated_points

            avg_points = round_up(sum_points / votes.__len__())

        poker_round = PokerRound.objects.get(pk=pokerRoundId)
        poker_round.avg_points = avg_points
        poker_round.open = False
        poker_round.save()
        return poker_round
    
    except PokerRound.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Poker Round matches the given ID."
            )
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )


#VOTE

#FIXME NEED TO DO THE PARTICIPANT PART
@vote_router.post(path="",
    summary="Create a new Vote",
    description="Create a new Vote",
    response={201: VoteSchema, 400: BadRequestHttpException, 404: NotFoundHttpException, 409: ConflictHttpException, 500: HttpException},
)
def createVote(request, body:VoteInSchema):
    try:
        if campo_vazio(str(body.poker_round)):
            return 400, BadRequestHttpException(
                status = 400,
                message = "Poker Round field is mandatory"
            )
        else:
            poker_round = PokerRound.objects.get(pk=body.poker_round)
        
        #if campo_vazio(str(body.participant)):
        #    return 400, BadRequestHttpException(
        #        status = 400,
        #        message = "Story field is mandatory"
        #    )
        #else:
        #    participant = Participant.objects.get(pk=body.participant)
            
        #if Vote.objects.filter(poker_round=body.poker_round).exists(): #and Vote.objects.filter(participant=body.participant).exists():
        #    return 409, ConflictHttpException(
        #        status = 409,
        #        message = "Vote already exists for Participant USER_ID for this Poker Round " + str(body.poker_round),
        #    ) 

        vote = Vote.objects.create(poker_round=poker_round, estimated_points=body.estimated_points)
        return 201, vote
    
    except PokerRound.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Poker Round matches the given ID."
            )
    
    #except Participant.DoesNotExist:
    #    return 404, NotFoundHttpException(
    #            status = 404,
    #            message = "No Participant matches the given ID."
    #        )
    
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e,
        )

@vote_router.get(path="",
    summary="GET all existing Votes",
    description="GET all existing Votes",
    response={200: list[VoteSchema], 500: HttpException},
)
def getVotes(request, query: GetVoteSchema = Query(None)):
    try:
        if query.poker_round: #and not query.participant:
            return Vote.objects.all().filter(poker_round=query.poker_round)

        #if query.participant and not query.poker_round:
        #    return Vote.objects.all().filter(participant=query.participant)
        
        #if query.poker_round and query.participant:
        #    return Vote.objects.all().filter(poker_round=query.poker_round).filter(participant=query.participant)
        
        return Vote.objects.all()
    
    except Exception as e:
        return 500, HttpException(
            status= 500,
            message= e.message,
        )
    
@vote_router.get(path="/{voteId}",
    summary="GET a specific Vote by ID",
    description="GET a specific Vote by ID",
    response={200: VoteSchema, 404: NotFoundHttpException, 500: HttpException},
)
def getVoteById(request, voteId: UUID):
    try:
        return Vote.objects.get(pk=voteId)
    
    except Vote.DoesNotExist:
        return 404, NotFoundHttpException(
                status = 404,
                message = "No Vote matches the given ID."
            )


def campo_vazio(campo):
    return not campo.strip()

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
