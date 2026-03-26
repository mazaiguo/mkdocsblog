---
title: "Debugging AutoCAD 2017 using Visual Studio 2015"
date: 2016-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "At present, developers are unable to debug the .NET modules in AutoCAD 2017 with VS 2015. As explained in Kean’s article for VS 2013 http://through..."
author: Autodesk
---
# Debugging AutoCAD 2017 using Visual Studio 2015

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/debugging-autocad-2017-using-visual-studio-2015.html

## 文章内容

By Virupaksha Aithal
At present, developers are unable to debug the .NET modules in AutoCAD 2017 with VS 2015. As explained in Kean’s article for VS 2013 http://through-the-interface.typepad.com/through_the_interface/2013/11/debugging-autocad-using-visual-studio-2013.html , the workaround for this issue is to either enable the native debugging or using the Compatibility mode in VS 2015.
Turn on “Use Managed Compatibility Mode” via Tools –> Options –> Debugging.
Turn on “Enable native code debugging” from Project –> Properties –> Debug.

## 评论

**内容**: Rafael CP said...
Thnaks man... it is very useful.
Reply
11/24/2016 at 03:27 PM

---
**内容**: Mika Suorsa said...
Thank You scratching my head for some time.. this workt!
Reply
05/09/2017 at 11:01 AM

---
**内容**: Jayson said...
Very informative.
Reply
06/30/2017 at 05:41 AM

---
**内容**: Rajendra Payare said...
Thanks you very much!!
Reply
11/28/2018 at 02:49 AM

---
