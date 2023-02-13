from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import *
from wxcloudrun.model import Counters
from wxcloudrun.model import UserChatInfo
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import openai
import config

# import azure.cognitiveservices.speech as speechsdk

model_engine = "text-davinci-003"


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


# @app.route('/api/text2audio', methods=['POST', 'GET'])
# def text2audio():
#     # 获取请求体参数
#     params = request.get_json()
#
#     speech_key = config.speech_key
#     service_region= config.service_region
#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#     speech_config.speech_synthesis_voice_name = "zh-CN-YunxiNeural"
#     speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
#     # 检查action参数
#     text = '梯形和正方形的区别？'
#     if 'prompt' in params:
#         text = params['text']
#     openai.api_key = config.chat_api_key
#     result = speech_synthesizer.speak_text_async(text).get()
#     return make_succ_response(result)


@app.route('/api/chat', methods=['POST', 'GET'])
def chat():
    # 获取请求体参数
    params = request.get_json()
    # 检查action参数
    prompt = '梯形和正方形的区别？'
    global_id = -1
    user_id = -1
    if 'prompt' in params:
        prompt = params['prompt']
    if 'global_id' in params:
        global_id = params['global_id']
    if 'user_id' in params:
        user_id = params['user_id']
    openai.api_key = config.chat_api_key
    creat_time = datetime.now()
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = completions.choices[0].text
    text = message.strip()
    finish_time = datetime.now()

    chat = query_chatbyid(global_id)
    if chat is None:
        chat = UserChatInfo()
        chat.dt = int(str(creat_time.date()).replace('-', ''))
        chat.user_id = user_id
        chat.global_id = global_id
        chat.creat_time = creat_time
        chat.finish_time = finish_time
        chat.duration_time = (finish_time - creat_time).seconds
        chat.question = prompt
        chat.answer = text
        chat.status = 1
        insert_chat(chat)
    else:
        chat.dt = int(str(creat_time.date()).replace('-', ''))
        chat.user_id = user_id
        chat.global_id = global_id
        chat.creat_time = creat_time
        chat.finish_time = finish_time
        chat.duration_time = (finish_time - creat_time).seconds
        chat.question = prompt
        chat.answer = text
        insert_chat(chat)
        chat.status = 1
        update_counterbyid(chat)

    return make_succ_response(text)


@app.route('/api/get_chat', methods=['POST', 'GET'])
def get_chat():
    params = request.get_json()
    global_id = 1
    if 'global_id' in params:
        global_id = params['global_id']
    chat = UserChatInfo.query.filter(UserChatInfo.global_id == global_id).first()
    return make_succ_response("查询失败") if chat is None else make_succ_response(chat.text)


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
