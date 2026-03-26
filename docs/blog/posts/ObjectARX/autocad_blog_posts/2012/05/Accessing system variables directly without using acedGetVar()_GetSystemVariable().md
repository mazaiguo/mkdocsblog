---
title: "Accessing system variables directly without using acedGetVar()/GetSystemVariable()"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "I just realized that variables like EXTMIN, EXTMAX, etc. can also be accessed directly through AcDbDatabase, so I do not need to use acedGetVar()"
author: Autodesk
---
# Accessing system variables directly without using acedGetVar()/GetSystemVariable()

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/accessing-system-variables-directly-without-using-acedgetvargetsystemvariable.html

## 文章内容

By Adam Nagy
I just realized that variables like EXTMIN, EXTMAX, etc. can also be accessed directly through AcDbDatabase, so I do not need to use acedGetVar()
Solution
Yes, that is correct.
acedGetVar() [aced = AutoCAD Editor] and Application.GetSystemVariable() enables you to access system variables that are also available for users through the AutoCAD Editor in the User Interface.
However, non-AutoCAD dependent system variables like EXTMIN, EXTMAX, UCSXDIR, etc. can also be found directly under AcDbDatabase/Database. For a complete list have a look at the AcDbDatabse methods or Database properties in the ObjectARX/.NET Reference Guide [arxdoc.chm].

