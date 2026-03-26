---
title: "Modifying an Associative Path Array using API"
date: 2015-09-01
categories:
  - AutoCAD
tags:
  - API
description: "In this blog post, we will look at modifying an associative path array. A path array can either be using the item spacing or the item count dependi..."
author: Autodesk
---
# Modifying an Associative Path Array using API

发布日期: 2015-09-01

原始链接: https://adndevblog.typepad.com/autocad/2015/09/modifying-an-associative-path-array-using-api.html

## 文章内容

By Balaji Ramamoorthy
In this blog post, we will look at modifying an associative path array. A path array can either be using the item spacing or the item count depending on how the path array is configured in its properties. The below code snippet decrements the item count or increases the item spacing to reduce the number of items along the path.
Here is a recording and a code snippet :
 #include  "AcDbAssocManager.h" 
 #include  "AcDbAssocArrayActionBody.h" 
 #include  "AcDbAssocArrayPathParameters.h" 
   Acad::ErrorStatus es;
   ads_name ename; 
 ads_point pickPt;
 int  rc = acedEntSel(_T("\\nSelect Entity" ), ename, pickPt);
 if  (rc != RTNORM)
  return ;
 AcDbObjectId entId; 
 acdbGetObjectId(entId, ename);
   AcDbObjectPointer <AcDbEntity> pEntity(entId, AcDb::kForRead);
 if ((es = pEntity.openStatus()) != Acad::eOk)
  return ;
   if (! AcDbAssocArrayActionBody::isAssociativeArray(pEntity))
 {
  acutPrintf(ACRX_T("\\nNot an associative array !" ));
  return ;
 }
     AcDbObjectId actionBodyId 
  = AcDbAssocArrayActionBody::getControllingActionBody(
  pEntity, NULL);
 pEntity->close();
   AcDbAssocArrayActionBody* pArrayActionBody = NULL;
 if ( (es = acdbOpenAcDbObject(
  (AcDbObject*&)pArrayActionBody, 
  actionBodyId, 
  AcDb::kForWrite)) != Acad::eOk)
  return ;
   AcDbAssocArrayParameters *pAssocArrayParams 
  = pArrayActionBody->parameters();
 AcDbAssocArrayPathParameters *pAssocArrayPathParams 
  = AcDbAssocArrayPathParameters::cast(pAssocArrayParams);
   AcDbAssocArrayPathParameters::Method pathArrMethod 
  = pAssocArrayPathParams->method();
 if (pathArrMethod 
  == AcDbAssocArrayPathParameters::Method::kDivide)
 {
  //The Divide method arranges the given number of items on the  
  // entire path equidistantly.  
  // So we will decrement the number of items along the path 
  pAssocArrayPathParams->setItemCount
   (pAssocArrayPathParams->itemCount() - 1);
 }
 else  if (pathArrMethod 
  == AcDbAssocArrayPathParameters::Method::kMeasure)
 {
  double  itemSpacingBefore 
   = pAssocArrayPathParams->itemSpacing();
    //The Measure method arranges the given number of items  
  // using the specified item spacing along the path. 
  pAssocArrayPathParams->setItemSpacing
   (pAssocArrayPathParams->itemSpacing() * 1.1);
    double  itemSpacingAfter 
   = pAssocArrayPathParams->itemSpacing();
    if (fabs(itemSpacingBefore-itemSpacingAfter) < 0.0001)
  {// Reduce the number of items 
   pAssocArrayPathParams->setItemCount
    (pAssocArrayPathParams->itemCount() - 1);
   pAssocArrayPathParams->setItemSpacing
    (pAssocArrayPathParams->itemSpacing() * 1.1);
  }
 }
 pArrayActionBody->close();
   AcDbAssocManager::evaluateTopLevelNetwork(entId.database());
 acedUpdateDisplay();

