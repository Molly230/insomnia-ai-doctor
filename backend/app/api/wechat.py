from flask import Blueprint, request, abort
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from config import Config
from app.services.wechat_service import WeChatService
from app.services.tcm_ai_service import TCMAIService

wechat_bp = Blueprint('wechat', __name__)

# 初始化服务
wechat_service = WeChatService()
tcm_ai_service = TCMAIService()

@wechat_bp.route('/wechat', methods=['GET', 'POST'])
def wechat():
    """微信公众号接口"""
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    
    # 调试信息
    print(f"收到微信验证请求:")
    print(f"signature: {signature}")
    print(f"timestamp: {timestamp}")
    print(f"nonce: {nonce}")
    print(f"echostr: {echo_str}")
    print(f"token: {Config.WECHAT_TOKEN}")
    
    try:
        check_signature(Config.WECHAT_TOKEN, signature, timestamp, nonce)
        print("Token验证成功")
    except InvalidSignatureException as e:
        print(f"Token验证失败: {e}")
        abort(403)
    except Exception as e:
        print(f"验证异常: {e}")
        abort(500)
    
    if request.method == 'GET':
        # 微信服务器验证
        print(f"返回echostr: {echo_str}")
        return echo_str
    
    # 处理微信消息
    msg = parse_message(request.get_data())
    
    if msg.type == 'text':
        return handle_text_message(msg)
    elif msg.type == 'event':
        return handle_event_message(msg)
    else:
        reply = create_reply('暂不支持此类型消息', msg)
        return reply.render()

def handle_text_message(msg):
    """处理文本消息"""
    openid = msg.source
    content = msg.content.strip()
    
    # 获取用户会话
    session = wechat_service.get_user_session(openid)
    user_info = wechat_service.get_user_info(openid)
    nickname = user_info.get('nickname', '朋友')
    
    reply_content = ""
    
    try:
        if session['status'] == 'idle':
            # 空闲状态，处理用户指令
            if content in ['开始', '开始问诊', 'START_CONSULTATION']:
                reply_content = start_consultation(openid, session)
            elif content in ['帮助', '使用说明', 'HELP_GUIDE']:
                reply_content = tcm_ai_service.get_help_message()
            elif content in ['查看报告', 'MY_REPORT']:
                reply_content = get_user_report(openid, session)
            elif content in ['重新问诊']:
                reply_content = restart_consultation(openid, session)
            else:
                # 智能对话
                reply_content = tcm_ai_service.chat_with_user(content)
                
        elif session['status'] == 'consulting':
            # 问诊状态，等待用户确认开始
            if content in ['开始', '好的', '是的', '确定']:
                reply_content = start_first_question(openid, session)
            else:
                reply_content = tcm_ai_service.get_consultation_start_message()
                
        elif session['status'] == 'answering':
            # 回答问题状态
            reply_content = handle_question_answer(openid, session, content)
            
        else:
            reply_content = tcm_ai_service.get_welcome_message(nickname)
            
    except Exception as e:
        print(f"处理消息异常: {e}")
        reply_content = tcm_ai_service.get_error_message("system_error")
    
    reply = create_reply(reply_content, msg)
    return reply.render()

def handle_event_message(msg):
    """处理事件消息"""
    openid = msg.source
    
    if msg.type == 'event':
        if msg.event == 'subscribe':
            # 用户关注事件
            user_info = wechat_service.get_user_info(openid)
            nickname = user_info.get('nickname', '朋友')
            reply_content = tcm_ai_service.get_welcome_message(nickname)
            
        elif msg.event == 'click':
            # 菜单点击事件
            key = msg.key
            session = wechat_service.get_user_session(openid)
            
            if key == 'START_CONSULTATION':
                reply_content = start_consultation(openid, session)
            elif key == 'INSOMNIA_CONSULT':
                reply_content = tcm_ai_service.chat_with_user("失眠咨询")
            elif key == 'MY_REPORT':
                reply_content = get_user_report(openid, session)
            elif key == 'TCM_KNOWLEDGE':
                reply_content = tcm_ai_service.chat_with_user("中医知识")
            elif key == 'HELP_GUIDE':
                reply_content = tcm_ai_service.get_help_message()
            elif key == 'CONTACT_DOCTOR':
                reply_content = "如需进一步咨询，请联系医师微信：[您的微信号]"
            else:
                reply_content = "功能开发中，敬请期待！"
        else:
            reply_content = "感谢您的关注！"
    else:
        reply_content = tcm_ai_service.get_welcome_message()
    
    reply = create_reply(reply_content, msg)
    return reply.render()

def start_consultation(openid: str, session: dict) -> str:
    """开始问诊流程"""
    session['status'] = 'consulting'
    session['current_question'] = 0
    session['answers'] = []
    
    wechat_service.save_user_session(openid, session)
    
    return tcm_ai_service.get_consultation_start_message()

def start_first_question(openid: str, session: dict) -> str:
    """开始第一个问题"""
    session['status'] = 'answering'
    session['current_question'] = 0
    
    wechat_service.save_user_session(openid, session)
    
    return tcm_ai_service.get_question_message(0)

def handle_question_answer(openid: str, session: dict, user_input: str) -> str:
    """处理问题回答"""
    current_question_index = session['current_question']
    
    # 解析用户答案
    selected_options = tcm_ai_service.parse_answer(user_input, current_question_index)
    
    if not selected_options:
        return tcm_ai_service.get_error_message("invalid_answer")
    
    # 保存答案
    session['answers'].append({
        'question_index': current_question_index,
        'selected_options': selected_options
    })
    
    # 检查是否所有问题都已回答
    if current_question_index >= Config.MAX_QUESTIONS - 1:
        # 问诊完成
        return complete_consultation(openid, session)
    else:
        # 继续下一题
        session['current_question'] = current_question_index + 1
        wechat_service.save_user_session(openid, session)
        
        return tcm_ai_service.get_question_message(current_question_index + 1)

def complete_consultation(openid: str, session: dict) -> str:
    """完成问诊"""
    session['status'] = 'completed'
    wechat_service.save_user_session(openid, session)
    
    # TODO: 调用诊断分析逻辑
    # diagnosis_result = analyze_answers(session['answers'])
    
    return tcm_ai_service.get_completion_message()

def get_user_report(openid: str, session: dict) -> str:
    """获取用户报告"""
    if session['status'] != 'completed':
        return "您还没有完成问诊，请先点击"开始问诊"完成评估。"
    
    # TODO: 生成详细报告
    diagnosis_result = {
        'syndrome_type': '待分析',
        'confidence': 0.85
    }
    
    return tcm_ai_service.get_diagnosis_result_message(diagnosis_result)

def restart_consultation(openid: str, session: dict) -> str:
    """重新开始问诊"""
    wechat_service.clear_user_session(openid)
    new_session = wechat_service.get_user_session(openid)
    
    return start_consultation(openid, new_session)

@wechat_bp.route('/wechat/menu/create', methods=['POST'])
def create_menu():
    """创建微信菜单"""
    try:
        result = wechat_service.create_menu()
        if result:
            return {'success': True, 'message': '菜单创建成功'}
        else:
            return {'success': False, 'message': '菜单创建失败'}, 500
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500