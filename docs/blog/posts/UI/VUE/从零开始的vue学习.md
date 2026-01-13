---
title: 从零开始的 Vue3 学习指南
date: 2026-01-13
categories:
  - 前端开发
  - Web框架
  - 教程文档
tags:
  - Vue3
  - JavaScript
  - TypeScript
  - 前端框架
  - 组件化开发
  - Composition API
  - Vue Router
  - Pinia
  - Element Plus
  - WebView2
description: 完整的 Vue3 学习指南，从基础到高级，包含项目实战、PWA开发、单文件HTML打包、美化技巧等，适合零基础和进阶开发者
author: AI Assistant
keywords:
  - Vue3教程
  - 前端开发
  - SPA应用
  - 响应式编程
  - 状态管理
  - 路由管理
  - UI组件库
  - 代码高亮
  - 离线HTML
cover: https://cn.vuejs.org/images/logo.png
---

# 从零开始的 Vue3 学习指南

## 目录

- [一、Vue3 简介](#一vue3-简介)
- [二、环境准备与安装](#二环境准备与安装)
- [三、Vue3 基础知识](#三vue3-基础知识)
- [四、Vue3 高级特性](#四vue3-高级特性)
- [五、Vue Router 路由](#五vue-router-路由)
- [六、状态管理 Pinia](#六状态管理-pinia)
- [七、UI 组件库](#七ui-组件库)
- [八、项目实战](#八项目实战)
- [九、Vue 应用美化与增强](#九vue-应用美化与增强)
- [十、常见问题与解决方案](#十常见问题与解决方案)
- [十一、将文档转换为离线 HTML](#十一将文档转换为离线-html)
- [十二、学习资源](#十二学习资源)

---

## 一、Vue3 简介

### 1.1 什么是 Vue？

Vue (读音 /vjuː/，类似于 view) 是一套用于构建用户界面的渐进式框架。与其它大型框架不同的是，Vue 被设计为可以自底向上逐层应用。Vue 的核心库只关注视图层，不仅易于上手，还便于与第三方库或既有项目整合。

### 1.2 Vue3 的特点

- **性能提升**：重写了虚拟 DOM 的实现，性能提升 1.3-2 倍
- **更好的 TypeScript 支持**：Vue3 本身使用 TypeScript 编写
- **Composition API**：更灵活的代码组织和逻辑复用
- **更小的打包体积**：通过 Tree-shaking 减少打包体积
- **更好的响应式系统**：使用 Proxy 替代 Object.defineProperty

---

## 二、环境准备与安装

### 2.1 前提条件

- 熟悉命令行操作
- 已安装 **Node.js 20.19.0** 或更高版本

检查 Node.js 版本：

```bash
node -v
npm -v
```

### 2.2 在线体验 Vue

在开始正式开发之前，你可以先在线体验 Vue：

- **Vue 演练场**：https://play.vuejs.org/
- **JSFiddle**：适合不用构建工具的原始 HTML
- **StackBlitz**：完整的构建设置体验
- **Scrimba 互动教程**：学习如何运行、编辑和部署 Vue 应用

### 2.3 创建 Vue3 项目

#### 方法一：使用 create-vue（推荐）

```bash
# 创建项目
npm create vue@latest

# 进入项目目录
cd <your-project-name>

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

创建项目时会有以下选项：

```
✔ Project name: … <your-project-name>
✔ Add TypeScript? … No / Yes
✔ Add JSX Support? … No / Yes
✔ Add Vue Router for Single Page Application development? … No / Yes
✔ Add Pinia for state management? … No / Yes
✔ Add Vitest for Unit Testing? … No / Yes
✔ Add an End-to-End Testing Solution? … No / Cypress / Nightwatch / Playwright
✔ Add ESLint for code quality? … No / Yes
✔ Add Prettier for code formatting? … No / Yes
✔ Add Vue DevTools 7 extension for debugging? (experimental) … No / Yes
```

**提示**：如果不确定是否开启某个功能，直接按回车选择 No 即可。

#### 方法二：使用 Vite

```bash
# 创建项目
npm init vite-app <project-name>

# 进入项目
cd <project-name>

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 2.4 通过 CDN 使用 Vue

如果你想快速体验或增强静态 HTML，可以通过 CDN 使用 Vue：

#### 使用全局构建版本

```html
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>

<div id="app">{{ message }}</div>

<script>
  const { createApp, ref } = Vue
  
  createApp({
    setup() {
      const message = ref('Hello Vue!')
      return {
        message
      }
    }
  }).mount('#app')
</script>
```

#### 使用 ES 模块构建版本

```html
<div id="app">{{ message }}</div>

<script type="module">
  import { createApp, ref } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

  createApp({
    setup() {
      const message = ref('Hello Vue!')
      return {
        message
      }
    }
  }).mount('#app')
</script>
```

#### 使用 Import Maps

```html
<script type="importmap">
  {
    "imports": {
      "vue": "https://unpkg.com/vue@3/dist/vue.esm-browser.js"
    }
  }
</script>

<div id="app">{{ message }}</div>

<script type="module">
  import { createApp, ref } from 'vue'

  createApp({
    setup() {
      const message = ref('Hello Vue!')
      return {
        message
      }
    }
  }).mount('#app')
</script>
```

### 2.5 推荐的 IDE 配置

- **Visual Studio Code** + **Vue - Official 扩展**（推荐）
- 其他编辑器请参考官方 IDE 支持文档

---

## 三、Vue3 基础知识

### 3.1 模板语法

#### 3.1.1 文本插值

使用双大括号语法（Mustache 语法）进行文本插值：

```vue
<template>
  <div id="root">
    <span>Message: {{ msg }}</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const msg = ref('Welcome to Your Vue.js App')
</script>
```

#### 3.1.2 原始 HTML

使用 `v-html` 指令插入 HTML：

```vue
<template>
  <p>Using v-html directive: <span v-html="rawHtml"></span></p>
</template>

<script setup>
import { ref } from 'vue'
const rawHtml = ref('<a href="https://www.baidu.com">百度一下</a>')
</script>
```

⚠️ **安全警告**：动态渲染任意 HTML 非常危险，容易造成 XSS 漏洞。请仅在内容安全可信时使用。

#### 3.1.3 Attribute 绑定

##### 动态绑定单个属性

```vue
<template>
  <!-- 完整写法 -->
  <div v-bind:id="dynamicId"></div>
  
  <!-- 简写 -->
  <div :id="dynamicId"></div>
</template>

<script setup>
import { ref } from 'vue'
const dynamicId = ref('my-id')
</script>
```

##### 动态绑定多个属性

```vue
<template>
  <div v-bind="objectOfAttrs"></div>
</template>

<script setup>
import { reactive } from 'vue'
const objectOfAttrs = reactive({
  id: 'container',
  class: 'wrapper'
})
</script>
```

#### 3.1.4 使用 JavaScript 表达式

在模板中可以使用 JavaScript 表达式：

```vue
<template>
  <div :id="`list-${id}`">
    <p>{{ number + 1 }}</p>
    <p>{{ ok ? 'YES' : 'NO' }}</p>
    <p>{{ message.split('').reverse().join('') }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const id = ref(1)
const number = ref(5)
const ok = ref(true)
const message = ref('Hello')
</script>
```

#### 3.1.5 指令（Directives）

指令是带有 `v-` 前缀的特殊 attribute。

##### 常用指令

- `v-if`：条件渲染
- `v-for`：列表渲染
- `v-on`（简写 `@`）：事件监听
- `v-bind`（简写 `:`）：属性绑定
- `v-model`：双向数据绑定

```vue
<template>
  <!-- v-if 条件渲染 -->
  <p v-if="seen">Now you see me</p>
  
  <!-- v-bind 属性绑定 -->
  <a v-bind:href="url">链接</a>
  <a :href="url">链接（简写）</a>
  
  <!-- v-on 事件监听 -->
  <button v-on:click="doSomething">点击</button>
  <button @click="doSomething">点击（简写）</button>
</template>

<script setup>
import { ref } from 'vue'
const seen = ref(true)
const url = ref('https://www.baidu.com')
function doSomething() {
  console.log('clicked')
}
</script>
```

##### 动态参数

```vue
<template>
  <a :[attributeName]="url">动态参数</a>
  <button @[eventName]="doSomething">动态事件</button>
</template>

<script setup>
import { ref } from 'vue'
const attributeName = ref('href')
const eventName = ref('click')
const url = ref('https://www.baidu.com')
function doSomething() {
  console.log('clicked')
}
</script>
```

##### 修饰符

修饰符是以点 `.` 开头的特殊后缀：

```vue
<template>
  <!-- .prevent 修饰符告诉 v-on 指令对触发的事件调用 event.preventDefault() -->
  <form @submit.prevent="onSubmit">
    <button type="submit">提交</button>
  </form>
</template>

<script setup>
function onSubmit() {
  console.log('form submitted')
}
</script>
```

### 3.2 响应式基础

#### 3.2.1 使用 `ref()`

`ref()` 用于声明响应式状态：

```vue
<template>
  <div>{{ count }}</div>
  <button @click="increment">{{ count }}</button>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)

function increment() {
  count.value++
}
</script>
```

**注意**：
- 在 `<script setup>` 中需要使用 `.value` 访问 ref 的值
- 在模板中会自动解包，不需要 `.value`

#### 3.2.2 使用 `reactive()`

`reactive()` 用于声明响应式对象：

```vue
<template>
  <div>{{ state.count }}</div>
  <button @click="state.count++">{{ state.count }}</button>
</template>

<script setup>
import { reactive } from 'vue'

const state = reactive({
  count: 0
})
</script>
```

#### 3.2.3 `reactive()` 的局限性

1. **有限的值类型**：只能用于对象类型（对象、数组、Map、Set），不能用于原始类型
2. **不能替换整个对象**：会丢失响应性连接
3. **对解构操作不友好**：解构后会丢失响应性

```vue
<script setup>
import { reactive } from 'vue'

const state = reactive({ count: 0 })

// ❌ 解构后失去响应性
let { count } = state
count++ // 不会影响原始的 state

// ❌ 替换整个对象会失去响应性
state = reactive({ count: 1 }) // 响应性连接已丢失
</script>
```

**建议**：优先使用 `ref()` 作为声明响应式状态的主要 API。

### 3.3 事件处理

#### 3.3.1 监听事件

使用 `v-on` 指令（简写 `@`）监听 DOM 事件：

```vue
<template>
  <!-- 内联事件处理器 -->
  <button @click="count++">Add 1</button>
  <p>Count is: {{ count }}</p>
  
  <!-- 方法事件处理器 -->
  <button @click="greet">Greet</button>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)
const name = ref('Vue.js')

function greet(event) {
  alert(`Hello ${name.value}!`)
  // event 是原生 DOM 事件对象
  if (event) {
    alert(event.target.tagName)
  }
}
</script>
```

#### 3.3.2 在内联处理器中调用方法

```vue
<template>
  <button @click="say('hello')">Say hello</button>
  <button @click="say('bye')">Say bye</button>
</template>

<script setup>
function say(message) {
  alert(message)
}
</script>
```

#### 3.3.3 在内联处理器中访问事件参数

```vue
<template>
  <!-- 使用特殊的 $event 变量 -->
  <button @click="warn('Form cannot be submitted yet.', $event)">
    Submit
  </button>
  
  <!-- 使用内联箭头函数 -->
  <button @click="(event) => warn('Form cannot be submitted yet.', event)">
    Submit
  </button>
</template>

<script setup>
function warn(message, event) {
  if (event) {
    event.preventDefault()
  }
  alert(message)
}
</script>
```

#### 3.3.4 事件修饰符

```vue
<template>
  <!-- 阻止默认行为 -->
  <form @submit.prevent="onSubmit"></form>
  
  <!-- 阻止事件冒泡 -->
  <a @click.stop="doThis"></a>
  
  <!-- 修饰符可以链式调用 -->
  <a @click.stop.prevent="doThat"></a>
  
  <!-- 只有修饰符 -->
  <form @submit.prevent></form>
  
  <!-- 仅当 event.target 是元素本身时触发 -->
  <div @click.self="doThat">...</div>
  
  <!-- 事件最多触发一次 -->
  <a @click.once="doThis"></a>
  
  <!-- 使用捕获模式 -->
  <div @click.capture="doThis">...</div>
  
  <!-- 滚动事件的默认行为将立即发生 -->
  <div @scroll.passive="onScroll">...</div>
</template>
```

常用事件修饰符：
- `.stop` - 阻止事件冒泡
- `.prevent` - 阻止默认行为
- `.self` - 只在元素本身触发
- `.capture` - 使用捕获模式
- `.once` - 只触发一次
- `.passive` - 改善滚屏性能

#### 3.3.5 按键修饰符

```vue
<template>
  <!-- 仅在按下 Enter 键时调用 -->
  <input @keyup.enter="submit" />
  
  <!-- 仅在按下 PageDown 键时调用 -->
  <input @keyup.page-down="onPageDown" />
  
  <!-- Alt + Enter -->
  <input @keyup.alt.enter="clear" />
  
  <!-- Ctrl + Click -->
  <div @click.ctrl="doSomething">Do something</div>
</template>
```

常用按键别名：
- `.enter`
- `.tab`
- `.delete`（捕获"Delete"和"Backspace"）
- `.esc`
- `.space`
- `.up` / `.down` / `.left` / `.right`

系统按键修饰符：
- `.ctrl`
- `.alt`
- `.shift`
- `.meta`（Mac 上的 Command，Windows 上的 Windows 键）

鼠标按键修饰符：
- `.left`
- `.right`
- `.middle`

### 3.4 列表渲染

#### 3.4.1 使用 `v-for` 渲染数组

```vue
<template>
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.message }}
    </li>
  </ul>
</template>

<script setup>
import { ref } from 'vue'
const items = ref([
  { id: 1, message: 'Foo' },
  { id: 2, message: 'Bar' }
])
</script>
```

#### 3.4.2 使用索引

```vue
<template>
  <ul>
    <li v-for="(item, index) in items" :key="item.id">
      {{ index }} - {{ item.message }}
    </li>
  </ul>
</template>
```

#### 3.4.3 `v-for` 遍历对象

```vue
<template>
  <ul>
    <li v-for="(value, key, index) in myObject" :key="key">
      {{ index }}. {{ key }}: {{ value }}
    </li>
  </ul>
</template>

<script setup>
import { reactive } from 'vue'
const myObject = reactive({
  title: 'How to do lists in Vue',
  author: 'Jane Doe',
  publishedAt: '2016-04-10'
})
</script>
```

输出：
- 0. title: How to do lists in Vue
- 1. author: Jane Doe
- 2. publishedAt: 2016-04-10

⚠️ **注意**：在 `v-for` 中使用 `:key` 是必须的，它帮助 Vue 跟踪每个节点的身份。

### 3.5 Class 与 Style 绑定

#### 3.5.1 绑定对象到 class

```vue
<template>
  <div :class="{ active: isActive, 'text-danger': hasError }">
    动态 class
  </div>
</template>

<script setup>
import { ref } from 'vue'
const isActive = ref(true)
const hasError = ref(false)
</script>
```

#### 3.5.2 绑定数组到 class

```vue
<template>
  <div :class="[activeClass, errorClass]">数组绑定</div>
  
  <!-- 数组中使用三元表达式 -->
  <div :class="[isActive ? activeClass : '', errorClass]">条件 class</div>
  
  <!-- 数组中嵌套对象 -->
  <div :class="[{ active: isActive }, errorClass]">混合绑定</div>
</template>

<script setup>
import { ref } from 'vue'
const activeClass = ref('active')
const errorClass = ref('text-danger')
const isActive = ref(true)
</script>
```

#### 3.5.3 绑定内联样式

```vue
<template>
  <!-- 对象语法 -->
  <div :style="{ color: activeColor, fontSize: fontSize + 'px' }">
    样式绑定
  </div>
  
  <!-- 绑定样式对象 -->
  <div :style="styleObject">样式对象</div>
  
  <!-- 数组语法 -->
  <div :style="[baseStyles, overridingStyles]">多个样式对象</div>
</template>

<script setup>
import { reactive, ref } from 'vue'
const activeColor = ref('red')
const fontSize = ref(30)

const styleObject = reactive({
  color: 'red',
  fontSize: '13px'
})

const baseStyles = reactive({ color: 'blue' })
const overridingStyles = reactive({ fontSize: '20px' })
</script>
```

### 3.6 表单输入绑定

#### 3.6.1 基本用法

##### 文本输入

```vue
<template>
  <p>Message is: {{ message }}</p>
  <input type="text" v-model="message" placeholder="edit me" />
</template>

<script setup>
import { ref } from 'vue'
const message = ref('')
</script>
```

##### 多行文本

```vue
<template>
  <span>Multiline message:</span>
  <p style="white-space: pre-line;">{{ message }}</p>
  <textarea v-model="message" placeholder="add multiple lines"></textarea>
</template>

<script setup>
import { ref } from 'vue'
const message = ref('')
</script>
```

##### 复选框

```vue
<template>
  <!-- 单个复选框 -->
  <input type="checkbox" id="checkbox" v-model="checked" />
  <label for="checkbox">{{ checked }}</label>
  
  <!-- 多个复选框 -->
  <input type="checkbox" id="jack" value="Jack" v-model="checkedNames" />
  <label for="jack">Jack</label>
  
  <input type="checkbox" id="john" value="John" v-model="checkedNames" />
  <label for="john">John</label>
  
  <input type="checkbox" id="mike" value="Mike" v-model="checkedNames" />
  <label for="mike">Mike</label>
  
  <span>Checked names: {{ checkedNames }}</span>
</template>

<script setup>
import { ref } from 'vue'
const checked = ref(false)
const checkedNames = ref([])
</script>
```

##### 单选按钮

```vue
<template>
  <div>Picked: {{ picked }}</div>
  
  <input type="radio" id="one" value="One" v-model="picked" />
  <label for="one">One</label>
  
  <input type="radio" id="two" value="Two" v-model="picked" />
  <label for="two">Two</label>
</template>

<script setup>
import { ref } from 'vue'
const picked = ref('')
</script>
```

##### 选择器

```vue
<template>
  <!-- 单选 -->
  <select v-model="selected">
    <option disabled value="">Please select one</option>
    <option>A</option>
    <option>B</option>
    <option>C</option>
  </select>
  <span>Selected: {{ selected }}</span>
  
  <!-- 多选 -->
  <select v-model="multiSelected" multiple>
    <option>A</option>
    <option>B</option>
    <option>C</option>
  </select>
  <span>Selected: {{ multiSelected }}</span>
</template>

<script setup>
import { ref } from 'vue'
const selected = ref('')
const multiSelected = ref([])
</script>

<style>
select[multiple] {
  width: 100px;
}
</style>
```

#### 3.6.2 修饰符

```vue
<template>
  <!-- .lazy - 在 change 事件后同步，而不是 input -->
  <input v-model.lazy="message" />
  
  <!-- .number - 自动将输入转为数字 -->
  <input type="number" v-model.number="age" />
  
  <!-- .trim - 自动过滤首尾空白字符 -->
  <input v-model.trim="message" />
</template>

<script setup>
import { ref } from 'vue'
const message = ref('')
const age = ref(0)
</script>
```

---

## 四、Vue3 高级特性

### 4.1 计算属性

计算属性用于声明性地描述依赖响应式状态的复杂逻辑：

```vue
<template>
  <p>Has published books:</p>
  <span>{{ publishedBooksMessage }}</span>
</template>

<script setup>
import { reactive, computed } from 'vue'

const author = reactive({
  name: 'John Doe',
  books: [
    'Vue 2 - Advanced Guide',
    'Vue 3 - Basic Guide',
    'Vue 4 - The Mystery'
  ]
})

// 计算属性会自动追踪响应式依赖
const publishedBooksMessage = computed(() => {
  return author.books.length > 0 ? 'Yes' : 'No'
})
</script>
```

### 4.2 侦听器

使用 `watch` 侦听响应式数据的变化：

```vue
<script setup>
import { ref, watch } from 'vue'

const question = ref('')
const answer = ref('Questions usually contain a question mark. ;-)')

// 可以直接侦听一个 ref
watch(question, async (newQuestion, oldQuestion) => {
  if (newQuestion.includes('?')) {
    answer.value = 'Thinking...'
    // 模拟异步操作
    setTimeout(() => {
      answer.value = 'Got the answer!'
    }, 1000)
  }
})
</script>

<template>
  <p>
    Ask a yes/no question:
    <input v-model="question" />
  </p>
  <p>{{ answer }}</p>
</template>
```

### 4.3 生命周期钩子

```vue
<script setup>
import { onMounted, onUpdated, onUnmounted } from 'vue'

onMounted(() => {
  console.log('组件已挂载')
})

onUpdated(() => {
  console.log('组件已更新')
})

onUnmounted(() => {
  console.log('组件已卸载')
})
</script>
```

常用生命周期钩子：
- `onBeforeMount` - 挂载之前
- `onMounted` - 挂载完成
- `onBeforeUpdate` - 更新之前
- `onUpdated` - 更新完成
- `onBeforeUnmount` - 卸载之前
- `onUnmounted` - 卸载完成

### 4.4 组件基础

#### 4.4.1 定义组件

```vue
<!-- ButtonCounter.vue -->
<template>
  <button @click="count++">You clicked me {{ count }} times.</button>
</template>

<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
```

#### 4.4.2 使用组件

```vue
<template>
  <h1>Here is a child component!</h1>
  <ButtonCounter />
</template>

<script setup>
import ButtonCounter from './ButtonCounter.vue'
</script>
```

#### 4.4.3 Props 传递数据

```vue
<!-- BlogPost.vue -->
<template>
  <h4>{{ title }}</h4>
</template>

<script setup>
defineProps({
  title: String
})
</script>
```

使用组件：

```vue
<template>
  <BlogPost title="My journey with Vue" />
  <BlogPost title="Blogging with Vue" />
  <BlogPost title="Why Vue is so fun" />
</template>

<script setup>
import BlogPost from './BlogPost.vue'
</script>
```

#### 4.4.4 监听事件

```vue
<!-- BlogPost.vue -->
<template>
  <div class="blog-post">
    <h4>{{ title }}</h4>
    <button @click="$emit('enlarge-text')">Enlarge text</button>
  </div>
</template>

<script setup>
defineProps({
  title: String
})

defineEmits(['enlarge-text'])
</script>
```

父组件监听事件：

```vue
<template>
  <BlogPost
    v-for="post in posts"
    :key="post.id"
    :title="post.title"
    @enlarge-text="postFontSize += 0.1"
  />
</template>

<script setup>
import { ref } from 'vue'
const postFontSize = ref(1)
const posts = ref([
  { id: 1, title: 'My journey with Vue' },
  { id: 2, title: 'Blogging with Vue' }
])
</script>
```

---

## 五、Vue Router 路由

### 5.1 安装 Vue Router

```bash
npm install vue-router@4
```

### 5.2 基本使用

#### main.js 配置

```javascript
import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'

// 定义路由
const routes = [
  { path: '/home', component: () => import('./components/Home.vue') },
  { path: '/about', component: () => import('./components/About.vue') }
]

// 创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 创建并挂载应用
const app = createApp(App)
app.use(router)
app.mount('#app')
```

#### App.vue

```vue
<template>
  <div id="app">
    <router-link to="/home">Home</router-link>
    <router-link to="/about">About</router-link>
    
    <!-- 路由出口 -->
    <router-view></router-view>
  </div>
</template>
```

### 5.3 编程式导航

#### 使用 router.push

```vue
<template>
  <div>
    <button @click="goToHome">Go to Home</button>
    <button @click="goToAbout">Go to About</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goToHome() {
  router.push('/home')
}

function goToAbout() {
  router.push({
    path: '/about',
    query: { id: 123, name: 'John' }
  })
}
</script>
```

### 5.4 路由传参

#### 传递参数

```vue
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function navigateWithParams() {
  router.push({
    path: '/home',
    query: {
      name: '张三',
      id: 1
    }
  })
}
</script>
```

#### 接收参数

```vue
<template>
  <div>
    <p>Name: {{ info.name }}</p>
    <p>ID: {{ info.id }}</p>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const info = reactive({
  id: route.query.id,
  name: route.query.name
})
</script>
```

### 5.5 嵌套路由

```javascript
const routes = [
  {
    path: '/main',
    component: () => import('./components/Main.vue'),
    children: [
      {
        path: '/main/profile',
        component: () => import('./components/Profile.vue')
      },
      {
        path: '/main/settings',
        component: () => import('./components/Settings.vue')
      }
    ]
  }
]
```

父组件需要包含 `<router-view>` 来渲染子路由：

```vue
<!-- Main.vue -->
<template>
  <div>
    <h2>Main Page</h2>
    <router-link to="/main/profile">Profile</router-link>
    <router-link to="/main/settings">Settings</router-link>
    
    <!-- 子路由出口 -->
    <router-view></router-view>
  </div>
</template>
```

---

## 六、状态管理 Pinia

### 6.1 什么是 Pinia？

Pinia 是 Vue 的专属状态管理库，它允许你跨组件或页面共享状态。它是 Vuex 的替代品，提供了更简单的 API 和更好的 TypeScript 支持。

### 6.2 安装 Pinia

```bash
npm install pinia
```

### 6.3 创建 Pinia 实例

在 `main.js` 中：

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.mount('#app')
```

### 6.4 定义 Store

#### Option Store（选项式）

```javascript
// stores/counter.js
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  getters: {
    double: (state) => state.count * 2
  },
  actions: {
    increment() {
      this.count++
    }
  }
})
```

#### Setup Store（组合式）

```javascript
// stores/counter.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const double = computed(() => count.value * 2)
  
  function increment() {
    count.value++
  }
  
  return { count, double, increment }
})
```

### 6.5 使用 Store

```vue
<template>
  <div>
    <p>Count: {{ store.count }}</p>
    <p>Double: {{ store.double }}</p>
    <button @click="store.increment">Increment</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
</script>
```

### 6.6 解构 Store

使用 `storeToRefs` 保持响应性：

```vue
<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double: {{ double }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

// 解构 state 和 getters，保持响应性
const { count, double } = storeToRefs(store)

// actions 可以直接解构
const { increment } = store
</script>
```

### 6.7 State 操作

#### 访问 State

```javascript
const store = useCounterStore()
console.log(store.count)
```

#### 重置 State

```javascript
// 仅适用于 Option Store
store.$reset()

// Setup Store 需要自定义 $reset 方法
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  
  function $reset() {
    count.value = 0
  }
  
  return { count, $reset }
})
```

#### 批量修改 State

```javascript
// 使用 $patch 对象
store.$patch({
  count: store.count + 1,
  name: 'DIO'
})

// 使用 $patch 函数
store.$patch((state) => {
  state.items.push({ name: 'shoes', quantity: 1 })
  state.hasChanged = true
})
```

### 6.8 订阅 State 变化

```javascript
<script setup>
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

store.$subscribe((mutation, state) => {
  // 每当状态发生变化时执行
  console.log(mutation.type) // 'direct' | 'patch object' | 'patch function'
  console.log(mutation.storeId) // 'counter'
  
  // 持久化到本地存储
  localStorage.setItem('counter', JSON.stringify(state))
})
</script>
```

---

## 七、UI 组件库

### 7.1 流行的 Vue3 UI 组件库

1. **Element Plus** - 基于 Element UI 的 Vue3 版本
2. **Ant Design Vue** - Ant Design 的 Vue 实现
3. **Naive UI** - 比较完整的 Vue3 组件库
4. **Vuetify** - Material Design 风格的组件库
5. **Vant** - 有赞前端团队开发的移动端组件库
6. **Quasar** - 支持桌面和移动端的全能框架
7. **Arco Design Vue** - 字节跳动的设计系统

### 7.2 Element Plus 快速上手

#### 安装

```bash
npm install element-plus --save
```

#### 完整引入

```javascript
// main.js
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
```

#### 使用组件

```vue
<template>
  <el-button type="primary">Primary Button</el-button>
  <el-button type="success">Success Button</el-button>
  <el-button type="info">Info Button</el-button>
  <el-button type="warning">Warning Button</el-button>
  <el-button type="danger">Danger Button</el-button>
</template>
```

#### 安装图标

```bash
npm install @element-plus/icons-vue
```

注册所有图标：

```javascript
// main.js
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
```

使用图标：

```vue
<template>
  <el-button :icon="Search" circle />
  <el-button type="primary" :icon="Edit" circle />
  <el-button type="success" :icon="Check" circle />
</template>

<script setup>
import { Search, Edit, Check } from '@element-plus/icons-vue'
</script>
```

### 7.3 Element Plus 常用组件示例

#### 布局

```vue
<template>
  <el-container>
    <el-aside width="200px">侧边栏</el-aside>
    <el-container>
      <el-header>头部</el-header>
      <el-main>主要内容</el-main>
    </el-container>
  </el-container>
</template>

<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
}
</style>
```

#### 表单

```vue
<template>
  <el-form :model="form" label-width="120px">
    <el-form-item label="用户名">
      <el-input v-model="form.name" />
    </el-form-item>
    
    <el-form-item label="密码">
      <el-input v-model="form.password" type="password" />
    </el-form-item>
    
    <el-form-item label="性别">
      <el-select v-model="form.gender" placeholder="请选择">
        <el-option label="男" value="male" />
        <el-option label="女" value="female" />
      </el-select>
    </el-form-item>
    
    <el-form-item>
      <el-button type="primary" @click="onSubmit">提交</el-button>
      <el-button @click="onReset">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  name: '',
  password: '',
  gender: ''
})

function onSubmit() {
  console.log('submit!', form)
}

function onReset() {
  form.name = ''
  form.password = ''
  form.gender = ''
}
</script>
```

#### 表格

```vue
<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="date" label="日期" width="180" />
    <el-table-column prop="name" label="姓名" width="180" />
    <el-table-column prop="address" label="地址" />
  </el-table>
</template>

<script setup>
import { ref } from 'vue'

const tableData = ref([
  {
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles'
  },
  {
    date: '2016-05-02',
    name: 'John',
    address: 'No. 189, Grove St, Los Angeles'
  }
])
</script>
```

#### 对话框

```vue
<template>
  <el-button type="primary" @click="dialogVisible = true">
    打开对话框
  </el-button>
  
  <el-dialog v-model="dialogVisible" title="提示" width="30%">
    <span>这是一段信息</span>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="dialogVisible = false">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
const dialogVisible = ref(false)
</script>
```

---

## 八、项目实战

### 8.1 项目结构

一个标准的 Vue3 项目结构：

```
my-vue-app/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/          # 静态资源
│   ├── components/      # 公共组件
│   ├── views/           # 页面组件
│   ├── router/          # 路由配置
│   ├── stores/          # Pinia 状态管理
│   ├── utils/           # 工具函数
│   ├── api/             # API 接口
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── .gitignore
├── index.html
├── package.json
├── vite.config.js       # Vite 配置
└── README.md
```

### 8.2 环境配置

#### vite.config.js

```javascript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: 'localhost',
    port: 8000
  }
})
```

#### 环境变量配置

创建 `src/config/index.js`：

```javascript
const env = import.meta.env.MODE || 'prod'

const EnvConfig = {
  dev: {
    baseApi: '/',
    mockApi: 'https://your-mock-api.com'
  },
  test: {
    baseApi: '/',
    mockApi: 'https://your-mock-api.com'
  },
  prod: {
    baseApi: '/',
    mockApi: 'https://your-mock-api.com'
  }
}

export default {
  env,
  mock: true,
  ...EnvConfig[env]
}
```

### 8.3 Axios 封装

创建 `src/utils/request.js`：

```javascript
import axios from 'axios'
import config from '../config'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const service = axios.create({
  baseURL: config.baseApi,
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(
  (req) => {
    const header = req.headers
    if (header.Authorization) {
      header.Authorization = `Bearer ${header.Authorization}`
    }
    return req
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (res) => {
    const { code, data, msg } = res.data
    
    if (code === 200) {
      return data
    } else if (code === 401) {
      ElMessage.error(msg || '未授权，请重新登录')
      return Promise.reject(msg)
    } else {
      ElMessage.error(msg || '请求失败')
      return Promise.reject(msg)
    }
  },
  (error) => {
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

// 请求核心函数
function request(options) {
  options.method = options.method || 'get'
  
  if (options.method.toLowerCase() === 'get') {
    options.params = options.data
  }
  
  if (config.env === 'prod') {
    service.defaults.baseURL = config.baseApi
  } else {
    service.defaults.baseURL = config.mock ? config.mockApi : config.baseApi
  }
  
  return service(options)
}

// 添加快捷方法
['get', 'post', 'put', 'delete', 'patch'].forEach((method) => {
  request[method] = (url, data, options) => {
    return request({
      method,
      url,
      data,
      ...options
    })
  }
})

export default request
```

使用示例：

```javascript
import request from '@/utils/request'

// GET 请求
request.get('/api/users').then(res => {
  console.log(res)
})

// POST 请求
request.post('/api/users', {
  name: 'John',
  age: 30
}).then(res => {
  console.log(res)
})
```

### 8.4 完整示例：Todo 应用

#### 创建 Store

```javascript
// stores/todo.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTodoStore = defineStore('todo', () => {
  const todos = ref([])
  const filter = ref('all')
  
  const filteredTodos = computed(() => {
    if (filter.value === 'active') {
      return todos.value.filter(todo => !todo.completed)
    } else if (filter.value === 'completed') {
      return todos.value.filter(todo => todo.completed)
    }
    return todos.value
  })
  
  const addTodo = (text) => {
    todos.value.push({
      id: Date.now(),
      text,
      completed: false
    })
  }
  
  const removeTodo = (id) => {
    const index = todos.value.findIndex(todo => todo.id === id)
    if (index > -1) {
      todos.value.splice(index, 1)
    }
  }
  
  const toggleTodo = (id) => {
    const todo = todos.value.find(todo => todo.id === id)
    if (todo) {
      todo.completed = !todo.completed
    }
  }
  
  const setFilter = (newFilter) => {
    filter.value = newFilter
  }
  
  return {
    todos,
    filter,
    filteredTodos,
    addTodo,
    removeTodo,
    toggleTodo,
    setFilter
  }
})
```

#### 创建组件

```vue
<template>
  <div class="todo-app">
    <h1>Todo App</h1>
    
    <!-- 输入框 -->
    <div class="input-section">
      <el-input
        v-model="newTodo"
        placeholder="输入待办事项"
        @keyup.enter="handleAdd"
      />
      <el-button type="primary" @click="handleAdd">添加</el-button>
    </div>
    
    <!-- 过滤器 -->
    <div class="filter-section">
      <el-radio-group v-model="todoStore.filter" @change="todoStore.setFilter">
        <el-radio-button label="all">全部</el-radio-button>
        <el-radio-button label="active">进行中</el-radio-button>
        <el-radio-button label="completed">已完成</el-radio-button>
      </el-radio-group>
    </div>
    
    <!-- 列表 -->
    <div class="todo-list">
      <el-empty v-if="todoStore.filteredTodos.length === 0" description="暂无待办事项" />
      
      <div
        v-for="todo in todoStore.filteredTodos"
        :key="todo.id"
        class="todo-item"
      >
        <el-checkbox
          v-model="todo.completed"
          @change="todoStore.toggleTodo(todo.id)"
        >
          <span :class="{ completed: todo.completed }">{{ todo.text }}</span>
        </el-checkbox>
        
        <el-button
          type="danger"
          size="small"
          @click="todoStore.removeTodo(todo.id)"
        >
          删除
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTodoStore } from '@/stores/todo'

const todoStore = useTodoStore()
const newTodo = ref('')

function handleAdd() {
  if (newTodo.value.trim()) {
    todoStore.addTodo(newTodo.value)
    newTodo.value = ''
  }
}
</script>

<style scoped>
.todo-app {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
}

.input-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-section {
  margin-bottom: 20px;
}

.todo-list {
  margin-top: 20px;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.completed {
  text-decoration: line-through;
  color: #999;
}
</style>
```

### 8.5 项目构建与部署

#### 构建生产版本

```bash
npm run build
```

构建后的文件会在 `dist` 目录中。

#### 预览构建结果

```bash
npm run preview
```

#### 部署到服务器

将 `dist` 目录中的文件上传到服务器即可。如果使用 Nginx，配置示例：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

### 8.6 构建单文件离线 HTML（内联所有资源）

有时候我们需要将 Vue 应用打包成一个单独的 HTML 文件，所有 CSS、JavaScript 和资源都内联其中，方便在 WebView2、Electron 或其他嵌入式浏览器中使用。

#### 8.6.1 使用 vite-plugin-singlefile（推荐）

**步骤 1：安装插件**

```bash
npm install -D vite-plugin-singlefile
```

**步骤 2：配置 vite.config.js**

```javascript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [
    vue(),
    viteSingleFile() // 添加单文件插件
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    // 确保资源内联
    assetsInlineLimit: 100000000, // 100MB，确保所有资源都内联
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        inlineDynamicImports: true
      }
    }
  }
})
```

**步骤 3：构建**

```bash
npm run build
```

构建完成后，在 `dist` 目录下会生成一个单独的 `index.html` 文件，包含所有资源。

#### 8.6.2 高级配置：优化单文件输出

如果需要更多控制，可以自定义配置：

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [
    vue(),
    viteSingleFile({
      removeViteModuleLoader: true, // 移除 Vite 模块加载器
      inlinePattern: ['**/*.{js,css,svg,png,jpg,jpeg,gif}'] // 内联这些类型的文件
    })
  ],
  build: {
    assetsInlineLimit: 100000000,
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
        // 移除哈希，使文件名更简洁
        entryFileNames: 'assets/[name].js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name].[ext]'
      }
    },
    // 如果需要支持旧版浏览器
    target: 'es2015',
    minify: 'terser', // 使用 terser 压缩
    terserOptions: {
      compress: {
        drop_console: true, // 移除 console.log
        drop_debugger: true
      }
    }
  }
})
```

