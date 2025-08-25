<template>
  <div class="prescription">
    <el-card class="prescription-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Setting /></el-icon>
          <span>个性化治疗方案</span>
        </div>
      </template>

      <!-- 无诊断结果提示 -->
      <div v-if="!diagnosisData" class="no-diagnosis">
        <el-result
          icon="warning"
          title="暂无诊断数据"
          sub-title="请先完成问诊评估获取个性化治疗方案"
        >
          <template #extra>
            <el-button type="primary" @click="goToConsultation">
              开始问诊评估
              <el-icon><Right /></el-icon>
            </el-button>
          </template>
        </el-result>
      </div>

      <!-- 有诊断结果时显示治疗方案 -->
      <div v-else class="treatment-content">
        <!-- 诊断摘要 -->
        <div class="diagnosis-summary">
          <el-alert
            :title="`诊断结果：${diagnosisData.syndrome_diagnosis?.final_diagnosis || '未确定证型'}`"
            type="success"
            :closable="false"
            show-icon
          >
            <template #default>
              <p><strong>睡眠质量等级：</strong>{{ diagnosisData.sleep_quality?.grade || '未评估' }}</p>
              <p><strong>综合评分：</strong>{{ diagnosisData.sleep_quality?.total_score || 0 }}分 / {{ diagnosisData.sleep_quality?.max_possible_score || 0 }}分</p>
              <p><strong>治疗类型：</strong>{{ diagnosisData.treatment_plan?.treatment_type || '未确定' }}</p>
            </template>
          </el-alert>
        </div>

        <!-- 个性化产品推荐 -->
        <div class="products-section">
          <h2 class="section-title">
            <el-icon><ShoppingBag /></el-icon>
            为您推荐的个性化产品
          </h2>

          <div class="treatment-description">
            <el-card shadow="never" class="description-card">
              <p class="treatment-explanation">
                {{ diagnosisData.treatment_plan?.instructions || '根据您的诊断结果，我们为您推荐以下个性化产品组合。' }}
              </p>
            </el-card>
          </div>

          <!-- 产品列表和组合购买区域 -->
          <div v-if="diagnosisData.treatment_plan?.products?.length > 0" class="products-container">
            <el-row :gutter="20">
              <!-- 左侧：产品列表 -->
              <el-col :span="16" class="products-section">
                <el-row :gutter="12">
                  <el-col 
                    :xs="24" :sm="12" :md="8" :lg="8"
                    v-for="(product, index) in diagnosisData.treatment_plan.products" 
                    :key="index"
                  >
                    <el-card 
                      class="product-card compact" 
                      shadow="hover"
                      :class="{ 'selected': selectedProducts.has(product) }"
                    >
                      <!-- 加号选择按钮 -->
                      <div class="select-button" @click="toggleProduct(product)">
                        <el-button 
                          :type="selectedProducts.has(product) ? 'success' : 'info'"
                          circle
                          size="small"
                        >
                          <el-icon v-if="selectedProducts.has(product)"><Check /></el-icon>
                          <el-icon v-else><Plus /></el-icon>
                        </el-button>
                      </div>
                      
                      <div class="product-header">
                        <div class="product-icon">{{ getProductIcon(product) }}</div>
                        <h4 class="product-name">{{ product }}</h4>
                      </div>
                      
                      <div class="product-body">
                        <div class="product-price">
                          <span class="current-price">¥{{ getProductPrice(product) }}</span>
                        </div>
                        
                        <div class="product-specs compact">
                          <div class="spec-item">
                            <span class="spec-label">规格：</span>
                            <span>{{ getProductSpec(product) }}</span>
                          </div>
                        </div>
                      </div>
                      
                      <div class="product-footer">
                        <el-button-group class="purchase-buttons">
                          <el-button 
                            type="success" 
                            size="small"
                            :disabled="product === '专业医生咨询'"
                            @click="handleWechatPurchase(product)"
                          >
                            <el-icon><ChatDotRound /></el-icon>
                            微信
                          </el-button>
                          <el-button 
                            type="primary" 
                            size="small"
                            :disabled="product === '专业医生咨询'"
                            @click="handleTaobaoPurchase(product)"
                          >
                            <el-icon><ShoppingBag /></el-icon>
                            天猫
                          </el-button>
                        </el-button-group>
                      </div>
                    </el-card>
                  </el-col>
                </el-row>
              </el-col>
              
              <!-- 右侧：固定的组合购买窗口 -->
              <el-col :span="8" class="combo-section">
                <div class="combo-purchase fixed">
                  <el-card class="combo-card" shadow="always">
                    <div class="combo-header">
                      <h3>🛒 购物车</h3>
                      <el-button v-if="selectedProducts.size > 0" size="small" @click="clearSelection">清空</el-button>
                    </div>
                    
                    <div v-if="selectedProducts.size === 0" class="empty-cart">
                      <el-empty description="请选择商品" :image-size="80">
                        <template #image>
                          🛍️
                        </template>
                      </el-empty>
                    </div>
                    
                    <div v-else class="cart-content">
                      <div class="selected-products">
                        <el-tag 
                          v-for="product in Array.from(selectedProducts)" 
                          :key="product"
                          size="large"
                          closable
                          @close="toggleProduct(product)"
                          class="product-tag"
                        >
                          {{ getProductIcon(product) }} {{ product }} ¥{{ getProductPrice(product) }}
                        </el-tag>
                      </div>
                      
                      <div class="combo-pricing">
                        <div class="price-row">
                          <span class="price-label">原价总计：</span>
                          <span class="original-total">¥{{ originalTotal }}</span>
                        </div>
                        <div class="price-row discount">
                          <span class="price-label">组合优惠：</span>
                          <span class="discount-amount">-¥{{ discountAmount }}</span>
                        </div>
                        <div class="price-row final">
                          <span class="price-label">优惠后价格：</span>
                          <span class="final-price">¥{{ finalPrice }}</span>
                          <el-tag type="danger" size="small">8.8折</el-tag>
                        </div>
                      </div>
                      
                      <div class="combo-actions">
                        <el-button 
                          type="success" 
                          size="large"
                          @click="handleComboPurchase('wechat')"
                          class="combo-btn"
                        >
                          <el-icon><ChatDotRound /></el-icon>
                          微信支付 ¥{{ finalPrice }}
                        </el-button>
                        <el-button 
                          type="primary" 
                          size="large"
                          @click="handleComboPurchase('alipay')"
                          class="combo-btn"
                        >
                          <el-icon><CreditCard /></el-icon>
                          支付宝 ¥{{ finalPrice }}
                        </el-button>
                      </div>
                    </div>
                  </el-card>
                </div>
              </el-col>
            </el-row>
          </div>

          <!-- 专业医生咨询推荐 -->
          <div v-if="diagnosisData.treatment_plan?.needs_professional" class="professional-consultation">
            <el-alert
              title="建议咨询专业医生"
              type="warning"
              :closable="false"
              show-icon
            >
              <template #default>
                <p>根据您的睡眠质量等级，建议您咨询专业中医师制定更详细的治疗方案。</p>
                <el-button type="warning" @click="goToDoctorConsultation" class="consult-btn">
                  <el-icon><ChatDotRound /></el-icon>
                  立即咨询专业医生
                </el-button>
              </template>
            </el-alert>
          </div>
        </div>

        <!-- 使用指导 -->
        <div class="usage-guidance">
          <h2 class="section-title">
            <el-icon><Document /></el-icon>
            使用指导
          </h2>
          
          <el-card class="guidance-card" shadow="never">
            <el-steps direction="horizontal" :active="4" finish-status="success">
              <el-step title="按时服用" description="严格按照推荐剂量和时间"></el-step>
              <el-step title="配合作息" description="保持规律的睡眠时间"></el-step>
              <el-step title="观察效果" description="记录睡眠改善情况"></el-step>
              <el-step title="及时调整" description="根据效果调整用量"></el-step>
            </el-steps>
            
            <div class="guidance-content">
              <h4>📝 重要提醒</h4>
              <ul class="guidance-list">
                <li>建议连续使用2-4周观察效果</li>
                <li>使用过程中如有不适请及时停用</li>
                <li>配合健康的生活方式效果更佳</li>
                <li>严重症状请及时就医</li>
              </ul>
            </div>
          </el-card>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button size="large" @click="goToConsultation">
            <el-icon><Refresh /></el-icon>
            重新评估
          </el-button>
          <el-button type="success" size="large" @click="goToDoctorConsultation">
            <el-icon><ChatDotRound /></el-icon>
            咨询医生
          </el-button>
          <el-button type="primary" size="large" @click="exportTreatmentPlan">
            <el-icon><Download /></el-icon>
            导出方案
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 支付二维码弹窗 -->
    <el-dialog
      v-model="showPaymentModal"
      title="扫码支付"
      width="400px"
      align-center
    >
      <div class="payment-modal">
        <div class="qr-code-container">
          <img :src="qrCodeUrl" alt="支付二维码" class="qr-code" />
        </div>
        
        <div class="payment-info">
          <p class="payment-amount">支付金额：<strong>¥{{ finalPrice }}</strong></p>
          <p class="payment-desc">请使用手机扫码完成支付</p>
          <p class="selected-count">已选择 {{ selectedProducts.size }} 个产品（组合优惠8.8折）</p>
        </div>
        
        <div class="payment-tips">
          <el-alert
            title="支付完成后，我们将尽快为您安排发货"
            type="success"
            :closable="false"
            show-icon
          />
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showPaymentModal = false">取消支付</el-button>
          <el-button type="success" @click="handlePaymentSuccess">支付完成</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Setting, 
  Right, 
  ShoppingBag,
  Document,
  Refresh,
  ChatDotRound,
  Download,
  Plus,
  Check,
  CreditCard
} from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const diagnosisData = ref(null)
const selectedProducts = ref(new Set())
const showPaymentModal = ref(false)
const qrCodeUrl = ref('')

