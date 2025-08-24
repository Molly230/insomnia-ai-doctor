<template>
  <div class="knowledge">
    <el-card class="knowledge-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Document /></el-icon>
          <span>中医失眠知识库</span>
        </div>
      </template>

      <!-- 知识分类导航 -->
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="基础理论" name="theory">
          <div class="knowledge-content">
            <h2>🔍 中医失眠基础理论</h2>
            
            <el-collapse v-model="activeCollapse">
              <el-collapse-item title="失眠的中医认识" name="1">
                <div class="theory-content">
                  <p><strong>病名：</strong>失眠，古称"不寐"、"不得眠"、"目不瞑"</p>
                  <p><strong>定义：</strong>以入睡困难、睡眠时间不足或睡眠不深为主要症状的疾病</p>
                  
                  <h4>📚 古代文献记载</h4>
                  <ul>
                    <li>《内经》："卫气不得入于阴，常留于阳，留于阳则阳气满，阳气满则阳跷盛，不得入于阴则阴气虚，故目不瞑矣"</li>
                    <li>《伤寒论》："虚烦不得眠"</li>
                    <li>《金匮要略》："虚劳虚烦不得眠，酸枣仁汤主之"</li>
                  </ul>

                  <h4>🎯 病机要点</h4>
                  <p>失眠的根本病机在于阴阳失衡，神不守舍。具体表现为：</p>
                  <ul>
                    <li><strong>阳不入阴：</strong>卫气不能正常由阳入阴</li>
                    <li><strong>心神不安：</strong>心主神志，心神失养则不寐</li>
                    <li><strong>脏腑功能失调：</strong>心、肝、脾、肾等脏腑功能失常</li>
                  </ul>
                </div>
              </el-collapse-item>

              <el-collapse-item title="失眠的病因病机" name="2">
                <div class="theory-content">
                  <h4>🎭 情志因素</h4>
                  <ul>
                    <li><strong>思虑过度：</strong>损伤心脾，心血不足，神不守舍</li>
                    <li><strong>情志不遂：</strong>肝气郁结，郁而化火，扰动心神</li>
                    <li><strong>惊恐忧虑：</strong>心神不宁，魂不守舍</li>
                  </ul>

                  <h4>🍽️ 饮食因素</h4>
                  <ul>
                    <li><strong>饮食不节：</strong>损伤脾胃，运化失职</li>
                    <li><strong>嗜食肥甘：</strong>酿生痰热，痰热内扰</li>
                    <li><strong>饥饱不均：</strong>胃不和则卧不安</li>
                  </ul>

                  <h4>🏃 劳倦因素</h4>
                  <ul>
                    <li><strong>久病体虚：</strong>气血阴阳俱虚，心神失养</li>
                    <li><strong>房事不节：</strong>肾精亏损，心肾不交</li>
                    <li><strong>年老体衰：</strong>阴血不足，阳气偏亢</li>
                  </ul>
                </div>
              </el-collapse-item>

              <el-collapse-item title="失眠的证型分类" name="3">
                <div class="theory-content">
                  <h4>💔 实证</h4>
                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="肝郁化火型">
                      <strong>症状：</strong>不寐多梦，急躁易怒，头晕头胀，目赤耳鸣，口苦而干，便秘溲赤<br>
                      <strong>舌脉：</strong>舌红苔黄，脉弦而数
                    </el-descriptions-item>
                    <el-descriptions-item label="痰热内扰型">
                      <strong>症状：</strong>不寐头重，胸闷脘痞，泛恶嗳气，口苦腹胀<br>
                      <strong>舌脉：</strong>舌偏红，苔黄腻，脉滑数
                    </el-descriptions-item>
                  </el-descriptions>

                  <h4>💙 虚证</h4>
                  <el-descriptions :column="1" border style="margin-top: 15px;">
                    <el-descriptions-item label="阴虚火旺型">
                      <strong>症状：</strong>心烦不寐，五心烦热，耳鸣健忘，腰膝酸软，遗精盗汗<br>
                      <strong>舌脉：</strong>舌红少苔，脉细数
                    </el-descriptions-item>
                    <el-descriptions-item label="心脾两虚型">
                      <strong>症状：</strong>不易入睡，多梦易醒，心悸健忘，神疲食少，面色萎黄<br>
                      <strong>舌脉：</strong>舌淡苔薄白，脉细弱
                    </el-descriptions-item>
                    <el-descriptions-item label="心肾不交型">
                      <strong>症状：</strong>心烦不寐，入睡困难，腰膝酸软，潮热盗汗，男子遗精，女子月经不调<br>
                      <strong>舌脉：</strong>舌红少苔，脉细数
                    </el-descriptions-item>
                    <el-descriptions-item label="心胆气虚型">
                      <strong>症状：</strong>虚烦不寐，触事易惊，胆怯心悸，气短自汗<br>
                      <strong>舌脉：</strong>舌淡，脉弦细
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-tab-pane>

        <el-tab-pane label="方剂大全" name="formulas">
          <div class="knowledge-content">
            <h2>💊 经典失眠方剂</h2>
            
            <el-row :gutter="20">
              <el-col :xs="24" :md="12" :lg="8" v-for="formula in formulas" :key="formula.name">
                <el-card class="formula-card" shadow="hover">
                  <h3>{{ formula.name }}</h3>
                  <div class="formula-content">
                    <p><strong>出处：</strong>{{ formula.source }}</p>
                    <p><strong>组成：</strong>{{ formula.composition }}</p>
                    <p><strong>功效：</strong>{{ formula.effects }}</p>
                    <p><strong>主治：</strong>{{ formula.indications }}</p>
                    <p><strong>用法：</strong>{{ formula.usage }}</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>

        <el-tab-pane label="穴位疗法" name="acupoints">
          <div class="knowledge-content">
            <h2>🖐️ 失眠常用穴位</h2>
            
            <el-row :gutter="20">
              <el-col :xs="24" :md="12" v-for="point in acupoints" :key="point.name">
                <el-card class="acupoint-card" shadow="hover">
                  <h3>{{ point.name }}</h3>
                  <div class="acupoint-content">
                    <p><strong>定位：</strong>{{ point.location }}</p>
                    <p><strong>主治：</strong>{{ point.indications }}</p>
                    <p><strong>操作：</strong>{{ point.method }}</p>
                    <p><strong>功效：</strong>{{ point.effects }}</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>

        <el-tab-pane label="食疗养生" name="diet">
          <div class="knowledge-content">
            <h2>🍲 失眠食疗方案</h2>
            
            <el-row :gutter="20">
              <el-col :xs="24" :md="8" v-for="recipe in dietRecipes" :key="recipe.name">
                <el-card class="recipe-card" shadow="hover">
                  <div class="recipe-header">
                    <span class="recipe-icon">{{ recipe.icon }}</span>
                    <h3>{{ recipe.name }}</h3>
                  </div>
                  <div class="recipe-content">
                    <p><strong>材料：</strong>{{ recipe.ingredients }}</p>
                    <p><strong>制法：</strong>{{ recipe.method }}</p>
                    <p><strong>用法：</strong>{{ recipe.usage }}</p>
                    <p><strong>功效：</strong>{{ recipe.effects }}</p>
                    <p><strong>适应证：</strong>{{ recipe.indications }}</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Document } from '@element-plus/icons-vue'

