---
title: "AcApDocManager::disableDocumentActivation() doesn't work after save & close document"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "AcApDocManager::disableDocumentActivation() should disable switching documents, opening new documents and closing documents. Usually, it does all t..."
author: Autodesk
---
# AcApDocManager::disableDocumentActivation() doesn't work after save & close document

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/acapdocmanagerdisabledocumentactivation-doesnt-work-after-save-close-document.html

## 文章内容

By Philippe Leefsma
Q:
AcApDocManager::disableDocumentActivation() should disable switching documents, opening new documents and closing documents. Usually, it does all this. However, if when saving the current document (eg. SAVE from command line), it is possible to directly close (fe. CLOSE from command line) the current document after that. Also opening a new document immediately after a SAVE is doable.
How can to make it work after SAVE?
A:
A workaround is to use AcEditorReactor and override commandEnded(). In it, you can check if the command is 'qsave' or 'save', if it is, call AcApDocManager::disableDocumentActivation() again (it is first called it in the acrxEntryPoint()).
  class CMyEditorReactor : public AcEditorReactor
{
public:
       void commandEnded(const ACHAR *pCmdStr)
       {
         if(_tcsicmp(pCmdStr, _T("qsave")) == 0 ||
            _tcsicmp(pCmdStr, _T("save")) == 0)
                     acDocManagerPtr()->disableDocumentActivation();
       }
};
  CMyEditorReactor *gpMyEdReactor = NULL;
//------------------------------------------------------------------
//----- ObjectARX EntryPoint
class CdisableDocumentActivationApp : public AcRxArxApp {
  public:
       CdisableDocumentActivationApp () : AcRxArxApp () {}
         virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt)
       {
              AcRx::AppRetCode retCode =
                  AcRxArxApp::On_kInitAppMsg (pkt) ;
                            acDocManagerPtr()->disableDocumentActivation();
                            gpMyEdReactor = new CMyEditorReactor();
              acedEditor->addReactor(gpMyEdReactor);
                return (retCode) ;
       }
         virtual AcRx::AppRetCode On_kUnloadAppMsg (void *pkt)
       {
              AcRx::AppRetCode retCode =
                  AcRxArxApp::On_kUnloadAppMsg (pkt) ;
                            if(acDocManagerPtr())
                     acDocManagerPtr()->enableDocumentActivation();
                if(gpMyEdReactor)
              {
                     acedEditor->removeReactor(gpMyEdReactor);
                     delete gpMyEdReactor;
              }
                return (retCode) ;
       }
         virtual void RegisterServerComponents () {
       }
  } ;
  //------------------------------------------------------------------
IMPLEMENT_ARX_ENTRYPOINT(CdisableDocumentActivationApp)

## 评论

**内容**: jignesh said...
activatedocument don't work in autocad2015 and autocad2016 so what to do for this ?
Reply
12/26/2016 at 04:55 AM

---
**内容**: jignesh said in reply to jignesh...
it's giving einvalidcontext(335)
Reply
12/26/2016 at 04:55 AM

---
