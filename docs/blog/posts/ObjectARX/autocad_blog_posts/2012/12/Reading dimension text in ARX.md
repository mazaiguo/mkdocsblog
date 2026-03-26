---
title: "Reading dimension text in ARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - Dimension
  - Unicode
description: "The dimension text cannot be read directly it is because the information is contained into an AdDbMtext entity owned by a block table record. From ..."
author: Autodesk
---
# Reading dimension text in ARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/reading-dimension-text-in-arx.html

## 文章内容

By Gopinath Taget
The dimension text cannot be read directly it is because the information is contained into an AdDbMtext entity owned by a block table record. From the AcDbDimension (or derived classes), you can get the block table record ID using the method dimBlockId(). Then you can iterate throught the AcDbBlockTableRecord object for the AcDbMText entity, and call the contents() method. See the following code:
AcDbEntity *pEnt;
AcDbObjectId id;
AcGePoint3d ptPick;
ads_name eName;
 if (acedEntSel (_T("Select a dimension: ") ,
  eName, asDblArray (ptPick)) != RTNORM )
  return;
acdbGetObjectId (id, eName);
acdbOpenAcDbEntity (pEnt, id, AcDb::kForRead);
 //----- Get the id of the block table
 // record which owns the text entity
AcDbDimension *pDim =AcDbDimension::cast (pEnt);
 if (pDim == NULL)
{
  pEnt->close ();
  return;
}
id =pDim->dimBlockId ();
pDim->close ();
AcDbBlockTableRecord *pr;
acdbOpenAcDbObject ((AcDbObject *&) pr,
  id, AcDb::kForRead);
 //----- Iterating the block table record
AcDbBlockTableRecordIterator *pi;
pr->newIterator (pi);
 while (!pi->done ())
{
  pi->getEntity (pEnt, AcDb::kForRead);
  if (pEnt->isKindOf (AcDbMText::desc ()))
  {
   AcDbMText *pt = (AcDbMText *) pEnt;
   ACHAR *s = pt->contents ();
   acutPrintf (s);
   delete s;
  }
  pEnt->close();
  pi->step();
}
pr->close();

## 评论

**内容**: Woody said...
Hi, I have some problems when using Dimension.GeometricExtents on autocad 2012. It is fine on autocad 2009. After debuging the program I found that the DimBlockId property of Dimension object was set to null. I have read the document of autodesk :http://docs.autodesk.com/ACDMAC/2011/ENU/ObjectARX%20Reference/index.html?frmname=topic&frmfile=AcDbDimension.html, but it is not just like that Modifying a dimension in a noncurrent database. It's just modifying the dimension in the current database. Because the DimBlockId is set to null(I don't know why), the GeometricExtents property will throw an exception. Do you have any idea about this?
Reply
06/19/2013 at 04:53 AM

---
**内容**: Smith011 said...
my autocad2020 will be crash when run this line delete s;
i dont know why.
Reply
01/18/2020 at 01:13 PM

---
