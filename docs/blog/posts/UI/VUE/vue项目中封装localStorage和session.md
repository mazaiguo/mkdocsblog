---
title: Vue项目中封装localStorage和session
date: 2024-04-25
categories:
  - Vue
  - 前端开发
  - JavaScript
tags:
  - Vue
  - localStorage
  - sessionStorage
  - 数据存储
description: Vue项目中封装localStorage和sessionStorage的实用工具类，提高代码的可维护性
author: JerryMa
---

# vue项目中封装localStorage和sessionStorage

## **1. 为什么需要封装localStorage和sessionStorage？**

因为封装localStorage和sessionStorage可以提高程序的维护性、可重用性和扩展性，同时也可以使代码更为简单、易懂。

## **2. 以下是一个简单的代码封装示例**

可以新建一个utils目录文件，在该文件下新建storage.js文件进行封装

```javascript
// 封装localhost和Session

// 本地储存
export const Local = {
  // 设置永久缓存
  set (key, val) {
    window.localStorage.setItem(key, JSON.stringify(val));
  },
  // 获取永久缓存
  get (key) {
    let json = window.localStorage.getItem(key);
    return JSON.parse(json);
  },
  // 移除永久缓存
  remove (key) {
    window.localStorage.removeItem(key);
  },
  // 移除全部永久缓存
  clear () {
    window.localStorage.clear();
  },
};

// 临时储存
export const Session = {
  // 设置临时缓存
  set (key, val) {
    window.sessionStorage.setItem(key, JSON.stringify(val));
  },
  // 获取临时缓存
  get (key) {
    let json = window.sessionStorage.getItem(key);
    return JSON.parse(json);
  },
  // 移除临时缓存
  remove (key) {
    window.sessionStorage.removeItem(key);
  },
  // 移除全部临时缓存
  clear () {
    window.sessionStorage.clear();
  },
}

export default {
  Local,
  Session
}
```

## **3.在vue组件中使用**

按需引入

```bash
import { Session } from '@/utils/storage'
```

页面使用

```javascript
 // 设置临时缓存
Session.set("key", value)
 // 获取临时缓存
Session.get("key")
 // 移除临时缓存
Session.remove("key")
 // 移除全部临时缓存
Session.clear()
```