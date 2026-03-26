---
title: "Dynamic dimension using GripOverrule"
date: 2015-06-01
categories:
  - AutoCAD
tags:
  - Dimension
description: "Dynamic dimensions are an easy and intuitive way to let users modify entity dimensions using grips. For this to work, the dimensional input is to b..."
author: Autodesk
---
# Dynamic dimension using GripOverrule

发布日期: 2015-06-01

原始链接: https://adndevblog.typepad.com/autocad/2015/06/dynamic-dimension-using-gripoverrule.html

## 文章内容

By Balaji Ramamoorthy
Dynamic dimensions are an easy and intuitive way to let users modify entity dimensions using grips. For this to work, the dimensional input is to be turned on by setting the DYNMODE system variable to either 2 or 3. If you wish to change the default grip editing behavior for an entity and prompt for another dimension that is more intuitive and readily available for users, grip overrule can help do that.
For a circle, when a grip turns hot, a dynamic dimension appears prompting for the radius value. In the following sample code, we will change that to accept diameter value by displaying a dynamic dimension diametrically on the circle being grid edited. Also, the prompt at the command line window is changed to make the user aware of the diameter input that we are expecting.
Here is a recording of the behavior with/without the grip overrule and the sample code :
 #include  "dbentityoverrule.h" 
   class  CMyGripOverrule: public  AcDbGripOverrule
 {
 public :
    static  CMyGripOverrule* _pTheOverrule;
  ACRX_DECLARE_MEMBERS(CMyGripOverrule);
    static  AcDbDimData *mpDimData;
    static  void  CMyGripOverrule::AddOverrule()
  {
   mpDimData = NULL;
     if (_pTheOverrule != NULL)
    return ;
     _pTheOverrule = new  CMyGripOverrule();
     AcRxOverrule::addOverrule(
       AcDbCircle::desc(),
       _pTheOverrule, 
       true 
       );
       CMyGripOverrule::setIsOverruling(true );
  }
    static  void  CMyGripOverrule::RemoveOverrule()
  {
   if (_pTheOverrule == NULL)
    return ;
     CMyGripOverrule::setIsOverruling(false );
     AcRxOverrule::removeOverrule(
      AcDbCircle::desc(), 
      _pTheOverrule
      );
   delete  _pTheOverrule;
     _pTheOverrule = NULL;
  }
    ACDB_PORT Acad::ErrorStatus moveGripPointsAt(
       AcDbEntity* pSubject,
                         const  AcDbVoidPtrArray& gripAppData,
                         const  AcGeVector3d& offset, 
                         const  int  bitflags)
  {
   if  (!pSubject->isKindOf(AcDbCircle::desc())) 
    return  Acad::eOk;
     AcDbCircle* pCircle = AcDbCircle::cast(pSubject);
     if  (pCircle == NULL) 
    return  Acad::eOk;
     AcGeVector3d normal = pCircle->normal();
   AcGeVector3d horizDir = normal.perpVector();
   AcGePoint3d center = pCircle->center();
   double  radius = pCircle->radius();
     AcGePoint3d pt1 = center + radius * horizDir;
   pt1 = pt1 + offset;
   AcGeVector3d radVec = pt1 - center;
     updateDimensions(
    pCircle, 
    center-radVec, 
    center+radVec);
     AcDbGripOverrule::moveGripPointsAt(
    pSubject, 
    gripAppData, 
    offset, 
    bitflags); 
  }
    ACDB_PORT Acad::ErrorStatus getGripPoints(
   const  AcDbEntity* pSubject, 
   AcDbGripDataPtrArray& grips, 
   const  double  curViewUnitSize, 
   const  int  gripSize, 
   const  AcGeVector3d& curViewDir, 
   const  int  bitflags
  )
  {
   if  (!pSubject->isKindOf(AcDbCircle::desc())) 
    return  Acad::eOk;
     AcDbCircle* pCircle 
    = AcDbCircle::cast(pSubject);
     if  (pCircle == NULL) 
    return  Acad::eOk;
     AcDbGripDataPtrArray oldGrips;
   AcDbGripOverrule::getGripPoints(
    pSubject, oldGrips, 
    curViewUnitSize, gripSize, 
    curViewDir, bitflags); 
     AcDbGripData * pGripData 
    = new  AcDbGripData(*(oldGrips.at(1)));
     pGripData->setGripPoint
    (oldGrips.at(1)->gripPoint());
     pGripData->setHotGripDimensionFunc
    (MyGripHotGripDimensionfunc);
     pGripData->setHoverDimensionFunc
    (MyHoverGripDimensionfunc);
     pGripData->setCLIPromptFunc
    (MyGripCLIPromptCallback);
     grips.append(pGripData);
     return  Acad::eOk;
  }
    static  void  gripDimensionCbackFunc(
   AcDbGripData* pGrip, 
   const  AcDbObjectId& objId, 
   double  dimScale, 
   AcDbDimDataPtrArray& dimDataArr)
  {
   Acad::ErrorStatus es;
     if  (pGrip == NULL)
    return ;
     AcDbEntity *pEnt = NULL;
   if  (acdbOpenAcDbEntity(
    pEnt, objId, 
    AcDb::kForRead) != Acad::eOk)
    return ;
     AcDbCircle *pCircle 
    = AcDbCircle::cast(pEnt);
   if  (pCircle == NULL) {
    pEnt->close();
    return ;
   }
     AcGeVector3d normal = pCircle->normal();
   AcGeVector3d horizDir = normal.perpVector();
   AcGeVector3d vertDir 
    = normal.crossProduct(horizDir);
   AcGePoint3d center = pCircle->center();
   double  radius = pCircle->radius();
     pCircle->close();
     AcDbAlignedDimension *pAlignedDim 
    = new  AcDbAlignedDimension();
   pAlignedDim->setDatabaseDefaults();
     es = pAlignedDim->setDimsah(true );
   es = pAlignedDim->setDimse1(true );
   es = pAlignedDim->setDimblk1(_T("None" ));
   es = pAlignedDim->setNormal(normal);
   es = pAlignedDim->setElevation(0.0);
   es = pAlignedDim->setHorizontalRotation(0.0);
   es = pAlignedDim->setXLine1Point
    (center - radius * horizDir);
      es = pAlignedDim->setXLine2Point
    (center + radius * horizDir);
   es = pAlignedDim->setDimLinePoint
    (center + 0.5 * radius * horizDir);
   es = pAlignedDim->setDynamicDimension(true );
   es = pAlignedDim->setColorIndex(1);
     AcDbDimData *pDimData 
    = new  AcDbDimData(pAlignedDim);
   es = pDimData->setOwnerId(objId);
   es = pDimData->setDimFocal(true );
   es = pDimData->setDimEditable(true );
   es = pDimData->setDimRadius(true );
   es = pDimData->setDimHideIfValueIsZero(true );
   es = pDimData->setDimValueFunc
    (setDimValueCbackFunc);
   es = pDimData->setDimension(pAlignedDim);
     dimDataArr.append(pDimData);
   mpDimData = pDimData;
  }
    bool  isApplicable(
   const  AcRxObject *pOverruledSubject) const 
  {
   if  (!pOverruledSubject->isKindOf
    (AcDbCircle::desc())) 
    return  false ;
   return  true ;
  }
     static  const  ACHAR* MyGripCLIPromptCallback
   (AcDbGripData *pGripData)
  {
   return  ACRX_T("\\nRing diameter : " ); 
  }
     static  void  MyGripHotGripDimensionfunc
   (AcDbGripData *pGripData, 
   const  AcDbObjectId &entId, 
   double  dimScale, 
   AcDbDimDataPtrArray &dimDataArr)
  {
   gripDimensionCbackFunc
    (pGripData, entId, dimScale, dimDataArr);
  }
    static  void  MyHoverGripDimensionfunc
   (AcDbGripData *pGripData, 
   const  AcDbObjectId &entId, 
   double  dimScale, 
   AcDbDimDataPtrArray &dimDataArr)
  {
   gripDimensionCbackFunc(pGripData, 
    entId, dimScale, dimDataArr);
  }
    static  AcGeVector3d setDimValueCbackFunc
   (AcDbDimData* pDimData, AcDbEntity* pEnt, 
   double  newValue, const  AcGeVector3d& offset)
  {
   AcGeVector3d newOffset(offset);
     if  ((pDimData == NULL) || (pEnt == NULL))
    return  newOffset;
     AcDbObjectId objId;
     AcDbCircle *pCir = AcDbCircle::cast(pEnt);
       if  (pCir == NULL)
    return  newOffset;
       pCir->setRadius(newValue * 0.5);
       return  newOffset;
  }
    static  bool  updateDimensions
   (AcDbCircle* pCircle, 
   AcGePoint3d xline1Pt, 
   AcGePoint3d xline2Pt)
  {
   if  (!pCircle || !mpDimData)
    return  false ;
     AcDbObjectId entId = pCircle->objectId();
   AcGeVector3d normal = pCircle->normal();
   AcGeVector3d horizDir = normal.perpVector();
   AcGeVector3d vertDir 
    = normal.crossProduct(horizDir);
   AcGePoint3d center = pCircle->center();
   double  radius = pCircle->radius();
     AcDbObjectId ownerId;
     AcDbDimData *pDimData = mpDimData;
   AcDbAlignedDimension *pAlignedDim 
    = AcDbAlignedDimension::cast(
    pDimData->dimension());
     if (pAlignedDim != NULL)
   {
    pAlignedDim->setXLine1Point(xline1Pt);
    pAlignedDim->setXLine2Point(xline2Pt);
    pAlignedDim->setDimLinePoint
     (xline1Pt + (xline2Pt - xline1Pt) * 0.5);
   }
   return  true ;
  }
 };
   AcDbDimData * CMyGripOverrule::mpDimData = NULL;
 CMyGripOverrule* CMyGripOverrule::_pTheOverrule = NULL;
   ACRX_NO_CONS_DEFINE_MEMBERS(
  CMyGripOverrule, 
  AcDbGripOverrule);

