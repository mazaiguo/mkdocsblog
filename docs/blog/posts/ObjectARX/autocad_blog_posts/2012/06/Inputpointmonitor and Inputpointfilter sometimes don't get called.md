---
title: "Inputpointmonitor and Inputpointfilter sometimes don't get called"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "If you uncheck the "Display Hyperlink Cursor and Shortcut menu" item on the User Preferences page of the Options dialog, your input point monitors ..."
author: Autodesk
---
# Inputpointmonitor and Inputpointfilter sometimes don't get called

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/inputpointmonitor-and-inputpointfilter-sometimes-dont-get-called.html

## 文章内容

By Gopinath Taget
If you uncheck the "Display Hyperlink Cursor and Shortcut menu" item on the User Preferences page of the Options dialog, your input point monitors and filters might not receive notifications. How can you force them to be called in this situation?
To work around this problem, you will have to invoke the AcEdInputPointManager::turnOnForcedPick() method of your global input point manager. This is demonstrated in the cmdForcedPickOn() function of the inputpoint sample in the ObjectARX SDK.

