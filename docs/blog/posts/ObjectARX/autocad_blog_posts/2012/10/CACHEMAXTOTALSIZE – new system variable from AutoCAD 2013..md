---
title: "CACHEMAXTOTALSIZE – new system variable from AutoCAD 2013."
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "AutoCAD has introduced a new system variable called CACHEMAXTOTALSIZE in 2013 version. This variable sets the maximum total size of all graphics ca..."
author: Autodesk
---
# CACHEMAXTOTALSIZE – new system variable from AutoCAD 2013.

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/cachemaxtotalsize-new-system-variable-from-autocad-2013.html

## 文章内容

By Virupaksha Aithal
AutoCAD has introduced a new system variable called CACHEMAXTOTALSIZE in 2013 version. This variable sets the maximum total size of all graphics cache files saved in the local configured temporary folder for AutoCAD. The cached graphics are stored in folder C:\Users\<username>\AppData\Local\Autodesk\AutoCAD 2013 - English\R19.0\enu\GraphicsCache.
When the total size of the graphics cache files reaches the maximum, the oldest files in the cache are automatically deleted. Set this system variable to 0 to disable the graphics cache.

## 评论

**内容**: Patrick Emin said...
Hi, what's the best value for this variable? What is is designed for?
Reply
10/16/2012 at 05:24 AM

---
**内容**: R.K. McSwain said...
I'm interested in the same question that Patrick asked, above. Thanks.
Reply
06/22/2016 at 09:19 AM

---
