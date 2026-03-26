---
title: "Dynamic Loading and Unloading Of Raster Images Depending On Zoom Scale"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Plugin
description: "Lets say you want to control the loading and unloading of the Raster images when the user is zooming or panning. The Images should load or unload o..."
author: Autodesk
---
# Dynamic Loading and Unloading Of Raster Images Depending On Zoom Scale

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/dynamic-loading-and-unloading-of-raster-images-depending-on-zoom-scale.html

## 文章内容

By Gopinath Taget
Lets say you want to control the loading and unloading of the Raster images when the user is zooming or panning. The Images should load or unload on two factors:
1) The zoom scale.
2) The Image is in visible area or not.
This can be achieved by adding an editor reactor that checks for the command “ZOOM” and “PAN”. If the user has invoked either of the command then do the following:
1) Scan for all the Raster Images in the drawing.
2) Check if a Raster Image is fully, partially or non visible in the current view.
3) If the Raster Image is fully or partially visible, check for ratio (Image diagonal /View diagonal). If this ratio lies with in the specified limit, then load the Image otherwise unload it. Also unload the image if it does not lie in the current view.
To check for visibility of the Raster Image in the current view:
1) Build a transformation matrix for the DCS coordinate system.
2) Get the view centre using VIEWCTR sysvar. This lies in the current UCS. Project the point onto the DCS XY plane.
3) Get the view height using VIEWSIZE and calculate the view width using the window aspect ratio "SCREENSIZE".
4) Calculate the extents in DCS XY plane using view centre and height/width.
5) To check if an entity lies fully in the current view, get the bounding box of the entity and project the maximum and minimum points of the extents onto DCS XY plane. Check if the projected points lie fully in the bounding box defined by DCS extents. If they do the entity is fully visible in the current view else check if the DCS extents lies fully in the entities extents bounding box. If yes then it means that the image fully covers the current view. If not, go to next step.
6) Create a polyline that forms rectangle with DCS extents as the corners. Test for the intersection of the polyline and the projected entity in DCS XY plane. If they intersect, the entity is partially visible. If not then the entity is not visible at all.
There are two major functions in the code provided below. First one is fCheckEntitiesInDispArea(). This function takes an object ID array as in parameter. It checks for visibility of the entities specified in the array and populates three object ID arrays and they contain entities that are fully visible, partially visible and not visible at all, respectively. The second function is fTest(), which actually iterates the AcDbRasterImage entities in the model space and then tests for the visibility, checks for the diagonal size of the image and loads or unloads depending on the size.
The snippets provided below has the complete code to do all the above. In the code, I defines a command "test" and also implements an editor reactor that reacts to "ZOOM" and “PAN" command. The program essentially unloads any the raster image which is smaller than 1/5 size and bigger than 10 times the size of the current view and also if they are not lying in the current view. The command “setratio” allows the user to change the minimum and maximum Image/View diagonal ratio.
Finally, this blog post will be useful in case you need to react to Real-time Zoom also:
  ///////////////////////////////////////////////////////////////////////////
//global variable to hold the max and minimum valid size for the raster
double gnMaxSize = 10.0;   //Raster should not ten times the screen size
double gnMinSize = 0.20; //Raster should not less than 1/5th of screen size
///////////////////////////////////////////////////////////////////////////
  //globals
//editor reactor
AsdkEdReactor *pEdReact = NULL;
  //========================================================
