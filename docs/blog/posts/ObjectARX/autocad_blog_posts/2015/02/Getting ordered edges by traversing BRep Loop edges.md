---
title: "Getting ordered edges by traversing BRep Loop edges"
date: 2015-02-01
categories:
  - AutoCAD
tags:
  - API
  - Solid
description: "When traversing the edges of a face loop using BRep API, the edges may not be in order such that the end point of the previous edge coincides with ..."
author: Autodesk
---
# Getting ordered edges by traversing BRep Loop edges

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/getting-ordered-edges-by-traversing-brep-loop-edges.html

## 文章内容

By Balaji Ramamoorthy
When traversing the edges of a face loop using BRep API, the edges may not be in order such that the end point of the previous edge coincides with the start point of the next edge. This is because, the edges are shared between faces, and the same edge is returned when the face's edge loop is traversed. As the start and end points of the edge remains unchanged, it will only match the orientation for one of the faces.
Here is a sample code to retrieve the edge information and orient them as per the loop being iterated.
 ads_name eName; 
 ads_point pt; 
   if ( RTNORM != 
  acedEntSel( L"\\nSelect a Solid: " , 
     eName, pt)) 
 return ; 
   AcDbObjectId id; 
 acdbGetObjectId( id, eName); 
   AcDb3dSolid* pSolid; 
 acdbOpenObject(pSolid, id, AcDb::kForRead); 
   if (pSolid == NULL ) return ; 
   AcBrBrep pBrep; 
 pBrep.setSubentPath( 
  AcDbFullSubentPath( id, kNullSubentId )); 
   AcBr::ErrorStatus returnValue = AcBr::eOk; 
   AcBrBrepFaceTraverser brepFaceTrav; 
 if  (brepFaceTrav.setBrep(pBrep) != AcBr::eOk) 
 { 
  acutPrintf(ACRX_T(
   "\\n Error in AcBrBrepFaceTraverser::setBrep:" ));
  return ; 
 } 
   int  faceCount = 0; 
 while  (!brepFaceTrav.done() && (returnValue == AcBr::eOk))
 { 
  faceCount++; 
    AcBrFace face; 
  if  ( brepFaceTrav.getFace(face) 
   != AcBr::ErrorStatus::eOk) 
  {
   continue ;
  }
    AcGeSurface *pGeSurface = NULL;
  face.getSurface(pGeSurface);
    AcGeInterval intervalU, intervalV;
  pGeSurface->getEnvelope(intervalU, intervalV);
          AcBrFaceLoopTraverser faLoTrav; 
  for ( faLoTrav.setFace(face); 
   !faLoTrav.done(); faLoTrav.next() ) 
  { 
   AcBrLoop lp; 
   faLoTrav.getLoop(lp); 
   AcBr::LoopType type; 
     acutPrintf(ACRX_T("\\nFACE : %d" ), faceCount);
     AcBrLoopEdgeTraverser loEdTrav; 
   if ( loEdTrav.setLoop(faLoTrav) == AcBr::eOk) 
   { 
    int  edgeCount = 0;
    AcGePoint2dArray verts; 
    AcGeVoidPointerArray edgeArray; 
    for (;! loEdTrav.done(); loEdTrav.next()) 
    { 
     edgeCount++;
       AcBrEdge edge; 
     loEdTrav.getEdge(edge); 
       AcBrVertex start;      
     edge.getVertex1( start );   
     AcGePoint3d stPt3d;            
     start.getPoint( stPt3d );  
       AcBrVertex end; 
     edge.getVertex2( end );   
     AcGePoint3d endPt3d;            
     end.getPoint( endPt3d ); 
       Adesk::Boolean orient 
      = Adesk::kFalse;
     loEdTrav.getEdgeOrientToLoop(orient);
     if (orient)
     {
     acutPrintf(ACRX_T("\\nEdge %d:  
      (%3.1f %3.1f %3.1f) 
      - (%3.1f %3.1f %3.1f)"),  
      edgeCount, stPt3d.x, 
      stPt3d.y, stPt3d.z, 
      endPt3d.x, endPt3d.y, 
      endPt3d.z);
     }
     else 
     {
     acutPrintf(ACRX_T("\\nEdge %d:  
      (%3.1f %3.1f %3.1f) 
      - (%3.1f %3.1f %3.1f)"), 
      edgeCount, endPt3d.x, 
      endPt3d.y, endPt3d.z, 
      stPt3d.x, stPt3d.y, 
      stPt3d.z);
     }
    } 
   } 
  } 
  returnValue = brepFaceTrav.next(); 
 } 
  As an example, here is an output of a face loop :
 // Considering edge orientation to loop 
 FACE : 3
 Edge 1: (0.0 0.0 30.0) - (0.0 0.0 0.0)
 Edge 2: (0.0 0.0 0.0) - (10.0 0.0 0.0)
 Edge 3: (10.0 0.0 0.0) - (10.0 0.0 30.0)
 Edge 4: (10.0 0.0 30.0) - (0.0 0.0 30.0)
   // Without considering edge orientation to loop 
 FACE : 3
 Edge 1: (0.0 0.0 30.0) - (0.0 0.0 0.0)
 Edge 2: (10.0 0.0 0.0) - (0.0 0.0 0.0)
 Edge 3: (10.0 0.0 30.0) - (10.0 0.0 0.0)
 Edge 4: (0.0 0.0 30.0) - (10.0 0.0 30.0)

## 评论

**内容**: Maxence said...
How do you do that in .NET? There is no BRepFaceLoopTraverser.
Reply
12/01/2022 at 12:33 AM

---