// 组件挂载时加载诊断数据
onMounted(() => {
  loadDiagnosisData()
})

// 加载诊断数据
const loadDiagnosisData = () => {
  try {
    const storedDiagnosis = localStorage.getItem('latestDiagnosis')
    if (storedDiagnosis) {
      diagnosisData.value = JSON.parse(storedDiagnosis)
      console.log('诊断数据:', diagnosisData.value)
    } else {
      // 如果没有存储数据，使用示例数据
      diagnosisData.value = {
        sleep_quality: {
          grade: '良',
          total_score: 42,
          max_possible_score: 64
        },
        syndrome_diagnosis: {
          final_diagnosis: '肝郁脑虚型失眠',
          primary_syndrome: '肝郁',
          secondary_syndrome: '脑虚'
        },
        treatment_plan: {
          treatment_type: '中等调理',
          products: ['舒肝解郁茶包', '植物蛋白奶粉', '坚果营养包', '穴位贴'],
          instructions: '根据您的诊断结果，推荐以下个性化产品组合，坚持使用2-4周可见效果。',
          needs_professional: false
        }
      }
    }
  } catch (error) {
    console.error('解析诊断数据失败:', error)
    // 错误时也使用示例数据
    diagnosisData.value = {
      sleep_quality: {
        grade: '良',
        total_score: 42,
        max_possible_score: 64
      },
      syndrome_diagnosis: {
        final_diagnosis: '肝郁脑虚型失眠'
      },
      treatment_plan: {
        treatment_type: '中等调理',
        products: ['通用安眠茶包', '植物蛋白奶粉'],
        instructions: '推荐使用以下产品改善睡眠质量。',
        needs_professional: false
      }
    }
  }
}

