from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class QuestionType(Enum):
    SINGLE_CHOICE = "单选"
    MULTIPLE_CHOICE = "多选"
    
@dataclass
class QuestionOption:
    value: str
    label: str
    score: float = 0.0  # 选项对应的分值

@dataclass  
class Question:
    id: int
    text: str
    type: QuestionType
    options: List[QuestionOption]
    category: str  # 问题分类，用于后续诊断

class InsomniaQuestionnaire:
    """失眠问诊表"""
    
    QUESTIONS = [
        Question(
            id=1,
            text="您认为自己的睡眠状况如何？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("好", "好"),
                QuestionOption("一般", "一般"), 
                QuestionOption("较差", "较差"),
                QuestionOption("差", "差")
            ],
            category="睡眠质量"
        ),
        Question(
            id=2,
            text="您感觉向上几个月（大约准备睡觉时）是正常入睡需要多长时间？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("5分钟以内", "5分钟以内"),
                QuestionOption("6-15分钟", "6-15分钟"),
                QuestionOption("16-30分钟", "16-30分钟"),
                QuestionOption("31-60分钟", "31-60分钟"),
                QuestionOption("60分钟以上", "60分钟以上")
            ],
            category="入睡时间"
        ),
        Question(
            id=3,
            text="过去一个月内，您每天夜间睡眠时间多长？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("8小时以上", "8小时以上"),
                QuestionOption("6-7小时", "6-7小时"),
                QuestionOption("5小时", "5小时"),
                QuestionOption("5小时以下", "5小时以下")
            ],
            category="睡眠时长"
        ),
        Question(
            id=4,
            text="过去一个月内，您夜间平均醒来的次数大约是？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("从来没有", "从来没有"),
                QuestionOption("1次", "1次"),
                QuestionOption("2-3次", "2-3次"),
                QuestionOption("4次及以上", "4次及以上")
            ],
            category="夜醒次数"
        ),
        Question(
            id=5,
            text="过去一个月内，您夜间醒来后，再次入睡通常需要长时间？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("5分钟以内", "5分钟以内"),
                QuestionOption("6-15分钟", "6-15分钟"),
                QuestionOption("16-30分钟", "16-30分钟"),
                QuestionOption("31-60分钟", "31-60分钟"),
                QuestionOption("60分钟以上", "60分钟以上")
            ],
            category="再入睡时间"
        ),
        Question(
            id=6,
            text="过去一个月内，您是否全夜在白天想出现不可抗拒的睡眠欲望（如工作、学习或开车时突然想睡觉）？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("从来没有", "从来没有"),
                QuestionOption("每周1-2次", "每周1-2次"),
                QuestionOption("每周3-5次", "每周3-5次"),
                QuestionOption("每天都有", "每天都有")
            ],
            category="日间嗜睡"
        ),
        Question(
            id=7,
            text="您有怎样的睡眠困扰？（多选）",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("反复清醒", "反复清醒"),
                QuestionOption("整夜服药", "整夜服药"),
                QuestionOption("晨起疲倦", "晨起疲倦"),
                QuestionOption("嗜睡状态", "嗜睡状态")
            ],
            category="睡眠困扰"
        ),
        Question(
            id=8,
            text="您是否有以下几种失眠症状？（多选）",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("形寒意冷", "形寒意冷：畏寒怕冷"),
                QuestionOption("非常 -- 病虚热", "非常 -- 病虚热：虚火内生，古代叫虚痿"),
                QuestionOption("液黑青 -- 冷活动", "液黑青 -- 冷活动：血液音调，古代叫血痿"),
                QuestionOption("食欲变化侵扰打", "食欲变化侵扰打：吾饮食失调，古代叫食积"),
                QuestionOption("抑郁低落", "抑郁低落：由血气，来源于"
            ],
            category="中医症状"
        ),
        Question(
            id=9,
            text="您服用安眠药时长多久？",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("1个月以内", "1个月以内"),
                QuestionOption("1-6个月", "1-6个月"),
                QuestionOption("3个月以上（高级）", "3个月以上（高级）")
            ],
            category="用药史"
        ),
        Question(
            id=10,
            text="您是否经常精神压力大/情绪紧张？口是/口否",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="精神状态"
        ),
        Question(
            id=11,
            text="您是否经常思虑过多？口是/口否",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="精神状态"
        ),
        Question(
            id=12,
            text="您是否经常心烦身热/背怕疼痛？口是/口否",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="身体症状"
        ),
        Question(
            id=13,
            text="您近期有无以下问题？",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("夜间盗汗/胸闷", "夜间盗汗/胸闷，心跳加速"),
                QuestionOption("皮肤瘙痒", "皮肤瘙痒，发烧解除"),
                QuestionOption("咳嗽/气短", "咳嗽/气短，呼吸急促")
            ],
            category="伴随症状"
        ),
        Question(
            id=14,
            text="您是否接触电子产品过3小时/天？口是/口否",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="生活习惯"
        ),
        Question(
            id=15,
            text="您近期有无以下问题？",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("面色苍黄", "面色苍黄，无神打采"),
                QuestionOption("食胃寒冷", "食胃寒冷，脘胁胀痛"),
                QuestionOption("夜间盗汗", "夜间盗汗")
            ],
            category="面色脾胃"
        ),
        Question(
            id=16,
            text="您是否舌头心悸？口是/口否",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="心脏症状"
        ),
        Question(
            id=17,
            text="您近期有无以下问题？",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("腰酸无力", "腰酸无力")
            ],
            category="腰肾症状"
        ),
        Question(
            id=18,
            text="您是否舌头心悸？口是/口否",
            type=QuestionType.SINGLE_CHOICE,
            options=[
                QuestionOption("是", "是"),
                QuestionOption("否", "否")
            ],
            category="心脏症状"
        ),
        Question(
            id=19,
            text="您近期有无以下问题？",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption("对事业", "对事业，记忆力下降"),
                QuestionOption("自天嗜睡", "自天嗜睡，夜间失眠"),
                QuestionOption("脖头痛/头痛", "脖头痛/头痛")
            ],
            category="神经症状"
        )
    ]
    
    @classmethod
    def get_questions(cls) -> List[Question]:
        """获取所有问诊问题"""
        return cls.QUESTIONS
    
    @classmethod
    def get_question_by_id(cls, question_id: int) -> Optional[Question]:
        """根据ID获取问题"""
        for question in cls.QUESTIONS:
            if question.id == question_id:
                return question
        return None