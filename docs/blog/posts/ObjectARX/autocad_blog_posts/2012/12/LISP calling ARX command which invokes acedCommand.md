---
title: "LISP calling ARX command which invokes acedCommand"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - AutoLISP
  - C++
  - ObjectARX
description: "Some developers defined the ARX command (by AddCommand )which invokes acedCommand and calls the ARX command by LISP (way1). In the previous release..."
author: Autodesk
---
# LISP calling ARX command which invokes acedCommand

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/lisp-calling-arx-command-which-invokes-acedcommand.html

## 文章内容

By Xiaodong Liang
Some developers defined the ARX command (by AddCommand )which invokes acedCommand and calls the ARX command by LISP (way1). In the previous release such as AutoCAD 2007, this caused the failure after running the LISP command several times, the solution is to define ARX command with acedDefun (way2)instead of AddCommand. This solution still works well in the latest releases.
This is a sample project: Download LispArx_VS2008. It also includes way1. Although way1 seems to work as well in the latest releases, it is still not a recommended way.
To test:
1. Build the attached ARX application and load it into AutoCAD.
2. Load test.lsp.
3. Run test1 or test2 command some times 
NOTE: You may want to inspect the CMDNAMES variable after each successful execution and note when AutoCAD does not properly exit the ARX command.
Some key codes:
// lisp2cmd.cpp : Initialization functions
#include "StdAfx.h"
#include "StdArx.h"
#include "resource.h"
  HINSTANCE _hdllInstance =NULL ;
  // This command registers an ARX command.
void AddCommand(const TCHAR* cmdGroup,
                const TCHAR* cmdInt,
                const TCHAR* cmdLoc,
                const int cmdFlags,
                const AcRxFunctionPtr cmdProc,
                const int idLocal = -1);
    // NOTE: DO NOT edit the following lines.
//{{AFX_ADS_FUNC_TABLE
typedef struct {
    TCHAR    *name;
    int     (*fptr)();
    BOOL    regFunc;
    BOOL    renderCmd;
} ftblent;
  #define ELEMENTS(array) (sizeof(array)/sizeof((array)[0]))
  //the functions for  acedDeFun
ftblent exfun[] = {
    {_T(""), NULL, FALSE, FALSE },
    {_T("c:testcmd"), testcmd, FALSE, FALSE },
}; //}}AFX_ADS_FUNC_TABLE
    //{{AFX_ARX_MSG
void InitApplication();
void UnloadApplication();
//}}AFX_ARX_MSG
  // NOTE: DO NOT edit the following lines.
//{{AFX_ARX_ADDIN_FUNCS
//}}AFX_ARX_ADDIN_FUNCS
    //////////////////////////////////////////////////////////
// DLL Entry Point
extern "C"
BOOL WINAPI DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID /*lpReserved*/)
{
    if (dwReason == DLL_PROCESS_ATTACH)
    {
        _hdllInstance = hInstance;
    } else if (dwReason == DLL_PROCESS_DETACH) {
      }
    return TRUE;    // ok
}
  ///////////////////////////////////////////////// ObjectARX EntryPoint
extern "C" AcRx::AppRetCode
acrxEntryPoint(AcRx::AppMsgCode msg, void* pkt)
{
    switch (msg) {
    case AcRx::kInvkSubrMsg:
        dofun();
        break;
    case AcRx::kUnloadDwgMsg:
        funcunload();
        break;
    case AcRx::kLoadDwgMsg:
        funcload();
        break;
    case AcRx::kInitAppMsg:
        // Comment out the following line if your
        // application should be locked into memory
        acrxDynamicLinker->unlockApplication(pkt);
        acrxDynamicLinker->registerAppMDIAware(pkt);
        InitApplication();
        break;
    case AcRx::kUnloadAppMsg:
        UnloadApplication();
        break;
    }
    return AcRx::kRetOK;
}
  // Init this application. Register your
// commands, reactors...
void InitApplication()
{
    // NOTE: DO NOT edit the following lines.
    //{{AFX_ARX_INIT
    AddCommand(_T("ASDKCMDS"), _T("TESTCMD"), _T("TESTCMD"), ACRX_CMD_TRANSPARENT, AsdkCMDStestcmd);
    //}}AFX_ARX_INIT
      // TODO: add your initialization functions
  }
  // Unload this application. Unregister all objects
// registered in InitApplication.
void UnloadApplication()
{
    // NOTE: DO NOT edit the following lines.
    //{{AFX_ARX_EXIT
    acedRegCmds->removeGroup(_T("ASDKCMDS"));
    //}}AFX_ARX_EXIT
      // TODO: clean up your application
}
  // This functions registers an ARX command.
// It can be used to read the localized command name
// from a string table stored in the resources.
void AddCommand(const TCHAR* cmdGroup,
                const TCHAR* cmdInt,
                const TCHAR* cmdLoc,
                const int cmdFlags,
                const AcRxFunctionPtr cmdProc,
                const int idLocal)
{
    TCHAR cmdLocRes[65];
      // If idLocal is not -1, it's treated as an ID for
    // a string stored in the resources.
    if (idLocal != -1) {
          // Load strings from the string table and register the command.
        ::LoadString(_hdllInstance,
                     idLocal,
                      cmdLocRes, 64);
        acedRegCmds->addCommand(cmdGroup,
                     cmdInt,
                     cmdLocRes,
                     cmdFlags,
                     cmdProc);
      } else
        // idLocal is -1, so the 'hard coded'
        // localized function name is used.
        acedRegCmds->addCommand(cmdGroup,
                      cmdInt,
                      cmdLoc, cmdFlags, cmdProc);
}
  /////////////////////////////////////////////////////////////////////
