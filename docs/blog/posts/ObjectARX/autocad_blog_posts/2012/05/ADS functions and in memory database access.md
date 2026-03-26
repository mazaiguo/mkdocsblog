---
title: "ADS functions and in memory database access"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Database
description: "Some of you might have tried using ADS functions like adsentget() on in-memory drawings opened as side databases using AcDbDatabase::readDwgFile() ..."
author: Autodesk
---
# ADS functions and in memory database access

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/ads-functions-and-in-memory-database-access.html

## 文章内容

By Gopinath Taget
Some of you might have tried using ADS functions like ads_entget() on in-memory drawings opened as side databases using AcDbDatabase::readDwgFile() and find that it returns NULL for some drawings and correct values for others. So is it safe to use ads functions on in-memory drawings opened as a side database?
The short answer is “no”. In recent versions of AutoCAD (from AutoCAD 2000 and up), ADS functions assume you are working with the current document's database. This is different from earlier versions where ADS functions only work with the drawing currently loaded in the AutoCAD editor. The subtlety here is that the “current” document is not necessarily the same as the document of the drawing visible in the editor.
The result (of this change in AutoCAD 2000 and up) is that for recent versions of AutoCAD, some ADS functions might work with objects in side databases in some circumstances, but that is not by design.Therefore, you should not rely on of ADS for side databases.
If you want to work on objects in side databases you'll need to use non-ads functions such as the methods in the various AcDb classes.

## 评论

**内容**: petcon said...
so no ads funcions in readdwg?
Reply
05/16/2012 at 09:44 PM

---
**内容**: Gopinath Taget said...
Hi Petcon,
You can use the ads_* defined in the RealDWG SDK. Some ads_*symbols defined in the header:
#define ads_entdel acdbEntDel
#define ads_entgetx acdbEntGetX
#define ads_entget acdbEntGet
#define ads_entlast acdbEntLast
#define ads_entnext acdbEntNext
Please check the RealDWG headers for more details.
Cheers
Gopinath
Reply
05/16/2012 at 10:02 PM

---
**内容**: petcon said...
where is the realdwg?
Reply
05/17/2012 at 03:27 AM

---
**内容**: Gopinath Taget said...
Hi Petcon,
I dont get the question. Are you looking for a place to download RealDWG from? Please visit the Autodesk website www.autodesk.com/realdwg for how you can obtain it.
Thanks
Gopinath
Reply
05/17/2012 at 12:26 PM

---
