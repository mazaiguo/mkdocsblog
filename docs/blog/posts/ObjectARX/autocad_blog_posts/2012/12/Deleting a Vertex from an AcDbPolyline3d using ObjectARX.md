---
title: "Deleting a Vertex from an AcDbPolyline3d using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Polyline
description: "Removing a vertex from an AcDbPolyline3d is a little more tricky than you would think. An AcDbPolyline3d is what’s known as a ‘Complex’ entity type..."
author: Autodesk
---
# Deleting a Vertex from an AcDbPolyline3d using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/deleting-a-vertex-from-an-acdbpolyline3d-using-objectarx.html

## 文章内容

by Fenton Webb
Removing a vertex from an AcDbPolyline3d is a little more tricky than you would think. An AcDbPolyline3d is what’s known as a ‘Complex’ entity type, it’s vertex data are contained inside of external AcDbVertex3d entities. So to delete a vertex, you have to find the vertex entity and then delete it using the erase() method.
Here’s what I mean…
#include <dbobjptr.h>
void deleteVertex()
{   
  ads_name polyName;    
  ads_point pt;   
  if(acedEntSel(_T("\nSelect a 3d polyline: "), polyName, pt) != RTNORM)        
    return;    
    AcDbObjectId    polyId;    
  acdbGetObjectId(polyId, polyName);    
  // get the polyline in an autoptr
  AcDbObjectPointer<AcDb3dPolyline> pPoly(polyId, AcDb::kForRead);
  Acad::ErrorStatus es = pPoly.openStatus();
  // if it didn't open
  if(es != Acad::eOk)
  {
    if (es == Acad::eNotThatKindOfClass)
      acutPrintf(_T("\nYou did not select a 3d polyline."));        
    else
      acutPrintf(_T("\nError opening entity."));       
    return;   
  }   
    // add each vertex to objectId array   
  AcDbObjectIdArray vertexArray;   
  AcDbObjectIterator *pIter = pPoly->vertexIterator();   
  for(pIter->start(); !pIter->done(); pIter->step())        
    vertexArray.append(pIter->objectId());   
  delete pIter;    
  // get vertex to delete   
  ACHAR prompt[256];   
  acutPrintf(prompt,_T( "\nSelect vertex to delete (1-%d): "),
                                    vertexArray.length());   
  int delVertex = -1;   
  if(acedGetInt(prompt, &delVertex) != RTNORM)      
    return;   
  if(delVertex < 1 || delVertex > vertexArray.length())
  {       
    acutPrintf(_T("\nInvalid vertex number."));       
    return;   
  }  
    // open the vertex entity and delete it   
  AcDbObjectPointer<AcDbObject> pObj(vertexArray[delVertex-1],
                                            AcDb::kForWrite);
  if(pObj.openStatus() != Acad::eOk)
  {      
    acutPrintf(_T("\nError opening vertex: %d"), delVertex);       
    return;   
  }  
  pObj->erase();   
}
  NOTE: If you are using .NET, you have to follow the same logic.

