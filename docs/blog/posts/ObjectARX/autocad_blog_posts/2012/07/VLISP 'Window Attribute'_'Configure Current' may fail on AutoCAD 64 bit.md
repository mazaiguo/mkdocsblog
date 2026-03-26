---
title: "VLISP 'Window Attribute'>'Configure Current' may fail on AutoCAD 64 bit"
date: 2012-07-01
categories:
  - Civil 3D
tags:
  - AutoCAD
  - AutoLISP
  - Civil 3D
description: "The option to configure VLISP editor color under menu 'Window Attribute'>'Configure Current' fail on AutoCAD 64 bit. The workaround if configure th..."
author: Autodesk
---
# VLISP 'Window Attribute'>'Configure Current' may fail on AutoCAD 64 bit

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/vlisp-window-attributeconfigure-current-may-fail-on-autocad-64-bit.html

## 文章内容

By Augusto Goncalves
The option to configure VLISP editor color under menu 'Window Attribute'>'Configure Current' fail on AutoCAD 64 bit. The workaround if configure the colors on a 32 bit platform, then copy the configuration file to the 64 bit machine. This config file is located at the following folder:
AutoCAD 2012
C:\Users\<<USER_NAME>>\AppData\Roaming\Autodesk\AutoCAD 2012\R18.2\enu\VLIDE.DSK
If you have another version of AutoCAD, change the 2012 and 18.2 number on the path. If you are using a vertical product, the file is located at the application folder, below is the path on Civil 3D:
Civil 3D 2012
C:\Users\<<USER_NAME>>\AppData\Roaming\Autodesk\C3D 2012\enu\VLIDE.DSK
If the file is not at this location, first go to the VLISP editor and change some colors, then close AutoCAD and the file will be created.

## 评论

**内容**: RenderMan said...
FWIW -
This was posted back on August 9, 2011:
Hacking Visual Lisp IDE to be a little more awesome!
~RM
You can also find your answers at TheSwamp
Reply
07/14/2012 at 01:01 PM

---
**内容**: Augusto Goncalves said in reply to RenderMan...
Thanks for pointing another source, it's the same idea.
Regards,
Augusto Goncalves
Reply
07/16/2012 at 06:14 AM

---
**内容**: RenderMan said in reply to Augusto Goncalves...
You're welcome, Augusto.
Just wanted to share that link, as it was posted almost a year earlier. ;)
In any event... Have you any idea when Autodesk is going to _actually_ fix this (or other) problem(s) with VLIDE, rather than asking users to fix this themselves on another computer?
Most of us only have one 64Bit work computer, and do not have a spare 32Bit machine sitting around with a valid license of AutoCAD installed. Just saying.
Thanks,
~RM
Reply
07/16/2012 at 07:36 AM

---
**内容**: Darrin Maidlow said in reply to RenderMan...
Thanks for pointing out my post RM. I appreciate that! This seems to have been corrected in AutoCAD 2013 x64 - at least in Vanilla.. Don't have a 2013 based vertical installed right now though.
Reply
08/07/2012 at 03:10 PM

---