// 获取产品图标
const getProductIcon = (product) => {
  if (product.includes('茶包') || product.includes('茶')) return '🍵'
  if (product.includes('奶粉') || product.includes('蛋白')) return '🥛'
  if (product.includes('坚果')) return '🌰'
  if (product.includes('鱼油')) return '🐟'
  if (product.includes('穴位贴')) return '🎯'
  if (product.includes('医生咨询')) return '👨‍⚕️'
  return '💊'
}

// 获取产品描述
const getProductDescription = (product) => {
  if (product.includes('舒肝解郁茶包')) return '针对情绪紧张、压力大的失眠患者，疏肝解郁，宁心安神'
  if (product.includes('补血活血茶包')) return '针对气血不足引起的失眠，补气养血，调和营卫'
  if (product.includes('安神定志茶包')) return '针对心神不宁、易惊醒的失眠，安神定志，宁心除烦'
  if (product.includes('通用安眠茶包')) return '适合各种失眠类型，温和安神，改善睡眠质量'
  if (product.includes('植物蛋白奶粉')) return '优质植物蛋白，补充营养，增强体质'
  if (product.includes('坚果营养包')) return '针对肾精不足，补肾填精，强筋健骨'
  if (product.includes('鱼油胶囊')) return '针对脑髓空虚，补脑益智，增强记忆'
  if (product.includes('穴位贴')) return '根据证型配制的专用穴位贴，外治内调，疗效显著'
  if (product.includes('专业医生咨询')) return '与资深中医师一对一咨询，获得个性化诊疗方案'
  return '专业调理产品，改善睡眠质量'
}