#### 8.6.3 处理外部依赖

如果使用了 CDN 资源或外部链接，需要将它们内联：

**方式一：使用本地依赖**

```javascript
// ❌ 不要使用 CDN
// import 'https://cdn.jsdelivr.net/npm/element-plus'

// ✅ 使用 npm 安装的本地依赖
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
```

**方式二：手动下载并内联**

如果必须使用外部资源，可以下载到本地：

```bash
# 下载 Element Plus CSS
curl -o src/assets/element-plus.css https://unpkg.com/element-plus/dist/index.css
```

然后在代码中引入：

```javascript
import './assets/element-plus.css'
```

#### 8.6.4 处理图片和字体

**内联图片**（推荐用于小图片）：

```vue
<script setup>
// 使用 import 导入图片，Vite 会自动内联小图片
import logo from '@/assets/logo.png'
</script>

<template>
  <img :src="logo" alt="Logo" />
</template>
```

**内联 SVG**：

```vue
<template>
  <!-- 直接内联 SVG 代码 -->
  <svg width="100" height="100">
    <circle cx="50" cy="50" r="40" fill="#42b983" />
  </svg>
</template>
```

**字体处理**：

优先使用系统字体，避免加载外部字体文件：

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 
    'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Microsoft YaHei', sans-serif;
}
```

如果必须使用自定义字体，转换为 Base64 内联：

```css
@font-face {
  font-family: 'CustomFont';
  src: url(data:font/woff2;base64,d09GMgABAAAAABK...) format('woff2');
}
```

#### 8.6.5 完整示例项目

创建一个简单的 Vue 项目并打包成单文件：

**1. 创建项目**

```bash
npm create vue@latest vue-singlefile-demo
cd vue-singlefile-demo
npm install
```

**2. 安装单文件插件**

```bash
npm install -D vite-plugin-singlefile
```

**3. 修改 vite.config.js**

```javascript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [vue(), viteSingleFile()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    assetsInlineLimit: 100000000,
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        inlineDynamicImports: true
      }
    }
  }
})
```

**4. 创建简单的应用 (src/App.vue)**

```vue
<template>
  <div class="app">
    <h1>{{ title }}</h1>
    <p>当前计数：{{ count }}</p>
    <button @click="count++">增加</button>
    <button @click="count--">减少</button>
    <button @click="count = 0">重置</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const title = ref('Vue 单文件 HTML 演示')
