---
title: "How to create multiple model space viewports from API?"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - Database
description: "I would like to create multiple viewports in model space, for example four viewports that would divide equally the screen, like four different view..."
author: Autodesk
---
# How to create multiple model space viewports from API?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/how-to-create-multiple-model-space-viewports-from-api.html

## 文章内容

By Philippe Leefsma
Q:
I would like to create multiple viewports in model space, for example four viewports that would divide equally the screen, like four different views of the same model. In addition I would like to do it automatically for each drawing that I create from the UI. How could this be achieved from arx?
A:
The code sample below illustrates how to create four viewports in model space, with possible different views of the model. For sake of simplicity, only the view parameters of the first viewport are set.
Concerning doing this processing on each new drawing, using the "AcApDocManagerReactor::documentCreated" event to place our viewport code can do the job.
void CreateViewPorts(AcDbDatabase* pDatabase, const ACHAR* vpName)
{
 AcDbViewportTable *pVT;
 pDatabase->getSymbolTable(pVT, AcDb::kForWrite);
   AcDbDictionary* pVisualStyleDic;
 pDatabase->getVisualStyleDictionary(pVisualStyleDic, AcDb::kForRead);
   AcGePoint2d ll, ur;
 AcDbObjectId vStyleId;
   AcDbViewportTableRecord* pVTR1=new AcDbViewportTableRecord;
 ll.set(0,0);
 ur.set(0.5,0.5);
   pVisualStyleDic->getAt(L"2dWireframe", vStyleId);
   pVTR1->setCenterPoint(AcGePoint2d(0, 0));
 pVTR1->setHeight(100);
 pVTR1->setWidth(100);
 pVTR1->setVisualStyle(vStyleId);
 pVTR1->setViewDirection(AcDb::kTopView);
 pVTR1->setLowerLeftCorner(ll);
 pVTR1->setUpperRightCorner(ur);
 pVTR1->setName(vpName);
   AcDbViewportTableRecord *pVTR2=new AcDbViewportTableRecord;
 ll.set(0,0.5);
 ur.set(0.5,1);
 pVTR2->setLowerLeftCorner(ll);
 pVTR2->setUpperRightCorner(ur);
 pVTR2->setName(vpName);
   AcDbViewportTableRecord *pVTR3=new AcDbViewportTableRecord;
 ll.set(0.5,0);
 ur.set(1,0.5);
 pVTR3->setLowerLeftCorner(ll);
 pVTR3->setUpperRightCorner(ur);
 pVTR3->setName(vpName);
   AcDbViewportTableRecord *pVTR4=new AcDbViewportTableRecord;
 ll.set(0.5,0.5);
 ur.set(1,1);
 pVTR4->setLowerLeftCorner(ll);
 pVTR4->setUpperRightCorner(ur);
 pVTR4->setName(vpName);
     pVT->add(pVTR1);
 pVT->add(pVTR2);
 pVT->add(pVTR3);
 pVT->add(pVTR4);
   pVT->close();
   pVTR1->close();
 pVTR2->close();
 pVTR3->close();
 pVTR4->close();
   acedCommand(RTSTR, L".-VPORTS", RTSTR, L"R", RTSTR, vpName, RTNONE);
}

## 评论

**内容**: Advance Creating said...
You provide good content.keep going
Reply
02/26/2022 at 02:39 AM

---
