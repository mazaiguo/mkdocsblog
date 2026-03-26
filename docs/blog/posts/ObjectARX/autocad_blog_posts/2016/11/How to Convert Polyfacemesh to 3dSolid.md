---
title: "How to Convert Polyfacemesh to 3dSolid"
date: 2016-11-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Solid
description: "We have an inbuilt AutoCAD command CONVTOSOLID, but this command is very limited doesn’t work effectively on"
author: Autodesk
---
# How to Convert Polyfacemesh to 3dSolid

发布日期: 2016-11-01

原始链接: https://adndevblog.typepad.com/autocad/2016/11/how-to-convert-polyfacemesh-to-3dsolid.html

## 文章内容

By Madhukar Moogala
We have an inbuilt AutoCAD command CONVTOSOLID, but this command is very limited doesn’t work effectively on
Polyfacemesh <AcDbPolyFaceMesh> entities.
We will create an in-memory subDMesh <AcDbSubDMesh> object from pfmesh [read as Polyfacemesh], first we will extract vertex and face information from pfmesh and use this information in constructing a subDMesh, convert this mesh object solid using convertToSolid API.
Before we get in to this, if you must know commands and their meaning while working on Meshs.
You can find full glossary at MeshPrimitives, a quick reference for the reader is below:
DIVMESHBOXWIDTH: Sets the number of subdivisions for the width of a mesh box along the Y axis.
DIVMESHBOXHEIGHT : Sets the number of subdivisions for the height of a mesh box along the Z axis.
DIVMESHCONEAXIS : Sets the number of subdivisions around the perimeter of the mesh cone base.
DIVMESHCONEHEIGHT : Sets the number of subdivisions between the base and the point or top of the mesh cone.
DIVMESHCONEBASE : Sets the number of subdivisions between the perimeter and the center point of the mesh cone base.
DIVMESHCYLAXIS : Sets the number of subdivisions around the perimeter of the mesh cylinder base.
DIVMESHCYLHEIGHT : Sets the number of subdivisions between the base and the top of the mesh cylinder.
DIVMESHCYLBASE : Sets the number of radial subdivisions from the center of the mesh cylinder base to its perimeter.
DIVMESHPYRLENGTH : Sets the number of subdivisions along each dimension of a mesh pyramid base.
DIVMESHPYRHEIGHT : Sets the number of subdivisions between the base and the top of the mesh pyramid.
DIVMESHPYRBASE : Sets the number of radial subdivisions between the center of the mesh pyramid base and its perimeter.
DIVMESHSPHEREAXIS : Sets the number of radial subdivisions around the axis endpoint of the mesh sphere.
DIVMESHSPHEREHEIGHT : Sets the number of subdivisions between the two axis endpoints of the mesh sphere.
DIVMESHWEDGELENGTH : Sets the number of subdivisions for the length of a mesh wedge along the X axis.
DIVMESHWEDGEWIDTH : Sets the number of subdivisions for the width of the mesh wedge along the Y axis.
DIVMESHWEDGEHEIGHT : Sets the number of subdivisions for the height of the mesh wedge along the Z axis.
DIVMESHWEDGESLOPE : Sets the number of subdivisions in the slope that extends from the apex of the wedge to the edge of the base.
DIVMESHWEDGEBASE : Sets the number of subdivisions between the midpoint of the perimeter of triangular dimension of the mesh wedge.
DIVMESHTORUSSECTION : Sets the number of subdivisions in the profile that sweeps the path of a mesh torus.
DIVMESHTORUSPATH : Sets the number of subdivisions in the path that is swept by the profile of a mesh torus
We have an API
AcDbSubDMesh::setSubDMesh which creates Mesh entity for a given vertex array and face array,  first we will try to understand about vertex array and face array
What is vertex array ?
An array of vertex points that makes each face.
What is Face array ?
The face Array defines an array of faces, and each face is defined by a set of numbers. The first number specifies the number of vertices in the face, the following numbers are the indices of the vertices making up the face. 
  Face array F[] = {N0,a0,...,aN0,N1,b0,...,bN1} Where N0 is Number of vertices in that particular face and a0,...,aN0 are the corresponding vertex indices in the Vertex array
