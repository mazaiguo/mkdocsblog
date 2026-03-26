---
title: "Adding an Attribute to a Block Definition using C++ COM/ActiveX Automation in ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - COM
  - ObjectARX
  - Plugin
description: "The trick to doing this is to use the IPtr interfaces (e.g. IAcadDocumentPtr) so that COM reference counting is handled automatically."
author: Autodesk
---
# Adding an Attribute to a Block Definition using C++ COM/ActiveX Automation in ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/adding-an-attribute-to-a-block-definition-using-c-comactivex-automation-in-objectarx.html

## 文章内容

by Fenton Webb
The trick to doing this is to use the I*Ptr interfaces (e.g. IAcadDocumentPtr) so that COM reference counting is handled automatically.
Also, another trick is to stay away from VARIANT’s as much as possible, we have various AcAx* classes which help you do this… Here’s the code…
#import "acax19ENU.tlb" no_namespace
#include <rxmfcapi.h>
#include <axpnt3d.h>
void fAddAttribute()
{
  try
  {
    // get the ActiveX application object from AutoCAD, inc ref count
    IAcadApplicationPtr pAcadApp = acedGetAcadWinApp()->GetIDispatch(TRUE);
    // now get the active doc
    IAcadDocumentPtr pActiveDoc = pAcadApp->ActiveDocument;
    IAcadBlockPtr pBlock = NULL;
    TCHAR *pBlkName = _T("some_block_name");
    // create an activex compatible insertion point3d
    AcAxPoint3d axInsPnt(0,0,0);
    // now add the block name
    pBlock = pActiveDoc->Blocks->Add(axInsPnt.asVariantPtr(),_bstr_t(pBlkName));
    // now add an Attribute to the block
    IAcadAttributePtr pAttDef;
    pAttDef = pBlock->AddAttribute(1.0, (AcAttributeMode)0 ,
      _bstr_t("Type the employee name"), axInsPnt.asVariantPtr(),
      _bstr_t("empname"),_bstr_t(""));
    //attribute added
  }
  catch(_com_error &es)
  {
    acutPrintf(L"\nError : %s", es.ErrorMessage());
  }
}

