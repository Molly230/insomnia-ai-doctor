from flask import Blueprint, request, jsonify
import xml.etree.ElementTree as ET
from app.services.work_wechat_service import WorkWeChatService
from app.services.tcm_ai_service import TCMAIService
from config import Config
import hashlib
import time

work_wechat_bp = Blueprint('work_wechat', __name__)

# 初始化服务
work_wechat_service = WorkWeChatService()
tcm_ai_service = TCMAIService()

@work_wechat_bp.route('/work_wechat', methods=['GET', 'POST'])
def work_wechat():
    """企业微信应用接口"""
    
    if request.method == 'GET':
        # 验证URL有效性
        return verify_url()
    else:
        # 处理企业微信消息
        return handle_work_wechat_message()

def verify_url():
    """验证企业微信URL"""
    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')
    
    print(f"企业微信URL验证:")
    print(f"msg_signature: {msg_signature}")
    print(f"timestamp: {timestamp}")
    print(f"nonce: {nonce}")
    print(f"echostr: {echostr}")
    
    # 验证签名
    if verify_signature(msg_signature, timestamp, nonce, echostr):
        print("✅ 企业微信URL验证成功")
        return echostr
    else:
        print("❌ 企业微信URL验证失败")
        return "fail"

def verify_signature(msg_signature, timestamp, nonce, echostr):
    """验证企业微信签名"""
    try:
        token = Config.WORK_WECHAT_TOKEN
        temp_list = [token, timestamp, nonce, echostr]
        temp_list.sort()
        temp_str = ''.join(temp_list)
        
        hash_str = hashlib.sha1(temp_str.encode('utf-8')).hexdigest()
        
        print(f"计算的签名: {hash_str}")
        print(f"企业微信签名: {msg_signature}")
        
        return hash_str == msg_signature
        
    except Exception as e:
        print(f"验证签名异常: {e}")
        return False

def handle_work_wechat_message():
    """处理企业微信消息"""
    try:
        # 解析XML消息
        xml_data = request.get_data()
        print(f"收到企业微信消息: {xml_data}")
        
        # 这里简化处理，实际需要解密
        root = ET.fromstring(xml_data)
        
        msg_type = root.find('MsgType').text
        from_user = root.find('FromUserName').text
        to_user = root.find('ToUserName').text
        
        if msg_type == 'text':
            content = root.find('Content').text
            return handle_text_message(from_user, content)
        elif msg_type == 'event':
            event = root.find('Event').text
            return handle_event_message(from_user, event)
        
        return build_text_reply(to_user, from_user, "暂不支持此类型消息")
        
    except Exception as e:
        print(f"处理消息异常: {e}")
        return "success"

def handle_text_message(userid, content):
    """处理文本消息"""
    try:
        # 获取用户会话
        session = work_wechat_service.get_user_session(userid)
        user_info = work_wechat_service.get_user_info(userid)
        username = user_info.get('name', '医生')
        
        reply_content = ""
        
        if session['status'] == 'idle':
            # 空闲状态，处理用户指令
            if content in ['开始问诊', '问诊', '失眠问诊']:
                reply_content = start_consultation(userid, session, username)
            elif content in ['帮助', '使用说明']:
                reply_content = tcm_ai_service.get_help_message()
            elif content in ['查看报告', '我的报告']:
                reply_content = get_user_report(userid, session)
            elif content in ['重新问诊']:
                reply_content = restart_consultation(userid, session, username)
            else:
                # 智能对话
                reply_content = tcm_ai_service.chat_with_user(content)
                
        elif session['status'] == 'consulting':
            # 问诊状态，等待用户确认开始
            if content in ['开始', '好的', '是的', '确定', 'ok']:
                reply_content = start_first_question(userid, session)
            else:
                reply_content = tcm_ai_service.get_consultation_start_message()
                
        elif session['status'] == 'answering':
            # 回答问题状态
            reply_content = handle_question_answer(userid, session, content)
            
        else:
            reply_content = tcm_ai_service.get_welcome_message(username)
        
        # 发送回复消息
        work_wechat_service.send_text_message(userid, reply_content)
        
        return "success"
        
    except Exception as e:
        print(f"处理文本消息异常: {e}")
        work_wechat_service.send_text_message(userid, "系统繁忙，请稍后重试")
        return "success"