// funcload(internal)
// This function is called to define all function names in the ADS
// function table.  Each named function will be callable from lisp or
// invokable from another ADS application.
/////////////////////////////////////////////////////////////////////
static int funcload(void)
{
    int i;
      for (i = 1; i < ELEMENTS(exfun); i++) {
        if (!acedDefun(exfun[i].name, i))
            return RTERROR;
        if (exfun[i].regFunc)
            acedRegFunc(exfun[i].fptr, i);
    }
      return RTNORM;
}
  /////////////////////////////////////////////////////////////////////
// funcunload(internal)
// This function is called to undefine all function names in the ADS
// function table.  Each named function will be removed from the
// AutoLISP hash table.
/////////////////////////////////////////////////////////////////////
static int funcunload(void)
{
    int i;
      // Undefine each function we defined
      for (i = 1; i < ELEMENTS(exfun); i++) {
        acedUndef(exfun[i].name,i);
    }
      return RTNORM;
}
  /////////////////////////////////////////////////////////////////////
// dofun(internal)
// This function is called to invoke the function which has the
// registerd function code that is obtained from acedGetFunCode.
/////////////////////////////////////////////////////////////////////
static int dofun(void)
{
    int val,
        rc;
      acedRetVoid();
      if ((val = acedGetFunCode()) < 1 || val > ELEMENTS(exfun))
        return RTERROR;
  #ifdef RENDER
    if (exfun[val].renderCmd)
        if (!InitRender(false))
            return RTERROR;
#endif
      rc = (*exfun[val].fptr)();
      return ((rc == RTNORM) ? RSRSLT:RSERR);
}
  // ObjectARX defined commands
  #include "StdAfx.h"
#include "StdArx.h"
  // This is command 'TESTCMD'
void AsdkCMDStestcmd()
{
    ads_command(RTSTR, _T("_.LINE"), RTSTR, _T("0,0"), RTSTR, _T("100,100"), RTSTR, _T(""), RTNONE);
}
  // This is command 'C:TESTCMD'
int testcmd()
{
    ads_command(RTSTR, _T("_.LINE"), RTSTR, _T("0,0"), RTSTR, _T("100,100"), RTSTR, _T(""), RTNONE);
    return RTNORM;
}

## 评论

**内容**: sofia said...
Hello,
I want to know the role of arx in autocad 2005 and I have a confusion whether objectarx and arx/ads is same or not ?
If not then what is the difference.?
Quick response will be appreciated
Thanks..!!!
Reply
11/16/2013 at 12:28 AM

---
**内容**: Alexander Rivilis said in reply to sofia...
ADS/ARX and ObjectARX are the same thing.
ADS was in AutoCAD R10...R12
ARX was in AutoCAD R13
ObjectARX was in AutoCAD R14,2000...2014
ADS and ARX has only functions. ObjectARX is for Object-oriented programming (used classes/methods).
Reply
11/17/2013 at 03:41 PM

---
**内容**: sofia said...
thanx alexander...:)
I have to actually upgrade autocad 2005 which is coded in LISP to 2014 using .Net .I am in a fix how should I start the process of upgrading as there are arx,exe and lsp files in the existing code how they are being used I dunno the actual flow.Do you have any idea that might help me out....
Thanks in advance....:)
Sofia
Reply
11/17/2013 at 11:31 PM

---
**内容**: Alexander Rivilis said in reply to sofia...
Hi Sofia!
You mix different concepts: ObjectARX is C++ library (native C++). If you have using .NET there is AutoCAD .NET API (which mostly is "wrappers" for ObjectARX classes/methods).
AutoCAD .NET API is for creating internal .NET-plugins (dll-files loaded to AutoCAD with help of command _NETLOAD or other methods). If you have to write external application (exe-file), which control AutoCAD, you have to use AutoCAD COM/ActiveX API
Other information can be found here: http://autodesk.com/developautocad
Reply
11/19/2013 at 03:53 PM

---
**内容**: Alexander Rivilis said in reply to sofia...
For most information you can see here: http://autodesk.com/developautocad
ObjectARX is C++ library
AutoCAD .NET API is mostly .NET "wrappers" for ObjectARX and can be used only in .NET-plugins (dll-files) loaded into AutoCAD with _NETLOAD command
AutoCAD COM/ActiveX API can be used both internal (.NET-plugins) and external (exe-files controlling AutoCAD)
Reply
11/19/2013 at 04:02 PM

---
**内容**: Alexander Rivilis said...
Best place to begin is http://www.autodesk.ru/developautocad
P.S.: ObjectARX is for C++ only, but AutoCAD .NET API is "wrapper" for ObjectARX and can be used with VB.NET/C# and other .NET langs.
Reply
11/20/2013 at 02:28 PM

---
**内容**: rangaswamy said...
HI
I WANT TO RECALL ARX COMMAD CT_PLACEMENT IN TO SHORTCUT AS BELOW FORMAT
(defun c:1()(command "CT_PLACEMENT" ))
IT'S NOT PROMPTING
PLEASE HELP ME
Reply
11/19/2016 at 10:00 PM

---
**内容**: maverick dude said...
When i load the solution in Visual Studio 2015, it doesn't work. It says that the solution is on an old version and it gives a migration report and doesn't load it.
Can you share the compiled file ?

Reply
12/22/2016 at 06:45 PM

---
