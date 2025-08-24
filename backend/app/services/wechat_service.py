import redis
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMenu
from config import Config

class WeChatService:
    def __init__(self):
        self.client = WeChatClient(Config.WECHAT_APP_ID, Config.WECHAT_APP_SECRET)
        self.redis_client = redis.from_url(Config.REDIS_URL)
        
    def get_user_session(self, openid: str) -> Dict:
        """获取用户会话信息"""
        session_key = f"wechat:session:{openid}"
        session_data = self.redis_client.get(session_key)
        
        if session_data:
            return json.loads(session_data)
        
        # 创建新会话
        session = {
            'openid': openid,
            'status': 'idle',  # idle, consulting, answering
            'current_question': 0,
            'answers': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.save_user_session(openid, session)
        return session
    
    def save_user_session(self, openid: str, session: Dict):
        """保存用户会话信息"""
        session['updated_at'] = datetime.now().isoformat()
        session_key = f"wechat:session:{openid}"
        
        # 设置过期时间为1小时
        self.redis_client.setex(
            session_key, 
            Config.SESSION_TIMEOUT, 
            json.dumps(session, ensure_ascii=False)
        )
    
    def clear_user_session(self, openid: str):
        """清除用户会话"""
        session_key = f"wechat:session:{openid}"
        self.redis_client.delete(session_key)
    
    def get_user_info(self, openid: str) -> Dict:
        """获取用户基本信息"""
        try:
            user_info = self.client.user.get(openid)
            return {
                'openid': user_info['openid'],
                'nickname': user_info.get('nickname', '用户'),
                'avatar': user_info.get('headimgurl', ''),
                'subscribe_time': user_info.get('subscribe_time', 0)
            }
        except Exception as e:
            print(f"获取用户信息失败: {e}")
            return {
                'openid': openid,
                'nickname': '用户',
                'avatar': '',
                'subscribe_time': 0
            }
    
    def create_menu(self):
        """创建公众号菜单"""
        menu_data = {
            "button": [
                {
                    "type": "click",
                    "name": "开始问诊",
                    "key": "START_CONSULTATION"
                },
                {
                    "name": "中医服务",
                    "sub_button": [
                        {
                            "type": "click",
                            "name": "失眠咨询",
                            "key": "INSOMNIA_CONSULT"
                        },
                        {
                            "type": "click", 
                            "name": "我的报告",
                            "key": "MY_REPORT"
                        },
                        {
                            "type": "click",
                            "name": "中医知识",
                            "key": "TCM_KNOWLEDGE"
                        }
                    ]
                },
                {
                    "name": "帮助中心",
                    "sub_button": [
                        {
                            "type": "click",
                            "name": "使用说明",
                            "key": "HELP_GUIDE"
                        },
                        {
                            "type": "click",
                            "name": "联系医师",
                            "key": "CONTACT_DOCTOR"
                        }
                    ]
                }
            ]
        }
        
        try:
            menu_api = WeChatMenu(self.client)
            result = menu_api.create(menu_data)
            return result
        except Exception as e:
            print(f"创建菜单失败: {e}")
            return None
    
    def send_text_message(self, openid: str, content: str):
        """发送文本消息"""
        try:
            return self.client.message.send_text(openid, content)
        except Exception as e:
            print(f"发送消息失败: {e}")
            return None
    
    def send_template_message(self, openid: str, template_id: str, data: Dict):
        """发送模板消息"""
        try:
            return self.client.message.send_template(openid, template_id, data)
        except Exception as e:
            print(f"发送模板消息失败: {e}")
            return None