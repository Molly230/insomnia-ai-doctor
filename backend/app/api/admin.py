"""
管理后台API
提供患者数据、诊断统计等管理功能
"""
from flask import Blueprint, request, jsonify
from app.models.database_models import Patient, DiagnosisRecord, Doctor, ChatConversation, DoctorConsultation
from app import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    """获取管理后台仪表盘统计数据"""
    try:
        # 基础统计
        total_patients = Patient.query.count()
        total_diagnoses = DiagnosisRecord.query.count()
        total_doctors = Doctor.query.count()
        total_consultations = DoctorConsultation.query.count()
        
        # 今日统计
        today = datetime.now().date()
        today_diagnoses = DiagnosisRecord.query.filter(
            func.date(DiagnosisRecord.diagnosed_at) == today
        ).count()
        
        today_patients = Patient.query.filter(
            func.date(Patient.created_at) == today
        ).count()
        
        # 本周统计
        week_ago = datetime.now() - timedelta(days=7)
        week_diagnoses = DiagnosisRecord.query.filter(
            DiagnosisRecord.diagnosed_at >= week_ago
        ).count()
        
        # 睡眠质量分布
        sleep_grade_stats = db.session.query(
            DiagnosisRecord.sleep_quality_grade,
            func.count(DiagnosisRecord.id).label('count')
        ).group_by(DiagnosisRecord.sleep_quality_grade).all()
        
        # 证型分布（取前10）
        syndrome_stats = db.session.query(
            DiagnosisRecord.final_diagnosis,
            func.count(DiagnosisRecord.id).label('count')
        ).group_by(DiagnosisRecord.final_diagnosis)\
         .order_by(desc('count'))\
         .limit(10).all()
        
        # 最近7天每日诊断趋势
        daily_stats = []
        for i in range(7):
            date = datetime.now().date() - timedelta(days=i)
            count = DiagnosisRecord.query.filter(
                func.date(DiagnosisRecord.diagnosed_at) == date
            ).count()
            daily_stats.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        daily_stats.reverse()
        
        return jsonify({
            'success': True,
            'data': {
                'overview': {
                    'total_patients': total_patients,
                    'total_diagnoses': total_diagnoses,
                    'total_doctors': total_doctors,
                    'total_consultations': total_consultations,
                    'today_diagnoses': today_diagnoses,
                    'today_patients': today_patients,
                    'week_diagnoses': week_diagnoses
                },
                'sleep_grade_distribution': [
                    {'grade': grade or '未评级', 'count': count} 
                    for grade, count in sleep_grade_stats
                ],
                'syndrome_distribution': [
                    {'syndrome': syndrome or '未确定', 'count': count} 
                    for syndrome, count in syndrome_stats
                ],
                'daily_trend': daily_stats
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取仪表盘数据失败: {str(e)}'
        }), 500

@admin_bp.route('/patients', methods=['GET'])
def get_patients():
    """获取患者列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        
        query = Patient.query
        
        # 搜索过滤
        if search:
            query = query.filter(
                db.or_(
                    Patient.name.like(f'%{search}%'),
                    Patient.phone.like(f'%{search}%')
                )
            )
        
        # 分页查询
        patients = query.order_by(desc(Patient.created_at))\
                      .paginate(page=page, per_page=per_page, error_out=False)
        
        # 获取每个患者的诊断次数
        patients_data = []
        for patient in patients.items:
            diagnosis_count = DiagnosisRecord.query.filter_by(patient_id=patient.id).count()
            patient_data = patient.to_dict()
            patient_data['diagnosis_count'] = diagnosis_count
            
            # 最近一次诊断
            latest_diagnosis = DiagnosisRecord.query.filter_by(patient_id=patient.id)\
                             .order_by(desc(DiagnosisRecord.diagnosed_at)).first()
            if latest_diagnosis:
                patient_data['latest_diagnosis'] = {
                    'grade': latest_diagnosis.sleep_quality_grade,
                    'syndrome': latest_diagnosis.final_diagnosis,
                    'date': latest_diagnosis.diagnosed_at.isoformat()
                }
            else:
                patient_data['latest_diagnosis'] = None
                
            patients_data.append(patient_data)
        
        return jsonify({
            'success': True,
            'data': {
                'patients': patients_data,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': patients.total,
                    'pages': patients.pages,
                    'has_next': patients.has_next,
                    'has_prev': patients.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取患者列表失败: {str(e)}'
        }), 500

@admin_bp.route('/diagnoses', methods=['GET'])
def get_diagnoses():
    """获取诊断记录列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        grade_filter = request.args.get('grade', '')
        syndrome_filter = request.args.get('syndrome', '')
        
        query = DiagnosisRecord.query.join(Patient)
        
        # 过滤条件
        if grade_filter:
            query = query.filter(DiagnosisRecord.sleep_quality_grade == grade_filter)
        if syndrome_filter:
            query = query.filter(DiagnosisRecord.final_diagnosis.like(f'%{syndrome_filter}%'))
        
        # 分页查询
        diagnoses = query.order_by(desc(DiagnosisRecord.diagnosed_at))\
                       .paginate(page=page, per_page=per_page, error_out=False)
        
        diagnoses_data = []
        for diagnosis in diagnoses.items:
            data = diagnosis.to_dict()
            # 添加患者信息
            if diagnosis.patient:
                data['patient_info'] = {
                    'name': diagnosis.patient.name,
                    'phone': diagnosis.patient.phone,
                    'age': diagnosis.patient.age,
                    'gender': diagnosis.patient.gender
                }
            else:
                data['patient_info'] = None
            diagnoses_data.append(data)
        
        return jsonify({
            'success': True,
            'data': {
                'diagnoses': diagnoses_data,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': diagnoses.total,
                    'pages': diagnoses.pages,
                    'has_next': diagnoses.has_next,
                    'has_prev': diagnoses.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取诊断记录失败: {str(e)}'
        }), 500

@admin_bp.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient_detail(patient_id):
    """获取患者详细信息"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        
        # 获取诊断历史
        diagnoses = DiagnosisRecord.query.filter_by(patient_id=patient_id)\
                   .order_by(desc(DiagnosisRecord.diagnosed_at)).all()
        
        # 获取聊天记录
        chats = ChatConversation.query.filter_by(patient_id=patient_id)\
               .order_by(desc(ChatConversation.created_at)).limit(50).all()
        
        # 获取医生咨询记录
        consultations = DoctorConsultation.query.filter_by(patient_id=patient_id)\
                       .order_by(desc(DoctorConsultation.created_at)).all()
        
        patient_data = patient.to_dict()
        patient_data['diagnoses'] = [d.to_dict() for d in diagnoses]
        patient_data['chat_history'] = [c.to_dict() for c in chats]
        patient_data['consultations'] = [c.to_dict() for c in consultations]
        
        return jsonify({
            'success': True,
            'data': patient_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取患者详情失败: {str(e)}'
        }), 500

@admin_bp.route('/diagnosis/<int:diagnosis_id>', methods=['GET'])
def get_diagnosis_detail(diagnosis_id):
    """获取诊断详细信息"""
    try:
        diagnosis = DiagnosisRecord.query.get_or_404(diagnosis_id)
        
        data = diagnosis.to_dict()
        
        # 添加患者信息
        if diagnosis.patient:
            data['patient_info'] = diagnosis.patient.to_dict()
        
        return jsonify({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取诊断详情失败: {str(e)}'
        }), 500

@admin_bp.route('/export/diagnoses', methods=['GET'])
def export_diagnoses():
    """导出诊断数据"""
    try:
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        query = DiagnosisRecord.query.join(Patient)
        
        # 时间范围过滤
        if start_date:
            query = query.filter(DiagnosisRecord.diagnosed_at >= start_date)
        if end_date:
            query = query.filter(DiagnosisRecord.diagnosed_at <= end_date)
        
        diagnoses = query.order_by(desc(DiagnosisRecord.diagnosed_at)).all()
        
        # 构建导出数据
        export_data = []
        for diagnosis in diagnoses:
            row = {
                '诊断ID': diagnosis.id,
                '患者姓名': diagnosis.patient.name if diagnosis.patient else '未知',
                '患者电话': diagnosis.patient.phone if diagnosis.patient else '未知',
                '年龄': diagnosis.patient.age if diagnosis.patient else '未知',
                '性别': diagnosis.patient.gender if diagnosis.patient else '未知',
                '睡眠质量等级': diagnosis.sleep_quality_grade,
                '总评分': diagnosis.total_sleep_score,
                '评分百分比': diagnosis.sleep_score_percentage,
                '最终证型': diagnosis.final_diagnosis,
                '诊断时间': diagnosis.diagnosed_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            export_data.append(row)
        
        return jsonify({
            'success': True,
            'data': export_data,
            'total': len(export_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'导出数据失败: {str(e)}'
        }), 500