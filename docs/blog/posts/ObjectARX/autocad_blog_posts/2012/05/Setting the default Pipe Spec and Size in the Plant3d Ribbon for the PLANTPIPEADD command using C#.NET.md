---
title: "Setting the default Pipe Spec and Size in the Plant3d Ribbon for the PLANTPIPEADD command using C#.NET"
date: 2012-05-01
categories:
  - Plant 3D
tags:
  - .NET
  - C#
  - Plant 3D
description: "In my previous post How to obtain a list of all Pipe Specs and Sizes in Plant3d using .NET C# I spoke about the Autodesk.ProcessPower.P3dUI.UISetti..."
author: Autodesk
---
# Setting the default Pipe Spec and Size in the Plant3d Ribbon for the PLANTPIPEADD command using C#.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/setting-the-default-pipe-spec-and-size-in-the-plant3d-ribbon-for-the-plantpipeadd-command-using-cnet.html

## 文章内容

by Fenton Webb
In my previous post How to obtain a list of all Pipe Specs and Sizes in Plant3d using .NET C# I spoke about the Autodesk.ProcessPower.P3dUI.UISettings object.
If you want to control the default settings for the PLANTPIPEADD command as shown here:
Simply use the UISettings.CurrentSpec and UISettings.CurrentSize, easy

## 评论

**内容**: Artvegas said...
Hi Fenton,
I think I found a bug with your MgdDbg Tool bundle's PackageContents.xml file.
Works fine for me in 2013, but it doesn't work for me in 2012. I narrowed the issue down to the first "RuntimeRequirements" element, the one that comes before any of the "Components" elements. If I set SeriesMax to R18.2 it works in 2012. I tried a bunch of settings, and basically anything up to R18.9 is ok, so is omitting this parameter altogether.
Sorry to post this here but it seems your original post has been closed out. Thought you should know in case it is an internal implementation problem.
Original post: http://adndevblog.typepad.com/autocad/2012/04/dwg-debugger-mgddbg-app-for-autocad-20122013.html
Art
Reply
05/24/2012 at 11:20 AM

---
**内容**: Fenton Webb said...
Thanks Art.
Did you install 2012 sp1 yet?
Reply
05/24/2012 at 11:41 AM

---
**内容**: Artvegas said...
No I never installed it. Just looked at the readme file. Ahhh I see there was a SeriesMax hotfix. My bad, cheers :-)
Reply
05/24/2012 at 11:52 AM

---
**内容**: Fenton Webb said...
My pleasure! :-)
Reply
07/02/2012 at 10:49 AM

---
**内容**: Owen Wengerd said in reply to Fenton Webb...
Psst Fenton, I think that's a spam comment.
Reply
07/02/2012 at 03:19 PM

---
**内容**: Fenton Webb said...
hehehe - typical
Reply
07/02/2012 at 03:52 PM

---
**内容**: Madhukar Moogala said...
Spam comment deleted (which probably makes this comment thread look a bit weird).
These blog spammers are ever so polite, don'tcha think :-).
Reply
07/02/2012 at 07:41 PM

---
