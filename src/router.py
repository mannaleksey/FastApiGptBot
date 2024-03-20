from fastapi import APIRouter, HTTPException
from starlette.background import BackgroundTasks

from repository import AnswerRepo
from schemas import RequestUser, UpdateData, Response
from tasks import gpt_msg, gpt_image

router = APIRouter()


@router.get("/")
async def get_all():
    _answerList = await AnswerRepo.retrieve()
    return Response(code=200, status="Ok", message="Success retrieve all data", result=_answerList).dict(exclude_none=True)


@router.post("/{msg_or_image}/create")
async def create(background_tasks: BackgroundTasks, request_user: RequestUser, msg_or_image: str):
    if msg_or_image in ['msg', 'image']:
        id = await AnswerRepo.insert(request_user)
        if msg_or_image == 'msg':
            background_tasks.add_task(gpt_msg, request_user.request, id)
        if msg_or_image == 'image':
            background_tasks.add_task(gpt_image, request_user.request, request_user.size, id)
        return Response(code=200, status="Ok", message="Success save data", result=id).dict(exclude_none=True)


@router.post("/update")
async def update(request_user: UpdateData):
    await AnswerRepo.update(request_user, request_user.id)
    return Response(code=200, status="Ok", message="Success update data").dict(exclude_none=True)


@router.get("/{id}")
async def get_id(background_tasks: BackgroundTasks, id: str):
    _answer = await AnswerRepo.retrieve_id(id)
    if _answer:
        if _answer['status'] == 'pending':
            raise HTTPException(status_code=503, detail=Response(code=400, status="Ok", message="Success retrieve data").dict(exclude_none=True))
    else:
        raise HTTPException(status_code=506, detail=Response(code=506, status="Error", message="Dont have data in db").dict(exclude_none=True))
    background_tasks.add_task(AnswerRepo.delete, id)
    return Response(code=200, status="Ok", message="Success retrieve data", result=_answer['answer']).dict(exclude_none=True)


@router.delete("/{id}")
async def delete(id: str):
    await AnswerRepo.delete(id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)
