---
title: "Visual Studio 2008 for ObjectARX 2010/11/12"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - C++
  - COM
  - ObjectARX
description: "The correct version of the Visual Studio 2008 with Service Pack 1. If you use the RTM version, it will throw an acarray related error on compile: "..."
author: Autodesk
---
# Visual Studio 2008 for ObjectARX 2010/11/12

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/visual-studio-2008-for-objectarx-20101112.html

## 文章内容

By Augusto Goncalves
The correct version of the Visual Studio 2008 with Service Pack 1. If you use the RTM version, it will throw an acarray related error on compile: "fatal error C1083: Cannot open include file: 'type_traits': No such file or directory".
Additionally, it is possible use Visual Studio 2010 with Platform toolset v90, as described here.

## 评论

**内容**: xanhnhnn280683@gmail.com said...
Welcome Forum!
I have a question related to vba of AutoCad, reference your comments. Comments Reference sent to the email address: xanhnhnn280683@gmail.com thank you.
Questions:( I write mã VBA trong autocad running best, select in objects domain non empty, select the outside of objects domain Empty:)
Sub testboundary
Dim kiemtradoituong As Long, RetPoint As Variant
kiemtradoituong = ThisDrawing.ModelSpace.Count
Dim pt As Variant
pt = ThisDrawing.Utility.GetPoint(, "Select object or enter to finish")
ThisDrawing.SendCommand "-Boundary" & vbCr & pt(0) & "," & pt(1) & vbCr & vbCr
If ThisDrawing.ModelSpace.Count > kiemtradoituong Then
RetPoint = ThisDrawing.Utility.GetPoint(, " non domain Empty ")
Else
RetPoint = ThisDrawing.Utility.GetPoint(, " domain Empty ")
End If
End sub
by vb.net language that supports creating dynamic library (dll), so I make run some examples vba in autocad.( Address reference: http://through-the-interface.typepad.com/through_the_interface/2011/08/debugging-autocad-net-projects-using-express-editions.html).
when I create file dll by visual tudio 2010 (vb.net) support, the variable (Dim pt As Variant) in vba autocad, vb.net changed (Dim pt As Object) run vba autocad error, looking for help
Best regards
Reply
12/13/2012 at 08:04 AM

---
**内容**: Augusto Goncalves said in reply to xanhnhnn280683@gmail.com...
Hi,
No sure if I understood, but can you try with
Dim pt as Object()
Regards,
Augusto
Reply
12/13/2012 at 08:10 AM

---
**内容**: xanhnhnn280683@gmail.com said...
welcome Augusto!
Thanks for your attention, the truth is that it have then good run in Autocad VBA, but to vb.net autocad Dim pt As Variant variable to replace Dim pt as object, to the command of Autocad run improperly
example:
http://www.cadviet.com/forum/index.php?showtopic=68238&pid=222452&st=0&#entry222452
Reply
12/13/2012 at 10:14 AM

---
