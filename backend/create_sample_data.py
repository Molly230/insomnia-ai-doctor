#!/usr/bin/env python3
"""
创建示例数据用于测试管理后台
"""
import requests
import json
import random
from datetime import datetime, timedelta

API_BASE = "http://localhost:5000/api"

# 示例患者数据
SAMPLE_PATIENTS = [
    {"name": "张三", "phone": "13800138001", "age": 35, "gender": "男"},
    {"name": "李四", "phone": "13800138002", "age": 28, "gender": "女"}, 
    {"name": "王五", "phone": "13800138003", "age": 42, "gender": "男"},
    {"name": "赵六", "phone": "13800138004", "age": 31, "gender": "女"},
    {"name": "钱七", "phone": "13800138005", "age": 38, "gender": "男"},
    {"name": "孙八", "phone": "13800138006", "age": 25, "gender": "女"},
    {"name": "周九", "phone": "13800138007", "age": 45, "gender": "男"},
    {"name": "吴十", "phone": "13800138008", "age": 33, "gender": "女"}
]

# 不同严重程度的问卷答案模板
ANSWER_TEMPLATES = {
    "优": [
        {"question_id": 1, "selected_options": ["好"]},
        {"question_id": 2, "selected_options": ["5分钟以内"]},
        {"question_id": 3, "selected_options": ["8小时及以上"]},
        {"question_id": 4, "selected_options": ["几乎不醒来"]},
        {"question_id": 5, "selected_options": ["5分钟以内"]},
        {"question_id": 6, "selected_options": ["几乎没有"]},
        {"question_id": 7, "selected_options": ["无"]},
        {"question_id": 8, "selected_options": ["无"]},
        {"question_id": 9, "selected_options": ["1个月以内"]},
        {"question_id": 10, "selected_options": ["否"]},
        {"question_id": 11, "selected_options": ["无"]},
        {"question_id": 12, "selected_options": ["否"]},
        {"question_id": 13, "selected_options": ["无"]},
        {"question_id": 14, "selected_options": ["否"]},
        {"question_id": 15, "selected_options": ["无"]},
        {"question_id": 16, "selected_options": ["否"]},
        {"question_id": 17, "selected_options": ["无"]},
        {"question_id": 18, "selected_options": ["否"]},
        {"question_id": 19, "selected_options": ["无"]},
        {"question_id": 20, "selected_options": ["淡红舌苔薄白"]},
        {"question_id": 21, "selected_options": ["沉细脉"]}
    ],
    
    "良": [
        {"question_id": 1, "selected_options": ["一般"]},
        {"question_id": 2, "selected_options": ["16-30分钟"]},
        {"question_id": 3, "selected_options": ["7-8小时"]},
        {"question_id": 4, "selected_options": ["1次"]},
        {"question_id": 5, "selected_options": ["6-15分钟"]},
        {"question_id": 6, "selected_options": ["每周1-2次"]},
        {"question_id": 7, "selected_options": ["晨起疲倦"]},
        {"question_id": 8, "selected_options": ["无"]},
        {"question_id": 9, "selected_options": ["1个月以内"]},
        {"question_id": 10, "selected_options": ["否"]},
        {"question_id": 11, "selected_options": ["无"]},
        {"question_id": 12, "selected_options": ["否"]},
        {"question_id": 13, "selected_options": ["无"]},
        {"question_id": 14, "selected_options": ["是"]},
        {"question_id": 15, "selected_options": ["无"]},
        {"question_id": 16, "selected_options": ["是"]},
        {"question_id": 17, "selected_options": ["无"]},
        {"question_id": 18, "selected_options": ["否"]},
        {"question_id": 19, "selected_options": ["无"]},
        {"question_id": 20, "selected_options": ["淡红舌苔薄白"]},
        {"question_id": 21, "selected_options": ["弱脉"]}
    ],
    
    "中": [
        {"question_id": 1, "selected_options": ["较差"]},
        {"question_id": 2, "selected_options": ["31-60分钟"]},
        {"question_id": 3, "selected_options": ["6-7小时"]},
        {"question_id": 4, "selected_options": ["2-3次"]},
        {"question_id": 5, "selected_options": ["16-30分钟"]},
        {"question_id": 6, "selected_options": ["每周3-5次"]},
        {"question_id": 7, "selected_options": ["反复清醒", "晨起疲倦"]},
        {"question_id": 8, "selected_options": ["无"]},
        {"question_id": 9, "selected_options": ["1-3个月（慢性）"]},
        {"question_id": 10, "selected_options": ["是"]},
        {"question_id": 11, "selected_options": ["腹胀/腹部不适"]},
        {"question_id": 12, "selected_options": ["是"]},
        {"question_id": 13, "selected_options": ["无"]},
        {"question_id": 14, "selected_options": ["是"]},
        {"question_id": 15, "selected_options": ["面色暗黑，无精打采"]},
        {"question_id": 16, "selected_options": ["是"]},
        {"question_id": 17, "selected_options": ["腰酸无力"]},
        {"question_id": 18, "selected_options": ["是"]},
        {"question_id": 19, "selected_options": ["好忘事，记忆力下降"]},
        {"question_id": 20, "selected_options": ["红舌少苔"]},
        {"question_id": 21, "selected_options": ["细脉"]}
    ],
    
    "差": [
        {"question_id": 1, "selected_options": ["较差"]},
        {"question_id": 2, "selected_options": ["60分钟以上"]},
        {"question_id": 3, "selected_options": ["5小时以下"]},
        {"question_id": 4, "selected_options": ["4次及以上"]},
        {"question_id": 5, "selected_options": ["60分钟以上"]},
        {"question_id": 6, "selected_options": ["每天都有"]},
        {"question_id": 7, "selected_options": ["反复清醒", "整夜做梦", "难以入眠"]},
        {"question_id": 8, "selected_options": ["苯二氮卓类：地西泮、劳拉西泮"]},
        {"question_id": 9, "selected_options": ["3个月以上（高级）"]},
        {"question_id": 10, "selected_options": ["是"]},
        {"question_id": 11, "selected_options": ["时有耳鸣", "腹胀/腹部不适"]},
        {"question_id": 12, "selected_options": ["是"]},
        {"question_id": 13, "selected_options": ["夜间憋醒/胸闷，心跳加速"]},
        {"question_id": 14, "selected_options": ["是"]},
        {"question_id": 15, "selected_options": ["面色暗黑，无精打采", "夜间盗汗"]},
        {"question_id": 16, "selected_options": ["是"]},
        {"question_id": 17, "selected_options": ["腰酸无力", "身寒怕冷", "夜尿频繁"]},
        {"question_id": 18, "selected_options": ["是"]},
        {"question_id": 19, "selected_options": ["好忘事，记忆力下降", "白天嗜睡"]},
        {"question_id": 20, "selected_options": ["红舌少津"]},
        {"question_id": 21, "selected_options": ["细数脉"]}
    ]
}

