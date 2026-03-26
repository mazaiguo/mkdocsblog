---
title: "“Nothing to Redo” message appears straight after UNDOing in AutoCAD for .NET and ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "I wonder how many people have this issue?"
author: Autodesk
---
# “Nothing to Redo” message appears straight after UNDOing in AutoCAD for .NET and ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/nothing-to-redo-message-appears-straight-after-undoing-in-autocad-for-net-and-objectarx.html

## 文章内容

by Fenton Webb
I wonder how many people have this issue?
A message appears when running the REDO command in AutoCAD straight after running the UNDO command… There’s a relatively simple explanation as to why this is happening.
In short, calling StartTransaction() or opening anything for kForWrite whenever UNDO or REDO is occurring will cause this issue to happen.
A lot of developers want to make special updates to objects while AutoCAD is running commands, perhaps they want to relink interconnecting entities, update parts schedules or move objects in relation to others.
Some examples of places where they might run this type of update code are:
In a CommandEnded event or reactor notification
In an ObjectModified, ObjectAppended, etc. event or reactor notification
In a Overrule or Custom entity callback
any other event or reactor notification
The problem stems from the fact that when you run the UNDO or REDO commands inside of AutoCAD, those commands also invoke the same callback mechanisms that all of the other normal commands do.
If that happens, and you call StartTransaction() or you open something for kForWrite from within one of those callback mechanisms, the REDO will fail. The reason is that StartTransaction() and kForWrite both initialize the UNDO filing system, and if you do that initialization while UNDO or REDO is happening then you trash the UNDO filer.
Here’s some tips on how to operate on entities from within these events or reactor notifications:
Don’t use StartTransaction(), simply calling this function while UNDO or REDO is running will blitz the UNDO filer – instead call StartOpenCloseTransaction() or use Open(kForRead).
Opening something for kForRead is fine, even when UNDOing, so you can safely record any updates that are happening in your own buffers.
There’s no need to update anything while the UNDO or REDO is happening – why? Because the UNDO and REDO will restore it for you anyway…
So what are our options…
In a CommandEnded event or reactor notification
you just need to make sure that UNDO and/or REDO is not happening by testing the command string that is passed to the event callback.
In an ObjectModified, ObjectAppended, etc event or reactor notification
you can test the entity that is passed to see if the IsUndoing property is set to true, if it is, do nothing.
In a Overrule or Custom entity callback
simply testing the host (this or me) object to see if the callback is occurring with IsUndoing is set to true, if it is, do nothing.

## 评论

**内容**: David said...
Hello Fenton.
That was a great tip. I was dealing with this in our company and told users " That is the way it should be ".
Shame on Me , I really thought so.
Thanks,
I am going to give my users the REDO , back.
Reply
11/30/2012 at 10:27 PM

---
**内容**: Paul said...
Hi Fenton,
I know this is quite old now, but I have a problem when overruling subGetGripPointsAt() in a custom entity (the code just increments a point3d property). When the .NET overrule is enabled UNDO and REDO stop working. The same c++ property is being modified in both cases.
Reply
03/06/2015 at 06:21 AM

---
