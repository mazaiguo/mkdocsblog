---
title: "Merging coplanar faces of a SubDMesh"
date: 2012-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The faces of a SubDMesh can be merged together if they are coplanar using the "mergeFaces" method of the "AcDbSubDMesh" class. Here is sample code ..."
author: Autodesk
---
# Merging coplanar faces of a SubDMesh

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/merging-coplanar-faces-of-a-subdmesh.html

## 文章内容

By Balaji Ramamoorthy
The faces of a SubDMesh can be merged together if they are coplanar using the "mergeFaces" method of the "AcDbSubDMesh" class. Here is sample code to demonstrated this.
// meshObjectId :
// ObjectId of the SubDMesh entity whose faces need merging
  Acad::ErrorStatus es;
AcDbSubDMesh *pMesh = NULL;
es = acdbOpenObject(pMesh, meshObjectId, kForWrite);
if(es != Acad::eOk)
    return;
  AcDbFullSubentPathArray subentPaths;
es = pMesh->getSubentPath(-1, kFaceSubentType, subentPaths);
  Adesk::Int32 numOfFaces = 0;
pMesh->numOfFaces(numOfFaces);
for(int face=0; face < numOfFaces; face++)
{
    int faceIndex = 0;
    AcGePlane facePlane1;
    es = pMesh->getFacePlane(
                    subentPaths.at(faceIndex).subentId(),
                    facePlane1);
    AcGePlane facePlane2;
    es = pMesh->getFacePlane(
                    subentPaths.at(faceIndex+1).subentId(),
                    facePlane2);
    if(facePlane1.isCoplanarTo(facePlane2) == Adesk::kTrue)
    {
        AcDbFullSubentPathArray subentPathsToMerge;
        subentPathsToMerge.append(
                    subentPaths.at(faceIndex));
        subentPathsToMerge.append(
                    subentPaths.at(faceIndex+1));
        es = pMesh->mergeFaces(subentPathsToMerge);
        if(es == Acad::eOk)
            acutPrintf(ACRX_T("\n2 faces merged."));
        else
            acutPrintf(ACRX_T("\nError merging the faces."));
    }
    else
    {
        acutPrintf(ACRX_T("\nFaces are non-coplanar."));
    }
}
pMesh->close();

