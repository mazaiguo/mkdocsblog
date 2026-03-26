---
title: "Insert Cone Along The Axis of 3D Polyline"
date: 2016-05-01
categories:
  - AutoCAD
tags:
  - Polyline
  - Solid
  - UCS
description: "This problem illustrates how we can insert a solid frustum along the axis of each segment of AcDb3dPolyline, the cone always points in right direct..."
author: Autodesk
---
# Insert Cone Along The Axis of 3D Polyline

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/insert-cone-along-the-axis-of-3d-polyline.html

## 文章内容

By Madhukar Moogala
This problem illustrates how we can insert a solid frustum along the axis of each segment of AcDb3dPolyline, the cone always points in right direction irrespective of view changes.
This may be useful in depicting flow direction in line diagrams of thermo-fluid dynamic analysis.
The code creates a temporary UCS on each segment of 3dpoly to ensure cone aligns always in correct direction.
Command Code:
  void testFlow()
  {
    bool OK = true;
    ads_name entres;
  ads_point ptres;
      while(OK)
      {
      if(acedEntSel(_T("Select 3d poly"),entres,ptres) != RTNORM)
        {
        OK = false;
         return;
        }
         /*Get List of vertex points*/
        AcGePoint3dArray listVertices;
        getListOfVerticesFromP3dLine(entres,listVertices);
        /*To avoid buffer overflow*/
        for(int i =0, j=1; i < listVertices.length()-1; i++)
          {
          insert_arrow_Adsk(listVertices.at(i), listVertices.at(j));
          j++;
            }
        listVertices.removeAll();
      }
  }
  Utility Methods:
  void createUCS(AcGePoint3d origin_point,AcGeVector3d UCSXaxis,AcGeVector3d UCSYaxis)
    {
    Acad::ErrorStatus es;
    AcDbUCSTableRecord *myUCS =NULL;
      AcDbObjectId UCSId;
    AcDbUCSTable *pUCSTable;
    if (acdbHostApplicationServices()->workingDatabase()->getUCSTable(pUCSTable,AcDb::kForWrite)==Acad::eOk)
      {
        if( pUCSTable->getAt(L"myUCS", myUCS, AcDb::kForWrite) != Acad::eOk)
        {
        myUCS = new AcDbUCSTableRecord;
        /*Define UCS*/
        myUCS->setOrigin(origin_point);
        myUCS->setXAxis(UCSXaxis);
        myUCS->setYAxis(UCSYaxis);
          es=myUCS->setName(_T("MyUCS"));
        if (es != Acad::eOk)
          {
          acutPrintf(_T("\nFailed to set name"));
          return;
          }
        es=pUCSTable->add(UCSId,myUCS);
        }
        /*Modify UCS*/
        myUCS->setOrigin(origin_point);
      myUCS->setXAxis(UCSXaxis);
      myUCS->setYAxis(UCSYaxis);
      /*Close*/ 
      es= myUCS->close();
      es=pUCSTable->close();
        }
    else
      {
      acutPrintf(_T("\nFailed to get UCS table"));
      return;
      }
        //To set the current UCS, I accessed the active AcDbViewportTableRecord
    // and used setUCS to set the UCS I created as current.
        AcDbViewportTable *pVT; 
    es = acedVports2VportTableRecords();
    if (es != Acad::eOk)
      {
      acutPrintf(_T("\nFailed to load vport info into vport table records"));
      return;
      }
      es=acdbHostApplicationServices()->workingDatabase()->getViewportTable(pVT,AcDb::kForRead);
    if (es != Acad::eOk)
      {
      acutPrintf(_T("\nFailed to get vport table"));
      pVT->close();
      return;
      }
      AcDbViewportTableIterator* pIter = NULL;
      es=pVT->newIterator(pIter);
    if (es != Acad::eOk)
      {
      acutPrintf(_T("\nFailed to get vport table"));
      pVT->close();
      delete pIter;
      return;
      }
      for (pIter->start();!pIter->done();pIter->step())
      {
        AcDbViewportTableRecord* pRec;
      es=pIter->getRecord(pRec,AcDb::kForWrite); //it should be open for write mode
      if (es != Acad::eOk)
        {
        acutPrintf(_T("\nFailed to get vport table record"));
        pVT->close();
        pRec->close();
        delete pIter;
        return;
        } 
        ACHAR* name=NULL;
      es=pRec->getName(name);
      if (es != Acad::eOk)
        {
        acutPrintf(_T("\nFailed to get name from vport table"));
        pVT->close();
        pRec->close();
        delete pIter;
        return;
        } 
          if (wcscmp(name,_T("*Active"))==0)
        {
        es=pRec->setUcs(myUCS->objectId());
        }
        es=pRec->close();         
      }
    es=acedVportTableRecords2Vports(); //force update
      es=pVT->close();
    delete pIter;
    return ; 
    }
    void insert_arrow_Adsk(AcGePoint3d startPt, AcGePoint3d trailPt)
    {
      AcGePoint3d midPt = AcGePoint3d ((startPt.x+ trailPt.x)/2 ,(startPt.y+ trailPt.y)/2 ,(startPt.z+ trailPt.z)/2 );
    AcGeVector3d direction((trailPt.x-startPt.x),(trailPt.y-startPt.y),(trailPt.z-startPt.z));
    AcGePlane* tempPlane = new AcGePlane(midPt,direction);
    AcGeVector3d uaxis,vaxis;
    AcGePoint3d point;
        tempPlane->get(point,uaxis,vaxis);
      /*Create UCS\ set UCS as Current*/
    createUCS(midPt,uaxis,vaxis);
    AcGeMatrix3d mat;
      mat.setCoordSystem(midPt,uaxis,vaxis,direction);
    acedSetCurrentUCS(mat);
      /*get Currennt UCS ,transform Cone to that UCS*/
      acedGetCurrentUCS(mat);
      /*Create cone frustrum*/
    AcDb3dSolid* pSolid = new AcDb3dSolid();
      pSolid->setDatabaseDefaults();
    pSolid->setColorIndex(3);
      /*hardcode*/
    pSolid->createFrustum(30.0,5.0,5.0,0.0);
    pSolid->transformBy(mat);
      AcDbObjectId oId = AcDbObjectId::kNull;
    /*Post entity to DB*/
      postToDb(pSolid);
    mat.setToIdentity();
    acedSetCurrentUCS(mat);
    }
    void getListOfVerticesFromP3dLine( ads_name entres,  AcGePoint3dArray& vArray)
    {
    AcDbObjectId oId = AcDbObjectId::kNull;
    if(acdbGetObjectId(oId,entres) != Acad::eOk) return;
    AcDbSmartObjectPointer<AcDb3dPolyline> pEnt(oId,AcDb::kForWrite);
    if(pEnt != nullptr && eOkVerify(pEnt.openStatus()))
      {
      AcDbObjectIterator* pIter = pEnt->vertexIterator();
      AcGePoint3d trailPt ,midPt, startPt;
      for(pIter->start(); !pIter->done(); pIter->step())
        {
        AcDbSmartObjectPointer<AcDb3dPolylineVertex>pVertex(pIter->objectId(), AcDb::kForRead);
        if(eOkVerify(pVertex.openStatus()))
          {
          vArray.append(pVertex->position());
          }
        }
      }
    }
  Working GIF:

## 评论

**内容**: Blob Opera said...
this hlep me alot
Reply
05/18/2023 at 07:57 PM

---
