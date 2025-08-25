#!/usr/bin/env python3
"""
启动带数据库的Flask应用
"""
from app import create_app, db
import os

def run_app():
    """启动应用"""
    app = create_app()
    
    # 确保数据库文件存在
    db_file = "insomnia_diagnosis.db"
    if not os.path.exists(db_file):
        print("数据库文件不存在，请先运行: python init_database.py")
        return
    
    with app.app_context():
        # 验证数据库连接
        try:
            # 导入模型以确保表结构存在
            from app.models.database_models import Patient, DiagnosisRecord, Doctor
            
            # 测试数据库连接
            patient_count = Patient.query.count()
            diagnosis_count = DiagnosisRecord.query.count()
            doctor_count = Doctor.query.count()
            
            print("=" * 50)
            print("失眠诊疗系统 - 数据库版本")
            print("=" * 50)
            print(f"数据库状态: 连接正常")
            print(f"患者记录: {patient_count} 条")
            print(f"诊断记录: {diagnosis_count} 条") 
            print(f"医生信息: {doctor_count} 条")
            print("=" * 50)
            print("启动Flask应用...")
            print("访问地址: http://localhost:5000")
            print("API文档: http://localhost:5000/api/")
            print("=" * 50)
            
        except Exception as e:
            print(f"数据库连接失败: {str(e)}")
            print("请检查数据库配置或重新初始化数据库")
            return
    
    # 启动应用
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_app()