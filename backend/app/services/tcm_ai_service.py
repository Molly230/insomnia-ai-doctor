from typing import Dict, List
from app.diagnosis.questionnaire import InsomniaQuestionnaire
from app.models.diagnosis_models import QuestionnaireAnswer, PatientAnswers

class TCMAIService:
    """中医AI分身服务"""
    
    def __init__(self):
        self.doctor_name = "中医师分身"
        self.greeting_messages = [
            f"您好！我是您的{self.doctor_name}，专注于失眠调理。",
            "我会通过专业的中医问诊，为您提供个性化的失眠治疗方案。",
            "请选择您需要的服务："
        ]
    
    def get_welcome_message(self, nickname: str = "朋友") -> str:
        """获取欢迎消息"""
        return f"""🌙 {nickname}，{self.greeting_messages[0]}

{self.greeting_messages[1]}

📋 点击"开始问诊"进行专业失眠评估
💬 或直接输入您的失眠问题，我来为您解答
📚 点击菜单了解更多中医知识

⚠️ 温馨提示：本系统仅供参考，如有严重症状请及时就医"""
    
    def get_consultation_start_message(self) -> str:
        """开始问诊的消息"""
        return f"""🔍 开始失眠专业问诊

我将通过{InsomniaQuestionnaire.get_questions().__len__()}个专业问题了解您的睡眠状况。

每个问题都很重要，请如实回答，这将帮助我为您制定最适合的调理方案。

准备好了吗？回复"开始"进入问诊 👇"""
    
    def get_question_message(self, question_index: int) -> str:
        """获取问题消息"""
        questions = InsomniaQuestionnaire.get_questions()
        
        if question_index >= len(questions):
            return "问诊已完成！"
        
        question = questions[question_index]
        total_questions = len(questions)
        
        # 构建选项文本
        options_text = ""
        for i, option in enumerate(question.options, 1):
            options_text += f"\n{i}. {option.label}"
        
        message = f"""📋 问题 {question_index + 1}/{total_questions}

【{question.category}】
{question.text}
{options_text}

💡 请回复选项数字（如：1）"""
        
        if question.type.value == "多选":
            message += "\n\n⚠️ 此题为多选题，可回复多个数字（如：1,3）"
            
        return message
    
    def parse_answer(self, user_input: str, question_index: int) -> List[str]:
        """解析用户答案"""
        questions = InsomniaQuestionnaire.get_questions()
        
        if question_index >= len(questions):
            return []
        
        question = questions[question_index]
        user_input = user_input.strip()
        
        try:
            if question.type.value == "多选":
                # 多选题处理: "1,3" 或 "1 3"
                numbers = user_input.replace(",", " ").split()
                selected_options = []
                
                for num_str in numbers:
                    num = int(num_str) - 1
                    if 0 <= num < len(question.options):
                        selected_options.append(question.options[num].value)
                
                return selected_options
            else:
                # 单选题处理
                num = int(user_input) - 1
                if 0 <= num < len(question.options):
                    return [question.options[num].value]
                
        except (ValueError, IndexError):
            pass
        
        return []
    
    def get_completion_message(self) -> str:
        """问诊完成消息"""
        return """🎉 问诊完成！

正在根据您的回答进行中医辨证分析...

📊 分析内容包括：
• 失眠证型判断
• 中药调理方案  
• 外治法建议
• 食疗调理方案
• 生活调养指导

请稍等片刻，马上为您生成个性化治疗方案 ⏳"""
    
    def get_diagnosis_result_message(self, diagnosis_result: Dict) -> str:
        """诊断结果消息"""
        # TODO: 根据实际诊断结果生成消息
        return f"""📋 您的失眠诊断报告

🔸 证型诊断：{diagnosis_result.get('syndrome_type', '待分析')}
🔸 置信度：{diagnosis_result.get('confidence', 0):.0%}

📄 详细报告已生成，包含：
• 中药调理方案
• 外治法指导  
• 食疗建议
• 生活调养

回复"查看报告"获取完整治疗方案 📖"""
    
    def get_help_message(self) -> str:
        """帮助信息"""
        return """📖 使用说明

🔹 开始问诊：完成19题专业评估
🔹 查看报告：获取个性化治疗方案
🔹 中医咨询：随时提问失眠相关问题

⭐ 问诊流程：
1️⃣ 点击"开始问诊"
2️⃣ 依次回答19个问题  
3️⃣ 获得证型诊断
4️⃣ 查看治疗方案

❓ 常见问题：
• 如何重新开始？回复"重新问诊"
• 忘记在哪一题？回复"当前进度"
• 有其他问题？直接描述症状即可

💊 温馨提示：建议在安静环境下完成问诊，确保回答准确性"""
    
    def get_error_message(self, error_type: str = "general") -> str:
        """错误提示消息"""
        error_messages = {
            "invalid_answer": "❌ 请输入有效的选项数字",
            "session_expired": "⏰ 会话已过期，请重新开始问诊",
            "system_error": "⚠️ 系统暂时繁忙，请稍后重试",
            "general": "❓ 抱歉，我没理解您的意思，请重新输入"
        }
        
        return error_messages.get(error_type, error_messages["general"])
    
    def chat_with_user(self, user_message: str) -> str:
        """与用户进行中医咨询对话"""
        # TODO: 集成AI对话功能
        # 这里可以接入大语言模型进行智能对话
        
        # 临时简单回复逻辑
        if "失眠" in user_message or "睡不着" in user_message:
            return """失眠确实困扰很多人。从中医角度来看，失眠的原因主要有：

🔸 心肾不交：心火上炎，肾水不济
🔸 肝郁气滞：情志不遂，肝气郁结  
🔸 心脾两虚：思虑过度，气血不足
🔸 阴虚火旺：阴液亏损，虚火扰神

想要准确了解您的具体证型，建议完成专业问诊评估。

点击"开始问诊"获得个性化调理方案 📋"""
        
        elif "怎么" in user_message or "如何" in user_message:
            return """中医调理失眠通常采用三位一体的方法：

💊 中药调理：
根据证型选择合适方剂，如甘麦大枣汤、安神定志丸等

🖐️ 外治法：
耳穴压豆、足浴安神、穴位按摩等

🍲 食疗养生：
百合莲子粥、酸枣仁茶等药食同源

具体用什么方法，需要先辨证论治。建议您完成问诊，我会为您制定专属方案！"""
        
        else:
            return """感谢您的咨询！

我是专业的中医失眠调理分身，可以为您提供：
• 失眠证型诊断
• 中药调理方案
• 外治法指导
• 食疗建议

如需详细分析，请点击"开始问诊"
如有具体问题，欢迎直接描述您的症状 😊"""