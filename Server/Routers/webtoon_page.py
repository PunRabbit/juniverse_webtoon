from fastapi import APIRouter, Depends
from starlette import status
from Server.Routers.Class.Get.get_class import HistoryGet
from Server.Routers.Class.Post.post_class import HistoryPost


# tags, dependencies 추후에 추가할 것
def create_router():
    new_router = APIRouter(
        prefix="/history",
        tags=["history"],
        # dependencies=[Depends(None)],
        responses={404: {"Critical": "Not Found"}}
    )

    return new_router


router = create_router()


@router.get("/")
async def history_search(response: HistoryGet = Depends()):
    """
    Create Your Own Information
    :param response: You have to follow his page's return value
    :return: It will return str "hi"
    """
    return "hi"


@router.post("/")
async def history_detail_search(response: HistoryPost):
    return "hi2"


@router.get("/{item_id}", tags=["custom"], status_code=status.HTTP_201_CREATED, description="item name")
async def history_test(item_id: str):
    return item_id


@router.post("/{item_id}", tags=["custom"], responses={400: {"Critical": "Open Browser"}})
async def history_test(item_id: str):
    return item_id