//========================================================
void fTest()
{
Acad::ErrorStatus mEs;
AcDbBlockTable *pBT;
AcDbBlockTableRecord *pBTR;
AcDbBlockTableRecordIterator *pBTIter;
  acdbHostApplicationServices()->workingDatabase()->
  getBlockTable(pBT,AcDb::kForRead);
pBT->getAt(ACDB_MODEL_SPACE,pBTR,AcDb::kForRead);
pBTR->newIterator(pBTIter);
pBT->close();
pBTR->close();
   //array to hold the entities
AcDbObjectIdArray aNoDispEntArray;
AcDbObjectIdArray mFullDispEntArray;
AcDbObjectIdArray mPartialDispArray;
AcDbEntity *pEnt;
  AcDbRasterImage *pRastImg;
   //populate the aNoDispEntArray with all
 //entites that are RasterImage
 while (!(pBTIter->done()))
{
  pBTIter->getEntity(pEnt,AcDb::kForRead);
  pRastImg = AcDbRasterImage::cast(pEnt);
    if(NULL != pRastImg)
  {
   aNoDispEntArray.append(pRastImg->objectId());
    }
  pEnt->close();
  pBTIter->step();
}
   //check for display of entities in the current view
fCheckEntitiesInDispArea(aNoDispEntArray,
  mFullDispEntArray,mPartialDispArray);
  acutPrintf(
  _T("\nNo of Images not lying in the current View : %d"),
  aNoDispEntArray.length());
acutPrintf(
  _T("\nNo of Images lying fully in the current View : %d"),
  mFullDispEntArray.length());
acutPrintf(
  _T("\nNo of Images lying partially in the current View : %d"),
  mPartialDispArray.length());
   //unload the images depending on their visibility
 long mCtr; //number of entities
AcDbRasterImageDef *pImgDef;
 for(mCtr = 0;mCtr < aNoDispEntArray.length();mCtr++)
{
  mEs = acdbOpenObject(pRastImg,
   aNoDispEntArray.at(mCtr),AcDb::kForRead);
  if(Acad::eOk == acdbOpenObject(pImgDef,
   pRastImg->imageDefId(),AcDb::kForRead))
  {
   if(Adesk::kTrue == pImgDef->isLoaded())
   {
    pImgDef->upgradeOpen();
    pImgDef->unload();
   }
   pImgDef->close();
  }
  pRastImg->close();
}
   //load or unload depending upon the VIEWSIZE
 //for fully visible or partially visible entities
 //get the view center
 struct resbuf rs;
 double nHeight;
 double nWidth;
 double nScreenDiag;
   //get the view height
acedGetVar(_T("VIEWSIZE"),&rs);
nHeight = rs.resval.rreal;
 //get the screen size
acedGetVar(_T("SCREENSIZE"),&rs);
nWidth = nHeight*(rs.resval.rpoint[0] / rs.resval.rpoint[1]);
 //get the dialgonal length
nScreenDiag = sqrt(pow(nHeight,2) + pow(nWidth,2));
   //append the full display entities
 //with the partial displayed entities
 //as we want similar behaviuor for both
 for(mCtr = 0;mCtr < mPartialDispArray.length();mCtr++)
{
  mFullDispEntArray.append(mPartialDispArray.at(mCtr));
}
   //hold Object ID from the array
AcDbObjectId aObjID;
 double nDiagRatio;
   for(mCtr = 0;mCtr < mFullDispEntArray.length();mCtr++)
{
  AcDbExtents mImgExts;
    //try opening the object for read
  if(Acad::eOk != acdbOpenObject(pRastImg,
   mFullDispEntArray.at(mCtr),AcDb::kForRead))
   continue;
  aObjID = pRastImg->imageDefId();
  pRastImg->getGeomExtents(mImgExts);
  pRastImg->close();
    //open the image definition
  if(Acad::eOk != acdbOpenObject(pImgDef,aObjID,
   AcDb::kForRead))
   continue;
    //the ratio is equal to raster size/screen size
  nDiagRatio = (mImgExts.maxPoint().
   distanceTo(mImgExts.minPoint())/nScreenDiag);
    //print the values on screen
  //char buf[255];//wb
  ACHAR buf[255];
  aObjID.handle().getIntoAsciiBuffer(buf);
  acutPrintf(_T("\nImage handle: %s , Diagonal Ratio: %f"),
   buf,nDiagRatio);
  //
    //if the Image diagonal is less than
  //gnMinSize or greater gnMaxSize, then unload
  if((nDiagRatio >= gnMinSize) &&
   (nDiagRatio <= gnMaxSize))
  {
   if(Adesk::kFalse == pImgDef->isLoaded())
   {
    pImgDef->upgradeOpen();  
    pImgDef->load(); //image is sufficently zoomed
   }
  }
  else
  {
   if(Adesk::kTrue == pImgDef->isLoaded())
   {
    pImgDef->upgradeOpen();
    //image is too small or too large to display
    pImgDef->unload();
   }
  }
    pImgDef->close();
}
   //clean up
 delete pBTIter;
}
  ////////////////////////////////////////////////////////////////
