---
title: "Associating hyperlink with BlockTableRecord"
date: 2015-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Block
  - C++
description: "In ObjectARX, BlockTableRecord provides access to its hyperlink collection using the AcDbEntityHyperlinkPE. In AutoCAD 2015, the Hyperlinks collect..."
author: Autodesk
---
# Associating hyperlink with BlockTableRecord

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/associating-hyperlink-with-blocktablerecord.html

## 文章内容

By Balaji Ramamoorthy
In ObjectARX, BlockTableRecord provides access to its hyperlink collection using the AcDbEntityHyperlinkPE. In AutoCAD 2015, the Hyperlinks collection is now also accessible using the AutoCAD .Net API.  
Here is a C++ and .Net code snippets to create a new block with hyperlink to AutoCAD Devblog :
ObjectARX C++ API :
 AcApDocument *pActiveDoc = acDocManager->mdiActiveDocument();
 AcDbDatabase *pDB = pActiveDoc->database();
   AcDbBlockTable *pBlockTable = NULL;
 Acad::ErrorStatus es = pDB->getBlockTable(
       pBlockTable, kForWrite);
 if (! pBlockTable->has(ACRX_T("Test" )))
 {
  // Create the BlockTableRecord with hyperlink 
  AcDbBlockTableRecord *pBTR = new  AcDbBlockTableRecord();
  pBTR->setName(ACRX_T("Test" ));
  AcDbObjectId btrId = AcDbObjectId::kNull;
  pBlockTable->add(btrId, pBTR);
    AcDbCircle *pCircle = new  AcDbCircle(
   AcGePoint3d::kOrigin, 
   AcGeVector3d::kZAxis, 10.0);
    pBTR->appendAcDbEntity(pCircle);
  pCircle->close();
    AcDbHyperlinkCollection * pcHCL = NULL;
  ACRX_X_CALL(pBTR, AcDbEntityHyperlinkPE)
   ->getHyperlinkCollection(pBTR, pcHCL, false , true );
    pcHCL->addTail(
   ACRX_T("http://adndevblog.typepad.com/autocad/" ), 
   ACRX_T("AutoCAD DevBlog" ));
    ACRX_X_CALL(pBTR, AcDbEntityHyperlinkPE)
  ->setHyperlinkCollection(pBTR, pcHCL);
       delete  pcHCL;
  pBTR->close();
 }
 pBlockTable->close();
  AutoCAD .Net API (should work in AutoCAD 2015+) :
 Database db = 
  Application.DocumentManager.MdiActiveDocument.Database;
   using  (Transaction tr = 
  db.TransactionManager.StartTransaction())
 {
     BlockTable bt = tr.GetObject(
                                     db.BlockTableId,
                                     OpenMode.ForRead
                                 ) as BlockTable;
       if  (bt.Has("MyBlock" ) == false )
     {
         bt.UpgradeOpen();
         BlockTableRecord btr = new  BlockTableRecord();
         btr.Name = "MyBlock" ;
         btr.Origin = Point3d.Origin;
         bt.Add(btr);
         tr.AddNewlyCreatedDBObject(btr, true );
           Circle c = new  Circle(
    Point3d.Origin, 
    Vector3d.ZAxis, 10.0);
           btr.AppendEntity(c);
         tr.AddNewlyCreatedDBObject(c, true );
         //Get the hyperlink collection from the entity 
         HyperLinkCollection linkCollection = btr.Hyperlinks;
           //Create a new hyperlink 
         HyperLink hyperLink = new  HyperLink();
         hyperLink.Description = "AutoCAD DevBlog" ;
         hyperLink.Name 
    = "http://adndevblog.typepad.com/autocad/" ;
         hyperLink.SubLocation = "" ;
         linkCollection.Add(hyperLink);
     }
     tr.Commit();
 }

