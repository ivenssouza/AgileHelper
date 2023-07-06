from ninja import NinjaAPI
#from users.api import router as users_router
from sprint.api import sprint_router,story_router 
from planning.api import planning_router, poker_round_router, vote_router
from participant.api import participant_router


api = NinjaAPI()

api.add_router("/sprints", sprint_router)
api.add_router("/stories", story_router)
api.add_router("/plannings", planning_router)
api.add_router("/participants", participant_router)
api.add_router("/poker_round", poker_round_router)
api.add_router("/votes", vote_router)

#api.add_router("/users/", users_router)