## 评论

**内容**: Keith Brown said...
Would it be possible to share a .net version of the code?
Reply
06/05/2015 at 09:02 AM

---
**内容**: Balaji said...
Hi Keith,
There are few missing API in the .Net version of the AcDbGripData and AcDbDimData classes which prevents from doing the same using .Net. I have logged them in our internal database for our engineering team to look at these missing API.
Sorry, it will not be possible to do the same at present using AutoCAD .Net API.
Regards,
Balaji
Reply
06/05/2015 at 08:57 PM

---
**内容**: CHRISTOPHER FUGITT said...
So I think I have most of a wrapper created for this in order to get it to work in c#.net. One of the last things that I think I need is a way to wrap the setDimValueFunc. Is this possible?
So far in the header file I have:
Acad::ErrorStatus setDimValueFunc(
DimDataSetValueFuncPtr funcPtr
);
Which doesn't work since .Net doesn't have the DimDataSetValueFuncPtr object. Do you know of a a way to create a wrapper for it since it is looking for this format for the function Ptr:
typedef void (*DimDataSetValueFuncPtr) (AcDbDimData* pThis, AcDbEntity* pEnt, double newValue, const AcGeVector3d& offset);
Here is a link to the c++ code I've created so far: https://drive.google.com/file/d/0B5Fp8nCG-F8vTE90YTF4amJFYW8/view?usp=sharing
Reply
06/15/2015 at 03:02 AM

---
**内容**: Balaji said in reply to CHRISTOPHER FUGITT...
Sorry, I am not aware of a way to implement that missing callback method in a .Net wrapper.
Regards,
Balaji
Reply
06/15/2015 at 09:03 PM

---
**内容**: Dan said...
If I want to add the standard dynamic dimensions to my custom objects (AcDbPolyline derived), do I just add similar code directly to my objects handlers? Can I point at any existing base class implementation, or do I have to re-implement the basics? (I just want angle and length as 'normal')
Reply
08/15/2016 at 07:25 PM

---
