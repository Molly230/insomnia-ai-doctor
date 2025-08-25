"""
测试新的评分系统
"""
from app.models.diagnosis_models import PatientAnswers, QuestionnaireAnswer
from app.diagnosis.scoring_engine import InsomniaScoring

def test_scoring_system():
    """测试评分系统的基本功能"""
    
    # 模拟患者答案 - 测试完整评分规则
    test_answers = [
        # 前6题 - 正分项
        QuestionnaireAnswer(question_id=1, selected_options=["较差"]),                    # 0分
        QuestionnaireAnswer(question_id=2, selected_options=["60分钟以上"]),               # 0分 
        QuestionnaireAnswer(question_id=3, selected_options=["5小时以下"]),                # 0分
        QuestionnaireAnswer(question_id=4, selected_options=["4次及以上"]),                # 0分
        QuestionnaireAnswer(question_id=5, selected_options=["60分钟以上"]),               # 0分
        QuestionnaireAnswer(question_id=6, selected_options=["每天都有"]),                  # 0分
        
        # 第7-8题 - 负分项
        QuestionnaireAnswer(question_id=7, selected_options=["反复清醒", "整夜做梦"]),       # -6分
        QuestionnaireAnswer(question_id=8, selected_options=["苯二氮卓类：地西泮、劳拉西泮"]), # -5分
        QuestionnaireAnswer(question_id=9, selected_options=["3个月以上（高级）"]),           # 不参与评分
        
        # 第10-19题 - 负分项
        QuestionnaireAnswer(question_id=10, selected_options=["是"]),                      # -1分
        QuestionnaireAnswer(question_id=11, selected_options=["时有耳鸣"]),                  # -1分
        QuestionnaireAnswer(question_id=12, selected_options=["是"]),                      # -1分
        QuestionnaireAnswer(question_id=13, selected_options=["无"]),                      # 0分
        QuestionnaireAnswer(question_id=14, selected_options=["是"]),                      # -1分
        QuestionnaireAnswer(question_id=15, selected_options=["夜间盗汗"]),                  # -1分
        QuestionnaireAnswer(question_id=16, selected_options=["是"]),                      # -1分
        QuestionnaireAnswer(question_id=17, selected_options=["腰酸无力", "身寒怕冷"]),      # -2分
        QuestionnaireAnswer(question_id=18, selected_options=["是"]),                      # -1分
        QuestionnaireAnswer(question_id=19, selected_options=["好忘事，记忆力下降"]),         # -1分
    ]
    
    patient_answers = PatientAnswers(answers=test_answers)
    
    # 执行综合分析
    result = InsomniaScoring.comprehensive_analysis(patient_answers)
    
    print("=== 失眠评分系统测试结果 ===")
    print(f"睡眠质量总分: {result['total_sleep_score']}/{result['sleep_quality_evaluation']['max_possible_score']} "
          f"({result['sleep_quality_evaluation']['percentage']}%)")
    
    print(f"睡眠质量等级: {result['sleep_quality_grade']}")
    print(f"主要证型: {result['primary_syndrome']} (得分: {result['primary_syndrome_score']})")
    print(f"分析总结: {result['analysis_summary']}")
    
    print("\n=== 各证型得分详情 ===")
    for syndrome, score_info in result['syndrome_evaluation'].items():
        print(f"{syndrome}: {score_info['total_score']}分")
    
    print("\n=== 睡眠质量评分详情（19题）===")
    for question, details in result['sleep_quality_evaluation']['question_scores'].items():
        if 'selected_options' in details:
            options_str = ', '.join([f"{opt['option']}({opt['score']}分)" for opt in details['selected_options']])
            print(f"{question}: {options_str} -> 总计{details['total_score']}分")
        else:
            print(f"{question}: {details['selected']} -> {details['score']}分")
    
    print("\n=== 治疗方案推荐 ===")
    treatment = result['treatment_plan']
    print(f"治疗类型: {treatment['treatment_type']}")
    print(f"方案描述: {treatment['treatment_description']}")
    print(f"食疗建议: {treatment['dietary_therapy']}")
    print(f"推荐食品: {', '.join(treatment['recommended_foods'])}")
    if treatment['acupoints']:
        print(f"穴位治疗: {', '.join(treatment['acupoints'])}")
    print(f"基础建议: {', '.join(treatment['basic_recommendations'])}")
    if treatment['needs_professional']:
        print("⚠️ 建议寻求专业中医师诊断治疗")
    
    return result

if __name__ == "__main__":
    test_scoring_system()