def create_sample_diagnosis(patient, grade_preference=None):
    """创建一个示例诊断"""
    
    # 如果没有指定等级偏好，随机选择
    if not grade_preference:
        grades = ["优", "良", "中", "差"]
        weights = [10, 30, 40, 20]  # 权重：优10%，良30%，中40%，差20%
        grade_preference = random.choices(grades, weights=weights)[0]
    
    # 获取对应等级的答案模板
    answers = ANSWER_TEMPLATES[grade_preference].copy()
    
    # 添加一些随机变化
    if random.random() < 0.3:  # 30%概率添加一些变化
        for answer in answers:
            if answer["question_id"] in [20, 21]:  # 舌象和脉象可以随机变化
                if answer["question_id"] == 20:
                    tongues = ["淡红舌苔薄白", "淡胖舌", "红舌少苔", "红舌少津", "淡胖舌苔白", "暗红舌或有瘀点"]
                    answer["selected_options"] = [random.choice(tongues)]
                elif answer["question_id"] == 21:
                    pulses = ["沉细脉", "弱脉", "细脉", "弦细脉", "细数脉", "沉迟脉", "弦脉"]
                    answer["selected_options"] = [random.choice(pulses)]
    
    # 构造诊断请求
    diagnosis_data = {
        "patient_info": patient,
        "session_id": f"session_{patient['phone']}_{int(datetime.now().timestamp())}",
        "answers": answers
    }
    
    return diagnosis_data

def submit_diagnosis(diagnosis_data):
    """提交诊断请求"""
    try:
        response = requests.post(
            f"{API_BASE}/diagnosis/analyze",
            json=diagnosis_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return True, result['data']
            else:
                return False, result.get('error', '未知错误')
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)

def create_multiple_samples():
    """创建多个示例数据"""
    print("开始创建示例诊断数据...")
    
    success_count = 0
    total_count = 0
    
    # 为每个患者创建1-3次诊断记录
    for patient in SAMPLE_PATIENTS:
        diagnosis_count = random.randint(1, 3)
        
        for i in range(diagnosis_count):
            total_count += 1
            
            # 生成诊断数据
            diagnosis_data = create_sample_diagnosis(patient)
            
            # 提交诊断
            success, result = submit_diagnosis(diagnosis_data)
            
            if success:
                success_count += 1
                print(f"✓ {patient['name']} 诊断记录 {i+1}: {result.get('sleep_quality', {}).get('grade', '未知')} - {result.get('syndrome_diagnosis', {}).get('final_diagnosis', '未知')}")
            else:
                print(f"✗ {patient['name']} 诊断记录 {i+1} 失败: {result}")
            
            # 稍微延迟避免请求过快
            import time
            time.sleep(0.5)
    
    print(f"\n创建完成！成功: {success_count}/{total_count}")
    return success_count, total_count

if __name__ == "__main__":
    print("=== 创建示例诊断数据 ===")
    print("注意: 请确保Flask应用正在运行 (http://localhost:5000)")
    
    try:
        # 测试API连接
        response = requests.get(f"{API_BASE}/admin/dashboard", timeout=5)
        if response.status_code == 200:
            print("✓ API连接正常")
        else:
            print(f"✗ API连接失败: {response.status_code}")
            exit(1)
    except Exception as e:
        print(f"✗ 无法连接到API: {e}")
        exit(1)
    
    # 创建示例数据
    success, total = create_multiple_samples()
    
    if success > 0:
        print(f"\n🎉 成功创建 {success} 条示例数据！")
        print("现在可以访问管理后台查看数据: http://localhost:3000/admin")
    else:
        print("\n❌ 没有成功创建任何数据，请检查API服务状态")