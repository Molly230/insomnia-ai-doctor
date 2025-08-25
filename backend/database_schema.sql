-- 失眠诊疗系统数据库表结构设计
-- SQLite数据库

-- 1. 患者基本信息表
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50),
    phone VARCHAR(20),
    age INTEGER,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 问卷诊断记录表
CREATE TABLE IF NOT EXISTS diagnosis_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    session_id VARCHAR(100) UNIQUE,  -- 前端会话ID
    
    -- 问卷答案(JSON格式存储)
    questionnaire_answers TEXT,  -- JSON字符串，存储所有21道题的答案
    
    -- 评分结果
    total_sleep_score INTEGER,
    sleep_quality_grade VARCHAR(10),  -- 优/良/中/差
    sleep_score_percentage REAL,
    
    -- 证型诊断结果
    syndrome_scores TEXT,  -- JSON字符串，存储各证型得分
    final_diagnosis VARCHAR(50),  -- 最终证型诊断
    binary_diagnosis_details TEXT,  -- JSON字符串，存储二元诊断详情
    
    -- 治疗方案
    treatment_plan TEXT,  -- JSON字符串，存储治疗方案
    
    -- 诊断时间
    diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- 3. 聊天对话记录表
CREATE TABLE IF NOT EXISTS chat_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    conversation_id VARCHAR(100),
    user_id VARCHAR(100),
    
    -- 对话内容
    message_id VARCHAR(100),
    role VARCHAR(20),  -- user/assistant/system
    content TEXT,
    timestamp TIMESTAMP,
    
    -- 关联诊断记录
    diagnosis_record_id INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (diagnosis_record_id) REFERENCES diagnosis_records(id)
);

-- 4. 医生咨询记录表
CREATE TABLE IF NOT EXISTS doctor_consultations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    
    -- 咨询基本信息
    consultation_id VARCHAR(100) UNIQUE,
    patient_name VARCHAR(50),
    patient_phone VARCHAR(20),
    patient_age INTEGER,
    patient_gender VARCHAR(10),
    
    -- 症状描述
    symptoms TEXT,
    duration VARCHAR(50),
    medication_history TEXT,
    
    -- 关联诊断记录
    diagnosis_record_id INTEGER,
    include_diagnosis BOOLEAN DEFAULT 0,
    
    -- 咨询状态
    status VARCHAR(20) DEFAULT 'pending',  -- pending/active/completed/cancelled
    consultation_fee DECIMAL(10,2),
    paid BOOLEAN DEFAULT 0,
    
    -- 时间记录
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (diagnosis_record_id) REFERENCES diagnosis_records(id)
);

-- 5. 医生基本信息表
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    title VARCHAR(100),
    specialty VARCHAR(200),
    experience INTEGER,
    status VARCHAR(20) DEFAULT '在线',  -- 在线/忙碌/离线
    consultation_fee DECIMAL(10,2),
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 医生咨询消息表
CREATE TABLE IF NOT EXISTS consultation_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultation_id VARCHAR(100),
    sender_type VARCHAR(20),  -- patient/doctor/system
    sender_name VARCHAR(50),
    content TEXT,
    message_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (consultation_id) REFERENCES doctor_consultations(consultation_id)
);

-- 创建索引优化查询性能
CREATE INDEX IF NOT EXISTS idx_patients_phone ON patients(phone);
CREATE INDEX IF NOT EXISTS idx_diagnosis_records_patient_id ON diagnosis_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_diagnosis_records_session_id ON diagnosis_records(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_conversations_patient_id ON chat_conversations(patient_id);
CREATE INDEX IF NOT EXISTS idx_chat_conversations_conversation_id ON chat_conversations(conversation_id);
CREATE INDEX IF NOT EXISTS idx_doctor_consultations_patient_id ON doctor_consultations(patient_id);
CREATE INDEX IF NOT EXISTS idx_doctor_consultations_status ON doctor_consultations(status);
CREATE INDEX IF NOT EXISTS idx_consultation_messages_consultation_id ON consultation_messages(consultation_id);

-- 插入初始医生数据
INSERT OR IGNORE INTO doctors (id, name, title, specialty, experience, status, consultation_fee) VALUES 
(1, '李中医', '主任医师', '中医内科、失眠专科', 25, '在线', 50.00),
(2, '王教授', '副主任医师', '中医神志病、睡眠障碍', 18, '在线', 80.00),
(3, '张医师', '主治医师', '中医养生、亚健康调理', 12, '忙碌', 30.00);