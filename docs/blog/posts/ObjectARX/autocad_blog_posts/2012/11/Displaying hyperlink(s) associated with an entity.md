---
title: "Displaying hyperlink(s) associated with an entity"
date: 2012-11-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "The code below demonstrates the use of the Hyperlink classes. (AcDbHyperlink, AcDbEntityHyperlinkPE and AcDbHyperlinkCollection ). There is a proto..."
author: Autodesk
---
# Displaying hyperlink(s) associated with an entity

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/displaying-hyperlinks-associated-with-an-entity.html

## 文章内容

By Balaji Ramamoorthy
The code below demonstrates the use of the Hyperlink classes. (AcDbHyperlink, AcDbEntityHyperlinkPE and AcDbHyperlinkCollection ). There is a protocol extension associated with every entity in the AutoCAD database and this code example displays the hyperlink associated with an entity.
NOTE: See the "Hyperlink Example" in the ObjectARX Developer's Guide for another example for accessing hyperlinks. That example shows how to add a hyperlink to a selected entity.
ads_name ename;
ads_point pt;
  int ret;
ret = acedEntSel
        (
            _T("\nSelect an entity with hyper link(s): "),
            ename,
            pt
        );
if(ret != RTNORM)
    return;
  AcDbObjectId gId;
acdbGetObjectId(gId, ename);
  AcDbEntity* pEnt = NULL;
if(acdbOpenAcDbEntity(pEnt, gId, AcDb::kForRead) == Acad::eOk)
{
    bool bHasHyperLink = false;
      AcDbEntityHyperlinkPE *pHyperLinkPE = ACRX_X_CALL(pEnt, AcDbEntityHyperlinkPE);
    pHyperLinkPE->hasHyperlink
        (
            (AcDbObject*)pEnt,
            bHasHyperLink
        );
      if(bHasHyperLink == true)
    {
        AcDbHyperlinkCollection* phlc;
          pHyperLinkPE->getHyperlinkCollection((AcDbObject*)pEnt, phlc);
        for(int i=0; i<phlc->count(); i++)
        {
            AcDbHyperlink* phl = phlc->item(i);
            acutPrintf(_T("\nHyperlink on this entity = %s"),phl->name());
        }
        delete phlc;
    }
    pEnt->close();
}

