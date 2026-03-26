---
title: "Drawing a Box with Meshes Programmatically"
date: 2015-11-01
categories:
  - AutoCAD
tags:
  - Surface
description: "A PolygonMesh is an M x N mesh, where M represents the number of vertices in a row of the mesh and N represents the number of vertices in a column ..."
author: Autodesk
---
# Drawing a Box with Meshes Programmatically

发布日期: 2015-11-01

原始链接: https://adndevblog.typepad.com/autocad/2015/11/drawing-a-box-with-meshes-programmatically.html

## 文章内容

By Madhukar Moogala
A PolygonMesh is an M x N mesh, where M represents the number of vertices in a row of the mesh and N represents the number of vertices in a column of the mesh.
A mesh can be open or closed in either or both the M and N directions. A mesh that is closed in a given direction is considered to be continuous from the last row or column on to the first row or column.
All the vertices in the mesh are stored in a single list. For a non-surface-fit mesh, the first N vertices are used to make up the first column, the second N vertices are used to make up the second column, and so on until all the vertices are used up (there do not have to be enough vertices to fully fill the M x N mesh).
For a surface-fit mesh, the surface density values are used in place of M and N for the vertex row x column sizes.
Mclosed
This function sets the PolygonMesh to be closed in the M direction. This means that the mesh will be treated as continuous from the last row on to the first row.
N Closed
This function sets the PolygonMesh to be closed in the N direction. This means that the mesh will be treated as continuous from the last column on to the first column.
For following code:
using (PolygonMesh acPolyMesh = new PolygonMesh())
    {
     acPolyMesh.MSize = 4;
     acPolyMesh.NSize = 4;
     acBlkTblRec.AppendEntity(acPolyMesh);
     acTrans.AddNewlyCreatedDBObject(acPolyMesh, true);
     Point3dCollection acPts3dPMesh = new Point3dCollection();
     acPts3dPMesh.Add(new Point3d(0, 0, 0));
     acPts3dPMesh.Add(new Point3d(2, 0, 1));
     acPts3dPMesh.Add(new Point3d(4, 0, 0));
     acPts3dPMesh.Add(new Point3d(6, 0, 1));
     acPts3dPMesh.Add(new Point3d(0, 2, 0));
     acPts3dPMesh.Add(new Point3d(2, 2, 1));
     acPts3dPMesh.Add(new Point3d(4, 2, 0));
     acPts3dPMesh.Add(new Point3d(6, 2, 1));
     acPts3dPMesh.Add(new Point3d(0, 4, 0));
     acPts3dPMesh.Add(new Point3d(2, 4, 1));
     acPts3dPMesh.Add(new Point3d(4, 4, 0));
     acPts3dPMesh.Add(new Point3d(6, 4, 0));
     acPts3dPMesh.Add(new Point3d(0, 6, 0));
     acPts3dPMesh.Add(new Point3d(2, 6, 1));
     acPts3dPMesh.Add(new Point3d(4, 6, 0));
     acPts3dPMesh.Add(new Point3d(6, 6, 0));
     foreach (Point3d acPt3d in acPts3dPMesh)
     {
      PolygonMeshVertex acPMeshVer = new PolygonMeshVertex(acPt3d);
      acPolyMesh.AppendVertex(acPMeshVer);
      acTrans.AddNewlyCreatedDBObject(acPMeshVer, true);
     }
    }
I can generate following mesh with 4 rows of vertices and 4 coloumns of vertices with M open and N open
To get Box like Polygon Mesh
 
public void TestSimpleMesh()
{
// Get the current document and database, and start a transaction
Database _database = HostApplicationServices.WorkingDatabase;
Document acDoc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Database acCurDb = acDoc.Database;
using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
{
BlockTable acBlkTbl = acTrans.GetObject(_database.BlockTableId, OpenMode.ForRead) as BlockTable;
// Open the Block table record for read
BlockTableRecord acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace], OpenMode.ForWrite) as BlockTableRecord; 
// Open the Block table record Model space for write
// Create a polygon mesh
PolygonMesh acPolyMesh = new PolygonMesh();
   
/*M indicates No of rows and N indicates No of columns, visualize it as Grid
So to have cube, we need two rows of vertices and 4 colomns of vertices
    
No we need to close last column of vertices with first column of vertices that makes a simple cube or else planar surface with facets.
     
*/
acPolyMesh.MSize = 2;
acPolyMesh.NSize = 4;
acPolyMesh.MakeNClosed(); 
//What is N???    
/*
* 
*/
//acPolyMesh.MakeMClosed(); 
//What is M???
/*
This function sets the PolygonMesh to be closed in the M direction.
 This means that the mesh will be treated as continuous from the last row on to the first row.
  */
// Add the new object to the block table record and the transaction        
acBlkTblRec.AppendEntity(acPolyMesh);
acTrans.AddNewlyCreatedDBObject(acPolyMesh, true);
//Creating collection of points to add to the mesh
Point3dCollection acPts3dPMesh = new Point3dCollection();
acPts3dPMesh.Add(new Point3d(100, 100, 0));
acPts3dPMesh.Add(new Point3d(200, 100, 0));
acPts3dPMesh.Add(new Point3d(200, 200, 0));
acPts3dPMesh.Add(new Point3d(100, 200, 0));
acPts3dPMesh.Add(new Point3d(100, 100, 100));
acPts3dPMesh.Add(new Point3d(200, 100, 100));
acPts3dPMesh.Add(new Point3d(200, 200, 100));
acPts3dPMesh.Add(new Point3d(100, 200, 100));
//Converting those points to PolygonMeshVertecies and appending them to the PolygonMesh
foreach (Point3d acPt3d in acPts3dPMesh)
{
PolygonMeshVertex acPMeshVer = new PolygonMeshVertex(acPt3d);
acPolyMesh.AppendVertex(acPMeshVer);
acTrans.AddNewlyCreatedDBObject(acPMeshVer, true);
}
// Save the new objects to the database        
acTrans.Commit();
}
} 
 
And following mesh is generated when makeNClosed, for details check in comments of above code;

