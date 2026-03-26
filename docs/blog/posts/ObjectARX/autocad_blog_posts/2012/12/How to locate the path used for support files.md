---
title: "How to locate the path used for support files"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "AutoCAD puts support files (i.e. acad.pgp) in the Users/username/... folder. My program searches for the acad.pgp and other support files to update..."
author: Autodesk
---
# How to locate the path used for support files

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-locate-the-path-used-for-support-files.html

## 文章内容

By Philippe Leefsma
Q:
AutoCAD puts support files (i.e. acad.pgp) in the Users/username/... folder. My program searches for the acad.pgp and other support files to update. How can I easily locate this directory?
A:
There are a couple of means available to retrieve this path. One is to get the value from the Registry. It is stored in the RoamableRootFolder key in this location: 
HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\<Release>\ACAD-<Version>:<Language>
You could use the value of CurVer key in this location
HKEY_CURRENT_USER\Software\Autodesk\AutoCAD\<Release> To first get the CurVer to get the correct location for different AutoCAD based products.
Another approach would be to use the sysvar roamablerootprefix. Which will also return this path.

## 评论

**内容**: Norman said...
if the user intends to locate support file (acad.pgp), NOT the location for roaming profile, then it is a bad suggestion to go RoamableRootFolder/roamablerootprefix. Yes, AutoCAD default installationo does include some paths underneath roamable root folder into its support paths. Only in this case it make sense to search there for acad.pgp. However, the paths underneath roamable root folder may not be included as support paths depending on how AutoCAD is set up in an office (such as in my office, we have acad.pgp located in particular location).
So, again, if user asks where to find support file, not where his/her roamable profile data, he/she should search AutoCAD support paths, which may or may not include paths underneath roamable root folder.
Reply
12/10/2012 at 10:20 AM

---
**内容**: Peter said...
An easy way to access the current support path is to use the UserConfigurationManager as Kean Walmsley mentioned in his blog: http://through-the-interface.typepad.com/through_the_interface/2008/05/storing-custom.html
Another way to find a file in the support path is to use the findfile function in Lisp.
Reply
12/11/2012 at 12:45 AM

---
