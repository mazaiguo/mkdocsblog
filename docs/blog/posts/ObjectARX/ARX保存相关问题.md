---
title: ARX保存相关问题
date: 2024-01-15
categories:
  - CAD开发
  - ObjectARX
  - 问题解决
tags:
  - ObjectARX
  - DBMOD
  - CAD保存
  - 数据库状态
description: ObjectARX开发中关于CAD图纸保存状态DBMOD的控制和处理方法
author: JerryMa
---
# 保存标记
DBMOD，只读

* //声明设置数据库模式的函数

  ```cpp
  extern long acdbSetDbmod(AcDbDatabase * pDb, long newVal); 
  ```

* 另外还有方法的，AcApDocment类有两个成员接口，pushDbmod和popDbmod

* 

