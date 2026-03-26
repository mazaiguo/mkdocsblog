---
title: "Set/Get AutoLISP symbol"
date: 2012-08-01
categories:
  - AutoLISP
tags:
  - API
  - AutoLISP
  - Unicode
description: "You can use "acedPutSym" API to set the AutoLISP symbol and "acedGetSym" API to retrieves the value of a AutoLISP symbol."
author: Autodesk
---
# Set/Get AutoLISP symbol

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/setget-autolisp-symbol.html

## 文章内容

By Virupaksha Aithal
You can use "acedPutSym" API to set the AutoLISP symbol and "acedGetSym" API to retrieves the value of a AutoLISP symbol.
//set the MySymbol value
struct resbuf *rb = acutBuildList(RTSTR,
                            _T("Unicode String"), RTNONE);
int res = acedPutSym(_T("MySymbol"), rb);
acutRelRb(rb);
  //get back the text
rb = NULL;
int  rc = acedGetSym(_T("MySymbol"), &rb);
acutPrintf(L"MySymbol value is %s\n", rb->resval.rstring);
acutRelRb(rb);

## 评论

**内容**: Subir Kumar Dutta said...
What is the .net equivalent of acedGetSym ?
Reply
03/18/2014 at 12:41 AM

---
**内容**: Subir Kumar Dutta said...
What is the .net equivalent of acedGetSym ?
I tried with the below code , but its giving error ---- "Unable to find an entry point named 'acedGetSym' in DLL 'acad.exe'.

[System.Security.SuppressUnmanagedCodeSecurity]
[DllImport("acad.exe", CharSet = CharSet.Unicode, CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedGetSym")]
extern static private int acedGetSym(string args, out IntPtr result);
static public ResultBuffer AcadGetSym(string varname, ref int stat)
{
IntPtr rb = IntPtr.Zero;
stat = acedGetSym(varname, out rb);
if (stat == (int)PromptStatus.OK && rb != IntPtr.Zero)
return (ResultBuffer)DisposableWrapper.Create(typeof(ResultBuffer), rb, true);
return null;
}
I am using AutoCAD 2014 and Visual Studio 2010 on windows 7 64 bit machine.
Reply
03/18/2014 at 01:53 AM

---
**内容**: Maxence said in reply to Subir Kumar Dutta...
Document.GetLispSymbol/SetLispSymbol
Reply
09/06/2017 at 09:41 AM

---
**内容**: Virupaksha Aithal said...
Hi ,
Please import the acedGetSym from accore.dll instead of acad.exe
Thanks
Viru
Reply
03/18/2014 at 04:40 PM

---
**内容**: aiyoung said in reply to Virupaksha Aithal...
Hello Virupaksha,
Has the location of acedGetSym been changed for AutoCAD 2015, 32 bit?
I get an error that acedGetSym cannot be found in acCore.dll when i run code that uses acedGetSym.
The same code runs fine in 32 bit AutoCAD 2013 and 2014. The same code also runs correctly in 64-bit versions of AutoCAD 2013 to 2015.
I've posted the same question to the AutoDesk forms and to theswamp.org, but i haven't gotten any good replies.
http://forums.autodesk.com/t5/NET/Issues-running-Net-code-that-uses-AcedGetSym-in-32-Bit-AutoCAD/td-p/5092498
http://www.theswamp.org/index.php?PHPSESSID=vqc0sh722a4lumftn0bg2d2qf6&topic=47248.0
I would appreciate any insights you might have on this issue.
Thanks!
Reply
06/16/2014 at 05:55 AM

---
**内容**: Alexander Rivilis said...
x86: "_acedGetSym" or "?acedGetSym@@YAHPB_WPAPAUresbuf@@@Z"
x64: "acedGetSym" or "?acedGetSym@@YAHPEB_WPEAPEAUresbuf@@@Z"
Reply
06/16/2014 at 06:28 AM

---
