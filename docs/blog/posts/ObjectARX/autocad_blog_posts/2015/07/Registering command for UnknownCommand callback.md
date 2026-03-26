---
title: "Registering command for UnknownCommand callback"
date: 2015-07-01
categories:
  - AutoCAD
tags:
  - API
description: "This sample answers couple queries regarding unknownCommand callback and usage of UnknownCommand,"
author: Autodesk
---
# Registering command for UnknownCommand callback

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/registering-command-for-unknowncommand-callback.html

## 文章内容

By Madhukar Moogala
This sample answers couple queries regarding unknownCommand callback and usage of UnknownCommand,
The basic usage of this API, when ever user enters wrong or unregistered command name, like a typo, we can use mechanism to capture the typo command and send our registered command or built command.
In this example user tries to enter some unknown command like “u60”, in the callback fired from the reactor event unknownCommand, we will load our “TestUknCom”.
Some challenges or queries:
How to suppress the unknown command message on CommandLine ?
Currently engineering team is working on this,ideally “AcadAppInfo::kNoAction;” in loaderFunPtr should solve the problem. However we have a workaround is to read the unknown command string and registered on the fly and unregister while unloading app, kind of hack.
How to remove the command called in the callback from Command history ?
The ACRX_CMD_NOHISTORY mask flag will help excluding our registered command “TestUknCom” from history.
  Code:
class adskedReactor : public AcEditorReactor
{
public:
  // Constructor / Destructor
adskedReactor(const bool autoInitAndRelease = true);
virtual ~adskedReactor();
  //{{AFX_ARX_METHODS(adskedReactor)
virtual void beginQuit();
virtual void unknownCommand(   const TCHAR* cmdStr,   AcDbVoidPtrArray *al);
//}}AFX_ARX_METHODS
  private:
// Auto initialization and release flag.
bool m_autoInitAndRelease;
};
adskedReactor::adskedReactor(const bool autoInitAndRelease)
{
m_autoInitAndRelease = autoInitAndRelease;
if (m_autoInitAndRelease)
if (NULL != acedEditor)
acedEditor->addReactor(this);
else
m_autoInitAndRelease = false;
}
  adskedReactor::~adskedReactor()
{
if (m_autoInitAndRelease)
if (NULL != acedEditor)
acedEditor->removeReactor(this);
}
  void adskedReactor::beginQuit()
{
AcApDocumentIterator *pIt;
pIt=acDocManager->newAcApDocumentIterator();
while(!pIt->done())
{
// For each open document...
AcApDocument* pDoc=pIt->document();
acDocManager->setCurDocument(pDoc);
struct resbuf res;
acedGetVar(_T("DBMOD"),&res);
if(res.resval.rint) // If changes have been made...
{
acDocManager->lockDocument(pDoc); // Lock
// If you want to save...
//SaveDb(pDoc);// call the save function.
//If you want to discard...
acdbSetDbmod(pDoc->database(),0); // clear changes flag
acDocManager->unlockDocument(pDoc);//unlock
}
pIt->step();
}
delete pIt;
}
/*Function callback*/
AcadAppInfo::CmdStatus LoaderFunPtr(void *p)
{   
  acedPostCommand ((LPCTSTR) gsCmd) ;
return AcadAppInfo::kNoAction;
}
  /*To suppress the UnknownCommand message,
make the unknowncommand on the fly as registered command*/
void unknwCommand()
{
/*Dummy function*/
}
  void adskedReactor::unknownCommand(   const TCHAR* cmdStr,   AcDbVoidPtrArray *al)
{
/*Don't forget remove command after use*/
acedRegCmds->addCommand(_T("UNKGrp"), cmdStr, cmdStr, ACRX_CMD_MODAL, unknwCommand);
CString sCmd;
unkCmd.Format(cmdStr);
gsCmd.Format(_T("TestUknCom\n"));
AcadAppInfo* pAppInfo = new AcadAppInfo();
pAppInfo->setAppLoader(LoaderFunPtr);
pAppInfo->setLoadReason(AcadApp::kLoadDisabled);
pAppInfo->setAppName(_T("TestCBCom"));
al->append(pAppInfo);
    }
/*Arx function*/
void TestUknCom()
{
acutPrintf(_T("TestUknCom is called \n"));
}
// Init this application. Register your
// commands, reactors...
void InitApplication()
{
  adskedReactor *pEdReactor=new adskedReactor();
acedEditor->addReactor(pEdReactor);
AddCommand(_T("TestCBCom"), _T("TestUknCom"), _T("TestUknCom"),ACRX_CMD_NOHISTORY , TestUknCom); //
}
  // Unload this application. Unregister all objects
// registered in InitApplication.
void UnloadApplication()
{
acedRegCmds->removeCmd(_T("UNKGrp"),unkCmd);
  }
  // This functions registers an ARX command.
void AddCommand(const TCHAR* cmdGroup, const TCHAR* cmdInt, const TCHAR* cmdLoc,
const int cmdFlags, const AcRxFunctionPtr cmdProc, const int idLocal)
{
acedRegCmds->addCommand(cmdGroup, cmdInt, cmdLoc, cmdFlags, cmdProc);
}
          extern "C"
AcRx::AppRetCode acrxEntryPoint(AcRx::AppMsgCode msg, void *pkt)
//**************************************************************
{
switch(msg)
{
case AcRx::kInitAppMsg:
acrxDynamicLinker->unlockApplication(pkt);
acrxDynamicLinker->registerAppMDIAware(pkt);
/*Load commands*/
acrxBuildClassHierarchy();/*use this for derived classes*/
InitApplication();
  break;
case AcRx::kUnloadAppMsg:
  UnloadApplication();
  break;
default:
break;
}
return AcRx::kRetOK;
}

## 评论

**内容**: backrooms said...
When a user makes a mistake or uses a command name that hasn't been registered, like a typo, we can use a mechanism to catch the typo command and send our registered command or a built command.
Reply
08/02/2023 at 01:50 AM

---