//Description: fCheckEntitiesInDispArea
////////////////////////////////////////////////////////////////
void fCheckEntitiesInDispArea(AcDbObjectIdArray &aNoDispEntArray,
AcDbObjectIdArray &aFullDispEntArray,
AcDbObjectIdArray &aPartDispEntArray)
{
 //get the display properties
CDcsProp mDcsPty;
 //create a pline to check for the interference
AcDbPolyline *paPline = new AcDbPolyline(4);
  fGetDCSBoundary(&mDcsPty,paPline);
   long mCtr; //number of entitie
AcDbObjectId aObjID;
AcDbObjectIdArray mTempEntArray;
   for(mCtr = 0;mCtr < aNoDispEntArray.length();mCtr++)
{
  aObjID = aNoDispEntArray.at(mCtr);
    //check if entity lies completely in the current display area
  if(Adesk::kTrue== fLiesCompleteyInView(aObjID,mDcsPty))
  {
   aFullDispEntArray.append(aObjID);
  }
  else
  {
   //check if it lies partially
   if(Adesk::kTrue== fLiesPartiallyInView(aObjID,
    paPline,mDcsPty))
   {
    aPartDispEntArray.append(aObjID);
   }
   else
   {
    //completely out of display
    mTempEntArray.append(aObjID);
   }
  }
  }
  aNoDispEntArray = mTempEntArray;
 //clean up
 delete paPline;
}
  //////////////////////////////////////////////////////////////
//Description: fGetDCSBoundary
//////////////////////////////////////////////////////////////
void fGetDCSBoundary(CDcsProp *paDcsPty,AcDbPolyline *paPline)
{
AcGeMatrix3d mMatDCS2WCS;
AcGePoint3d mPtMax;
    AcGePoint3d mPtMin;
   //returns DCS2WCS matrix and the extents in DCS coords
fGetViewCornersInDcs(mMatDCS2WCS,mPtMax,mPtMin);
   //get the projection plane
AcGePlane pPlnDCSXY = fGetXYPlane(mMatDCS2WCS);
 //create a box
paPline->addVertexAt(0,AcGePoint2d(mPtMin.x,mPtMin.y));
paPline->addVertexAt(1,AcGePoint2d(mPtMax.x,mPtMin.y));
paPline->addVertexAt(2,AcGePoint2d(mPtMax.x,mPtMax.y));
paPline->addVertexAt(3,AcGePoint2d(mPtMin.x,mPtMax.y));
paPline->setClosed(Adesk::kTrue);
paPline->transformBy(mMatDCS2WCS);
   //add the pline to MS
 //fAddToMS((AcDbEntity *)pPolyline);
   //prepare the DCS poperties
paDcsPty->m_matMatrix = mMatDCS2WCS;
paDcsPty->fCalculate();
paDcsPty->m_maxPt = mPtMax;
paDcsPty->m_minPt = mPtMin;
}
  //////////////////////////////////////////////////////////////
//Description: fLiesPartiallyInView
//////////////////////////////////////////////////////////////
Adesk::Boolean fLiesPartiallyInView(AcDbObjectId aObjID,
AcDbPolyline *paPline,const CDcsProp aDcsPty)
{
 //area, so check if lies partially
AcGePoint3dArray mInterPoints;
AcDbEntity *pEnt;
   //try opening the object for read
 if(Acad::eOk != acdbOpenObject(pEnt,aObjID,
  AcDb::kForRead)) return Adesk::kFalse;
   //check for intersection
paPline->intersectWith(pEnt,AcDb::kOnBothOperands,
  aDcsPty.m_PlnXY ,mInterPoints);
   //close the entity
pEnt->close();
   //how many points are intersecting?
 if (0 != mInterPoints.length())
  return Adesk::kTrue;  //intersects
 else
  return Adesk::kFalse; //does not intersect
}
  /////////////////////////////////////////////////////////
