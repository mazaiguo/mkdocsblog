---
title: "Creating Assoc Array Objects with ObjectARX"
date: 2016-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "In this blog post, we will see how we can create Array objects, the three array parameters deriving from"
author: Autodesk
---
# Creating Assoc Array Objects with ObjectARX

发布日期: 2016-05-01

原始链接: https://adndevblog.typepad.com/autocad/2016/05/creating-assoc-array-objects-with-objectarx.html

## 文章内容

By Madhukar Moogala
In this blog post, we will see how we can create Array objects, the three array parameters deriving from
AcDbAssocArrayCommonParameters
AcDbAssocArrayPathParameters
AcDbAssocArrayPolarParameters
AcDbAssocArrayRectangularParameters
will be used to provide an interface for manipulating array parameters that are common to Rectangular, Path and Polar Arrays.
AcDbAssocArrayActionBody is an associative action that can be evaluated to manage or position array items based on Array parameters.
  Creating Path Array:
This array requires a guiding curve and source entity as profile to pattern along the curve, basically all arrays are represented as a block reference entity, which references an array block table record (array BTR). An array BTR contains a list of entities to represent items in the array. By default, this class represents an array item as an instance of AcDbBlocReference referencing a source block table record (source BTR) positioned at the item transform. 
  void createPathArray()
    {
    try
      {
          Acad::ErrorStatus es;
        // argument variables
        int nVarCount = 0;
        int index = 0;
          int isAssociative = 1;
        AcGePoint3d basePoint;
    double itemsapcing = 1.573;
        double rowSpacing = 1.5;
        double levelSpacing = 1;
        int itemCount = 1;
        int rowCount = 1;
        int levelCount = 1;
        double rowElevation = 1;
        int method=0;
          AcDbObjectId      profileEntityId;
        AcDbObjectId      CurveEntityId;
        AcDbEntity *      profileEntity = NULL;
        AcDbEntity *      curveEntity = NULL;
        AcDbObjectIdArray profileEntityIdArray;
        AcDbObjectId      arrayId;
        AcDbObjectId      actionBodyId;
      index = 1;
    isAssociative = 1;
    basePoint = basePoint.kOrigin;
          Adesk::Boolean isAssoc = !!isAssociative;
        AcDbVertexRef *basePointVertex = new AcDbVertexRef(basePoint);
          // create the profile entity
        profileEntity = createEntity(index);
        //post the newly created entity to database
        Adesk::Boolean rVal = post_to_database(profileEntity, profileEntityId);
    //This will create the path on which the array will be created
    index = 3;
        curveEntity =  createEntity(index); 
        AcDbLine* path =  (AcDbLine*)curveEntity;
    double param1,length;
    path->getEndParam(param1);
    path->getDistAtParam(param1,length);
        itemCount = int(length / itemsapcing);
        //post the newly created entity to database
        rVal = post_to_database(curveEntity, CurveEntityId);         
    if(rVal)
    {
      AcDbSmartObjectPointer<AcDbEntity> profileEntity1(profileEntityId,AcDb::kForRead);
      if(!eOkVerify(profileEntity1.openStatus())) return;
        AcDbSmartObjectPointer<AcDbEntity> curveEntity1(CurveEntityId,AcDb::kForRead);
      if(!eOkVerify(curveEntity1.openStatus()))return ;
      //Add the profile entity id to the profile entity id array
      profileEntityIdArray.append(profileEntityId);
          // Create the PathArrayParameters object
      AcDbAssocArrayPathParameters *pathParam =new AcDbAssocArrayPathParameters(itemsapcing,rowSpacing,
                                  levelSpacing,itemCount,rowCount,
                                  levelCount,rowElevation);
        //Add code to set the path of the array
       AcDbEdgeRef edge(curveEntity1);
       es=pathParam->setPath(edge);
       //Set the method Divide or Measure
       if(method==1)
        es= pathParam->setMethod(AcDbAssocArrayPathParameters::kDivide);
       else
         es= pathParam->setMethod(AcDbAssocArrayPathParameters::kMeasure);
          //Create the array from the source entities
      es = AcDbAssocArrayActionBody::createInstance(profileEntityIdArray,*basePointVertex,pathParam,arrayId,actionBodyId);
        // The newly created action will be automatically evaluated at the end
      // of the command.
      //
      // If we want to know whether the evaluation is going to succeed, we can
      // evaluate the network explicitly and check the evaluation status
      // of the action
      //
      bool beval= AcDbAssocManager::evaluateTopLevelNetwork(arrayId.database());
         if(pathParam!=NULL)
        delete pathParam;
    }
      } // try
    catch (...)
    {
        acutPrintf( _T("Exception Catch"));
    }
  }
  Creating Rectangular Array :
