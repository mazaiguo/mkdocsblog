---
title: "Creating PolyfaceMesh from a 3D Solid"
date: 2013-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Solid
description: "Here is a sample code to create a Polyface Mesh from a 3D solid. Most of the code in this blog post is from Kean's blog post on a similar topic wit..."
author: Autodesk
---
# Creating PolyfaceMesh from a 3D Solid

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/creating-polyfacemesh-from-a-3d-solid.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to create a Polyface Mesh from a 3D solid. Most of the code in this blog post is from Kean's blog post on a similar topic with some changes made to create a Polyface Mesh. As in the original post, I have tested it with a sphere and the mesh parameters may need tweaking for more complex solids.
using Autodesk.AutoCAD.BoundaryRepresentation;
  [CommandMethod("SOL2POLYFACEMESH")]
static public void PolyfaceMeshFromSolid()
{
    Document doc =
    Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions peo =
    new PromptEntityOptions("Select a 3D solid");
    peo.SetRejectMessage("\nA 3D solid must be selected.");
    peo.AddAllowedClass(typeof(Solid3d), true);
    PromptEntityResult per = ed.GetEntity(peo);
      if (per.Status != PromptStatus.OK)
        return;
      Transaction tr = db.TransactionManager.StartTransaction();
    using (tr)
    {
        BlockTable bt = (BlockTable)tr.GetObject
            (
                db.BlockTableId,
                OpenMode.ForRead,
                false
            );
          BlockTableRecord btr = (BlockTableRecord)
                tr.GetObject(
                                bt[BlockTableRecord.ModelSpace],
                                OpenMode.ForWrite, false
                            );
          Solid3d sol = tr.GetObject(
                                    per.ObjectId,
                                    OpenMode.ForRead
                                  ) as Solid3d;
          // Calculate the approximate size of our solid
        double length = sol.GeometricExtents.MinPoint.GetVectorTo
                        (sol.GeometricExtents.MaxPoint).Length;
          using (Brep brp = new Brep(sol))
        {
            // Create and set our mesh control object
              using (Mesh2dControl mc = new Mesh2dControl())
            {
                // These settings seem extreme, but only result
                // in ~500 faces for a sphere (during my testing,
                // anyway). Other control settings are available
                  mc.MaxNodeSpacing = length / 10000;
                mc.MaxSubdivisions = 100000000;
                  // Create a mesh filter object
                  using (Mesh2dFilter mf = new Mesh2dFilter())
                {
                    // Use it to map our control settings
                    // to the Brep
                      mf.Insert(brp, mc);
                      // Generate a mesh using the filter
                      PolyFaceMesh pfm = new PolyFaceMesh();
                    pfm.SetDatabaseDefaults();
                    pfm.ColorIndex = 2;
                    btr.AppendEntity(pfm);
                      short v0 = 0;
                    short v1 = 0;
                    short v2 = 0;
                    short v3 = 0;
                    short v = 0;
                      Dictionary<Point3d, short> vertexLookup
                            = new Dictionary<Point3d, short>();
                      using (Mesh2d m = new Mesh2d(mf))
                    {
                        // Extract individual faces
                        // from the mesh data
                          foreach (Element2d e in m.Element2ds)
                        {
                            foreach (Node n in e.Nodes)
                            {
                                if (! vertexLookup.ContainsKey(n.Point))
                                {
                                    PolyFaceMeshVertex pfmVertex
                                        = new PolyFaceMeshVertex(n.Point);
                                      pfm.AppendVertex(pfmVertex);
                                    vertexLookup.Add(n.Point, ++v);
                                      tr.AddNewlyCreatedDBObject
                                            (pfmVertex, true);
                                }
                                  n.Dispose();
                            }
                        }
                          foreach (Element2d e in m.Element2ds)
                        {
                            Point3dCollection pts
                                    = new Point3dCollection();
                            foreach (Node n in e.Nodes)
                            {
                                pts.Add(n.Point);
                                  n.Dispose();
                            }
                              e.Dispose();
                              v0 = 0;
                            if (vertexLookup.ContainsKey(pts[0]))
                                v0 = vertexLookup[pts[0]];
                              v1 = 0;
                            if (vertexLookup.ContainsKey(pts[1]))
                                v1 = vertexLookup[pts[1]];
                              v2 = 0;
                            if (vertexLookup.ContainsKey(pts[2]))
                                v2 = vertexLookup[pts[2]];
                              v3 = 0;
                            if (pts.Count == 4)
                            {
                                if (vertexLookup.ContainsKey(pts[3]))
                                    v3 = vertexLookup[pts[3]];
                            }
                              FaceRecord fr
                               = new FaceRecord(v0, v1, v2, v3);
                            pfm.AppendFaceRecord(fr);
                            tr.AddNewlyCreatedDBObject(fr, true);
                        }
                    }
                      tr.AddNewlyCreatedDBObject(pfm, true);
                      vertexLookup.Clear();
                }
            }
        }
        tr.Commit();
    }
}
Here is a screenshot of the Polyface Mesh created from the sphere :

## 评论

**内容**: Ernesto Gatto said...
no se ingles alguien me puede decir que significa edge surface gracias
Reply
12/13/2013 at 05:38 AM

---
**内容**: F_Rollan said...
Could you post the same sample in ARX (c++) ?
thanks.
Reply
07/03/2014 at 04:56 AM

---
