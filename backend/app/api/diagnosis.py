from flask import Blueprint, request, jsonify
from app.models.diagnosis_models import PatientAnswers, QuestionnaireAnswer

diagnosis_bp = Blueprint('diagnosis', __name__)

@diagnosis_bp.route('/analyze', methods=['POST'])
def analyze_patient():
    """分析患者症状，进行二元诊断"""
    try:
        data = request.get_json()
        
        if not data or 'answers' not in data:
            return jsonify({
                'success': False,
                'error': '请提供患者答案数据'
            }), 400
        
        # 解析患者答案
        answers = []
        for answer_data in data['answers']:
            answer = QuestionnaireAnswer(
                question_id=answer_data['question_id'],
                selected_options=answer_data['selected_options']
            )
            answers.append(answer)
        
        patient_answers = PatientAnswers(answers=answers)
        
        # TODO: 实现二元诊断逻辑
        # diagnosis_result = BinaryDiagnosisEngine.diagnose(patient_answers)
        
        # 临时返回示例结果
        return jsonify({
            'success': True,
            'data': {
                'patient_id': data.get('patient_id', 'unknown'),
                'diagnosis_result': {
                    'row_dimension': '骨髓',
                    'column_dimension': '空虚',
                    'final_syndrome': '骨髓空虚',
                    'confidence_score': 0.85,
                    'analysis': '基于问诊结果的二元诊断分析'
                },
                'timestamp': '2024-01-01T00:00:00Z'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@diagnosis_bp.route('/syndrome-info/<syndrome_name>', methods=['GET'])
def get_syndrome_info(syndrome_name):
    """获取证型详细信息"""
    try:
        # TODO: 从知识库获取证型信息
        syndrome_info = {
            'name': syndrome_name,
            'category': '虚证',
            'symptoms': ['严重失眠', '记忆力下降', '腰膝酸软'],
            'tongue': '淡红舌苔薄白',
            'pulse': '沉细脉',
            'pathogenesis': '先天不足，后天失养，骨髓空虚'
        }
        
        return jsonify({
            'success': True,
            'data': syndrome_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@diagnosis_bp.route('/dimensions', methods=['GET'])
def get_diagnosis_dimensions():
    """获取二元诊断的所有维度"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'row_dimensions': [
                    '骨髓',
                    '肝脾循环',
                    '血内循环',
                    '神内循环'
                ],
                'column_dimensions': [
                    '空虚',
                    '不足',
                    '不畅'
                ],
                'description': '行列交叉确定最终证型'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500