const activeTab = ref('theory')
const activeCollapse = ref(['1'])

// 经典方剂数据
const formulas = ref([
  {
    name: '甘麦大枣汤',
    source: '《金匮要略》',
    composition: '甘草9g，小麦30g，大枣10枚',
    effects: '养心安神，和中缓急',
    indications: '心阴不足，肝气失和之脏躁',
    usage: '水煎服，每日一剂'
  },
  {
    name: '酸枣仁汤',
    source: '《金匮要略》',
    composition: '酸枣仁15g，甘草3g，知母6g，茯苓6g，川芎6g',
    effects: '养血安神，清热除烦',
    indications: '虚烦不得眠，心悸盗汗',
    usage: '水煎服，睡前温服'
  },
  {
    name: '朱砂安神丸',
    source: '《内外伤辨惑论》',
    composition: '朱砂15g，黄连6g，炙甘草9g，生地黄1.5g，当归1.5g',
    effects: '镇心安神，泻火养阴',
    indications: '心火亢盛，阴血不足证',
    usage: '每服6g，临卧津下'
  },
  {
    name: '天王补心丹',
    source: '《摄生秘剖》',
    composition: '生地黄120g，人参15g，丹参15g，玄参15g等',
    effects: '滋阴养血，补心安神',
    indications: '心肾阴虚，心神不安',
    usage: '每服6-9g，空心淡盐汤送下'
  },
  {
    name: '安神定志丸',
    source: '《医学心悟》',
    composition: '人参30g，茯苓30g，茯神30g，远志30g，石菖蒲15g',
    effects: '益气镇惊，安神定志',
    indications: '心气不足，神志不安',
    usage: '每服6g，温开水送下'
  },
  {
    name: '归脾汤',
    source: '《济生方》',
    composition: '人参9g，白术9g，黄芪12g，当归9g，茯神9g等',
    effects: '益气补血，健脾养心',
    indications: '心脾两虚，气血不足',
    usage: '水煎服，每日一剂'
  }
])

