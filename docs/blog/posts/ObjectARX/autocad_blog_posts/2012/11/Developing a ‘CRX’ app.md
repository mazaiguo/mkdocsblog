---
title: "Developing a ‘CRX’ app"
date: 2012-11-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "We’ve received a few common questions recently from developers using AcCoreConsole (which Balaji blogged about here, and Kean here). Here are the t..."
author: Autodesk
---
# Developing a ‘CRX’ app

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/developing-a-crx-app.html

## 文章内容

By Stephen Preston
We’ve received a few common questions recently from developers using AcCoreConsole (which Balaji blogged about here, and Kean here). Here are the two questions (and answers kindly provided by a member of our AutoCAD development team) …
  Q1: What ObjectARX libraries can I link to for my DLL to load in to AcCoreConsole (or other ‘AcCore enabled’ product that Autodesk may ship in the future)?
A1: Here’s the list of libs that you can link with when you are developing an ARX, CRX or DBX app -
LIBRARY
OK in DBX
OK in CRX
OK in ARX
ac1st19.lib
YES
YES
YES
acdb19.lib
YES
YES
YES
acdbmgd.lib
YES
YES
YES
AcDbPointCloudObj.lib
YES
YES
YES
acge19.lib
YES
YES
YES
acgiapi.lib
YES
YES
YES
acismobj19.lib
YES
YES
YES
AcMPolygonObj19.lib
YES
YES
YES
AcSceneOE.lib
YES
YES
YES
axdb.lib
YES
YES
YES
rxapi.lib
YES
YES
YES
acbr19.lib
YES
YES
YES
acgex19.lib
YES
YES
YES
AdImaging.lib
YES
YES
YES
AdIntImgServices.lib
YES
YES
YES
AecModeler.lib
YES
YES
YES
AsdkHlrApi19.lib
YES
YES
YES
acapp_crx.lib
NO
YES
YES
AcCamera.lib
NO
YES
YES
accore.lib
NO
YES
YES
AcFdEval.lib
NO
YES
YES
AcPublish_crx.lib
NO
YES
YES
acad.lib
NO
NO
YES
acapp.lib
NO
NO
YES
AcFdUi.lib
NO
NO
YES
acModelDocObj.lib
NO
NO
YES
AcTc.lib
NO
NO
YES
AcTcUi.lib
NO
NO
YES
acui19.lib
NO
NO
YES
AdApplicationFrame.lib
NO
NO
YES
adui19.lib
NO
NO
YES
aNav.lib
NO
NO
YES
aseapi19.lib
NO
NO
YES
asiapi19.lib
NO
NO
YES
Checking a .NET DLL is easier – you just remove the reference to AcMgd.dll.
  Q2: How do I register my CRX app for demand loading (e.g. on command invocation)?
A2: You register them exactly as you would for an AutoCAD app. The only difference is that AcCoreConsole will not load an ObjectARX DLL with the extension ‘ARX’. You have to rename the extension to ‘CRX’.

## 评论

**内容**: Loic said...
Hi Preston,
This post is pretty old, so, sorry for the delay!
My application is made of about 40 arx (20 dbx) and I've just begin my "application-split" (on acad 2015).
I'd like to share a few stuff I've experienced to (I hope) complete this post (random remarks):
- crx applications are compatible with OEM - tested on OEM 2015 (BindArx option has to be checked in oemmakewizard)
- I've hugely used dependency walker to identify actual __direct__ function calls from my modules to any of modules you've listed in this post (I actually only had dependencies to acad, acui20 and adui20). This helped me to identify code sections that were purely arx (vs crx)
- Having my own arx modules dependency graph essential to define the best order of "migration"
- Some arx I had were eligible to be moved to crx without any code modification (no dependencies found)
I haven't finished the split yet but for now I found it quite straightforward despite there is a real lack of documentation.
It's probably too late to post these comments since I guess all who would have been interested in accore features (batch) have probably migrated already...
my two cents.
Reply
12/23/2014 at 02:54 AM

---
