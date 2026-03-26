---
title: "Cancel AutoCAD commands programmatically using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "How do I cancel out of a currently running AutoCAD command, such as MOVE. I would do some handling in an editor reactor's commandWillStart function..."
author: Autodesk
---
# Cancel AutoCAD commands programmatically using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/cancel-autocad-commands-programmatically-using-objectarx.html

## 文章内容

By Xiaodong Liang
Issue
How do I cancel out of a currently running AutoCAD command, such as MOVE. I would do some handling in an editor reactor's commandWillStart function, and in some cases, cancel the regular AutoCAD MOVE function.
Solution
The AcEdCommandStack stores pointers to ARX objects and functions, but there is no access to the function pointers of native AutoCAD commands. However, you can perform a cancellation in an editor reactor callback.
extern Adesk::Boolean acedPostCommand(const char* );
void MyEditorReactor::commandWillStart(const char * pCmdStr)
{
   if ( strcmp(pCmdStr,"MOVE" ) == 0  )
    acedPostCommand("CANCELCMD"); 
}