const count = ref(0)
</script>

<style scoped>
.app {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  color: white;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

h1 {
  font-size: 2.5em;
  margin-bottom: 30px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

p {
  font-size: 1.5em;
  margin: 20px 0;
}

button {
  margin: 10px;
  padding: 12px 30px;
  font-size: 1.1em;
  border: 2px solid white;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

button:active {
  transform: translateY(0);
}
</style>
```

**5. 构建**

```bash
npm run build
```

**6. 查看结果**

生成的 `dist/index.html` 就是一个完全离线的单文件，可以直接双击打开或在 WebView2 中使用。

#### 8.6.6 验证离线特性

**检查是否真的是单文件**：

```bash
# 查看 dist 目录
ls -la dist/

# 应该只有一个 index.html 文件
# 没有 assets 目录
# 没有 js、css 文件
```

**检查文件中是否有外部依赖**：

```bash
# 在 Windows PowerShell 中
Select-String -Path "dist/index.html" -Pattern "http://" -AllMatches
Select-String -Path "dist/index.html" -Pattern "https://" -AllMatches

# 在 Linux/Mac 中
grep -o "https\?://" dist/index.html

# 如果没有输出，说明没有外部依赖
```

**在浏览器中测试**：

1. 打开浏览器的开发者工具（F12）
2. 切换到 Network（网络）标签
3. 刷新页面
4. 确认没有额外的网络请求（只有 index.html 本身）

#### 8.6.7 使用替代方案：HTML Webpack Plugin Inline

如果使用 Webpack 而不是 Vite：

```bash
npm install -D html-webpack-plugin html-inline-script-webpack-plugin
```

```javascript
// webpack.config.js
const HtmlWebpackPlugin = require('html-webpack-plugin')
const HtmlInlineScriptPlugin = require('html-inline-script-webpack-plugin')

module.exports = {
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
      inlineSource: '.(js|css)$' // 内联所有 JS 和 CSS
    }),
    new HtmlInlineScriptPlugin()
  ]
}
```

#### 8.6.8 注意事项和最佳实践

**1. 文件大小限制**

- 单文件 HTML 会变得很大（几 MB 到几十 MB）
- 首次加载会比较慢
- 适合场景：WebView2、Electron、离线文档

**2. 性能优化**

```javascript
// vite.config.js
export default defineConfig({
  build: {
    // 启用压缩
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log'] // 移除 console.log
      }
    }
  }
})
```

**3. 避免动态导入**

```javascript
// ❌ 避免使用动态导入
const component = () => import('./Component.vue')