// 穴位数据
const acupoints = ref([
  {
    name: '神门穴',
    location: '腕横纹尺侧端，尺侧腕屈肌腱桡侧凹陷处',
    indications: '失眠，心悸，健忘，痴呆，癫狂痫',
    method: '直刺0.3-0.5寸，可灸',
    effects: '宁心安神，清心火'
  },
  {
    name: '三阴交',
    location: '内踝尖上3寸，胫骨内侧缘后方',
    indications: '失眠，神经衰弱，月经不调，遗精',
    method: '直刺1-1.5寸，避开大隐静脉',
    effects: '健脾益气，调理冲任'
  },
  {
    name: '百会穴',
    location: '头顶部，前发际正中直上7寸',
    indications: '失眠，健忘，眩晕，头痛，中风',
    method: '平刺0.5-0.8寸，可灸',
    effects: '醒脑开窍，安神定志'
  },
  {
    name: '印堂穴',
    location: '额部，两眉头连线中点',
    indications: '失眠，头痛，眩晕，鼻塞',
    method: '提捏局部皮肤，向下平刺0.3-0.5寸',
    effects: '清头明目，通鼻窍'
  },
  {
    name: '涌泉穴',
    location: '足底部，卷足时足前部凹陷处',
    indications: '失眠，神经衰弱，高血压，小儿惊风',
    method: '直刺0.5-0.8寸，可灸',
    effects: '滋阴降火，宁心安神'
  },
  {
    name: '太溪穴',
    location: '内踝后方，内踝尖与跟腱间的凹陷处',
    indications: '失眠，神经衰弱，肾虚，腰痛',
    method: '直刺0.5-0.8寸，可灸',
    effects: '滋肾阴，降虚火'
  }
])

// 食疗方案数据
const dietRecipes = ref([
  {
    name: '百合莲子粥',
    icon: '🍚',
    ingredients: '百合30g，莲子30g，大米100g',
    method: '将百合、莲子洗净，先煮莲子至半熟，再加百合、大米同煮成粥',
    usage: '每日1-2次，温热服用',
    effects: '养心安神，润肺止咳',
    indications: '心阴不足型失眠'
  },
  {
    name: '酸枣仁粥',
    icon: '🌰',
    ingredients: '酸枣仁15g，粳米100g',
    method: '酸枣仁炒熟研末，粳米煮粥，临熟加入酸枣仁末',
    usage: '每晚睡前温服',
    effects: '养心安神，敛汗生津',
    indications: '心血不足型失眠'
  },
  {
    name: '龙眼肉粥',
    icon: '🫐',
    ingredients: '龙眼肉20g，大米60g，红枣6枚',
    method: '将龙眼肉、红枣洗净，与大米同煮成粥',
    usage: '每日早晚各一次',
    effects: '补益心脾，养血安神',
    indications: '心脾两虚型失眠'
  },
  {
    name: '小麦甘草茶',
    icon: '🌾',
    ingredients: '浮小麦30g，甘草10g，大枣5枚',
    method: '将三味药物水煎取汁',
    usage: '代茶频饮',
    effects: '养心安神，和中缓急',
    indications: '心神不宁，烦躁不安'
  },
  {
    name: '合欢花茶',
    icon: '🌸',
    ingredients: '合欢花10g，夜交藤15g',
    method: '开水冲泡，闷10分钟即可',
    usage: '睡前1小时饮用',
    effects: '解郁安神，活血消肿',
    indications: '肝郁气滞型失眠'
  },
  {
    name: '银耳莲子汤',
    icon: '🍄',
    ingredients: '银耳10g，莲子15g，冰糖适量',
    method: '银耳泡发后与莲子同炖至软烂，加冰糖调味',
    usage: '每日下午服用',
    effects: '滋阴润燥，养心安神',
    indications: '阴虚火旺型失眠'
  }
])

const handleTabClick = (tab) => {
  console.log('切换到:', tab.props.name)
}
</script>

<style scoped>
.knowledge {
  max-width: 1200px;
  margin: 0 auto;
}

.knowledge-card {
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

.knowledge-content {
  padding: 20px 0;
}

.knowledge-content h2 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.theory-content {
  padding: 15px;
  line-height: 1.8;
}

.theory-content h4 {
  color: #409eff;
  margin: 20px 0 10px 0;
}

.theory-content ul {
  padding-left: 20px;
}

.theory-content li {
  margin-bottom: 8px;
}

.formula-card,
.acupoint-card,
.recipe-card {
  margin-bottom: 20px;
  height: 100%;
}

.formula-card h3,
.acupoint-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  text-align: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.formula-content,
.acupoint-content,
.recipe-content {
  line-height: 1.6;
}

.formula-content p,
.acupoint-content p,
.recipe-content p {
  margin-bottom: 10px;
}

.recipe-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.recipe-icon {
  font-size: 24px;
  margin-right: 10px;
}

.recipe-header h3 {
  margin: 0;
  color: #2c3e50;
}
</style>