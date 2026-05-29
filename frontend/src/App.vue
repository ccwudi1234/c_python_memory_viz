<template>
  <div id="app">
    <el-container class="main-container">
      <el-header class="header">
        <div class="header-content">
          <h1 class="logo">内存可视化系统</h1>
          <div class="nav-menu">
            <router-link to="/" class="nav-item">首页</router-link>
            <el-dropdown trigger="click" class="nav-item">
              <span class="el-dropdown-link">
                代码分析
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="$router.push('/analyze/python')">
                    <el-icon :size="18" style="margin-right: 8px; color: #3776AB;"><Document /></el-icon>
                    Python分析
                  </el-dropdown-item>
                  <el-dropdown-item @click="$router.push('/analyze/c')">
                    <el-icon :size="18" style="margin-right: 8px; color: #00599C;"><Document /></el-icon>
                    C/C++分析
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <router-link to="/examples" class="nav-item">示例</router-link>
            <router-link to="/user-center" class="nav-item">
              <el-icon><User /></el-icon> 用户中心
            </router-link>
          </div>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ArrowDown, Document, User } from '@element-plus/icons-vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  width: 100%;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.main-container {
  height: 100vh;
}

.header {
  background-color: #2c3e50;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo {
  color: white;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.nav-menu {
  display: flex;
  gap: 30px;
  align-items: center;
}

.nav-item {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: #3498db;
}

.el-dropdown-link {
  color: #ecf0f1;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.el-dropdown-link:hover {
  color: #3498db;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