//Description: fLiesCompleteyInView
/////////////////////////////////////////////////////////
Adesk::Boolean fLiesCompleteyInView(AcDbObjectId aObjID,
 const CDcsProp aDcsPty)
{
AcDbEntity *pEnt;
   //try opening the object for read
 if(Acad::eOk != acdbOpenObject(
  pEnt,aObjID,AcDb::kForRead)) return Adesk::kFalse;
   //check if the entity lies in the display area completely
AcDbExtents mEntExts;
pEnt->getGeomExtents(mEntExts);
   //close the entity
pEnt->close();
  AcGePoint3d mPtExtMax;
    AcGePoint3d mPtExtMin;
  mPtExtMax = mEntExts.maxPoint();
mPtExtMin = mEntExts.minPoint();
  mPtExtMax = mPtExtMax.project(aDcsPty.m_PlnXY,
  aDcsPty.m_PlnXY.normal());
mPtExtMin = mPtExtMin.project(aDcsPty.m_PlnXY,
  aDcsPty.m_PlnXY.normal());
   //transform the extents
mPtExtMax.transformBy(aDcsPty.m_matMatrix.inverse());
mPtExtMin.transformBy(aDcsPty.m_matMatrix.inverse());
   //lies in the display area
 if((aDcsPty.m_minPt.x <= mPtExtMin.x) &&
  (mPtExtMin.x <= aDcsPty.m_maxPt.x) &&
  (aDcsPty.m_minPt.y <= mPtExtMin.y) &&
  (mPtExtMin.y <= aDcsPty.m_maxPt.y) &&
  (aDcsPty.m_minPt.x <= mPtExtMax.x) &&
  (mPtExtMax.x <= aDcsPty.m_maxPt.x) &&
  (aDcsPty.m_minPt.y <= mPtExtMax.y) &&
  (mPtExtMax.y <= aDcsPty.m_maxPt.y))
  return Adesk::kTrue;
 else
  //screen lies completely with in the entity
  if ((mPtExtMin.x <= aDcsPty.m_minPt.x) &&
   (aDcsPty.m_minPt.x <= mPtExtMax.x) &&
   (mPtExtMin.y <= aDcsPty.m_minPt.y) &&
   (aDcsPty.m_minPt.y <= mPtExtMax.y) &&
   (mPtExtMin.x <= aDcsPty.m_maxPt.x) &&
   (aDcsPty.m_maxPt.x <= mPtExtMax.x ) &&
   (mPtExtMin.y <= aDcsPty.m_maxPt.y) &&
   (aDcsPty.m_maxPt.y <= mPtExtMax.y))
   return Adesk::kTrue;
  else
   return Adesk::kFalse;
}
  //////////////////////////////////////////////////////
//Description: fGetViewCornersInDcs
//////////////////////////////////////////////////////
void fGetViewCornersInDcs(AcGeMatrix3d &aMatDCS2WCS,
AcGePoint3d &aPtMax,AcGePoint3d &aPtMin)
{
AcGePoint3d mPtCen;
 double nHeight,nWidth;
   //get the required current VIEW properties
   //get the view center
 struct resbuf rs;
acedGetVar(_T("VIEWCTR"),&rs);
mPtCen.x = rs.resval.rpoint[X];
mPtCen.y = rs.resval.rpoint[Y];
mPtCen.z = rs.resval.rpoint[Z];
   //get the view height
acedGetVar(_T("VIEWSIZE"),&rs);
nHeight = rs.resval.rreal;
   //get the screen size
acedGetVar(_T("SCREENSIZE"),&rs);
nWidth = nHeight*(rs.resval.rpoint[0] / rs.resval.rpoint[1]);
   //get the TARGET,VIEWDIR and TWISTANGLE to prepare the DCS matrix
 //you can use acedTrans..but using the pure ARX methods
AcGePoint3d ptTarget;
AcGeVector3d vecDir;
 double nTwistAngle;
   //get the screen size
acedGetVar(_T("TARGET"),&rs);
ptTarget.x = rs.resval.rpoint[X];
ptTarget.y = rs.resval.rpoint[Y];
ptTarget.z = rs.resval.rpoint[Z];
   //get the screen size
acedGetVar(_T("VIEWDIR"),&rs);
vecDir.x = rs.resval.rpoint[X];
vecDir.y = rs.resval.rpoint[Y];
vecDir.z = rs.resval.rpoint[Z];
   //get the screen size
acedGetVar(_T("VIEWTWIST"),&rs);
nTwistAngle = rs.resval.rpoint[0];
   //transform the UCS VIEWCTR and TARGET to WCS
AcGeMatrix3d matUCSToWCS;
acedGetCurrentUCS(matUCSToWCS);
mPtCen.transformBy(matUCSToWCS);
ptTarget.transformBy(matUCSToWCS);
   //prepare Matrix for DCS to WCS transformation
 //note that VIEWDIR sysvar is reported in UCS
  vecDir.transformBy(matUCSToWCS);
vecDir.normalize();
aMatDCS2WCS.setToPlaneToWorld(vecDir);
aMatDCS2WCS = AcGeMatrix3d::translation(
  ptTarget - AcGePoint3d::kOrigin) *
  aMatDCS2WCS; //for DCS target point is the origin
aMatDCS2WCS = AcGeMatrix3d::rotation(
  -nTwistAngle, vecDir.normal(),ptTarget) *
  aMatDCS2WCS;//DCS Xaxis is twisted by twist angle
   //project the point to the DCS XY plane
AcGePlane plDCSXY;
plDCSXY = fGetXYPlane(aMatDCS2WCS);
mPtCen = mPtCen.project(plDCSXY, vecDir);
mPtCen.transformBy(aMatDCS2WCS.inverse());
   //get the top right corner and lower left corner
 //in DCS XY plane
aPtMax.x = mPtCen.x + nWidth/2;
aPtMax.y = mPtCen.y + nHeight/2;
aPtMax.z = mPtCen.z;
  aPtMin.x = mPtCen.x - nWidth/2;
aPtMin.y = mPtCen.y - nHeight/2;
aPtMin.z = mPtCen.z;
}
  ////////////////////////////////////////////////
