---
title: "Maximize or minimize AutoCAD window through automation?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "AutoCAD application can be maximized or minimized through automation by utilizing the 'WindowState' property of the Application object as shown in ..."
author: Autodesk
---
# Maximize or minimize AutoCAD window through automation?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/maximize-or-minimize-autocad-window-through-automation.html

## 文章内容

By Gopinath Taget
AutoCAD application can be maximized or minimized through automation by utilizing the 'WindowState' property of the Application object as shown in the following sample code:
'To minimize the application
Application.WindowState = acMin
  'To maximize the application
Application.WindowState = acMax
  'The window is normal (neither minimized nor maximized).
Application.WindowState = acNorm

## 评论

**内容**: Luisa said...
3D cad drafting looks complex... I've just started interior design classes and I can't wait to get out of 2D modelling but 3D drafting looks intimidating! :)
Reply
01/16/2013 at 11:55 AM

---
**内容**: JW said...
How do we navigate to this setting. The format looks like a registry entry, but I am not finding it there.
Reply
07/30/2015 at 08:10 AM

---
