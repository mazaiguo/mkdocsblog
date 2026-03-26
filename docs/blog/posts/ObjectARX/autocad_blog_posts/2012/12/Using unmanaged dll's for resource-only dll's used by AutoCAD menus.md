---
title: "Using unmanaged dll's for resource-only dll's used by AutoCAD menus"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
description: "Is there a way to build a resource-only DLL for an AutoCAD menu using Visual Studio?"
author: Autodesk
---
# Using unmanaged dll's for resource-only dll's used by AutoCAD menus

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/using-unmanaged-dlls-for-resource-only-dlls-used-by-autocad-menus.html

## 文章内容

By Philippe Leefsma
Q:
Is there a way to build a resource-only DLL for an AutoCAD menu using Visual Studio? 
A:
A resource-only dll for an AutoCAD menu needs to be created as an unmanaged dll. To create a resource-only dll as an unmanaged dll, use a C++ dll project. In File->New Project, choose win32 project and then choose a "dll".  You can then add your bitmaps into the resource section. The attached zip file has an example.
ResDll.zip

## 评论

**内容**: CanopenR said...
This works, except when i copy the button to another menu.
So i create a custom menu and dll. I then load that menu as a partial menu (all works).
I then create a toolbar/panel and copy one of the button in my custom menu file to my new toolbar/panel . the button works fine, but the image is lost.
Any ideal why the new toolar\panel can't see the image once it copied out sides it menu?
PS. this same thing work fine wth Acad menu ideals..
Reply
12/10/2012 at 02:59 PM

---
