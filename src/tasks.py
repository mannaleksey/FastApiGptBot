import asyncio
from repository import AnswerRepo, ChatRepo, ChatAnswerRepo
from aiohttp import ClientSession

from schemas import Msg
from config import API_KEY

api_url_competition = 'https://api.openai.com/v1/chat/completions'
api_url_image = 'https://api.openai.com/v1/images/generations'


class Data:
    def dict(self):
        return self.__dict__


async def gpt_msg(msg, id: str):
    update_data = Data()
    try:
        update_data.status = 'success'
        messages = [
            {
                'role': 'user',
                'content': f'{msg}',
            },
        ]
        update_data.answer = str(await request_to_gpt_msg(messages))
    except:
        update_data.status = 'error'
        update_data.answer = 'Error'
    await AnswerRepo.update(update_data, id)


async def gpt_msg_chat(request_user: Msg, id: str, messages: list):
    update_data = Data()
    messages_data = Data()
    try:
        update_data.status = 'success'
        messages.append({
            'role': 'user',
            'content': f'{request_user.msg}'
        })
        update_data.answer = str(await request_to_gpt_msg(messages))
        new_messages = [
            {
                'role': 'user',
                'content': f'{request_user.msg}'
            },
            {
                'role': 'assistant',
                'content': f'{update_data.answer}'
            },
        ]
    except:
        update_data.status = 'error'
        update_data.answer = 'Error'
    await ChatAnswerRepo.update(update_data, id)
    if update_data.status == 'success':
        messages_data.user_id = request_user.user_id
        messages_data.messages = new_messages
        await ChatRepo.add(messages_data)


async def gpt_image(msg, size, id: str):
    update_data = Data()
    messages = [
        {
            'role': 'user',
            'content': f'{msg} переведи на английский',
        },
    ]
    try:
        translated_msg = await request_to_gpt_msg(messages)
        update_data.status = 'success'
        update_data.answer = str(await request_to_dalle_photo(translated_msg, size))
    except:
        update_data.status = 'error'
        update_data.answer = 'Error'
    await AnswerRepo.update(update_data, id)


async def request_to_gpt_msg(messages):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
    }
    for _ in range(3):
        try:
            async with ClientSession(headers=headers) as session:
                async with session.post(api_url_competition, json=json_data) as response:
                    response_json = await response.json()
            result = response_json['choices'][0]['message']['content']
            break
        except:
            pass
    # print(response_json['choices'][0]['message']['content'])
    return result


async def request_to_dalle_photo(msg, size):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }
    json_data = {
        'prompt': f'{msg}',
        'n': 1,
        'size': f'{size}',
    }
    for _ in range(3):
        try:
            async with ClientSession(headers=headers) as session:
                async with session.post(api_url_image, json=json_data) as response:
                    response_json = await response.json()
            result = response_json['data'][0]['url']
            break
        except:
            pass
    # print(response_json['data'][0]['url'])
    return result


# if __name__ == '__main__':
#     # request_to_gpt_msg('Напиши текст в блог на тему Машины. Используй Вдохновляющий стиль письма. Добавь немного смайлов по смыслу текста')
#     # asyncio.run(gpt_msg('test', '1052e25d-0ffb-4142-879c-b2ed37a77ad3'))
#     # asyncio.run(request_to_gpt_msg('Subject: Машина, Style: Ван гог, aspect ratio 3:4 переведи на английский'))
#     asyncio.run(request_to_dalle_photo('Subject: portrait close up of a Car, Style: hyper-realistic photograph, Camera: Canon EOS 5D Mark IV DSLR, Camera Settings: f/5.6 aperture, 1/125 second shutter speed, ISO 100, aspect ratio 2:3', '1024x1024'))
#     asyncio.run(request_to_dalle_photo('Subject: photo of Car, city in the background, Style: hyper-realistic photo, Camera: Canon EOS 5D Mark IV DSLR, the camera is 10 meters away from the object, aspect ratio 3:4', '1024x1024'))
