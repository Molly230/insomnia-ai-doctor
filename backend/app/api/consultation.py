from flask import Blueprint, request, jsonify
from app.diagnosis.questionnaire import InsomniaQuestionnaire
from app.models.diagnosis_models import QuestionnaireAnswer, PatientAnswers

consultation_bp = Blueprint('consultation', __name__)

@consultation_bp.route('/questions', methods=['GET'])
def get_questions():
    """获取问诊问题列表"""
    try:
        questions = InsomniaQuestionnaire.get_questions()
        questions_data = []
        
        for q in questions:
            question_data = {
                'id': q.id,
                'text': q.text,
                'type': q.type.value,
                'category': q.category,
                'options': [
                    {
                        'value': opt.value,
                        'label': opt.label,
                        'score': opt.score
                    } for opt in q.options
                ]
            }
            questions_data.append(question_data)
        
        return jsonify({
            'success': True,
            'data': questions_data,
            'total_questions': len(questions_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@consultation_bp.route('/submit-answers', methods=['POST'])
def submit_answers():
    """提交问诊答案"""
    try:
        data = request.get_json()
        
        if not data or 'answers' not in data:
            return jsonify({
                'success': False,
                'error': '请提供问诊答案'
            }), 400
        
        # 解析答案
        answers = []
        for answer_data in data['answers']:
            answer = QuestionnaireAnswer(
                question_id=answer_data['question_id'],
                selected_options=answer_data['selected_options']
            )
            answers.append(answer)
        
        patient_answers = PatientAnswers(answers=answers)
        
        # TODO: 调用诊断引擎进行分析
        # diagnosis_result = DiagnosisEngine.analyze(patient_answers)
        
        # 暂时返回成功状态
        return jsonify({
            'success': True,
            'message': '问诊答案提交成功',
            'data': {
                'answers_count': len(answers),
                'next_step': '诊断分析'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@consultation_bp.route('/question/<int:question_id>', methods=['GET'])
def get_question_detail(question_id):
    """获取单个问题详情"""
    try:
        question = InsomniaQuestionnaire.get_question_by_id(question_id)
        
        if not question:
            return jsonify({
                'success': False,
                'error': f'问题 {question_id} 不存在'
            }), 404
        
        question_data = {
            'id': question.id,
            'text': question.text,
            'type': question.type.value,
            'category': question.category,
            'options': [
                {
                    'value': opt.value,
                    'label': opt.label,
                    'score': opt.score
                } for opt in question.options
            ]
        }
        
        return jsonify({
            'success': True,
            'data': question_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500