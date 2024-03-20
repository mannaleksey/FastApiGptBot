from schemas import RequestUser, UpdateData, Msg, MsgDB
from config import database
import uuid


class ChatAnswerRepo:

    @staticmethod
    async def retrieve_answer_id(id: str):
        return await database.get_collection('chat_answer').find_one({"_id": id})

    @staticmethod
    async def retrieve_delete_answer_id(id: str):
        await database.get_collection('chat_answer').delete_one({"_id": id})

    @staticmethod
    async def insert(msg: Msg):
        id = str(uuid.uuid4())
        _answer = {
            "_id": id,
            "user_id": msg.user_id,
            "request": msg.msg,
            "status": "pending",
            "answer": None,
        }
        await database.get_collection('chat_answer').insert_one(_answer)
        return id

    @staticmethod
    async def update(update_data: UpdateData, id: str):
        _date = await database.get_collection('chat_answer').find_one({"_id": id})
        _date["status"] = update_data.status
        _date["answer"] = update_data.answer
        await database.get_collection('chat_answer').update_one({"_id": id}, {"$set": _date})


class ChatRepo:

    @staticmethod
    async def retrieve():
        _msg = []
        collection = database.get_collection('chat').find()
        async for msgs in collection:
            _msg.append({'user_id': msgs['user_id'], 'messages': msgs['messages']})
        return _msg

    @staticmethod
    async def retrieve_user_id(user_id: str):
        _data = await database.get_collection('chat').find_one({"user_id": user_id})
        if _data:
            return {'user_id': user_id, 'messages': _data['messages']}
        else:
            return {'user_id': user_id, 'messages': []}

    @staticmethod
    async def add(msg_data: MsgDB):
        _date = await database.get_collection('chat').find_one({"user_id": msg_data.user_id})
        if _date:
            _messages = _date['messages']
            msg_data.messages = _messages + msg_data.messages
            await database.get_collection('chat').update_one({"user_id": msg_data.user_id}, {"$set": msg_data.dict()})
        else:
            await database.get_collection('chat').insert_one(msg_data.dict())

    @staticmethod
    async def delete(user_id: str):
        await database.get_collection('chat').delete_one({"user_id": user_id})


class AnswerRepo:

    @staticmethod
    async def retrieve():
        _answer = []
        collection = database.get_collection('answer').find()
        async for answer in collection:
            _answer.append(answer)
        return _answer

    @staticmethod
    async def insert(gpt: RequestUser):
        id = str(uuid.uuid4())
        _answer = {
            "_id": id,
            "user_id": gpt.user_id,
            "request": gpt.request,
            "status": "pending",
            "answer": None,
        }
        await database.get_collection('answer').insert_one(_answer)
        return id

    @staticmethod
    async def update(update_data: UpdateData, id: str):
        _date = await database.get_collection('answer').find_one({"_id": id})
        _date["status"] = update_data.status
        _date["answer"] = update_data.answer
        await database.get_collection('answer').update_one({"_id": id}, {"$set": _date})

    @staticmethod
    async def retrieve_id(id: str):
        return await database.get_collection('answer').find_one({"_id": id})

    @staticmethod
    async def delete(id: str):
        await database.get_collection('answer').delete_one({"_id": id})
