---
title: "XRef Unload / Detach event in .Net"
date: 2013-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - XREF
description: "In an ObjectARX application, to get a notification after an XRef has been unloaded or detached, it is needed to override the "AcEditorReactor::xref..."
author: Autodesk
---
# XRef Unload / Detach event in .Net

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/xref-unload-detach-event-in-net.html

## 文章内容

By Balaji Ramamoorthy
In an ObjectARX application, to get a notification after an XRef has been unloaded or detached, it is needed to override the "AcEditorReactor::xrefSubcommandUnloadItem" and "AcEditorReactor::xrefSubcommandDetachItem" in the editor reactor class. Unfortunately, there is no equivalent of these methods in the AutoCAD .Net API. 
A workaround for getting this notification in a .Net plugin is implemented in the attached project.
For the complete code, please refer to the attachment. The steps with only the relevant code are : 
1) Export a method from the .arx which accepts a function pointer to use for notification.
// Function pointer that we will store in our editor reactor
typedef void (__stdcall *PTRFN_Notify)(int xrefUnloadType);
  // Exported method that will be called from .Net
extern "C" DLLIMPEXP
            void SetXrefEventNotifyCB(PTRFN_Notify callBack);
2) Implement an editor reactor in the ObjectARX module.
// asdkMyEdReactor.h
  class asdkMyEdReactor : public AcEditorReactor
{
protected:
    // Override virtual functions to get notified about Xref
    // unload / detach.
    virtual void xrefSubcommandUnloadItem(
                                           AcDbDatabase* pHost,
                                           int activity,
                                           AcDbObjectId blockId
                                         );
      virtual void xrefSubcommandDetachItem(
                                           AcDbDatabase* pHost,
                                           int activity,
                                           AcDbObjectId blockId
                                          );
  public:
    static PTRFN_Notify mXrefCB;
      //...
} ;
    // asdkMyEdReactor.cpp
  PTRFN_Notify asdkMyEdReactor::mXrefCB = NULL;
  void asdkMyEdReactor::xrefSubcommandUnloadItem(
                                        AcDbDatabase* pHost,
                                        int activity,
                                        AcDbObjectId blockId)
{
    acutPrintf(ACRX_T("\nC++ : XRef unloaded."));
      // Check if we have a function pointer that we can use to notify
    if(mXrefCB != NULL)
    {
        // Notify our C# module about unload
        (mXrefCB)(1);
    }
    AcEditorReactor::xrefSubcommandUnloadItem(pHost, activity, blockId);
}
  void asdkMyEdReactor::xrefSubcommandDetachItem(
                                        AcDbDatabase* pHost,
                                        int activity,
                                        AcDbObjectId blockId)
{
    acutPrintf(ACRX_T("\nC++ : XRef detached."));
      // Check if we have a function pointer that we can use to nofity.
    if(mXrefCB != NULL)
    {
        // Notify our C# module about detach
        (mXrefCB)(2);
    }
    AcEditorReactor::xrefSubcommandDetachItem(pHost, activity, blockId);
}
  // Store the function pointer for future use.
// This will used to notify when Xref unload/detach happens.
void SetXrefEventNotifyCB(PTRFN_Notify callBack)
{
    asdkMyEdReactor::mXrefCB = callBack;
}
3) Implement a callback method in .Net plugin and invoke the exported method with a delegate initialized to the callback method.
// Needed for dllimport
using System.Runtime.InteropServices;
  public delegate void XrefUnloadDelegate(int xrefUnloadType);
  // Delegate that will be passed to the .arx module
static XrefUnloadDelegate _xrefUnloadCB = null;
  // Get the method exposed in the .arx module
[DllImport("AdskXrefUnloadTest.arx", CharSet = CharSet.Auto)]
public static extern void
            SetXrefEventNotifyCB(MulticastDelegate callback);
  // Callback that will be invoked from .arx module when
// an Xref unload / detach happens
// xrefUnloadType = 1 indicates a unload
// xrefUnloadType = 2 indicates a detach
public void xrefCB(int xrefUnloadType)
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    if (xrefUnloadType == 1)
        ed.WriteMessage("\nC# : XRef unloaded.");
    else if (xrefUnloadType == 2)
        ed.WriteMessage("\nC# : XRef detached.");
    else
        ed.WriteMessage("\nC# : XRef CB. Unload type unknown.");
}
  void IExtensionApplication.Initialize()
{
    if (_xrefUnloadCB == null)
        _xrefUnloadCB = new XrefUnloadDelegate(xrefCB);
      // Provide the callback to the .arx module
    SetXrefEventNotifyCB(_xrefUnloadCB);
}
Here is the sample project :
Download XrefUnloadDetach

