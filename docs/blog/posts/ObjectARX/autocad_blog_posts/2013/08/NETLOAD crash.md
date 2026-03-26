---
title: "NETLOAD crash"
date: 2013-08-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Plugin
description: "A developer reported a crash when using the NETLOAD command. Just before NETLOAD dialog should come up AutoCAD shuts down. In case of demand loadin..."
author: Autodesk
---
# NETLOAD crash

发布日期: 2013-08-01

原始链接: https://adndevblog.typepad.com/autocad/2013/08/netload-crash.html

## 文章内容

By Adam Nagy
A developer reported a crash when using the NETLOAD command. Just before NETLOAD dialog should come up AutoCAD shuts down. In case of demand loading instead of directly loading the AddIn this error happened when trying to execute a command from the AddIn:
System.ArgumentNullException: Value cannot be null.
Parameter name: key
at System.Collections.Generic.Dictionary`2.FindEntry(TKey key)
at System.Collections.Generic.Dictionary`2.TryGetValue(TKey key, TValue& value)
at Autodesk.AutoCAD.Runtime.PerDocumentCommandClass.Invoke(MethodInfo mi, Boolean bLispFunction)
at Autodesk.AutoCAD.Runtime.CommandClass.CommandThunk.Invoke()
Once the video drivers got updated on the laptop the above issues went away and everything seems to work fine now. This example is just there to show what strange issues can be caused by outdated drivers on the system.

