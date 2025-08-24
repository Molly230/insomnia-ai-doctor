"""
简单的微信验证测试脚本
"""
from flask import Flask, request
import hashlib

app = Flask(__name__)

# 你的Token
TOKEN = "tcm2024insomnia"

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 获取微信参数
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        print(f"收到验证请求:")
        print(f"signature: {signature}")
        print(f"timestamp: {timestamp}")
        print(f"nonce: {nonce}")
        print(f"echostr: {echostr}")
        print(f"token: {TOKEN}")
        
        # 手动验证签名
        tmp_arr = [TOKEN, timestamp, nonce]
        tmp_arr.sort()
        tmp_str = ''.join(tmp_arr)
        hash_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
        
        print(f"计算的签名: {hash_str}")
        print(f"微信签名: {signature}")
        
        if hash_str == signature:
            print("验证成功!")
            return echostr
        else:
            print("验证失败!")
            return "fail"
    
    return "hello"

if __name__ == '__main__':
    app.run(debug=True, port=5000)