#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
import hashlib

app = Flask(__name__)

# 你的微信Token（必须与微信平台设置一致）
WECHAT_TOKEN = "tcmDoctor2024"

@app.route('/wechat', methods=['GET'])
def wechat_verify():
    """微信服务器验证"""
    
    # 获取微信发送的参数
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')
    
    print("=" * 50)
    print("微信验证请求参数:")
    print(f"signature: {signature}")
    print(f"timestamp: {timestamp}")
    print(f"nonce: {nonce}")
    print(f"echostr: {echostr}")
    print(f"本地token: {WECHAT_TOKEN}")
    
    # 验证签名
    if verify_signature(signature, timestamp, nonce):
        print("✅ 验证成功!")
        return echostr
    else:
        print("❌ 验证失败!")
        return "fail"

def verify_signature(signature, timestamp, nonce):
    """验证微信签名"""
    try:
        # 1. 将token、timestamp、nonce三个参数进行字典序排序
        temp_list = [WECHAT_TOKEN, timestamp, nonce]
        temp_list.sort()
        
        # 2. 将三个参数字符串拼接成一个字符串进行sha1加密
        temp_str = ''.join(temp_list)
        print(f"拼接字符串: {temp_str}")
        
        # 3. 加密后的字符串与signature对比
        hash_object = hashlib.sha1(temp_str.encode('utf-8'))
        hash_str = hash_object.hexdigest()
        
        print(f"计算签名: {hash_str}")
        print(f"微信签名: {signature}")
        
        return hash_str == signature
        
    except Exception as e:
        print(f"验证异常: {e}")
        return False

if __name__ == '__main__':
    print("🚀 启动微信验证服务...")
    print(f"📱 Token: {WECHAT_TOKEN}")
    print("🌐 验证地址: http://localhost:5000/wechat")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)