---
title: "Vertex color for a SubDMesh"
date: 2013-09-01
categories:
  - AutoCAD
tags:
  - Database
description: "To assign per-vertex colors for a SubDMesh, the subDMesh entity must be added to the database before the "AcDbSubDMesh::setVertexColorArray" can be..."
author: Autodesk
---
# Vertex color for a SubDMesh

发布日期: 2013-09-01

原始链接: https://adndevblog.typepad.com/autocad/2013/09/vertex-color-for-a-subdmesh.html

## 文章内容

By Balaji Ramamoorthy
To assign per-vertex colors for a SubDMesh, the subDMesh entity must be added to the database before the "AcDbSubDMesh::setVertexColorArray" can be used. Here is a sample code :
// Vertex color
AcCmEntityColor vColor;
vColor.setColorMethod(AcCmEntityColor::kByACI);
  AcArray<AcCmEntityColor> clrArray;
  // Vertices
AcGePoint3dArray vertexArray;
vertexArray.setPhysicalLength(4);
  // Vertex-1
AcGePoint3d pt1(0.0, 0.0, 0.0);
vertexArray.append(pt1);
vColor.setColorIndex(1); // Red
clrArray.append(vColor);
  // Vertex-2
AcGePoint3d pt2(20.0, 0.0, 0.0);
vertexArray.append(pt2);
vColor.setColorIndex(3); // Green
clrArray.append(vColor);
  // Vertex-3
AcGePoint3d pt3(20.0, 10.0, 0.0);
vertexArray.append(pt3);
vColor.setColorIndex(2); // Yellow
clrArray.append(vColor);
  // Vertex-4
AcGePoint3d pt4(0.0, 10.0, 0.0);
vertexArray.append(pt4);
vColor.setColorIndex(5); // Blue
clrArray.append(vColor);
  // Faces
AcArray<Adesk::Int32> faceArray;
faceArray.setPhysicalLength(8);
  // Face-1 (Vertex-1 Vertex-2 Vertex-4)
faceArray.append(3);
faceArray.append(0);faceArray.append(1);faceArray.append(3);
  // Face-2 (Vertex-2 Vertex-3 Vertex-4)
faceArray.append(3);
faceArray.append(1);faceArray.append(2);faceArray.append(3);
  AcDbSubDMesh *pSubDMesh = new AcDbSubDMesh();
Acad::ErrorStatus es = pSubDMesh->setSubDMesh
                                (vertexArray, faceArray, 0);
  AcDbBlockTable *pBlockTable;
AcDbBlockTableRecord *pSpaceRecord;
  es = acdbHostApplicationServices()->workingDatabase()
                ->getSymbolTable(pBlockTable, AcDb::kForRead);
es = pBlockTable
    ->getAt(ACDB_MODEL_SPACE, pSpaceRecord, AcDb::kForWrite);
es = pBlockTable->close();
  // For Vertex color to work, the SubDMesh must be added
// to the database
AcDbObjectId meshId = AcDbObjectId::kNull;
es = pSpaceRecord->appendAcDbEntity(meshId, pSubDMesh);
  es = pSubDMesh->setVertexColorArray(clrArray);
  es = pSubDMesh->close();
  es = pSpaceRecord->close();
Here is the SubDMesh created by the sample code :