//Description: fGetXYPlane
////////////////////////////////////////////////
void fSetMaxMin()
{
ads_real mAdsTemp;
acutPrintf(
_T("\nType the maximum and minimum (raster size/screen) size ratios..."));
   //get the Min ratio
acedInitGet(RSG_NOZERO + RSG_NONEG,_T(""));
  acutPrintf(_T("\nminimum raster/screen size <%f>: "),
  gnMinSize);
 if(RTNORM == acedGetReal(_T(""), &mAdsTemp))
  gnMinSize = mAdsTemp;
   //get the Min ratio
acedInitGet(RSG_NOZERO + RSG_NONEG,_T(""));
acutPrintf(_T("\nmaximum raster/screen size <%f>: "),gnMaxSize);
  if(RTNORM == acedGetReal(_T(""), &mAdsTemp))
   gnMaxSize = mAdsTemp;  
}
  //////////////////////////////////////////////////////////////////
//Description: fGetXYPlane
//Parameters:
//a)AcGeMatrix of the coordinate system whose XY plane is returned
//
//////////////////////////////////////////////////////////////////
AcGePlane fGetXYPlane(AcGeMatrix3d aMatInput)
{
AcGePoint3d ptOrg;
AcGeVector3d vecXaxis,vecYaxis,vecZaxis;
aMatInput.getCoordSystem(ptOrg,vecXaxis,vecYaxis,vecZaxis);
 return AcGePlane::AcGePlane(ptOrg,vecXaxis,vecYaxis);
}
  //////////////////////////////////////////////////////////////////
//Description: fAddToMS
//////////////////////////////////////////////////////////////////
AcDbObjectId fAddToMS(AcDbEntity *paEnt)
{
    AcDbBlockTable *pBlockTable;
      acdbHostApplicationServices()->workingDatabase()->
  getSymbolTable(pBlockTable, AcDb::kForRead);
      AcDbBlockTableRecord *pBlockTableRecord;
      pBlockTable->getAt(ACDB_MODEL_SPACE,
  pBlockTableRecord,AcDb::kForWrite);
    pBlockTable->close();
      AcDbObjectId aObjID;
      pBlockTableRecord->appendAcDbEntity(aObjID, paEnt);
    pBlockTableRecord->close();
    paEnt->close();
    return aObjID;
}
Here is the code for the commands:
// - ASDKTS70498_Raster_Zoom._Test command (do not rename)
 static void ASDKTS70498_Raster_Zoom_Test(void)
{
  fTest();
}
 // - ASDKTS70498_Raster_Zoom._setRatio command (do not rename)
 static void ASDKTS70498_Raster_Zoom_setRatio(void)
{
  fSetMaxMin();
}
Here is the code for the reactor:
//---------------------------------------------------------------
void AsdkEdReactor::commandEnded(const ACHAR* cmdStr)
{
 // TODO: implement this function.
 if ((!_tcscmp(cmdStr,_T("ZOOM"))||!_tcscmp(cmdStr,_T("PAN"))))
{
  fTest();
}
}

