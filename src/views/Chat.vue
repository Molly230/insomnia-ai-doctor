<template>
  <div class="chat-container">
    <!-- 聊天标题 -->
    <div class="chat-header">
      <div class="header-content">
        <el-icon class="chat-icon"><ChatLineRound /></el-icon>
        <div class="header-text">
          <h2>中医智能助手</h2>
          <p>专业的中医失眠健康指导，基于传统中医理论为您答疑解惑</p>
        </div>
        <div class="header-status">
          <el-tag :type="isOnline ? 'success' : 'danger'" size="small">
            {{ isOnline ? '在线' : '离线' }}
          </el-tag>
        </div>
      </div>
    </div>

    <!-- 聊天消息区域 -->
    <div class="chat-messages" ref="messagesContainer">
      <div class="messages-wrapper">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="welcome-message">
          <el-card shadow="never">
            <div class="welcome-content">
              <el-icon size="48" color="#409EFF"><UserFilled /></el-icon>
              <h3>欢迎使用中医智能助手！</h3>
              <p>您可以咨询以下问题：</p>
              <el-row :gutter="12" class="quick-questions">
                <el-col :span="12">
                  <el-button 
                    text 
                    size="small" 
                    @click="sendQuickQuestion('失眠是什么原因引起的？')"
                  >
                    失眠原因
                  </el-button>
                </el-col>
                <el-col :span="12">
                  <el-button 
                    text 
                    size="small" 
                    @click="sendQuickQuestion('失眠有哪些证型？')"
                  >
                    证型分类
                  </el-button>
                </el-col>
                <el-col :span="12">
                  <el-button 
                    text 
                    size="small" 
                    @click="sendQuickQuestion('有什么穴位可以治疗失眠？')"
                  >
                    穴位治疗
                  </el-button>
                </el-col>
                <el-col :span="12">
                  <el-button 
                    text 
                    size="small" 
                    @click="sendQuickQuestion('失眠吃什么比较好？')"
                  >
                    食疗建议
                  </el-button>
                </el-col>
                <el-col :span="12">
                  <el-button 
                    text 
                    size="small" 
                    @click="sendQuickQuestion('失眠患者生活中要注意什么？')"
                  >
                    生活调理
                  </el-button>
                </el-col>
                <el-col :span="12">
                  <el-button 
                    text 
                    size="small" 
                    @click="sendQuickQuestion('失眠需要用药吗？')"
                  >
                    用药指导
                  </el-button>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </div>

        <!-- 聊天消息 -->
        <div
          v-for="(message, index) in messages"
          :key="message.id"
          class="message-item"
          :class="{ 'user-message': message.role === 'user', 'assistant-message': message.role === 'assistant' }"
        >
          <div class="message-avatar">
            <el-avatar 
              :size="40" 
              :src="message.role === 'user' ? '/user-avatar.png' : '/tcm-avatar.png'"
            >
              <el-icon v-if="message.role === 'user'"><User /></el-icon>
              <el-icon v-else><Memo /></el-icon>
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              <div class="message-text" v-html="formatMessage(message.content)"></div>
              <div class="message-time">
                {{ formatTime(message.timestamp) }}
              </div>
            </div>
          </div>
        </div>

        <!-- 加载提示 -->
        <div v-if="isLoading" class="message-item assistant-message">
          <div class="message-avatar">
            <el-avatar :size="40">
              <el-icon><Memo /></el-icon>
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-bubble loading">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <div class="loading-text">中医助手正在思考...</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input">
      <el-row :gutter="12" class="input-row">
        <el-col :span="20">
          <el-input
            v-model="newMessage"
            type="textarea"
            :rows="2"
            placeholder="请输入您的健康问题..."
            maxlength="500"
            show-word-limit
            @keydown.enter="handleEnter"
            @keydown.ctrl.enter="sendMessage"
            :disabled="isLoading"
          />
        </el-col>
        <el-col :span="4">
          <el-button
            type="primary"
            size="large"
            @click="sendMessage"
            :loading="isLoading"
            :disabled="!newMessage.trim() || isLoading"
            class="send-button"
          >
            <el-icon><Promotion /></el-icon>
            发送
          </el-button>
        </el-col>
      </el-row>
      <div class="input-tips">
        <el-text size="small" type="info">
          💡 按 Ctrl + Enter 快速发送 | Enter 换行 | 
          <el-button text size="small" @click="clearChat">清空聊天</el-button>
        </el-text>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="chat-actions">
      <el-button-group size="small">
        <el-button @click="exportChat" :disabled="messages.length === 0">
          <el-icon><Download /></el-icon>
          导出对话
        </el-button>
        <el-button @click="showKnowledgeTopics">
          <el-icon><Reading /></el-icon>
          知识库
        </el-button>
        <el-button @click="showHelp">
          <el-icon><QuestionFilled /></el-icon>
          帮助
        </el-button>
      </el-button-group>
    </div>

    <!-- 知识库主题对话框 -->
    <el-dialog
      v-model="knowledgeDialogVisible"
      title="中医知识库"
      width="50%"
    >
      <div v-if="knowledgeTopics.length > 0">
        <el-row :gutter="16">
          <el-col :span="8" v-for="topic in knowledgeTopics" :key="topic.topic">
            <el-card class="topic-card" shadow="hover" @click="selectTopic(topic)">
              <div class="topic-title">{{ topic.topic }}</div>
              <div class="topic-keywords">
                <el-tag 
                  v-for="keyword in topic.keywords.slice(0, 3)" 
                  :key="keyword"
                  size="small"
                  class="topic-tag"
                >
                  {{ keyword }}
                </el-tag>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div v-else>
        <el-empty description="暂无知识库内容" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  ChatLineRound, 
  UserFilled, 
  User, 
  Memo, 
  Promotion, 
  Download, 
  Reading,
  QuestionFilled 
} from '@element-plus/icons-vue'
import { chatAPI } from '../api/chatAPI'

