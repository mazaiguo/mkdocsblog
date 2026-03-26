---
title: "Batch rendering of drawings"
date: 2015-10-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - COM
description: "In a recent query, a developer wanted to batch render drawings in AutoCAD. The API does support rendering to a file as explained in this blog post...."
author: Autodesk
---
# Batch rendering of drawings

发布日期: 2015-10-01

原始链接: https://adndevblog.typepad.com/autocad/2015/10/batch-rendering-of-drawings.html

## 文章内容

By Balaji Ramamoorthy
In a recent query, a developer wanted to batch render drawings in AutoCAD. The API does support rendering to a file as explained in this blog post. But, if you do not want to code all that and would prefer running AutoCAD's Render command on a set of files, here is a code snippet to do that. This uses the AutoCAD's COM API to open the drawing, run the Render command and close it after its done. As the Render command in AutoCAD brings up the Render window, the following code snippet closes that window using Win32 API.
Here is a recording to show the Batch rendering of drawings in action :
Here is the code snippet :
#include 

#pragma warning( disable : 4278 )
// Change it if you use a different AutoCAD version
#import "acax19ENU.tlb" no_implementation raw_interfaces_only named_guids
using namespace AutoCAD; 
#pragma warning( default : 4278 )

#pragma pack (pop)


Acad::ErrorStatus es;
AcDbBlockTable *pBlockTable = NULL;

AcDbDatabase *pDb = acdbHostApplicationServices()->workingDatabase();
  
HRESULT hr;

CStringArray m_arDrawingsToOpen ;
m_arDrawingsToOpen.SetSize(3);
m_arDrawingsToOpen[0] = "D:\\Temp\\RT1.dwg";
m_arDrawingsToOpen[1] = "D:\\Temp\\RT2.dwg";
m_arDrawingsToOpen[2] = "D:\\Temp\\RT3.dwg";

CWinApp* pWinApp = acedGetAcadWinApp(); 
if(! pWinApp) 
 return;
CComPtr pDisp = pWinApp->GetIDispatch(TRUE); 
if(! pDisp) 
 return;
   
CComPtr pComApp; 
hr = pDisp->QueryInterface(
    AutoCAD::IID_IAcadApplication,(void**)&pComApp); 
if(FAILED(hr)) 
 return;

CComPtr pDocs;
hr = pComApp->get_Documents(&pDocs);
if(FAILED(hr)) 
 return;
      
for (int index = 0; 
    index < m_arDrawingsToOpen.GetSize(); index++)
{
 CString strDrawingFile = m_arDrawingsToOpen[index];

 CComPtr pDispDoc;
 hr = pDocs->Open(CComBSTR(strDrawingFile), 
    CComVariant(true), CComVariant(NULL), &pDispDoc);

 if(SUCCEEDED(hr))
 {
  WaitUntilReady(pComApp);

  //;;Command
  //-RENDER
  //;;Specify render preset [Draft/Low/Medium/High/Presentation/Other] : 
  //Medium
  //;;Specify render destination [Render window/Viewport] : 
  //R
  //;;Enter output width <640>:
  //640
  //;;Enter output height <480>:
  //480
  //;;Save rendering to a file? [Yes/No] : 
  //Y
  //;;Specify output file name and path: 
  //D:\Temp\Test.png
  CString outFilePath;
  outFilePath.Format(ACRX_T("D:\\Temp\\Test%d.jpg"), index+1);

  CString cmd;
  cmd.Format(ACRX_T("-RENDER Medium R 640 480 Y %s\n"), outFilePath); 
  BSTR bstrCmd = cmd.AllocSysString();

  CFile file;
  CFileStatus status;
  if(file.GetStatus(outFilePath, status) == TRUE)
  {// Erase existing file, before proceeding to render
   CFile::Remove(outFilePath);
  }

  hr = pDispDoc->SendCommand(bstrCmd);

  ::SysFreeString(bstrCmd);

  TCHAR windowText[MAX_PATH];
  GetWindowTextW(GetActiveWindow(), windowText, MAX_PATH);

  CString wndCaption;
  wndCaption.Format(ACRX_T("Test%d - Render"), index+1);

  if (! lstrcmpi(windowText, wndCaption))
  {
   SendMessage(GetActiveWindow(), WM_CLOSE, 0,0);
   acutPrintf(ACRX_T("\n%s window closed."), windowText);
  }

  _variant_t b(VARIANT_FALSE);
  hr = pDispDoc->Close(b);
 }
}


static Adesk::Boolean WaitUntilReady(CComPtr pComApp)
{
 HRESULT hr;
 Adesk::Boolean renderDone = Adesk::kFalse;
 int maxTries = 10;
 do
 {
  CComPtr pAcadState;
  hr = pComApp->GetAcadState(&pAcadState);
  if(SUCCEEDED(hr))
  {
   VARIANT_BOOL bReady = VARIANT_FALSE; 
   pAcadState->get_IsQuiescent(&bReady);
   if(bReady == VARIANT_TRUE)
   {
    return Adesk::kTrue;
   }
   else
    ::Sleep(1000);
  }
  maxTries--;
 }while( (maxTries > 0) && ! renderDone);
 return Adesk::kFalse;
}

## 评论

**内容**: Peter said...
Hi Balaji
the screencast looks a little bit strange: the size of embedded area is too small, the sidebar with the commands is really big and the time of the movie is displayed as "0:13 / 0:00".
Is it possible to improve it?
Thanks
Peter
Reply
10/26/2015 at 01:38 PM

---
**内容**: Balaji said...
Hi Peter,
Thanks for bringing this to my notice.
The screencast video looks ok. But, there have been some recent format changes to this blog and the embedding of screencast videos does not seem to be working as it did earlier. Sorry about that.
You can watch it full screen by scrolling down and clicking on the up arrows at the bottom right.
Hope that helps.
Regards,
Balaji
Reply
10/26/2015 at 09:40 PM

---
**内容**: Peter said...
Hi Balaji
also in Fullscreen the picture is strange: the left half of the display is darkened and overwritten by huge strings, displaying the currently used commands.
http://www.pixhost.org/show/67/30143106_typepad_screencast.png
Regards
Peter
Reply
10/28/2015 at 02:45 AM

---
**内容**: joao said...
Any chance of doing this for Revit??
Reply
11/16/2015 at 08:54 AM

---
