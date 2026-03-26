---
title: "Did you know about this utility class?"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - C++
  - Database
description: "A very useful, yet often overlooked, utility class is Autodesk.AutoCAD.DatabaseServices.SymbolUtilityServices. It’s a placeholder class where you’l..."
author: Autodesk
---
# Did you know about this utility class?

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/did-you-know-about-this-utility-class.html

## 文章内容

By Stephen Preston
A very useful, yet often overlooked, utility class is Autodesk.AutoCAD.DatabaseServices.SymbolUtilityServices. It’s a placeholder class where you’ll find lots of useful functions for working with symbols tables (block tables, layer tables, etc.). Here’s a really short piece of (VB.NET) sample code showing how to use it:
      Dim db As Database
      Dim id As ObjectId
      db = Application.DocumentManager.MdiActiveDocument.Database
      id = SymbolUtilityServices.GetBlockModelSpaceId(db)
  Look it up in the ObjectARX helpfiles to see all the helper functions it includes.

