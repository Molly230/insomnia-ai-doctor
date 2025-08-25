from flask import Blueprint, request, jsonify
import uuid
import datetime
from typing import Dict, List

doctor_consultation_bp = Blueprint('doctor_consultation', __name__)

class DoctorConsultationService:
    """医生咨询服务"""
    
    # 模拟医生数据库
    DOCTORS = {
        1: {
            'id': 1,
            'name': '李中医',
            'title': '主任医师',
            'specialty': '中医内科、失眠专科',
            'experience': 25,
            'status': '在线',
            'price': 50,
            'avatar': '/doctor1.jpg',
            'introduction': '从事中医临床工作25年，擅长失眠、焦虑等神志病的中医诊疗',
            'qualifications': ['中医执业医师', '中医内科主任医师', '北京中医药学会会员']
        },
        2: {
            'id': 2,
            'name': '王教授',
            'title': '副主任医师',
            'specialty': '中医神志病、睡眠障碍',
            'experience': 18,
            'status': '在线',
            'price': 80,
            'avatar': '/doctor2.jpg',
            'introduction': '中医药大学教授，专注睡眠障碍研究18年',
            'qualifications': ['中医执业医师', '副主任医师', '中医药大学副教授']
        },
        3: {
            'id': 3,
            'name': '张医师',
            'title': '主治医师',
            'specialty': '中医养生、亚健康调理',
            'experience': 12,
            'status': '忙碌',
            'price': 30,
            'avatar': '/doctor3.jpg',
            'introduction': '专注中医养生和亚健康调理，注重预防保健',
            'qualifications': ['中医执业医师', '主治医师', '中医养生师']
        }
    }
    
    # 模拟咨询记录存储
    consultations = {}
    consultation_messages = {}
    
    @classmethod
    def get_all_doctors(cls) -> List[Dict]:
        """获取所有医生信息"""
        return list(cls.DOCTORS.values())
    
    @classmethod
    def get_doctor_by_id(cls, doctor_id: int) -> Dict:
        """根据ID获取医生信息"""
        return cls.DOCTORS.get(doctor_id)
    
    @classmethod
    def create_consultation(cls, consultation_data: Dict) -> Dict:
        """创建咨询会话"""
        consultation_id = str(uuid.uuid4())
        
        consultation = {
            'id': consultation_id,
            'doctor_id': consultation_data['doctor_id'],
            'patient_name': consultation_data['patient_name'],
            'age': consultation_data['age'],
            'gender': consultation_data['gender'],
            'phone': consultation_data['phone'],
            'symptoms': consultation_data['symptoms'],
            'duration': consultation_data['duration'],
            'medication_history': consultation_data.get('medication_history', ''),
            'diagnosis_data': consultation_data.get('diagnosis_data'),
            'status': 'active',
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        
        cls.consultations[consultation_id] = consultation
        cls.consultation_messages[consultation_id] = []
        
        # 添加医生欢迎消息
        doctor = cls.get_doctor_by_id(consultation_data['doctor_id'])
        if doctor:
            welcome_message = {
                'id': str(uuid.uuid4()),
                'consultation_id': consultation_id,
                'sender_type': 'doctor',
                'sender_name': doctor['name'],
                'content': f"您好 {consultation_data['patient_name']}，我是{doctor['name']}。我已经收到您的咨询申请，现在开始为您分析病情。请问您还有什么需要补充的症状吗？",
                'timestamp': datetime.datetime.now().isoformat(),
                'read_status': False
            }
            cls.consultation_messages[consultation_id].append(welcome_message)
        
        return consultation
    
    @classmethod
    def add_message(cls, consultation_id: str, message_data: Dict) -> Dict:
        """添加咨询消息"""
        if consultation_id not in cls.consultations:
            raise ValueError('咨询会话不存在')
        
        message = {
            'id': str(uuid.uuid4()),
            'consultation_id': consultation_id,
            'sender_type': message_data['sender_type'],  # 'patient' or 'doctor'
            'sender_name': message_data['sender_name'],
            'content': message_data['content'],
            'timestamp': datetime.datetime.now().isoformat(),
            'read_status': False
        }
        
        cls.consultation_messages[consultation_id].append(message)
        cls.consultations[consultation_id]['updated_at'] = datetime.datetime.now().isoformat()
        
        return message
    
    @classmethod
    def get_consultation_messages(cls, consultation_id: str) -> List[Dict]:
        """获取咨询消息记录"""
        return cls.consultation_messages.get(consultation_id, [])
    
    @classmethod
    def end_consultation(cls, consultation_id: str) -> bool:
        """结束咨询会话"""
        if consultation_id in cls.consultations:
            cls.consultations[consultation_id]['status'] = 'ended'
            cls.consultations[consultation_id]['ended_at'] = datetime.datetime.now().isoformat()
            return True
        return False
    
    @classmethod
    def generate_doctor_reply(cls, user_message: str, patient_info: Dict) -> str:
        """生成医生回复（基于规则和二元诊断结果的智能回复）"""
        user_message_lower = user_message.lower()
        
        # 如果有诊断数据，优先基于证型给出专业建议
        diagnosis_data = patient_info.get('diagnosis_data')
        if diagnosis_data and 'syndrome_type' in diagnosis_data:
            syndrome = diagnosis_data['syndrome_type']
            
            # 基于6种二元诊断证型确认诊断结果
            if '肝郁肾虚' in syndrome:
                return "我已经收到您的二元诊断结果：肝郁肾虚型，这是肝肠维度与骨髓维度的交叉证型。我会根据这个诊断结果为您制定专业的治疗方案。"
            
            elif '肝郁脑虚' in syndrome:
                return "根据您的诊断结果，证型为肝郁脑虚，属于肝肠与脑髓交叉的证型。我会结合您的具体症状进行详细分析。"
            
            elif '气血两虚' in syndrome:
                return "诊断显示为气血两虚型，是血液维度与骨髓维度的结合。我需要了解更多您的症状细节以制定治疗方案。"
                
            elif '气滞血瘀' in syndrome:
                return "您的证型是气滞血瘀，血液维度与脑髓维度交叉。请详细描述您的症状表现，我会据此调整治疗方案。"
                
            elif '精髓空虚' in syndrome:
                return "诊断为精髓空虚型，神内与骨髓维度的交叉证型。我会根据这个诊断为您制定相应的调理方案。"
                
            elif '神经衰弱' in syndrome:
                return "您的证型为神经衰弱，属于神内与脑髓的双重问题。我会综合您的整体情况进行专业分析。"
        
        # 如果没有诊断数据，基于症状关键词回复
        if any(keyword in user_message_lower for keyword in ['头痛', '头疼', '头晕']):
            return "根据您描述的头痛症状，这可能与失眠相互影响。中医认为'头为诸阳之会'，建议您按摩百会穴、太阳穴，同时注意颈椎保健。配合规律作息，症状会有所改善。"
        
        elif any(keyword in user_message_lower for keyword in ['心慌', '心悸', '胸闷']):
            return "心悸胸闷多与心神不安有关。建议您平时多做深呼吸，保持情绪稳定。可以尝试按摩神门穴、内关穴。如果症状持续，建议配合中药调理，如甘麦大枣汤。"
        
        elif any(keyword in user_message_lower for keyword in ['多梦', '噩梦', '梦多']):
            return "多梦是失眠的常见症状，中医认为多与心血不足、肝火旺盛有关。建议睡前用温水泡脚，按摩涌泉穴。饮食上可以多吃桂圆、红枣等养心血的食物。"
        
        elif any(keyword in user_message_lower for keyword in ['早醒', '醒得早', '凌晨醒']):
            return "早醒常见于肝郁化火或阴虚内热。建议您睡前避免过度思虑，可以听轻音乐放松。中药方面，可考虑柴胡疏肝散或知柏地黄丸，但需要面诊确定具体证型。"
        
        elif any(keyword in user_message_lower for keyword in ['入睡难', '入睡困难', '睡不着']):
            return "入睡困难多与肝气郁滞有关。建议您睡前1小时避免使用电子设备，可以做一些轻柔的拉伸运动。按摩神门穴、三阴交穴有助于安神入睡。"
        
        elif any(keyword in user_message_lower for keyword in ['压力大', '焦虑', '紧张', '工作压力']):
            return "压力和焦虑是失眠的重要诱因。中医讲'思虑伤脾'，建议您学会释放压力，可以通过冥想、瑜伽等方式放松。穴位方面，可以经常按摩印堂穴、太冲穴来疏肝解郁。"
        
        elif any(keyword in user_message_lower for keyword in ['药物', '安眠药', '吃药']):
            return "关于用药，建议您在医生指导下进行。中医强调辨证论治，不同的证型用药不同。西药安眠药只能短期使用，长期依赖会有副作用。中药相对温和，但也需要根据体质选择。"
        
        else:
            # 默认的专业回复
            replies = [
                "根据您的描述，建议您详细记录一下睡眠日记，包括入睡时间、醒来次数等，这有助于更准确的诊断。同时注意睡前避免刺激性食物和饮料。",
                "从中医角度看，失眠往往与脏腑功能失调有关。建议您保持规律作息，适当运动，注意情志调节。如果症状持续，建议面诊进行详细的望闻问切。",
                "您的情况需要综合调理。除了穴位按摩和中药治疗，生活方式的调整也很重要。建议您创造良好的睡眠环境，保持卧室安静、黑暗、凉爽。",
                "中医治疗失眠注重整体调理，不仅要治疗症状，更要调理体质。建议您平时多吃一些养心安神的食物，如百合、莲子、酸枣仁等。"
            ]
            return replies[abs(hash(user_message)) % len(replies)]

@doctor_consultation_bp.route('/doctors', methods=['GET'])
def get_doctors():
    """获取医生列表"""
    try:
        doctors = DoctorConsultationService.get_all_doctors()
        return jsonify({
            'success': True,
            'data': {
                'doctors': doctors,
                'total': len(doctors)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取医生列表失败: {str(e)}'
        }), 500

@doctor_consultation_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor_detail(doctor_id):
    """获取医生详细信息"""
    try:
        doctor = DoctorConsultationService.get_doctor_by_id(doctor_id)
        if not doctor:
            return jsonify({
                'success': False,
                'error': '医生不存在'
            }), 404
            
        return jsonify({
            'success': True,
            'data': doctor
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取医生信息失败: {str(e)}'
        }), 500

@doctor_consultation_bp.route('/consultations', methods=['POST'])
def create_consultation():
    """创建咨询会话"""
    try:
        data = request.get_json()
        
        required_fields = ['doctor_id', 'patient_name', 'age', 'gender', 'phone', 'symptoms', 'duration']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'缺少必要字段: {field}'
                }), 400
        
        # 验证医生是否存在
        doctor = DoctorConsultationService.get_doctor_by_id(data['doctor_id'])
        if not doctor:
            return jsonify({
                'success': False,
                'error': '指定的医生不存在'
            }), 404
        
        # 检查医生状态
        if doctor['status'] != '在线':
            return jsonify({
                'success': False,
                'error': '医生当前不在线，请选择其他医生'
            }), 400
        
        # 创建咨询会话
        consultation = DoctorConsultationService.create_consultation(data)
        
        return jsonify({
            'success': True,
            'data': {
                'consultation': consultation,
                'doctor': doctor
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建咨询失败: {str(e)}'
        }), 500

@doctor_consultation_bp.route('/consultations/<consultation_id>/messages', methods=['GET'])
def get_consultation_messages(consultation_id):
    """获取咨询消息"""
    try:
        messages = DoctorConsultationService.get_consultation_messages(consultation_id)
        return jsonify({
            'success': True,
            'data': {
                'messages': messages,
                'total': len(messages)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取消息失败: {str(e)}'
        }), 500

@doctor_consultation_bp.route('/consultations/<consultation_id>/messages', methods=['POST'])
def send_message(consultation_id):
    """发送咨询消息"""
    try:
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({
                'success': False,
                'error': '消息内容不能为空'
            }), 400
        
        # 添加患者消息
        message_data = {
            'sender_type': 'patient',
            'sender_name': data.get('sender_name', '患者'),
            'content': data['content']
        }
        
        patient_message = DoctorConsultationService.add_message(consultation_id, message_data)
        
        # 获取咨询信息用于生成医生回复
        consultation = DoctorConsultationService.consultations.get(consultation_id)
        if not consultation:
            return jsonify({
                'success': False,
                'error': '咨询会话不存在'
            }), 404
        
        # 生成医生回复
        doctor = DoctorConsultationService.get_doctor_by_id(consultation['doctor_id'])
        if doctor:
            doctor_reply = DoctorConsultationService.generate_doctor_reply(
                data['content'], 
                consultation
            )
            
            # 模拟医生回复延迟
            import time
            time.sleep(1)  # 1秒延迟模拟真实场景
            
            doctor_message_data = {
                'sender_type': 'doctor',
                'sender_name': doctor['name'],
                'content': doctor_reply
            }
            
            doctor_message = DoctorConsultationService.add_message(consultation_id, doctor_message_data)
            
            return jsonify({
                'success': True,
                'data': {
                    'patient_message': patient_message,
                    'doctor_message': doctor_message
                }
            })
        
        return jsonify({
            'success': True,
            'data': {
                'patient_message': patient_message
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'发送消息失败: {str(e)}'
        }), 500

@doctor_consultation_bp.route('/consultations/<consultation_id>/end', methods=['POST'])
def end_consultation(consultation_id):
    """结束咨询会话"""
    try:
        success = DoctorConsultationService.end_consultation(consultation_id)
        if success:
            return jsonify({
                'success': True,
                'message': '咨询已结束'
            })
        else:
            return jsonify({
                'success': False,
                'error': '咨询会话不存在'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'结束咨询失败: {str(e)}'
        }), 500

@doctor_consultation_bp.route('/consultations/<consultation_id>', methods=['GET'])
def get_consultation_detail(consultation_id):
    """获取咨询详情"""
    try:
        consultation = DoctorConsultationService.consultations.get(consultation_id)
        if not consultation:
            return jsonify({
                'success': False,
                'error': '咨询记录不存在'
            }), 404
        
        doctor = DoctorConsultationService.get_doctor_by_id(consultation['doctor_id'])
        messages = DoctorConsultationService.get_consultation_messages(consultation_id)
        
        return jsonify({
            'success': True,
            'data': {
                'consultation': consultation,
                'doctor': doctor,
                'messages': messages
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取咨询详情失败: {str(e)}'
        }), 500