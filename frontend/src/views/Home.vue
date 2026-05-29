<template>
  <div class="home">
    <div class="hero-section">
      <h2>可视化你的程序内存</h2>
      <p>直观理解变量、引用、复制的工作原理</p>
    </div>

    <div class="features-grid">
      <el-card class="feature-card" shadow="hover">
        <div class="feature-icon python-icon">
          <el-icon :size="40"><Document /></el-icon>
        </div>
        <h3>Python 分析</h3>
        <p>解析 Python 代码，可视化变量和内存状态</p>
        <el-button type="primary" @click="$router.push('/analyze/python')">开始使用</el-button>
      </el-card>

      <el-card class="feature-card" shadow="hover">
        <div class="feature-icon c-icon">
          <el-icon :size="40"><Document /></el-icon>
        </div>
        <h3>C/C++ 分析</h3>
        <p>分析 C/C++ 代码，展示指针和内存分配</p>
        <el-button type="primary" @click="$router.push('/analyze/c')">开始使用</el-button>
      </el-card>

      <el-card class="feature-card" shadow="hover">
        <div class="feature-icon copy-icon">
          <el-icon :size="40"><Files /></el-icon>
        </div>
        <h3>复制对比</h3>
        <p>理解引用、浅拷贝、深拷贝的区别</p>
        <el-button type="success" @click="$router.push('/examples')">查看示例</el-button>
      </el-card>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="info-card">
          <template #header>
          <span>什么是内存可视化？</span>
        </template>
        <p>内存可视化可以帮助你更好地理解程序在运行时如何使用内存，包括：</p>
        <ul>
          <li>变量如何在内存中存储</li>
          <li>引用和拷贝的区别</li>
          <li>列表、字典等数据结构的内存布局</li>
        </ul>
      </el-card>
    </el-col>
    <el-col :span="12">
      <el-card class="info-card">
        <template #header>
          <span>如何使用？</span>
        </template>
        <p>只需几步就能开始使用：</p>
        <ol>
          <li>选择语言（Python 或 C/C++）</li>
          <li>输入或粘贴代码</li>
          <li>点击运行分析</li>
          <li>单步查看内存变化</li>
        </ol>
      </el-card>
    </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { Document, Files } from '@element-plus/icons-vue'
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero-section h2 {
  color: white;
  font-size: 36px;
  margin-bottom: 15px;
}

.hero-section p {
  color: #bdc3c7;
  font-size: 18px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.feature-card {
  text-align: center;
  padding: 30px;
}

.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.python-icon {
  background-color: #e3f2fd;
  color: #3776ab;
}

.c-icon {
  background-color: #e3f2fd;
  color: #00599C;
}

.copy-icon {
  background-color: #e8f5e9;
  color: #27ae60;
}

.feature-card h3 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.feature-card p {
  color: #7f8c8d;
  margin-bottom: 20px;
}

.info-card {
  margin-bottom: 20px;
}

.info-card ul, .info-card ol {
  margin: 15px 0 0 20px;
  color: #34495e;
}

.info-card li {
  margin: 8px 0;
}
</style>
