import axios from 'axios'

const API_BASE = '/api'

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 可以在这里添加认证token等
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error.response?.data || error)
  }
)

// 获取问诊问题列表
export const getQuestions = () => {
  return apiClient.get('/consultation/questions')
}

// 获取单个问题详情
export const getQuestionDetail = (questionId) => {
  return apiClient.get(`/consultation/question/${questionId}`)
}

// 提交问诊答案
export const submitQuestionnaireAnswers = (answers) => {
  return apiClient.post('/consultation/submit-answers', answers)
}

// 分析患者症状
export const analyzePatient = (answers) => {
  return apiClient.post('/diagnosis/analyze', answers)
}

// 获取证型信息
export const getSyndromeInfo = (syndromeName) => {
  return apiClient.get(`/diagnosis/syndrome-info/${syndromeName}`)
}

// 获取诊断维度
export const getDiagnosisDimensions = () => {
  return apiClient.get('/diagnosis/dimensions')
}

// 生成处方
export const generatePrescription = (data) => {
  return apiClient.post('/prescription/generate', data)
}

// 获取方剂库
export const getFormulas = () => {
  return apiClient.get('/prescription/formulas')
}

// 获取外治法
export const getExternalTreatments = () => {
  return apiClient.get('/prescription/external-treatments')
}

// 获取食疗方
export const getDietTherapy = () => {
  return apiClient.get('/prescription/diet-therapy')
}

export default apiClient