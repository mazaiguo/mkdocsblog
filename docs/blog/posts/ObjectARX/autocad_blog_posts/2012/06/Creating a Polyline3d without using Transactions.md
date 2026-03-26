---
title: "Creating a Polyline3d without using Transactions"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Plugin
  - Polyline
description: "You may or may not be aware, but you can actually handle AutoCAD database entities without using transactions… The sample code below shows how to d..."
author: Autodesk
---
# Creating a Polyline3d without using Transactions

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/creating-a-polyline3d-without-using-transactions.html

## 文章内容

by Fenton Webb
You may or may not be aware, but you can actually handle AutoCAD database entities without using transactions… The sample code below shows how to do this using Open and Close (Close happens via the end bracket of the using statement) along with also showing how to create a Polyline3d with its associated PolylineVertex3d’s.
I like using Open and Close above transactions for a couple of reasons…
First of all, in my opinion, the Open and Close style is much cleaner in terms of the amount of code needed.
Second, StartTransaction() has a huge overhead for small operations – about 100 times slower that Open and Close style for entity read operations totaling less than about 80 in a single transaction. StartOpenCloseTransaction() can be easily substituted for StartTransaction() calls, thus regaining your performance while maintaining the same code layout. I should mention that StartTransaction() really comes into it’s own on large datasets, quickly becoming 1000+ times quicker than Open and Close for write operations.
Now to talk about Polyline3d and Polyline2d a little… These types of entities are known as Complex Entities inside of AutoCAD. They are called this because their point data is made up of different vertex entity entries in the database, namely, PolylineVertex3d and PolylineVertex2d objects respectively. People don’t really use Polyline2d anymore because they are slower to process and very heavy in data size – instead the lightweight Polyline class type is used more because it’s much faster to process the point data and, of course, takes up less data space.
We haven’t created a lightweight 3d Polyline type in AutoCAD yet, so Polyline3d’s are still being used as before… When creating Polyline3d vertices, you need to make sure the host Polyline3d is added to the database before you start adding the Polyline3dVertex’s, this is shown in the code below…
// create a 3d polyline, using open and close (no transactions)
// by Fenton Webb, Autodesk, 15/06/2012
[CommandMethod("My3dPoly")]
public void My3dPoly()
{
  // get the std items
  Database db = HostApplicationServices.WorkingDatabase;
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    Point3dCollection pnts = new Point3dCollection();
  // now input some points
  PromptPointResult res = null;
  do
  {
    // pint the point
    res = ed.GetPoint("Pick a 3d point");
    // if point picked
    if (res.Status == PromptStatus.OK)
    {
      // add it to our list of points
      pnts.Add(res.Value);
    }
    else
      break;
    } while (res.Status == PromptStatus.OK);
    // if we have enough points
  if (pnts.Count >= 2)
  {
    // Create a 3D polyline with two segments (3 points)
    using (Polyline3d poly3d = new Polyline3d())
    {
      poly3d.SetDatabaseDefaults();
      // Add the new object to the current space block table record
      using (BlockTableRecord curSpace = db.CurrentSpaceId.
                                 Open(OpenMode.ForWrite) as BlockTableRecord)
      {
        // because before adding vertexes, the polyline must be in the drawing
        curSpace.AppendEntity(poly3d);
        foreach (Point3d pnt in pnts)
        {
          // now create the vertices
          using (PolylineVertex3d poly3dVertex = new PolylineVertex3d(pnt))
            // and add them to the 3dpoly (this adds them to the db also
            poly3d.AppendVertex(poly3dVertex);
        }
      }
    }
  }
}

## 评论

**内容**: Matus Brlit said...
Why don't you use the constructor with parameters?
poly3d = new Polyline3d(Poly3dType.SimplePoly, pnts, False)
Reply
06/22/2012 at 05:35 AM

---
**内容**: Fenton Webb said...
Thanks Matus!
It's a really good point... Although it wouldn't explain the points of the post very well if I used the constructor version, but your way is best in my opinion.
Thanks again
Reply
06/22/2012 at 11:56 AM

---
