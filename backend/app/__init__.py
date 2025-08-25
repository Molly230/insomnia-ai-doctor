from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

# 初始化SQLAlchemy实例
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    # 初始化数据库
    db.init_app(app)
    
    # 创建数据库表（如果不存在）
    with app.app_context():
        # 导入所有模型
        from app.models import database_models
        from app.models.database_models import Doctor
        
        # 创建表
        db.create_all()
        
        # 插入初始医生数据（如果不存在）
        if Doctor.query.count() == 0:
            doctors = [
                Doctor(id=1, name='李中医', title='主任医师', 
                      specialty='中医内科、失眠专科', experience=25, 
                      status='在线', consultation_fee=50.00),
                Doctor(id=2, name='王教授', title='副主任医师', 
                      specialty='中医神志病、睡眠障碍', experience=18, 
                      status='在线', consultation_fee=80.00),
                Doctor(id=3, name='张医师', title='主治医师', 
                      specialty='中医养生、亚健康调理', experience=12, 
                      status='忙碌', consultation_fee=30.00)
            ]
            for doctor in doctors:
                db.session.add(doctor)
            db.session.commit()
    
    # 注册蓝图
    from app.api.consultation import consultation_bp
    from app.api.diagnosis import diagnosis_bp
    from app.api.prescription import prescription_bp
    from app.api.chat import chat_bp
    from app.api.doctor_consultation import doctor_consultation_bp
    from app.api.admin import admin_bp
    # from app.api.wechat import wechat_bp
    # from app.api.work_wechat import work_wechat_bp
    
    app.register_blueprint(consultation_bp, url_prefix='/api/consultation')
    app.register_blueprint(diagnosis_bp, url_prefix='/api/diagnosis')
    app.register_blueprint(prescription_bp, url_prefix='/api/prescription')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(doctor_consultation_bp, url_prefix='/api/doctor-consultation')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    # app.register_blueprint(wechat_bp, url_prefix='/api')
    # app.register_blueprint(work_wechat_bp, url_prefix='/api')
    
    return app