// 获取产品使用方法
const getProductUsage = (product) => {
  if (product.includes('茶包') || product.includes('茶')) return '每日1-2次，温水冲泡，睡前1小时饮用'
  if (product.includes('奶粉')) return '每日1-2次，温水冲调，早晚餐后服用'
  if (product.includes('坚果')) return '每日适量，可作为零食或配餐食用'
  if (product.includes('鱼油')) return '每日1-2粒，饭后温水送服'
  if (product.includes('穴位贴')) return '贴敷于相应穴位，每次6-8小时，隔日使用'
  if (product.includes('医生咨询')) return '在线咨询或预约面诊'
  return '请按照产品说明使用'
}

// 获取产品价格
const getProductPrice = (product) => {
  if (product.includes('舒肝解郁茶包')) return '128'
  if (product.includes('补血活血茶包')) return '138'
  if (product.includes('安神定志茶包')) return '118'
  if (product.includes('通用安眠茶包')) return '98'
  if (product.includes('植物蛋白奶粉')) return '168'
  if (product.includes('坚果营养包')) return '88'
  if (product.includes('鱼油胶囊')) return '188'
  if (product.includes('穴位贴')) return '68'
  return '98'
}

// 获取产品原价
const getOriginalPrice = (product) => {
  const currentPrice = parseInt(getProductPrice(product))
  return Math.round(currentPrice * 1.3).toString() // 原价比现价高30%
}

// 获取产品规格
const getProductSpec = (product) => {
  if (product.includes('茶包')) return '30袋/盒'
  if (product.includes('奶粉')) return '800g/罐'
  if (product.includes('坚果')) return '混合装200g'
  if (product.includes('鱼油')) return '60粒/瓶'
  if (product.includes('穴位贴')) return '10贴/盒'
  return '1盒装'
}

// 处理微信购买
const handleWechatPurchase = (product) => {
  // 这里可以跳转到微信小程序或者显示二维码
  ElMessage({
    message: `正在跳转微信购买 ${product}，请稍候...`,
    type: 'success',
    duration: 2000
  })
  
  // 实际应用中可以：
  // 1. 跳转到微信小程序
  // 2. 显示微信二维码
  // 3. 复制微信号让用户添加客服
  setTimeout(() => {
    ElMessage({
      message: '请添加客服微信：insomnia-shop 购买产品',
      type: 'info',
      duration: 5000
    })
  }, 2000)
}

