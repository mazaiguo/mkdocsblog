---
title: "Shared/Static CommandMethods"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "If you set your CommandMethods as normal class instance members:"
author: Autodesk
---
# Shared/Static CommandMethods

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/sharedstatic-commandmethods.html

## 文章内容

By Stephen Preston
If you set your CommandMethods as normal class instance members:
    Public Class MyCommands
    <CommandMethod("TEST")> _
    Public Sub MyCommand()
      'My code
    End Sub
  End Class
  then AutoCAD will automatically instantiate your class when your command is called in a new document. However, if you make your CommandMethod a Shared (static in C#) method, then AutoCAD can call your method without instantiating your class:
  Public Class MyCommands
    <CommandMethod("TEST")> _
    Public Shared Sub MyCommand()
      'My code
    End Sub
  End Class
  You can test this by writing a constructor for your class and watching when its called.

## 评论

**内容**: David said...
Hi Stephen,
Sorry I am not good in English , Which one is better ?
and basically what is the meaning of instantiate ?
Sorry for my low level question .
Reply
07/04/2012 at 07:31 PM

---
**内容**: Madhukar Moogala said in reply to David...
Neither is better or worse - it depends on the architecture you're implementing. I tend to use the shared/static approach for simple apps - but for no particular reason.
'Instantiate' means 'to create an instance of that class'.
Reply
07/05/2012 at 10:39 AM

---
**内容**: David said in reply to Madhukar Moogala...
Thank you Stephen
Reply
07/05/2012 at 08:14 PM

---