void createRectArray()
{
  try
  {
          // argument variables
       int index = 1;
      double columnSpacing = 10;
      double rowSpacing = 10;
      double levelSpacing = 10;
      int columnCount = 10;
      int rowCount =  10;
      int levelCount = 1;
      double rowElevation = 1;
      double axesAngle = 90;
      double rotation = 0;
      AcGePoint3d basePoint;
        AcDbObjectId      profileEntityId;
      AcDbEntity *      profileEntity = NULL;
      AcDbObjectIdArray profileEntityIdArray;
      AcDbObjectId      arrayId;
      AcDbObjectId      actionBodyId;
      basePoint = basePoint.kOrigin;
      AcDbVertexRef basePointVertex(basePoint);
           // create the profile entity based on the profile entity index
       profileEntity = createEntity(index);
           //post the newly created entity to database
       Adesk::Boolean rVal = post_to_database(profileEntity, profileEntityId);
     if(rVal)
     {
        //Add the profile entity id to the profile entity id array
       profileEntityIdArray.append(profileEntityId);
         // Create the AcDbRectangularParameters object
       AcDbAssocArrayRectangularParameters *rectParam = new AcDbAssocArrayRectangularParameters(columnSpacing,
                                   rowSpacing,levelSpacing,columnCount,rowCount,
                                   levelCount,rowElevation,axesAngle);
         //Create the array from the source entities
       if(!eOkVerify(AcDbAssocArrayActionBody::createInstance(profileEntityIdArray,basePointVertex,rectParam,arrayId,actionBodyId))) return;
      // The newly created action will be automatically evaluated at the end
        // of the command.
        //
        // If we want to know whether the evaluation is going to succeed, we can
        // evaluate the network explicitly and check the evaluation status
        // of the action
        //
       bool beval = AcDbAssocManager::evaluateTopLevelNetwork(arrayId.database());
     }
         } // try
   catch (...)
   {
       acutPrintf( _T("Exception Catch: Acad::eUnrecoverableErrors"));
   } // catch
  }
  Creating Polar Array :
