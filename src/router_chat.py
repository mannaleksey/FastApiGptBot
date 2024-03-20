from fastapi import APIRouter, HTTPException
from starlette.background import BackgroundTasks

from repository import ChatRepo, ChatAnswerRepo
from schemas import Response, Msg
from tasks import gpt_msg_chat

router = APIRouter()


@router.post("/put_question")
async def chat_put_question(background_tasks: BackgroundTasks, request_user: Msg):
    id = await ChatAnswerRepo.insert(request_user)
    _msgList = await ChatRepo.retrieve_user_id(request_user.user_id)
    background_tasks.add_task(gpt_msg_chat, request_user, id, _msgList['messages'])
    return Response(code=200, status="Ok", message="Success send data to chat gpt", result=id).dict(exclude_none=True)


@router.get("/get_answer/{id}")
async def chat_get_answer(background_tasks: BackgroundTasks, id: str):
    _answer = await ChatAnswerRepo.retrieve_answer_id(id)
    if _answer:
        if _answer['status'] == 'pending':
            raise HTTPException(status_code=503, detail=Response(code=400, status="Ok", message="Success retrieve data").dict(exclude_none=True))
    else:
        raise HTTPException(status_code=506, detail=Response(code=506, status="Error", message="Dont have data in db").dict(exclude_none=True))
    background_tasks.add_task(ChatAnswerRepo.retrieve_delete_answer_id, id)
    return Response(code=200, status="Ok", message="Success retrieve data", result=_answer['answer']).dict(exclude_none=True)


@router.get("/")
async def chat_retrieve():
    _msgList = await ChatRepo.retrieve()
    return Response(code=200, status="Ok", message="Success retrieve all data", result=_msgList).dict(exclude_none=True)


@router.get("/{user_id}")
async def chat_retrieve_one(user_id: str):
    _msgList = await ChatRepo.retrieve_user_id(user_id)
    if _msgList:
        return Response(code=200, status="Ok", message="Success retrieve data", result=_msgList).dict(exclude_none=True)
    else:
        return Response(code=200, status="Ok", message="Success retrieve data", result=[]).dict(exclude_none=True)


@router.delete("/{user_id}")
async def chat_delete(user_id: str):
    await ChatRepo.delete(user_id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)


# @router.post("/chat/add")
# async def chat_add(request_user: Msg):
#     await ChatRepo.add(request_user)
#     return Response(code=200, status="Ok", message="Success send data to chat gpt").dict(exclude_none=True)