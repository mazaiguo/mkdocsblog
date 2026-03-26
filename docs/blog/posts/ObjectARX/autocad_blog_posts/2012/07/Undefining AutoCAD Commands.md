---
title: "Undefining AutoCAD Commands"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - AutoLISP
  - C++
  - DWG
description: "The initial option, acedRegCmds->removeCmd(), only works with ARX registered commands. It does not undefine AutoCAD native commands. The AutoCAD co..."
author: Autodesk
---
# Undefining AutoCAD Commands

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/undefining-autocad-commands.html

## 文章内容

By Augusto Goncalves
The initial option, acedRegCmds->removeCmd(), only works with ARX registered commands. It does not undefine AutoCAD native commands. The AutoCAD command UNDEFINE is definitively the way to go. Because after a OPEN or a NEW, the commands are redefined by AutoCAD you have to call Undefine each time AutoCAD sends the kLoadDwgMsg notification to your program.
The problem is that we cannot use acedCommand() within the kLoadDwgMsg notification. The workaround is to use the undocumented function ads_queueexpr() to queue the command in form of a LISP expression:
virtual AcRx::AppRetCode On_kLoadDwgMsg(void * pkt)
{
  AcRx::AppRetCode retCode =AcRxArxApp::On_kLoadDwgMsg (pkt) ;
    // queue the expression
  ads_queueexpr(_T("(command \"_.undefine\" \"saveas\")"));
    return (retCode) ;
}
ads_queueexpr will send a command to the AutoCAD command line, but won't process it until the command processor is ready. Also, that is why it is the only command capable of passing a command in while opening a drawing from zero document state

