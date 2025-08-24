// 直接在前端定义19个问诊问题，不依赖后端API
const QUESTIONS = [
  {
    id: 1,
    text: "您认为自己的睡眠状况如何？",
    type: "单选",
    options: [
      { value: "好", label: "好" },
      { value: "一般", label: "一般" },
      { value: "较差", label: "较差" }
    ],
    category: "睡眠质量"
  },
  {
    id: 2,
    text: "通常情况下，您从上床准备睡觉到真正入睡需要多长时间？",
    type: "单选",
    options: [
      { value: "5分钟以内", label: "5分钟以内" },
      { value: "6-15分钟", label: "6-15分钟" },
      { value: "16-30分钟", label: "16-30分钟" },
      { value: "31-60分钟", label: "31-60分钟" },
      { value: "60分钟以上", label: "60分钟以上" }
    ],
    category: "入睡时间"
  },
  {
    id: 3,
    text: "过去一个月内，您每天夜间睡眠时间有多长？",
    type: "单选",
    options: [
      { value: "8小时及以上", label: "8小时及以上" },
      { value: "7-8小时", label: "7-8小时" },
      { value: "6-7小时", label: "6-7小时" },
      { value: "5-6小时", label: "5-6小时" },
      { value: "5小时以下", label: "5小时以下" }
    ],
    category: "睡眠时长"
  },
  {
    id: 4,
    text: "过去一个月内，您夜间平均醒来的次数大约是？",
    type: "单选",
    options: [
      { value: "几乎不醒来", label: "几乎不醒来" },
      { value: "1次", label: "1次" },
      { value: "2-3次", label: "2-3次" },
      { value: "4次及以上", label: "4次及以上" }
    ],
    category: "夜醒次数"
  },
  {
    id: 5,
    text: "过去一个月内，您夜间醒来后，再次入睡通常需要多长时间？",
    type: "单选",
    options: [
      { value: "5分钟以内", label: "5分钟以内" },
      { value: "6-15分钟", label: "6-15分钟" },
      { value: "16-30分钟", label: "16-30分钟" },
      { value: "31-60分钟", label: "31-60分钟" },
      { value: "60分钟以上", label: "60分钟以上" }
    ],
    category: "再入睡时间"
  },
  {
    id: 6,
    text: "过去一个月内，您是否会在白天出现不可抗拒的睡眠欲望（如工作、学习或开车时突然想睡觉）？",
    type: "单选",
    options: [
      { value: "几乎没有", label: "几乎没有" },
      { value: "每周1-2次", label: "每周1-2次" },
      { value: "每周3-5次", label: "每周3-5次" },
      { value: "每天都有", label: "每天都有" }
    ],
    category: "白天嗜睡"
  },
  {
    id: 7,
    text: "您有怎样的睡眠困扰？（多选）",
    type: "多选",
    options: [
      { value: "反复清醒", label: "反复清醒" },
      { value: "整夜做梦", label: "整夜做梦" },
      { value: "晨起疲倦", label: "晨起疲倦" },
      { value: "难以入眠", label: "难以入眠" }
    ],
    category: "睡眠困扰"
  },
  {
    id: 8,
    text: "您是否服用过以下类药物？（多选）",
    type: "多选",
    options: [
      { value: "苯二氮卓类：地西泮、劳拉西泮", label: "苯二氮卓类：地西泮、劳拉西泮" },
      { value: "非苯二氮卓类：唑吡坦、右佐匹克隆", label: "非苯二氮卓类：唑吡坦、右佐匹克隆" },
      { value: "褪黑素受体激动剂：雷美替胺", label: "褪黑素受体激动剂：雷美替胺" },
      { value: "食欲素受体拮抗剂：苏沃雷生", label: "食欲素受体拮抗剂：苏沃雷生" },
      { value: "抗抑郁药物：曲唑酮、米氮平", label: "抗抑郁药物：曲唑酮、米氮平" }
    ],
    category: "用药史"
  },
  {
    id: 9,
    text: "您服用安眠药时长多久？",
    type: "单选",
    options: [
      { value: "1个月以内", label: "1个月以内" },
      { value: "1-3个月（慢性）", label: "1-3个月（慢性）" },
      { value: "3个月以上（高级）", label: "3个月以上（高级）" }
    ],
    category: "用药时长"
  },
  {
    id: 10,
    text: "您是否经常精神压力大/情绪紧张？",
    type: "单选",
    options: [
      { value: "是", label: "是" },
      { value: "否", label: "否" }
    ],
    category: "精神状态"
  },
  {
    id: 11,
    text: "您近期有无如下问题？",
    type: "单选",
    options: [
      { value: "时有耳鸣", label: "时有耳鸣" },
      { value: "时实疲乏，乏力周身疲", label: "时实疲乏，乏力周身疲" },
      { value: "腹胀/腹泻不适", label: "腹胀/腹泻不适" }
    ],
    category: "身体症状"
  },
  {
    id: 12,
    text: "您是否经常周身酸痛/骨节疼痛？",
    type: "单选",
    options: [
      { value: "是", label: "是" },
      { value: "否", label: "否" }
    ],
    category: "疼痛症状"
  },
  {
    id: 13,
    text: "您近期有无如下问题？",
    type: "单选",
    options: [
      { value: "夜间遗精/遗尿，心悸加速", label: "夜间遗精/遗尿，心悸加速" },
      { value: "皮肤蚊疹，发骚麻疹", label: "皮肤蚊疹，发骚麻疹" },
      { value: "咳嗽/气短/难呼气", label: "咳嗽/气短/难呼气" }
    ],
    category: "特殊症状"
  },
  {
    id: 14,
    text: "您是否持续电子产品超过3小时/天？",
    type: "单选",
    options: [
      { value: "是", label: "是" },
      { value: "否", label: "否" }
    ],
    category: "生活习惯"
  },
  {
    id: 15,
    text: "您近期有无如下问题？",
    type: "单选",
    options: [
      { value: "面色暗黑，无精打采", label: "面色暗黑，无精打采" },
      { value: "容易受惊，害怕", label: "容易受惊，害怕" },
      { value: "夜间盗汗", label: "夜间盗汗" }
    ],
    category: "中医症状"
  },
  {
    id: 16,
    text: "您是否劳心耗神过度？",
    type: "单选",
    options: [
      { value: "是", label: "是" },
      { value: "否", label: "否" }
    ],
    category: "精神消耗"
  },
  {
    id: 17,
    text: "您近期有无如下问题？",
    type: "单选",
    options: [
      { value: "腰酸无力", label: "腰酸无力" }
    ],
    category: "肾虚症状"
  },
  {
    id: 18,
    text: "您是否用脑过度？",
    type: "单选",
    options: [
      { value: "是", label: "是" },
      { value: "否", label: "否" }
    ],
    category: "用脑过度"
  },
  {
    id: 19,
    text: "您近期有无如下问题？",
    type: "多选",
    options: [
      { value: "好忘事，记忆力下降", label: "好忘事，记忆力下降" },
      { value: "白天嗜睡", label: "白天嗜睡" },
      { value: "偏头痛/头痛", label: "偏头痛/头痛" }
    ],
    category: "认知功能"
  }
]

// 模拟API调用，直接返回问题
export const getQuestions = async () => {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 500))
  return { data: QUESTIONS }
}

// 模拟提交答案
export const submitQuestionnaireAnswers = async (answers) => {
  await new Promise(resolve => setTimeout(resolve, 1000))
  console.log('提交的答案:', answers)
  return { success: true, message: '问诊提交成功' }
}

export default { getQuestions, submitQuestionnaireAnswers }