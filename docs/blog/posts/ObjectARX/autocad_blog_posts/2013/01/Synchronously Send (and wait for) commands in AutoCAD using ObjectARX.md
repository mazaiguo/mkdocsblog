---
title: "Synchronously Send (and wait for) commands in AutoCAD using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Polyline
description: "Leading on from this post, I thought you guys should at least know how to do the same thing in ObjectARX…"
author: Autodesk
---
# Synchronously Send (and wait for) commands in AutoCAD using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/synchronously-send-and-wait-for-commands-in-autocad-using-objectarx.html

## 文章内容

By Fenton Webb
Leading on from this post, I thought you guys should at least know how to do the same thing in ObjectARX…
Issue
How can I permit a user to draw a multi-point polyline from ObjectARX? I tried to use the acedCommand to send the '_pline' command to AutoCAD, but it's impossible to predetermine how many polyline points a user will decide to enter.
Solution
A function can be implemented that first issues the PLINE command and then continually checks if PLINE is still active in the AutoCAD command buffer. If so, command pauses are sent to the command line to allow further user input.
This activity can happen repetitively until the user escapes or presses the Enter key to complete the polyline.
The following code segment does this:

Adesk::Boolean isPlineActive() 
{  
    struct resbuf rb;  
    acedGetVar(_T("CMDNAMES"),&rb);
    if(rb.restype == RTSTR && rb.resval.rstring != NULL)  
    {   
        //"PLINE" contained in CMDNAMES?
        if(_tcsstr(rb.resval.rstring,_T("PLINE"))) 
            return Adesk::kTrue;  
    }  
    return Adesk::kFalse;  
}  
void mkline() 
{
    acedCommand(RTSTR,_T("_.pline"),RTSTR,PAUSE,RTNONE);  
    while(isPlineActive())
        acedCommand(RTSTR,PAUSE,RTNONE);   
    acutPrintf (_T("\nContinue processing")); 
}

## 评论

**内容**: Oleg said...
Hi Fenton
Thanks for the good article
Btw, I'm using acedPostCommand this way instead
and it works like a charm:
[System.Security.SuppressUnmanagedCodeSecurity]
[DllImport("acad.exe", CharSet = CharSet.Auto,
CallingConvention = CallingConvention.Cdecl,
EntryPoint = "?acedPostCommand@@YAHPB_W@Z")]
extern static private int acedPostCommand(string strExpr);
[CommandMethod("pipp")]
public void tesPlineCommand()
{
acedPostCommand("_.PLINE ");
bool quit = false;
// loop round while the PLINE command is active
while (!quit)
{
// see what commands are active
string cmdNames = (string)Autodesk.AutoCAD.ApplicationServices.Application.GetSystemVariable("CMDNAMES");
// if the PLINE command is active
if (cmdNames.ToUpper().IndexOf("PLINE") >= 0)
{
//// then send a PAUSE to the command line
acedPostCommand("\\");
}
else
// otherwise quit
quit = true;
}
}
Kind regards,
Oleg
Reply
01/07/2013 at 01:14 PM

---
**内容**: Owen Wengerd said in reply to Oleg...
Oleg, your code is very dangerous. You should never make any assumptions about when an asynchronous command produces side effects.
Reply
01/07/2013 at 03:04 PM

---
**内容**: Oleg said in reply to Owen Wengerd...
Thanks mr.Owen Wengerd,
You are quite right, if the command runs in the middle of process, then the process stops, but when the code used in the end of
then everything works without problems
Kind regards,
Oleg
Reply
01/08/2013 at 08:01 AM

---
