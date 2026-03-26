---
title: "RealDWG: Implementation of dumpAcDbSubDMesh"
date: 2018-04-01
categories:
  - AutoCAD
tags:
  - DWG
  - Unicode
description: "In RealDWG dumpDWG sample project [RealDWG 2018\Samples\DumpDWG], dumpAcDbSubDMesh implementation is missing, I received a query from a ADN partner..."
author: Autodesk
---
# RealDWG: Implementation of dumpAcDbSubDMesh

发布日期: 2018-04-01

原始链接: https://adndevblog.typepad.com/autocad/2018/04/realdwg-implementation-of-dumpacdbsubdmesh.html

## 文章内容

By Madhukar Moogala
In RealDWG dumpDWG sample project [RealDWG 2018\Samples\DumpDWG], dumpAcDbSubDMesh implementation is missing, I received a query from a ADN partner, so for the benefit of every one I blogging this.
Context: If input drawing to your RealDWG app contains Mesh elements, and you would like to view this elements in any other 3d viewer for example, OpenGL, this implementation will come handy.
void dumpAcDbSubDMesh(AcDbEntity *pEnt)
{
entInfo(pEnt, sizeof(AcDbSubDMesh));
if (pEnt->isKindOf(AcDbSubDMesh::desc())) 
{
 entInfo(pEnt, sizeof(AcDbSubDMesh));
 AcDbSubDMesh *pMesh = AcDbSubDMesh::cast(pEnt);
 Adesk::Int32  nFaces, 
     nEdges, 
     nVertices,
     nSubFaces,
     nSubVertices,
     nSubdLevel;
 bool bWaterTight;
 Acad::ErrorStatus es = pMesh->numOfFaces(nFaces);
 es = pMesh->numOfVertices(nVertices);
 AcGePoint3d pt;
 // this is just for simplicity instead of 
 //traversing all the vertices. 
 //if the vertices > 50 it increments by that number fold.
 int increment = nVertices / 50;
 if (!increment)increment++;
 for (int i = 0; igetVertexAt(i, pt);
  _print(_T("\t\t Vertex Points[%d] %g,%g,%g\n"), i,
   pt.x, pt.y, pt.z);
 }

 es = pMesh->numOfSubDividedFaces(nSubFaces);
 es = pMesh->numOfSubDividedVertices(nSubVertices);
 es = pMesh->isWatertight(bWaterTight);
 es = pMesh->subdLevel(nSubdLevel);
 es = pMesh->numOfEdges(nEdges);
 
 AcGePoint3dArray nsubVerticesArray;
 es = pMesh->getSubDividedVertices(nsubVerticesArray);

 AcArray nsubfacesArray;
 es = pMesh->getSubDividedFaceArray(nsubfacesArray);
 // The content of the faces list is like so :
 // [number of vertices of next face],
 // ,
 // e.g. [4], <1, 2, 3, 4>, [3], <1, 2, 3>, etc


 for (int numVertices = 0, 
  i = 0; 
  i < nsubfacesArray.length();
  i += numVertices + 1)
 {
 numVertices = nsubfacesArray.at(i);
 // Let's print the edges of the face
 _print(_T("\t SubDMesh Edge Points \n"));
 _print(_T("\t\t Face vertex Points[%d] \n"), numVertices);      
 for (int j = 0; j < numVertices; j++)
 {
  AcGePoint3d startPt = 
  nsubVerticesArray.at(nsubfacesArray.at(i + j + 1));
  AcGePoint3d endPt =
  nsubVerticesArray.at(nsubfacesArray.at(i + ((j + 1) % numVertices) + 1));       
  _print(_T("\t\t Vertex Points[%d] [{%g,%g,%g} ,{ %g,%g,%g }]\n"), j,
   startPt.x, startPt.y, startPt.z , endPt.x, endPt.y, endPt.z);
  //Now you can draw lines using these points in OpenGl

 }
 }
}
}
Sample Output
SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{10.1735,8.28866,16.5088} ,{ 16.5135,8.28866,16.5088 }]
                 Vertex Points[1] [{16.5135,8.28866,16.5088} ,{ 16.5135,11.4619,16.5088 }]
                 Vertex Points[2] [{16.5135,11.4619,16.5088} ,{ 10.1735,11.4619,16.5088 }]
                 Vertex Points[3] [{10.1735,11.4619,16.5088} ,{ 10.1735,8.28866,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{10.1735,5.11544,16.5088} ,{ 16.5135,5.11544,16.5088 }]
                 Vertex Points[1] [{16.5135,5.11544,16.5088} ,{ 16.5135,8.28866,16.5088 }]
                 Vertex Points[2] [{16.5135,8.28866,16.5088} ,{ 10.1735,8.28866,16.5088 }]
                 Vertex Points[3] [{10.1735,8.28866,16.5088} ,{ 10.1735,5.11544,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{10.1735,1.94223,16.5088} ,{ 16.5135,1.94223,16.5088 }]
                 Vertex Points[1] [{16.5135,1.94223,16.5088} ,{ 16.5135,5.11544,16.5088 }]
                 Vertex Points[2] [{16.5135,5.11544,16.5088} ,{ 10.1735,5.11544,16.5088 }]
                 Vertex Points[3] [{10.1735,5.11544,16.5088} ,{ 10.1735,1.94223,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{16.5135,8.28866,16.5088} ,{ 22.8534,8.28866,16.5088 }]
                 Vertex Points[1] [{22.8534,8.28866,16.5088} ,{ 22.8534,11.4619,16.5088 }]
                 Vertex Points[2] [{22.8534,11.4619,16.5088} ,{ 16.5135,11.4619,16.5088 }]
                 Vertex Points[3] [{16.5135,11.4619,16.5088} ,{ 16.5135,8.28866,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{16.5135,5.11544,16.5088} ,{ 22.8534,5.11544,16.5088 }]
                 Vertex Points[1] [{22.8534,5.11544,16.5088} ,{ 22.8534,8.28866,16.5088 }]
                 Vertex Points[2] [{22.8534,8.28866,16.5088} ,{ 16.5135,8.28866,16.5088 }]
                 Vertex Points[3] [{16.5135,8.28866,16.5088} ,{ 16.5135,5.11544,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{16.5135,1.94223,16.5088} ,{ 22.8534,1.94223,16.5088 }]
                 Vertex Points[1] [{22.8534,1.94223,16.5088} ,{ 22.8534,5.11544,16.5088 }]
                 Vertex Points[2] [{22.8534,5.11544,16.5088} ,{ 16.5135,5.11544,16.5088 }]
                 Vertex Points[3] [{16.5135,5.11544,16.5088} ,{ 16.5135,1.94223,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{22.8534,8.28866,16.5088} ,{ 29.1934,8.28866,16.5088 }]
                 Vertex Points[1] [{29.1934,8.28866,16.5088} ,{ 29.1934,11.4619,16.5088 }]
                 Vertex Points[2] [{29.1934,11.4619,16.5088} ,{ 22.8534,11.4619,16.5088 }]
                 Vertex Points[3] [{22.8534,11.4619,16.5088} ,{ 22.8534,8.28866,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{22.8534,5.11544,16.5088} ,{ 29.1934,5.11544,16.5088 }]
                 Vertex Points[1] [{29.1934,5.11544,16.5088} ,{ 29.1934,8.28866,16.5088 }]
                 Vertex Points[2] [{29.1934,8.28866,16.5088} ,{ 22.8534,8.28866,16.5088 }]
                 Vertex Points[3] [{22.8534,8.28866,16.5088} ,{ 22.8534,5.11544,16.5088 }]
         SubDMesh Edge Points
                 Face vertex Points[4]
                 Vertex Points[0] [{22.8534,1.94223,16.5088} ,{ 29.1934,1.94223,16.5088 }]
                 Vertex Points[1] [{29.1934,1.94223,16.5088} ,{ 29.1934,5.11544,16.5088 }]
                 Vertex Points[2] [{29.1934,5.11544,16.5088} ,{ 22.8534,5.11544,16.5088 }]
                 Vertex Points[3] [{22.8534,5.11544,16.5088} ,{ 22.8534,1.94223,16.5088 }]

