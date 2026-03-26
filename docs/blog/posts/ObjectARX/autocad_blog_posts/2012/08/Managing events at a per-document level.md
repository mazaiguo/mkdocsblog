---
title: "Managing events at a per-document level"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
description: "I need to keep track of events such as Database.ObjectAppended, Database.ObjectModified at a per-document level for all documents opened, created a..."
author: Autodesk
---
# Managing events at a per-document level

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/managing-events-at-a-per-document-level.html

## 文章内容

By Philippe Leefsma
Q:
I need to keep track of events such as Database.ObjectAppended, Database.ObjectModified at a per-document level for all documents opened, created and existing in AutoCAD.
What is the best way to achieve this through the .Net API?
A:
The attached VB.Net sample illustrates how to achieve this:
The idea is to create a custom class, called PerDocController in my example, that will be responsible for holding the events at a per-document level.
The command class is then holding a dictionary of <Document, PerDocController> pairs for each loaded document.
The events DocumentActivated and DocumentToBeDestroyed are then used to keep this dictionary up-to-date.
The complete code is provided in the attached project.
_perdocmanagervbnet.zip

## 评论

**内容**: David said...
Thanks Good Sample
Reply
09/28/2012 at 09:50 AM

---
