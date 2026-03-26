---
title: "SendStringToExecute does not work when called during kLoadDwgMsg"
date: 2013-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - AutoLISP
  - C++
  - DWG
  - ObjectARX
description: "Why does an "eNoDocument" error occur when executing an AutoLISP expression while in the kLoadDwgMsg handler and when using sendStringToExecute?"
author: Autodesk
---
# SendStringToExecute does not work when called during kLoadDwgMsg

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/sendstringtoexecute-does-not-work-when-called-during-kloaddwgmsg.html

## 文章内容

By Xiaodong Liang
Issue
Why does an "eNoDocument" error occur when executing an AutoLISP expression while in the kLoadDwgMsg handler and when using sendStringToExecute?
Solution
Although sendStringToExecute is the preferred way to execute an AutoLISP expression or commands on AutoCAD, this function does not work during the kLoadDwgMsg. This is because the AutoCAD command line is not yet fully ready at this point. (Note that your application receives a kLoadDwgMsg when it is loaded
into AutoCAD in the middle of a session, and at that time sendStringToExecute will work. However, kLoadDwgMsg is also sent to your application when a new document is created and sendStringToExecute will not work in this scenario.)
The workaround is to use the ads_queueexpr function in this context. (Search the ObjectARX online help for more information on ads_queueexpr.)
Example:
extern "C" int ads_queueexpr(const TCHAR*);
  void OnkLoadDwgMsg()
{
    ads_queueexpr(L"(command \"line\" \"0,0\" \"1,1\" \"\")\n");
}

