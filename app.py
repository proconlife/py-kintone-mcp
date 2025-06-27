from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from mcp.server.fastmcp import FastMCP

# .env ファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)
mcp = FastMCP()

@app.route('/')
def hello_world():
    return 'Hello, MCP Server!'

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    return mcp.handle_request(request.json)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)