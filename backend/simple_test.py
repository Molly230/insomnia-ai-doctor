import requests
import json

# 配置信息
corpid = "wwb8026fb932028052"
corpsecret = "32H_eA3osvZxDCAhCoTaYIf50BSjN0Ydhb6CLpzFdIM"
agentid = 1000023

def test_simple():
    # 1. 获取access_token
    print("🔑 获取access_token...")
    token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    
    try:
        response = requests.get(token_url, timeout=10)
        result = response.json()
        
        if result.get('errcode') == 0:
            access_token = result['access_token']
            print(f"✅ 获取成功: {access_token[:20]}...")
            
            # 2. 获取部门用户列表
            print("\n👥 获取用户列表...")
            user_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token={access_token}&department_id=1"
            user_response = requests.get(user_url, timeout=10)
            user_result = user_response.json()
            
            print("用户列表:")
            if user_result.get('errcode') == 0:
                for user in user_result.get('userlist', []):
                    print(f"  - 用户ID: {user.get('userid')} | 姓名: {user.get('name')}")
            else:
                print(f"获取用户列表失败: {user_result}")
            
            # 3. 测试发送消息到所有找到的用户
            print(f"\n📨 测试发送消息...")
            if user_result.get('errcode') == 0 and user_result.get('userlist'):
                for user in user_result.get('userlist', []):
                    userid = user.get('userid')
                    name = user.get('name')
                    
                    msg_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
                    
                    data = {
                        "touser": userid,
                        "msgtype": "text",
                        "agentid": agentid,
                        "text": {
                            "content": f"🎉 测试消息\n\n你好 {name}！\n这是企业微信中医分身的测试消息。"
                        }
                    }
                    
                    msg_response = requests.post(msg_url, json=data, timeout=10)
                    msg_result = msg_response.json()
                    
                    if msg_result.get('errcode') == 0:
                        print(f"✅ 发送到 {name}({userid}) 成功")
                    else:
                        print(f"❌ 发送到 {name}({userid}) 失败: {msg_result}")
            else:
                print("没有找到可用的用户")
                
        else:
            print(f"❌ 获取access_token失败: {result}")
            
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == '__main__':
    test_simple()