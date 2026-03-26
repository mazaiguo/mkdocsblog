---
title: "Recognising Cancel when using acedCommandC"
date: 2014-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Sending commands to AutoCAD command line now has two variants of the earlier acedCommand method. The acedCommandS is simpler to use and suitable wh..."
author: Autodesk
---
# Recognising Cancel when using acedCommandC

发布日期: 2014-05-01

原始链接: https://adndevblog.typepad.com/autocad/2014/05/recognising-cancel-when-using-acedcommandc.html

## 文章内容

By Balaji Ramamoorthy
Sending commands to AutoCAD command line now has two variants of the earlier acedCommand method. The acedCommandS is simpler to use and suitable when all the parameters (a.k.a tokens) that are required by AutoCAD to complete the command execution are known without a need for user input. When using acedCommandS by providing all the parameters, there is no possibility of cancelling the command.
acedCommandC is to be used when you need AutoCAD to pause for some user input while is command is run by AutoCAD. In this case, there is a possibility of user cancelling the command without providing the input. To identify this condition, here is a code snippet that uses the "acedCmdCWasCancelled" and "acedCallBackOnCancel" methods. Also, due to the asynchronous nature of acedCommandC, the completion of the command can only be identified from the callback method provided to acedCommandC as in this code snippet.
#include "acedCmdNF.h"
  static void AdskMyTestCommand()
{
    ads_point pt1;
    int rt = ads_getpoint(
        NULL,
        _T("\nSelect first point: "), pt1);
      int rs = acedCommandC
                (
                    &MyCallback,
                    NULL,
                    RTSTR,
                    _T("_line"),
                    RT3DPOINT,
                    pt1,
                    RTNONE
                );
      acutPrintf(ACRX_T("\nAfter acedCommandC call.
                        acedCommandC is asynchronous..."));
}
  static int MyCallback(void * pData)
{
    if (acedCmdCWasCancelled())
    {
        acutPrintf(ACRX_T("\nCommand was cancelled..."));
        return 0;
    }
      if(isLineActive())
    {
        int rs = acedCommandC
            (
                &MyCallback,
                NULL,
                RTSTR,
                PAUSE,
                RTNONE
            );
          acedCallBackOnCancel();
          return 1;
    }
      CallWhenLineDone();
      return 0;
}
  static void CallWhenLineDone()
{
    acutPrintf(ACRX_T("\nCommand completed."));
}
  static Adesk::Boolean isLineActive()
{
    struct resbuf rb;
    acedGetVar(_T("CMDNAMES"),&rb);
    if (_tcsstr(rb.resval.rstring, _T("LINE")))
        return Adesk::kTrue;
    return Adesk::kFalse;
}

## 评论

**内容**: George Csikos said...
In isLineActive there is a memory leak.
The resbuf has a string that needs to be freed before exit.
It would be easier like this:
static Adesk::Boolean isLineActive()
{
struct resbuf *rb = acutNewRb(RTSTR);
acedGetVar(_T("CMDNAMES"), rb);
Adesk::Boolean result =_tcsstr(rb->resval.rstring, _T("LINE")) != NULL;
acutRelRb(rb);
return result;
}
Reply
10/27/2016 at 10:28 PM

---
