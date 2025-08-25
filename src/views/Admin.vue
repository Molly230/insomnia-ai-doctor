<template>
  <div class="admin-dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <el-icon size="32" color="#409EFF"><Monitor /></el-icon>
        <div class="header-text">
          <h1>管理后台</h1>
          <p>诊疗数据管理与统计分析</p>
        </div>
      </div>
    </div>

    <!-- 数据统计卡片 -->
    <div class="stats-cards">
      <el-row :gutter="20">
        <el-col :xs="12" :sm="6" :md="6" :lg="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon patients">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ dashboardData.overview?.total_patients || 0 }}</div>
                <div class="stat-label">总患者数</div>
                <div class="stat-sub">今日新增: {{ dashboardData.overview?.today_patients || 0 }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="12" :sm="6" :md="6" :lg="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon diagnoses">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ dashboardData.overview?.total_diagnoses || 0 }}</div>
                <div class="stat-label">总诊断数</div>
                <div class="stat-sub">今日: {{ dashboardData.overview?.today_diagnoses || 0 }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="12" :sm="6" :md="6" :lg="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon doctors">
                <el-icon><Avatar /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ dashboardData.overview?.total_doctors || 0 }}</div>
                <div class="stat-label">在线医生</div>
                <div class="stat-sub">咨询中: {{ dashboardData.overview?.total_consultations || 0 }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="12" :sm="6" :md="6" :lg="6">
          <el-card class="stat-card">
            <div class="stat-item">
              <div class="stat-icon trend">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ dashboardData.overview?.week_diagnoses || 0 }}</div>
                <div class="stat-label">本周诊断</div>
                <div class="stat-sub">较上周: +12%</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-tabs v-model="activeTab" type="card">
        <!-- 数据概览 -->
        <el-tab-pane label="数据概览" name="overview">
          <el-row :gutter="20">
            <!-- 睡眠质量分布 -->
            <el-col :xs="24" :sm="12" :md="12" :lg="12">
              <el-card title="睡眠质量分布">
                <template #header>
                  <span>睡眠质量分布</span>
                </template>
                <div class="chart-container" ref="sleepGradeChart" style="height: 300px;"></div>
                <div class="grade-summary">
                  <div v-for="item in dashboardData.sleep_grade_distribution" :key="item.grade" 
                       class="grade-item">
                    <span class="grade-label">{{ item.grade }}:</span>
                    <span class="grade-count">{{ item.count }}人</span>
                  </div>
                </div>
              </el-card>
            </el-col>
            
            <!-- 证型分布 -->
            <el-col :xs="24" :sm="12" :md="12" :lg="12">
              <el-card title="证型分布">
                <template #header>
                  <span>证型分布（TOP10）</span>
                </template>
                <div class="syndrome-list">
                  <div v-for="(item, index) in dashboardData.syndrome_distribution" 
                       :key="item.syndrome" class="syndrome-item">
                    <div class="syndrome-rank">{{ index + 1 }}</div>
                    <div class="syndrome-name">{{ item.syndrome }}</div>
                    <div class="syndrome-count">{{ item.count }}</div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <!-- 趋势图 -->
          <el-card title="诊断趋势" class="trend-card">
            <template #header>
              <span>近7天诊断趋势</span>
            </template>
            <div class="chart-container" ref="trendChart" style="height: 300px;"></div>
          </el-card>
        </el-tab-pane>

        <!-- 患者管理 -->
        <el-tab-pane label="患者管理" name="patients">
          <div class="table-header">
            <el-input
              v-model="patientSearch"
              placeholder="搜索患者姓名或手机号"
              style="width: 300px;"
              @input="searchPatients"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button type="primary" @click="exportPatients">
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
          </div>
          
          <el-table :data="patients" stripe style="width: 100%;" v-loading="patientsLoading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="phone" label="手机号" width="130" />
            <el-table-column prop="age" label="年龄" width="80" />
            <el-table-column prop="gender" label="性别" width="80" />
            <el-table-column prop="diagnosis_count" label="诊断次数" width="100" />
            <el-table-column label="最近诊断" width="200">
              <template #default="scope">
                <div v-if="scope.row.latest_diagnosis">
                  <el-tag :type="getGradeType(scope.row.latest_diagnosis.grade)">
                    {{ scope.row.latest_diagnosis.grade }}
                  </el-tag>
                  <div class="latest-diagnosis">{{ scope.row.latest_diagnosis.syndrome }}</div>
                </div>
                <span v-else>未诊断</span>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="注册时间" width="180">
              <template #default="scope">
                {{ formatDateTime(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="viewPatientDetail(scope.row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-pagination
            v-model:current-page="patientPage"
            :page-size="patientPageSize"
            :total="patientTotal"
            layout="prev, pager, next, sizes, total"
            @current-change="loadPatients"
            @size-change="onPatientPageSizeChange"
            style="margin-top: 20px; justify-content: center;"
          />
        </el-tab-pane>

        <!-- 诊断记录 -->
        <el-tab-pane label="诊断记录" name="diagnoses">
          <div class="table-header">
            <div class="filters">
              <el-select v-model="diagnosisGradeFilter" placeholder="睡眠质量" @change="loadDiagnoses">
                <el-option value="" label="全部等级" />
                <el-option value="优" label="优" />
                <el-option value="良" label="良" />
                <el-option value="中" label="中" />
                <el-option value="差" label="差" />
              </el-select>
              
              <el-input
                v-model="diagnosisSyndromeFilter"
                placeholder="证型关键词"
                style="width: 200px;"
                @input="loadDiagnoses"
              />
            </div>
            
            <el-button type="primary" @click="exportDiagnoses">
              <el-icon><Download /></el-icon>
              导出记录
            </el-button>
          </div>
          
          <el-table :data="diagnoses" stripe style="width: 100%;" v-loading="diagnosesLoading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="患者信息" width="150">
              <template #default="scope">
                <div v-if="scope.row.patient_info">
                  <div>{{ scope.row.patient_info.name }}</div>
                  <div class="patient-sub">{{ scope.row.patient_info.phone }}</div>
                </div>
                <span v-else>匿名</span>
              </template>
            </el-table-column>
            <el-table-column label="睡眠质量" width="120">
              <template #default="scope">
                <el-tag :type="getGradeType(scope.row.sleep_quality_grade)">
                  {{ scope.row.sleep_quality_grade }}
                </el-tag>
                <div class="score-sub">{{ scope.row.total_sleep_score }}分</div>
              </template>
            </el-table-column>
            <el-table-column prop="final_diagnosis" label="证型诊断" width="150" />
            <el-table-column prop="diagnosed_at" label="诊断时间" width="180">
              <template #default="scope">
                {{ formatDateTime(scope.row.diagnosed_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="viewDiagnosisDetail(scope.row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-pagination
            v-model:current-page="diagnosisPage"
            :page-size="diagnosisPageSize"
            :total="diagnosisTotal"
            layout="prev, pager, next, sizes, total"
            @current-change="loadDiagnoses"
            @size-change="onDiagnosisPageSizeChange"
            style="margin-top: 20px; justify-content: center;"
          />
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 患者详情对话框 -->
    <el-dialog
      v-model="patientDetailVisible"
      title="患者详细信息"
      width="80%"
      :before-close="handleClose"
    >
      <div v-if="selectedPatient" class="patient-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">{{ selectedPatient.name }}</el-descriptions-item>
          <el-descriptions-item label="手机">{{ selectedPatient.phone }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ selectedPatient.age }}岁</el-descriptions-item>
          <el-descriptions-item label="性别">{{ selectedPatient.gender }}</el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ formatDateTime(selectedPatient.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="诊断次数">{{ selectedPatient.diagnoses?.length || 0 }}次</el-descriptions-item>
        </el-descriptions>
        
        <h3 style="margin: 20px 0;">诊断历史</h3>
        <el-timeline>
          <el-timeline-item
            v-for="diagnosis in selectedPatient.diagnoses"
            :key="diagnosis.id"
            :timestamp="formatDateTime(diagnosis.diagnosed_at)"
          >
            <el-card>
              <p>睡眠质量: <el-tag :type="getGradeType(diagnosis.sleep_quality_grade)">{{ diagnosis.sleep_quality_grade }}</el-tag></p>
              <p>总评分: {{ diagnosis.total_sleep_score }}分</p>
              <p>证型诊断: {{ diagnosis.final_diagnosis }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-dialog>

    <!-- 诊断详情对话框 -->
    <el-dialog
      v-model="diagnosisDetailVisible"
      title="诊断详细信息"
      width="90%"
      :before-close="handleClose"
    >
      <div v-if="selectedDiagnosis" class="diagnosis-detail">
        <!-- 基本信息 -->
        <el-card title="基本信息" class="detail-section">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="诊断ID">{{ selectedDiagnosis.id }}</el-descriptions-item>
            <el-descriptions-item label="会话ID">{{ selectedDiagnosis.session_id }}</el-descriptions-item>
            <el-descriptions-item label="诊断时间">{{ formatDateTime(selectedDiagnosis.diagnosed_at) }}</el-descriptions-item>
            <el-descriptions-item label="睡眠质量等级">
              <el-tag :type="getGradeType(selectedDiagnosis.sleep_quality_grade)">
                {{ selectedDiagnosis.sleep_quality_grade }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="总评分">{{ selectedDiagnosis.total_sleep_score }}分</el-descriptions-item>
            <el-descriptions-item label="评分百分比">{{ selectedDiagnosis.sleep_score_percentage }}%</el-descriptions-item>
            <el-descriptions-item label="最终证型">{{ selectedDiagnosis.final_diagnosis }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 问卷答案 -->
        <el-card title="问卷答案" class="detail-section">
          <div class="questionnaire-answers">
            <div v-for="answer in selectedDiagnosis.questionnaire_answers" 
                 :key="answer.question_id" class="answer-item">
              <strong>问题{{ answer.question_id }}:</strong>
              <el-tag v-for="option in answer.selected_options" :key="option" style="margin-left: 5px;">
                {{ option }}
              </el-tag>
            </div>
          </div>
        </el-card>

        <!-- 治疗方案 -->
        <el-card title="治疗方案" class="detail-section" v-if="selectedDiagnosis.treatment_plan">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="治疗类型">{{ selectedDiagnosis.treatment_plan.treatment_type }}</el-descriptions-item>
            <el-descriptions-item label="治疗描述">{{ selectedDiagnosis.treatment_plan.treatment_description }}</el-descriptions-item>
            <el-descriptions-item label="推荐产品">
              <el-tag v-for="product in selectedDiagnosis.treatment_plan.products" :key="product" style="margin-right: 5px;">
                {{ product }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="注意事项">{{ selectedDiagnosis.treatment_plan.instructions }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Monitor, 
  User, 
  Document, 
  Avatar, 
  TrendCharts,
  Search,
  Download
} from '@element-plus/icons-vue'
import axios from 'axios'

// 响应式数据
const activeTab = ref('overview')
const dashboardData = ref({})
const patients = ref([])
const diagnoses = ref([])
const patientsLoading = ref(false)
const diagnosesLoading = ref(false)

// 分页数据
const patientPage = ref(1)
const patientPageSize = ref(20)
const patientTotal = ref(0)
const patientSearch = ref('')

const diagnosisPage = ref(1)
const diagnosisPageSize = ref(20)
const diagnosisTotal = ref(0)
const diagnosisGradeFilter = ref('')
const diagnosisSyndromeFilter = ref('')

// 详情对话框
const patientDetailVisible = ref(false)
const diagnosisDetailVisible = ref(false)
const selectedPatient = ref(null)
const selectedDiagnosis = ref(null)

// API配置
const API_BASE = 'http://localhost:5000/api'

// 加载仪表盘数据
const loadDashboard = async () => {
  try {
    const response = await axios.get(`${API_BASE}/admin/dashboard`)
    if (response.data.success) {
      dashboardData.value = response.data.data
    }
  } catch (error) {
    console.error('加载仪表盘数据失败:', error)
    ElMessage.error('加载仪表盘数据失败')
  }
}

// 加载患者数据
const loadPatients = async () => {
  patientsLoading.value = true
  try {
    const params = {
      page: patientPage.value,
      per_page: patientPageSize.value,
      search: patientSearch.value
    }
    
    const response = await axios.get(`${API_BASE}/admin/patients`, { params })
    if (response.data.success) {
      patients.value = response.data.data.patients
      patientTotal.value = response.data.data.pagination.total
    }
  } catch (error) {
    console.error('加载患者数据失败:', error)
    ElMessage.error('加载患者数据失败')
  } finally {
    patientsLoading.value = false
  }
}

// 加载诊断数据
const loadDiagnoses = async () => {
  diagnosesLoading.value = true
  try {
    const params = {
      page: diagnosisPage.value,
      per_page: diagnosisPageSize.value,
      grade: diagnosisGradeFilter.value,
      syndrome: diagnosisSyndromeFilter.value
    }
    
    const response = await axios.get(`${API_BASE}/admin/diagnoses`, { params })
    if (response.data.success) {
      diagnoses.value = response.data.data.diagnoses
      diagnosisTotal.value = response.data.data.pagination.total
    }
  } catch (error) {
    console.error('加载诊断数据失败:', error)
    ElMessage.error('加载诊断数据失败')
  } finally {
    diagnosesLoading.value = false
  }
}

// 搜索患者
const searchPatients = () => {
  patientPage.value = 1
  loadPatients()
}

// 分页大小变化
const onPatientPageSizeChange = (size) => {
  patientPageSize.value = size
  loadPatients()
}

const onDiagnosisPageSizeChange = (size) => {
  diagnosisPageSize.value = size
  loadDiagnoses()
}

// 查看患者详情
const viewPatientDetail = async (patient) => {
  try {
    const response = await axios.get(`${API_BASE}/admin/patient/${patient.id}`)
    if (response.data.success) {
      selectedPatient.value = response.data.data
      patientDetailVisible.value = true
    }
  } catch (error) {
    console.error('获取患者详情失败:', error)
    ElMessage.error('获取患者详情失败')
  }
}

// 查看诊断详情
const viewDiagnosisDetail = async (diagnosis) => {
  try {
    const response = await axios.get(`${API_BASE}/admin/diagnosis/${diagnosis.id}`)
    if (response.data.success) {
      selectedDiagnosis.value = response.data.data
      diagnosisDetailVisible.value = true
    }
  } catch (error) {
    console.error('获取诊断详情失败:', error)
    ElMessage.error('获取诊断详情失败')
  }
}

// 导出数据
const exportPatients = () => {
  ElMessage.info('导出患者数据功能开发中...')
}

const exportDiagnoses = () => {
  ElMessage.info('导出诊断数据功能开发中...')
}

// 工具函数
const getGradeType = (grade) => {
  const typeMap = {
    '优': 'success',
    '良': 'primary', 
    '中': 'warning',
    '差': 'danger'
  }
  return typeMap[grade] || 'info'
}

const formatDateTime = (datetime) => {
  if (!datetime) return ''
  return new Date(datetime).toLocaleString('zh-CN')
}

const handleClose = () => {
  patientDetailVisible.value = false
  diagnosisDetailVisible.value = false
  selectedPatient.value = null
  selectedDiagnosis.value = null
}

// 组件挂载
onMounted(() => {
  loadDashboard()
  loadPatients()
  loadDiagnoses()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  background: #f5f5f5;
  min-height: calc(100vh - 60px);
}

.page-header {
  background: linear-gradient(135deg, #409EFF 0%, #6bb6ff 100%);
  color: white;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-text h1 {
  margin: 0 0 5px;
  font-size: 28px;
  font-weight: bold;
}

.header-text p {
  margin: 0;
  font-size: 16px;
  opacity: 0.9;
}

.stats-cards {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
}

.stat-item {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}

.stat-icon.patients { background: #67C23A; }
.stat-icon.diagnoses { background: #409EFF; }
.stat-icon.doctors { background: #E6A23C; }
.stat-icon.trend { background: #F56C6C; }

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.stat-label {
  color: #606266;
  margin: 5px 0;
  font-size: 14px;
}

.stat-sub {
  color: #909399;
  font-size: 12px;
}

.main-content {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.chart-container {
  width: 100%;
}

.grade-summary {
  margin-top: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.grade-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.grade-label {
  color: #606266;
}

.grade-count {
  font-weight: bold;
  color: #409EFF;
}

.syndrome-list {
  max-height: 300px;
  overflow-y: auto;
}

.syndrome-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.syndrome-rank {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  margin-right: 10px;
}

.syndrome-name {
  flex: 1;
  color: #303133;
}

.syndrome-count {
  color: #409EFF;
  font-weight: bold;
}

.trend-card {
  margin-top: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filters {
  display: flex;
  gap: 10px;
}

.latest-diagnosis {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.patient-sub {
  font-size: 12px;
  color: #909399;
}

.score-sub {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.patient-detail, .diagnosis-detail {
  max-height: 70vh;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 20px;
}

.questionnaire-answers {
  max-height: 300px;
  overflow-y: auto;
}

.answer-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.answer-item:last-child {
  border-bottom: none;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 10px;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .table-header {
    flex-direction: column;
    gap: 10px;
  }
}
</style>