---
title: "Can the ObjectARX acedGetFileD() prompt for directory only?"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - C++
  - ObjectARX
  - Selection
description: "Although you can set flags to disable default file selection or to enter a new file name, the acedGetFileD() function is designed to return a quali..."
author: Autodesk
---
# Can the ObjectARX acedGetFileD() prompt for directory only?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/can-the-objectarx-acedgetfiled-prompt-for-directory-only.html

## 文章内容

By Gopinath Taget
Although you can set flags to disable default file selection or to enter a new file name, the acedGetFileD() function is designed to return a qualified file name, not just a directory. If you need to deal with paths only, you may want to use acedGetFileNavDialog().

## 评论

**内容**: Oleg said...
Hi, Gopinath,
I've tried to adopt this function in C#
but with no chance
Can you provide an appropriate code example on C#?
Kind regards,
Oleg
Reply
01/02/2013 at 09:51 AM

---
**内容**: Gopinath Taget said in reply to Oleg...
Hi Oleg,
You dont really have to rely on the ARX functions I mentioned above for .NET. You can use the Autodesk.AutoCAD.Windows.OpenFileDialog for a file dialog and control how it behaves using the Autodesk.AutoCAD.Windows.OpenFileDialog.OpenFileDialogFlags enumeration. Please look up the AutoCAD .NET documentation for more information.
Cheers
Gopinath
Reply
01/02/2013 at 06:43 PM

---
