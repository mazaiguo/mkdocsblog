---
title: "Migrating ObjectARX and .NET plug-ins to AutoCAD 2013"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
  - Plugin
description: "Here are two videos documenting the simple steps required to migrate your AutoCAD ObjectARX and .NET plug-ins to AutoCAD 2013. The videos were reco..."
author: Autodesk
---
# Migrating ObjectARX and .NET plug-ins to AutoCAD 2013

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/migrating-objectarx-and-net-plug-ins-to-autocad-2013.html

## 文章内容

By Stephen Preston
Here are two videos documenting the simple steps required to migrate your AutoCAD ObjectARX and .NET plug-ins to AutoCAD 2013. The videos were recorded for the benefit of our Autodesk Developer Network partners during the Beta cycle, which means you’ll see/hear references to AutoCAD ‘Jaws’. Jaws was the codename for AutoCAD 2013 during development, so just substitute ‘2013’ every time you see/hear the word ‘Jaws’.
Download the videos from the following links, extract the files from the zip, and click in the HTML or MP4 file to play the video.
ObjectARX Migration – recorded by Fenton Webb. (Includes an AutoCAD 2013 version of the Visual Teefy project migration wizard).
.NET Migration – recorded by Stephen Preston
Update (May 29th 2012): See this post for a clarification of the use of extension methods in AutoCAD 2013.

## 评论

**内容**: Nikolay Poleshchuk said...
Stephen, Fenton recommends to include "sdkddkver.h" but I cannot find it.
Reply
04/19/2012 at 06:18 AM

---
**内容**: Fenton Webb said...
The documentation for this subject can be found here... http://msdn.microsoft.com/en-us/library/aa383745(v=vs.85).aspx
Actually, I have the Windows 7 SDK installed and that contains the header, once you have installed the SDK, you will find it in this folder C:\Program Files (x86)\Microsoft SDKs\Windows\v7.0A\Include
Reply
04/19/2012 at 11:24 AM

---
**内容**: Kerry Brown said...

Thanks for the migration info Stephen.
The NET Migration video references Jim Awe's MgdDbg Program. Is the migrated version you worked on available for download in source solution?
Regards
Kerry
Reply
04/20/2012 at 08:31 PM

---
**内容**: Madhukar Moogala said...
Hi Kerry,
I promise we'll post that very soon. Fenton is just wrapping it up in an Autoloader bundle.
Cheers,
Stephen
Reply
04/23/2012 at 10:41 AM

---
**内容**: Madhukar Moogala said...
Its here - http://adndevblog.typepad.com/autocad/2012/04/dwg-debugger-mgddbg-app-for-autocad-20122013.html
Reply
04/23/2012 at 04:36 PM

---
**内容**: Kerry Brown said...

Thanks Stephen
Regards
Reply
04/25/2012 at 12:51 AM

---
**内容**: imvivs said...
Hi Stephen, Thanks for this post.
Here is one question for you:
I have ObjectARX-2005 project for AutoCAD-2005, now I want to migrate it to ObjectARX-2014 for AutoCAD-2014, so the migration process will be the same using VisualTeefy for 2010(in mentioned Video) or it will different, if it is different then can you please provide me the process/methods to migrate?
Thanks,
Vivs
Reply
11/21/2013 at 10:43 AM

---
**内容**: Virupaksha Aithal said in reply to imvivs...
Hi Vivs,
This migration video is specifically for migrations of apps from ObjectARX 2012 to ObjectARX 2013. So, I am sure you need much more then what this video shows. My suggestion is to post your specific issue in http://forums.autodesk.com/t5/Autodesk-ObjectARX/bd-p/34
Reply
11/27/2013 at 12:55 AM

---
**内容**: imvivs said in reply to Virupaksha Aithal...
Thanks, I will post my issue in provided link.
Reply
11/27/2013 at 05:11 AM

---
**内容**: imvivs said...
My Visual Studio 2010 Conversion Wizard is stopped working (Not Responding) while loading the ObjectARX 2007 sample project(clonenod_dg), How to fix this problem?
Reply
11/22/2013 at 10:52 AM

---
