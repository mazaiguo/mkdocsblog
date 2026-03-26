---
title: "Calling a VBA macro from ARX and getting data back"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - VBA
description: "How can I call a VBA macro from ARX and get data back? After I input some data into the dialog box, which now is in VBA environment, how can I get ..."
author: Autodesk
---
# Calling a VBA macro from ARX and getting data back

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/calling-a-vba-macro-from-arx-and-getting-data-back.html

## 文章内容

By Fenton Webb
Issue
How can I call a VBA macro from ARX and get data back? After I input some data into the dialog box, which now is in VBA environment, how can I get this data back to my ARX project?
Solution
If you have a dialog box built in VBA, and want your ObjectARX project to run the dialog box, and then retrieve the data that has been input into the dialog
box so that you can continue your .ARX project, you can call a VBA macro (named "test" for example) from an ARX application using ads_command() :
acedCommand (RTSTR, _T("_-vbarun"), RTSTR, _T("test"), RTNONE);
It is not possible to return values from VBA to ARX, but you can work around this by using the system variables USERS1 ... USERS5 for strings and USERR1 ... USERR5 for doubles to exchange data between C++ and VBA.
When working with VBA you can use the SetVariable method to set the system variables values.
Public Sub test()
  Dim sysVarName As String   
  Dim sysVarData As Variant
  Dim dataType As Integer    
  Dim dataDouble As Double
  sysVarName = "USERR1"
  dataDouble = 3#
  sysVarData = dataDouble
  Call ThisDrawing.SetVariable(sysVarName, sysVarData)
End Sub
Your C++ code should contain something like:
int adstest()
{
  acedCommand (RTSTR, _T("_-vbarun"), RTSTR, _T("test"), RTNONE);
  struct resbuf result;
  if (acedGetVar("Userr1", &result) != RTNORM)   
  {
    acutPrintf("\nError getting USERR1");
    return RTNORM;     
  }
    acutPrintf ("Userr1 = %f\n", result.resval.rreal);
  return RTNORM;
}

