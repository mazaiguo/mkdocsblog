---
title: "Creating a Rectangular RevCloud using acedCommandS"
date: 2015-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When running the RevCloud command from a script or using acedCommandS, the options presented in AutoCAD's command window did not match the options ..."
author: Autodesk
---
# Creating a Rectangular RevCloud using acedCommandS

发布日期: 2015-10-01

原始链接: https://adndevblog.typepad.com/autocad/2015/10/creating-a-rectangular-revcloud-using-acedcommands.html

## 文章内容

By Balaji Ramamoorthy
When running the _RevCloud command from a script or using acedCommandS, the options presented in AutoCAD's command window did not match the options that one gets when running _RevCloud command in AutoCAD UI. The option to set the Revcloud type was not appearing when invoked from acedCommandS.
Here are screenshots of the options to show how they differed :
The following reason for this behavior was provided by Markus Kraus from our AutoCAD engineering team :
When driven from apps or from script, most AutoCAD commands default to their first command version (the version where the command has been introduced the first time in AutoCAD)
Here is a small code snippet that set the command version to get this working :
 Adesk::UInt8 cmdVerNew = 2;
 Adesk::UInt8 cmdVerOld 
  = acedInitCommandVersion(cmdVerNew);
 AcGePoint2d ll(0.0, 0.0); 
 AcGePoint2d ur(4.0, 5.0);
 acedCommandS(RTSTR, _T("_.revcloud" ), 
     RTSTR, _T("_R" ), 
     RTSTR, _T("_A" ), 
     RTREAL, 0.25, RTREAL, 0.75, 
     RTPOINT, ll, RTPOINT, ur, RTNONE);
  Such the command versioning can also be implemented for custom commands that you create. To do this, please refer to the ObjectARX documentation on "acedGetCommandVersion". Based on the command version, a custom command can vary in its functioning.

## 评论

**内容**: ramiz said...
how to implement this method in autocad???
Reply
04/26/2018 at 12:23 AM

---
