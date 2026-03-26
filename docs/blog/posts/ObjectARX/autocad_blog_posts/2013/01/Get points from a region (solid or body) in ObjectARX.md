---
title: "Get points from a region (solid or body) in ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Solid
description: "Using BRrep (Bound Representation) this sample does this for AcDbRegion. It can be modified to work on AcDb3dSolid or AcDbBody."
author: Autodesk
---
# Get points from a region (solid or body) in ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/get-points-from-a-region-solid-or-body-in-objectarx.html

## 文章内容

By Augusto Goncalves
Using BRrep (Bound Representation) this sample does this for AcDbRegion. It can be modified to work on AcDb3dSolid or AcDbBody.
// Make sure you uncomment the following
//      #define _BREP_SUPPORT_
// On your StdAfx.h header file
// This will enable BREP on the code
static void getPoints(
            AcDbObjectId id,
            AcGePoint3dArray &points )
{   
  AcBrBrep*pBrep = new AcBrBrep;
  pBrep->setSubentPath( AcDbFullSubentPath( id, kNullSubentId ));  
  AcBrBrepFaceTraverser brFaTrav; 
  for (brFaTrav.setBrep(*pBrep);!brFaTrav.done();brFaTrav.next()) 
  {       
    AcBrFaceLoopTraverser faLoTrav;      
    AcBrFace face;    
    brFaTrav.getFace(face);    
    for(faLoTrav.setFace(face);!faLoTrav.done();faLoTrav.next())
    {         
      AcBrLoopEdgeTraverser loEdTrav; 
      if(loEdTrav.setLoop(faLoTrav) == AcBr::eOk)
      {           
        for( ; !loEdTrav.done(); loEdTrav.next())
        {            
          AcBrEdge edge;   
          loEdTrav.getEdge(edge);
          AcBrVertex start;     
          edge.getVertex1( start );  
          AcGePoint3d pt;           
          start.getPoint( pt );    
          points.append( pt );       
        }          
      } // else its an isolated loop    
    }   
  }
  delete pBrep;
}
  static void AdskPointsFromRegion_GetPoints(void)
{
  ads_name eName;  
  ads_point pt;  
  if( RTNORM != acedEntSel(
    _T("\nPlease select a region "),
    eName, pt ) )
    return;
  AcDbObjectId id;
  acdbGetObjectId( id, eName ); 
  AcDbRegion*pRegion;   
  acdbOpenObject(pRegion, id, AcDb::kForRead );
  if( pRegion == NULL )   
    return; 
  AcGePoint3dArray points; 
  pRegion->close(); 
  getPoints( id, points );
  int nPoints = points.length();
  for( int i=0; i<nPoints; i++ )
  {
    acedGrDraw(
      asDblArray(points[i]),
      asDblArray(points[(i+1)%nPoints]), 1,0 );
  }
}