// 响应式数据
const messages = ref([])
const newMessage = ref('')
const isLoading = ref(false)
const isOnline = ref(true)
const conversationId = ref('')
const messagesContainer = ref(null)
const knowledgeDialogVisible = ref(false)
const knowledgeTopics = ref([])

// 用户信息
const userId = ref('user-' + Date.now())

// 组件挂载时初始化
onMounted(() => {
  console.log('中医智能助手已加载')
  checkServiceStatus()
  loadKnowledgeTopics()
})

// 监听消息变化，自动滚动到底部
watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })

// 发送消息
const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  
  const userMessageContent = newMessage.value.trim()
  newMessage.value = ''
  
  // 添加用户消息到界面
  const userMessage = {
    id: 'user-' + Date.now(),
    role: 'user',
    content: userMessageContent,
    timestamp: new Date().toISOString()
  }
  messages.value.push(userMessage)
  
  // 显示加载状态
  isLoading.value = true
  
  try {
    // 调用中医智能助手
    const response = await chatAPI.sendMessage({
      message: userMessageContent,
      conversationId: conversationId.value,
      userId: userId.value
    })
    
    if (response.success) {
      // 更新对话ID
      conversationId.value = response.data.conversationId
      
      // 添加助手回复到界面
      const aiMessage = {
        id: response.data.message.id,
        role: 'assistant',
        content: response.data.message.content,
        timestamp: response.data.message.timestamp
      }
      messages.value.push(aiMessage)
    } else {
      throw new Error(response.error || '智能助手响应异常')
    }
    
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送失败: ' + error.message)
    
    // 添加错误提示消息
    const errorMessage = {
      id: 'error-' + Date.now(),
      role: 'assistant',
      content: '抱歉，服务暂时不可用。请稍后重试，或直接咨询专业中医师。\n\n💡 **建议**：您可以先完成我们的专业问卷获取初步诊断建议。',
      timestamp: new Date().toISOString()
    }
    messages.value.push(errorMessage)
    isOnline.value = false
  } finally {
    isLoading.value = false
  }
}

// 快速问题
const sendQuickQuestion = (question) => {
  newMessage.value = question
  sendMessage()
}

// 处理Enter键
const handleEnter = (e) => {
  if (e.ctrlKey) {
    e.preventDefault()
    sendMessage()
  }
}

