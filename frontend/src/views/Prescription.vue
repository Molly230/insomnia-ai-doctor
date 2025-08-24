<template>
  <div class="prescription">
    <el-card class="prescription-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Medicine /></el-icon>
          <span>个性化治疗方案</span>
        </div>
      </template>

      <!-- 证型摘要 -->
      <div class="syndrome-summary">
        <el-alert
          title="诊断证型：心肾不交型失眠"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            <p>病机：心火上炎，肾水不济，心神失养而不寐</p>
            <p>治则：滋阴降火，交通心肾，养心安神</p>
          </template>
        </el-alert>
      </div>

      <!-- 中药方剂 -->
      <div class="treatment-section">
        <h2 class="section-title">
          <el-icon><Grape /></el-icon>
          中药调理方案
        </h2>
        
        <el-card class="formula-card" shadow="hover">
          <h3>黄连阿胶汤加减</h3>
          
          <el-table :data="herbalFormula" style="width: 100%">
            <el-table-column prop="herb" label="药材" width="120" />
            <el-table-column prop="dosage" label="用量" width="80" />
            <el-table-column prop="effects" label="功效" />
          </el-table>

          <div class="formula-instructions">
            <h4>📋 服用方法</h4>
            <ul>
              <li><strong>煎煮方法</strong>：水煎服，先煎30分钟</li>
              <li><strong>服用剂量</strong>：每日一剂，分早晚两次服用</li>
              <li><strong>服用时间</strong>：饭后30分钟，睡前2小时</li>
              <li><strong>疗程建议</strong>：连续服用2-4周，根据症状调整</li>
            </ul>
          </div>
        </el-card>
      </div>

      <!-- 外治疗法 -->
      <div class="treatment-section">
        <h2 class="section-title">
          <el-icon><Connection /></el-icon>
          外治疗法
        </h2>

        <el-row :gutter="20">
          <el-col :xs="24" :md="12">
            <el-card class="therapy-card" shadow="hover">
              <h3>🖐️ 穴位按摩</h3>
              <div class="therapy-content">
                <p><strong>主要穴位：</strong>神门、心俞、肾俞、三阴交、涌泉</p>
                <p><strong>手法：</strong>指腹按揉，力度适中</p>
                <p><strong>时间：</strong>每穴按压1-2分钟</p>
                <p><strong>频率：</strong>每日睡前30分钟</p>
                <p><strong>功效：</strong>宁心安神，调理气血</p>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="24" :md="12">
            <el-card class="therapy-card" shadow="hover">
              <h3>🛁 药浴足疗</h3>
              <div class="therapy-content">
                <p><strong>配方：</strong>酸枣仁30g、夜交藤30g、合欢花15g</p>
                <p><strong>方法：</strong>煎煮取汁，温度40-42℃</p>
                <p><strong>时间：</strong>浸泡20-30分钟</p>
                <p><strong>频率：</strong>每日睡前1小时</p>
                <p><strong>功效：</strong>温经通络，安神助眠</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 食疗调理 -->
      <div class="treatment-section">
        <h2 class="section-title">
          <el-icon><Bowl /></el-icon>
          食疗调理方案
        </h2>

        <el-row :gutter="20">
          <el-col :xs="24" :md="8" v-for="recipe in dietRecipes" :key="recipe.name">
            <el-card class="recipe-card" shadow="hover">
              <h3>{{ recipe.icon }} {{ recipe.name }}</h3>
              <div class="recipe-content">
                <p><strong>材料：</strong>{{ recipe.ingredients }}</p>
                <p><strong>制作：</strong>{{ recipe.method }}</p>
                <p><strong>用法：</strong>{{ recipe.usage }}</p>
                <p><strong>功效：</strong>{{ recipe.effects }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 生活调养 -->
      <div class="treatment-section">
        <h2 class="section-title">
          <el-icon><Sunny /></el-icon>
          生活调养建议
        </h2>

        <el-card class="lifestyle-card" shadow="hover">
          <el-row :gutter="30">
            <el-col :xs="24" :md="12">
              <h3>🌙 睡眠卫生</h3>
              <ul class="lifestyle-list">
                <li>规律作息，晚上10点前入睡</li>
                <li>卧室环境安静，温度适宜（18-22℃）</li>
                <li>睡前避免使用电子设备</li>
                <li>睡前可进行冥想或深呼吸练习</li>
              </ul>
            </el-col>
            <el-col :xs="24" :md="12">
              <h3>🏃 运动调节</h3>
              <ul class="lifestyle-list">
                <li>每日适量运动30分钟</li>
                <li>推荐：散步、太极拳、瑜伽</li>
                <li>避免睡前3小时剧烈运动</li>
                <li>运动以微汗为度，不宜过量</li>
              </ul>
            </el-col>
          </el-row>
          
          <el-row :gutter="30" style="margin-top: 20px;">
            <el-col :xs="24" :md="12">
              <h3>🍽️ 饮食调节</h3>
              <ul class="lifestyle-list">
                <li>晚餐清淡，睡前3小时停止进食</li>
                <li>避免咖啡、浓茶、辛辣刺激食物</li>
                <li>可适量食用安神食品：红枣、桂圆</li>
                <li>保持饮食规律，营养均衡</li>
              </ul>
            </el-col>
            <el-col :xs="24" :md="12">
              <h3>😌 情志调节</h3>
              <ul class="lifestyle-list">
                <li>保持情绪稳定，避免过度思虑</li>
                <li>学会释放压力，适时放松</li>
                <li>培养兴趣爱好，丰富精神生活</li>
                <li>必要时寻求心理咨询支持</li>
              </ul>
            </el-col>
          </el-row>
        </el-card>
      </div>

      <!-- 重要提醒 -->
      <el-alert
        title="⚠️ 重要提醒"
        type="warning"
        :closable="false"
        show-icon
      >
        <template #default>
          <ul>
            <li>本方案仅供参考，具体用药请咨询专业中医师</li>
            <li>服药过程中如有不适，请及时停药并就医</li>
            <li>孕妇、哺乳期妇女、儿童慎用</li>
            <li>如症状严重或持续不改善，请及时就医</li>
          </ul>
        </template>
      </el-alert>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button size="large" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回诊断
        </el-button>
        <el-button type="primary" size="large" @click="downloadPrescription">
          <el-icon><Download /></el-icon>
          下载处方
        </el-button>
        <el-button size="large" @click="goToConsultation">
          <el-icon><Refresh /></el-icon>
          重新问诊
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Medicine, Grape, Connection, Bowl, Sunny, ArrowLeft, Download, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 中药方剂数据
const herbalFormula = ref([
  { herb: '黄连', dosage: '6g', effects: '清心火，燥湿解毒' },
  { herb: '阿胶', dosage: '9g', effects: '滋阴润燥，补血止血' },
  { herb: '白芍', dosage: '12g', effects: '养血敛阴，柔肝止痛' },
  { herb: '黄芩', dosage: '9g', effects: '清热燥湿，泻火解毒' },
  { herb: '鸡子黄', dosage: '2枚', effects: '滋阴润燥，宁心安神' },
  { herb: '酸枣仁', dosage: '15g', effects: '养心安神，敛汗' },
  { herb: '龙骨', dosage: '15g', effects: '镇心安神，收敛固涩' }
])

// 食疗方案数据
const dietRecipes = ref([
  {
    name: '百合莲子粥',
    icon: '🍚',
    ingredients: '百合30g、莲子30g、大米100g',
    method: '先煮莲子至软，再加百合和大米煮粥',
    usage: '晚餐或睡前温服',
    effects: '养心安神，润肺止咳'
  },
  {
    name: '酸枣仁茶',
    icon: '🍵',
    ingredients: '酸枣仁15g、龙眼肉10g',
    method: '开水冲泡，焖10分钟即可',
    usage: '睡前1小时饮用',
    effects: '宁心安神，养血润燥'
  },
  {
    name: '银耳雪梨汤',
    icon: '🍐',
    ingredients: '银耳10g、雪梨1个、冰糖适量',
    method: '银耳泡发，与雪梨同煮至软烂',
    usage: '每日午后饮用',
    effects: '滋阴润肺，清热安神'
  }
])

const goBack = () => {
  router.go(-1)
}

const goToConsultation = () => {
  router.push('/consultation')
}

const downloadPrescription = () => {
  ElMessage.success('处方下载功能开发中...')
}
</script>

<style scoped>
.prescription {
  max-width: 1200px;
  margin: 0 auto;
}

.prescription-card {
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

.syndrome-summary {
  margin-bottom: 30px;
}

.treatment-section {
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 20px;
}

.section-title .el-icon {
  margin-right: 8px;
  font-size: 24px;
}

.formula-card {
  margin-bottom: 20px;
}

.formula-card h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 18px;
}

.formula-instructions {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.formula-instructions h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.formula-instructions ul {
  list-style: none;
  padding: 0;
}

.formula-instructions li {
  margin-bottom: 8px;
  padding-left: 20px;
  position: relative;
}

.formula-instructions li:before {
  content: "•";
  color: #409eff;
  position: absolute;
  left: 0;
}

.therapy-card,
.recipe-card {
  height: 100%;
  margin-bottom: 20px;
}

.therapy-card h3,
.recipe-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  text-align: center;
}

.therapy-content,
.recipe-content {
  line-height: 1.8;
}

.therapy-content p,
.recipe-content p {
  margin-bottom: 8px;
}

.lifestyle-card {
  padding: 20px;
}

.lifestyle-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.lifestyle-list {
  list-style: none;
  padding: 0;
}

.lifestyle-list li {
  margin-bottom: 10px;
  padding-left: 20px;
  position: relative;
  line-height: 1.6;
}

.lifestyle-list li:before {
  content: "✓";
  color: #67c23a;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.action-buttons {
  text-align: center;
  padding: 30px 0;
  margin-top: 20px;
}

.action-buttons .el-button {
  margin: 0 10px;
}
</style>