---
title: "Changing AutoCAD OEM (and normal AutoCAD) default INSTALLDIR"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "If you want to change the default install path that AutoCAD OEM and indeed all AutoCAD installers these days prompt, then don’t look to the INSTALL..."
author: Autodesk
---
# Changing AutoCAD OEM (and normal AutoCAD) default INSTALLDIR

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/changing-autocad-oem-and-normal-autocad-default-installdir.html

## 文章内容

By Fenton Webb
If you want to change the default install path that AutoCAD OEM and indeed all AutoCAD installers these days prompt, then don’t look to the INSTALLDIR of the MSI’s themselves but the SETUP.INI file itself.
In the SETUP.INI file, simply search for the INSTALL_PATH setting and change it to what you need. Be sure to search all setup.ini files and change those also.

## 评论

**内容**: Dave JOHNSON said...
Hi,
We are on the way to use AutoCAD OEM but we discovered that the VLISP VLAX functions are not implemented. somebody was already faced with this problem and wrote some walk around ARX functions ?
Reply
02/10/2013 at 01:00 AM

---
**内容**: Fenton Webb said...
Hey Dave!
sorry, that is a limitation of LISP on OEM. I'm sure someone has done it, but we are not aware who.
Sorry about that.
Reply
02/11/2013 at 10:01 AM

---
