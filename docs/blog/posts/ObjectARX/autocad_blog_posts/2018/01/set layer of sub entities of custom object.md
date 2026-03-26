---
title: "set layer of sub entities of custom object"
date: 2018-01-01
categories:
  - AutoCAD
tags:
  - Layer
description: "Some customers wanted to set sub entities of custom object to the specific layers. When the corresponding layers changed ( such as visibility, colo..."
author: Autodesk
---
# set layer of sub entities of custom object

发布日期: 2018-01-01

原始链接: https://adndevblog.typepad.com/autocad/2018/01/set-layer-of-sub-entities-of-custom-object.html

## 文章内容

By Xiaodong Liang
Some customers wanted to set sub entities of custom object to the specific layers. When the corresponding layers changed ( such as visibility, color etc), the entities will update accordingly. 
The solution is very straightforward. worldDraw->subEntityTraits().setLayer allows us to specify the specific primitives of the custom object to the specific layer. This method sets the AcGiSubEntityTraits object to use layerId to specify the layer on which to draw graphics primitives until the next call to this function, or the end of the worldDraw() or viewportDraw() execution.
I did an experiment based on SDK sample PolySample. In asdkpolyobj project >> poly.cpp  >> drawEdges method, add some lines as below.  
  
static Acad::ErrorStatus drawEdges(const AsdkPoly*         poly,
                                         AcGiWorldDraw*    worldDraw,
                                         AcGiViewportDraw* vportDraw)
{
    Acad::ErrorStatus es = Acad::eOk;

    // Draw each edge of the polygon as a line. We could have drawn
    // the whole polygon as a polyline, but we want to attach subEntity
    // traits (e.g. which line it is) to each line which will be used
    // for snap.
    //
    // Since we are drawing the polygon line by line, we also have the
    // control over setting the linetype and color of each line (via
    // subEntity traits), but we won't get that fancy.

 //get the specific layers ID
 AcDbObjectId testLayerId = AcDbObjectId::kNull; 
 AcDbObjectId zeroLayerId = AcDbObjectId::kNull;

 AcDbLayerTable* lTable = NULL;  
 AcDbDatabase *pDb = acdbHostApplicationServices()->workingDatabase(); 
 Acad::ErrorStatus layer_table_es = pDb->getSymbolTable(lTable, AcDb::kForRead); 

 if (Acad::eOk == layer_table_es && lTable)
 {   
  if (lTable->getAt(_T("MyTestLayer"), testLayerId) != Acad::eOk) 
   ::acutPrintf(_T("ERROR Getting MyTestLayer\n"));  
  if (lTable->getAt(_T("0"), zeroLayerId) != Acad::eOk)
   ::acutPrintf(_T("ERROR Getting 0 Layer\n"));

  lTable->close(); 
 }

    AcGePoint3dArray vertexArray;
    if ((es = poly->getVertices3d(vertexArray)) != Acad::eOk) {
        return es;
    }

    AcGePoint3d ptArray[2];

    for (int i = 0; i < vertexArray.length() - 1; i++) {

        if (worldDraw != NULL) {

    if(i%3==0 ){
     //if a specific edge. set it to the layer MyTestLayer
     if(!testLayerId.isNull())
     worldDraw->subEntityTraits().setLayer(testLayerId); 
    
    }
    else {
     //other edges. set them to the layer 0
     if (!zeroLayerId.isNull())
      worldDraw->subEntityTraits().setLayer(zeroLayerId);
    }
             worldDraw->subEntityTraits().setSelectionMarker(i + 1);
        } else {
            assert(Adesk::kFalse);
            //vportDraw->subEntityTraits().setSelectionMarker(i + 1);
        }

        ptArray[0] = vertexArray[i];
        ptArray[1] = vertexArray[i + 1];

        if (worldDraw != NULL) {
            worldDraw->geometry().polyline(2, ptArray);
        } else {
            assert(Adesk::kFalse);
            //vportDraw->geometry().polyline3d(2, ptArray);
        }
    }

    return es;
}
The snapshots are two tests. One toggle MyTestLayer off. The other change the layer's color.

## 评论

**内容**: James Gray said...
Great post it was. I am really impressed with the work done by the author. Keep posting and also visit: Home daycare Columbia
Reply
04/18/2018 at 04:21 AM

---
