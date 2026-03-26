---
title: "Converting a Polyline2d to Polyline"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - Database
  - ObjectARX
  - Polyline
description: "For converting Polyline2d to Polyline, you can use Polyline.ConvertFrom API. But this API throws the eInvalidContext exception when the second argu..."
author: Autodesk
---
# Converting a Polyline2d to Polyline

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/converting-a-polyline2d-to-polyline.html

## 文章内容

By Virupaksha Aithal
For converting Polyline2d to Polyline, you can use Polyline.ConvertFrom API. But this API throws the eInvalidContext exception when the second argument for ConvertFrom() is set to true, inside the transaction. The true argument will handover the same object Id's to the new entity. This is fine except for a rule that AcDbObject::handOverTo() (defined in ObjectARX) cannot be used inside of a transaction. So, to solve issue, use Open and Close technology as shown in below code.
[CommandMethod("TestConvertPoly")]
public void testConvertPoly()
{
 Document doc = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
 Editor ed = doc.Editor;
   // select the entity
 PromptEntityResult res = ed.GetEntity("Select PolyLine: ");
 // if ok
 if (res.Status == PromptStatus.OK)
 {
     // use the using keyword so that the objects auto-dispose
     //(close)  at the end of the brace
     // open for write otherwise ConvertFrom will fail
     using (Entity ent =
         (Entity)res.ObjectId.Open(OpenMode.ForRead))
     {
           // if it's a polyline2d
         if (ent is Polyline2d)
         {
             Polyline2d poly2d = (Polyline2d)ent;
             poly2d.UpgradeOpen();
               // again use the using keyword to ensure auto-closing
             using (Autodesk.AutoCAD.DatabaseServices.Polyline poly
                 = new Autodesk.AutoCAD.DatabaseServices.Polyline())
             {
                 poly.ConvertFrom(poly2d, true);
             }
         }
     }
 }
}

## 评论

**内容**: Artvegas said...
What about using the OpenCloseTransaction class instead?
using (OpenCloseTransaction tr = db.TransactionManager.StartOpenCloseTransaction())
{
Polyline2d poly2d = (Polyline2d)tr.GetObject(res.ObjectId, OpenMode.ForWrite);
poly.ConvertFrom(poly2d, true);
tr.Commit();
}
This is how Kean did it a while back:
http://through-the-interface.typepad.com/through_the_interface/2010/07/shortening-a-set-of-autocad-lines-using-net.html
Reply
06/06/2012 at 06:46 PM

---
**内容**: Artvegas said...
Actually after a little more experimenting I found that the OpenCloseTransaction causes some other issues with the conversion. In particular the converted polyline couldn't be selected, so I'll go with what you have here.
Reply
06/06/2012 at 07:15 PM

---
**内容**: Artvegas said...
OpenCloseTransaction is now working for me. You just have to make sure you add the newly created polylines to the transaction using AddNewlyCreatedDBObject(). At the end of the day I get the same result.
Reply
06/06/2012 at 08:19 PM

---
**内容**: Virupaksha Aithal said...
Thanks. your comments will help anyone how wants to use OpenCloseTransaction.
-Viru
Reply
06/08/2012 at 01:52 AM

---
**内容**: Antti Karanta said...
The given code works if the polyline2d is of Poly2dType.SimplePoly or Poly2dType.FitCurvePoly. However, it fails with eNotApplicable if the type is Poly2dType.CubicSplinePoly (and I would imagine the same would happen with Poly2dType.QuadSplinePoly). From ConvertFrom docs: "entity must point to a SimplePoly or FitCurvePoly type of Polyline2d".
Any ideas on how to convert CubicSplinePoly or QuadSplinePoly to Polylines? Is it possible?
Reply
06/30/2015 at 04:13 AM

---
**内容**: Shinu Mathew said...
Hi Viru, I am getting a eInvalidInput at the poly.ConvertFrom line. I am supplying it a 2D Polyline, with true flag as shown in your example. I also copied your code into a separate module to see if it works, but it fails wit the same error. Any Idea why or how I can do this?
Reply
07/11/2021 at 11:36 PM

---
**内容**: Shinu Mathew said in reply to Shinu Mathew...
Well, My Bad. The object had Xdata.. Precisely what you advised!
Reply
07/11/2021 at 11:56 PM

---
