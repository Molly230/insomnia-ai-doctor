from flask import Blueprint, request, jsonify
from app.models.diagnosis_models import PatientAnswers, QuestionnaireAnswer
from app.models.database_models import Patient, DiagnosisRecord
from app.diagnosis.scoring_engine import InsomniaScoring
from app import db
import uuid
from datetime import datetime

diagnosis_bp = Blueprint('diagnosis', __name__)

@diagnosis_bp.route('/analyze', methods=['POST'])
def analyze_patient():
    """分析患者症状，进行二元诊断并保存到数据库"""
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
        
        # 调用新的评分引擎进行综合分析
        analysis_result = InsomniaScoring.comprehensive_analysis(patient_answers)
        
        # 处理患者信息
        patient_info = data.get('patient_info', {})
        patient = None
        
        if patient_info and patient_info.get('phone'):
            # 查找现有患者或创建新患者
            patient = Patient.query.filter_by(phone=patient_info['phone']).first()
            
            if not patient:
                patient = Patient(
                    name=patient_info.get('name', ''),
                    phone=patient_info.get('phone', ''),
                    age=patient_info.get('age', 0),
                    gender=patient_info.get('gender', '')
                )
                db.session.add(patient)
                db.session.flush()  # 获取ID但不提交
        
        # 生成会话ID
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # 保存诊断记录
        diagnosis_record = DiagnosisRecord(
            patient_id=patient.id if patient else None,
            session_id=session_id,
            total_sleep_score=analysis_result['total_sleep_score'],
            sleep_quality_grade=analysis_result['sleep_quality_grade'],
            sleep_score_percentage=analysis_result['sleep_quality_evaluation']['percentage'],
            final_diagnosis=analysis_result['final_diagnosis'],
            diagnosed_at=datetime.utcnow()
        )
        
        # 设置JSON字段
        diagnosis_record.set_questionnaire_answers(data['answers'])
        diagnosis_record.set_syndrome_scores(analysis_result['syndrome_evaluation'])
        diagnosis_record.set_binary_diagnosis_details(analysis_result['binary_diagnosis'])
        diagnosis_record.set_treatment_plan(analysis_result['treatment_plan'])
        
        db.session.add(diagnosis_record)
        db.session.commit()
        
        # 返回统一的诊断结果
        return jsonify({
            'success': True,
            'data': {
                'patient_id': patient.id if patient else None,
                'diagnosis_record_id': diagnosis_record.id,
                'session_id': session_id,
                'timestamp': diagnosis_record.diagnosed_at.isoformat(),
                
                # 睡眠质量评分结果
                'sleep_quality': {
                    'total_score': analysis_result['total_sleep_score'],
                    'percentage': analysis_result['sleep_quality_evaluation']['percentage'],
                    'grade': analysis_result['sleep_quality_grade'],
                    'max_possible_score': analysis_result['sleep_quality_evaluation']['max_possible_score'],
                    'question_details': analysis_result['sleep_quality_evaluation']['question_scores']
                },
                
                # 二元诊断结果
                'syndrome_diagnosis': {
                    'final_diagnosis': analysis_result['final_diagnosis'],
                    'binary_diagnosis_details': analysis_result['binary_diagnosis'],
                    'syndrome_scores': analysis_result['syndrome_evaluation'],
                    'primary_syndrome': analysis_result['primary_syndrome'],
                    'primary_score': analysis_result['primary_syndrome_score']
                },
                
                # 治疗方案
                'treatment_plan': analysis_result['treatment_plan'],
                
                # 综合分析摘要
                'summary': analysis_result['analysis_summary']
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'诊断过程中发生错误: {str(e)}'
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

@diagnosis_bp.route('/history/<session_id>', methods=['GET'])
def get_diagnosis_history(session_id):
    """根据session_id获取诊断历史记录"""
    try:
        diagnosis_record = DiagnosisRecord.query.filter_by(session_id=session_id).first()
        
        if not diagnosis_record:
            return jsonify({
                'success': False,
                'error': '未找到诊断记录'
            }), 404
        
        return jsonify({
            'success': True,
            'data': diagnosis_record.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取诊断记录失败: {str(e)}'
        }), 500

@diagnosis_bp.route('/patient/<int:patient_id>/history', methods=['GET'])
def get_patient_diagnosis_history(patient_id):
    """获取患者的所有诊断记录"""
    try:
        diagnosis_records = DiagnosisRecord.query.filter_by(patient_id=patient_id)\
                          .order_by(DiagnosisRecord.diagnosed_at.desc()).all()
        
        if not diagnosis_records:
            return jsonify({
                'success': True,
                'data': [],
                'message': '该患者暂无诊断记录'
            })
        
        records = [record.to_dict() for record in diagnosis_records]
        
        return jsonify({
            'success': True,
            'data': records,
            'total': len(records)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取患者诊断历史失败: {str(e)}'
        }), 500

@diagnosis_bp.route('/stats', methods=['GET'])
def get_diagnosis_stats():
    """获取诊断统计信息"""
    try:
        from sqlalchemy import func
        
        # 总诊断次数
        total_diagnosis = DiagnosisRecord.query.count()
        
        # 各等级睡眠质量分布
        grade_stats = db.session.query(
            DiagnosisRecord.sleep_quality_grade,
            func.count(DiagnosisRecord.id).label('count')
        ).group_by(DiagnosisRecord.sleep_quality_grade).all()
        
        # 各证型分布
        syndrome_stats = db.session.query(
            DiagnosisRecord.final_diagnosis,
            func.count(DiagnosisRecord.id).label('count')
        ).group_by(DiagnosisRecord.final_diagnosis).all()
        
        # 今日诊断数
        from datetime import date
        today_diagnosis = DiagnosisRecord.query.filter(
            func.date(DiagnosisRecord.diagnosed_at) == date.today()
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_diagnosis': total_diagnosis,
                'today_diagnosis': today_diagnosis,
                'sleep_grade_distribution': [
                    {'grade': grade, 'count': count} for grade, count in grade_stats
                ],
                'syndrome_distribution': [
                    {'syndrome': syndrome, 'count': count} for syndrome, count in syndrome_stats
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取统计信息失败: {str(e)}'
        }), 500