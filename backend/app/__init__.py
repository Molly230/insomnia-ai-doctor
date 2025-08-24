from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    # 注册蓝图
    from app.api.consultation import consultation_bp
    from app.api.diagnosis import diagnosis_bp
    from app.api.prescription import prescription_bp
    from app.api.wechat import wechat_bp
    from app.api.work_wechat import work_wechat_bp
    
    app.register_blueprint(consultation_bp, url_prefix='/api/consultation')
    app.register_blueprint(diagnosis_bp, url_prefix='/api/diagnosis')
    app.register_blueprint(prescription_bp, url_prefix='/api/prescription')
    app.register_blueprint(wechat_bp, url_prefix='/api')
    app.register_blueprint(work_wechat_bp, url_prefix='/api')
    
    return app