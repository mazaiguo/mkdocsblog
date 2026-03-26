---
title: "Introduction to RealDWG .Net Programming"
date: 2015-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - DWG
description: "My colleague Adam Nagy had created an nice video recording back in 2008 on "Introduction to RealDWG .Net programming". You can download the recordi..."
author: Autodesk
---
# Introduction to RealDWG .Net Programming

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/introduction-to-realdwg-net-programming.html

## 文章内容

By Balaji Ramamoorthy
My colleague Adam Nagy had created an nice video recording back in 2008 on "Introduction to RealDWG .Net programming". You can download the recording here
DevTV on RealDWG programming
Here is another recording with the same sample project. The changes are mainly in the installer creation and in the licensing steps which have changed since the last recording was created.
The sample project and the slides can be downloaded here :
SampleCode_DevTV

## 评论

**内容**: CAD bloke said...
Where on earth does one get "Microsoft_VC110_MFC_x64.msm" and "Microsoft_VC110_MFCLOC_x64.msm" if they even the right ones for RealDwg 2016? I have to say the process of building an installer for RealDwg is the most half-baked, infuriating process I have ever paid (a lot) for.
Reply
01/23/2016 at 03:30 AM

---
**内容**: CAD bloke said...
Solved. So I just did what anyone would do, fired up a Windows 7 x64 VM I had lying around, installed a Visual Studio 2012 Ultimate I had lying around and waited for the files to appear in the right place. You all have these things conveniently lying around, right? Or you are working with a version of Visual Studio that is 3 generations behind, right?
Don't forget to tick the box for "Visual C++ MFC class libraries" in the installation options or the MFC dlls won' appear.
Reply
01/23/2016 at 01:30 PM

---
**内容**: CAD bloke said...
This sample is not out of date for RealDwg 2017. More significantly, there is nothing even remotely as useful as this included with RealDwg. Why not?
Reply
04/15/2016 at 04:30 AM

---
**内容**: Joel Martins said in reply to CAD bloke...
can you tell me how to install realdwg?
Reply
10/24/2022 at 07:36 AM

---
**内容**: Kevin Kim said...
Hi Balaji,
I downloaded sample application(SsmpleCode_DevTV).
I complied and made an Wix installer for this sample code. But after installing this on my test fresh win7 computer with .netframework 4.5, it crashed and won’t work. though it works on my development computer.
I need your support to make it work.
Kevin Kim
Reply
06/01/2017 at 11:19 AM

---
**内容**: Aleksandr Konstantinov said...
What is a purpose of assigning new database to HostApplicationServices::WorkingDatabase? I tried to skip that and code seems to still work. And if it is required then how multiple databases are supposed to be handled in parallel?
Reply
08/02/2021 at 09:10 AM

---