To illustrate :
Face array F[] for the above faces would be - {3, 0, 1, 2,     -3, 3, 4, 5,      3, 6, 7, 8};  A negative before a Number of vertices <for e.g.,-3> indicates the face is lying inside or a hole.
Code:
  void test4()
  {
  AcDbObjectId entId;
  ads_name ent_name;
  AcGePoint3d pickPnt;
    if (acedEntSel(_T("\n Pick a PFACE\n"), ent_name,
          asDblArray(pickPnt)) != RTNORM) return;
  if (!eOkVerify(acdbGetObjectId(entId, ent_name))) return;
  AcDbSmartObjectPointer<AcDbPolyFaceMesh> pFace(entId, AcDb::kForWrite);
  // polyface mesh
  if (!eOkVerify(pFace.openStatus())) return;
    AcGePoint3dArray vertexArray;
  AcArray<Adesk::Int32> faceArray;
  AcArray<AcCmColor> colorArray;
  AcArray<AcDbObjectId> materialArray;
  Acad::ErrorStatus es = GetPolyFaceMeshData(pFace, vertexArray, faceArray);
  if (es != eOk)
    return;
    /*Mesh Type ":
      Specifies the type of mesh to be used in the conversion. (FACETERMESHTYPE system variable)
      0 : Smooth Mesh Optimized. Sets the shape of the mesh faces to adapt to the shape of the mesh object.
      1 : Mostly Quads. Sets the shape of the mesh faces to be mostly quadrilateral.
      2 : Triangles. Sets the shape of the mesh faces to be mostly triangular.*/
  int faceterMeshType = 0;
  int nSmoothLevel = 0;
  int nMaxFaces = 0;
  resbuf rb;
  /*
  This variable sets the default level of smoothness that is applied to
  mesh that is created as a result of conversion from another object with the MESHSMOOTH command.
  The value cannot be greater than the value of SMOOTHMESHMAXLEV.
  */
  if (acedGetVar(_T("FACETERSMOOTHLEV"), &rb) == RTNORM)
  {
    nSmoothLevel = rb.resval.rint;
    nSmoothLevel = (nSmoothLevel < 0 ? 0 : nSmoothLevel);
  }       
  if (acedGetVar(_T("FACETERMESHTYPE"), &rb) == RTNORM)
  {
    faceterMeshType = rb.resval.rint;
  }
  int newSubdLevel = (faceterMeshType == 0) ? nSmoothLevel : 0;
  int oldSubdLevel = nSmoothLevel;
  // If oldSubdivLevel > SmoothMeshMaxLev, we need to reset oldSubdivLevel
  // value to SmoothMeshMaxLev.
  // If newSubdivLevel > SmoothMeshMaxLev, we need to reset newSubdivLevel
  // value to SmoothMeshMaxLev.
    //The valid range is from 1 to 255. The recommended range is 1 - 5.
  //Use this limit to prevent creating extremely dense meshes that might affect program performance.
  if (acedGetVar(_T("SMOOTHMESHMAXLEV"), &rb) == RTNORM)
  {
    int nMaxLevel = rb.resval.rint;
    if (nMaxLevel >= 0 && oldSubdLevel > nMaxLevel)
      oldSubdLevel = nMaxLevel;
    if (nMaxLevel >= 0 && newSubdLevel > nMaxLevel)
      newSubdLevel = nMaxLevel;
  }
  /*We create an in-memory mesh and convert mesh to solid*/
  AcDbSubDMesh* pSubDMesh = nullptr;
  if (!eOkVerify(CreateSubdMesh(vertexArray, faceArray, newSubdLevel, pSubDMesh)))
    return;
  pSubDMesh->setPropertiesFrom(pFace);   
  /*Create A solid and Convert SubDMesh to Solid*/
  AcDb3dSolid* pMeshSolid = new AcDb3dSolid();
  AcDbObjectId meshSolId;
  /*Now convert to Solid using CONVTOSOLID  API*/
  /*We will restrict to polygonal solid, we set false for smoothness, so not to abuse CPU*/
  pSubDMesh->convertToSolid(false, false, pMeshSolid);
  postToDatabase(NULL, pMeshSolid, meshSolId);
  /*Delete Pface */
  if (pFace)
  {
    pFace->erase();
  }
      }
