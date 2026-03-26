---
title: "How to Find intersections between two entities (line and spline) using ObjectARX or LISP?"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - COM
  - ObjectARX
description: "Although conventional AutoLISP doesn't provide functions for this purpose, you can use ActiveX or ObjectARX. Here's some code to show you how:"
author: Autodesk
---
# How to Find intersections between two entities (line and spline) using ObjectARX or LISP?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-find-intersections-between-two-entities-line-and-spline-using-objectarx-or-lisp.html

## 文章内容

By Gopinath Taget
Although conventional AutoLISP doesn't provide functions for this purpose, you can use ActiveX or ObjectARX. Here's some code to show you how:
Visual LISP sample using ActiveX:
(defun c:Test ()
  (vl-load-com)
  (setq ent1 (vlax-ename->vla-object (car (entsel "First entity: ")))
ent2 (vlax-ename->vla-object (car (entsel "Second entity: ")))
  )
  (vlax-safearray->list
    (vlax-variant-value
      (vla-IntersectWith ent1 ent2 acExtendBoth)
    )
  )
)
  ObjectARX sample:
AcDbEntity* selectEntity(const ACHAR* prompt,
AcDbObjectId& id,
AcGePoint3d& pick,
AcDb::OpenMode openMode )
{
AcDbEntity* ent = NULL;
ads_name ename;
   if(acedEntSel(prompt, ename, asDblArray(pick) ) == RTNORM)
{
  if(acdbGetObjectId(id,ename)==Acad::eOk)
  {
   if(acdbOpenAcDbEntity(ent,id,openMode)==Acad::eOk)
    return ent;
  }
}
 return ent;
}
  void Test()
{
 // TODO: Implement the command
AcDbEntity* pEnt1;
AcDbEntity* pEnt2;
AcGePoint3d pick;
AcDbObjectId id;
Acad::ErrorStatus es;
AcGePoint3dArray is;
   if((pEnt1 = selectEntity(_T("\nSelect 1st entity : "),
  id,pick,AcDb::kForRead))== NULL)
{
  acutPrintf(L"\nSelection failed");
  return;
}
   if((pEnt2 = selectEntity(_T("\nSelect 2nd entity : "),
  id,pick,AcDb::kForRead))== NULL)
{
  acutPrintf(_T("\nSelection failed"));
  pEnt1->close();
  return;
}
  es = pEnt1->intersectWith(pEnt2,AcDb::kOnBothOperands,is);
   if(es != Acad::eOk)
{
  acutPrintf(_T("\nIntersectWith failed : es = %s"),
   acadErrorStatusText(es));
}
 else
{
  acutPrintf(_T("\nGot %d intersections"),is.length());
  for(int i= 0;i<is.length();i++)
  {
   acutPrintf(_T("\nIntersection[%d] :(%.3lf,%.3lf,%3.lf)"),
    i,is[i].x,is[i].y,is[i].z);
  }
}
pEnt1->close();
pEnt2->close();
}

