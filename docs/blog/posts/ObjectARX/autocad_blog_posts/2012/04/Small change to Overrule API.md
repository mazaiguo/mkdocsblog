---
title: "Small change to Overrule API"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "I recently became aware of a change in the Overrule API. As of AutoCAD 2012, you can no longer turn overruling off using Overrule.Overruling = Fals..."
author: Autodesk
---
# Small change to Overrule API

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/small-change-to-overrule-api.html

## 文章内容

By Stephen Preston
I recently became aware of a change in the Overrule API. As of AutoCAD 2012, you can no longer turn overruling off using Overrule.Overruling = False. This change was made to prevent programmers inadvertently disabling the increasing number of AutoCAD features that make use of this API – which is sensible. To turn your custom overrules on and off, you’ll need to register and unregister your overrules with the system – using Overrule>AddOverrule() and Overrule.RemoveOverrule(). Unfortunately, this means that all the Overrule samples I wrote for my AU 2009 and 2010 classes are now outdated .
Overrules have been around since AutoCAD 2010.

## 评论

**内容**: SpeedCAD said...
Hi.
Can you give an example?
Reply
01/17/2016 at 01:22 PM

---