Helper Methods
  /*Get the Mesh data, not accounted for Color and Material of Faces*/
  Acad::ErrorStatus GetPolyFaceMeshData(AcDbPolyFaceMesh* pMesh,
                       AcGePoint3dArray& vertexArray,
                       AcArray<Adesk::Int32>& faceArray)
  {
    if (pMesh == NULL)
      return eNullObjectPointer;
    const bool dbResident = (pMesh->database() != NULL);
    AcDbObjectIterator*  pIter = pMesh->vertexIterator();
    if (pIter == NULL)
      return eNullObjectPointer;
    Acad::ErrorStatus es;
    AcGePoint3d pt;
    AcDbVertex* pVtxObj = NULL;
    AcDbPolyFaceMeshVertex *pVertex = NULL;
    AcDbFaceRecord *pFaceRec = NULL; 
    int nFaces = pMesh->numFaces(); 
    for (; !pIter->done(); pIter->step())
    {
      if (acdbHostApplicationServices()->userBreak())
      {
        delete pIter;
        return eUserBreak;
      }
      if (dbResident)
      {
        es = acdbOpenObject(pVtxObj, pIter->objectId(), AcDb::kForRead);
        if (es != Acad::eOk)
          continue;
      }
      else
      {
        pVtxObj = (AcDbVertex*)pIter->entity();
      }
      // Build vertex list
      if ((pVertex = AcDbPolyFaceMeshVertex::cast(pVtxObj)) != NULL)
      {
        pt = pVertex->position();
        vertexArray.append(pt);
      }// Build face list   
      else if ((pFaceRec = AcDbFaceRecord::cast(pVtxObj)) != NULL)
      {
        int count = 0;
        Adesk::Int16 indices[4], newIndex =0;
        for (int i = 0; i < 4; i++)
        {
          pFaceRec->getVertexAt(i, indices[i]);
          if (indices[i] == 0)
            break;
          count++;
          }
        // Quick triangle test by checking if the first vertex
        // is the same as the last vertex
        if (count == 4 && (abs(indices[0]) == abs(indices[3])))
          count = 3;
          // Per face record can be a triangle or quad
        if (count > 2)
        {             
          faceArray.append(count);
          for (int i = 0; i < count; i++)
          {
            newIndex = abs(indices[i]) - 1;
              faceArray.append(newIndex);
          }
        }
      }
      if (dbResident)
        pVtxObj->close();
    }
    delete pIter;
    return eOk;
  }
    Acad::ErrorStatus CreateSubdMesh(AcGePoint3dArray& vertexArray,
              AcArray<Adesk::Int32>&  faceArray,
              int nSubdivLevel,
              AcDbSubDMesh*& poly)
    {
    if (vertexArray.length() <= 0 || faceArray.length() <= 0)
      return Acad::eCreateFailed;
    poly = new AcDbSubDMesh();
    ASSERT(poly != NULL);
    if (poly == NULL)
      return Acad::eCreateFailed;
    Acad::ErrorStatus es = poly->setSubDMesh(vertexArray, faceArray, nSubdivLevel);
    return es;
    }

## 评论

**内容**: Olivier B. said...
Thanks for the code.
1) may be a memory leak if you don't delete pSubDMesh after calling convertToSolid.
2) the resulting solid is very dependent on the many MeshPrimitives : first I tried to convert a simple "polyfacemesh-box" and the resulting solid was very different of a box.
=> instead of a AcDbSubDMesh, I prefer create a AcDbSurface and call AcDb3dSolid::createFrom
Reply
11/24/2016 at 05:51 AM

