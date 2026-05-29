# 内存可视化系统

一个用于可视化程序内存管理的Web应用，支持Python和C/C++代码分析与内存状态可视化。

## 功能特性

- **Python代码分析** - 使用AST解析Python代码，可视化变量赋值、列表操作等
- **C/C++代码分析** - 支持C/C++代码解析，展示指针、数组和内存分配
- **代码审核功能** - 静态代码分析，检测语法错误、逻辑问题并提供修复建议
- **引用与拷贝对比** - 直观展示引用赋值、浅拷贝、深拷贝的区别
- **列表与数组可视化** - 支持一维、二维列表/数组的内存展示
- **单步执行** - 可以单步查看内存变化过程
- **用户系统** - 用户注册、登录、历史记录管理
- **响应式界面** - 基于Element Plus的现代化UI设计

## 技术栈

### 后端
- **FastAPI** - Web框架（v0.109.0）
- **SQLAlchemy** - ORM（v2.0+）
- **SQLite** - 数据库
- **Python AST** - Python代码解析
- **pycparser** - C/C++代码解析
- **python-jose** - JWT认证
- **passlib** - 密码加密

### 前端
- **Vue 3** - 前端框架
- **Vite** - 构建工具（v5.0+）
- **Element Plus** - UI组件库
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP客户端

## 快速开始

### 本地开发

#### 后端开发
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### 前端开发
```bash
cd frontend
npm install
npm install pinia  # 安装状态管理
npm run dev
```

访问 http://localhost:5173 开始使用

### Docker部署

```bash
# 构建和启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 使用说明

### Python代码分析
1. 进入「代码分析」->「Python分析」页面
2. 在代码编辑器中输入Python代码
3. 点击「运行分析」按钮查看内存可视化
4. 使用单步执行控件查看内存变化过程
5. 点击「代码审核」检测代码中的问题

### C/C++代码分析
1. 进入「代码分析」->「C/C++分析」页面
2. 在代码编辑器中输入C/C++代码
3. 支持变量声明、指针、数组等解析

### 示例学习
1. 进入「示例」页面
2. 选择感兴趣的示例场景（变量赋值、引用拷贝、列表操作）
3. 点击卡片直接跳转到分析页面并加载示例代码

## 项目结构

```
memory-visualizer/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由（auth.py, parse.py, visualize.py）
│   │   ├── core/           # 核心功能
│   │   │   ├── python_parser.py    # Python代码解析器
│   │   │   ├── c_parser.py         # C/C++代码解析器
│   │   │   ├── memory_simulator.py # 内存模拟器
│   │   │   └── code_auditor.py     # 代码审核器
│   │   ├── db/             # 数据库相关（models.py, crud.py）
│   │   ├── utils/          # 工具函数（auth.py）
│   │   ├── config.py       # 配置文件
│   │   └── main.py         # FastAPI入口
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   │   ├── Home.vue           # 首页
│   │   │   ├── PythonAnalysis.vue  # Python分析页
│   │   │   ├── CAnalysis.vue       # C/C++分析页
│   │   │   ├── Examples.vue        # 示例页
│   │   │   └── UserCenter.vue      # 用户中心
│   │   ├── stores/         # Pinia状态管理
│   │   │   ├── user.js            # 用户状态
│   │   │   └── analysis.js        # 分析状态
│   │   ├── router/         # 路由配置（index.js）
│   │   ├── App.vue         # 根组件
│   │   ├── main.js         # 入口文件
│   │   └── assets/styles/  # 全局样式
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── test_api.py             # API测试脚本
└── README.md
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的API文档

### 主要API端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/parse/python` | POST | Python代码解析 |
| `/api/parse/simulate` | POST | 内存模拟 |
| `/api/parse/audit` | POST | 代码审核 |
| `/health` | GET | 健康检查 |

## 代码审核功能

代码审核器支持检测以下类型的问题：

**Python代码**
- 语法错误检测
- 条件语句中使用赋值而非比较（`if x = 5` vs `if x == 5`）
- 无限循环检测（`while True`）
- 空循环体检测
- 行长度过长检测
- import语句位置检测
- 空代码块检测

**C/C++代码**
- 条件语句中赋值错误
- 行长度检测
- 行内注释检测
- TODO/FIXME注释检测
- 花括号风格检测

## 测试

运行API测试脚本：

```bash
python test_api.py
```

## 开发计划

- [x] Python代码基础解析
- [x] 内存可视化基础
- [x] 单步执行功能
- [x] 代码审核功能
- [x] 用户登录注册
- [x] 页面组件完善
- [x] Pinia状态管理
- [x] C/C++指针和数组解析
- [ ] 历史记录持久化
- [ ] 更丰富的可视化效果
- [ ] 代码导出功能

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
