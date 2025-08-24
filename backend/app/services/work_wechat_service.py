import redis
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config import Config

class WorkWeChatService:
    """企业微信服务"""
    
    def __init__(self):
        self.corpid = Config.WORK_WECHAT_CORP_ID
        self.corpsecret = Config.WORK_WECHAT_CORP_SECRET  
        self.agentid = Config.WORK_WECHAT_AGENT_ID
        self.redis_client = redis.from_url(Config.REDIS_URL)
        self._access_token = None
        self._token_expires_at = None
        
    def get_access_token(self) -> str:
        """获取企业微信access_token"""
        if self._access_token and self._token_expires_at and datetime.now() < self._token_expires_at:
            return self._access_token
            
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('errcode') == 0:
                self._access_token = data['access_token']
                self._token_expires_at = datetime.now() + timedelta(seconds=data['expires_in'] - 300)
                return self._access_token
            else:
                print(f"获取access_token失败: {data}")
                return None
                
        except Exception as e:
            print(f"请求access_token异常: {e}")
            return None
    
    def send_text_message(self, userid: str, content: str) -> bool:
        """发送文本消息给指定用户"""
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        
        data = {
            "touser": userid,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": content
            }
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                return True
            else:
                print(f"发送消息失败: {result}")
                return False
                
        except Exception as e:
            print(f"发送消息异常: {e}")
            return False
    
    def send_markdown_message(self, userid: str, content: str) -> bool:
        """发送markdown格式消息"""
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        
        data = {
            "touser": userid,
            "msgtype": "markdown",
            "agentid": self.agentid,
            "markdown": {
                "content": content
            }
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                return True
            else:
                print(f"发送markdown消息失败: {result}")
                return False
                
        except Exception as e:
            print(f"发送markdown消息异常: {e}")
            return False
    
    def send_card_message(self, userid: str, title: str, description: str, url: str = "") -> bool:
        """发送卡片消息"""
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        card_content = f"""
# {title}

{description}

[点击查看详情]({url})
        """ if url else f"""
# {title}

{description}
        """
        
        return self.send_markdown_message(userid, card_content.strip())
    
    def get_user_session(self, userid: str) -> Dict:
        """获取用户会话信息"""
        session_key = f"work_wechat:session:{userid}"
        session_data = self.redis_client.get(session_key)
        
        if session_data:
            return json.loads(session_data)
        
        # 创建新会话
        session = {
            'userid': userid,
            'status': 'idle',  # idle, consulting, answering
            'current_question': 0,
            'answers': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.save_user_session(userid, session)
        return session
    
    def save_user_session(self, userid: str, session: Dict):
        """保存用户会话信息"""
        session['updated_at'] = datetime.now().isoformat()
        session_key = f"work_wechat:session:{userid}"
        
        # 设置过期时间为1小时
        self.redis_client.setex(
            session_key, 
            Config.SESSION_TIMEOUT, 
            json.dumps(session, ensure_ascii=False)
        )
    
    def clear_user_session(self, userid: str):
        """清除用户会话"""
        session_key = f"work_wechat:session:{userid}"
        self.redis_client.delete(session_key)
    
    def get_user_info(self, userid: str) -> Dict:
        """获取用户基本信息"""
        access_token = self.get_access_token()
        if not access_token:
            return {'userid': userid, 'name': '用户'}
            
        url = f"https://qyapi.weixin.qq.com/cgi-bin/user/get"
        params = {
            'access_token': access_token,
            'userid': userid
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('errcode') == 0:
                return {
                    'userid': data['userid'],
                    'name': data.get('name', '用户'),
                    'department': data.get('department', []),
                    'position': data.get('position', ''),
                    'mobile': data.get('mobile', ''),
                    'email': data.get('email', '')
                }
            else:
                print(f"获取用户信息失败: {data}")
                return {'userid': userid, 'name': '用户'}
                
        except Exception as e:
            print(f"获取用户信息异常: {e}")
            return {'userid': userid, 'name': '用户'}