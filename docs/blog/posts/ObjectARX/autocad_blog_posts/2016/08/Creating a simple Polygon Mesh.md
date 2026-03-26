---
title: "Creating a simple Polygon Mesh"
date: 2016-08-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "Here is a sample code to create a simple Polygon mesh using ObjectARX. When AcDbPolygonMesh() constructor is used without any parameters,vertex cou..."
author: Autodesk
---
# Creating a simple Polygon Mesh

发布日期: 2016-08-01

原始链接: https://adndevblog.typepad.com/autocad/2016/08/creating-a-simple-polygon-mesh.html

## 文章内容

By Deepak Nadig
Here is a sample code to create a simple Polygon mesh using ObjectARX. When AcDbPolygonMesh() constructor is used without any parameters,vertex count in M and N directions has to be set explicitly and it needs to be specified if PolygonMesh is to be open or closed in M and N directions. 
void createSimplePolygonMesh() 
{
 // polyline creation 
 AcGePoint3dArray ptArr;
 ptArr.setLogicalLength(4);
 for (int i = 0; i < 4; i++) 
 {
 ptArr[i].set((double)(i/2), (double)(i%2), 0.0);
 }
 AcDb2dPolyline *pNewPline = new AcDb2dPolyline( AcDb::k2dSimplePoly, ptArr, 0.0, Adesk::kTrue);
 pNewPline->setColorIndex(3);
//polygon mesh constructor without any parameter
 AcDbPolygonMesh *pMesh = new AcDbPolygonMesh(); 
 pMesh->setMSize(1);
 pMesh->setNSize(4);
 pMesh->makeMClosed();
 pMesh->makeNClosed();
AcDbVoidPtrArray arr; 
 arr.append(pMesh);
AcDbBlockTable *pBlockTable;
 acdbHostApplicationServices()->workingDatabase()->getSymbolTable(pBlockTable, AcDb::kForRead);
AcDbBlockTableRecord *pBlockTableRecord;
 pBlockTable->getAt(ACDB_MODEL_SPACE, pBlockTableRecord,AcDb::kForWrite);
 pBlockTable->close();
AcDbObjectId plineObjId;
 pBlockTableRecord->appendAcDbEntity(plineObjId,pNewPline);
AcDbObjectIterator *pVertIter= pNewPline->vertexIterator();
 AcDb2dVertex *pVertex;
 AcGePoint3d location;
 AcDbObjectId vertexObjId; 
 for (int vertexNumber = 0; !pVertIter->done();
 vertexNumber++, pVertIter->step())
 {
 vertexObjId = pVertIter->objectId();
 acdbOpenObject(pVertex, vertexObjId,
 AcDb::kForRead);
 location = pVertex->position();
 pVertex->close(); 
 AcDbPolygonMeshVertex* polyVertex = new AcDbPolygonMeshVertex(pVertex->position()); 
 pMesh->appendVertex(polyVertex);
 polyVertex->close();
 }
 delete pVertIter;
pBlockTableRecord->appendAcDbEntity(pMesh);
 pBlockTableRecord->close();
 pNewPline->close();
 pMesh->close(); 
}

