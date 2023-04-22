# -*- coding: utf-8 -*-
# @Time    : 2023/4/22 下午3:48
# @Author  : Su Yang
# @File    : app.py
# @Software: PyCharm 
# @Comment :


from flask import Flask, request, jsonify, make_response

from jarvis.agent import SearchAgent

app = Flask(__name__)

agents = {}


@app.route("/chat", methods=["POST"])
def chat():
    chat_id = request.form.get("chat_id")
    query = request.form.get("query")
    current_time = request.form.get("current_time")
    position = request.form.get("position")
    if chat_id == '':
        agent = SearchAgent()
        chat_id = agent.id
        agents[chat_id] = agent
    else:
        agent = agents.get(chat_id, None)
        if agent is None:
            response = make_response(jsonify({
                'error': 'Invalid chat id'
            }))
            response.status_code = 404
            return response

    response = make_response(jsonify({
        'chat_id': chat_id,
        'content': f'{agent.search(query, current_time=current_time, position=position)}',
    }))
    response.status_code = 200
    return response


@app.route('/del_chat', methods=['POST'])
def del_chat():
    chat_id = request.form.get("chat_id")
    try:
        agents.pop(chat_id)
        response = make_response(jsonify({
            'chat_id': chat_id
        }))
        response.status_code = 200
        return response
    except KeyError as error:
        response = make_response(jsonify({
            'error': error
        }))
        response.status_code = 404
        return response


if __name__ == '__main__':
    app.run(port=8000)
