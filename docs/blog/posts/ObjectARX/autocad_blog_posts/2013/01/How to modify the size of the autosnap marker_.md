---
title: "How to modify the size of the autosnap marker?"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - API
  - AutoCAD
  - AutoLISP
description: "You might wonder if there is a more straightforward way to control the Autosnap marker size without having to use DDOSNAP or OSNAP commands?"
author: Autodesk
---
# How to modify the size of the autosnap marker?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-modify-the-size-of-the-autosnap-marker.html

## 文章内容

By Gopinath Taget
You might wonder if there is a more straightforward way to control the Autosnap marker size without having to use DDOSNAP or OSNAP commands?
The size of the AutoSnap Marker is controlled by the AutoSnapSize variable. This variable is stored outside of AutoCAD, and can be accessed by using GETENV and SETENV. It's important to note that the case of the letters is important, therefore capitalize the name as shown. The following two LISP commands will retrieve the value of AutoSnapSize and then set it to 10 pixels.
(getenv "AutoSnapSize")
(setenv "AutoSnapSize" "10")

## 评论

**内容**: Emmanuel Garcia said...
Gopinath, I'm curious why System and Environment variables are treated differently when it comes to casing. System variables appear to not be case sensitive, while Environment Variables appear to require strict adherence to CamelCasing. I've always enjoyed LISP's relaxed approach to casing. ;-)
Reply
01/09/2013 at 11:43 AM

---
**内容**: Gopinath Taget said in reply to Emmanuel Garcia...
Hi Emmanuel,
By definition environment variables are "A setting stored in the operating system that controls the operation of a program". So they are not governed by AutoLisp semantics.
Cheers
Gopinath
Reply
01/16/2013 at 08:49 PM

---
**内容**: ritusharma said...
It is a time saver and I always work with it in AutoCAD.
Reply
09/21/2021 at 05:13 AM

---
**内容**: ritusharma said...
It helps in deciding the points of the objects.
Reply
09/26/2021 at 09:40 PM

---
