---
title: "Setting position of an MText for each annotation scale"
date: 2015-07-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Unicode
description: "For an MText that is annotative, its positions can be changed using its grip. The position is specific to the current annotative scale of the drawi..."
author: Autodesk
---
# Setting position of an MText for each annotation scale

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/setting-position-of-an-mtext-for-each-annotation-scale-.html

## 文章内容

By Balaji Ramamoorthy
For an MText that is annotative, its positions can be changed using its grip. The position is specific to the current annotative scale of the drawing. The API to set the position of an annotative entity for each scale programmatically is not available at present as part of the public API. A way to workaround this is to set the drawing annotation scale before changing the position. Here is a sample code to iterate the object context collection of the database and set the position of an MText for each scale.
 Document doc = 
 Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   PromptEntityOptions peo 
 = new  PromptEntityOptions("\\nSelect an MText : " );
 peo.SetRejectMessage("\\nMust be an MText ..." );
 peo.AddAllowedClass(typeof (MText), true );
   PromptEntityResult per = ed.GetEntity(peo);
   if  (per.Status != PromptStatus.OK)
     return ;
   ObjectId mtId = per.ObjectId;
   ObjectContextManager ocm = db.ObjectContextManager;
 ObjectContextCollection occ 
 = ocm.GetContextCollection("ACDB_ANNOTATIONSCALES" );
   if  (ocm == null )
     return ;
   foreach  (ObjectContext oc in  occ)
 {
     using  (Transaction tr 
         = db.TransactionManager.StartTransaction())
     {
         MText mt 
         = tr.GetObject(mtId, OpenMode.ForRead) as  MText;
         Point3d pos = mt.Location;
         if  (mt.HasContext(oc))
         {
             AnnotationScale annoScale 
             = oc as  AnnotationScale;
                           if  (annoScale != null )
                 db.Cannoscale = annoScale;
               mt.UpgradeOpen();
                           mt.Location = pos 
             + Vector3d.XAxis * 3 
             + Vector3d.YAxis * 3;
         }
         tr.Commit();
     }
 }
  Here are two screenshots showing the scale specific positions before and after the change

## 评论

**内容**: Bruno GEOFFROY said...
Why they do not give access to the annotation scale info?
I have some (plenty) drawings where the annotative position of block attributes have been set to a wrong z values (how? I really do not know how draughtsmen have made this...).
I have tried with .net, VBA or ObjectARX to get access to the position points for each scale and set their z to zero for all but it does not seem to be available.
Reply
02/09/2016 at 07:04 AM

---