// 处理天猫购买
const handleTaobaoPurchase = (product) => {
  // 这里可以跳转到天猫店铺或者复制淘口令
  ElMessage({
    message: `正在跳转天猫购买 ${product}，请稍候...`,
    type: 'success',
    duration: 2000
  })
  
  // 实际应用中可以：
  // 1. 跳转到天猫店铺链接
  // 2. 复制淘宝口令
  // 3. 打开淘宝APP
  const taobaoUrl = `https://shop.tmall.com/search.htm?keyword=${encodeURIComponent(product)}`
  setTimeout(() => {
    window.open(taobaoUrl, '_blank')
  }, 1000)
}

// 跳转到问诊页面
const goToConsultation = () => {
  router.push('/consultation')
}

// 跳转到医生咨询页面
const goToDoctorConsultation = () => {
  router.push('/doctor-consultation')
}

// 切换产品选择状态
const toggleProduct = (product) => {
  if (product === '专业医生咨询') {
    ElMessage.warning('医生咨询服务不支持在线购买')
    return
  }
  
  if (selectedProducts.value.has(product)) {
    selectedProducts.value.delete(product)
  } else {
    selectedProducts.value.add(product)
  }
  // 触发响应式更新
  selectedProducts.value = new Set(selectedProducts.value)
}

// 清空选择
const clearSelection = () => {
  selectedProducts.value.clear()
  selectedProducts.value = new Set()
}

// 计算原价总计
const originalTotal = computed(() => {
  let total = 0
  for (const product of selectedProducts.value) {
    total += parseInt(getProductPrice(product))
  }
  return total
})

// 计算折扣金额
const discountAmount = computed(() => {
  return Math.round(originalTotal.value * 0.12) // 12%折扣（8.8折 = 88%，所以折扣是12%）
})

// 计算最终价格
const finalPrice = computed(() => {
  return originalTotal.value - discountAmount.value
})

// 处理组合购买
const handleComboPurchase = (paymentMethod) => {
  console.log('handleComboPurchase called:', paymentMethod)
  console.log('selectedProducts.value.size:', selectedProducts.value.size)
  
  if (selectedProducts.value.size === 0) {
    ElMessage.warning('请先选择产品')
    return
  }
  
  // 生成订单信息
  const orderInfo = {
    products: Array.from(selectedProducts.value),
    originalTotal: originalTotal.value,
    discountAmount: discountAmount.value,
    finalPrice: finalPrice.value,
    paymentMethod: paymentMethod,
    orderTime: new Date().toLocaleString()
  }
  
  console.log('订单信息:', orderInfo)
  
  // 显示支付二维码
  showPaymentQR(paymentMethod, finalPrice.value)
}

// 显示支付二维码
const showPaymentQR = (paymentMethod, amount) => {
  console.log('showPaymentQR called:', paymentMethod, amount)
  console.log('showPaymentModal before:', showPaymentModal.value)
  
  // 模拟生成支付二维码URL
  const mockQRData = {
    paymentMethod,
    amount,
    orderId: 'INS' + Date.now(),
    products: Array.from(selectedProducts.value)
  }
  
  console.log('mockQRData:', mockQRData)
  
  // 使用简单的SVG方式生成二维码
  const svgContent = `<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg" style="background: white;">
    <rect width="200" height="200" fill="white" stroke="#ddd" stroke-width="2"/>
    <text x="100" y="50" text-anchor="middle" font-size="14" font-family="Arial" fill="#333">
      ${paymentMethod === 'wechat' ? '微信支付' : '支付宝'}
    </text>
    <text x="100" y="80" text-anchor="middle" font-size="20" font-family="Arial" fill="#f56c6c" font-weight="bold">
      ¥${amount}
    </text>
    <rect x="50" y="100" width="100" height="60" fill="#f8f9fa" stroke="#e4e7ed" stroke-width="1"/>
    <text x="100" y="125" text-anchor="middle" font-size="12" font-family="Arial" fill="#666">
      扫码支付
    </text>
    <text x="100" y="145" text-anchor="middle" font-size="10" font-family="Arial" fill="#999">
      [二维码区域]
    </text>
    <text x="100" y="180" text-anchor="middle" font-size="10" font-family="Arial" fill="#999">
      请使用手机扫码支付
    </text>
  </svg>`
  
  qrCodeUrl.value = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgContent)
  
  console.log('qrCodeUrl set:', qrCodeUrl.value.substring(0, 100) + '...')
  
  showPaymentModal.value = true
  console.log('showPaymentModal after:', showPaymentModal.value)
  
  ElMessage({
    message: `正在生成${paymentMethod === 'wechat' ? '微信' : '支付宝'}支付二维码...`,
    type: 'success',
    duration: 2000
  })
}