// ✅ 使用静态导入
import Component from './Component.vue'
```

**4. 限制第三方库**

只使用必要的库，减小文件体积：

```javascript
// ❌ 引入整个库
import _ from 'lodash'

// ✅ 只引入需要的函数
import debounce from 'lodash/debounce'
```

**5. 图片优化**

```bash
# 压缩图片
npm install -D vite-plugin-imagemin

# 或者使用在线工具
# https://tinypng.com/
# https://squoosh.app/
```

**6. Base64 限制**

对于大文件，Base64 会增加约 33% 的体积：

```javascript
// vite.config.js
export default defineConfig({
  build: {
    // 只内联小于 10KB 的文件
    assetsInlineLimit: 10240 // 10KB
  }
})
```

#### 8.6.9 在 WebView2 中使用

**C# 示例**：

```csharp
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        InitializeWebView();
    }

    private async void InitializeWebView()
    {
        await webView.EnsureCoreWebView2Async();
        
        // 方式一：加载本地文件
        string htmlPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "dist", "index.html");
        webView.CoreWebView2.Navigate($"file:///{htmlPath}");
        
        // 方式二：读取内容加载
        string htmlContent = File.ReadAllText(htmlPath);
        webView.NavigateToString(htmlContent);
    }
}
```

**禁用网络请求（可选）**：

```csharp
webView.CoreWebView2.Settings.IsWebMessageEnabled = true;
webView.CoreWebView2.Settings.AreDefaultContextMenusEnabled = false;

