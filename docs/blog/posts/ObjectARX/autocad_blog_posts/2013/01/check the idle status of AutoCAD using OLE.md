---
title: "check the idle status of AutoCAD using OLE"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How do I check the idle status of AutoCAD using OLE automation functions? How do I suppress the "Server Busy Error" dialog?"
author: Autodesk
---
# check the idle status of AutoCAD using OLE

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/check-the-idle-status-of-autocad-using-ole.html

## 文章内容

By Xiaodong Liang
  Issue
How do I check the idle status of AutoCAD using OLE automation functions? How do I suppress the "Server Busy Error" dialog?
Solution
You can reliably use IAcadState to check whether the AutoCAD is free to process Automation calls. But you should have a global IAcadState object initialized and that should happen when AutoCAD is free. For any future automation requests you
can check the busy state of AutoCAD using IAcadState object and then proceed to wait till AutoCAD is free or cancel the request.
You can also use the COleMessageFilter to set the properties of the OLE automation interaction. If you do not want the Server Busy error dialog, you can suppress it using COleMessageFilter. So you can make your application wait until AutoCAD is free to process the Automation request without displaying the error dialog. The following sample code shows how to achieve this.
    COleException e;
CComPtr<IAcadApplication>  aApp;
CComPtr<IAcadState>   aState;
COleMessageFilter* pFilter;
  //how to initailize the IAcadState
//in this way we are sure that AutoCAD
//will be free to process the request.
void iniState()
{
    // get active AutoCAD
  IDispatch* pDisp = acedGetAcadWinApp()->GetIDispatch(TRUE);
    HRESULT hr = pDisp->QueryInterface(IID_IAcadApplication,
(void**)&aApp);
    if(FAILED(hr))
        return;
       if(aApp != NULL)
     {  
         aApp->GetAcadState(&aState);
    }
}
  //later whenever you want to process an automation call,
// check for IAcadState and then proceed suitably
//use acad state to check wether it is busy or not
void checkIfBusy()
{
    VARIANT_BOOL bReady = VARIANT_FALSE;
     aState->get_IsQuiescent(&bReady);
    if(bReady == VARIANT_TRUE)
    {
        CComPtr<IAcadDocument> aDoc;
        aApp->get_ActiveDocument(&aDoc);
      }
    else
        AfxMessageBox(_T("AutoCad is busy"), MB_SYSTEMMODAL );
    //you can also alter the standard behavior of your application on how to handle the Server busy responses. Please check MSDN on further information on this
  ////set client properties of OLE interactions. code
    pFilter = AfxOleGetMessageFilter();
      ASSERT(pFilter != NULL);   
      DWORD dTimedelay = 1000;
    pFilter->SetMessagePendingDelay(dTimedelay);
    dTimedelay = -1;
    pFilter->SetRetryReply(dTimedelay);
      pFilter->EnableBusyDialog(FALSE);
    pFilter->EnableNotRespondingDialog(FALSE);

## 评论

**内容**: niaz ahmad said...
Plz help. I have lost my many autocad drawings. When I am open the drawing and using the command eras or move. The drawing is disappear and given message Automation error drawing is busy. I can't recover the drawing.
Reply
11/11/2013 at 05:18 AM

---
