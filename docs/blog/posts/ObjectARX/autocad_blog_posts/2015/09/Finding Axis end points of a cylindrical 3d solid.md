---
title: "Finding Axis end points of a cylindrical 3d solid"
date: 2015-09-01
categories:
  - AutoCAD
tags:
  - API
  - Solid
description: "In a recent query from a developer, the axis end points of a cylindrical solid were needed to be retrieved. For this, it is required to get the cir..."
author: Autodesk
---
# Finding Axis end points of a cylindrical 3d solid

发布日期: 2015-09-01

原始链接: https://adndevblog.typepad.com/autocad/2015/09/finding-axis-end-points-of-a-cylindrical-3d-solid.html

## 文章内容

By Balaji Ramamoorthy
In a recent query from a developer, the axis end points of a cylindrical solid were needed to be retrieved. For this, it is required to get the circular edges that make the cylinder and find its center points. I remembered Gilles Chanteau's elegant code snippet in a discussion forum post that made use of Linq query with BRep API and went in search of it and found this. It turned out that the code could be made to retrieve the axis end points of a cylindrical solid with minimal change.
So here is the modified code snippet and thanks to Gilles.
 [CommandMethod("FindCylinderAxis" )]
 public  void  FindCylinderAxis()
 {
     Document doc 
     = Application.DocumentManager.MdiActiveDocument;
     Editor ed = doc.Editor;
       PromptEntityOptions peo 
     = new  PromptEntityOptions("Pick a cylinder : " );
     peo.SetRejectMessage
     ("\\nA 3d solid of cylindrical shape must be selected." );
     peo.AddAllowedClass(
     typeof (Autodesk.AutoCAD.DatabaseServices.Solid3d), true );
     PromptEntityResult per = ed.GetEntity(peo);
     if  (per.Status != PromptStatus.OK)
         return ;
       using  (Transaction tr 
     = doc.Database.TransactionManager.StartTransaction())
     {
         Solid3d sld = tr.GetObject(
         per.ObjectId, OpenMode.ForRead, false ) as  Solid3d;
         Point3d axisPt1 = Point3d.Origin;
         Point3d axisPt2 = Point3d.Origin;
         if  (GetCylinderAxis(sld, ref  axisPt1, ref  axisPt2))
         {
             ed.WriteMessage(String.Format("{0}Axis points : {1} {2}" , 
             Environment.NewLine, 
             axisPt1.ToString(), axisPt2.ToString()));
         }
         else 
             ed.WriteMessage(String.Format("{0}Not a cylinder." , 
             Environment.NewLine));
           tr.Commit();
     }
 }
   private  bool  GetCylinderAxis(
     Solid3d solid, ref  Point3d axisPt1, ref  Point3d axisPt2)
 {
     bool  isCylinder = false ;
     axisPt1 = Point3d.Origin;
     axisPt2 = Point3d.Origin;
     using  (Brep brep = new  Brep(solid))
     {
         if  (brep.Complexes.Count() != 1)
             return  false ;
         if  (brep.Faces.Count() != 3)
             return  false ;
         BrepEdgeCollection edges = brep.Edges;
         if  (edges.Count() != 2)
             return  false ;
         CircularArc3d[] circles = brep.Edges
             .Select(edge => 
             ((ExternalCurve3d)edge.Curve).NativeCurve 
             as  CircularArc3d)
             .Where(circle => circle != null )
             .ToArray();
         if  (circles.Length != 2)
             isCylinder = false ;
         else 
         {
             isCylinder = 
             (circles[0].Radius == circles[1].Radius &&
             circles[0].Normal.IsParallelTo(circles[1].Normal));
             axisPt1 = circles[0].Center;
             axisPt2 = circles[1].Center;
         }
     }
     return  isCylinder;
 }

## 评论

**内容**: lalit said...
i am very new to objectarx, I am trying to implement boolean subtract operation using objectarx for subtracting a cylinder from a cuboid. Could you provide some reference code as how can I do this?
Reply
09/16/2015 at 05:13 AM

---
**内容**: Balaji said in reply to lalit...
Hi Lalit,
This blog post should help you get started :
http://through-the-interface.typepad.com/through_the_interface/2013/01/performing-boolean-operations-on-autocad-solids-using-net.html
Regards,
Balaji
Reply
09/17/2015 at 04:30 PM

---
