---
title: Cursor 开发环境配置迁移指南
date: 2026-03-05
categories:
  - 开发工具
  - Cursor
tags:
  - Cursor
  - MCP
  - Skills
  - Rules
  - 环境配置
description: 记录 Cursor IDE 的完整配置，包含全局规则、MCP 工具、Skills 技能库等，换新电脑时可直接参照还原
author: JerryMa
---

# Cursor 开发环境配置迁移指南

本文档记录当前 Cursor 的完整配置，换新电脑时按步骤操作即可还原。

---

## 一、安装软件

1. 下载并安装 [Cursor](https://cursor.sh/)
2. 登录账号（Settings > Sign in）

---

## 二、全局规则（Rules for AI）

### 规则体系设计说明

三层规则各司其职，互不重叠：

| 层级 | 位置 | 内容 |
|---|---|---|
| **User Rules** | Cursor Settings > General | 最基础：语言、MCP、WPF |
| **cursor.rules** | settings.json | 技术规范：编码、Vue、C++、UI |
| **.cursorrules** | 项目根目录 | 项目细节：完整 UI 规范、组件模板 |

### 方式 A：通过 UI 设置（推荐）

1. `Ctrl+Shift+J` 打开 Cursor Settings
2. 找到 **Rules for AI** 文本框
3. 粘贴以下内容（仅技术规范，不含已在 User Rules 的基础规则）：

```
## 文件编码规范
- Vue/TS 文件：UTF-8
- C++ 文件：GB2312（兼容 CAD 编译器）

## Vue 3 规范
- 使用 `<script setup lang="ts">` 写法，所有 Props/Emits 必须有类型定义，避免 `any`
- UI 组件库优先使用 **Element Plus**，避免自行实现已有的组件
- 不要为简单任务创建文档文件（README/CHANGELOG 等）

## CAD 嵌入式 UI 规范（Industrial UI Pro）
- 所有容器必须使用 `width: 100%; height: 100%` 适配 PaletteSet/Dialog
- 基准字号 12px，间距 4px/8px/12px，禁止大留白(> 24px)
- 所有交互元素必须有悬停高亮（#d9ecff），过渡时间 0.15-0.2s
- 禁止：渐变装饰背景、玻璃态效果（backdrop-filter）、过度动画(> 300ms)
- 属性编辑器不使用 ElMessageBox.confirm，改用自定义 el-dialog
- 数字输入不用 :min/:max 强制限制，验证只在 @blur/@change 触发

## C++ 开发规范（ObjectARX/ZRX）
- 标准：C++17 或以下；框架：ObjectARX (AutoCAD) / ZRX (ZWCAD)
- **字符集：Unicode**，所有字符串字面量使用 `L""` 前缀，字符串类型使用 `std::wstring`
- JSON：使用 `nlohmann/json`（wide string 需先转 UTF-8）
- XML：使用 `pugixml`（pugi::xml_document）
- YAML：使用 `yaml-cpp`（YAML::Node）
- Excel：使用 `libxl`（xlBook）或 `OpenXLSX`
- 日志：使用 `spdlog`（spdlog::info/warn/error）
- 严格管理 CAD 数据库对象生命周期（open 后必须 close）
- **所有 C++ 代码中的字符串字面量、注释、日志均使用英文**（除非有特殊说明）

## C# 开发规范
- JSON：使用 `Newtonsoft.Json`（JsonConvert.SerializeObject/DeserializeObject）
- YAML：使用 `YamlDotNet`（IDeserializer/ISerializer）
- XML：使用 `System.Xml.Linq`（XDocument/XElement）或 `XmlSerializer`
- Excel：使用 `EPPlus`（ExcelPackage）或 `NPOI`（HSSFWorkbook/XSSFWorkbook）；优先 EPPlus
- CSV：使用 `CsvHelper`（CsvReader/CsvWriter）
- HTTP 请求：使用 `HttpClient`（推荐）或 `RestSharp`
- 日志：使用 `NLog` 或 `Serilog`
- 异步：优先使用 async/await，避免 .Result 和 .Wait() 死锁
- 依赖注入：使用 `Microsoft.Extensions.DependencyInjection`

## Git 提交规范
- 格式：`<type>(<scope>): <subject>`（feat/fix/docs/refactor/chore）
```

### 方式 B：直接修改 settings.json

文件位置：`%APPDATA%\Cursor\User\settings.json`（Windows）

在 JSON 对象中添加 `cursor.rules` 字段，内容同上（将换行替换为 `\n`）。

---

## 三、User Rules（最高优先级规则）

1. `Ctrl+Shift+J` → **General** → **User Rules**
2. 添加以下规则（每行一条）：

```
在任何过程、任务或对话中，无论是提问、回应还是完成阶段任务，都必须调用 MCP mcp-feedback-enhanced。
Always respond in Chinese-simplified
所有WPF代码都基于C#7.3和CommunityToolkit.Mvvm框架编写
WPF代码不要使用 Source Generator
md文件不要添加编号
注释和打印提示尽量用英文
```

---

## 四、Skills（全局技能库）

Skills 存放目录：`C:\Users\<用户名>\.cursor\skills-cursor\`

### 当前已有的全局 Skills

| Skill 名称 | 描述 | 来源 |
|---|---|---|
| `create-rule` | 创建 Cursor rules（.mdc 规则文件） | Cursor 内置 |
| `create-skill` | 创建新 Agent Skill（SKILL.md） | Cursor 内置 |
| `create-subagent` | 创建自定义 Subagent（任务专属 AI 代理） | Cursor 内置 |
| `migrate-to-skills` | 将 .mdc rules/命令迁移为 Skills 格式 | Cursor 内置 |
| `update-cursor-settings` | 修改 Cursor/VSCode settings.json | Cursor 内置 |
| `industrial-ui-pro` | CAD 嵌入式 UI 设计规范（CSS 变量、悬停样式、布局模式） | 自定义 |
| `vue-prototype-builder` | Vue 3 + Element Plus CAD UI 代码模板（5个完整组件模板） | 自定义 |

### 迁移自定义 Skills 到新电脑

**方法 1：从 Git 仓库直接复制（需先 Clone 仓库）**

```powershell
$skillsGlobal = "$env:USERPROFILE\.cursor\skills-cursor"
New-Item -ItemType Directory -Force -Path "$skillsGlobal\industrial-ui-pro"
New-Item -ItemType Directory -Force -Path "$skillsGlobal\vue-prototype-builder"

# 仅复制 SKILL.md（已精简为仅需此文件）
Copy-Item "E:\Gitee\project\api-demo\Vue\CADWebViewUI\.cursor\skills\industrial-ui-pro\SKILL.md" -Destination "$skillsGlobal\industrial-ui-pro\SKILL.md" -Force
Copy-Item "E:\Gitee\project\api-demo\Vue\CADWebViewUI\.cursor\skills\vue-prototype-builder\SKILL.md" -Destination "$skillsGlobal\vue-prototype-builder\SKILL.md" -Force

Write-Host "Skills 已复制完成"
```

**方法 2：从本文档第十节复制内容（无需 Git）**

1. 找到本文档第十节「Skill 完整内容」
2. 将 `industrial-ui-pro` 的内容保存为 `C:\Users\<用户名>\.cursor\skills-cursor\industrial-ui-pro\SKILL.md`
3. 将 `vue-prototype-builder` 的内容保存为 `C:\Users\<用户名>\.cursor\skills-cursor\vue-prototype-builder\SKILL.md`

> 注意：Cursor 内置的 5 个 Skills（create-rule、create-skill 等）会随 Cursor 自动安装，无需手动复制。

---

## 五、MCP 工具配置

配置文件位置：`C:\Users\<用户名>\.cursor\mcp.json`

### 当前 mcp.json 完整内容

```json
{
  "mcpServers": {
    "mcp-feedback-enhanced": {
      "command": "uvx",
      "args": [
        "mcp-feedback-enhanced@latest"
      ],
      "timeout": 600,
      "env": {
        "MCP_DESKTOP_MODE": "true",
        "MCP_WEB_HOST": "127.0.0.1",
        "MCP_WEB_PORT": "8765",
        "MCP_DEBUG": "false"
      },
      "autoApprove": [
        "interactive_feedback"
      ]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    },
    "server-memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

### 新电脑安装步骤

1. 安装 [Python](https://www.python.org/) 并确保 `pip` 可用
2. 安装 `uv`（用于运行 `uvx`）：
   ```bash
   pip install uv
   ```
3. 安装 Node.js（用于 `npx`）：[https://nodejs.org/](https://nodejs.org/)
4. 将上方 mcp.json 内容保存到 `C:\Users\<用户名>\.cursor\mcp.json`
5. 重启 Cursor，在 Cursor Settings > MCP 中验证工具已加载

---

## 六、编辑器基本设置

`%APPDATA%\Cursor\User\settings.json` 当前配置：

```json
{
    "aicontext.personalContext": "",
    "[vue]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[css]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "explorer.confirmDelete": false,
    "[html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "workbench.statusBar.visible": false
}
```

---

## 七、推荐安装的扩展

| 扩展 ID | 用途 |
|---|---|
| `esbenp.prettier-vscode` | Vue/CSS/HTML 代码格式化 |
| `Vue.volar` | Vue 3 语言支持 |
| `ms-vscode.cpptools` | C++ 语言支持 |

安装命令：
```bash
cursor --install-extension esbenp.prettier-vscode
cursor --install-extension Vue.volar
cursor --install-extension ms-vscode.cpptools
```

---

## 八、项目级配置（无需迁移，已在 Git 仓库中）

以下配置存储在项目仓库中，Clone 后自动生效：

| 文件 | 说明 |
|---|---|
| `.cursorrules` | 项目专属规则（Vue/UI 详细规范） |
| `.cursor/rules/*.mdc` | 项目规则文件（如有） |
| `.cursor/skills/` | 项目专属 Skills（源文件） |

---

## 九、迁移检查清单

换电脑后按顺序完成：

- [ ] 安装 Cursor 并登录账号
- [ ] 设置 User Rules（第三步）
- [ ] 设置 Rules for AI（第二步，方式 A 或 B）
- [ ] 复制 Skills 到全局目录（第四步）
- [ ] 安装并配置 MCP 工具（第五步）
- [ ] 安装推荐扩展（第七步）
- [ ] Clone 项目代码（`.cursorrules` 自动生效）
- [ ] 重启 Cursor

---

> 文档生成时间：2026-03-05
> 配置版本：基于当前 `C:\Users\localuser\.cursor\` 目录



---

## 十、Skill 完整内容（用于新电脑还原）

在新电脑上将以下内容分别保存为对应路径的 SKILL.md 文件即可还原 Skills。

---

### Skill：industrial-ui-pro

保存路径：`C:\Users\<用户名>\.cursor\skills-cursor\industrial-ui-pro\SKILL.md`

# Industrial UI Pro - CAD 嵌入式 UI 设计规范

**适用场景**: CAD Dialog、PaletteSet、WebView2 嵌入面板  
**配合使用**: `vue-prototype-builder` Skill 提供代码模板

---

## CSS 变量（设计令牌）

```css
:root {
  /* Backgrounds */
  --cad-bg-primary: #f5f7fa;
  --cad-bg-secondary: #ffffff;
  --cad-bg-header: #e1e1e1;
  --cad-bg-footer: #f5f5f5;
  --cad-bg-hover: #d9ecff;     /* ⭐ 悬停高亮 - 强制使用 */
  --cad-bg-active: #cce8ff;    /* ⭐ 激活/选中 - 强制使用 */

  /* Text */
  --cad-text-primary: #303133;
  --cad-text-secondary: #606266;

  /* Borders */
  --cad-border: #d4d4d4;
  --cad-border-hover: #409eff;  /* ⭐ 悬停边框 - 强制使用 */

  /* Spacing */
  --cad-spacing-xs: 4px;
  --cad-spacing-sm: 8px;
  --cad-spacing-md: 12px;

  /* Font */
  --cad-font-base: 12px;
  --cad-font-sm: 10px;
  --cad-font-md: 13px;
  --cad-font-mono: 'Consolas', monospace;

  /* Heights */
  --cad-height-input: 24px;
  --cad-height-button: 26px;
}
```

---

## 必须实现的悬停 CSS

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
.el-table__header th:hover { background-color: #d0d0d0; }

/* 按钮 */
.el-button { transition: all 0.2s; }
.el-button:hover { background-color: #d9ecff; border-color: #409eff; color: #409eff; }

/* 树节点 */
.el-tree-node__content { transition: background-color 0.15s; }
.el-tree-node__content:hover { background-color: #d9ecff !important; }
```

---

## 紧凑样式覆盖

```css
/* 表格紧凑 */
.el-table { font-size: 12px; width: 100%; }
.el-table .cell { padding: 0 4px; line-height: 20px; }
.el-table__cell { padding: 2px 0; }

/* 表单紧凑 */
.el-form-item { margin-bottom: 8px; }
.el-form-item__label { font-size: 12px; line-height: 24px; padding: 0 8px 0 0; }
.el-input__inner { height: 24px; line-height: 24px; font-size: 12px; }
.el-input-number { width: 100%; }

/* 树紧凑 */
.el-tree-node__content { height: 24px; }
.el-tree { font-size: 12px; }
```

---

## 容器尺寸规格

| 容器类型 | 默认宽度 | 典型用途 |
|---------|---------|---------|
| 小型 Dialog | 400px | 快速设置、简单表单 |
| 中型 Dialog | 600px | 属性编辑、图块插入 |
| 大型 Dialog | 800px | 表格编辑、数据管理 |
| PaletteSet 面板 | 250-400px | 图块库、图层管理 |

响应式断点：
- `< 450px`：单列，侧边栏折叠
- `450-600px`：单列 + 可折叠侧边栏
- `600-800px`：双列，侧边栏可见
- `> 800px`：多列，全功能展示

---

## 布局模式

### SplitPanel（分栏 + 可折叠侧边栏）

```css
.split-container { display: flex; height: 100%; overflow: hidden; }
.sidebar { display: flex; flex-direction: column; border-right: 1px solid var(--cad-border); background: #f9fafc; transition: width 0.2s; }
.sidebar-header { padding: 6px 8px; background: var(--cad-bg-header); font-weight: bold; border-bottom: 1px solid var(--cad-border); font-size: 12px; }
.splitter-handle { width: 8px; background: #f0f0f0; border-right: 1px solid var(--cad-border); cursor: pointer; display: flex; align-items: center; justify-content: center; }
.splitter-handle:hover { background: #e0e0e0; }
.main-content { flex: 1; overflow: hidden; display: flex; flex-direction: column; background: #fff; }
.content-header { padding: 6px 8px; border-bottom: 1px solid var(--cad-border); background: var(--cad-bg-footer); }
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

## 禁止使用

```css
/* ❌ 装饰性渐变 */
background: linear-gradient(135deg, #667eea, #764ba2);

/* ❌ 玻璃态 */
backdrop-filter: blur(10px);

/* ❌ 过大留白 */
padding: 32px;

/* ❌ 过度动画 */
transition: all 0.5s;

/* ❌ 悬停效果太微弱 */
.element:hover { opacity: 0.95; } /* 用户感知不到变化 */
```

---

## WebView2 通信模式

```typescript
// 前端发送消息给 C++
const postMsg = (msg: object) => {
  window.chrome?.webview?.postMessage(JSON.stringify(msg))
}

// 监听 C++ 发来的消息
window.chrome?.webview?.addEventListener('message', (e: any) => {
  const data = JSON.parse(e.data)
  // handle data
})

// 标准消息格式
postMsg({ type: 'command', action: 'insertBlock', data: { name: 'BOLT', path: 'C:\\blocks\\bolt.dwg' } })
postMsg({ type: 'scanDwgFolder', data: { folderPath: 'C:\\drawings' } })
```


---

### Skill：vue-prototype-builder

保存路径：`C:\Users\<用户名>\.cursor\skills-cursor\vue-prototype-builder\SKILL.md`

# Vue CAD UI Builder - 代码模板库

**适用场景**: CAD Dialog、PaletteSet、WebView2 嵌入面板的 Vue 3 + Element Plus 开发  
**配合使用**: `industrial-ui-pro` Skill 提供 CSS 变量和设计规范

---

## 模板 1：SplitPanel 分栏布局

```vue
<template>
  <div class="cad-split-panel">
    <div v-show="sidebarOpen" class="sidebar" :style="{ width: sidebarWidth + 'px' }">
      <div class="sidebar-header">
        <el-input v-model="search" size="small" placeholder="Search..." clearable />
      </div>
      <div class="sidebar-body">
        <el-scrollbar>
          <el-tree :data="treeData" highlight-current node-key="id" :props="{ label: 'name' }"
            @node-click="onNodeClick" class="compact-tree" />
        </el-scrollbar>
      </div>
    </div>
    <div class="splitter" @click="sidebarOpen = !sidebarOpen">
      <el-icon><component :is="sidebarOpen ? 'ArrowLeft' : 'ArrowRight'" /></el-icon>
    </div>
    <div class="main-content">
      <div class="content-header">
        <el-button-group size="small">
          <el-button :icon="Plus" @click="handleAdd">Add</el-button>
          <el-button :icon="Delete" :disabled="!selected" @click="handleDelete">Delete</el-button>
          <el-button :icon="Refresh" @click="handleRefresh">Refresh</el-button>
        </el-button-group>
      </div>
      <div class="content-body">
        <el-table :data="tableData" size="small" border highlight-current-row height="100%"
          @row-click="row => selected = row" @row-dblclick="handleEdit">
          <el-table-column prop="name" label="Name" />
          <el-table-column prop="value" label="Value" width="120" />
          <el-table-column label="Op" width="80" fixed="right">
            <template #default="{ row }">
              <el-button link size="small" @click.stop="handleEdit(row)">Edit</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Plus, Delete, Refresh } from '@element-plus/icons-vue'

const sidebarOpen = ref(true)
const sidebarWidth = ref(180)
const search = ref('')
const selected = ref<any>(null)
const treeData = ref<any[]>([])
const tableData = ref<any[]>([])

const onNodeClick = (node: any) => { console.log('[SplitPanel] Node selected:', node) }
const handleAdd = () => { console.log('[SplitPanel] Add') }
const handleDelete = () => { console.log('[SplitPanel] Delete:', selected.value) }
const handleRefresh = () => { console.log('[SplitPanel] Refresh') }
const handleEdit = (row: any) => { console.log('[SplitPanel] Edit:', row) }
</script>

<style scoped>
.cad-split-panel { display: flex; height: 100%; font-size: 12px; overflow: hidden; }
.sidebar { display: flex; flex-direction: column; border-right: 1px solid #d4d4d4; background: #f9fafc; min-width: 120px; }
.sidebar-header { padding: 6px 8px; border-bottom: 1px solid #d4d4d4; }
.sidebar-body { flex: 1; overflow: hidden; }
.splitter { width: 8px; background: #f0f0f0; border-right: 1px solid #d4d4d4; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.splitter:hover { background: #e0e0e0; }
.main-content { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.content-header { padding: 6px 8px; border-bottom: 1px solid #d4d4d4; background: #f5f5f5; flex-shrink: 0; }
.content-body { flex: 1; overflow: hidden; }
:deep(.compact-tree .el-tree-node__content) { height: 24px; }
:deep(.compact-tree .el-tree-node__content:hover) { background-color: #d9ecff; }
:deep(.el-table__body tr:hover > td) { background-color: #d9ecff !important; }
</style>
```

---

## 模板 2：属性编辑器（折叠分组）

```vue
<template>
  <div class="property-editor">
    <div class="editor-header">
      <el-tag size="small" type="info">{{ entityType }}</el-tag>
      <span style="margin-left:8px;color:#606266;font-size:11px;">{{ selectedCount }} selected</span>
      <el-button link size="small" @click="refresh" style="margin-left:auto;">Refresh</el-button>
    </div>
    <el-scrollbar class="editor-body">
      <el-collapse v-model="openSections">
        <el-collapse-item name="basic" title="Basic">
          <el-form :model="props" label-width="80px" size="small">
            <el-form-item label="Layer">
              <el-select v-model="props.layer" @change="onChange">
                <el-option label="0" value="0" />
                <el-option label="Walls" value="Walls" />
              </el-select>
            </el-form-item>
            <el-form-item label="Color">
              <el-select v-model="props.color" @change="onChange">
                <el-option label="ByLayer" value="ByLayer" />
                <el-option label="Red" value="Red" />
              </el-select>
            </el-form-item>
          </el-form>
        </el-collapse-item>
        <el-collapse-item name="geometry" title="Geometry">
          <el-form :model="props" label-width="80px" size="small">
            <el-form-item label="X">
              <el-input-number v-model="props.x" :precision="3" controls-position="right" @change="onChange" />
            </el-form-item>
            <el-form-item label="Y">
              <el-input-number v-model="props.y" :precision="3" controls-position="right" @change="onChange" />
            </el-form-item>
          </el-form>
        </el-collapse-item>
      </el-collapse>
    </el-scrollbar>
    <div class="editor-footer">
      <el-button size="small" type="primary" @click="applyChanges">Apply</el-button>
      <el-button size="small" @click="resetChanges">Reset</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const entityType = ref('Line')
const selectedCount = ref(1)
const openSections = ref(['basic'])
const props = reactive({ layer: '0', color: 'ByLayer', x: 0, y: 0 })

const onChange = () => { console.log('[PropertyEditor] Changed:', props) }
const refresh = () => { console.log('[PropertyEditor] Refresh from CAD') }
const applyChanges = () => { console.log('[PropertyEditor] Apply:', props) }
const resetChanges = () => { Object.assign(props, { layer: '0', color: 'ByLayer', x: 0, y: 0 }) }
</script>

<style scoped>
.property-editor { display: flex; flex-direction: column; height: 100%; font-size: 12px; }
.editor-header { padding: 6px 10px; background: #e1e1e1; border-bottom: 1px solid #d4d4d4; display: flex; align-items: center; flex-shrink: 0; }
.editor-body { flex: 1; }
.editor-footer { padding: 6px 10px; background: #f5f5f5; border-top: 1px solid #d4d4d4; display: flex; gap: 8px; flex-shrink: 0; }
:deep(.el-collapse-item__header) { font-size: 12px; height: 28px; padding-left: 8px; background: #f5f7fa; }
:deep(.el-collapse-item__content) { padding: 8px 8px 4px; }
:deep(.el-form-item) { margin-bottom: 8px; }
:deep(.el-form-item__label) { font-size: 12px; line-height: 24px; }
:deep(.el-input__wrapper:hover) { border-color: #409eff !important; background-color: #f5f9ff; }
:deep(.el-select .el-input__wrapper:hover) { border-color: #409eff !important; background-color: #f5f9ff; }
</style>
```

---

## 模板 3：图块库（网格 + 预览图）

```vue
<template>
  <div class="block-library">
    <div class="lib-toolbar">
      <el-input v-model="search" size="small" placeholder="Search blocks..." clearable style="flex:1;" />
      <el-button-group size="small" style="margin-left:8px;">
        <el-button :icon="Grid" :type="viewMode === 'grid' ? 'primary' : ''" @click="viewMode = 'grid'" />
        <el-button :icon="List" :type="viewMode === 'list' ? 'primary' : ''" @click="viewMode = 'list'" />
      </el-button-group>
    </div>
    <!-- Grid View -->
    <el-scrollbar class="lib-content" v-if="viewMode === 'grid'">
      <div class="block-grid">
        <div v-for="block in filteredBlocks" :key="block.name"
          class="block-card" :class="{ selected: selectedBlock?.name === block.name }"
          @click="selectedBlock = block"
          @dblclick="insertBlock(block)"
          draggable="true" @dragstart="onDragStart($event, block)">
          <div class="block-thumb">
            <img v-if="block.thumbnail" :src="block.thumbnail" />
            <el-icon v-else :size="28"><Box /></el-icon>
          </div>
          <span class="block-name">{{ block.name }}</span>
        </div>
      </div>
    </el-scrollbar>
    <!-- List View -->
    <el-table v-else :data="filteredBlocks" size="small" highlight-current-row height="100%"
      @row-click="row => selectedBlock = row" @row-dblclick="insertBlock">
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="path" label="Path" show-overflow-tooltip />
    </el-table>
    <div class="lib-footer">
      <el-button size="small" type="primary" :disabled="!selectedBlock" @click="selectedBlock && insertBlock(selectedBlock)">Insert</el-button>
      <span style="margin-left:auto;color:#909399;font-size:11px;">{{ filteredBlocks.length }} blocks</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Grid, List, Box } from '@element-plus/icons-vue'

interface Block { name: string; path: string; thumbnail?: string }

const search = ref('')
const viewMode = ref<'grid' | 'list'>('grid')
const selectedBlock = ref<Block | null>(null)
const blocks = ref<Block[]>([])

const filteredBlocks = computed(() =>
  search.value ? blocks.value.filter(b => b.name.toLowerCase().includes(search.value.toLowerCase())) : blocks.value
)

const insertBlock = (block: Block) => {
  console.log('[BlockLibrary] Insert:', block.name)
  window.chrome?.webview?.postMessage(JSON.stringify({ type: 'command', action: 'insertBlock', data: { name: block.name, path: block.path } }))
}

const onDragStart = (e: DragEvent, block: Block) => {
  e.dataTransfer?.setData('text/plain', JSON.stringify(block))
  // Immediately trigger insert on drag (for drag-to-canvas pattern)
  insertBlock(block)
}
</script>

<style scoped>
.block-library { display: flex; flex-direction: column; height: 100%; font-size: 12px; }
.lib-toolbar { padding: 6px 8px; border-bottom: 1px solid #d4d4d4; background: #f5f5f5; display: flex; align-items: center; flex-shrink: 0; }
.lib-content { flex: 1; }
.lib-footer { padding: 6px 10px; border-top: 1px solid #d4d4d4; background: #f5f5f5; display: flex; align-items: center; flex-shrink: 0; }
.block-grid { display: flex; flex-wrap: wrap; gap: 6px; padding: 8px; }
.block-card { width: 72px; display: flex; flex-direction: column; align-items: center; padding: 6px; border: 1px solid #e4e7ed; border-radius: 4px; cursor: pointer; transition: all 0.15s; }
.block-card:hover { background: #d9ecff; border-color: #409eff; }
.block-card.selected { background: #cce8ff; border-color: #409eff; }
.block-thumb { width: 52px; height: 52px; display: flex; align-items: center; justify-content: center; background: #f5f7fa; border-radius: 2px; overflow: hidden; }
.block-thumb img { max-width: 100%; max-height: 100%; object-fit: contain; }
.block-name { font-size: 10px; text-align: center; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%; color: #303133; }
:deep(.el-table__body tr:hover > td) { background-color: #d9ecff !important; }
</style>
```

---

## 模板 4：数据表格（与 CAD 双向同步）

```vue
<template>
  <div class="sync-table-panel">
    <div class="table-toolbar">
      <el-button size="small" :icon="Refresh" @click="syncFromCAD">Sync from CAD</el-button>
      <el-button size="small" :icon="Upload" :disabled="modifiedCount === 0" @click="syncToCAD">
        Apply ({{ modifiedCount }})
      </el-button>
      <el-switch v-model="autoSync" active-text="Auto" size="small" style="margin-left:auto;" />
    </div>
    <el-table :data="rows" size="small" border highlight-current-row height="100%"
      @row-click="onRowClick" @row-dblclick="onRowDblClick" class="data-table">
      <el-table-column type="index" width="36" />
      <el-table-column prop="handle" label="Handle" width="80">
        <template #default="{ row }">
          <span style="font-family:monospace;font-size:11px;">{{ row.handle }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="Type" width="80">
        <template #default="{ row }">
          <el-tag size="small" :type="typeColor(row.type)">{{ row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="layer" label="Layer">
        <template #default="{ row }">
          <el-select v-model="row.layer" size="small" @change="markDirty(row)">
            <el-option label="0" value="0" /><el-option label="Walls" value="Walls" />
          </el-select>
        </template>
      </el-table-column>
      <el-table-column label="Status" width="80">
        <template #default="{ row }">
          <el-tag size="small" :type="row.dirty ? 'warning' : 'success'">
            {{ row.dirty ? 'Modified' : 'Synced' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-footer">Total: {{ rows.length }} | Modified: {{ modifiedCount }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Refresh, Upload } from '@element-plus/icons-vue'

interface Row { handle: string; type: string; layer: string; dirty: boolean }

const autoSync = ref(false)
const rows = ref<Row[]>([])
const modifiedCount = computed(() => rows.value.filter(r => r.dirty).length)

const postMsg = (msg: object) => window.chrome?.webview?.postMessage(JSON.stringify(msg))

const syncFromCAD = () => postMsg({ type: 'getEntityList' })
const syncToCAD = () => {
  const dirty = rows.value.filter(r => r.dirty)
  postMsg({ type: 'command', action: 'updateEntities', data: dirty })
  dirty.forEach(r => r.dirty = false)
}
const markDirty = (row: Row) => {
  row.dirty = true
  if (autoSync.value) setTimeout(() => syncToCAD(), 300)
}
const onRowClick = (row: Row) => postMsg({ type: 'command', action: 'highlightEntity', data: { handle: row.handle } })
const onRowDblClick = (row: Row) => postMsg({ type: 'command', action: 'zoomToEntity', data: { handle: row.handle } })
const typeColor = (t: string) => ({ Line: 'info', Circle: 'success', Arc: 'warning' }[t] || '')
</script>

<style scoped>
.sync-table-panel { display: flex; flex-direction: column; height: 100%; font-size: 12px; }
.table-toolbar { padding: 6px 8px; border-bottom: 1px solid #d4d4d4; background: #f5f7fa; display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.data-table { flex: 1; }
.table-footer { padding: 4px 12px; border-top: 1px solid #d4d4d4; background: #f5f5f5; font-size: 11px; color: #909399; flex-shrink: 0; }
:deep(.data-table .el-table__body tr:hover > td) { background-color: #d9ecff !important; cursor: pointer; }
:deep(.data-table .el-table__header th) { background: #e1e1e1; font-size: 12px; }
</style>
```

---

## 模板 5：标准面板（Header + Tabs + Footer）

```vue
<template>
  <div class="cad-panel">
    <div class="panel-header">
      <span class="panel-title">Panel Title</span>
      <el-button link :icon="Close" size="small" @click="$emit('close')" />
    </div>
    <el-tabs v-model="activeTab" class="panel-tabs" type="border-card">
      <el-tab-pane label="Tab 1" name="tab1">
        <el-scrollbar><div class="tab-content"><!-- Tab 1 Content --></div></el-scrollbar>
      </el-tab-pane>
      <el-tab-pane label="Tab 2" name="tab2">
        <el-scrollbar><div class="tab-content"><!-- Tab 2 Content --></div></el-scrollbar>
      </el-tab-pane>
    </el-tabs>
    <div class="panel-footer">
      <el-button size="small" type="primary" @click="onConfirm">OK</el-button>
      <el-button size="small" @click="onCancel">Cancel</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Close } from '@element-plus/icons-vue'

const emit = defineEmits<{ close: [] }>()
const activeTab = ref('tab1')
const onConfirm = () => { console.log('[Panel] Confirm'); emit('close') }
const onCancel = () => emit('close')
</script>

<style scoped>
.cad-panel { display: flex; flex-direction: column; width: 100%; height: 100%; font-size: 12px; }
.panel-header { padding: 6px 10px; background: #e1e1e1; border-bottom: 1px solid #d4d4d4; display: flex; align-items: center; flex-shrink: 0; }
.panel-title { font-size: 13px; font-weight: 600; flex: 1; }
.panel-tabs { flex: 1; overflow: hidden; }
.tab-content { padding: 8px; }
.panel-footer { padding: 6px 10px; background: #f5f5f5; border-top: 1px solid #d4d4d4; display: flex; gap: 8px; justify-content: flex-end; flex-shrink: 0; }
</style>
```

---

## WebView2 消息通信

```typescript
// 发送消息
const postMsg = (msg: object) =>
  window.chrome?.webview?.postMessage(JSON.stringify(msg))

// 监听消息
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
postMsg({ type: 'command', action: 'scanDwgFolder', data: { folderPath: 'C:\\drawings' } })
postMsg({ type: 'getEntityList' })
postMsg({ type: 'command', action: 'highlightEntity', data: { handle: '1A3F' } })
```
