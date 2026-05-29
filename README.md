# C 与 Python 数据存储对比可视化网页

本项目提供一个教学用交互式网页，比较 C 语言与 Python 在数据存储、内存布局、引用关系和持久化方式上的差异。

## 目录结构

```
c_python_memory_viz/
├── frontend/
│   ├── index.html
│   ├── styles/main.css
│   ├── js/main.js
│   ├── js/memoryChart.js
│   ├── js/pythonSim.js
│   └── js/codeEditor.js
├── backend/
│   ├── app.py
│   ├── c_compiler.py
│   ├── memory_analyzer.py
│   └── requirements.txt
├── docker/
│   ├── Dockerfile
│   └── start.sh
├── examples/
│   ├── c_samples.json
│   └── py_samples.json
└── README.md
```

## 功能说明

- C 模式：前端将用户代码发送到后端 `/run_c`，后端在 Docker 沙箱中编译运行，提取栈、堆、静态变量信息，并返回 JSON 数据。
- Python 模式：前端模拟 Python 对象模型、小整数缓存、字符串驻留与引用关系，无需后端执行。
- 可视化：使用 Canvas 绘制内存区域、变量块、引用箭头，并支持鼠标悬停查看详细信息。
- 编辑器：集成 CodeMirror，可切换语法高亮，并支持示例代码注入。

## 前置依赖

- Docker
- Python 3.10+
- pip
- 现代浏览器（Chrome/Firefox/Edge）

## 后端部署步骤

1. 进入后端目录并安装依赖：

```bash
cd c_python_memory_viz/backend
pip install -r requirements.txt
```

2. 启动 Docker 沙箱容器：

```bash
cd ../docker
./start.sh
```

3. 启动 FastAPI 后端服务：

```bash
cd ../backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

> 如果端口 `8000` 已被占用，后端也可以改为使用 `8001`，前端默认配置已更新为 `http://127.0.0.1:8001`。
> 
> 也可以直接运行仓库根目录下的 `run_local.ps1`，它会自动启动后端和前端本地服务器。  

## 前端部署

- 直接打开 `frontend/index.html`（推荐使用本地 HTTP 服务器，以避免浏览器跨域或文件访问限制）。
- 使用简单服务器：

```bash
cd c_python_memory_viz/frontend
python -m http.server 5500
```

然后访问 `http://127.0.0.1:5500`。

## 注意事项

- C 代码运行在 Docker 沙箱容器中，后端通过 `c_compiler.py` 将源代码编译并执行。请确保 Docker 容器 `c_sandbox` 正常启动。
- Python 可视化仅为前端模拟，不会将 Python 代码发送到后端。
- 如果后端无法连接，请检查 `app.py` 中的 `API_BASE` 配置，确保前端请求地址和后端服务地址一致。

## 文件说明

- `frontend/index.html`：UI 页面结构。
- `frontend/styles/main.css`：视觉样式与悬停提示。
- `frontend/js/main.js`：交互逻辑、语言切换、按钮行为。
- `frontend/js/memoryChart.js`：Canvas 绘图与悬停提示实现。
- `frontend/js/pythonSim.js`：Python 对象模型模拟逻辑。
- `frontend/js/codeEditor.js`：CodeMirror 编辑器封装。
- `backend/app.py`：FastAPI 应用入口。
- `backend/c_compiler.py`：Docker 沙箱编译与运行 C 代码。
- `backend/memory_analyzer.py`：解析分析输出，生成前端可用 JSON。
- `docker/Dockerfile`：沙箱容器构建配置。
- `docker/start.sh`：启动沙箱容器脚本。
- `examples/`：C / Python 预置示例代码。
