---
title: "How to disable the “Save As” dialog"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
description: "You should be able to bypass AutoCAD's prompt to save drawings by using a couple of different techniques. You can catch the AutoCAD close notificat..."
author: Autodesk
---
# How to disable the “Save As” dialog

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-disable-the-save-as-dialog.html

## 文章内容

By Gopinath Taget
You should be able to bypass AutoCAD's prompt to save drawings by using a couple of different techniques. You can catch the AutoCAD close notification within a beginQuit() Editor Reactor notification handler, and set the DBMOD AutoCAD variable to 0 for each open drawing. When a document is closed however, the Save Drawing warning dialog has to be caught just prior to being displayed, at which point we can again set the DBMOD variable(s), cancel the dialog, and re-issue the command which was originally called to finally close the document. This second technique requires setting a Windows CBT (Computer Based Training) hook, which is relatively simple.
Under normal circumstances, the DBMOD variable (which is non-zero when its database requires saving) is READ-ONLY, and cannot be modified, however there is an undocumented (and unsupported) API you can use to change its value called 'acdbSetDbmod()', which is in acdbXX.lib (Where XX is the version number of the library. The current version is 19). Use this API with extreme caution, as it can lead to data loss if improperly used. With this app loaded, you will never get the opportunity to save any drawings if you close them, or exit AutoCAD, so again, extreme care is needed when using it.
One variation of these techniques could be implemented which would allow you to automatically save the drawing instead, (with the current name) and still bypass the save-as dialog. I will include comments within the code below to
demonstrate this.
Here is an example of the code required to disable the Save-As Dialog (error checking removed for brevity):
// global hook
HHOOK MyHook;
// Here we load the reactor, and set our windows CBT hook...
void InitApplication()
{   
ADSEdReactor *pEdReactor = new ADSEdReactor();   
acedEditor->addReactor(pEdReactor);   
MyHook=::SetWindowsHookEx(WH_CBT,
  (HOOKPROC)FileHook,(HINSTANCE)NULL,
  ::GetCurrentThreadId());
}
The code within the beginQuit() notification handler would just be:
void ADSEdReactor::beginQuit(void)
{
AcEditorReactor3::beginQuit () ;
AcApDocumentIterator *pIt;
pIt=acDocManager->newAcApDocumentIterator();
 while(!pIt->done())
{
  // For each open document...
  AcApDocument* pDoc=pIt->document();
  acDocManager->setCurDocument(pDoc);
  struct resbuf res;
  acedGetVar(L"DBMOD",&res);
  if(res.resval.rint) // If changes have been made...
  {
   acDocManager->lockDocument(pDoc); // Lock
   // If you want to save...
   //SaveDb(pDoc);// call the save function option.
   //If you want to discard...
   acdbSetDbmod(pDoc->database(),0); // clear changes flag
   acDocManager->unlockDocument(pDoc);//unlock
  }
  pIt->step();
}
 delete pIt;
}
Here is the CBT hook callback...
LRESULT CALLBACK FileHook(int nCode, WPARAM wParam,
LPARAM lParam)
{
 if(nCode==HCBT_CREATEWND)
{
  CBT_CREATEWND* pCbt=(CBT_CREATEWND*)lParam;
  CREATESTRUCT* pCS=(CREATESTRUCT*)(pCbt->lpcs);
  try // exception handling required...
  {
   if(pCS->lpszName &&
    !wcscmp(pCS->lpszName, L"AutoCAD") &&
    pCS->dwExStyle==65793)
   {
    AcApDocument *pDoc=acDocManager->curDocument();
    // If you Want to Save...
    //acDocManager->lockDocument(pDoc);// lock
    //SaveDb(pDoc); // call to save option
    //acDocManager->unlockDocument(pDoc); // unlock
    // If you want to discard...
    acdbSetDbmod(pDoc->database(),0); // clear changes flag
    // Re-send the command which invoked the save-as
    //dialog...
    struct resbuf res;
    acedGetVar(L"CMDNAMES",&res);
    if(!wcscmp(res.resval.rstring, L"NEW") ||
     !wcscmp(res.resval.rstring, L"OPEN"))
    {
     acDocManager->sendStringToExecute(pDoc,
      res.resval.rstring);
    }
    else
    {
     acDocManager->sendStringToExecute(pDoc,
      L".CLOSE ");
    }
      return TRUE;
   }// if
  }// try
  catch(...)
  {
  }
}// if
   return (::CallNextHookEx(MyHook,nCode,wParam,lParam));
}
Here is the option to save the drawing...
void SaveDb(AcApDocument* pDoc)
{   
 const ACHAR*pChar=pDoc->fileName();
 // Get the current filename   
AcDbDatabase *pDb=pDoc->database();   
pDb->saveAs(pChar);// call to save...   
acdbSetDbmod(pDb,0);// make sure it will close...
}
void UnloadApplication()
{   
::UnhookWindowsHookEx(MyHook); // always remove your hooks...
}
While this ARX is loaded, you should be able avoid the save-as dialog, and you should always be able to close AutoCAD. You can still save your drawing explicitly with the save command, but if you ever close a drawing, or exit AutoCAD, your changes will not be saved to the current project drawing.

## 评论

**内容**: Alexander Rivilis said...
Hi, Gopinath!
I do not know system variable "LCMDNAMES". Maybe "CMDNAMES"?
Reply
01/03/2013 at 07:23 AM

---
**内容**: Gopinath Taget said in reply to Alexander Rivilis...
Apologies. Yes, it is a typo. I will fix it.
Cheers
Gopinath
Reply
01/03/2013 at 08:09 AM

---
