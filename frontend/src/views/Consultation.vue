<template>
  <div class="consultation">
    <el-card class="consultation-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Edit /></el-icon>
          <span>失眠问诊表</span>
          <div class="progress-info">
            问题 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}
          </div>
        </div>
      </template>

      <!-- 进度条 -->
      <el-progress 
        :percentage="progressPercentage" 
        :stroke-width="8"
        status="success"
        class="progress-bar"
      />

      <!-- 问题内容 -->
      <div v-if="!isLoading && currentQuestion" class="question-section">
        <div class="question-header">
          <h3>{{ currentQuestion.text }}</h3>
          <el-tag :type="getQuestionTypeColor(currentQuestion.category)">
            {{ currentQuestion.category }}
          </el-tag>
        </div>

        <!-- 单选题 -->
        <div v-if="currentQuestion.type === '单选'" class="options-section">
          <el-radio-group 
            v-model="currentAnswer" 
            @change="handleAnswerChange"
            class="radio-group"
          >
            <el-radio 
              v-for="option in currentQuestion.options" 
              :key="option.value"
              :label="option.value"
              class="radio-option"
            >
              {{ option.label }}
            </el-radio>
          </el-radio-group>
        </div>

        <!-- 多选题 -->
        <div v-else-if="currentQuestion.type === '多选'" class="options-section">
          <el-checkbox-group 
            v-model="currentMultipleAnswers" 
            @change="handleMultipleAnswerChange"
            class="checkbox-group"
          >
            <el-checkbox 
              v-for="option in currentQuestion.options" 
              :key="option.value"
              :label="option.value"
              class="checkbox-option"
            >
              {{ option.label }}
            </el-checkbox>
          </el-checkbox-group>
        </div>

        <!-- 导航按钮 -->
        <div class="navigation-buttons">
          <el-button 
            @click="previousQuestion" 
            :disabled="currentQuestionIndex === 0"
          >
            <el-icon><ArrowLeft /></el-icon>
            上一题
          </el-button>
          
          <el-button 
            v-if="currentQuestionIndex < totalQuestions - 1"
            type="primary" 
            @click="nextQuestion"
            :disabled="!hasAnswer"
          >
            下一题
            <el-icon><ArrowRight /></el-icon>
          </el-button>
          
          <el-button 
            v-else
            type="success" 
            @click="submitAnswers"
            :disabled="!hasAnswer"
            :loading="isSubmitting"
          >
            提交问诊
            <el-icon><Check /></el-icon>
          </el-button>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-else-if="isLoading" class="loading-section">
        <el-skeleton :rows="5" animated />
      </div>

      <!-- 完成状态 -->
      <div v-else-if="isCompleted" class="completed-section">
        <el-result
          icon="success"
          title="问诊完成"
          sub-title="正在分析您的症状，请稍候..."
        >
          <template #extra>
            <el-button type="primary" @click="viewResults">
              查看诊断结果
              <el-icon><Right /></el-icon>
            </el-button>
          </template>
        </el-result>
      </div>
    </el-card>

    <!-- 答题进度 -->
    <el-card class="answer-summary" shadow="hover" v-if="!isLoading && !isCompleted">
      <template #header>
        <div class="summary-header">
          <el-icon><List /></el-icon>
          <span>答题进度</span>
        </div>
      </template>
      
      <div class="answer-grid">
        <div 
          v-for="(answer, index) in allAnswers" 
          :key="index"
          class="answer-item"
          :class="{ 
            'answered': answer.length > 0, 
            'current': index === currentQuestionIndex 
          }"
          @click="jumpToQuestion(index)"
        >
          {{ index + 1 }}
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElLoading } from 'element-plus'
import { 
  Edit, ArrowLeft, ArrowRight, Check, Right, List 
} from '@element-plus/icons-vue'
import { getQuestions, submitQuestionnaireAnswers } from '../api/consultation'

const router = useRouter()

// 响应式数据
const isLoading = ref(true)
const isSubmitting = ref(false)
const isCompleted = ref(false)
const questions = ref([])
const currentQuestionIndex = ref(0)
const allAnswers = ref([])

// 当前答案
const currentAnswer = ref('')
const currentMultipleAnswers = ref([])

// 计算属性
const totalQuestions = computed(() => questions.value.length)
const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])
const progressPercentage = computed(() => 
  Math.round(((currentQuestionIndex.value + 1) / totalQuestions.value) * 100)
)

const hasAnswer = computed(() => {
  if (!currentQuestion.value) return false
  
  if (currentQuestion.value.type === '单选') {
    return currentAnswer.value !== ''
  } else if (currentQuestion.value.type === '多选') {
    return currentMultipleAnswers.value.length > 0
  }
  return false
})

