<template>
  <div class="examples-page">
    <h2>可视化示例</h2>
    <p class="subtitle">通过实例理解内存管理的关键概念</p>

    <el-tabs v-model="activeTab" class="examples-tabs">
      <el-tab-pane label="变量与赋值" name="variables">
        <el-row :gutter="20">
          <el-col :span="8" v-for="example in variableExamples" :key="example.id">
            <el-card class="example-card" shadow="hover" @click="loadExample(example)">
              <div class="example-icon" :style="{ backgroundColor: example.color + '20', color: example.color }">
                <el-icon :size="36"><component :is="example.icon" /></el-icon>
              </div>
              <h3>{{ example.title }}</h3>
              <p>{{ example.description }}</p>
              <div class="example-code">
                <pre><code>{{ example.code }}</code></pre>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <el-tab-pane label="引用与拷贝" name="copy">
        <el-card class="copy-comparison-card">
          <template #header>
            <div class="card-header">
              <span>引用 vs 浅拷贝 vs 深拷贝</span>
            </div>
          </template>
          <div class="comparison-content">
            <div class="comparison-item reference">
              <h4>引用赋值</h4>
              <div class="code-block">
                <pre><code>a = [1, 2, 3]
b = a</code></pre>
              </div>
              <p class="explanation">
                b 与 a 指向同一内存地址，修改一个会影响另一个
              </p>
              <el-button type="danger" @click="loadCopyExample('reference')">
                查看示例
              </el-button>
            </div>

            <div class="comparison-item shallow">
              <h4>浅拷贝</h4>
              <div class="code-block">
                <pre><code>a = [1, [2, 3]]
b = a.copy()</code></pre>
              </div>
              <p class="explanation">
                新建列表对象，但内部元素仍为引用
              </p>
              <el-button type="warning" @click="loadCopyExample('shallow')">
                查看示例
              </el-button>
            </div>

            <div class="comparison-item deep">
              <h4>深拷贝</h4>
              <div class="code-block">
                <pre><code>import copy
a = [1, [2, 3]]
b = copy.deepcopy(a)</code></pre>
              </div>
              <p class="explanation">
                完全独立的副本，递归复制所有对象
              </p>
              <el-button type="success" @click="loadCopyExample('deep')">
                查看示例
              </el-button>
            </div>
          </div>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="列表与数组" name="lists">
        <el-row :gutter="20">
          <el-col :span="8" v-for="example in listExamples" :key="example.id">
            <el-card class="example-card" shadow="hover" @click="loadExample(example)">
              <div class="example-icon" :style="{ backgroundColor: example.color + '20', color: example.color }">
                <el-icon :size="36"><component :is="example.icon" /></el-icon>
              </div>
              <h3>{{ example.title }}</h3>
              <p>{{ example.description }}</p>
              <div class="example-code">
                <pre><code>{{ example.code }}</code></pre>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Guide, Files, DataLine, Box } from '@element-plus/icons-vue'

const router = useRouter()
const activeTab = ref('variables')

const variableExamples = [
  {
    id: 1,
    title: '基本变量',
    description: '理解基本类型变量的存储',
    icon: Guide,
    color: '#3498db',
    code: 'a = 10\nb = 20\nc = a'
  },
  {
    id: 2,
    title: '字符串',
    description: 'Python字符串的不可变特性',
    icon: Guide,
    color: '#9b59b6',
    code: 's = "hello"\nt = s\ns = "world"'
  },
  {
    id: 3,
    title: '字典操作',
    description: '字典的内存结构与引用',
    icon: DataLine,
    color: '#1abc9c',
    code: 'd = {"x": 1, "y": 2}\ne = d\nd["z"] = 3'
  }
]

const listExamples = [
  {
    id: 4,
    title: '简单列表',
    description: '一维列表的内存布局',
    icon: DataLine,
    color: '#27ae60',
    code: 'nums = [1, 2, 3, 4]\nnums.append(5)\nnums[0] = 100'
  },
  {
    id: 5,
    title: '二维列表',
    description: '嵌套列表的内存关系',
    icon: Box,
    color: '#f39c12',
    code: 'matrix = [[1, 2], [3, 4]]\nrow = matrix[0]\nrow[0] = 99'
  },
  {
    id: 6,
    title: '列表切片',
    description: '切片操作与浅拷贝',
    icon: DataLine,
    color: '#e67e22',
    code: 'a = [1, 2, 3]\nb = a[:]\nb[0] = 99'
  }
]

function loadExample(example) {
  router.push({
    path: '/analyze/python',
    state: { code: example.code }
  })
}

function loadCopyExample(type) {
  let code = ''
  if (type === 'reference') {
    code = 'a = [1, 2, 3]\nb = a\nprint(a is b)  # True'
  } else if (type === 'shallow') {
    code = 'a = [1, [2, 3]]\nb = a.copy()\nb[1][0] = 99\nprint(a)  # [1, [99, 3]]'
  } else if (type === 'deep') {
    code = 'import copy\na = [1, [2, 3]]\nb = copy.deepcopy(a)\nb[1][0] = 99\nprint(a)  # [1, [2, 3]]'
  }
  router.push({
    path: '/analyze/python',
    state: { code: code }
  })
}
</script>

<style scoped>
.examples-page {
  max-width: 1200px;
  margin: 0 auto;
}

.examples-page h2 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 28px;
}

.subtitle {
  color: #7f8c8d;
  margin-bottom: 30px;
  font-size: 16px;
}

.examples-tabs {
  margin-top: 20px;
}

.example-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s;
}

.example-card:hover {
  transform: translateY(-5px);
}

.example-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.example-card h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.example-card p {
  color: #7f8c8d;
  margin-bottom: 15px;
}

.example-code {
  background: #2c3e50;
  padding: 12px;
  border-radius: 6px;
}

.example-code pre {
  margin: 0;
}

.example-code code {
  color: #27ae60;
  font-size: 13px;
}

.copy-comparison-card {
  margin-top: 20px;
}

.comparison-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.comparison-item {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  border: 2px solid;
}

.comparison-item.reference {
  border-color: #e74c3c;
}

.comparison-item.shallow {
  border-color: #f39c12;
}

.comparison-item.deep {
  border-color: #27ae60;
}

.comparison-item h4 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.code-block {
  background: #2c3e50;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 15px;
}

.code-block pre {
  margin: 0;
}

.code-block code {
  color: #ecf0f1;
  font-size: 13px;
  text-align: left;
  display: block;
}

.explanation {
  color: #7f8c8d;
  margin-bottom: 15px;
  min-height: 48px;
}
</style>
