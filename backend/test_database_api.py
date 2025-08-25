#!/usr/bin/env python3
"""
测试数据库API功能
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_diagnosis_api():
    """测试诊断API"""
    print("=== 测试诊断API ===")
    
    # 测试数据
    test_data = {
        "patient_info": {
            "name": "测试患者",
            "phone": "13800138888",
            "age": 30,
            "gender": "女"
        },
        "session_id": "test_session_2024",
        "answers": [
            {"question_id": 1, "selected_options": ["较差"]},
            {"question_id": 2, "selected_options": ["60分钟以上"]},
            {"question_id": 3, "selected_options": ["5小时以下"]},
            {"question_id": 4, "selected_options": ["4次及以上"]},
            {"question_id": 5, "selected_options": ["60分钟以上"]},
            {"question_id": 6, "selected_options": ["每天都有"]},
            {"question_id": 7, "selected_options": ["反复清醒", "整夜做梦"]},
            {"question_id": 8, "selected_options": ["苯二氮卓类：地西泮、劳拉西泮"]},
            {"question_id": 9, "selected_options": ["3个月以上（高级）"]},
            {"question_id": 10, "selected_options": ["是"]},
            {"question_id": 11, "selected_options": ["时有耳鸣"]},
            {"question_id": 12, "selected_options": ["是"]},
            {"question_id": 13, "selected_options": ["无"]},
            {"question_id": 14, "selected_options": ["是"]},
            {"question_id": 15, "selected_options": ["夜间盗汗"]},
            {"question_id": 16, "selected_options": ["是"]},
            {"question_id": 17, "selected_options": ["腰酸无力", "身寒怕冷"]},
            {"question_id": 18, "selected_options": ["是"]},
            {"question_id": 19, "selected_options": ["好忘事，记忆力下降"]},
            {"question_id": 20, "selected_options": ["红舌少苔"]},
            {"question_id": 21, "selected_options": ["细数脉"]}
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/diagnosis/analyze", 
                               json=test_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 诊断API测试成功!")
                data = result['data']
                print(f"  患者ID: {data.get('patient_id')}")
                print(f"  诊断记录ID: {data.get('diagnosis_record_id')}")
                print(f"  会话ID: {data.get('session_id')}")
                print(f"  睡眠质量等级: {data['sleep_quality']['grade']}")
                print(f"  总分: {data['sleep_quality']['total_score']}")
                print(f"  最终证型: {data['syndrome_diagnosis']['final_diagnosis']}")
                print(f"  治疗方案类型: {data['treatment_plan']['treatment_type']}")
                return data.get('session_id')
            else:
                print(f"✗ 诊断失败: {result.get('error')}")
        else:
            print(f"✗ HTTP错误: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
    
    return None

def test_history_api(session_id):
    """测试历史记录API"""
    print(f"\n=== 测试历史记录API ===")
    
    if not session_id:
        print("跳过历史记录测试 - 没有有效的session_id")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/diagnosis/history/{session_id}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 历史记录API测试成功!")
                data = result['data']
                print(f"  记录ID: {data.get('id')}")
                print(f"  睡眠等级: {data.get('sleep_quality_grade')}")
                print(f"  诊断时间: {data.get('diagnosed_at')}")
            else:
                print(f"✗ 获取历史记录失败: {result.get('error')}")
        else:
            print(f"✗ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")

def test_stats_api():
    """测试统计API"""
    print(f"\n=== 测试统计API ===")
    
    try:
        response = requests.get(f"{BASE_URL}/diagnosis/stats")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 统计API测试成功!")
                data = result['data']
                print(f"  总诊断次数: {data.get('total_diagnosis')}")
                print(f"  今日诊断: {data.get('today_diagnosis')}")
                print("  睡眠质量分布:")
                for item in data.get('sleep_grade_distribution', []):
                    print(f"    {item['grade']}: {item['count']}人")
                print("  证型分布:")
                for item in data.get('syndrome_distribution', []):
                    print(f"    {item['syndrome']}: {item['count']}人")
            else:
                print(f"✗ 获取统计信息失败: {result.get('error')}")
        else:
            print(f"✗ HTTP错误: {response.status_code}")
    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")

def main():
    """主测试函数"""
    print("开始测试数据库API功能...\n")
    print("注意: 请确保Flask应用已经启动在 http://localhost:5000")
    
    # 1. 测试诊断API
    session_id = test_diagnosis_api()
    
    # 2. 测试历史记录API
    test_history_api(session_id)
    
    # 3. 测试统计API
    test_stats_api()
    
    print(f"\n=== 测试完成 ===")

if __name__ == "__main__":
    main()