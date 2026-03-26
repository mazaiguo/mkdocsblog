---
title: "How to lock Block Table Records from being edited?"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
description: "It would be nice to have the ability to lock up table records like block definitions so they can't be altered. I know this can be done through the ..."
author: Autodesk
---
# How to lock Block Table Records from being edited?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/how-to-lock-block-table-records-from-being-edited.html

## 文章内容

By Philippe Leefsma
Q:
It would be nice to have the ability to lock up table records like block definitions so they can't be altered. I know this can be done through the use of reactors, but I don't want our blocks being changed when going out to a client or design firm. This would allow to keep drawing integrity better.
A:
You are correct with what you say about using reactors - without your application loaded the user can indeed modify the AcDbBlockTableRecord's.
The other way to do what you want is to create your own custom AcDbBlockTableRecord by deriving from AcDbBlockTableRecord and simply vetoing the subOpen() for write. This will work fine - unfortunately, the exception is when your custom AcDbBlockTableRecord DBX is not loaded; in this case AutoCAD does not expect to find Proxy entities residing in the AcDbBlockTable and because of this, implements no proxy support whatsoever. Obviously, without the proxy entity support trying to access the custom AcDblockTableRecord without the DLL host loaded will cause an exception.
At this time, there is no workaround.

## 评论

**内容**: Owen Wengerd said...
There is a commercial solution. CADVault also requires the recipient to install the object enabler (aka runtime), but AutoCAD won't crash if they haven't installed it.
Reply
07/18/2012 at 11:19 AM

---
**内容**: Philippe Leefsma said...
So that's the same limitation than what the post is talking about in the first place concerning reactors, without the app installed on client machines there is no way to enforce locking block records.
Reply
07/18/2012 at 01:44 PM

---
**内容**: Owen Wengerd said in reply to Philippe Leefsma...
Sorry, I should have been more clear. It's actually not the same. In the missing reactors case, you end up with a normal block definition. In the case of a vault with a missing runtime, you end up with proxy graphics.
Reply
07/18/2012 at 04:47 PM

---
