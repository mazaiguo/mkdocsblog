---
title: "Facet SubD Mesh"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Palette
description: "If you want to get back the facet geometry of an AcDbSubDMesh entity (simply called “Mesh” in the Properties palette), then you can use either getF..."
author: Autodesk
---
# Facet SubD Mesh

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/facet-subd-mesh.html

## 文章内容

By Adam Nagy
If you want to get back the facet geometry of an AcDbSubDMesh entity (simply called “Mesh” in the Properties palette), then you can use either getFaceArray (Returns Level 0 (base) mesh face list array) or getSubDividedFaceArray (Returns smoothed mesh face list array).
The below sample code uses the latter.
void
drawSubDMeshFacets()
{
  ads_name name;
  AcGePoint3d pt;
    int ret = acedEntSel(
    _T("\nSelect a SubD Mesh: "), name, asDblArray(pt));
    if (ret != RTNORM)
  {
      acutPrintf(_T("\nNothing selected"));
      return;
  }
    AcDbObjectId id;
  acdbGetObjectId(id, name);
    if (id.objectClass() != AcDbSubDMesh::desc())
  {
      acutPrintf(_T("\nSelected entity is not a SubD Mesh"));
      return;
  }
    AcDbObjectPointer<AcDbSubDMesh> mesh(id, AcDb::kForRead);
    AcGePoint3dArray vertices;
  mesh->getSubDividedVertices(vertices);
    AcArray<Adesk::Int32> faces;
  mesh->getSubDividedFaceArray(faces);
    // The content of the faces list is like so:
  // [number of vertices of next face],
  // <vertexIndex1, vertexIndex2, etc>,
  // e.g. [4], <1, 2, 3, 4>, [3], <1, 2, 3>, etc
    AcDbDatabase * pDb =
    acdbHostApplicationServices()->workingDatabase();
  AcDbBlockTableRecordPointer
    ms(ACDB_MODEL_SPACE, pDb, AcDb::kForWrite);
    for (int numVertices = 0, i = 0;
    i < faces.length(); i += numVertices + 1)
  {
    numVertices = faces.at(i);
      // Let's draw the edges of the face
    for (int j = 0; j < numVertices; j++)
    {
      AcGePoint3d pt1 =
        vertices.at(faces.at(i + j + 1));
      AcGePoint3d pt2 =
        vertices.at(faces.at(i + ((j + 1) % numVertices) + 1));
        AcDbObjectPointer<AcDbLine> line;
      line.create();
      line->setStartPoint(pt1);
      line->setEndPoint(pt2);
        ms->appendAcDbEntity(line);
    }
  }
}

