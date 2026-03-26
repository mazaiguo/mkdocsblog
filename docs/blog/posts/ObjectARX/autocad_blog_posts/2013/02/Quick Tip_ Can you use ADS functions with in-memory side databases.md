---
title: "Quick Tip: Can you use ADS functions with in-memory side databases"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - DXF
  - Database
description: "Using AcDbDatabase::readDwgFile(), you read several drawings into memory. With adsentget() you try to get a resbuf of some DXF-values. But for most..."
author: Autodesk
---
# Quick Tip: Can you use ADS functions with in-memory side databases

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/quick-tip-can-you-use-ads-functions-with-in-memory-side-databases.html

## 文章内容

By Gopinath Taget
Consider this:
Using AcDbDatabase::readDwgFile(), you read several drawings into memory. With ads_entget() you try to get a resbuf of some DXF-values. But for most databases it returns NULL, while returning the correct value for some random databases. If ads-functions can be used on in-memory drawings, how do you direct the function to the correct drawing?
The short answer is, you cannot.
Some ADS functions might work with objects in other databases in some circumstances, but that is not by design. Therefore, you should not rely on of ADS style functions in such a case.
If you want to work on objects in databases that are not loaded into the AutoCAD editor, then you cannot safely use the ADS functions; you'll need to usenon-ads functions such as the methods in the various AcDb classes.

## 评论

**内容**: Tony Tanzillo said...
Temporarily setting AcDbHostApplicationServices::setWorkingDatabase to the database that contains the objects used with ads-style APIs often works.
As a matter of fact, it even works for acedSSGet("X"), with the caveat that it sets the "Previous" selection set, so you have to get rid of that before returning control to the user.
Reply
02/13/2013 at 07:31 PM

---
**内容**: Gopinath Taget said...
Hi Tony,
"often" is a dangerous word. As I mentioned, these functions are not intended to work with non-current databases. If it works, your lucky and if I does not, then "I told you so" applies.
If you do want to switch working databases, it is far more robust to switch documents itself (obtain the document associated with a database and use it) with AcApDocManager::setCurDocument. This takes care of setting the working database with the database associated with the document.
Cheers
Gopinath
Reply
02/14/2013 at 04:41 PM

---
