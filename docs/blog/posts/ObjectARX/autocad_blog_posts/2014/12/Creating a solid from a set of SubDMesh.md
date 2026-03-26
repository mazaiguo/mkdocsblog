---
title: "Creating a solid from a set of SubDMesh"
date: 2014-12-01
categories:
  - AutoCAD
tags:
  - Solid
  - Surface
description: "If you have a collection of subDMesh and wish to create a Solid from it, first convert each of those mesh to a surface. If the sufaces all put toge..."
author: Autodesk
---
# Creating a solid from a set of SubDMesh

发布日期: 2014-12-01

原始链接: https://adndevblog.typepad.com/autocad/2014/12/creating-a-solid-from-a-set-of-subdmesh.html

## 文章内容

By Balaji Ramamoorthy
If you have a collection of subDMesh and wish to create a Solid from it, first convert each of those mesh to a surface. If the sufaces all put together form a closed volume, then a sculpted solid can be created from these surfaces. Here is a sample code snippet :
 // For SubDMesh  
 #include  "dbSubD.h" 
   static  void  AdskMeshToSolid()
 {
  Acad::ErrorStatus es;
  int  ret;
    // Select the meshes to create the solid from 
  AcArray<AcDbObjectId> meshIdArray;
  do 
  {
   ads_name entName;
   ads_point pt;
   ret = acedEntSel(L"Select a mesh : " , 
       entName, pt);
     if (RTNORM != ret) 
    break ;
     AcDbObjectId objId = AcDbObjectId::kNull;
   if ( Acad::eOk != acdbGetObjectId(objId, entName)) 
    break ;
     if (objId.objectClass() == AcDbSubDMesh::desc())
   {
    meshIdArray.append(objId);
   }
  }while (ret == RTNORM);
    // Convert the meshes to surfaces 
  AcArray<AcDbEntity*> surfacesArray;
  AcGeIntArray limits;
  AcDbSurface *pSurface = NULL;
    for (int  mesh = 0; mesh < meshIdArray.length(); mesh++)
  {
   AcDbEntity *pEntity = NULL; 
   if (acdbOpenAcDbEntity(pEntity, meshIdArray[mesh], 
        AcDb::kForRead) != Acad::eOk) 
   {
    return ; 
   }
        AcDbSubDMesh *pMesh = AcDbSubDMesh::cast(pEntity); 
   if (pMesh)
   {
    es = pMesh->convertToSurface(
        false , 
        false , 
        pSurface);
      if (es != Acad::eOk)
     return ;
      if  ( es == Acad::eOk && 
     pSurface->isKindOf(AcDbSurface::desc()))
    {
     surfacesArray.append(pSurface);
    }
   }
     pEntity->close();
  }
    // Create a sculpted solid from surfaces 
  AcDb3dSolid *pSolid = new  AcDb3dSolid();
  pSolid->setDatabaseDefaults();
       es = pSolid->createSculptedSolid(
      surfacesArray, 
      limits);
    if (es == Acad::eOk)
  {
   // Add sculpted solid to the database  
   AcDbObjectId solidOid = AcDbObjectId::kNull;
   postToDb(pSolid, &solidOid);
      // To show the newly created solid away 
   // from the surfaces, we transform it.. 
   AcDbEntity *pSolidEnt;
   es = acdbOpenAcDbEntity(
     pSolidEnt, solidOid, AcDb::kForWrite);
   if   (es == Acad::eOk &&
     pSolidEnt->isKindOf(AcDb3dSolid::desc()))
   {
    AcGeVector3d vec(15.0, 15.0, 0.0);
    AcGeMatrix3d transform 
       = transform.setToTranslation(vec);
    es = pSolidEnt->transformBy(transform);
    pSolidEnt->close();
    acutPrintf(
     ACRX_T("Solid3d created from mesh !" ));
   }
   else 
   {
    acutPrintf(
     ACRX_T("Solid3d creation failed !" ));
   }
  }
  else 
  {
   acutPrintf(ACRX_T("Solid3d creation failed !" ));
   delete  pSolid;
  }
     // Cleanup 
  // We do not need the surfaces anymore 
  int  surfCnt = 0;
  for (;surfCnt < surfacesArray.length(); surfCnt++)
  {
   AcDbEntity *pEnt = surfacesArray[surfCnt];
   delete  pEnt;
  }
 }
   static  void  postToDb( AcDbEntity* pEnt, AcDbObjectId *pOid) 
 {
  AcDbBlockTable* pBlockTable;
  AcDbDatabase *pDb = 
   acdbHostApplicationServices()->workingDatabase();
  pDb->getBlockTable(pBlockTable, AcDb::kForRead);
     AcDbBlockTableRecord* pModelSpaceBTR =  NULL; 
  pBlockTable->getAt(
   ACDB_MODEL_SPACE, 
   pModelSpaceBTR, 
   AcDb::kForWrite);
     AcDbObjectId oid = AcDbObjectId::kNull;
  if (pOid != NULL)
  {
   pModelSpaceBTR->appendAcDbEntity(*pOid, pEnt);
  }
  else 
  {
   pModelSpaceBTR->appendAcDbEntity(oid, pEnt);
  }
  pEnt->close(); 
     pModelSpaceBTR->close();
  pBlockTable->close();
 }
  Here is a screenshot of the output

