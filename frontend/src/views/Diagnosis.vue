<template>
  <div class="diagnosis">
    <el-card class="diagnosis-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><TrendCharts /></el-icon>
          <span>诊断结果</span>
        </div>
      </template>

      <div v-if="!hasResult" class="no-result">
        <el-result
          icon="warning"
          title="暂无诊断结果"
          sub-title="请先完成问诊评估"
        >
          <template #extra>
            <el-button type="primary" @click="goToConsultation">
              开始问诊
              <el-icon><Right /></el-icon>
            </el-button>
          </template>
        </el-result>
      </div>

      <div v-else class="result-content">
        <el-steps :active="3" finish-status="success" align-center class="result-steps">
          <el-step title="问诊评估" description="已完成19项问题" />
          <el-step title="数据分析" description="二元诊断系统分析" />
          <el-step title="证型判定" description="确定最终证型" />
          <el-step title="治疗方案" description="生成个性化建议" />
        </el-steps>

        <div class="diagnosis-result">
          <h2>🔍 诊断结果</h2>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="证型诊断">
              <el-tag type="primary" size="large">{{ result.syndrome_type }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="置信度">
              <el-progress :percentage="result.confidence * 100" :color="getConfidenceColor(result.confidence)" />
            </el-descriptions-item>
            <el-descriptions-item label="病理特征">
              {{ result.pathogenesis }}
            </el-descriptions-item>
            <el-descriptions-item label="主要症状">
              <el-tag v-for="symptom in result.main_symptoms" :key="symptom" class="symptom-tag">
                {{ symptom }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="treatment-preview">
          <h3>💊 治疗方案预览</h3>
          <el-row :gutter="20">
            <el-col :xs="24" :sm="8">
              <el-card class="treatment-card" shadow="hover">
                <div class="treatment-icon">🌿</div>
                <h4>中药调理</h4>
                <p>{{ result.herbal_preview }}</p>
              </el-card>
            </el-col>
            <el-col :xs="24" :sm="8">
              <el-card class="treatment-card" shadow="hover">
                <div class="treatment-icon">🖐️</div>
                <h4>外治疗法</h4>
                <p>{{ result.external_preview }}</p>
              </el-card>
            </el-col>
            <el-col :xs="24" :sm="8">
              <el-card class="treatment-card" shadow="hover">
                <div class="treatment-icon">🍲</div>
                <h4>食疗调理</h4>
                <p>{{ result.diet_preview }}</p>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <div class="action-buttons">
          <el-button size="large" @click="goToConsultation">
            <el-icon><Refresh /></el-icon>
            重新问诊
          </el-button>
          <el-button type="primary" size="large" @click="goToPrescription">
            查看完整治疗方案
            <el-icon><Right /></el-icon>
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { TrendCharts, Right, Refresh } from '@element-plus/icons-vue'

const router = useRouter()

// 示例诊断结果（实际应从API获取）
const result = ref({
  syndrome_type: '心肾不交型失眠',
  confidence: 0.85,
  pathogenesis: '心火上炎，肾水不济，心神不安',
  main_symptoms: ['入睡困难', '心烦不安', '腰膝酸软', '头晕耳鸣'],
  herbal_preview: '黄连阿胶汤加减，滋阴降火，交通心肾',
  external_preview: '神门、心俞、肾俞穴位按摩，安神定志',
  diet_preview: '百合莲子粥，酸枣仁茶，养心安神'
})

const hasResult = computed(() => {
  // 实际应检查是否有诊断数据
  return true // 暂时设为true显示示例
})

const getConfidenceColor = (confidence) => {
  if (confidence >= 0.8) return '#67c23a'
  if (confidence >= 0.6) return '#e6a23c'
  return '#f56c6c'
}

const goToConsultation = () => {
  router.push('/consultation')
}

const goToPrescription = () => {
  router.push('/prescription')
}

onMounted(() => {
  // 这里可以加载实际的诊断结果
})
</script>

<style scoped>
.diagnosis {
  max-width: 1000px;
  margin: 0 auto;
}

.diagnosis-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.card-header .el-icon {
  margin-right: 8px;
  font-size: 20px;
}

.no-result {
  padding: 40px;
}

.result-content {
  padding: 20px 0;
}

.result-steps {
  margin-bottom: 40px;
}

.diagnosis-result {
  margin-bottom: 40px;
}

.diagnosis-result h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.symptom-tag {
  margin-right: 8px;
  margin-bottom: 4px;
}

.treatment-preview {
  margin-bottom: 40px;
}

.treatment-preview h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.treatment-card {
  text-align: center;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.treatment-card:hover {
  transform: translateY(-5px);
}

.treatment-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.treatment-card h4 {
  color: #2c3e50;
  margin: 10px 0;
}

.treatment-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

.action-buttons {
  text-align: center;
  padding: 20px 0;
}

.action-buttons .el-button {
  margin: 0 10px;
}
</style>