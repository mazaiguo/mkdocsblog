---
title: "Making a custom entity Associative Dimension enabled"
date: 2015-02-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Dimension
description: "You can create associative dimensions after setting the system variable DIMASSOC value to 2 and calling any of the dimensioning commands. This work..."
author: Autodesk
---
# Making a custom entity Associative Dimension enabled

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/making-a-custom-entity-associative-dimension-enabled.html

## 文章内容

By Balaji Ramamoorthy
You can create associative dimensions after setting the system variable DIMASSOC value to 2 and calling any of the dimensioning commands. This works fine on all the native AutoCAD entities, but it does not with your own custom entity. To enable associative dimensioning for your custom entity, there are two ways. In this blog post and in its attached sample, these are demonstrated.
Before we look at sample code, here is a short video of its working :
Method 1 : 
You need to take help of few exported APIs in AcDimX20.dll. Unfortunately these are not published APIs and hence they are *not supported* and you have to use them at your own risk.
The three APIs exported in the AcDimX20.dll are:

Acad::ErrorStatus acdbEnableDimAssocForEntity(AcRxClass* pClass)
Acad::ErrorStatus acdbDisableDimAssocForEntity(AcRxClass* pClass)
bool acdbDimAssocIsEnabledForEntity(AcRxClass* pClass)

Their function is self explanatory. The AcDimX.dll file is available in the AutoCAD install folder.

Using acdbEnableDimAssocForEntity() API you can enable associative dimensioning for your custom entity. In the attached sample project, "MyEnt2" uses this approach.

You should look at the On_kInitAppMsg() function in the acrxEntryPoint.cpp that registers the custom entity class for associative dimensioning.

Also, you *must* implement subSubentPtr() override for your custom entity. In the attached sample project, "MyEnt2" is a custom entity that enables associative dimension using this method. It has subSubentPtr method implemented which allows the user to use associative dimensioning at its end points.
Here is the relevant portion of the code. To try it, please download the attached sample project.
 typedef  Acad::ErrorStatus 
  (*exp_acdbDimAssocForEntity)(AcRxClass* pClass);
   MyEnt2::rxInit();
 acrxBuildClassHierarchy();
 HMODULE hModule = LoadLibrary( _T("AcDimX20.dll" ));
   exp_acdbDimAssocForEntity fPtrEnableDimAssoc = NULL;
 if  (NULL != hModule)
 {
  fPtrEnableDimAssoc = (exp_acdbDimAssocForEntity)
   GetProcAddress(hModule, 
   "acdbEnableDimAssocForEntity" );
 }
   Acad::ErrorStatus es;
 if (fPtrEnableDimAssoc)
 {
  // Enable associative dimension for MyEnt2 using  
  // acdbEnableDimAssocForEntity 
  es = fPtrEnableDimAssoc(MyEnt2::desc());
 }
   //free the library 
 if  (NULL != hModule)
 {
  FreeLibrary(hModule);
 }
  Method 2 :