// 拦截网络请求
webView.CoreWebView2.WebResourceRequested += (sender, args) =>
{
    // 只允许加载本地文件
    if (!args.Request.Uri.StartsWith("file://"))
    {
        args.Response = webView.CoreWebView2.Environment.CreateWebResourceResponse(
            null, 403, "Forbidden", "");
    }
};
```

#### 8.6.10 调试单文件 HTML

**开发时使用普通构建**：

```json
// package.json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "build:single": "vite build --config vite.config.single.js"
  }
}
```

**创建专门的配置文件 vite.config.single.js**：

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteSingleFile } from 'vite-plugin-singlefile'

export default defineConfig({
  plugins: [vue(), viteSingleFile()],
  build: {
    assetsInlineLimit: 100000000,
    cssCodeSplit: false,
    rollupOptions: {
      output: {
        inlineDynamicImports: true
      }
    }
  }
})
```

这样开发时用 `npm run dev`，需要单文件时用 `npm run build:single`。

#### 8.6.11 完整打包流程总结

```bash
# 1. 创建 Vue 项目
npm create vue@latest my-vue-app
cd my-vue-app

# 2. 安装依赖
npm install

# 3. 安装单文件插件
npm install -D vite-plugin-singlefile

# 4. 配置 vite.config.js（参考上面的配置）

# 5. 开发应用
npm run dev

# 6. 构建单文件
npm run build

# 7. 验证（dist/index.html 应该是单个文件）
ls -la dist/

# 8. 测试
# 双击 dist/index.html 或在 WebView2 中加载
```

**生成的文件特点**：
- ✅ 单个 HTML 文件
- ✅ 所有 CSS 内联在 `<style>` 标签中
- ✅ 所有 JavaScript 内联在 `<script>` 标签中
- ✅ 所有小图片转为 Base64 内联
- ✅ 无外部依赖
- ✅ 可离线使用
- ✅ 适合 WebView2、Electron、离线文档

### 8.7 构建离线应用（PWA）

Progressive Web App（PWA）可以让你的 Vue 应用支持离线访问，提供类似原生应用的体验。

#### 8.6.1 使用 vite-plugin-pwa

**安装插件**：

```bash
npm install -D vite-plugin-pwa
```

**配置 vite.config.js**：

```javascript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: '我的 Vue 应用',
        short_name: 'Vue App',
        description: '一个支持离线访问的 Vue3 应用',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      workbox: {
        // 缓存策略
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'google-fonts-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365 // 1 年
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          },
          {
            urlPattern: /^https:\/\/cdn\.jsdelivr\.net\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'cdn-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 30 // 30 天
              }
            }
          },
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'image-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 * 30 // 30 天
              }
            }
          },
          {
            urlPattern: /^https:\/\/api\.example\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 20,
                maxAgeSeconds: 60 * 5 // 5 分钟
              },
              networkTimeoutSeconds: 10
            }
          }
        ],
        // 离线页面
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/api/]
      },
      devOptions: {
        enabled: true // 开发环境也启用 PWA
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: 'localhost',
    port: 8000
  }
})
```

#### 8.6.2 在应用中使用 PWA

**在 main.js 中注册 Service Worker**：

```javascript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app')

// 注册 Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('SW registered: ', registration)
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError)
      })
  })
}
```

#### 8.6.3 添加 PWA 更新提示

创建一个更新提示组件：

```vue
<!-- components/UpdatePrompt.vue -->
<template>
  <div v-if="needRefresh" class="update-prompt">
    <div class="update-content">
      <p>发现新版本，请刷新页面获取最新内容</p>
      <div class="update-actions">
        <button @click="updateApp" class="btn-update">立即更新</button>
        <button @click="closePrompt" class="btn-close">稍后</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRegisterSW } from 'virtual:pwa-register/vue'

const needRefresh = ref(false)
let updateSW

onMounted(() => {
  const { needRefresh: _needRefresh, updateServiceWorker } = useRegisterSW()
  needRefresh.value = _needRefresh.value
  updateSW = updateServiceWorker
})

function updateApp() {
  updateSW && updateSW(true)
}

function closePrompt() {
  needRefresh.value = false
}
</script>

<style scoped>
.update-prompt {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 300px;
}

.update-content p {
  margin: 0 0 15px;
  color: #333;
}

.update-actions {
  display: flex;
  gap: 10px;
}

.btn-update,
.btn-close {
  flex: 1;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-update {
  background: #409eff;
  color: white;
}

.btn-close {
  background: #ddd;
  color: #333;
}
</style>
```

在 App.vue 中使用：

```vue
<template>
  <div id="app">
    <UpdatePrompt />
    <router-view />
  </div>
</template>

<script setup>
import UpdatePrompt from './components/UpdatePrompt.vue'
</script>
```

#### 8.6.4 自定义 Service Worker

如果需要更多控制，可以自定义 Service Worker：

创建 `public/sw.js`：

```javascript
// 缓存名称
const CACHE_NAME = 'vue-app-v1'

// 需要缓存的文件
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/css/app.css',
  '/js/app.js'
]

// 安装 Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache')
        return cache.addAll(urlsToCache)
      })
  )
})

// 激活 Service Worker
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName)
            return caches.delete(cacheName)
          }
        })
      )
    })
  )
})

// 拦截请求
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // 缓存命中 - 返回缓存的响应
        if (response) {
          return response
        }

        // 克隆请求
        const fetchRequest = event.request.clone()

        return fetch(fetchRequest).then(response => {
          // 检查是否是有效响应
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response
          }

          // 克隆响应
          const responseToCache = response.clone()

          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache)
            })

          return response
        })
      })
  )
})
```

#### 8.6.5 添加离线页面

创建 `public/offline.html`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>离线模式</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .offline-container {
      text-align: center;
      padding: 40px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      backdrop-filter: blur(10px);
    }
    h1 {
      font-size: 3em;
      margin: 0 0 20px;
    }
    p {
      font-size: 1.2em;
      margin: 0 0 30px;
    }
    .retry-btn {
      padding: 15px 30px;
      font-size: 1em;
      background: white;
      color: #667eea;
      border: none;
      border-radius: 50px;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .retry-btn:hover {
      transform: scale(1.05);
    }
  </style>
</head>
<body>
  <div class="offline-container">
    <h1>📱 离线模式</h1>
    <p>您当前处于离线状态</p>
    <p>请检查网络连接后重试</p>
    <button class="retry-btn" onclick="location.reload()">重新加载</button>
  </div>
</body>
</html>
```

#### 8.6.6 监听网络状态

创建一个组合式函数监听网络状态：

```javascript
// composables/useNetworkStatus.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useNetworkStatus() {
  const isOnline = ref(navigator.onLine)

  const updateOnlineStatus = () => {
    isOnline.value = navigator.onLine
  }

  onMounted(() => {
    window.addEventListener('online', updateOnlineStatus)
    window.addEventListener('offline', updateOnlineStatus)
  })

  onUnmounted(() => {
    window.removeEventListener('online', updateOnlineStatus)
    window.removeEventListener('offline', updateOnlineStatus)
  })

  return {
    isOnline
  }
}
```

在组件中使用：

```vue
<template>
  <div class="network-status">
    <div v-if="!isOnline" class="offline-banner">
      ⚠️ 您当前处于离线状态
    </div>
  </div>
