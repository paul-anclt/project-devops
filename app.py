"""simple website app for CI"""
import os
from flask import Flask, current_app
app = Flask(__name__)

@app.route('/')
def hello_world():
    """main route to return index.html"""
    return current_app.send_static_file('index.html')

if __name__ == '__main__':
    DEFAULT_PORT = 5000
    port = int(os.getenv('PORT',DEFAULT_PORT))
    app.run(debug=True,host='0.0.0.0', port=port)
