---
title: "How to close AutoCAD drawing immediately after opening"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Database
  - Unicode
  - XREF
description: "You may need to close an AutoCAD drawing immediately after performing some validity checks during the open procedure, but before the user has a cha..."
author: Autodesk
---
# How to close AutoCAD drawing immediately after opening

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-close-autocad-drawing-immediately-after-opening.html

## 文章内容

By Gopinath Taget
You may need to close an AutoCAD drawing immediately after performing some validity checks during the open procedure, but before the user has a chance to interact with AutoCAD.
In general, calling ads_queueexpr("(COMMAND \"CLOSE\")\n") from the acrxEntryPoint handler for the kLoadDwgMsg message will close the newly opened drawing. However, under certain circumstances this will fail, and AutoCAD will report the error "AutoCAD cannot close [drawing name] because there is a command active." There are a few subtle issues which conspire to make AutoCAD exhibit this behavior, but basically it boils down to the fact that at the time the kLoadDwgMsg notification is sent, the command throat for the new drawing is just barely created, and sending commands at that time can be fairly unpredictable. I have narrowed down the issues.
First, AutoCAD will send TWO separate kLoadDwgMsg notifications (prompting the sending of two CLOSE commands) if you OPEN a drawing on top of the 'null' ("drawing1.dwg") drawing when it is unmodified (DBMOD=0). AutoCAD's default behavior closes this drawing, and that operation will interfere with your attempt to CLOSE the new drawing, so the solution is to set the DBMOD for the 'null' drawing to 1 (unsaved) so that AutoCAD will not try to close it. My example below uses an undocumented/unsupported feature ("acdbSetDbmod()") of AutoCAD which can directly change the DBMOD variable. Use extreme care when using it.
Second, depending on the content of the drawing, whether the initial view is model space or paperspace, and whether there are XREF's included, the "CLOSE" command, which is called from application context, can get caught in the command throat, and cough up the "AutoCAD cannot close..." message (above). The remedy for this symptom is to create a custom AutoCAD command that runs in the document context, which subsequently calls the ads_queueexpr(..."CLOSE"...) function.
Here is the relevant code:
extern long acdbSetDbmod(AcDbDatabase* pDb, long newVal);
bool DontOpenDrawing = true;
virtual AcRx::AppRetCode On_kLoadDwgMsg (void *pkt)
{
  AcRx::AppRetCode retCode =AcRxArxApp::On_kLoadDwgMsg (pkt);
  // We want to close immediately (You decide why)
  if(DontOpenDrawing==true)
  {
   AcApDocumentIterator *Iter =
    acDocManager->newAcApDocumentIterator();
   // Iterate through all open drawings
   // to find the  'null' drawing.
   while(!Iter->done())
   {
    const ACHAR *name;
    Acad::ErrorStatus es = 
     Iter->document()->database()->getFilename(name);
    // getFilename() will return a null
    // pointer for the 'null' drawing.
    if(!name)
    {
     // Set 'null' drawing as  modified
     acdbSetDbmod(Iter->document()->database(),1);
     // push is necessary for setting DBMOD
     Iter->document()->pushDbmod();                                     
    }
    Iter->step();
   }
   delete Iter;
   // send the custom command to close
   ads_queueexpr(L"(COMMAND \"CLOSECMD\")\n");
  }
  return retCode;
}
// - asdkArxCloseDoc._CloseCmd command (do not rename)
 static void asdkArxCloseDoc_CloseCmd(void)
{
  // Add your code for command asdkArxCloseDoc._CloseCmd here
   ads_queueexpr(L"(COMMAND \"CLOSE\")\n");
}

