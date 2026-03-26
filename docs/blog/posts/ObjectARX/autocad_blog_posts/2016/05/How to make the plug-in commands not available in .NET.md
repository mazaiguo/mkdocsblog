---
title: "How to make the plug-in commands not available in .NET"
date: 2016-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Plugin
description: "Question: Recently I received a question on how to avoid exposing commands in the custom plug-in when the license verification fails."
author: Autodesk
---
# How to make the plug-in commands not available in .NET

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/how-to-make-the-plug-in-commands-not-available-in-net-.html

## 文章内容

By Virupaksha Aithal
Question: Recently I received a question on how to avoid exposing commands in the custom plug-in when the license verification fails.
Answer: One of the procedure to achieve this requirement is to do license verification in IExtensionApplication.Initialize() and throwing an exception if license verification fails. After throwing exception, none of the commands in plug-in will be available for the user.
void IExtensionApplication.Initialize()
{
    //your check...

    //throw LoadFailed error...
    throw new Autodesk.AutoCAD.Runtime.Exception(
        Autodesk.AutoCAD.Runtime.ErrorStatus.LoadFailed);
}

## 评论

**内容**: Charles Ndung'u said...
Thanks for the infomation
Reply
07/10/2016 at 12:41 AM

---
**内容**: Sun Son said...
Dear Sir,
I have just signed for ADN membership and I would like to be a ACAD.net api developer using
ACAD.net API.
I am very beginner for the both the Visual basic 2010 express and the Autocad.net api,
when I try with “My first plug-in” the “Autocad plug-in” is not appear after I clicked
New project – Visual Basic in the Installed Templates in both the Visual basic 2010 express
and Visual studio 2015 express which are just downloaded and tried respectively,
it means those are never used with autocad 2014 installed in my computer.
Which work should I do first and which files do I need?
Any material for the plug-in you recommend?
Your kind instruction would be highly appreciated.
Thanks and Regards,
Sun, Son from Seoul, Korea
My E-mail : sonsun@sunyang.co.kr

Reply
07/10/2016 at 03:54 AM

---
