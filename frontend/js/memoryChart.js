const COLORS = {
  stack: '#fb7185',
  heap: '#34d399',
  static: '#60a5fa',
  constant: '#94a3b8',
  text: '#e2e8f0',
  arrow: '#cbd5e1'
};

function getContext(canvasId) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.font = '14px Inter, ui-sans-serif';
  ctx.textBaseline = 'top';
  return ctx;
}

function drawRect(ctx, x, y, width, height, color, label) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, width, height);
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1;
  ctx.strokeRect(x, y, width, height);
  if (label) {
    ctx.fillStyle = COLORS.text;
    ctx.fillText(label, x + 8, y + 8);
  }
}

function drawArrow(ctx, fromX, fromY, toX, toY) {
  ctx.strokeStyle = COLORS.arrow;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(fromX, fromY);
  ctx.lineTo(toX, toY);
  ctx.stroke();
  const headSize = 8;
  const angle = Math.atan2(toY - fromY, toX - fromX);
  ctx.fillStyle = COLORS.arrow;
  ctx.beginPath();
  ctx.moveTo(toX, toY);
  ctx.lineTo(toX - headSize * Math.cos(angle - Math.PI / 6), toY - headSize * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(toX - headSize * Math.cos(angle + Math.PI / 6), toY - headSize * Math.sin(angle + Math.PI / 6));
  ctx.closePath();
  ctx.fill();
}

function createTooltip(content, x, y) {
  const tooltip = document.getElementById('canvasTooltip');
  tooltip.innerHTML = content;
  tooltip.style.left = `${x + 16}px`;
  tooltip.style.top = `${y + 16}px`;
  tooltip.classList.remove('hidden');
}

export function drawMemoryLayout(data, canvasId, activeTab = 'layout') {
  const ctx = getContext(canvasId);
  const canvas = document.getElementById(canvasId);
  const padding = 18;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;
  const columnWidth = Math.floor(width * 0.44);
  const left = padding;
  const right = padding + columnWidth + 20;

  const sections = [
    { key: 'stack', title: '栈区', color: COLORS.stack, items: data.stack || [] },
    { key: 'heap', title: '堆区', color: COLORS.heap, items: data.heap || [] },
    { key: 'static', title: '静态区', color: COLORS.static, items: data.static || [] }
  ];

  const rowHeight = 72;
  let yOffset = padding;
  const itemRects = [];

  sections.forEach((section, index) => {
    const x = index === 1 ? right : left;
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(x, yOffset, columnWidth, rowHeight + section.items.length * 78 + 16);
    ctx.fillStyle = COLORS.text;
    ctx.fillText(section.title, x + 12, yOffset + 8);
    section.items.forEach((item, idx) => {
      const itemY = yOffset + 30 + idx * 78;
      drawRect(ctx, x + 8, itemY, columnWidth - 16, 62, section.color, `${item.name || item.type || '未知'} (${item.type || section.key})`);
      ctx.fillStyle = COLORS.text;
      const meta = `地址: ${item.address || 'N/A'}  值: ${item.value || item.content || 'N/A'}`;
      ctx.fillText(meta, x + 16, itemY + 24);

      itemRects.push({
        x: x + 8,
        y: itemY,
        w: columnWidth - 16,
        h: 62,
        tooltip: `<strong>${item.name || item.type}</strong><br/>类型: ${item.type || 'N/A'}<br/>地址: ${item.address || 'N/A'}<br/>值: ${item.value || item.content || 'N/A'}<br/>大小: ${item.size || 'N/A'}<br/>引用计数: ${item.ref_count || item.refs || 'N/A'}`
      });
    });
    yOffset += rowHeight + section.items.length * 78 + 22;
  });

  if (data.references && data.references.length > 0) {
    data.references.forEach((reference) => {
      const source = reference.fromRect;
      const target = reference.toRect;
      if (source && target) {
        drawArrow(ctx, source.x + source.w, source.y + source.h / 2, target.x, target.y + target.h / 2);
      }
    });
  }

  if (activeTab === 'references' && data.references && data.references.length > 0) {
    ctx.fillStyle = COLORS.text;
    ctx.fillText('引用关系演示：从变量到对象指针', left, canvas.height - padding - 20);
  }

  canvas.onmousemove = (event) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
    let matched = false;

    itemRects.forEach((region) => {
      if (!matched && mouseX >= region.x && mouseX <= region.x + region.w && mouseY >= region.y && mouseY <= region.y + region.h) {
        matched = true;
        createTooltip(region.tooltip, event.clientX - rect.left, event.clientY - rect.top);
      }
    });
    if (!matched) {
      document.getElementById('canvasTooltip').classList.add('hidden');
    }
  };
}

export function drawMessage(canvasId, message) {
  const ctx = getContext(canvasId);
  ctx.fillStyle = COLORS.text;
  ctx.textAlign = 'center';
  ctx.fillText(message, ctx.canvas.width / 2, ctx.canvas.height / 2);
  ctx.textAlign = 'left';
}