void createPolarArray()
  {
  Acad::ErrorStatus es;
  try
    {
  // argument variables
  int NoOfSrcEntities = 2;
  int index = 1;
  double columnSpacing = 0;
  double rowSpacing = 10;
  double levelSpacing = 5;
  int itemCount = 6;
  int rowCount = 2;
  int levelCount = 2;
  double rowElevation = 3;
  double Angle = 90;
    AcGePoint3d basePoint;
  basePoint = basePoint.kOrigin;
      AcDbObjectId      profileEntity1Id;
  AcDbObjectId      profileEntity2Id;
    AcDbEntity *      profileEntity1 = NULL;
  AcDbEntity *      profileEntity2 = NULL;
    AcDbObjectIdArray profileEntityIdArray;
  AcDbObjectId      arrayId;
  AcDbObjectId      actionBodyId;
      AcDbVertexRef *basePointVertex = new AcDbVertexRef(basePoint);
    // create the profile entity based on the profile entity index
  profileEntity1 = createEntity(index);          
    //post the newly created entity to database
  Adesk::Boolean rval = post_to_database(profileEntity1, profileEntity1Id);
  if(rval)
    {
    //Add the profile entity id to the profile entity id array
    profileEntityIdArray.append(profileEntity1Id);
      //Create AcDbAssocArrayParameters
    AcDbAssocArrayPolarParameters *polarParam = new AcDbAssocArrayPolarParameters (Angle,rowSpacing,levelSpacing,itemCount,rowCount,levelCount,rowElevation);
      //Create the array from the source entities
    es = AcDbAssocArrayActionBody::createInstance(profileEntityIdArray,*basePointVertex,polarParam,arrayId,actionBodyId);
      // The newly created action will be automatically evaluated at the end
        // of the command.
        //
        // If we want to know whether the evaluation is going to succeed, we can
        // evaluate the network explicitly and check the evaluation status
        // of the action
        //
    bool beval = AcDbAssocManager::evaluateTopLevelNetwork(arrayId.database());
      }
    }
  catch(...)
    {
      acutPrintf( _T("Exception Catch: Acad::eUnrecoverableErrors"));
    }
  }
  Utility and Command Method:
    /*Util Method To create Entity*/
  AcDbEntity* createEntity(int index)
    {
    AcDbEntity* entity = NULL;
    AcGePoint3d startPt(0,0,0);
    AcGePoint3d endPt(20,20,0);
      switch(index)
      {
      /*Profile 1*/
      case 1:
        {
        AcDbCircle* c = new AcDbCircle(AcGePoint3d(0.0,0.0,0.0),AcGeVector3d(0.0,0.0,1.0),0.5);
        entity = (AcDbEntity*)c;
        break;
        }
      /*Profile 2*/
      case 2:
        {
        AcDbPolyline *pRect = new AcDbPolyline();
        AcGePoint2d vertex1(startPt.x,startPt.y);
        AcGePoint2d vertex2(endPt.x,startPt.y);
        AcGePoint2d vertex3(endPt.x,endPt.y);
        AcGePoint2d vertex4(startPt.x,endPt.y);
        pRect->addVertexAt(0,vertex1);
        pRect->addVertexAt(1,vertex2);
        pRect->addVertexAt(2,vertex3);
        pRect->addVertexAt(3,vertex4);
        pRect->setClosed(Adesk::kTrue);
        entity = (AcDbEntity*)pRect;
        break;
        }
             /*Path for Path ARRAY*/
      case 3:
        {
        AcDbLine *line = new AcDbLine(startPt,endPt);
        entity = (AcDbEntity*)line;
        break;
        }
      default:
        break;
      }
      return entity;
    }
        void createArray()
  {
      CString prompt = _T("Select Type of array :"); 
    acedInitGet(0, _T("Curve Rect Polar"));
    ACHAR kword[255]; ACHAR pr[255];
    wsprintf(pr, ACRX_T("%s Curve/Rect/<Polar>"), prompt);
   if(acedGetKword(pr, kword) == RTNORM)
     {
     if(!_tcscmp(kword,L"Curve"))
       {
       acutPrintf(_T("Curve\n"));
       createPathArray();
       }
     else if(!_tcscmp(kword,L"Rect"))
       {
        acutPrintf(_T("Rect\n"));
        createRectArray();
       }
    else if(!_tcscmp(kword,L"Polar"))
      {
      acutPrintf(_T("Polar\n"));
      createPolarArray();
      }
    else
    {
    acutPrintf(_T("InvalidInput"));
    }
     }     
  }
    //**************************************************************
extern "C"
  AcRx::AppRetCode acrxEntryPoint(AcRx::AppMsgCode msg, void *pkt)
  //**************************************************************
  {
  switch(msg)
    {
    case AcRx::kInitAppMsg:
      acrxDynamicLinker->unlockApplication(pkt);
      acrxDynamicLinker->registerAppMDIAware(pkt);   
      acedRegCmds->addCommand(_T("TestCmd"),_T("ARY"),_T("ARY"), ACRX_CMD_TRANSPARENT,createArray);
      break;
      case AcRx::kUnloadAppMsg:
      acedRegCmds->removeGroup(_T("TestCmd"));
        break;
      default:
      break;
    }
  return AcRx::kRetOK;
  }
  Screecast of Different Arrays

