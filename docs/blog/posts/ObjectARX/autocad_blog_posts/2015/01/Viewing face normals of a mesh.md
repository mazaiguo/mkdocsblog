---
title: "Viewing face normals of a mesh"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Recently I had a drawing sent over by a developer which had a SubDMesh that was created through code using vertex and face information. In such mes..."
author: Autodesk
---
# Viewing face normals of a mesh

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/viewing-face-normals-of-a-mesh.html

## 文章内容

By Balaji Ramamoorthy
Recently I had a drawing sent over by a developer which had a SubDMesh that was created through code using vertex and face information. In such meshes, the normals of the faces would depend on the order of vertices while defining the face vertices, so wanted to check if the normals were all ok.
Just in case you would like to view the normals for a mesh, here is the code snippet to show the normals of the facets. This blog post by my colleague Adam Nagy draws the edges of the mesh which formed the basis for this code snippet. 
 Acad::ErrorStatus es;
   ads_name name;
 AcGePoint3d pt;
    int  ret = acedEntSel(
 _T("\\nSelect a SubD Mesh: " ), name, asDblArray(pt));
    if  (ret != RTNORM)
 {
  acutPrintf(_T("\\nNothing selected" ));
  return ;
 }
    AcDbObjectId id;
 acdbGetObjectId(id, name);
    if  (id.objectClass() != AcDbSubDMesh::desc())
 {
  acutPrintf(
   _T("\\nSelected entity is not a SubD Mesh" ));
  return ;
 }
   AcDbObjectPointer<AcDbSubDMesh> mesh(
      id, AcDb::kForRead);
    AcDbFullSubentPathArray subentPaths;
 es = mesh->getSubentPath(-1,
   kFaceSubentType, subentPaths);
   AcGePoint3dArray vertices;
 es = mesh->getSubDividedVertices(vertices);
    AcArray<Adesk::Int32> faceInfo;
 es = mesh->getSubDividedFaceArray(faceInfo);
   // The content of the faces list is like so: 
 // [number of vertices of next face], 
 // <vertexIndex1, vertexIndex2, etc>, 
 // e.g. [4], <1, 2, 3, 4>, [3], <1, 2, 3>, etc 
    AcDbDatabase * pDb =
 acdbHostApplicationServices()->workingDatabase();
 AcDbBlockTableRecordPointer
 ms(ACDB_MODEL_SPACE, pDb, AcDb::kForWrite);
    AcDbVoidPtrArray lineArray;
 int  face = 0;
 int  numVerticesInFace = 0;
 for  (int  i = 0; i < faceInfo.length(); 
  i += numVerticesInFace + 1, face++)
 {
  numVerticesInFace = faceInfo.at(i);
    AcGePlane facePlane;
  es = mesh->getFacePlane(
   subentPaths.at(face).subentId(), 
   facePlane);
    AcGeBoundBlock3d boundBox;
  for  (int  j = 0; j < numVerticesInFace; j++)
  {
   AcGePoint3d pt1 =
   vertices.at(faceInfo.at(i + j + 1));
   AcGePoint3d pt2 =
   vertices.at(
   faceInfo.at(i + ((j + 1) % numVerticesInFace) + 1));
      if (j == 0)
    boundBox.set(pt1, pt2);
   else 
   {
    boundBox.extend(pt1);
    boundBox.extend(pt2);
   }
         // If the edges are also required 
   //AcDbObjectPointer<AcDbLine> line; 
   //line.create(); 
   //line->setStartPoint(pt1); 
   //line->setEndPoint(pt2); 
   //ms->appendAcDbEntity(line); 
  }
    AcGePoint3d minPt;
  AcGePoint3d maxPt;
  boundBox.getMinMaxPoints(minPt, maxPt);
  AcGeVector3d normalLen = maxPt - minPt;
    AcGeVector3d normal = facePlane.normal();
         // Arrow 
  AcDbLine *pArrow = new  AcDbLine;
  pArrow->setColorIndex(2);
    AcGePoint3d sp = minPt + normalLen * 0.5;
  pArrow->setStartPoint(sp);
    AcGePoint3d ep = sp 
   + normal.normalize() * normalLen.length();
  pArrow->setEndPoint(ep);
    ms->appendAcDbEntity(pArrow);
  pArrow->close();
    // Arrow head 
  double  arrowLen = normalLen.length() * 0.2;
  AcDb3dSolid *pArrowHead = new  AcDb3dSolid;
  es = pArrowHead->createFrustum(
   arrowLen, 
   arrowLen / 3.0, 
   arrowLen / 3.0, 
   0.0);
       AcGeVector3d zd = (ep - sp).normalize();
  AcGeVector3d yd = zd.perpVector().normalize();
  AcGeVector3d xd = yd.crossProduct(zd).normalize();
  AcGeMatrix3d mat;
  mat.setCoordSystem(ep, xd, yd, zd);
  pArrowHead->transformBy(mat);
       ms->appendAcDbEntity(pArrowHead);
  pArrowHead->close();
 }
  Here is a screenshot of the normals for a simple box mesh :

## 评论

**内容**: Arifin said...
I am not familiar with the command mesh , here I can learn a lot about it.Thanks .
Reply
01/16/2015 at 12:37 AM

---
