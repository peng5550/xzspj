import flask, json
from flask import request

server = flask.Flask(__name__)

@server.route('/verify', methods=['GET', 'POST'])
def verifyCaptcha():
    if request.method == "POST":
        message = request.form.to_dict()
        if message:
            code = message.get("code", "")
            if code == "123456":
                return json.dumps({"status":True}, ensure_ascii=False)
        else:
            return json.dumps({"status": False}, ensure_ascii=False)

    if request.method == "GET":
        return json.dumps({"status": False}, ensure_ascii=False)

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8888)