For custom entity derived from AcDb3dSolid and AcDbSurface, Method 1 does not work. Here is the explanation provided by Jiri Kripac from our engineering team on why the first approach does not work :
AcDb3dSolid and AcDbSurface use the new associativity mechanism based on the Associative Framework. The associative dimension is controlled by an action derived from AcDbAssocAnnotationActionBody, not by the legacy AcDbDimAssoc. This allows to maintain associativity even when the topology of the solid/surface changes because the new mechanism uses persistent subentity ids (complex internal objects) to persistently identify subentities (faces/edges/vertices) of the entity, whereas AcDbDimAssoc uses just simple indices that become invalid when the topology of the entity changes.
Entities reveal their subentities by implementing AcDbAssocPersSubentIdPE. The Associative Framework queries this protocol extension when creating new associative dimensions based on AcDbAssocAnnotationActionBody. AcDb3dSolid exposes this protocol extension. Your custom entity derived from AcDb3dSolid does not expose this protocol extension to reveal your subentities, therefore the base class protocol extension for AcDb3dSolid is used that reveals subentities of the solid. 
You need to implement AcDbAssocPersSubentIdPE to reveal your subentities of your custom entity.
In the attached sample project, "MyEnt1" is a custom entity derived from AcDb3dSolid and implements AcDbAssocPersSubentIdPE to reveal its subentities.
The header file of "AcDbAssocPersSubentIdPE" is very well documented by our engineering team. Please read it and that should help in customizing it for your custom entity. Here is the relevant portion of the custom AcDbAssocPersSubentIdPE implementation for "MyEnt1" custom entity from the attached sample project.
 // MyEntPersSubentIdPE.cpp 
   AcDbAssocPersSubentId* MyEntPersSubentIdPE::
  createNewPersSubent(
      AcDbEntity*                 pEntity,
      AcDbDatabase*               pDatabase,
                     const  AcDbCompoundObjectId& compId,
                     const  AcDbSubentId&         subentId)
 {
  switch (subentId.index())
  {
   case  100: 
    return  new  AcDbAssocEdgePersSubentId(101, 102);
     case  101: 
    return  new  AcDbAssocEdgePersSubentId(101, 0);
     case  102: 
    return  new  AcDbAssocEdgePersSubentId(102, 0);
     default :
   {
    acutPrintf(ACRX_T("\\n createNewPersSubent  
     not implemented !!")); 
    break ;
   }
  }
     return  new  AcDbAssocSimplePersSubentId(subentId);
 }
   Acad::ErrorStatus MyEntPersSubentIdPE::
     getTransientSubentIds(
     const  AcDbEntity* pEntity, 
                 AcDbDatabase*                pDatabase,
                 const  AcDbAssocPersSubentId* pPersSubentId,
                 AcArray<AcDbSubentId>&       subents) const 
 {
  Acad::ErrorStatus es = Acad::eNotImplemented;
    MyEnt1 *pMyEnt1 = MyEnt1::cast(pEntity);
  if (pMyEnt1 != NULL)
  {
   AcDbAssocEdgePersSubentId *pEdgePerSubEntId 
    = AcDbAssocEdgePersSubentId::cast(pPersSubentId);
   if (pEdgePerSubEntId != NULL)
   {
    int  index1 = pEdgePerSubEntId->index1();
    int  index2 = pEdgePerSubEntId->index2();
    if (index2 == 0)
    {
     subents.append(
      AcDbSubentId(
      AcDb::kVertexSubentType, 
      index1));
    }
    else 
    {
     subents.append(
      AcDbSubentId(
      AcDb::kEdgeSubentType, 
      100));
    }
      return  Acad::eOk;
   }
  }
  return  es;
 }
   Acad::ErrorStatus MyEntPersSubentIdPE::
    getAllSubentities(
      const  AcDbEntity* pEntity,
      AcDb::SubentType subentType,
                     AcArray<AcDbSubentId>& allSubentIds)
 {
  Acad::ErrorStatus es = Acad::eNotImplemented;
    MyEnt1 *pMyEnt1 = MyEnt1::cast(pEntity);
  if (pMyEnt1 != NULL)
  {
   if (subentType == AcDb::kEdgeSubentType)
   {
    allSubentIds.append(
     AcDbSubentId(AcDb::kEdgeSubentType, 100));
    return  Acad::eOk;
   }
   else  if (subentType == AcDb::kVertexSubentType)
   {
    allSubentIds.append(
     AcDbSubentId(
     AcDb::kVertexSubentType, 101));
      allSubentIds.append(
     AcDbSubentId(
     AcDb::kVertexSubentType, 102));
    return  Acad::eOk;
   }
  }
     return  es;
 }
   Acad::ErrorStatus MyEntPersSubentIdPE::
     getEdgeVertexSubentities(
     const  AcDbEntity*      pEntity,
                 const  AcDbSubentId&    edgeSubentId,
     AcDbSubentId&          startVertexSubentId,
                 AcDbSubentId&          endVertexSubentId,
     AcArray<AcDbSubentId>& otherVertexSubentIds)
 {
    Acad::ErrorStatus es = Acad::eNotImplemented;
    MyEnt1 *pMyEnt1 = MyEnt1::cast(pEntity);
  Adesk::GsMarker gsMarker = edgeSubentId.index();
  switch (gsMarker)
  {
   case  100:
    startVertexSubentId = AcDbSubentId(
     AcDb::kVertexSubentType, 101);
    endVertexSubentId = AcDbSubentId(
     AcDb::kVertexSubentType, 102);
    return  Acad::eOk;
     default :
   {
    acutPrintf(ACRX_T(
     "\\n getEdgeVertexSubentities  
     not implemented !!")); 
    break ;
   }
  }
     return  es;
 }
   Acad::ErrorStatus MyEntPersSubentIdPE::
     getVertexSubentityGeometry(
     const  AcDbEntity*   pEntity,
                 const  AcDbSubentId& vertexSubentId,
                 AcGePoint3d&        vertexPosition)
 {
  Acad::ErrorStatus es =  Acad::eNotImplemented;
    MyEnt1 *pMyEnt1 = MyEnt1::cast(pEntity);
    Adesk::GsMarker gsMarker = vertexSubentId.index();
  switch (gsMarker)
  {
   case  100:
   {
    acutPrintf(ACRX_T("\\n  
     getVertexSubentityGeometry 
     not implemented for  %d !!"), gsMarker); 
    vertexPosition = pMyEnt1->m_ptEP;
    return  Acad::eOk;
   }
     case  101:
    vertexPosition = pMyEnt1->m_ptSP;
    return  Acad::eOk;
     case  102:
    vertexPosition = pMyEnt1->m_ptEP;
    return  Acad::eOk;
     case  0: 
    return  Acad::eOk;
     default  :
   {
    acutPrintf(ACRX_T("\\n  
     getVertexSubentityGeometry 
     not implemented !!")); 
    break ;
   }
  }
     return  es;
 }
   Acad::ErrorStatus MyEntPersSubentIdPE::
    getEdgeSubentityGeometry(
     const  AcDbEntity*   pEntity,
                 const  AcDbSubentId& edgeSubentId,
                 AcGeCurve3d*&       pEdgeCurve)
 {
  Acad::ErrorStatus es =  Acad::eNotImplemented;
    MyEnt1 *pMyEnt1 = MyEnt1::cast(pEntity);
  switch (edgeSubentId.index())
  {
   case  100:
    pEdgeCurve = new  AcGeLine3d(
     pMyEnt1->m_ptSP, pMyEnt1->m_ptEP);
    return  Acad::eOk;
     default :
   {
    acutPrintf(ACRX_T("\\n  
     getEdgeSubentityGeometry 
     not implemented for  %d!!"),  
     edgeSubentId.index());
    break ;
   }
  }
       return  es;
 }
  Here is the project for download :
Download Customentity_assocdimEnabled

