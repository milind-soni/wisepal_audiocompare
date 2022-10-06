from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route('/main', methods=['POST', 'OPTIONS'])
def main():

    file = request.files['file']
    print(file)

    return {"ok": True}


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
