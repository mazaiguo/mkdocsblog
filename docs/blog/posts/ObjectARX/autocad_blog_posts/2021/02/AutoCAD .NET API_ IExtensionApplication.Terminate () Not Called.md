---
title: "AutoCAD .NET API: IExtensionApplication.Terminate () Not Called"
date: 2021-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Plugin
description: "I am creating and running an add-in application with the AutoCAD .NET API, but after applying the AutoCAD 2020.1 Update, IExtensionApplication.Term..."
author: Autodesk
---
# AutoCAD .NET API: IExtensionApplication.Terminate () Not Called

发布日期: 2021-02-01

原始链接: https://adndevblog.typepad.com/autocad/2021/02/autocad-net-api-iextensionapplicationterminate-not-called.html

## 文章内容

Issue
I am creating and running an add-in application with the AutoCAD .NET API, but after applying the AutoCAD 2020.1 Update, IExtensionApplication.Terminate() is no longer called. 
The same is true for AutoCAD 2020.1.2 Update and AutoCAD 2021 including all updates.
Was there a specification change?
Solution
The new feature add-in Save to Autodesk Web and Mobile introduced in AutoCAD is conflicting with other plugins unloading mechanism.
We have two solutions to fix this -
If you are not using the SAVETOWEBMOBILE command, uninstalling the Save to Autodesk Web and Mobile add-in from the Windows Control Panel.
If you are using then enter the command SAVETOWEBMOBILE on AutoCAD Command Line Interface, it will pop up for update.
Please go ahead and update.

## 评论

**内容**: Súhi said...
"Was there a specification change?" https://webecomewhatwebehold.online I think this is inevitable. But maybe not much.
Reply
11/20/2022 at 08:16 PM

---
