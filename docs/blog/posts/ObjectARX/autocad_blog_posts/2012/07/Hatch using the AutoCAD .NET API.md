---
title: "Hatch using the AutoCAD .NET API"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
  - Hatch
description: "Below code shows the procedure to create associative hatch using .NET. Before making the hatch "Associative", hatch object is added to database."
author: Autodesk
---
# Hatch using the AutoCAD .NET API

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/hatch-using-the-autocad-net-api.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to create associative hatch using .NET. Before making the hatch "Associative", hatch object is added to database.
[CommandMethod("testHatch")]
static public void testHatch()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        ObjectId ModelSpaceId =
                SymbolUtilityServices.GetBlockModelSpaceId(db);
          BlockTableRecord btr = Tx.GetObject(ModelSpaceId,
                          OpenMode.ForWrite) as BlockTableRecord;
          Point2d pt = new Point2d(0.0, 0.0);
        Autodesk.AutoCAD.DatabaseServices.Polyline plBox =
                  new Autodesk.AutoCAD.DatabaseServices.Polyline(4);
          plBox.Normal = Vector3d.ZAxis;
        plBox.AddVertexAt(0, pt, 0.0, -1.0, -1.0);
        plBox.AddVertexAt(1,
                     new Point2d(pt.X + 10, pt.Y), 0.0, -1.0, -1.0);
        plBox.AddVertexAt(2,
                  new Point2d(pt.X + 10, pt.Y + 5), 0.0, -1.0, -1.0);
        plBox.AddVertexAt(3,
                      new Point2d(pt.X, pt.Y + 5), 0.0, -1.0, -1.0);
        plBox.Closed = true;
          ObjectId pLineId;
        pLineId = btr.AppendEntity(plBox);
        Tx.AddNewlyCreatedDBObject(plBox, true);
          ObjectIdCollection ObjIds = new ObjectIdCollection();
        ObjIds.Add(pLineId);
          Hatch oHatch = new Hatch();
        Vector3d normal = new Vector3d(0.0, 0.0, 1.0);
        oHatch.Normal = normal;
        oHatch.Elevation = 0.0;
        oHatch.PatternScale = 2.0;
        oHatch.SetHatchPattern(HatchPatternType.PreDefined, "ZIGZAG");
        oHatch.ColorIndex = 1;
          btr.AppendEntity(oHatch);
        Tx.AddNewlyCreatedDBObject(oHatch, true);
        //this works ok  
        oHatch.Associative = true;
        oHatch.AppendLoop((int)HatchLoopTypes.Default, ObjIds);
        oHatch.EvaluateHatch(true);
          Tx.Commit();
    }
  }

## 评论

**内容**: Dale Bartlett said...
Many thanks for your excellent examples. With this one I have changed to a user-defined hatch type as follows:
oHatch.SetHatchPattern(HatchPatternType.UserDefined, "_USER");
oHatch.PatternScale = 1000.0;
oHatch.PatternAngle = MathTools.DegreeToRadian(45.0);
oHatch.PatternSpace = 1000.0;
oHatch.PatternDouble = false;
Unfortunately I get an error eInvalidInput at line oHatch.EvaluateHatch(true);
This is a common problem on the forums, but I have not been able to resolve. Any ideas? Regards, Dale
Reply
11/18/2012 at 03:01 AM

---
**内容**: rajesh said in reply to Dale Bartlett...
I too have the problem.
Does some one has a solution?
Reply
05/09/2013 at 03:14 AM

---
**内容**: Ryan Thomas said in reply to Dale Bartlett...
I ran into this problem (and many variations of it) as well. I found that the API is very peculiar about the order in which you set the property values of the hatch.
This worked for me:
Hatch oHatch = new Hatch();
// set the hatch pattern first
oHatch.SetHatchPattern(HatchPatternType.UserDefined, "_USER");
// set other properties
Vector3d normal = new Vector3d(0.0, 0.0, 1.0);
oHatch.Normal = normal;
oHatch.Elevation = 0.0;
oHatch.PatternScale = 2.0;
oHatch.PatternAngle = 0.0;
oHatch.ColorIndex = 1;
oHatch.Layer = "00-Construction";
// !!IMPORTANT You must reaffirm the hatch pattern
oHatch.SetHatchPattern(HatchPatternType.UserDefined, "_USER");
// Then you can proceed as normal
btr.AppendEntity(oHatch);
Tx.AddNewlyCreatedDBObject(oHatch, true);

oHatch.Associative = true;
oHatch.AppendLoop((int)HatchLoopTypes.Default, ObjIds);
oHatch.EvaluateHatch(true);

Tx.Commit();
Reply
08/22/2013 at 11:28 AM

---
**内容**: Tom DiVittis said...
Some documentation on this order issue would be spectacular. This is costing days (literally) to figure out by the poke and hope method.
Reply
02/17/2017 at 01:41 PM

---
**内容**: Larn Regis said...
Is there any example how to create a hatch on a region? Especially a region which has a hole in it, like a rectangle with a small circle in it.
ObjectIdCollection acObjIdColl = new ObjectIdCollection();
acObjIdColl.Add(re.ObjectId);
hat.AppendLoop(HatchLoopTypes.Default, acObjIdColl);
re is my region
hat is the hatch
I tried all HatchLoopTypes, but none of them worked.
I always get eInvalidInput on AppendLoop.
Do i have to explode the region back into multiple polylines and then build the hatch from these?
Reply
03/11/2019 at 02:11 AM

---
**内容**: viru said in reply to Larn Regis...
Hi,
see if https://adndevblog.typepad.com/autocad/2013/07/create-hatch-objects-using-trace-boundaries-using-net.html or https://stackoverflow.com/questions/19922816/how-to-cut-a-hole-in-a-hatch-autocad/19930730#19930730 helps.
Thanks
Reply
03/11/2019 at 03:04 AM

---
**内容**: Larn Regis said in reply to Larn Regis...
I got it working by converting the region back into polylines using the example from
https://through-the-interface.typepad.com/through_the_interface/2008/08/creating-a-seri.html
then i had to sort the resulting DBObjectCollection by Area size, so i get the biggest first.
Then i was able to create the hatch using the following code
dbo is the sorted DBObjectCollection with the biggest one first
for (int i = 0; i < dbo.Count; i++)
{
ObjectIdCollection acObjIdColl = new ObjectIdCollection();
Entity e = (Entity)dbo[i];
btr_entity.AppendEntity(e);
acTrans.AddNewlyCreatedDBObject(e, true);//the entity needs to exist in the DB, otherwise AppendLoop throws an eInvalidInput exception
acObjIdColl.Add(e.ObjectId);
if (i == 0)
hat.AppendLoop(HatchLoopTypes.Outermost, acObjIdColl);
else
hat.AppendLoop(HatchLoopTypes.Default, acObjIdColl);
e.Erase(); //remove the temporary Entity again
}
Reply
03/11/2019 at 03:27 AM

---
