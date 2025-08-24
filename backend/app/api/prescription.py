from flask import Blueprint, request, jsonify

prescription_bp = Blueprint('prescription', __name__)

@prescription_bp.route('/generate', methods=['POST'])
def generate_prescription():
    """根据证型生成治疗方案"""
    try:
        data = request.get_json()
        
        if not data or 'syndrome_type' not in data:
            return jsonify({
                'success': False,
                'error': '请提供证型信息'
            }), 400
        
        syndrome_type = data['syndrome_type']
        patient_info = data.get('patient_info', {})
        
        # TODO: 根据证型从知识库获取对应的治疗方案
        treatment_plan = {
            'syndrome_type': syndrome_type,
            'herbal_prescription': {
                'formula_name': '定志丸加减',
                'ingredients': {
                    '人参': '10g',
                    '茯苓': '15g',
                    '远志': '10g',
                    '石菖蒲': '10g',
                    '酸枣仁': '20g',
                    '龙骨': '15g',
                    '牡蛎': '15g'
                },
                'preparation': '水煎服',
                'dosage': '每日一剂，分两次服用',
                'duration': '14天为一疗程'
            },
            'external_treatments': [
                {
                    'method': '耳穴压豆',
                    'points': ['神门', '心', '肾', '皮质下'],
                    'frequency': '每日按压3-5次',
                    'duration': '留置3天更换'
                },
                {
                    'method': '足浴安神',
                    'formula': '酸枣仁30g、夜交藤30g、合欢花15g',
                    'temperature': '40-42℃',
                    'duration': '浸泡20-30分钟',
                    'timing': '睡前1小时'
                }
            ],
            'diet_therapy': [
                {
                    'name': '百合莲子粥',
                    'ingredients': ['百合30g', '莲子30g', '大米100g'],
                    'method': '先煮莲子至软，再加百合和大米煮粥',
                    'timing': '晚餐服用',
                    'effects': '养心安神，润肺止咳'
                },
                {
                    'name': '酸枣仁茶',
                    'ingredients': ['酸枣仁15g', '龙眼肉10g'],
                    'method': '开水冲泡，焖10分钟',
                    'timing': '睡前饮用',
                    'effects': '宁心安神'
                }
            ],
            'lifestyle_advice': [
                '规律作息，晚上10点前入睡',
                '睡前避免使用电子设备',
                '保持室内安静，温度适宜',
                '适当运动，但避免睡前剧烈运动',
                '放松心情，可做冥想或深呼吸练习'
            ],
            'precautions': [
                '服药期间忌食辛辣刺激食物',
                '如有不适及时就医',
                '定期复诊，根据症状调整用药'
            ]
        }
        
        return jsonify({
            'success': True,
            'data': treatment_plan
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prescription_bp.route('/formulas', methods=['GET'])
def get_formulas():
    """获取方剂库"""
    try:
        # TODO: 从知识库获取方剂信息
        formulas = [
            {
                'name': '甘麦大枣汤',
                'category': '安神剂',
                'ingredients': {
                    '甘草': '9g',
                    '小麦': '30g',
                    '大枣': '10枚'
                },
                'indications': ['心神不宁', '情志异常'],
                'effects': '养心安神，和中缓急'
            },
            {
                'name': '安神定志丸',
                'category': '安神剂',
                'ingredients': {
                    '人参': '6g',
                    '茯苓': '9g',
                    '远志': '6g',
                    '石菖蒲': '6g'
                },
                'indications': ['心神不安', '健忘'],
                'effects': '益气镇惊，安神定志'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': formulas
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prescription_bp.route('/external-treatments', methods=['GET'])
def get_external_treatments():
    """获取外治法库"""
    try:
        treatments = [
            {
                'name': '耳穴压豆',
                'category': '穴位疗法',
                'acupoints': ['神门', '心', '肾', '皮质下', '交感'],
                'technique': '王不留行籽贴压',
                'frequency': '每日按压3-5次，每次30秒',
                'duration': '留置3-5天更换',
                'effects': ['宁心安神', '调节植物神经'],
                'indications': ['失眠', '心神不宁']
            },
            {
                'name': '足浴安神',
                'category': '药浴疗法',
                'formula': {
                    '酸枣仁': '30g',
                    '夜交藤': '30g',
                    '合欢花': '15g',
                    '薰衣草': '10g'
                },
                'method': '煎煮取汁，温度40-42℃',
                'duration': '浸泡20-30分钟',
                'timing': '睡前1小时',
                'effects': ['温经通络', '宁心安神']
            }
        ]
        
        return jsonify({
            'success': True,
            'data': treatments
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prescription_bp.route('/diet-therapy', methods=['GET'])
def get_diet_therapy():
    """获取食疗方库"""
    try:
        recipes = [
            {
                'name': '百合莲子粥',
                'category': '安神食疗',
                'ingredients': ['百合30g', '莲子30g', '大米100g'],
                'preparation': '先煮莲子至软，再加百合和大米煮粥',
                'effects': '养心安神，润肺止咳',
                'timing': '晚餐或睡前服用',
                'contraindications': ['脾胃虚寒者慎用'],
                'suitable_syndromes': ['心阴不足', '肺燥咳嗽']
            },
            {
                'name': '酸枣仁粥',
                'category': '安神食疗',
                'ingredients': ['酸枣仁15g', '粳米100g'],
                'preparation': '酸枣仁研末，与粳米同煮粥',
                'effects': '养心安神，敛汗生津',
                'timing': '早晚各一次',
                'contraindications': ['实热证者不宜'],
                'suitable_syndromes': ['心血不足', '神经衰弱']
            }
        ]
        
        return jsonify({
            'success': True,
            'data': recipes
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500