---
title: "VBA macro compatibility in AutoCAD 2014 64-bit"
date: 2014-02-01
categories:
  - AutoCAD VBA
tags:
  - AutoCAD
  - COM
  - COM Interop
  - VBA
description: "I've been handling quite a few questions recently from customers migrating to AutoCAD 2014 64-bit from an earlier 64-bit AutoCAD version. The typic..."
author: Autodesk
---
# VBA macro compatibility in AutoCAD 2014 64-bit

发布日期: 2014-02-01

原始链接: https://adndevblog.typepad.com/autocad/2014/02/vba-macro-compatibility-in-autocad-2014-64-bit.html

## 文章内容

By Stephen Preston
I've been handling quite a few questions recently from customers migrating to AutoCAD 2014 64-bit from an earlier 64-bit AutoCAD version. The typical problem is something like this:
My VBA macro is referencing some additional OCX control or Type Library. It worked fine on AutoCAD 64-bit versions prior to AutoCAD 2014. But now my macro generates an error related to that Type Library or OCX control.
The explanation for this is that AutoCAD 2014 is the first AutoCAD release to use Microsoft's newer VBA 7.1 engine, where older AutoCAD versions used the VBA 6.3 engine. VBA 6.3 was available as a 32-bit component only. VBA 7.1 is available as 32-bit and 64-bit components - and (as you'd expect) AutoCAD 2014 64-bit uses the 64-bit component. Your Type Library/OCX control can't be loaded because it is a 32-bit component. It is impossible to load any 32-bit component into a 64-bit process space. This is the reason for your error.
In order to make your macro work again, you must replace your 32-bit component with a 64-bit version - or refactor your project to use an alternative if the vendor of that component doesn't provide a 64-bit version.
The reason the same VBA macro worked in older AutoCAD 64-bit versions is because AutoCAD launched VBA 6.3 in a separate (32-bit) process to which AutoCAD marshals its COM calls. So, although AutoCAD was running 64-bit native, the VBA engine was still a 32-bit process and could happily load 32-bit components.
VBA being run in a separate process like this is also the reason why VBA macros used to be about 30 times slower running in AutoCAD 64-bit compared to AutoCAD 32-bit. The new VBA 7.1 engine fixes that problem for AutoCAD 2014 64-bit.

## 评论

**内容**: Nick Hall said...
Stephen
One thing that definitely doesn't work is the MS Calendar Control OCX. To get round this I modified the VBA Calendar Control from here
https://sites.google.com/site/e90e50/calendar-control-class
It only took about 30 minutes to get a date picker working, much less time than I spent tracking down the 32/64 bit OCX issue.
Reply
03/13/2014 at 05:55 AM

---
**内容**: Madhukar Moogala said in reply to Nick Hall...
Thanks for the helpful link Nick.
Reply
03/13/2014 at 06:34 AM

---
**内容**: Ricardo Cuan said...
In the 7.1 version of VBA I have trouble connecting a BD access 97.
What connection string should I use? and I should have installed?
Reply
04/11/2014 at 03:05 PM

---
**内容**: nisar said...
dear sir,could you help me to install the macros in autocad to export and import the survey conrdinates.please let me know ,how to down load the macros
Reply
01/10/2015 at 06:44 AM

---