// 方法
const loadQuestions = async () => {
  try {
    const response = await getQuestions()
    questions.value = response.data
    // 初始化答案数组
    allAnswers.value = Array(questions.value.length).fill([])
    isLoading.value = false
  } catch (error) {
    ElMessage.error('加载问题失败')
    console.error(error)
  }
}

const handleAnswerChange = (value) => {
  allAnswers.value[currentQuestionIndex.value] = [value]
}

const handleMultipleAnswerChange = (values) => {
  allAnswers.value[currentQuestionIndex.value] = values
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    saveCurrentAnswer()
    currentQuestionIndex.value++
    loadQuestionAnswer()
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    saveCurrentAnswer()
    currentQuestionIndex.value--
    loadQuestionAnswer()
  }
}

const jumpToQuestion = (index) => {
  if (index >= 0 && index < totalQuestions.value) {
    saveCurrentAnswer()
    currentQuestionIndex.value = index
    loadQuestionAnswer()
  }
}

const saveCurrentAnswer = () => {
  if (currentQuestion.value.type === '单选') {
    allAnswers.value[currentQuestionIndex.value] = currentAnswer.value ? [currentAnswer.value] : []
  } else if (currentQuestion.value.type === '多选') {
    allAnswers.value[currentQuestionIndex.value] = [...currentMultipleAnswers.value]
  }
}

const loadQuestionAnswer = () => {
  const answers = allAnswers.value[currentQuestionIndex.value] || []
  
  if (currentQuestion.value.type === '单选') {
    currentAnswer.value = answers[0] || ''
  } else if (currentQuestion.value.type === '多选') {
    currentMultipleAnswers.value = [...answers]
  }
}

const submitAnswers = async () => {
  saveCurrentAnswer()
  
  // 检查是否所有问题都已回答
  const unansweredQuestions = allAnswers.value.findIndex(answers => answers.length === 0)
  if (unansweredQuestions !== -1) {
    ElMessage.warning(`请回答第 ${unansweredQuestions + 1} 题`)
    jumpToQuestion(unansweredQuestions)
    return
  }

  try {
    isSubmitting.value = true
    
    // 格式化答案数据
    const formattedAnswers = allAnswers.value.map((answers, index) => ({
      question_id: questions.value[index].id,
      selected_options: answers
    }))

    await submitQuestionnaireAnswers({ answers: formattedAnswers })
    
    ElMessage.success('问诊提交成功')
    isCompleted.value = true
    
    // 3秒后跳转到诊断结果页面
    setTimeout(() => {
      router.push('/diagnosis')
    }, 3000)
    
  } catch (error) {
    ElMessage.error('提交失败，请重试')
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
}

const viewResults = () => {
  router.push('/diagnosis')
}

const getQuestionTypeColor = (category) => {
  const colorMap = {
    '睡眠质量': 'primary',
    '入睡时间': 'success',
    '睡眠时长': 'warning',
    '夜醒次数': 'danger',
    '中医症状': 'info',
    '精神状态': 'primary',
    '身体症状': 'warning'
  }
  return colorMap[category] || 'info'
}

// 生命周期
onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.consultation {
  max-width: 800px;
  margin: 0 auto;
}

.consultation-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header span {
  font-size: 18px;
  font-weight: bold;
  margin-left: 8px;
}

.progress-info {
  color: #909399;
  font-size: 14px;
}

.progress-bar {
  margin-bottom: 30px;
}

.question-section {
  min-height: 400px;
}

.question-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
}

.question-header h3 {
  margin: 0;
  color: #2c3e50;
  flex: 1;
  margin-right: 20px;
}

.options-section {
  margin-bottom: 40px;
}

.radio-group,
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.radio-option,
.checkbox-option {
  padding: 15px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.radio-option:hover,
.checkbox-option:hover {
  border-color: #409eff;
  background: #f0f9ff;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
}

.loading-section {
  padding: 40px;
}

.completed-section {
  padding: 20px;
}

.answer-summary {
  margin-bottom: 20px;
}

.summary-header {
  display: flex;
  align-items: center;
}

.summary-header span {
  margin-left: 8px;
  font-weight: bold;
}

.answer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 10px;
  margin-top: 15px;
}

.answer-item {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
}

.answer-item:hover {
  border-color: #409eff;
}

.answer-item.answered {
  background: #67c23a;
  border-color: #67c23a;
  color: white;
}

.answer-item.current {
  border-color: #409eff;
  background: #409eff;
  color: white;
}
</style>