</template>

<script setup>
import { useNetworkStatus } from '@/composables/useNetworkStatus'

const { isOnline } = useNetworkStatus()
</script>

<style scoped>
.offline-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #f56c6c;
  color: white;
  padding: 10px;
  text-align: center;
  z-index: 9999;
}
</style>
```

#### 8.6.7 IndexedDB 离线数据存储

对于需要离线存储数据的应用，可以使用 IndexedDB：

```javascript
// utils/db.js
class Database {
  constructor(dbName, storeName) {
    this.dbName = dbName
    this.storeName = storeName
    this.db = null
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        this.db = request.result
        resolve()
      }

      request.onupgradeneeded = (event) => {
        const db = event.target.result
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id', autoIncrement: true })
        }
      }
    })
  }

  async add(data) {
    const transaction = this.db.transaction([this.storeName], 'readwrite')
    const store = transaction.objectStore(this.storeName)
    return store.add(data)
  }

  async getAll() {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([this.storeName], 'readonly')
      const store = transaction.objectStore(this.storeName)
      const request = store.getAll()

      request.onsuccess = () => resolve(request.result)
      request.onerror = () => reject(request.error)
    })
  }

  async delete(id) {
    const transaction = this.db.transaction([this.storeName], 'readwrite')
    const store = transaction.objectStore(this.storeName)
    return store.delete(id)
  }

  async clear() {
    const transaction = this.db.transaction([this.storeName], 'readwrite')
    const store = transaction.objectStore(this.storeName)
    return store.clear()
  }
}

export default Database
```

使用示例：

```javascript
import Database from '@/utils/db'

// 初始化数据库
const db = new Database('MyApp', 'todos')
await db.init()

// 添加数据
await db.add({ text: 'Learn Vue3', completed: false })

// 获取所有数据
const todos = await db.getAll()

// 删除数据
await db.delete(1)

// 清空所有数据
await db.clear()
```

#### 8.6.8 构建与测试

**构建 PWA 应用**：

```bash
npm run build
```

**本地测试 PWA**：

```bash
# 安装 serve
npm install -g serve

# 启动静态服务器
serve -s dist -p 3000

# 或使用 Vite 的预览功能
npm run preview
```

**PWA 检查清单**：

1. ✅ HTTPS 部署（本地开发可以用 localhost）
2. ✅ 有效的 `manifest.json`
3. ✅ Service Worker 正确注册
4. ✅ 至少有 192x192 和 512x512 的图标
5. ✅ 离线时可访问
6. ✅ 快速加载（< 3 秒）
7. ✅ 响应式设计

**使用 Lighthouse 测试**：

在 Chrome 开发者工具中：
1. 打开 DevTools（F12）
2. 点击 "Lighthouse" 标签
3. 选择 "Progressive Web App"
4. 点击 "Generate report"

#### 8.6.9 PWA 部署注意事项

1. **HTTPS 要求**：PWA 必须通过 HTTPS 提供服务（localhost 除外）

2. **缓存策略选择**：
   - `CacheFirst`：优先使用缓存（适用于静态资源）
   - `NetworkFirst`：优先使用网络（适用于 API 请求）
   - `StaleWhileRevalidate`：返回缓存同时更新缓存（适用于可容忍过期数据）

3. **版本管理**：每次更新时修改 Service Worker 以触发更新

4. **调试技巧**：
   - Chrome DevTools → Application → Service Workers
   - 可以手动注销 Service Worker 进行测试
   - 使用 "Update on reload" 选项方便开发

---

## 九、Vue 应用美化与增强

### 9.1 动画库 - 让页面动起来

#### 9.1.1 Animate.css（最简单）

**安装**：

```bash
npm install animate.css
```

**在 main.js 中引入**：

```javascript
import 'animate.css'
```

**使用示例**：

```vue
<template>
  <!-- 基础动画 -->
  <div class="animate__animated animate__fadeIn">
    <h1 class="animate__animated animate__bounceIn">欢迎来到 Vue3</h1>
  </div>
  
  <!-- 带延迟的动画 -->
  <div class="animate__animated animate__slideInLeft animate__delay-1s">
    延迟 1 秒出现
  </div>
  
  <!-- 无限循环动画 -->
  <div class="animate__animated animate__bounce animate__infinite">
    一直跳动
  </div>
  
  <!-- 配合 v-if 使用 -->
  <div v-if="show" class="animate__animated animate__zoomIn">
    条件显示
  </div>
</template>

<script setup>
import { ref } from 'vue'
const show = ref(true)
</script>
```

**常用动画类名**：
- `animate__fadeIn` / `animate__fadeOut` - 淡入/淡出
- `animate__slideInLeft` / `animate__slideInRight` - 滑入
- `animate__bounceIn` / `animate__bounceOut` - 弹跳
- `animate__zoomIn` / `animate__zoomOut` - 缩放
- `animate__rotateIn` / `animate__rotateOut` - 旋转
- `animate__flip` - 翻转

#### 9.1.2 GSAP（专业级动画库）

**安装**：

```bash
npm install gsap
```

**基础使用**：

```vue
<template>
  <div ref="box" class="box">动画盒子</div>
  <button @click="animateBox">播放动画</button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'

const box = ref(null)

// 组件挂载时的动画
onMounted(() => {
  gsap.from(box.value, {
    duration: 1,
    x: -100,
    opacity: 0,
    ease: 'power2.out'
  })
})

// 点击触发的动画
function animateBox() {
  gsap.to(box.value, {
    duration: 0.5,
    rotation: 360,
    scale: 1.2,
    backgroundColor: '#42b983',
    ease: 'elastic.out(1, 0.3)'
  })
}
</script>

<style scoped>
.box {
  width: 100px;
  height: 100px;
  background: #409eff;
  border-radius: 10px;
  margin: 20px;
}
</style>
```

**时间线动画**：

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'

const container = ref(null)

onMounted(() => {
  const tl = gsap.timeline()
  
  tl.from('.title', {
    duration: 1,
    y: -50,
    opacity: 0
  })
  .from('.subtitle', {
    duration: 0.8,
    y: 30,
    opacity: 0
  }, '-=0.5') // 提前 0.5 秒开始
  .from('.content', {
    duration: 1,
    scale: 0,
    stagger: 0.2 // 每个元素间隔 0.2 秒
  })
})
</script>

<template>
  <div ref="container">
    <h1 class="title">标题</h1>
    <h2 class="subtitle">副标题</h2>
    <div class="content">内容 1</div>
    <div class="content">内容 2</div>
    <div class="content">内容 3</div>
  </div>
</template>
```

#### 9.1.3 Vue Transition 内置动画

```vue
<template>
  <!-- 基础过渡 -->
  <button @click="show = !show">切换</button>
  <Transition name="fade">
    <p v-if="show">Hello Vue!</p>
  </Transition>
  
  <!-- 列表过渡 -->
  <TransitionGroup name="list" tag="ul">
    <li v-for="item in items" :key="item">
      {{ item }}
    </li>
  </TransitionGroup>
</template>

<script setup>
import { ref } from 'vue'
const show = ref(true)
const items = ref([1, 2, 3, 4, 5])
</script>

<style scoped>
/* 淡入淡出 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 列表过渡 */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
```

### 9.2 粒子效果背景

#### 9.2.1 particles.js

**安装**：

```bash
npm install particles.js
```

**创建粒子组件**：

```vue
<!-- components/ParticlesBackground.vue -->
<template>
  <div id="particles-js"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import 'particles.js'

onMounted(() => {
  window.particlesJS('particles-js', {
    particles: {
      number: {
        value: 80,
        density: {
          enable: true,
          value_area: 800
        }
      },
      color: {
        value: '#42b983'
      },
      shape: {
        type: 'circle'
      },
      opacity: {
        value: 0.5,
        random: false
      },
      size: {
        value: 3,
        random: true
      },
      line_linked: {
        enable: true,
        distance: 150,
        color: '#42b983',
        opacity: 0.4,
        width: 1
      },
      move: {
        enable: true,
        speed: 2,
        direction: 'none',
        random: false,
        straight: false,
        out_mode: 'out',
        bounce: false
      }
    },
    interactivity: {
      detect_on: 'canvas',
      events: {
        onhover: {
          enable: true,
          mode: 'repulse'
        },
        onclick: {
          enable: true,
          mode: 'push'
        },
        resize: true
      }
    },
    retina_detect: true
  })
})
</script>

<style scoped>
#particles-js {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
```

#### 9.2.2 vue-particles

**安装**：

```bash
npm install @tsparticles/vue3
```

**使用示例**：

```vue
<template>
  <Particles
    id="tsparticles"
    :particlesInit="particlesInit"
    :options="options"
  />
</template>

<script setup>
import { loadFull } from 'tsparticles'

const particlesInit = async (engine) => {
  await loadFull(engine)
}

const options = {
  background: {
    color: {
      value: '#0d47a1'
    }
  },
  fpsLimit: 60,
  particles: {
    color: {
      value: '#ffffff'
    },
    links: {
      color: '#ffffff',
      distance: 150,
      enable: true,
      opacity: 0.5,
      width: 1
    },
    move: {
      enable: true,
      speed: 2
    },
    number: {
      value: 80
    },
    opacity: {
      value: 0.5
    },
    size: {
      value: { min: 1, max: 5 }
    }
  }
}
</script>
```

### 9.3 图表库

#### 9.3.1 ECharts

**安装**：

```bash
npm install echarts
```

**使用示例**：

```vue
<template>
  <div ref="chartRef" style="width: 600px; height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)

onMounted(() => {
  const myChart = echarts.init(chartRef.value)
  
  const option = {
    title: {
      text: 'Vue3 学习进度'
    },
    tooltip: {},
    xAxis: {
      data: ['基础', '组件', '路由', 'Pinia', '项目实战']
    },
    yAxis: {},
    series: [
      {
        name: '掌握程度',
        type: 'bar',
        data: [90, 85, 80, 75, 70],
        itemStyle: {
          color: '#42b983'
        }
      }
    ]
  }
  
  myChart.setOption(option)
  
  // 响应式
  window.addEventListener('resize', () => {
    myChart.resize()
  })
})
</script>
```

#### 9.3.2 Chart.js

**安装**：

```bash
npm install chart.js vue-chartjs
```

**使用示例**：