---
**内容**: Madhukar Moogala said...
Hi Olivier,
Thanks for your message, I have not done a lot of testing on this. I missed to delete pSubDMesh thanks for notifying.
Can you please share the drawing, I can see what's going on..
And if you set smoothness to true in ConvertToSolid API, the resulting topology of solid may be different from the expected one.
Reply
11/24/2016 at 09:05 PM

---
**内容**: Evangelos said...
Dear Madhukar,
thank you very much for the code it is very nicely explained.
However, I am facing a problem when I try to convert the subDMesh to 3dSolid.
I take an eInvalidContext error from the following function and I do not know why.
pSubDMesh->convertToSolid(false, false, pMeshSolid);
Do you have any idea why?
Kind regards,
Evangelos
Reply
11/20/2017 at 05:48 AM

---
**内容**: Madhukar Moogala said in reply to Evangelos...

Typepad HTML Email

Hi Thanks for your post,
 
Can you verify working on your MESH interactively?
 
https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-Core/files/GUID-45E37A82-3175-4F20-A5F7-316C46DBEBBB-htm.html
 
Or you can share the drawing, if there are any self-intersecting entities, operator may reject.
  Reply
11/20/2017 at 06:56 AM

---
**内容**: Evangelos said in reply to Madhukar Moogala...
What I am doing is to read a dxf file and print its geometric properties. In case of a polyface mesh, I would like to convert it to 3dSolid in order to use the Brep functionalities.
Interactively, you are right the object cannot be converted to solid. So, I think there is a problem with the drawing itself.
What I observed until now is that sometimes drawers use the block reference tool to create "3D" shapes. However, this makes the geometry reading through ObjectARX very hard. I encountered the following problems:
- When I encounter an AcDbBlockReference entity I cannot find any attributes for it.
- When you explode an AcDbBlockReference entity you end up with pFace meshes. Then, you encounter the problem you cannot convert them to solids.
You can find the drawing in the following link.
In addition, if you go to Insert-> Insert you will see the block references I mentioned.
https://www.dropbox.com/s/t38or2zb483oejr/polyface%20mesh.dwg?dl=0
I hope what I wrote is not out of topic.
Thank you very much for your interest!
Reply
11/21/2017 at 12:23 AM

---
**内容**: Madhukar Moogala said in reply to Evangelos...

Typepad HTML Email

Hi,
 
I have checked the drawing, I suspect the problem could be with one face, where it has overlapping vertices.
I highlighted in screenshot.
 
But to use Brep, you can convert it to pfacemesh to surface, apply AcBrMesh to surface instead of solid.
 
Explode the pFacemesh
CONVTOSURFACE on the faces you got from exploding.
Union
 
Now you will have single Surface entity, you can use AcBr library.
 
 
 
 
  Reply
11/21/2017 at 03:11 AM

---
**内容**: Madhukar Moogala said...
Hi,
I have checked the drawing, I suspect the problem could be with one face, where it has overlapping vertices.
I highlighted in screenshot.

get picture url
But to use Brep, you can convert it to pfacemesh to surface, apply AcBrMesh to surface instead of solid.
Explode the pFacemesh
CONVTOSURFACE on the faces you got from exploding.
Union
Now you will have single Surface entity, you can use AcBr library.
Reply
11/21/2017 at 01:53 AM

---
**内容**: Evangelos said...
Thank you very much Madhukar for solving my problem!
I will try to create an automated process in ObjectARX to handle this type of objects.
I think this would be a good enhancement for your robust code!
I will let you know if I succeeded!
Reply
11/22/2017 at 12:20 AM

---
**内容**: joan said...
Hi
do you know if its possible to join 3d faces that have in common vertices, just in that case. I mean to select a big amount of 3dfaces and to joint together just in the case that they share a edge.
im interesting in a routine that can do this, thanks, my email is jgonzalez@azvi.no
Reply
02/26/2021 at 04:19 AM

---
