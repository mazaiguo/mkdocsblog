---
title: "Create Bitmap Of Selected Entities"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - COM
  - ObjectARX
description: "If you want to generate/create a BMP out of selected entities then you need to use Export() method of the AcadDocument class of ActiveX Automation ..."
author: Autodesk
---
# Create Bitmap Of Selected Entities

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/create-bitmap-of-selected-entities.html

## 文章内容

By Gopinath Taget
If you want to generate/create a BMP out of selected entities then you need to use Export() method of the AcadDocument class of ActiveX Automation API of AutoCAD.
The VC++ sample below creates a BMP image out of the selection set.
// Important: check ?Use MFC? option while creating the
// ObjectARX project using ObjectARX Wizard
  void fCreateBMP()
{
 try
{
  IAcadApplicationPtr pApp;
  IAcadDocumentPtr pAtvDoc;
  IAcadSelectionSetPtr pSS;
  pApp = acedGetAcadWinApp()->GetIDispatch(TRUE);
    //get the active document and selectionset
  pApp->get_ActiveDocument(&pAtvDoc);
  pSS = pAtvDoc->get_ActiveSelectionSet(&pSS);
  pSS->SelectOnScreen();//without any filters
  if(S_OK == pAtvDoc->Export(_bstr_t("c:\\test"),
   _bstr_t("BMP"),pSS))
   acutPrintf(L"\nCreated BMP successfully.");
}
 catch (_com_error &es)
{
  acutPrintf(L"\nerror %s",(char *) es.Description());
}
}
Note that the bitmap is generated out of the viewable area of the current document and the size is dependent on the window size of the document while generating the bitmap.
If you want to control the size of the bitmap then before generating the bitmap, set the window size of the document using the Height() and Width() properties of IAcadDocument class. Also before changing the window size make sure that the windowState() is set to normal size. Then, zoom to the area that contains your objects, this you may have to do it programmatically after the user selects the objects on the screen.

## 评论

**内容**: sudarshan d. said...
how to use AcadDocument class in ObjectARX
Reply
01/18/2016 at 05:31 AM

---
