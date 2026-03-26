---
title: "Converting a surface to a subDMesh"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Surface
description: "This involves two steps :"
author: Autodesk
---
# Converting a surface to a subDMesh

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/converting-a-surface-to-a-subdmesh.html

## 文章内容

By Balaji Ramamoorthy
This involves two steps :
1. Call the static method “SubDMesh.GetObjectMesh” to retrieve the vertex and face array from a surface.
2. Call the “SubDMesh.SetSubDMesh” method and pass the vertex and face information retrieved in step1.
Here is a sample code :
[CommandMethod("SubDMeshFromSurface")]
public void TestMethod()
{
    Document activeDoc
        = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      Point3d p1 = new Point3d(0.0, 0.0, 0.0);
    Point3d p2 = new Point3d(5.0, 0.0, 0.0);
    Point3d p3 = new Point3d(5.0, 5.0, 0.0);
    Point3d p4 = new Point3d(0.0, 5.0, 0.0);
      ObjectId oid = ObjectId.Null;
    using (Transaction tr
        = db.TransactionManager.StartTransaction())
    {
        Autodesk.AutoCAD.DatabaseServices.Face face
            = new Autodesk.AutoCAD.DatabaseServices.Face
                            (
                                p1,
                                p2,
                                p3,
                                p4,
                                true,
                                true,
                                true,
                                true
                            );
        Autodesk.AutoCAD.DatabaseServices.Surface surface
            = new Autodesk.AutoCAD.DatabaseServices.Surface();
          surface.SetDatabaseDefaults();
        surface
            = Autodesk.AutoCAD.DatabaseServices.Surface.CreateFrom(face);
          BlockTable bt = tr.GetObject(
                                        db.BlockTableId,
                                        OpenMode.ForRead
                                    ) as BlockTable;
        BlockTableRecord modelSpaceBTR
            = tr.GetObject
                        (
                            bt[BlockTableRecord.ModelSpace],
                            OpenMode.ForWrite
                        ) as BlockTableRecord;
        oid = modelSpaceBTR.AppendEntity(surface);
          tr.AddNewlyCreatedDBObject(surface, true);
        tr.Commit();
    }
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        Autodesk.AutoCAD.DatabaseServices.Surface surf
            = tr.GetObject
                        (
                            oid,
                            OpenMode.ForRead
                        ) as Autodesk.AutoCAD.DatabaseServices.Surface;
          MeshFaceterData mfd = new MeshFaceterData();
        mfd.FaceterMeshType = 0;
        mfd.FaceterMaxEdgeLength = 0.5;
          MeshDataCollection md = SubDMesh.GetObjectMesh(surf, mfd);
          SubDMesh mesh = new SubDMesh();
        mesh.SetDatabaseDefaults();
        mesh.SetSubDMesh(md.VertexArray, md.FaceArray, 1);
          BlockTable bt
                = tr.GetObject
                            (
                                db.BlockTableId,
                                OpenMode.ForRead
                            ) as BlockTable;
        BlockTableRecord modelSpaceBTR
            = tr.GetObject
                        (
                            bt[BlockTableRecord.ModelSpace],
                            OpenMode.ForWrite
                        ) as BlockTableRecord;
        modelSpaceBTR.AppendEntity(mesh);
          tr.AddNewlyCreatedDBObject(mesh, true);
        tr.Commit();
    }
}

## 评论

**内容**: Afshin said...
Hi Balaji,
I was trying to test the above code (with some changes) and got an error "eInvalidInput" on creating some surfaces. tried to debug and found out that AutoCAD can not create Surface object from some Face objects in some circumstances!
for instance, following code could not be run on my machine (Windows 7 x64, AutoCAD 2012 - English) but every other faces are being generated without any problem, I don't understand what's wrong with this particular face!
Any idea/suggestion?

face = new Face(new Autodesk.AutoCAD.Geometry.Point3d(249111.163422751, 15107.1921285706, 567684.207116981), new Autodesk.AutoCAD.Geometry.Point3d(249073.772313812, 15111.1612905044, 567682.875008800), new Autodesk.AutoCAD.Geometry.Point3d(249110.672949469, 15113.8711037982, 567682.875008800), true, true, true, true);
surface = new Autodesk.AutoCAD.DatabaseServices.Surface();
surface = Autodesk.AutoCAD.DatabaseServices.Surface.CreateFrom(face);
Reply
07/15/2012 at 02:38 PM

---
**内容**: Balaji said in reply to Afshin...
Hi Afshin,
Sorry for the delay in replying to your comment.
I have seen such issues when using large coordinates. One possible workaround is to move the face closer to the origin and then mesh it. After the meshing, you can move it back to its original position.
Please try this :
Point3d p1 = new Point3d(249111.163422751, 15107.1921285706, 567684.207116981);
Point3d p2 = new Point3d(249073.772313812, 15111.1612905044, 567682.875008800);
Point3d p3 = new Point3d(249110.672949469, 15113.8711037982, 567682.875008800);
Autodesk.AutoCAD.DatabaseServices.Face face = new Autodesk.AutoCAD.DatabaseServices.Face(p1, p2, p3, true, true, true, true);
face.TransformBy(Matrix3d.Displacement(p1 - Point3d.Origin));
Hope this helps.
Reply
07/16/2012 at 05:47 PM

---
**内容**: Afshin said...
Hi Balaji,
Thanks for the answer,
I actually did the same workaround after posting the question. yes, this worked.
I have another issue which you may have faced as well...
I have a face with narrow two angles and one wide one. I could create face object but failed creating the surface. with eInvalidInput error.
the only workaround I thought is to divide the triangle into parts, could do that and surfaces created successfully, but at the end, the solid3d couldn't create solid object with resultant surfaces...
basically I'm converting a mesh to 3dsolid, reading vertexes, faces and creating face/surface object then creating solid by passing surface[]. am I on the right track?!
Reply
07/16/2012 at 07:22 PM

---
**内容**: Balaji said in reply to Afshin...
Hi Afshin,
I find that my colleague has just answered to your request which was created through the DevHelp. Since this query is not directly related to this post, I suggest you to continue the discussion as part of the ADN request.
Reply
07/17/2012 at 02:51 AM

---
**内容**: ali said...
Hi Balaji,
I experience memory not being freed up in the above routine(having the second using block commented out)
in Autocad 2016-17. I have posted the issue in the forum here too. Could consider looking at it? thanks.Ali
https://forums.autodesk.com/t5/net/memory-no-freed-up-in-surface-createfrom-in-autocad-2016-17/td-p/7245209
Reply
07/21/2017 at 08:04 AM

---
**内容**: ali said...
Even removing this line:
Autodesk.AutoCAD.DatabaseServices.Surface surface = new Autodesk.AutoCAD.DatabaseServices.Surface();
didn't help. It sounds like a memory leak in Autocad to me, is that right?
Reply
07/24/2017 at 01:28 AM

---
