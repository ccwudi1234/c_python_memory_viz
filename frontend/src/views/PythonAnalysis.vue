<template>
  <div class="analyze-page">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="code-editor-card">
          <template #header>
            <div class="card-header">
              <span>Python代码编辑器</span>
            </div>
          </template>
          <el-input
            v-model="code"
            type="textarea"
            :rows="15"
            placeholder="在此输入 Python 代码..."
            class="code-input"
          />
          <div class="button-group" style="margin-top: 15px">
            <el-button type="primary" @click="runAnalysis" :loading="loading">
              <el-icon><VideoPlay /></el-icon> 运行分析
            </el-button>
            <el-button @click="runAudit" :loading="auditLoading">
              <el-icon><Search /></el-icon> 代码审核
            </el-button>
            <el-button @click="reset">
              <el-icon><RefreshLeft /></el-icon> 重置
            </el-button>
            <el-button @click="loadExample">
              <el-icon><DocumentCopy /></el-icon> 加载示例
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="visualization-card">
          <template #header>
            <div class="card-header">
              <span>内存可视化</span>
              <div class="step-controls" v-if="simulationStates.length > 0">
                <el-button-group>
                  <el-button @click="prevStep" :disabled="currentStep === 0">
                    <el-icon><DArrowLeft /></el-icon>
                  </el-button>
                  <span class="step-indicator">
                    步骤 {{ currentStep + 1 }} / {{ simulationStates.length }}
                  </span>
                  <el-button @click="nextStep" :disabled="currentStep >= simulationStates.length - 1">
                    <el-icon><DArrowRight /></el-icon>
                  </el-button>
                </el-button-group>
              </div>
            </div>
          </template>
          <div ref="visualContainer" class="visual-container">
            <div v-if="!currentState" class="placeholder">
              <el-empty description="点击运行分析开始可视化" />
            </div>
            <div v-else class="memory-visual">
              <div class="memory-blocks">
                <div v-for="(block, addr) in currentState.memory" :key="addr" class="memory-block">
                  <div class="block-header">
                    <span class="block-addr">{{ addr }}</span>
                    <span class="block-type">{{ block.type }}</span>
                  </div>
                  <div class="block-value">{{ formatValue(block.value) }}</div>
                  <div class="block-refs">
                    <el-tag v-for="ref in block.refs" :key="ref" size="small" type="info">
                      {{ ref }}
                    </el-tag>
                  </div>
                </div>
              </div>
              <div class="variables-section" v-if="currentState.variables">
                <h4>变量映射</h4>
                <div class="var-list">
                  <div v-for="(addr, varName) in currentState.variables" :key="varName" class="var-item">
                    <span class="var-name">{{ varName }}</span>
                    <el-icon class="arrow-icon"><Right /></el-icon>
                    <span class="var-addr">{{ addr }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="audit-card" style="margin-top: 20px" v-if="auditResults">
      <template #header>
        <div class="card-header">
          <span>代码审核结果</span>
          <div class="audit-summary">
            <el-tag type="danger" size="small" v-if="auditResults.summary.errors > 0">
              错误: {{ auditResults.summary.errors }}
            </el-tag>
            <el-tag type="warning" size="small" v-if="auditResults.summary.warnings > 0">
              警告: {{ auditResults.summary.warnings }}
            </el-tag>
            <el-tag type="info" size="small" v-if="auditResults.summary.info > 0">
              提示: {{ auditResults.summary.info }}
            </el-tag>
          </div>
        </div>
      </template>
      <div class="audit-list" v-if="auditResults.issues.length > 0">
        <el-timeline>
          <el-timeline-item
            v-for="(issue, index) in auditResults.issues"
            :key="index"
            :type="getIssueType(issue.severity)"
          >
            <div class="issue-item">
              <div class="issue-header">
                <span class="issue-line">行 {{ issue.line }}</span>
                <el-tag :type="getIssueTagType(issue.severity)" size="small">{{ issue.severity }}</el-tag>
                <span class="issue-code">{{ issue.code }}</span>
              </div>
              <div class="issue-message">{{ issue.message }}</div>
              <div class="issue-suggestion">
                <el-icon><Lightbulb /></el-icon> {{ issue.suggestion }}
              </div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
      <div v-else class="no-issues">
        <el-empty description="代码审核通过，未发现问题" />
      </div>
    </el-card>

    <el-card class="console-card" style="margin-top: 20px" v-if="parsedVariables">
      <template #header>
        <span>变量详情</span>
      </template>
      <el-row :gutter="20">
        <el-col v-for="(info, name) in parsedVariables" :key="name" :span="8">
          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="变量名">{{ name }}</el-descriptions-item>
            <el-descriptions-item label="类型">{{ info.type }}</el-descriptions-item>
            <el-descriptions-item label="值">{{ formatValue(info.value) }}</el-descriptions-item>
            <el-descriptions-item label="地址">{{ info.address }}</el-descriptions-item>
          </el-descriptions>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { VideoPlay, RefreshLeft, DocumentCopy, DArrowLeft, DArrowRight, Right, Search, Lightbulb } from '@element-plus/icons-vue'

const route = useRoute()
const code = ref(`a = [1, 2, 3]
b = a
c = 42
d = "hello"`)
const language = ref('python')

onMounted(() => {
  if (route.state?.code) {
    code.value = route.state.code
  }
})
const loading = ref(false)
const auditLoading = ref(false)
const parsedVariables = ref(null)
const simulationStates = ref([])
const currentStep = ref(0)
const currentState = ref(null)
const auditResults = ref(null)

async function runAnalysis() {
  loading.value = true
  try {
    const response = await axios.post('/api/parse/simulate', {
      code: code.value,
      language: language.value
    })
    
    if (response.data.success) {
      parsedVariables.value = response.data.data.variables
      simulationStates.value = response.data.data.states
      currentStep.value = 0
      if (simulationStates.value.length > 0) {
        currentState.value = simulationStates.value[0]
      }
    }
  } catch (error) {
    console.error('分析失败:', error)
  } finally {
    loading.value = false
  }
}

async function runAudit() {
  auditLoading.value = true
  try {
    const response = await axios.post('/api/parse/audit', {
      code: code.value,
      language: language.value
    })
    
    if (response.data.success) {
      auditResults.value = response.data.data
    }
  } catch (error) {
    console.error('审核失败:', error)
  } finally {
    auditLoading.value = false
  }
}

function nextStep() {
  if (currentStep.value < simulationStates.value.length - 1) {
    currentStep.value++
    currentState.value = simulationStates.value[currentStep.value]
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--
    currentState.value = simulationStates.value[currentStep.value]
  }
}

function reset() {
  parsedVariables.value = null
  simulationStates.value = []
  currentStep.value = 0
  currentState.value = null
  auditResults.value = null
}

function loadExample() {
  code.value = `a = [1, 2, 3]
b = a
c = 42
d = "hello"
e = [1, [2, 3]]`
}

function formatValue(val) {
  if (val === null || val === undefined) return 'null'
  return JSON.stringify(val)
}

function getIssueType(severity) {
  switch (severity) {
    case 'error': return 'danger'
    case 'warning': return 'warning'
    case 'info': return 'info'
    default: return 'default'
  }
}

function getIssueTagType(severity) {
  switch (severity) {
    case 'error': return 'danger'
    case 'warning': return 'warning'
    case 'info': return 'info'
    default: return 'primary'
  }
}
</script>

<style scoped>
.analyze-page {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.code-input {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
}

.button-group {
  display: flex;
  gap: 10px;
}

.step-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.step-indicator {
  padding: 0 15px;
  font-weight: 500;
  color: #2c3e50;
}

.visual-container {
  min-height: 400px;
  background-color: #fafafa;
  border-radius: 8px;
  padding: 20px;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 360px;
}

.memory-visual {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.memory-blocks {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.memory-block {
  background: white;
  border: 2px solid #3498db;
  border-radius: 8px;
  padding: 15px;
  min-width: 150px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.block-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e0e0e0;
}

.block-addr {
  font-size: 12px;
  color: #7f8c8d;
  font-family: monospace;
}

.block-type {
  font-size: 12px;
  background: #3498db;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
}

.block-value {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
  word-break: break-all;
}

.block-refs {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.variables-section h4 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.var-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.var-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 8px 15px;
  border-radius: 6px;
  border: 1px solid #dcdfe6;
}

.var-name {
  font-weight: 600;
  color: #2c3e50;
}

.var-addr {
  font-family: monospace;
  color: #7f8c8d;
  font-size: 12px;
}

.arrow-icon {
  color: #3498db;
}

.audit-summary {
  display: flex;
  gap: 10px;
}

.audit-list {
  max-height: 400px;
  overflow-y: auto;
}

.issue-item {
  padding: 10px 0;
}

.issue-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.issue-line {
  font-family: monospace;
  font-size: 12px;
  color: #7f8c8d;
  background: #f5f5f5;
  padding: 2px 8px;
  border-radius: 4px;
}

.issue-code {
  font-family: monospace;
  font-size: 12px;
  color: #3498db;
}

.issue-message {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 5px;
}

.issue-suggestion {
  font-size: 13px;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 5px;
}

.no-issues {
  padding: 20px;
}
</style>
