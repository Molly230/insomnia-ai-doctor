"""
数据库模型定义
使用SQLAlchemy ORM定义数据表模型
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db
import json

class Patient(db.Model):
    """患者基本信息表"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    diagnosis_records = db.relationship('DiagnosisRecord', backref='patient', lazy=True)
    chat_conversations = db.relationship('ChatConversation', backref='patient', lazy=True)
    doctor_consultations = db.relationship('DoctorConsultation', backref='patient', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DiagnosisRecord(db.Model):
    """问卷诊断记录表"""
    __tablename__ = 'diagnosis_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    session_id = db.Column(db.String(100), unique=True)
    
    # 问卷答案(JSON格式存储)
    questionnaire_answers = db.Column(db.Text)  # JSON字符串
    
    # 评分结果
    total_sleep_score = db.Column(db.Integer)
    sleep_quality_grade = db.Column(db.String(10))  # 优/良/中/差
    sleep_score_percentage = db.Column(db.Float)
    
    # 证型诊断结果
    syndrome_scores = db.Column(db.Text)  # JSON字符串
    final_diagnosis = db.Column(db.String(50))
    binary_diagnosis_details = db.Column(db.Text)  # JSON字符串
    
    # 治疗方案
    treatment_plan = db.Column(db.Text)  # JSON字符串
    
    # 诊断时间
    diagnosed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    chat_conversations = db.relationship('ChatConversation', backref='diagnosis_record', lazy=True)
    doctor_consultations = db.relationship('DoctorConsultation', backref='diagnosis_record', lazy=True)
    
    def get_questionnaire_answers(self):
        """获取问卷答案（解析JSON）"""
        if self.questionnaire_answers:
            try:
                return json.loads(self.questionnaire_answers)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_questionnaire_answers(self, answers):
        """设置问卷答案（转换为JSON）"""
        self.questionnaire_answers = json.dumps(answers, ensure_ascii=False)
    
    def get_syndrome_scores(self):
        """获取证型得分（解析JSON）"""
        if self.syndrome_scores:
            try:
                return json.loads(self.syndrome_scores)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_syndrome_scores(self, scores):
        """设置证型得分（转换为JSON）"""
        self.syndrome_scores = json.dumps(scores, ensure_ascii=False)
    
    def get_binary_diagnosis_details(self):
        """获取二元诊断详情（解析JSON）"""
        if self.binary_diagnosis_details:
            try:
                return json.loads(self.binary_diagnosis_details)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_binary_diagnosis_details(self, details):
        """设置二元诊断详情（转换为JSON）"""
        self.binary_diagnosis_details = json.dumps(details, ensure_ascii=False)
    
    def get_treatment_plan(self):
        """获取治疗方案（解析JSON）"""
        if self.treatment_plan:
            try:
                return json.loads(self.treatment_plan)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_treatment_plan(self, plan):
        """设置治疗方案（转换为JSON）"""
        self.treatment_plan = json.dumps(plan, ensure_ascii=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'session_id': self.session_id,
            'questionnaire_answers': self.get_questionnaire_answers(),
            'total_sleep_score': self.total_sleep_score,
            'sleep_quality_grade': self.sleep_quality_grade,
            'sleep_score_percentage': self.sleep_score_percentage,
            'syndrome_scores': self.get_syndrome_scores(),
            'final_diagnosis': self.final_diagnosis,
            'binary_diagnosis_details': self.get_binary_diagnosis_details(),
            'treatment_plan': self.get_treatment_plan(),
            'diagnosed_at': self.diagnosed_at.isoformat() if self.diagnosed_at else None
        }

class ChatConversation(db.Model):
    """聊天对话记录表"""
    __tablename__ = 'chat_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    conversation_id = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    
    # 对话内容
    message_id = db.Column(db.String(100))
    role = db.Column(db.String(20))  # user/assistant/system
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    
    # 关联诊断记录
    diagnosis_record_id = db.Column(db.Integer, db.ForeignKey('diagnosis_records.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'message_id': self.message_id,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'diagnosis_record_id': self.diagnosis_record_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Doctor(db.Model):
    """医生基本信息表"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100))
    specialty = db.Column(db.String(200))
    experience = db.Column(db.Integer)
    status = db.Column(db.String(20), default='在线')  # 在线/忙碌/离线
    consultation_fee = db.Column(db.Numeric(10, 2))
    avatar_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    consultations = db.relationship('DoctorConsultation', backref='doctor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'specialty': self.specialty,
            'experience': self.experience,
            'status': self.status,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else 0,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DoctorConsultation(db.Model):
    """医生咨询记录表"""
    __tablename__ = 'doctor_consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    
    # 咨询基本信息
    consultation_id = db.Column(db.String(100), unique=True)
    patient_name = db.Column(db.String(50))
    patient_phone = db.Column(db.String(20))
    patient_age = db.Column(db.Integer)
    patient_gender = db.Column(db.String(10))
    
    # 症状描述
    symptoms = db.Column(db.Text)
    duration = db.Column(db.String(50))
    medication_history = db.Column(db.Text)
    
    # 关联诊断记录
    diagnosis_record_id = db.Column(db.Integer, db.ForeignKey('diagnosis_records.id'))
    include_diagnosis = db.Column(db.Boolean, default=False)
    
    # 咨询状态
    status = db.Column(db.String(20), default='pending')  # pending/active/completed/cancelled
    consultation_fee = db.Column(db.Numeric(10, 2))
    paid = db.Column(db.Boolean, default=False)
    
    # 时间记录
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    messages = db.relationship('ConsultationMessage', backref='consultation', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'consultation_id': self.consultation_id,
            'patient_name': self.patient_name,
            'patient_phone': self.patient_phone,
            'patient_age': self.patient_age,
            'patient_gender': self.patient_gender,
            'symptoms': self.symptoms,
            'duration': self.duration,
            'medication_history': self.medication_history,
            'diagnosis_record_id': self.diagnosis_record_id,
            'include_diagnosis': self.include_diagnosis,
            'status': self.status,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else 0,
            'paid': self.paid,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ConsultationMessage(db.Model):
    """医生咨询消息表"""
    __tablename__ = 'consultation_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.String(100), db.ForeignKey('doctor_consultations.consultation_id'))
    sender_type = db.Column(db.String(20))  # patient/doctor/system
    sender_name = db.Column(db.String(50))
    content = db.Column(db.Text)
    message_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'consultation_id': self.consultation_id,
            'sender_type': self.sender_type,
            'sender_name': self.sender_name,
            'content': self.content,
            'message_time': self.message_time.isoformat() if self.message_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }