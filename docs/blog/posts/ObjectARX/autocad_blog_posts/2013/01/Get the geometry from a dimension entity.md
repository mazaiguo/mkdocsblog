---
title: "Get the geometry from a dimension entity"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Dimension
description: "How find information about the three AcDbLine Objects used in a AcDbDimension Object? It’s known that the 'subentities' of the dimension is stored ..."
author: Autodesk
---
# Get the geometry from a dimension entity

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/get-the-geometry-from-a-dimension-entity.html

## 文章内容

By Augusto Goncalves
How find information about the three AcDbLine Objects used in a AcDbDimension Object? It’s known that the 'subentities' of the dimension is stored in a block definition (AcDbBlockTableRecord), and that I have to get this block definition. After getting the block definition, if we try use the function getStartPoint and getEndPoint of the AcDbLine class, but the z component of the returned coordinates is always '0'. Is it possible to get the 'real' coordinates of the dimension lines?
It is normal that getStartPoint() and endStartPoint() returns a Z-value of 0.0 in this case because this is how dimension entities work. The graphics of a dimension is stored in a block table record as an anonymous block. In this block definition there is no z-value used because the entities stored in the block definition are relative to the 'insertion point' of the dimension entity. As a result, every line stored in this block definition returns 0.0 for the z component of the start/endpoints. When AutoCAD has to draw a dimension, it gets the insertion point (location) of the dimension object. Then it takes the block definition and transforms it to the dimension location.
When you need to get the 'real' coordinate of the lines from the dimension block definition, you have to do this transformation manually. The following code shows how to get the transformation matrix. The code iterates all entities stored in the block definition. If the entity iterated to is a line, it transforms to coordinates to the 'real' coordinates and places a new line entity at the same position in the model space.
// Iterate every entity stored in the
// block definition of the dimension.
for (; !pIter->done(); pIter->step())
{
  AcDbEntity *pEnt;   pIter->getEntity(pEnt, AcDb::kForRead); 
  if (pEnt->isKindOf(AcDbLine::desc())) 
  {
    AcDbLine *pLine = (AcDbLine*) pEnt; 
    // Get the start and end point. 
    AcGePoint3d ptStart,    
      ptEnd;     pLine->getStartPoint(ptStart);
    pLine->getEndPoint(ptEnd); 
    //     // Transform the start and end point.  
    //     // Get the transformation matrix.  
    AcGeMatrix3d mat;  
    // Get the axis of the dimension entity.
    AcGeVector3d zAxis(pDim->normal());  
    AcGeVector3d xAxis(zAxis.perpVector()); 
    AcGeVector3d yAxis(zAxis.crossProduct(xAxis));
    // Build the transformation matrix.   
    mat.setToAlignCoordSys(AcGePoint3d::kOrigin,
      AcGeVector3d(1.0, 0.0, 0.0),
      AcGeVector3d(0.0, 1.0, 0.0),
      AcGeVector3d(0.0, 0.0, 1.0),
      AcGePoint3d::kOrigin,
      xAxis, yAxis, zAxis);  
      // z axis  
    // To test this matrix create a new line  
    // using the start and endpoint of the line
    // from the block definition, and transform  
    // the line using the calculated transformation matrix.    
    AcDbLine *pNewLine = new AcDbLine(ptStart, ptEnd);   
    pNewLine->transformBy(mat);    
    AcGePoint3d nptStart, nptEnd;   
    pNewLine->getStartPoint(nptStart);    
    pNewLine->getEndPoint(nptEnd);    
    pNewLine->setColorIndex(4);    
    // Append the new line to the model space and close it.   
    // The new line should be at the location    
    // of the dimension entity.    
    AppendToModelSpaceAndClose(pNewLine);
  }  
  pEnt->close();
}