```vue
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartData = {
  labels: ['一月', '二月', '三月', '四月', '五月'],
  datasets: [
    {
      label: '数据集',
      backgroundColor: '#42b983',
      data: [40, 20, 30, 50, 60]
    }
  ]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
</script>
```

### 9.4 拖拽排序

#### 9.4.1 Sortable.js

**安装**：

```bash
npm install sortablejs
```

**使用示例**：

```vue
<template>
  <div>
    <h3>拖拽排序列表</h3>
    <ul ref="listRef" class="sortable-list">
      <li v-for="item in items" :key="item.id" class="sortable-item">
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sortable from 'sortablejs'

const listRef = ref(null)
const items = ref([
  { id: 1, name: '项目 1' },
  { id: 2, name: '项目 2' },
  { id: 3, name: '项目 3' },
  { id: 4, name: '项目 4' }
])

onMounted(() => {
  Sortable.create(listRef.value, {
    animation: 150,
    onEnd: (evt) => {
      const movedItem = items.value.splice(evt.oldIndex, 1)[0]
      items.value.splice(evt.newIndex, 0, movedItem)
      console.log('新顺序:', items.value)
    }
  })
})
</script>

<style scoped>
.sortable-list {
  list-style: none;
  padding: 0;
}

.sortable-item {
  padding: 15px;
  margin: 10px 0;
  background: #f5f5f5;
  border-radius: 8px;
  cursor: move;
  transition: background 0.3s;
}

.sortable-item:hover {
  background: #e0e0e0;
}
</style>
```

### 9.5 Toast 通知

#### 9.5.1 使用 Element Plus Message

```vue
<script setup>
import { ElMessage } from 'element-plus'

function showSuccess() {
  ElMessage.success('操作成功！')
}

function showError() {
  ElMessage.error('操作失败！')
}

function showWarning() {
  ElMessage.warning('警告信息')
}

function showInfo() {
  ElMessage.info('提示信息')
}
</script>

<template>
  <div>
    <el-button @click="showSuccess">成功</el-button>
    <el-button @click="showError">错误</el-button>
    <el-button @click="showWarning">警告</el-button>
    <el-button @click="showInfo">信息</el-button>
  </div>
</template>
```

#### 9.5.2 Vue Toastification

**安装**：

```bash
npm install vue-toastification@next
```

**配置**：

```javascript
// main.js
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

app.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
})
```

**使用**：

```vue
<script setup>
import { useToast } from 'vue-toastification'

const toast = useToast()

function showToast() {
  toast.success('太棒了！')
  toast.error('出错了！')
  toast.warning('请注意！')
  toast.info('温馨提示')
}
</script>
```

### 9.6 加载动画

#### 9.6.1 Element Plus Loading

```vue
<script setup>
import { ElLoading } from 'element-plus'

function showLoading() {
  const loading = ElLoading.service({
    lock: true,
    text: '加载中...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  
  setTimeout(() => {
    loading.close()
  }, 2000)
}

async function fetchData() {
  const loading = ElLoading.service()
  try {
    // 模拟 API 请求
    await new Promise(resolve => setTimeout(resolve, 2000))
  } finally {
    loading.close()
  }
}
</script>

<template>
  <el-button @click="showLoading">显示加载</el-button>
  <el-button @click="fetchData">加载数据</el-button>
</template>
```

#### 9.6.2 自定义骨架屏

```vue
<template>
  <div v-if="loading" class="skeleton">
    <div class="skeleton-avatar"></div>
    <div class="skeleton-content">
      <div class="skeleton-line"></div>
      <div class="skeleton-line short"></div>
    </div>
  </div>
  <div v-else class="content">
    <!-- 实际内容 -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(true)

onMounted(() => {
  setTimeout(() => {
    loading.value = false
  }, 2000)
})
</script>

<style scoped>
.skeleton {
  display: flex;
  padding: 20px;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.skeleton-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #e0e0e0;
  margin-right: 20px;
}

.skeleton-content {
  flex: 1;
}

.skeleton-line {
  height: 16px;
  background: #e0e0e0;
  border-radius: 4px;
  margin-bottom: 10px;
}

.skeleton-line.short {
  width: 60%;
}
</style>
```

### 9.7 图标库

#### 9.7.1 Element Plus Icons

```bash
npm install @element-plus/icons-vue
```

```vue
<script setup>
import { Search, Edit, Delete, Plus } from '@element-plus/icons-vue'
</script>

<template>
  <el-button :icon="Search">搜索</el-button>
  <el-button :icon="Edit" type="primary">编辑</el-button>
  <el-button :icon="Delete" type="danger">删除</el-button>
  <el-button :icon="Plus" type="success">添加</el-button>
</template>
```

#### 9.7.2 Font Awesome

```bash
npm install @fortawesome/fontawesome-svg-core
npm install @fortawesome/free-solid-svg-icons
npm install @fortawesome/vue-fontawesome@latest-3
```

```javascript
// main.js
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(fas)
app.component('font-awesome-icon', FontAwesomeIcon)
```

```vue
<template>
  <font-awesome-icon icon="coffee" />
  <font-awesome-icon icon="home" size="2x" />
  <font-awesome-icon icon="spinner" spin />
</template>
```

### 9.8 滚动动画

#### 9.8.1 AOS (Animate On Scroll)

**安装**：

```bash
npm install aos
```

**配置**：

```javascript
// main.js
import AOS from 'aos'
import 'aos/dist/aos.css'

app.mount('#app')
AOS.init()
```

**使用**：

```vue
<template>
  <div data-aos="fade-up">淡入向上</div>
  <div data-aos="fade-down" data-aos-delay="300">延迟 300ms</div>
  <div data-aos="zoom-in" data-aos-duration="1000">缩放 1 秒</div>
  <div data-aos="flip-left">翻转</div>
</template>
```

### 9.9 颜色选择器

#### 9.9.1 Element Plus Color Picker

```vue
<template>
  <div>
    <el-color-picker v-model="color" />
    <p>选择的颜色：{{ color }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const color = ref('#42b983')
</script>
```

### 9.10 富文本编辑器

#### 9.10.1 Quill

**安装**：

```bash
npm install @vueup/vue-quill
```

**使用**：

```vue
<template>
  <QuillEditor 
    v-model:content="content" 
    theme="snow"
    toolbar="full"
  />
</template>

<script setup>
import { ref } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const content = ref('')
</script>
```

### 9.11 日期时间选择器增强

#### 9.11.1 Vue Datepicker

```bash
npm install @vuepic/vue-datepicker
```

```vue
<template>
  <Datepicker v-model="date" />
</template>

<script setup>
import { ref } from 'vue'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

const date = ref(new Date())
</script>
```

### 9.12 虚拟滚动（大数据列表优化）

#### 9.12.1 vue-virtual-scroller

**安装**：

```bash
npm install vue-virtual-scroller
```

**使用**：

```vue
<template>
  <RecycleScroller
    class="scroller"
    :items="items"
    :item-size="50"
    key-field="id"
    v-slot="{ item }"
  >
    <div class="item">{{ item.name }}</div>
  </RecycleScroller>
</template>

<script setup>
import { ref } from 'vue'
import { RecycleScroller } from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

const items = ref(
  Array.from({ length: 10000 }, (_, i) => ({
    id: i,
    name: `Item ${i}`
  }))
)
</script>

<style scoped>
.scroller {
  height: 400px;
}

.item {
  height: 50px;
  padding: 15px;
  border-bottom: 1px solid #eee;
}
</style>
```

### 9.13 完整美化示例

```vue
<template>
  <div class="beautiful-page">
    <!-- 粒子背景 -->
    <ParticlesBackground />
    
    <!-- 主内容区 -->
    <div class="content">
      <!-- 标题动画 -->
      <h1 
        class="animate__animated animate__fadeInDown"
        data-aos="fade-down"
      >
        欢迎来到 Vue3
      </h1>
      
      <!-- 卡片网格 -->
      <div class="card-grid">
        <div 
          v-for="(card, index) in cards" 
          :key="index"
          class="card"
          data-aos="zoom-in"
          :data-aos-delay="index * 100"
        >
          <el-icon :size="40" class="card-icon">
            <component :is="card.icon" />
          </el-icon>
          <h3>{{ card.title }}</h3>
          <p>{{ card.description }}</p>
        </div>
      </div>
      
      <!-- 统计图表 -->
      <div class="chart-container" data-aos="fade-up">
        <div ref="chartRef" style="width: 100%; height: 400px;"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Star, Trophy } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import AOS from 'aos'
import 'aos/dist/aos.css'
import 'animate.css'

const cards = [
  { icon: Search, title: '快速搜索', description: '强大的搜索功能' },
  { icon: Star, title: '收藏夹', description: '收藏你喜欢的内容' },
  { icon: Trophy, title: '成就系统', description: '解锁各种成就' }
]

const chartRef = ref(null)

onMounted(() => {
  AOS.init({
    duration: 1000,
    once: true
  })
  
  // 初始化图表
  const myChart = echarts.init(chartRef.value)
  myChart.setOption({
    title: { text: '数据统计' },
    tooltip: {},
    xAxis: { data: ['周一', '周二', '周三', '周四', '周五'] },
    yAxis: {},
    series: [{
      name: '访问量',
      type: 'line',
      smooth: true,
      data: [120, 200, 150, 300, 250],
      itemStyle: { color: '#42b983' }
    }]
  })
})
</script>

<style scoped>
.beautiful-page {
  min-height: 100vh;
  position: relative;
}

.content {
  position: relative;
  z-index: 1;
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: white;
  font-size: 3em;
  margin-bottom: 60px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.card {
  background: rgba(255, 255, 255, 0.9);
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  backdrop-filter: blur(10px);
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.card-icon {
  color: #42b983;
  margin-bottom: 20px;
}

.card h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.card p {
  color: #666;
}

.chart-container {
  background: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}
</style>
```

---

## 十、常见问题与解决方案

### 10.1 TypeScript 相关

#### 问题：找不到模块 './App.vue'

**解决方案**：在 `env.d.ts` 文件中添加：

```typescript
declare module "*.vue" {
  import type { DefineComponent } from "vue"
  const vueComponent: DefineComponent<{}, {}, any>
  export default vueComponent
}
```

在 `tsconfig.json` 中确保包含：

```json
{
  "include": [
    "env.d.ts",
    "src/**/*.ts",
    "src/**/*.d.ts",
    "src/**/*.tsx",
    "src/**/*.vue"
  ]
}
```

#### 问题：导入 JSON 文件报错

**解决方案**：在 `tsconfig.json` 中添加：

