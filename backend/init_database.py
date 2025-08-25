#!/usr/bin/env python3
"""
数据库初始化脚本
创建SQLite数据库和表结构
"""
import sqlite3
import os
from datetime import datetime

def init_database(db_path="insomnia_diagnosis.db"):
    """初始化数据库"""
    print(f"正在初始化数据库: {db_path}")
    
    # 读取SQL脚本
    script_path = os.path.join(os.path.dirname(__file__), "database_schema.sql")
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 连接数据库并执行SQL
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 执行建表脚本
        cursor.executescript(sql_script)
        
        # 提交更改
        conn.commit()
        
        # 验证表是否创建成功
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("数据库初始化成功!")
        print("已创建的表:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # 检查医生数据
        cursor.execute("SELECT COUNT(*) FROM doctors")
        doctor_count = cursor.fetchone()[0]
        print(f"初始医生数量: {doctor_count}")
        
        conn.close()
        return True
        
    except FileNotFoundError:
        print(f"错误: 找不到SQL脚本文件 {script_path}")
        return False
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return False

def create_test_data(db_path="insomnia_diagnosis.db"):
    """创建一些测试数据"""
    print("\n正在创建测试数据...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建测试患者
        test_patients = [
            ("张三", "13800138001", 35, "男"),
            ("李四", "13800138002", 28, "女"),
            ("王五", "13800138003", 42, "男")
        ]
        
        for patient in test_patients:
            cursor.execute("""
                INSERT OR IGNORE INTO patients (name, phone, age, gender) 
                VALUES (?, ?, ?, ?)
            """, patient)
        
        # 创建一个测试诊断记录
        sample_answers = '''[
            {"question_id": 1, "selected_options": ["较差"]},
            {"question_id": 2, "selected_options": ["60分钟以上"]},
            {"question_id": 3, "selected_options": ["5小时以下"]},
            {"question_id": 10, "selected_options": ["是"]},
            {"question_id": 20, "selected_options": ["红舌少苔"]},
            {"question_id": 21, "selected_options": ["细数脉"]}
        ]'''
        
        sample_treatment = '''{"sleep_grade": "差", "syndrome_type": "气血两虚", "treatment_type": "专业医疗", "products": ["专业医生咨询"]}'''
        
        cursor.execute("""
            INSERT OR IGNORE INTO diagnosis_records 
            (patient_id, session_id, questionnaire_answers, total_sleep_score, 
             sleep_quality_grade, final_diagnosis, treatment_plan) 
            VALUES (1, 'test_session_001', ?, -25, '差', '气血两虚', ?)
        """, (sample_answers, sample_treatment))
        
        conn.commit()
        
        # 验证测试数据
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM diagnosis_records")
        diagnosis_count = cursor.fetchone()[0]
        
        print(f"测试数据创建成功!")
        print(f"测试患者数量: {patient_count}")
        print(f"测试诊断记录: {diagnosis_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"创建测试数据失败: {str(e)}")
        return False

def check_database_status(db_path="insomnia_diagnosis.db"):
    """检查数据库状态"""
    print(f"\n数据库状态检查: {db_path}")
    
    if not os.path.exists(db_path):
        print("数据库文件不存在")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查所有表的记录数
        tables = ['patients', 'diagnosis_records', 'chat_conversations', 
                 'doctor_consultations', 'doctors', 'consultation_messages']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   {table}: {count} 条记录")
            except sqlite3.OperationalError:
                print(f"   {table}: 表不存在")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"检查数据库状态失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 失眠诊疗系统数据库初始化 ===")
    
    # 数据库文件路径
    db_file = "insomnia_diagnosis.db"
    
    # 1. 初始化数据库
    if init_database(db_file):
        # 2. 创建测试数据
        create_test_data(db_file)
        
        # 3. 检查数据库状态
        check_database_status(db_file)
        
        print(f"\n数据库初始化完成! 数据库文件: {db_file}")
        print("提示: 现在可以启动Flask应用了")
    else:
        print("\n数据库初始化失败!")
        exit(1)