// 处理支付成功
const handlePaymentSuccess = () => {
  showPaymentModal.value = false
  
  ElMessage({
    message: '支付成功！订单已提交，我们将尽快为您安排发货',
    type: 'success',
    duration: 3000
  })
  
  // 清空选择
  setTimeout(() => {
    clearSelection()
    ElMessage({
      message: '如有疑问，请联系客服微信：insomnia-shop',
      type: 'info',
      duration: 5000
    })
  }, 1000)
}

// 导出治疗方案
const exportTreatmentPlan = () => {
  if (!diagnosisData.value) {
    ElMessage.warning('暂无治疗方案可导出')
    return
  }
  
  // 构建导出内容
  const content = [
    '个性化失眠治疗方案',
    '========================',
    '',
    `诊断证型：${diagnosisData.value.syndrome_diagnosis?.final_diagnosis || '未确定'}`,
    `睡眠质量：${diagnosisData.value.sleep_quality?.grade || '未评估'}`,
    `综合评分：${diagnosisData.value.sleep_quality?.total_score || 0}分`,
    `治疗类型：${diagnosisData.value.treatment_plan?.treatment_type || '未确定'}`,
    '',
    '推荐产品：',
    ...(diagnosisData.value.treatment_plan?.products || []).map(p => `• ${p}`),
    '',
    '使用说明：',
    `${diagnosisData.value.treatment_plan?.instructions || '请按照产品说明正确使用'}`,
    '',
    '重要提醒：',
    '• 建议连续使用2-4周观察效果',
    '• 配合健康的生活方式效果更佳',
    '• 严重症状请及时就医',
    '',
    `导出时间：${new Date().toLocaleString()}`
  ].join('\n')
  
  // 创建下载
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `失眠治疗方案-${new Date().toISOString().split('T')[0]}.txt`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('治疗方案已导出')
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
  gap: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #409EFF;
}

.no-diagnosis {
  padding: 40px 20px;
  text-align: center;
}

.diagnosis-summary {
  margin-bottom: 30px;
}

.diagnosis-summary .el-alert {
  border-radius: 8px;
}

.products-section {
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409EFF;
  font-size: 20px;
  margin-bottom: 20px;
}

.description-card {
  margin-bottom: 20px;
  background: #f8f9fa;
}

.treatment-explanation {
  color: #606266;
  line-height: 1.6;
  margin: 0;
}

/* 新的产品容器布局 */
.products-container {
  margin-bottom: 30px;
}

.products-section {
  padding-right: 10px;
}

.combo-section {
  padding-left: 10px;
}

/* 紧凑版产品卡片 */
.product-card.compact {
  height: 280px;
  margin-bottom: 15px;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  border: 1px solid #e4e7ed;
}

.product-card.compact:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
  border-color: #409EFF;
}

.product-header {
  text-align: center;
  padding: 12px 8px;
  border-bottom: 1px solid #f0f0f0;
}

.product-icon {
  font-size: 28px;
  margin-bottom: 6px;
  display: block;
}

.product-name {
  color: #303133;
  font-size: 13px;
  font-weight: 600;
  margin: 0;
  line-height: 1.3;
}

.product-body {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-price {
  text-align: center;
  margin-bottom: 10px;
}

.current-price {
  color: #F56C6C;
  font-size: 18px;
  font-weight: bold;
  margin-right: 6px;
}

.original-price {
  color: #909399;
  font-size: 12px;
  text-decoration: line-through;
}

.product-specs.compact {
  font-size: 11px;
  color: #909399;
  margin-bottom: 10px;
  flex: 1;
}

.spec-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
  line-height: 1.2;
}

