import { initEditor, getCode, setCode, setMode } from './codeEditor.js';
import { drawMemoryLayout, drawMessage } from './memoryChart.js';
import { simulatePython } from './pythonSim.js';

// 后端服务运行在 8001 端口时使用。
const API_BASE = 'http://127.0.0.1:8001';
const langSelect = document.getElementById('languageSelect');
const runButton = document.getElementById('runButton');
const aiButton = document.getElementById('aiButton');
const clearButton = document.getElementById('clearButton');
const statusBar = document.getElementById('statusBar');
const tabButtons = Array.from(document.querySelectorAll('.tab-btn'));
const canvasId = 'memoryCanvas';
const canvasContainer = document.getElementById('canvasContainer');
const canvasWidthInput = document.getElementById('canvasWidth');
const canvasHeightInput = document.getElementById('canvasHeight');
const applyCanvasSizeButton = document.getElementById('applyCanvasSize');
let currentLang = 'c';
let currentTab = 'layout';

function setCanvasSize(width, height) {
  const canvas = document.getElementById(canvasId);
  canvas.width = width;
  canvas.height = height;
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  if (canvasWidthInput) canvasWidthInput.value = width;
  if (canvasHeightInput) canvasHeightInput.value = height;
  drawMessage(canvasId, '准备就绪');
}

function refreshCanvasSize() {
  if (!canvasContainer) return;
  const rect = canvasContainer.getBoundingClientRect();
  const width = Math.max(640, Math.floor(rect.width - 16));
  const height = Math.max(420, Math.floor(rect.height - 16));
  setCanvasSize(width, height);
}

if (canvasContainer) {
  const observer = new ResizeObserver(refreshCanvasSize);
  observer.observe(canvasContainer);
  window.addEventListener('resize', refreshCanvasSize);
}

if (applyCanvasSizeButton) {
  applyCanvasSizeButton.addEventListener('click', () => {
    const width = Number(canvasWidthInput?.value || 900);
    const height = Number(canvasHeightInput?.value || 600);
    if (width >= 640 && height >= 420) {
      setCanvasSize(width, height);
    } else {
      updateStatus('最小尺寸为 640x420。', 'error');
    }
  });
}

const sampleSets = {
  c: [
    {
      name: '栈变量示例',
      code: '#include <stdio.h>\nint main() {\n  int a = 10;\n  int b = 20;\n  printf("a=%d b=%d\\n", a, b);\n  return 0;\n}'
    },
    {
      name: '指针示例',
      code: '#include <stdio.h>\nint main() {\n  int x = 5;\n  int *p = &x;\n  *p = 10;\n  printf("x=%d p=%p\\n", x, (void*)p);\n  return 0;\n}'
    },
    {
      name: '堆分配示例',
      code: '#include <stdio.h>\n#include <stdlib.h>\nint main() {\n  int *arr = malloc(3 * sizeof(int));\n  if (!arr) return 1;\n  arr[0] = 1; arr[1] = 2; arr[2] = 3;\n  printf("arr=%p arr[0]=%d\\n", (void*)arr, arr[0]);\n  free(arr);\n  return 0;\n}'
    }
  ],
  python: [
    {
      name: '小整数缓存',
      code: 'a = 100\nb = 100\nprint(a is b)'
    },
    {
      name: '列表引用',
      code: 'list1 = [1, 2]\nlist2 = list1\nlist2.append(3)\nprint(list1, list2)'
    },
    {
      name: '字符串驻留',
      code: 's1 = "hello"\ns2 = "hello"\nprint(s1 is s2)'
    }
  ]
};

function updateStatus(message, variant = 'info') {
  statusBar.textContent = message;
  statusBar.className = 'rounded-full px-3 py-1 text-sm';
  if (variant === 'error') {
    statusBar.classList.add('bg-rose-500', 'text-white');
  } else if (variant === 'success') {
    statusBar.classList.add('bg-emerald-500', 'text-slate-950');
  } else {
    statusBar.classList.add('bg-slate-800', 'text-slate-300');
  }
}

function setActiveTab(tab) {
  currentTab = tab;
  tabButtons.forEach((button) => {
    button.classList.toggle('bg-cyan-500', button.dataset.tab === tab);
    button.classList.toggle('text-slate-950', button.dataset.tab === tab);
  });
  drawMessage(canvasId, `当前标签：${tab === 'layout' ? '内存布局' : tab === 'references' ? '引用关系' : '持久化方式'}`);
}

async function runCVisualization(code) {
  updateStatus('正在发送 C 代码到后端...', 'info');
  try {
    const response = await fetch(`${API_BASE}/run_c`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    const result = await response.json();
    if (!response.ok) {
      updateStatus(result.detail || 'C 编译运行失败', 'error');
      drawMessage(canvasId, '编译运行错误，请检查状态栏信息。');
      return;
    }
    updateStatus('C 代码执行成功，正在绘制可视化...', 'success');
    drawMemoryLayout(result, canvasId, currentTab);
  } catch (error) {
    updateStatus(`后端请求失败：${error.message}`, 'error');
    drawMessage(canvasId, '无法连接后端服务。');
  }
}

function runPythonVisualization(code) {
  updateStatus('模拟 Python 内存对象关系...', 'info');
  const result = simulatePython(code);
  drawMemoryLayout(result, canvasId, currentTab);
  updateStatus('Python 模拟可视化已生成。', 'success');
}

function randomSample() {
  const samples = sampleSets[currentLang];
  const sample = samples[Math.floor(Math.random() * samples.length)];
  setCode(sample.code);
  updateStatus(`已加载示例：${sample.name}`, 'success');
}

runButton.addEventListener('click', () => {
  const code = getCode();
  if (!code.trim()) {
    updateStatus('代码不能为空。', 'error');
    return;
  }
  if (currentLang === 'c') {
    runCVisualization(code);
  } else {
    runPythonVisualization(code);
  }
});

aiButton.addEventListener('click', () => randomSample());
clearButton.addEventListener('click', () => {
  setCode('');
  updateStatus('编辑器已清空。', 'info');
  drawMessage(canvasId, '请编写代码并点击“运行并可视化”。');
});

langSelect.addEventListener('change', (event) => {
  currentLang = event.target.value;
  const mode = currentLang === 'c' ? 'text/x-csrc' : 'python';
  setMode(mode);
  setCode(sampleSets[currentLang][0].code);
  updateStatus(`${currentLang === 'c' ? '已切换到C模式' : '已切换到Python模式'}`, 'info');
  drawMessage(canvasId, `当前语言：${currentLang.toUpperCase()}`);
});

tabButtons.forEach((button) => {
  button.addEventListener('click', () => setActiveTab(button.dataset.tab));
});

window.addEventListener('load', () => {
  initEditor(sampleSets.c[0].code, 'text/x-csrc');
  setActiveTab('layout');
  drawMessage(canvasId, '请编写代码并点击“运行并可视化”。');
  updateStatus('准备就绪');
});
