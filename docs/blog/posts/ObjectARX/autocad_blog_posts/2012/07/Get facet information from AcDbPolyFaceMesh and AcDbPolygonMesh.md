---
title: "Get facet information from AcDbPolyFaceMesh and AcDbPolygonMesh"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
description: "I'd like to get facet information from polygon and polyface mesh entities. Do you have a sample for that?"
author: Autodesk
---
# Get facet information from AcDbPolyFaceMesh and AcDbPolygonMesh

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/get-facet-information-from-acdbpolyfacemesh-and-acdbpolygonmesh.html

## 文章内容

By Adam Nagy
I'd like to get facet information from polygon and polyface mesh entities. Do you have a sample for that?
Solution
The following code samples draw lines crossing each facet of the selected polygon mesh or polyface mesh entity.
static void AEN1ArxAcDbPolyFaceMesh_PolyFace(void)
{
  int ret;
  ads_name name;
  ads_point pt;
    if (acedEntSel(_T("Select Poly Face Mesh\n"), name, pt) != RTNORM)
    return;
    AcDbObjectId id;
  if(acdbGetObjectId(id, name) != Acad::eOk)
    return;
    AcDbObjectPointer<AcDbPolyFaceMesh> mesh(id, AcDb::kForRead); 
  if (mesh.openStatus() != Acad::eOk)
    return;
    AcArray<AcDbObjectId> vertexIds;
  AcArray<AcDbLine*> lines;
  AcDbObjectIterator * iter = mesh->vertexIterator();
  for (; !iter->done(); iter->step())
  {
    if (iter->objectId().objectClass() ==
      AcDbPolyFaceMeshVertex::desc())
    {
      vertexIds.append(iter->objectId()); 
        // You could get the vertex positions from here as well
      // instead of collecting the ObjectId's of the vertices
    }
    else if (iter->objectId().objectClass() ==
      AcDbFaceRecord::desc())
    {
      // Get vertices from the face record
        AcDbObjectPointer<AcDbFaceRecord>
        face(iter->objectId(), AcDb::kForRead);
      AcGePoint3d pts[4];
      for (Adesk::UInt16 i = 0; i < 4; i++)
      {
        // Vertex index starts with 1, and that will be at 0 index
        // in the list so we need to deduct 1 from it.
        // The returned index will be negative if
        // it is hidden so turn it into positive using abs()
          Adesk::Int16 vertexIndex;
        if (face->getVertexAt(i, vertexIndex) == Acad::eOk)
        {
          AcDbObjectPointer<AcDbPolyFaceMeshVertex>
            vertex(vertexIds[abs(vertexIndex) - 1], AcDb::kForRead);
          pts[i] = vertex->position();
        }
      }
        // Create two lines crossing the face for testing purposes
        AcDbLine * line1 = new AcDbLine(pts[0], pts[2]);
      AcDbLine * line2 = new AcDbLine(pts[1], pts[3]);
      lines.append(line1);
      lines.append(line2);
    }
  }
    delete iter;
    // Add the test lines to the model space
    AcDbDatabase * pDb =
    acdbHostApplicationServices()->workingDatabase();
  AcDbBlockTableRecordPointer
    ms(ACDB_MODEL_SPACE, pDb, AcDb::kForWrite);
    for (int i = 0; i < lines.length(); i++)
  {
    ms->appendAcDbEntity(lines[i]);
    lines[i]->close();
  }
}
  static void AEN1ArxAcDbPolyFaceMesh_Polygon(void)
{
  int ret;
  ads_name name;
  ads_point pt;
    if (acedEntSel(_T("Select Polygon Mesh\n"), name, pt) != RTNORM)
    return;
    AcDbObjectId id;
  if(acdbGetObjectId(id, name) != Acad::eOk)
    return;
    AcDbObjectPointer<AcDbPolygonMesh> mesh(id, AcDb::kForRead); 
  if (mesh.openStatus() != Acad::eOk)
    return;
    Adesk::Int16 M;
  Adesk::Int16 N;
    if (mesh->polyMeshType() == AcDb::kSimpleMesh)
  {
    M = mesh->mSize();
    N = mesh->nSize();    
  }
  else
  {
    M = mesh->mSurfaceDensity();
    N = mesh->nSurfaceDensity();    
  }
    // Collect the points
    AcArray<AcGePoint3d> pts;
    AcDbObjectIterator * iter = mesh->vertexIterator();
  Adesk::Int16 m = 0, n = 0;
  for (int i = 0; !iter->done(); iter->step(), i++)
  {
    if (iter->objectId().objectClass() ==
      AcDbPolygonMeshVertex::desc())
    {
      AcDbObjectPointer<AcDbPolygonMeshVertex>
        vertex(iter->objectId(), AcDb::kForRead);
        if (vertex->vertexType() == AcDb::k3dSimpleVertex ||
          vertex->vertexType() == AcDb::k3dFitVertex
         )
        pts.append(vertex->position());
    }
  }
    delete iter;
    // Create the crossing lines
    AcArray<AcDbLine*> lines;
    for (m = 0; m < M - 1; m++)
    for (n = 0; n < N - 1; n++)
    {
      // The indices of vertices of the face can easily
      // be calculated. If the top left is m and n, then the
      // top right is m, n + 1
      // bottom right is m + 1, n + 1,
      // and bottom left is m + 1, n
        AcDbLine * line1 =
        new AcDbLine(
          pts[(m * N) + (n)],
          pts[((m + 1) * N) + (n + 1)]);
      AcDbLine * line2 =
        new AcDbLine(
          pts[((m + 1) * N) + (n)],
          pts[(m * N) + (n + 1)]);
      lines.append(line1);
      lines.append(line2);
    }
    // Add the test lines to the model space
    AcDbDatabase * pDb = acdbHostApplicationServices()->workingDatabase();
  AcDbBlockTableRecordPointer ms(ACDB_MODEL_SPACE, pDb, AcDb::kForWrite);
    for (int i = 0; i < lines.length(); i++)
  {
    ms->appendAcDbEntity(lines[i]);
    lines[i]->close();
  }
}

## 评论

**内容**: Konstantin said...
Is it possible to do the same using the C# .NET API?
If yes, is there a sample ?
Reply
07/26/2012 at 06:34 AM

---
**内容**: Adam Nagy said...
Hi Konstantin,
I was not aware of a sample, so I migrated the poly face mesh part to .NET:
http://adndevblog.typepad.com/autocad/2012/07/get-facet-information-from-polyfacemesh.html
Cheers,
Adam
Reply
07/26/2012 at 11:06 AM

---
**内容**: Konstantin said in reply to Adam Nagy...
Hi Adam,
thanks for your response !
I am going to test it asap...
Best Regards
Konstantin
Reply
07/27/2012 at 12:26 AM

---
**内容**: Matt Kincaid said...
Helpful post! Could you explain why in the polygonMesh routine you only append vertices if the vertex type is a SimpleVertex or a FitVertex?
I've spent several hours trying to figure out why my PolygonMesh parsing methods weren't working. Then I added the VertexType check and it worked! But I don't understand why...
Many thanks!
Reply
03/22/2018 at 04:05 PM

---
