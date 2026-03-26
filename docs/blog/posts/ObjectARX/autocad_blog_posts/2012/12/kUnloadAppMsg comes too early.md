---
title: "kUnloadAppMsg comes too early"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DWG
  - Database
  - ObjectARX
description: "How do we do some cleanup when my application is unloaded, such as closing database connections? The kUnloadAppMsg comes too early: my custom entit..."
author: Autodesk
---
# kUnloadAppMsg comes too early

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/kunloadappmsg-comes-too-early.html

## 文章内容

By Augusto Goncalves
How do we do some cleanup when my application is unloaded, such as closing database connections? The kUnloadAppMsg comes too early: my custom entities need this connection during dwgOutFields and kUnloadAppMsg is sent before the custom entities are saved.
Actually the application is not unloaded before the custom objects are all saved - it is only the kUnloadAppMsg that comes too early. The solution is to use some other code that can be executed when the ARX is being unloaded. The easiest place is the destructor of a global object. DLL files written in C++ construct their global class variables as the first thing when the DLL is loaded and destruct these variables just before the DLL is unloaded from memory.
Therefore, one solution is to have something like the following code in your ARX application:
class CLoadUnload
{
  CLoadUnload()
  {
    //this will be called during loading
  }
  ~CLoadUnload()
  {
    //this will be called just before unloading
    //long after kUnloadAppMsg - add any clean-up code here
  }
  }
//declare a global instance of this class in your ARX
CLoadUnload gTheWatcher;

