---
title: CAD WebView UI - 通用开发规则
date: 2026-03-04
categories:
  - CAD二次开发
  - 前端开发
tags:
  - Vue3
  - TypeScript
  - Element Plus
  - WebView2
  - ObjectARX
  - ZWCAD
  - WPF
  - CommunityToolkit.Mvvm
description: 适用于 CAD 嵌入式 UI 项目的通用开发规则与设计规范
authors:
  - JerryMa
---

# CAD WebView UI - 通用开发规则

适用于 Vue 3 + TypeScript + Element Plus 的 CAD 嵌入式 UI 项目（Dialog / PaletteSet / WebView2）。

---

## 语言和响应

- **始终使用简体中文回复**
- 代码注释和 console.log 使用英文
- MD 文件不要添加自动编号

## 技术栈

- **前端**: Vue 3 组合式 API (`<script setup>`)，TypeScript，Element Plus
- **后端**: C++ (ObjectARX/ZRX) 或 C# (.NET / CommunityToolkit.Mvvm)
- **通信**: WebView2 postMessage
- **编码**: Vue/TS 使用 UTF-8；C++ 使用 GB2312（兼容 CAD 编译器）

---

## Industrial UI Pro 设计规范

### CSS 变量（设计令牌）

```css
:root {
  --cad-bg-primary: #f5f7fa;
  --cad-bg-secondary: #ffffff;
  --cad-bg-header: #e1e1e1;
  --cad-bg-footer: #f5f5f5;
  --cad-bg-hover: #d9ecff;
  --cad-bg-active: #cce8ff;
  --cad-text-primary: #303133;
  --cad-text-secondary: #606266;
  --cad-border: #d4d4d4;
  --cad-border-hover: #409eff;
  --cad-spacing-xs: 4px;
  --cad-spacing-sm: 8px;
  --cad-spacing-md: 12px;
  --cad-font-base: 12px;
  --cad-font-sm: 10px;
  --cad-font-md: 13px;
  --cad-font-mono: 'Consolas', monospace;
  --cad-height-input: 24px;
  --cad-height-button: 26px;
  --cad-transition-fast: 0.15s;
  --z-context-menu: 1999;
  --z-modal-overlay: 2000;
  --z-modal-dialog: 2001;
  --z-tooltip: 3000;
}
```

### 核心设计原则

- **容器约束**: 适配 Dialog/PaletteSet 嵌入式环境，有限尺寸
- **响应式布局**: 必须使用 `width: 100%; height: 100%` 适配任意容器（300px-1200px）
- **紧凑布局**: 高信息密度，12px 基准字体，间距 4px/8px/12px
- **明显反馈**: 所有交互元素必须有明显的悬停色差（#d9ecff）
- **工具导向**: 快速操作，键盘快捷键，即时反馈

### 容器尺寸与响应式断点

| 容器类型 | 默认宽度 | 典型用途 |
|---------|---------|---------|
| 小型 Dialog | 400px | 快速设置、简单表单 |
| 中型 Dialog | 600px | 属性编辑、图块插入 |
| 大型 Dialog | 800px | 表格编辑、数据管理 |
| PaletteSet 面板 | 250-400px | 图块库、图层管理 |

- `< 450px`：单列，侧边栏折叠
- `450-600px`：单列 + 可折叠侧边栏
- `600-800px`：双列，侧边栏可见
- `> 800px`：多列，全功能展示

### 悬停效果 CSS（强制实现）

```css
/* 输入框 */
.el-input__wrapper { border: 1px solid #dcdfe6; transition: all 0.2s; }
.el-input__wrapper:hover { border-color: #409eff !important; background-color: #f5f9ff; }
.el-input__wrapper.is-focus { border-color: #409eff !important; box-shadow: 0 0 0 2px rgba(64,158,255,0.2); }

/* 下拉框 */
.el-select .el-input__wrapper:hover { border-color: #409eff !important; background-color: #f5f9ff; }
.el-select-dropdown__item:hover { background-color: #d9ecff !important; }

/* 表格行 */
.el-table__body tr { transition: background-color 0.15s; }
.el-table__body tr:hover > td { background-color: #d9ecff !important; cursor: pointer; }
.el-table__body tr.current-row > td { background-color: #cce8ff !important; }
.el-table__header th { background-color: #e1e1e1; }

/* 按钮 */
.el-button { transition: all 0.2s; }
.el-button:hover { background-color: #d9ecff; border-color: #409eff; color: #409eff; }

/* 树节点 */
.el-tree-node__content { transition: background-color 0.15s; }
.el-tree-node__content:hover { background-color: #d9ecff !important; }
```

### 紧凑样式覆盖

