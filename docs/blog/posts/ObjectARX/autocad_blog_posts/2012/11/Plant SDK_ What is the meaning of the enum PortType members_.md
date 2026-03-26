---
title: "Plant SDK: What is the meaning of the enum PortType members?"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Several methods in the Plant SDK accept a parameter, which type is enum PortType. What do the members of this enumeration mean?"
author: Autodesk
---
# Plant SDK: What is the meaning of the enum PortType members?

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/plant-sdk-what-is-the-meaning-of-the-enum-porttype-members.html

## 文章内容

By Marat Mirgaleev
Issue
Several methods in the Plant SDK accept a parameter, which type is enum PortType. What do the members of this enumeration mean?
Solution
This enum has the following members:
  public enum PortType
  {
    Static   = 0x01,
    Dynamic  = 0x02,
    Both     = 0x03,
    Symbolic = 0x04,
    All      = 0x07,
  }
Static ports are defined by the object, i.e. an object has predefined ports that do not change.
Dynamic ports are defined by a user at run-time. These ports may move around, be deleted, etc. For example, if you drill a hole in a pipe and run a new pipe into hole with a weld.
Both means to fetch static and dynamic ports.
Symbolic are special ports used only by Isometric symbols. The main difference here is that no connector entity is used between the pipe fitting and the isometric object. It’s a symbolic port to get desired connection behavior but not truly a port as the model is concerned.
All means static, dynamic, and symbolic ports.

