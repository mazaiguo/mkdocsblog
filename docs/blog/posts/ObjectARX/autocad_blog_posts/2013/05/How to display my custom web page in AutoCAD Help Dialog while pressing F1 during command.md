---
title: "How to display my custom web page in AutoCAD Help Dialog while pressing F1 during command"
date: 2013-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
description: "There is one particular whitelist in AutoCAD concerning online help. Only the domains on the list will be accepted by help browser, and the others ..."
author: Autodesk
---
# How to display my custom web page in AutoCAD Help Dialog while pressing F1 during command

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/how-to-display-my-custom-web-page-in-autocad-help-dialog-while-pressing-f1-during-command.html

## 文章内容

By Philippe Leefsma
There is one particular whitelist in AutoCAD concerning online help. Only the domains on the list will be accepted by help browser, and the others will be forwarded to system default browser.
This white list is hardcoded in 2013, but in the 2014, developers can now create below registry key to add their own domain into it. The default value of this key is “autodesk.com”.
HKLM\SOFTWARE\Autodesk\AutoCAD\RXX.X\ACAD-XXX:XXX\SupportedUrls = "autodesk.com, mycustomdomain.com"
    Here is the VB.Net code:
<CommandMethod("MyHelp",
   "InvokeHelpWeb",
   Nothing,
   CommandFlags.Transparent,
   Nothing,
   "http://adndevblog.typepad.com/autocad/",
   "")> _
Public Shared Sub InvokeHelpWeb2()
    Dim doc As Document =
Application.DocumentManager.MdiActiveDocument
      'Press F1 while prompted to input value
    doc.Editor.GetDouble("Get Double:")
  End Sub
-

## 评论

**内容**: Gaetano said...
Why is not shown in my AutoCAD Map 3D 2014 (..\R19.1\ACAD-D002:409)? Can I add it?
Reply
05/28/2013 at 02:38 AM

---
**内容**: Philippe said in reply to Gaetano...
Hi Gaetano, this is working for me on Acad Mechanical 2014. Are you sure you created the correct reg key at the right place? I will ask a colleague with Map 2014 to test it...
Reply
05/29/2013 at 01:41 AM

---
**内容**: Cado Magenge said...
That’s pretty cool, thanks
Reply
05/04/2015 at 12:07 AM

---