def handle_event_message(userid, event):
    """处理事件消息"""
    try:
        user_info = work_wechat_service.get_user_info(userid)
        username = user_info.get('name', '医生')
        
        if event == 'subscribe' or event == 'enter_agent':
            # 用户进入应用
            reply_content = tcm_ai_service.get_welcome_message(username)
            work_wechat_service.send_text_message(userid, reply_content)
            
        return "success"
        
    except Exception as e:
        print(f"处理事件消息异常: {e}")
        return "success"

def start_consultation(userid: str, session: dict, username: str) -> str:
    """开始问诊流程"""
    session['status'] = 'consulting'
    session['current_question'] = 0
    session['answers'] = []
    
    work_wechat_service.save_user_session(userid, session)
    
    return f"""👨‍⚕️ {username}医生，欢迎使用失眠智能诊疗系统！

{tcm_ai_service.get_consultation_start_message()}"""

def start_first_question(userid: str, session: dict) -> str:
    """开始第一个问题"""
    session['status'] = 'answering'
    session['current_question'] = 0
    
    work_wechat_service.save_user_session(userid, session)
    
    return tcm_ai_service.get_question_message(0)

def handle_question_answer(userid: str, session: dict, user_input: str) -> str:
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
        return complete_consultation(userid, session)
    else:
        # 继续下一题
        session['current_question'] = current_question_index + 1
        work_wechat_service.save_user_session(userid, session)
        
        return tcm_ai_service.get_question_message(current_question_index + 1)

def complete_consultation(userid: str, session: dict) -> str:
    """完成问诊"""
    session['status'] = 'completed'
    work_wechat_service.save_user_session(userid, session)
    
    # TODO: 调用诊断分析逻辑
    # diagnosis_result = analyze_answers(session['answers'])
    
    completion_msg = tcm_ai_service.get_completion_message()
    
    # 发送完成消息后，再发送诊断结果
    diagnosis_result = {
        'syndrome_type': '待完善诊断逻辑',
        'confidence': 0.85
    }
    
    result_msg = tcm_ai_service.get_diagnosis_result_message(diagnosis_result)
    
    # 延迟发送诊断结果
    import threading
    def delayed_send():
        time.sleep(3)
        work_wechat_service.send_markdown_message(userid, result_msg)
    
    threading.Thread(target=delayed_send).start()
    
    return completion_msg

def get_user_report(userid: str, session: dict) -> str:
    """获取用户报告"""
    if session['status'] != 'completed':
        return "您还没有完成问诊，请先发送"开始问诊"完成评估。"
    
    # TODO: 生成详细报告
    diagnosis_result = {
        'syndrome_type': '待完善诊断逻辑',
        'confidence': 0.85
    }
    
    return tcm_ai_service.get_diagnosis_result_message(diagnosis_result)

def restart_consultation(userid: str, session: dict, username: str) -> str:
    """重新开始问诊"""
    work_wechat_service.clear_user_session(userid)
    new_session = work_wechat_service.get_user_session(userid)
    
    return start_consultation(userid, new_session, username)

def build_text_reply(to_user, from_user, content):
    """构建文本回复消息XML"""
    reply_xml = f"""
    <xml>
    <ToUserName><![CDATA[{from_user}]]></ToUserName>
    <FromUserName><![CDATA[{to_user}]]></FromUserName>
    <CreateTime>{int(time.time())}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    </xml>
    """
    return reply_xml.strip()

@work_wechat_bp.route('/work_wechat/send_test', methods=['POST'])
def send_test_message():
    """测试发送消息接口"""
    try:
        data = request.get_json()
        userid = data.get('userid', '')
        message = data.get('message', '测试消息')
        
        success = work_wechat_service.send_text_message(userid, message)
        
        return jsonify({
            'success': success,
            'message': '发送成功' if success else '发送失败'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500