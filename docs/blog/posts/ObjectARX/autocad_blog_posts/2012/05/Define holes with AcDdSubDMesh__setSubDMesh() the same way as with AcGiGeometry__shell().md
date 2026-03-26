---
title: "Define holes with AcDdSubDMesh::setSubDMesh() the same way as with AcGiGeometry::shell()"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Solid
description: "I know how to set AcGiFaceData for AcGiGeometry::shell() to define holes. I'm trying to do the same with AcDbSubDMesh::setSubDMesh(), but that does..."
author: Autodesk
---
# Define holes with AcDdSubDMesh::setSubDMesh() the same way as with AcGiGeometry::shell()

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/define-holes-with-acddsubdmeshsetsubdmesh-the-same-way-as-with-acgigeometryshell.html

## 文章内容

By Adam Nagy
I know how to set AcGiFaceData for AcGiGeometry::shell() to define holes. I'm trying to do the same with AcDbSubDMesh::setSubDMesh(), but that does not seem to work. Is it not possible to do that?
Solution
No it isn't. You need to divide your manifold into faces without holes and set up the face data for AcDbSubDMesh::setSubDMesh() accordingly.
Another thing that might be helpful is using AcDb3dSolid entities, create the holes in them using boolean operations and then create an AcDbSubDMesh from that:
static void AcDbSubDMeshfromAcDb3dSolid(void)
{
  Acad::ErrorStatus err;
    ads_name name;
  ads_point pt;
  if (acedEntSel(L"Select a solid", name, pt) != RTNORM)
    return;
    AcDbObjectId id;
  acdbGetObjectId(id, name);
  AcDbObjectPointer<AcDb3dSolid> ptrSolid(id, AcDb::kForRead);
    AcDbFaceterSettings settings;
  AcGePoint3dArray pts;
  AcArray faces;
  AcGiFaceData* faceData;
  err = acdbGetObjectMesh(ptrSolid, &settings, pts, faces, faceData);
  if (faceData)
  {
    delete [] faceData->trueColors();
    delete [] faceData->materials();
    delete faceData;
  }
    AcDbObjectPointer<AcDbSubDMesh> ptrMesh;
  ptrMesh.create();
  ptrMesh->setSubDMesh(pts, faces, 0);
    AcDbDatabase* pDb =
    acdbHostApplicationServices()->workingDatabase();
  AcDbBlockTableRecordPointer
    ptrMS(ACDB_MODEL_SPACE, pDb, AcDb::kForWrite);
  ptrMS->appendAcDbEntity(ptrMesh);
}