```json
{
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

#### 问题：引用 process 提示错误

**解决方案**：

1. 安装类型定义：

```bash
npm i --save-dev @types/node
```

2. 在 `tsconfig.json` 中添加：

```json
{
  "compilerOptions": {
    "types": ["vite/client", "node"]
  }
}
```

3. 在 `vite.config.js` 中添加：

```javascript
export default defineConfig({
  define: {
    'process.env': {}
  }
})
```

或直接使用 Vite 的环境变量：

```javascript
console.log(import.meta.env)
```

### 10.2 开发建议

1. **使用 Composition API**：更灵活，更易于代码复用
2. **优先使用 `ref()`**：比 `reactive()` 限制更少
3. **组件职责单一**：每个组件只做一件事
4. **合理使用 Pinia**：不要滥用全局状态
5. **注意性能优化**：使用 `v-memo`、`v-once` 等优化指令
6. **代码规范**：使用 ESLint + Prettier
7. **类型安全**：尽可能使用 TypeScript

---

## 十一、将文档转换为离线 HTML

### 11.1 使用 Markdown 转 HTML 工具

#### 方法一：使用 marked-cli（推荐）

**安装工具**：

```bash
npm install -g marked
```

**转换命令**：

```bash
# 基础转换
marked 从零开始的vue学习.md -o vue学习文档.html

# 添加 GitHub 样式
marked 从零开始的vue学习.md -o vue学习文档.html --gfm
```

#### 方法二：使用 Pandoc

**安装 Pandoc**：

```bash
# Windows (使用 Chocolatey)
choco install pandoc

# macOS (使用 Homebrew)
brew install pandoc

# Linux (Ubuntu/Debian)
sudo apt-get install pandoc
```

**转换命令**：

```bash
pandoc 从零开始的vue学习.md -s -o vue学习文档.html --metadata title="Vue3学习指南"
```

**带样式的转换**：

```bash
pandoc 从零开始的vue学习.md -s -o vue学习文档.html \
  --metadata title="Vue3学习指南" \
  --css=github-markdown.css \
  --toc \
  --toc-depth=3
```

#### 方法三：使用在线工具

1. **Markdown to HTML**：https://markdowntohtml.com/
   - 上传 MD 文件
   - 选择样式
   - 下载 HTML

2. **Dillinger**：https://dillinger.io/
   - 粘贴 Markdown 内容
   - 导出为 HTML

3. **StackEdit**：https://stackedit.io/
   - 导入 MD 文件
   - 导出为 HTML

#### 方法四：使用 Node.js 脚本

创建 `convert-to-html.js`：

```javascript
const fs = require('fs')
const marked = require('marked')
const path = require('path')

// 配置 marked
marked.setOptions({
  highlight: function(code, lang) {
    // 可选：添加代码高亮
    return code
  },
  breaks: true,
  gfm: true
})

// HTML 模板
const htmlTemplate = (content, title) => `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      background: #f5f5f5;
      padding: 20px;
    }
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      background: white;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    h1 {
      color: #42b983;
      border-bottom: 3px solid #42b983;
      padding-bottom: 10px;
      margin-bottom: 30px;
    }
    
    h2 {
      color: #35495e;
      margin-top: 40px;
      margin-bottom: 20px;
      padding-bottom: 10px;
      border-bottom: 2px solid #e0e0e0;
    }
    
    h3 {
      color: #2c3e50;
      margin-top: 30px;
      margin-bottom: 15px;
    }
    
    h4 {
      color: #34495e;
      margin-top: 20px;
      margin-bottom: 10px;
    }
    
    code {
      background: #f4f4f4;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: 'Courier New', Courier, monospace;
      font-size: 0.9em;
      color: #e83e8c;
    }
    
    pre {
      background: #2d2d2d;
      color: #f8f8f2;
      padding: 20px;
      border-radius: 6px;
      overflow-x: auto;
      margin: 20px 0;
    }
    
    pre code {
      background: transparent;
      color: inherit;
      padding: 0;
      font-size: 14px;
    }
    
    blockquote {
      border-left: 4px solid #42b983;
      padding-left: 20px;
      margin: 20px 0;
      color: #666;
      font-style: italic;
      background: #f9f9f9;
      padding: 15px 20px;
      border-radius: 4px;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    
    th, td {
      padding: 12px;
      text-align: left;
      border: 1px solid #ddd;
    }
    
    th {
      background: #42b983;
      color: white;
      font-weight: bold;
    }
    
    tr:nth-child(even) {
      background: #f9f9f9;
    }
    
    a {
      color: #42b983;
      text-decoration: none;
    }
    
    a:hover {
      text-decoration: underline;
    }
    
    ul, ol {
      margin: 15px 0;
      padding-left: 30px;
    }
    
    li {
      margin: 8px 0;
    }
    
    img {
      max-width: 100%;
      height: auto;
      border-radius: 4px;
      margin: 20px 0;
    }
    
    hr {
      border: none;
      border-top: 2px solid #e0e0e0;
      margin: 40px 0;
    }
    
    .toc {
      background: #f9f9f9;
      padding: 20px;
      border-radius: 6px;
      margin: 30px 0;
    }
    
    .toc h2 {
      margin-top: 0;
      color: #42b983;
      border: none;
    }
    
    .toc ul {
      list-style-type: none;
      padding-left: 0;
    }
    
    .toc li {
      margin: 5px 0;
    }
    
    .toc a {
      color: #35495e;
    }
    
    @media print {
      body {
        background: white;
        padding: 0;
      }
      
      .container {
        box-shadow: none;
      }
    }
    
    @media (max-width: 768px) {
      body {
        padding: 10px;
      }
      
      .container {
        padding: 20px;
      }
      
      pre {
        padding: 15px;
        font-size: 12px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    ${content}
  </div>
  
  <script>
    // 添加代码复制功能
    document.querySelectorAll('pre code').forEach(block => {
      const pre = block.parentElement
      const button = document.createElement('button')
      button.textContent = '复制'
      button.style.cssText = 'position:absolute;top:5px;right:5px;padding:5px 10px;background:#42b983;color:white;border:none;border-radius:3px;cursor:pointer;font-size:12px;'
      
      pre.style.position = 'relative'
      pre.appendChild(button)
      
      button.addEventListener('click', () => {
        navigator.clipboard.writeText(block.textContent)
        button.textContent = '已复制!'
        setTimeout(() => {
          button.textContent = '复制'
        }, 2000)
      })
    })
    
    // 添加平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault()
        const target = document.querySelector(this.getAttribute('href'))
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth'
          })
        }
      })
    })
  </script>
</body>
</html>
`

// 读取并转换
const mdContent = fs.readFileSync('从零开始的vue学习.md', 'utf8')
const htmlContent = marked.parse(mdContent)
const fullHtml = htmlTemplate(htmlContent, 'Vue3 学习指南')

// 保存 HTML
fs.writeFileSync('vue学习文档.html', fullHtml, 'utf8')

console.log('✅ HTML 文档已生成：vue学习文档.html')
```

**使用方法**：

```bash
# 安装依赖
npm install marked

# 运行脚本
node convert-to-html.js
```

#### 方法五：使用 VuePress 或 VitePress

如果想要更专业的文档站点：

**VitePress（推荐）**：

```bash
# 安装 VitePress
npm install -D vitepress

# 创建文档目录
mkdir docs
mv 从零开始的vue学习.md docs/index.md

# 添加配置文件 docs/.vitepress/config.js
```

```javascript
// docs/.vitepress/config.js
export default {
  title: 'Vue3 学习指南',
  description: '从零开始学习 Vue3',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/index' }
    ],
    sidebar: [
      {
        text: '指南',
        items: [
          { text: 'Vue3 学习', link: '/index' }
        ]
      }
    ]
  }
}
```

**运行文档站点**：

```bash
# 开发模式
npx vitepress dev docs

# 构建为静态 HTML
npx vitepress build docs

# 预览构建结果
npx vitepress preview docs
```

构建后的 HTML 文件位于 `docs/.vitepress/dist` 目录，可以直接用浏览器打开 `index.html`。

### 11.2 添加代码高亮

如果需要代码高亮，可以使用 `highlight.js`：

```bash
npm install highlight.js
```

修改转换脚本：

```javascript
const hljs = require('highlight.js')

marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  }
})
```

并在 HTML 模板中添加高亮样式：

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
```

### 11.3 生成 PDF

如果需要 PDF 版本：

```bash
# 使用 Pandoc
pandoc 从零开始的vue学习.md -o vue学习文档.pdf

# 或者先转 HTML，再用浏览器打印为 PDF
# 在浏览器中打开 HTML，按 Ctrl+P，选择"另存为 PDF"
```

---

## 十二、学习资源

### 12.1 官方资源

- **Vue3 官方文档**：https://cn.vuejs.org/
- **Vue Router 文档**：https://router.vuejs.org/zh/
- **Pinia 文档**：https://pinia.vuejs.org/zh/
- **Vite 文档**：https://cn.vitejs.dev/

### 12.2 UI 组件库

- **Element Plus**：https://element-plus.org/zh-CN/
- **Ant Design Vue**：https://www.antdv.com/
- **Naive UI**：https://www.naiveui.com/zh-CN/
- **Vant**：https://vant-ui.github.io/vant/

### 12.3 学习平台

- **Vue Mastery**：https://www.vuemastery.com/
- **Vue School**：https://vueschool.io/
- **哔哩哔哩**：搜索"Vue3 教程"

### 12.4 开发工具

- **Vue DevTools**：浏览器扩展，用于调试 Vue 应用
- **Volar**：VS Code 的 Vue3 语言支持扩展
- **Vite**：下一代前端构建工具

---

## 总结

通过本指南，你已经学习了：

1. ✅ Vue3 的基本概念和特点
2. ✅ 环境搭建和项目创建
3. ✅ 模板语法、响应式系统、事件处理
4. ✅ 组件开发、Props、事件传递
5. ✅ Vue Router 路由管理
6. ✅ Pinia 状态管理
7. ✅ Element Plus 等 UI 组件库的使用
8. ✅ 完整项目的开发流程

**下一步建议**：

1. 动手实践，完成几个小项目
2. 深入学习 Composition API
3. 学习 TypeScript 与 Vue3 的结合
4. 了解 Vue3 性能优化技巧
5. 学习服务端渲染（SSR）和静态站点生成（SSG）

祝你学习愉快！💪🚀
