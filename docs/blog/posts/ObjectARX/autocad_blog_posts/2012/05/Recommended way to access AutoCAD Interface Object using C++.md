---
title: "Recommended way to access AutoCAD Interface Object using C++"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM
  - ObjectARX
description: "The common way to access AutoCAD interface object is GetActiveObject, but this may return null on certain scenarios, such as OnkInitAppMsg, and is ..."
author: Autodesk
---
# Recommended way to access AutoCAD Interface Object using C++

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/recommended-way-to-access-autocad-interface-object-using-c.html

## 文章内容

By Augusto Goncalves
The common way to access AutoCAD interface object is GetActiveObject, but this may return null on certain scenarios, such as On_kInitAppMsg, and is not guaranteed to access the current AutoCAD.
Since the ObjectARX application is loaded into AutoCAD process space, there is no need to go to running object’s table to get the COM pointer. So we can get it directly using the following code snippet (which requires MFC support):
IAcadApplicationPtr pAcadApp;
IDispatch* pDispatch = acedGetAcadWinApp()->GetIDispatch(FALSE);
pDispatch->QueryInterface(__uuidof(IAcadApplication),
                         (void**)&pAcadApp);

## 评论

**内容**: daniel said...
how about acedGetIDispatch?
Reply
05/23/2012 at 06:16 AM

---
**内容**: Augusto Goncalves said...
It's basically the same. The key here is use GetIDispatch instead GetObject. Thanks.
Reply
05/23/2012 at 07:13 AM

---
**内容**: Fenton Webb said...
Personally, I like this way - it's very slick and succinct, best of all it automatically cleans up COM reference counts when the function returns...
#import "acax18ENU.tlb"

// get the dispatch driver from autocad
CComQIPtr acad = acedGetAcadWinApp()->GetIDispatch(TRUE);
// now, for exaple, get the menu bar
CComQIPtr menuBar = acad->GetMenuBar();
Also, passing FALSE for the GetIDispatch() is only used if you want the interface object to live past the end of the function, normally it would always be TRUE. Obviously, we can't see the context that Augusto is using that code in so I just wanted to say.
Reply
05/24/2012 at 08:18 AM

---
**内容**: Fenton Webb said...
oops, the less that/greater than symbols are not there...
// get the dispatch driver from autocad
CComQIPtrLESSTHANAutoCAD::IAcadApplicationGREATERTHAN acad = acedGetAcadWinApp()->GetIDispatch(TRUE);
// now get the menu bar
CComQIPtrLESSTHANAutoCAD::IAcadMenuBarGREATERTHAN menuBar = acad->GetMenuBar();
Reply
05/24/2012 at 08:19 AM

---