```css
.el-table { font-size: 12px; width: 100%; }
.el-table .cell { padding: 0 4px; line-height: 20px; }
.el-table__cell { padding: 2px 0; }
.el-form-item { margin-bottom: 8px; }
.el-form-item__label { font-size: 12px; line-height: 24px; padding: 0 8px 0 0; }
.el-input__inner { height: 24px; line-height: 24px; font-size: 12px; }
.el-input-number { width: 100%; }
.el-tree-node__content { height: 24px; }
.el-tree { font-size: 12px; }
.el-collapse-item__header { font-size: 12px; height: 28px; padding-left: 8px; background: #f5f7fa; }
.el-collapse-item__content { padding: 8px 8px 4px; }
```

### 禁止使用

- ❌ 花哨渐变背景（装饰性 `linear-gradient`）
- ❌ 玻璃态效果（`backdrop-filter`, `blur`）
- ❌ 过度动画（> 300ms）
- ❌ 大留白（padding/margin > 24px）
- ❌ 背景装饰（渐变球、光效、`absolute` 装饰层）
- ❌ 过大的阴影（`box-shadow` blur > 12px）
- ❌ `ElMessageBox.confirm`（z-index 问题，用自定义 `el-dialog` 替代）

---

## 布局模式

### SplitPanel（分栏 + 可折叠侧边栏）

```css
.split-container { display: flex; height: 100%; overflow: hidden; }
.sidebar { display: flex; flex-direction: column; border-right: 1px solid var(--cad-border); background: #f9fafc; transition: width 0.2s; min-width: 120px; }
.sidebar-header { padding: 6px 8px; background: var(--cad-bg-header); font-weight: bold; border-bottom: 1px solid var(--cad-border); font-size: 12px; }
.splitter-handle { width: 8px; background: #f0f0f0; border-right: 1px solid var(--cad-border); cursor: pointer; display: flex; align-items: center; justify-content: center; }
.splitter-handle:hover { background: #e0e0e0; }
.main-content { flex: 1; overflow: hidden; display: flex; flex-direction: column; background: #fff; }
.content-header { padding: 6px 8px; border-bottom: 1px solid var(--cad-border); background: var(--cad-bg-footer); flex-shrink: 0; }
.content-body { flex: 1; overflow: hidden; }
```

### 标准面板（Header + Body + Footer）

```css
.cad-panel { display: flex; flex-direction: column; width: 100%; height: 100%; font-size: 12px; }
.panel-header { padding: 6px 10px; background: var(--cad-bg-header); border-bottom: 1px solid var(--cad-border); display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.panel-body { flex: 1; overflow: hidden; }
.panel-footer { padding: 6px 10px; background: var(--cad-bg-footer); border-top: 1px solid var(--cad-border); display: flex; gap: 8px; flex-wrap: wrap; flex-shrink: 0; }
```

---

## 属性编辑器规范

### 验证规则

- ✅ 验证规则集成在 Edit Property 对话框中，不要单独对话框
- ✅ 提供默认错误提示词和自定义选项
- ✅ 数字输入不使用 `:min/:max` 强制限制，通过 `@blur/@change` 验证
- ✅ 使用 `prop.Error = undefined` 清除错误（不用 `delete`）
- ✅ 正确处理 `0` 和 `false` 作为有效值

### 验证时机

| 输入类型 | @input | @blur | @change |
|---------|--------|-------|---------|
| Text / Textarea | ✅ | ✅ | ✅ |
| Number | ❌ | ✅ | ✅ |
| Select | ❌ | ❌ | ✅ |

### 错误提示样式

```css
.property-form-item.has-error {
  background: #fef0f0;
  border-left: 2px solid #f56c6c;
  padding-left: 4px;
  margin-left: -6px;
}
.property-error {
  display: flex; align-items: center; gap: 4px;
  color: #f56c6c; font-size: 10px;
  padding: 4px 0; margin-top: -4px;
}
```

### 删除确认对话框

```typescript
// ❌ 禁止使用 ElMessageBox.confirm（z-index 问题）
// ✅ 使用自定义 el-dialog
const confirmDeleteDialog = reactive({
  visible: false,
  message: '',
  onConfirm: null as (() => void) | null
})
```

---

## WebView2 通信模式

```typescript
const postMsg = (msg: object) =>
  window.chrome?.webview?.postMessage(JSON.stringify(msg))

window.chrome?.webview?.addEventListener('message', (e: any) => {
  const data = JSON.parse(e.data)
  switch (data.type) {
    case 'blockList': handleBlockList(data.data); break
    case 'entitySelected': handleEntitySelected(data.data); break
    case 'error': console.error('[CAD]', data.message); break
  }
})

// 常用消息格式
postMsg({ type: 'command', action: 'insertBlock', data: { name: 'BOLT', path: 'C:\\blocks\\bolt.dwg' } })
postMsg({ type: 'getEntityList' })
postMsg({ type: 'command', action: 'highlightEntity', data: { handle: '1A3F' } })
```