.spec-label {
  color: #606266;
  font-weight: 500;
}

.product-footer {
  padding: 0 12px 12px;
  border-top: 1px solid #f0f0f0;
  margin-top: auto;
}

.purchase-buttons {
  width: 100%;
  margin-top: 8px;
}

.purchase-buttons .el-button {
  flex: 1;
  font-size: 10px;
  padding: 6px 4px;
}

.purchase-buttons .el-button:first-child {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.purchase-buttons .el-button:last-child {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.professional-consultation {
  margin-bottom: 30px;
}

.consult-btn {
  margin-top: 10px;
}

.usage-guidance {
  margin-bottom: 30px;
}

.guidance-card {
  background: #fafafa;
}

.guidance-content {
  margin-top: 30px;
}

.guidance-content h4 {
  color: #409EFF;
  margin-bottom: 15px;
}

.guidance-list {
  color: #606266;
  line-height: 1.8;
}

.guidance-list li {
  margin-bottom: 8px;
}

.action-buttons {
  text-align: center;
  padding: 20px 0;
  border-top: 1px solid #e4e7ed;
}

.action-buttons .el-button {
  margin: 0 10px;
}

/* 产品选择相关样式 */
.product-card {
  position: relative;
}

.product-card.selected {
  border-color: #67C23A;
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.15);
}

.select-button {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
  cursor: pointer;
}

/* 固定的组合购买窗口 */
.combo-purchase.fixed {
  position: sticky;
  top: 20px;
  z-index: 100;
}

.combo-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  min-height: 400px;
}

.combo-card :deep(.el-card__body) {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.combo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.combo-header h3 {
  margin: 0;
  color: white;
  font-size: 18px;
}

/* 空购物车状态 */
.empty-cart {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
}

.empty-cart :deep(.el-empty__description) {
  color: rgba(255, 255, 255, 0.8);
}

/* 有商品时的内容 */
.cart-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.selected-products {
  margin-bottom: 20px;
  flex: 1;
}

.product-tag {
  margin: 5px 8px 5px 0;
  font-size: 12px;
  padding: 6px 10px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.product-tag :deep(.el-tag__close) {
  color: white;
}

.combo-pricing {
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.price-row.final {
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  padding-top: 8px;
  margin-top: 8px;
  font-size: 16px;
}

.price-label {
  font-size: 14px;
}

.original-total {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: line-through;
  font-size: 14px;
}

.discount-amount {
  color: #FDD835;
  font-weight: bold;
  font-size: 14px;
}

.final-price {
  color: #FDD835;
  font-size: 20px;
  font-weight: bold;
  margin-right: 8px;
}

.combo-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: auto;
}

.combo-btn {
  width: 100%;
  padding: 12px 15px;
  font-size: 15px;
  font-weight: bold;
  border-radius: 8px;
}

/* 支付弹窗样式 */
.payment-modal {
  text-align: center;
  padding: 20px;
}

.qr-code-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.qr-code {
  width: 200px;
  height: 200px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  background: white;
}

.payment-info {
  margin-bottom: 20px;
}

.payment-amount {
  font-size: 18px;
  color: #303133;
  margin-bottom: 10px;
}

.payment-amount strong {
  color: #F56C6C;
  font-size: 24px;
}

.payment-desc {
  color: #606266;
  margin-bottom: 10px;
}

.selected-count {
  color: #909399;
  font-size: 14px;
}

.payment-tips {
  margin-bottom: 10px;
}

.dialog-footer {
  text-align: center;
}

@media (max-width: 768px) {
  .action-buttons .el-button {
    display: block;
    width: 100%;
    margin: 10px 0;
  }
  
  .combo-actions {
    flex-direction: column;
  }
  
  .combo-btn {
    width: 100%;
  }
}
</style>