// 格式化消息内容
const formatMessage = (content) => {
  return content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/🔹 \*\*(.*?)\*\*/g, '<strong style="color: #409EFF;">🔹 $1</strong>')
    .replace(/🟡 \*\*(.*?)\*\*/g, '<strong style="color: #E6A23C;">🟡 $1</strong>')
    .replace(/🎯 \*\*(.*?)\*\*/g, '<strong style="color: #67C23A;">🎯 $1</strong>')
    .replace(/🍵 \*\*(.*?)\*\*/g, '<strong style="color: #909399;">🍵 $1</strong>')
    .replace(/💊 \*\*(.*?)\*\*/g, '<strong style="color: #F56C6C;">💊 $1</strong>')
    .replace(/⚠️ \*\*(.*?)\*\*/g, '<strong style="color: #F56C6C;">⚠️ $1</strong>')
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) {
    return '刚刚'
  } else if (diff < 3600000) {
    return Math.floor(diff / 60000) + '分钟前'
  } else if (diff < 86400000) {
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else {
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 清空聊天
const clearChat = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有聊天记录吗？', '确认', {
      type: 'warning'
    })
    messages.value = []
    conversationId.value = ''
    ElMessage.success('聊天记录已清空')
  } catch {
    // 用户取消
  }
}

// 导出聊天记录
const exportChat = () => {
  const chatData = messages.value.map(msg => ({
    role: msg.role === 'user' ? '用户' : '中医助手',
    content: msg.content.replace(/<[^>]*>/g, ''),
    time: formatTime(msg.timestamp)
  }))
  
  const text = chatData.map(msg => `${msg.role} (${msg.time}):\n${msg.content}\n`).join('\n')
  
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `中医助手对话记录-${new Date().toLocaleDateString()}.txt`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('对话记录已导出')
}

// 检查服务状态
const checkServiceStatus = async () => {
  try {
    await chatAPI.healthCheck()
    isOnline.value = true
  } catch {
    isOnline.value = false
  }
}

// 加载知识库主题
const loadKnowledgeTopics = async () => {
  try {
    const response = await chatAPI.getKnowledgeTopics()
    if (response.success) {
      knowledgeTopics.value = response.data.topics
    }
  } catch (error) {
    console.error('加载知识库失败:', error)
  }
}

// 显示知识库主题
const showKnowledgeTopics = () => {
  knowledgeDialogVisible.value = true
}

// 选择知识库主题
const selectTopic = (topic) => {
  knowledgeDialogVisible.value = false
  const question = `请介绍一下${topic.topic}`
  sendQuickQuestion(question)
}

// 显示帮助
const showHelp = () => {
  ElMessageBox.alert(
    '使用说明：\n\n1. 直接输入您的健康问题\n2. 点击快捷问题快速咨询\n3. Ctrl+Enter快速发送\n4. 可以导出对话记录\n5. 查看知识库获取更多信息\n\n⚠️ 重要提醒：AI建议仅供参考，严重症状请及时就医！',
    '使用帮助',
    { type: 'info' }
  )
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 180px);
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-header {
  background: linear-gradient(135deg, #67C23A 0%, #85CE61 100%);
  color: white;
  padding: 20px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-icon {
  font-size: 32px;
  margin-right: 15px;
}

.header-text h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.header-text p {
  margin: 5px 0 0;
  opacity: 0.9;
  font-size: 14px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
}

.welcome-message {
  text-align: center;
  margin: 50px 0;
}

.welcome-content h3 {
  color: #67C23A;
  margin: 15px 0;
}

.quick-questions {
  margin-top: 20px;
}

.quick-questions .el-button {
  width: 100%;
  margin-bottom: 8px;
  text-align: left;
  border: 1px dashed #67C23A;
  border-radius: 6px;
  padding: 8px 12px;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  margin: 0 10px;
}

.message-content {
  max-width: 70%;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  word-break: break-word;
}

.user-message .message-bubble {
  background: #409EFF;
  color: white;
  margin-right: 10px;
}

.assistant-message .message-bubble {
  background: white;
  border: 1px solid #e4e7ed;
  margin-left: 10px;
}

.message-text {
  line-height: 1.6;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 8px;
  text-align: right;
}

.user-message .message-time {
  text-align: left;
}

.loading .typing-indicator {
  display: flex;
  gap: 4px;
  margin-bottom: 8px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #67C23A;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

.loading-text {
  color: #909399;
  font-size: 12px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #e4e7ed;
  background: white;
}

.send-button {
  height: 60px;
  width: 100%;
}

.input-tips {
  margin-top: 10px;
  text-align: center;
}

.chat-actions {
  padding: 15px 20px;
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
  text-align: center;
}

.topic-card {
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.topic-card:hover {
  transform: translateY(-2px);
}

.topic-title {
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.topic-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-10px); }
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>