---

## 响应式布局监听模板

```vue
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const containerWidth = ref(600)
const updateLayout = () => {
  const el = document.querySelector('.container') as HTMLElement
  if (el) containerWidth.value = el.offsetWidth
}
onMounted(() => { updateLayout(); window.addEventListener('resize', updateLayout) })
onUnmounted(() => { window.removeEventListener('resize', updateLayout) })
</script>

<template>
  <div class="container"
    :class="{
      'compact': containerWidth < 450,
      'small': containerWidth >= 450 && containerWidth < 600,
      'medium': containerWidth >= 600 && containerWidth < 800,
      'large': containerWidth >= 800
    }">
  </div>
</template>
```

---

## C++ 开发规范 (ObjectARX/ZRX)

- **标准**: C++17 及以下
- **字符串**: 使用 `AcString` / `ZcString` 或 `std::wstring`
- **内存管理**: 严格管理 CAD 数据库对象（`AcDbObjectPointer` 或智能指针）
- **注释**: 尽量使用英文
- **推荐库**:

| 用途 | 推荐库 | 说明 |
|------|--------|------|
| JSON | `nlohmann/json` | Header-only，语法简洁，直接 `#include` |
| XML | `pugixml` | 轻量高性能，Header-only 可选，XPath 支持 |
| YAML | `yaml-cpp` | C++ YAML 解析标准选择，MIT 协议 |
| INI | `inih` (benhoyt/inih) | 极简 C 库，单文件，直接嵌入项目 |
| CSV | `csv-parser` (vincentlaucsb) | Header-only，流式解析，高性能 |
| 日志 | `spdlog` | Header-only，高性能异步日志 |
| HTTP | `cpp-httplib` | Header-only，适合简单 REST 调用 |

## C# / WPF 开发规范

- **框架**: CommunityToolkit.Mvvm（不使用 Source Generator）
- **语言版本**: C# 7.3
- **MVVM**: 使用 `ObservableObject`、`RelayCommand`
- **注释**: 尽量使用英文
- **推荐库**:

| 用途 | 推荐库 (NuGet) | 说明 |
|------|----------------|------|
| JSON | `System.Text.Json` 或 `Newtonsoft.Json` | 内置优先，复杂场景用 Newtonsoft |
| XML | `System.Xml.Linq` (XDocument) | .NET 内置，LINQ to XML |
| YAML | `YamlDotNet` | C# YAML 解析标准选择 |
| INI | `ini-parser` (rickyah) | 轻量 INI 读写 |
| CSV | `CsvHelper` | C# CSV 处理标准库 |
| Excel | `EPPlus` 或 `ClosedXML` | EPPlus 5+ 商用需授权，ClosedXML 为 MIT |
| 日志 | `Serilog` | 结构化日志，支持多种 Sink |
| 音频 | `NAudio` | 音频录制/播放，适合语音批注场景 |
| SQLite | `Microsoft.Data.Sqlite` | 轻量数据库，适合全局变量存储 |

---

## Vue 组件开发规范

### 新建组件检查清单

添加或修改函数时必须检查：
- [ ] 声明位置是否正确
- [ ] 类型定义是否完整
- [ ] 导入路径是否正确
- [ ] 调用位置是否更新

### 组件模板

```vue
<template>
  <div class="component-name"><!-- 内容 --></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Props { title: string; count?: number }
const props = withDefaults(defineProps<Props>(), { count: 0 })

interface Emits { (e: 'update', value: number): void; (e: 'close'): void }
const emit = defineEmits<Emits>()
</script>

<style scoped>
.component-name {
  width: 100%; height: 100%;
  padding: var(--cad-spacing-md);
  background: var(--cad-bg-secondary);
  font-size: var(--cad-font-base);
}
.component-name :deep(.el-input__wrapper:hover) { border-color: #409eff !important; background-color: #f5f9ff; }
.component-name :deep(.el-table__body tr:hover > td) { background-color: #d9ecff !important; cursor: pointer; }
</style>
```

---

## MCP Feedback（重要）

在完成任何任务后，必须调用 MCP feedback 工具：

```typescript
mcp_mcp-feedback-enhanced_interactive_feedback({
  project_directory: ".",
  summary: "我已完成了[具体任务描述]。请查看并提供反馈。",
  timeout: 600
})
```

---

## Git 提交规范

```
<type>(<scope>): <subject>
```

类型：`feat` | `fix` | `docs` | `style` | `refactor` | `perf` | `test` | `chore`
