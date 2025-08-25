"""
失眠评分引擎 - 基于用户提供的两阶段评分逻辑
"""
from typing import Dict, List, Tuple
from app.models.diagnosis_models import PatientAnswers, QuestionnaireAnswer

class InsomniaScoring:
    """失眠评分系统"""
    
    # 睡眠质量总评分配置（除了问题9，其他18题参与评分）
    SLEEP_QUALITY_SCORING = {
        1: {  # 睡眠状况
            "好": 10,
            "一般": 5,
            "较差": 0
        },
        2: {  # 入睡时间
            "5分钟以内": 12,
            "6-15分钟": 9,
            "16-30分钟": 6,
            "31-60分钟": 3,
            "60分钟以上": 0
        },
        3: {  # 睡眠时长
            "8小时及以上": 12,
            "7-8小时": 9,
            "6-7小时": 6,
            "5-6小时": 3,
            "5小时以下": 0
        },
        4: {  # 夜醒次数
            "几乎不醒来": 9,
            "1次": 6,
            "2-3次": 3,
            "4次及以上": 0
        },
        5: {  # 再入睡时间
            "5分钟以内": 12,
            "6-15分钟": 9,
            "16-30分钟": 6,
            "31-60分钟": 3,
            "60分钟以上": 0
        },
        6: {  # 白天嗜睡
            "几乎没有": 9,
            "每周1-2次": 6,
            "每周3-5次": 3,
            "每天都有": 0
        },
        7: {  # 睡眠困扰（多选，负分项）
            "反复清醒": -3,
            "整夜做梦": -3,
            "晨起疲倦": -3,
            "难以入眠": -3,
            "无": 0
        },
        8: {  # 用药史（多选，负分项）
            "苯二氮卓类：地西泮、劳拉西泮": -5,
            "非苯二氮卓类：唑吡坦、右佐匹克隆": -5,
            "褪黑素受体激动剂：雷美替胺": -5,
            "食欲素受体拮抗剂：苏沃雷生": -5,
            "抗抑郁药物：曲唑酮、米氮平": -5,
            "无": 0
        },
        # 注意：问题9不参与评分，只用于诊断跳转
        10: {"是": -1, "否": 0},  # 精神压力
        11: {  # 身体症状
            "时有耳鸣": -1,
            "时发痔疮，肛周瘙痒": -1,
            "腹胀/腹部不适": -1,
            "无": 0
        },
        12: {"是": -1, "否": 0},  # 周身酸痛
        13: {  # 特殊症状
            "夜间憋醒/胸闷，心跳加速": -1,
            "皮肤瘙痒，发荨麻疹": -1,
            "咳嗽/气短/喘促等": -1,
            "无": 0
        },
        14: {"是": -1, "否": 0},  # 电子产品使用
        15: {  # 中医症状
            "面色暗黑，无精打采": -1,
            "容易受惊，害怕": -1,
            "夜间盗汗": -1,
            "无": 0
        },
        16: {"是": -1, "否": 0},  # 劳心耗神
        17: {  # 肾虚症状
            "腰酸无力": -1,
            "身寒怕冷": -1,
            "夜尿频繁": -1,
            "无": 0
        },
        18: {"是": -1, "否": 0},  # 用脑过度
        19: {  # 认知功能（多选）
            "好忘事，记忆力下降": -1,
            "白天嗜睡": -1,
            "偏头痛/头痛": -1,
            "无": 0
        }
    }
    
    # 第二阶段：二元诊断配置（从问题10开始）
    SYNDROME_SCORING = {
        # 肝肠（问题10-11）
        "肝肠": {
            "questions": [10, 11],
            "scoring": {
                10: {"是": 1, "否": 0},  # 精神压力大/情绪紧张
                11: {  # 身体症状
                    "时有耳鸣": 1,
                    "时发痔疮，肛周瘙痒": 1,
                    "腹胀/腹部不适": 1,
                    "无": 0
                }
            }
        },
        
        # 血液（问题12-13）
        "血液": {
            "questions": [12, 13],
            "scoring": {
                12: {"是": 1, "否": 0},  # 周身酸痛/脊柱疼痛
                13: {  # 特殊症状
                    "夜间憋醒/胸闷，心跳加速": 1,
                    "皮肤瘙痒，发荨麻疹": 1,
                    "咳嗽/气短/喘促等": 1,
                    "无": 0
                }
            }
        },
        
        # 神内（问题14-15）
        "神内": {
            "questions": [14, 15],
            "scoring": {
                14: {"是": 1, "否": 0},  # 电子产品使用超过3小时/天
                15: {  # 中医症状
                    "面色暗黑，无精打采": 1,
                    "容易受惊，害怕": 1,
                    "夜间盗汗": 1,
                    "无": 0
                }
            }
        },
        
        # 骨髓空虚（问题16-17）
        "骨髓空虚": {
            "questions": [16, 17],
            "scoring": {
                16: {"是": 1, "否": 0},  # 劳心耗神过度
                17: {  # 肾虚症状
                    "腰酸无力": 1,
                    "身寒怕冷": 1,
                    "夜尿频繁": 1,
                    "无": 0
                }
            }
        },
        
        # 脑髓空虚（问题18-19）
        "脑髓空虚": {
            "questions": [18, 19],
            "scoring": {
                18: {"是": 1, "否": 0},  # 用脑过度
                19: {  # 认知功能（多选）
                    "好忘事，记忆力下降": 1,
                    "白天嗜睡": 1,
                    "偏头痛/头痛": 1,
                    "无": 0
                }
            }
        }
    }
    
    # 睡眠质量分级标准（基于用户提供的标准：-57到+64的评分范围）
    SLEEP_QUALITY_GRADES = {
        "优": {"min_score": 54, "description": "睡眠质量优秀"},      # 54-64分 
        "良": {"min_score": 34, "description": "睡眠质量良好"},      # 34-53分  
        "中": {"min_score": 0, "description": "睡眠质量一般"},       # 0-33分
        "差": {"min_score": -57, "description": "睡眠质量较差"}      # -57到-1分
    }
    
    @classmethod
    def calculate_total_sleep_score(cls, patient_answers: PatientAnswers) -> Dict:
        """计算睡眠质量总评分（除问题9外的18题）"""
        total_score = 0
        question_scores = {}
        max_possible_score = 0
        
        # 遍历参与评分的题目（跳过问题9）
        scoring_questions = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        
        for i in scoring_questions:
            answer = patient_answers.get_answer_by_question_id(i)
            question_score = 0
            selected_options = []
            scoring_config = cls.SLEEP_QUALITY_SCORING.get(i, {})
            
            if answer and answer.selected_options:
                for option in answer.selected_options:
                    option_score = scoring_config.get(option, 0)
                    question_score += option_score
                    selected_options.append({
                        "option": option,
                        "score": option_score
                    })
                
                total_score += question_score
                question_scores[f"问题{i}"] = {
                    "selected_options": selected_options,
                    "total_score": question_score
                }
            
            # 计算该题的最高可能分数（只计算正分）
            if scoring_config:
                question_max = max(scoring_config.values())
                if question_max > 0:  # 只计算正分作为最高分
                    max_possible_score += question_max
        
        return {
            "total_score": total_score,
            "max_possible_score": max_possible_score,
            "percentage": round(total_score / max_possible_score * 100, 1) if max_possible_score > 0 else 0,
            "question_scores": question_scores,
            "note": "问题9不参与评分，仅用于诊断跳转"
        }
    
    @classmethod
    def calculate_syndrome_scores(cls, patient_answers: PatientAnswers) -> Dict:
        """计算各证型得分"""
        syndrome_scores = {}
        
        for syndrome_name, config in cls.SYNDROME_SCORING.items():
            syndrome_score = 0
            question_details = {}
            
            for question_id in config["questions"]:
                answer = patient_answers.get_answer_by_question_id(question_id)
                if answer and answer.selected_options:
                    question_score = 0
                    selected_options = []
                    
                    for option in answer.selected_options:
                        option_score = config["scoring"].get(question_id, {}).get(option, 0)
                        question_score += option_score
                        selected_options.append({
                            "option": option,
                            "score": option_score
                        })
                    
                    syndrome_score += question_score
                    question_details[f"问题{question_id}"] = {
                        "selected_options": selected_options,
                        "total_score": question_score
                    }
            
            syndrome_scores[syndrome_name] = {
                "total_score": syndrome_score,
                "question_details": question_details
            }
        
        return syndrome_scores
    
    @classmethod
    def determine_sleep_quality_grade(cls, total_sleep_score: int) -> str:
        """根据19题总分确定睡眠质量等级"""
        for grade, criteria in cls.SLEEP_QUALITY_GRADES.items():
            if total_sleep_score >= criteria["min_score"]:
                return grade
        return "很差"
    
    # 二元诊断矩阵配置
    BINARY_DIAGNOSIS_MATRIX = {
        ("肝肠", "骨髓空虚"): "肝郁肾虚",
        ("肝肠", "脑髓空虚"): "肝郁脑虚", 
        ("血液", "骨髓空虚"): "气血两虚",
        ("血液", "脑髓空虚"): "气滞血瘀",
        ("神内", "骨髓空虚"): "精髓空虚",
        ("神内", "脑髓空虚"): "神经衰弱"
    }
    
    @classmethod
    def determine_binary_diagnosis(cls, syndrome_scores: Dict) -> Dict:
        """二元诊断：行列交叉确定最终证型"""
        # 行维度：肝肠、血液、神内（取最低分，即数值最小）
        row_syndromes = {
            "肝肠": syndrome_scores["肝肠"]["total_score"],
            "血液": syndrome_scores["血液"]["total_score"], 
            "神内": syndrome_scores["神内"]["total_score"]
        }
        
        # 列维度：骨髓空虚、脑髓空虚（取最低分，即数值最小）
        column_syndromes = {
            "骨髓空虚": syndrome_scores["骨髓空虚"]["total_score"],
            "脑髓空虚": syndrome_scores["脑髓空虚"]["total_score"]
        }
        
        # 找到行维度最低分（数值最小）
        min_row_syndrome = min(row_syndromes.items(), key=lambda x: x[1])
        
        # 找到列维度最低分（数值最小）  
        min_column_syndrome = min(column_syndromes.items(), key=lambda x: x[1])
        
        # 矩阵交叉查找最终诊断
        matrix_key = (min_row_syndrome[0], min_column_syndrome[0])
        final_diagnosis = cls.BINARY_DIAGNOSIS_MATRIX.get(matrix_key, "未知证型")
        
        return {
            "row_dimension": min_row_syndrome[0],
            "row_score": min_row_syndrome[1],
            "column_dimension": min_column_syndrome[0], 
            "column_score": min_column_syndrome[1],
            "matrix_key": matrix_key,
            "final_diagnosis": final_diagnosis
        }
    
    @classmethod
    def determine_primary_syndrome(cls, syndrome_scores: Dict) -> Tuple[str, int]:
        """确定主要证型（保留原逻辑用于兼容）"""
        max_syndrome = None
        max_score = -1
        
        for syndrome_name, score_info in syndrome_scores.items():
            if score_info["total_score"] > max_score:
                max_score = score_info["total_score"]
                max_syndrome = syndrome_name
        
        return max_syndrome, max_score
    
    # 治疗方案配置 - 基于用户提供的分级个性化方案
    TREATMENT_RECOMMENDATIONS = {
        # 各证型对应的穴位贴
        "syndrome_acupoint_patches": {
            "肝郁肾虚": "肝郁肾虚穴位贴",
            "肝郁脑虚": "肝郁脑虚穴位贴", 
            "气血两虚": "气血两虚穴位贴",
            "气滞血瘀": "气滞血瘀穴位贴",
            "精髓空虚": "精髓空虚穴位贴",
            "神经衰弱": "神经衰弱穴位贴"
        },
        
        # 茶包配置（根据肝肠/血液/神内维度）
        "tea_packages": {
            "肝肠": "舒肝解郁茶包",
            "血液": "补血活血茶包", 
            "神内": "安神定志茶包",
            "通用": "通用安眠茶包"
        },
        
        # 营养补充（根据骨髓/脑髓维度）
        "nutritional_supplements": {
            "骨髓": "坚果营养包",
            "脑髓": "鱼油胶囊",
            "奶粉": "植物蛋白奶粉"
        },
        
        # 分级治疗方案
        "grade_treatments": {
            "优": {
                "type": "保持", 
                "description": "睡眠质量优秀，简单保健即可",
                "products": ["通用安眠茶包"]
            },
            "良": {
                "type": "食疗调理",
                "description": "根据主要问题维度进行针对性调理", 
                "products": ["针对性茶包", "奶粉"]
            },
            "中": {
                "type": "食疗+外治",
                "description": "营养补充配合穴位治疗",
                "products": ["营养补充品", "奶粉", "证型穴位贴"]
            },
            "差": {
                "type": "专业医疗",
                "description": "需要专业医生制定个性化中药+食疗方案",
                "products": ["引导咨询专业医生"]
            }
        }
    }
    
    @classmethod
    def generate_treatment_plan(cls, sleep_grade: str, final_diagnosis: str, syndrome_scores: Dict, binary_diagnosis: Dict) -> Dict:
        """根据睡眠等级和二元诊断生成个性化治疗方案"""
        
        # 获取基础治疗方案
        base_treatment = cls.TREATMENT_RECOMMENDATIONS["grade_treatments"].get(sleep_grade, {})
        
        # 初始化治疗方案
        treatment_plan = {
            "sleep_grade": sleep_grade,
            "syndrome_type": final_diagnosis,
            "treatment_type": base_treatment.get("type", "未知"),
            "treatment_description": base_treatment.get("description", ""),
            "products": [],
            "instructions": "",
            "needs_professional": False
        }
        
        # 根据不同等级生成具体方案
        if sleep_grade == "优":
            # 优：只给通用茶包
            treatment_plan["products"] = [cls.TREATMENT_RECOMMENDATIONS["tea_packages"]["通用"]]
            treatment_plan["instructions"] = "继续保持良好的睡眠习惯，定期饮用保健茶包即可。"
            
        elif sleep_grade == "良":
            # 良：根据肝肠/血液/神内最高分维度 + 奶粉
            row_scores = {
                "肝肠": syndrome_scores.get("肝肠", {}).get("total_score", 0),
                "血液": syndrome_scores.get("血液", {}).get("total_score", 0),
                "神内": syndrome_scores.get("神内", {}).get("total_score", 0)
            }
            
            # 找到最高分维度
            max_dimension = max(row_scores.items(), key=lambda x: x[1])[0]
            
            treatment_plan["products"] = [
                cls.TREATMENT_RECOMMENDATIONS["tea_packages"][max_dimension],
                cls.TREATMENT_RECOMMENDATIONS["nutritional_supplements"]["奶粉"]
            ]
            treatment_plan["instructions"] = f"根据您的主要问题（{max_dimension}维度），配置针对性茶包和营养补充。"
            
        elif sleep_grade == "中":
            # 中：根据骨髓/脑髓分数高低 + 奶粉 + 对应证型穴位贴
            column_scores = {
                "骨髓空虚": syndrome_scores.get("骨髓空虚", {}).get("total_score", 0),
                "脑髓空虚": syndrome_scores.get("脑髓空虚", {}).get("total_score", 0)
            }
            
            # 确定主要虚损维度
            if column_scores["骨髓空虚"] >= column_scores["脑髓空虚"]:
                supplement = cls.TREATMENT_RECOMMENDATIONS["nutritional_supplements"]["骨髓"]
                main_dimension = "骨髓"
            else:
                supplement = cls.TREATMENT_RECOMMENDATIONS["nutritional_supplements"]["脑髓"]
                main_dimension = "脑髓"
            
            # 获取证型对应的穴位贴
            acupoint_patch = cls.TREATMENT_RECOMMENDATIONS["syndrome_acupoint_patches"].get(final_diagnosis, "")
            
            treatment_plan["products"] = [
                supplement,
                cls.TREATMENT_RECOMMENDATIONS["nutritional_supplements"]["奶粉"],
                acupoint_patch
            ]
            treatment_plan["instructions"] = f"根据您的{main_dimension}虚损情况，配置营养补充品、奶粉和{final_diagnosis}专用穴位贴。"
            
        elif sleep_grade == "差":
            # 差：引导咨询专业医生
            treatment_plan["products"] = ["专业医生咨询"]
            treatment_plan["instructions"] = "您的睡眠质量较差，需要专业中医师制定个性化的中药+食疗+外治方案，建议立即咨询专业医生。"
            treatment_plan["needs_professional"] = True
        
        return treatment_plan
    
    @classmethod
    def comprehensive_analysis(cls, patient_answers: PatientAnswers) -> Dict:
        """综合分析"""
        # 第一阶段：睡眠质量总评分（19题总分）
        sleep_score_result = cls.calculate_total_sleep_score(patient_answers)
        
        # 第二阶段：从第10题开始的二元诊断
        syndrome_scores = cls.calculate_syndrome_scores(patient_answers)
        
        # 确定睡眠质量等级（基于19题总分）
        sleep_grade = cls.determine_sleep_quality_grade(sleep_score_result["total_score"])
        
        # 二元诊断：行列交叉确定最终证型
        binary_diagnosis = cls.determine_binary_diagnosis(syndrome_scores)
        
        # 保留原逻辑用于兼容
        primary_syndrome, primary_score = cls.determine_primary_syndrome(syndrome_scores)
        
        # 生成个性化治疗方案
        treatment_plan = cls.generate_treatment_plan(
            sleep_grade, 
            binary_diagnosis["final_diagnosis"], 
            syndrome_scores,
            binary_diagnosis
        )
        
        return {
            "sleep_quality_evaluation": sleep_score_result,
            "syndrome_evaluation": syndrome_scores,
            "sleep_quality_grade": sleep_grade,
            
            # 新的二元诊断结果
            "binary_diagnosis": binary_diagnosis,
            "final_diagnosis": binary_diagnosis["final_diagnosis"],
            
            # 治疗方案推荐
            "treatment_plan": treatment_plan,
            
            # 保留原字段用于兼容
            "primary_syndrome": primary_syndrome,
            "primary_syndrome_score": primary_score,
            "total_sleep_score": sleep_score_result["total_score"],
            
            "analysis_summary": f"睡眠质量总分：{sleep_score_result['total_score']}分，等级：{sleep_grade}；二元诊断：{binary_diagnosis['final_diagnosis']}（{binary_diagnosis['row_dimension']}×{binary_diagnosis['column_dimension']}）；治疗方案：{treatment_plan['treatment_type']}"
        }