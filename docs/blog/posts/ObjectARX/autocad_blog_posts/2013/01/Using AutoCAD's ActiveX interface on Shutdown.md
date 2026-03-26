---
title: "Using AutoCAD's ActiveX interface on Shutdown"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM
  - ObjectARX
description: "When accessing the ActiveX interface of AutoCAD in an ObjectARX application, we may try use the IAcadApplication and IAcadPreferences interfaces to..."
author: Autodesk
---
# Using AutoCAD's ActiveX interface on Shutdown

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/using-autocads-activex-interface-on-shutdown.html

## 文章内容

By Augusto Goncalves
When accessing the ActiveX interface of AutoCAD in an ObjectARX application, we may try use the IAcadApplication and IAcadPreferences interfaces to set a user profile at AutoCAD startup and shutdown.
Consider the scenario: on the AcRx::kInitAppMsg it is stored the actual user profile and set another profile. On AcRx::kUnloadAppMsg we may want to restore the previous profile. It's not a problem to set the profile on kInitAppMsg, but on kUnloadAppMsg I'm not able to get the active AutoCAD ActiveX object using GetActiveObject(). The call to GetActiveObject() returns MK_E_UNAVAILABLE instead of S_OK.
The problem is that AutoCAD unregisters its ActiveX application object before unloading the ObjectARX modules; therefore, we cannot access AutoCAD's ActiveX interface on the kUnloadAppMsg notification. The kPreQuitMsg doesn't work, either.
When AutoCAD quits, it performs the following steps:
1. Unregisters the ActiveX application object (removes it from the running object table).
2. Sends kPreQuitMsg to every loaded ObjectARX application.
3. Sends kUnloadAppMsg to every ObjectARX application before unloading them.
Therefore, you cannot use AutoCAD's ActiveX interface on kUnloadAppMsg. You can work around this by using a reactor. You could react on the AcEditorReactor::databaseToBeDestroyed() notification, but the result of this is that you will reset the profile every time the user loads or creates a new drawing, so you have to set your profile when a new drawing is loaded or created.

