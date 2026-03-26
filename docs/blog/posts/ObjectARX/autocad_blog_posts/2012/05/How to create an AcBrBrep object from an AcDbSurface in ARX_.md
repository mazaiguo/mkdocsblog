---
title: "How to create an AcBrBrep object from an AcDbSurface in ARX?"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Surface
description: "Is it possible to create a BRep object out of a surface using ARX?"
author: Autodesk
---
# How to create an AcBrBrep object from an AcDbSurface in ARX?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-create-an-acbrbrep-object-from-an-acdbsurface-in-arx.html

## 文章内容

By Philippe Leefsma
Is it possible to create a BRep object out of a surface using ARX?
Solution
The following code illustrates how to achieve that. Once the BRep object has been created, you could use it to access the NURB information of your surface for example:
void BrepSurface(AcDbSurface* pSurface)
{
 AcDbBody* pBody = new AcDbBody();
   Acad::ErrorStatus es = pBody->setASMBody(pSurface->ASMBodyCopy());
   AcBrBrep* pBrep = new AcBrBrep();
   if(AcBr::eOk == pBrep->set(*pBody))
 {
  AcBrBrepFaceTraverser* pFaceTrav = new AcBrBrepFaceTraverser;
    if(AcBr::eOk == pFaceTrav->setBrep(*pBrep))
  {
   for(pFaceTrav->restart();!pFaceTrav->done();pFaceTrav->next())
   {
    AcBrFace face;
      if(AcBr::eOk == pFaceTrav->getFace(face))
    {
     double area = 0.0f;
     face.getSurfaceArea(area);
          acutPrintf(L"\nSurface Area: %f", area);
          AcGeNurbSurface nurbSurface;
     face.getSurfaceAsNurb(nurbSurface);
     //face.getSurfaceAsTrimmedNurbs(); 
    }
   }
  }
  delete pFaceTrav;
 }
 delete pBrep;
}
  void BrepSurface()
{
 ads_name eName;
 ads_point pt;
   if(RTNORM != acedEntSel(L"\nSelect a surface: ", eName, pt ))
        return;
   AcDbObjectId id;
 acdbGetObjectId(id, eName);
 AcDbSurface* pSurface = NULL;
 acdbOpenObject(pSurface, id, AcDb::kForRead);
   if(pSurface == NULL )
 {
  acutPrintf(L"\nNot a surface...");
  return;
 }
   BrepSurface(pSurface);
 pSurface->close();
}

## 评论

**内容**: Evangelos said...
Dear Philippe,
Thank you for this help full post.
I used your process and I would like to ask you what this line exactly does, as I could not find ant relevant information in the documentation (for internal use only).
Acad::ErrorStatus es = pBody->setASMBody(pSurface->ASMBodyCopy());
In addition, I observed that the pBody is not database-resident. For this reason, I had to add it first to one block table record.
Could you verify this step?
Kind regards,
Evangelos
Reply
03/22/2018 at 03:11 AM

---
