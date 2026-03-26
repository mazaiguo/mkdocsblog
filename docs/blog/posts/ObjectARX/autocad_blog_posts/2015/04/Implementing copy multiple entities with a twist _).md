---
title: "Implementing copy multiple entities with a twist :)"
date: 2015-04-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - AutoLISP
  - C++
  - Dimension
description: "In a recent query, a developer mentioned about a behavior of the AutoCAD's COPYcommand which I thought was a little different from how some of the ..."
author: Autodesk
---
# Implementing copy multiple entities with a twist :)

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/implementing-copy-multiple-entities-with-a-twist-.html

## 文章内容

By Balaji Ramamoorthy
In a recent query, a developer mentioned about a behavior of the AutoCAD's COPYcommand which I thought was a little different from how some of the other commands behaved. In the COPY command when multiple entities are selected for copying and after a base point is chosen, AutoCAD places copies of the selected entities as expected. But when the Enter key is hit, we would usually want the command to terminate like most other AutoCAD commands do. But in case of the COPY command, hitting the Enter key is treated as a "use first point as displacement" and a copy is placed before terminating the command. 
If you do not want this behavior, you may need to implement the copy multiple entities command which is simple to do. Here is a sample code that implements it using ObjectARX API and exposes it as Lisp callable. Additionally, while dragging the entities the position is constrained along X axis just as the .yz coordinate filter would do with the native COPY command.
Here is the code snippet :
 // Global, so it can be used in the 
 // DragGen callback function... 
 AcGePoint3d basePt;
   // Here is the callback... 
 static  int  dragGenCallback(ads_point pt,ads_matrix mt)
 {
      //AcGeVector3d vec(pt[0]-basePt[0],  
   // pt[1]-basePt[1], pt[2]-basePt[2]); 
     // To restrict dragging movement to X axis alone 
   AcGeVector3d vec(pt[0]-basePt[0], 0, 0);
        AcGeMatrix3d mat;
      // Set our matrix to translate the mouse  
   // movements... 
      mat.setToTranslation(vec);
      // And place the results in mt 
      for (int  c=0;c<4;c++)
      {
           for (int  cd=0;cd<4;cd++)
           mt[c][cd]=mat(c,cd);
      }
      return  RTNORM;
 }
   int  CopyMultipleEntitiesFunc()
 {
   ads_name ss;   
        // Get the Selection Set 
      acedSSGet(NULL, NULL, NULL, NULL, ss); 
        // Base Point for copying... 
      acedGetPoint(NULL, 
                   L"Specify base point" , 
                    asDblArray(basePt));
      long  len;
      acedSSLength(ss,&len);
      int  ret = 0;
   do 
   {
   //Value of the's final location  
   //after the user finishes 
   // dragging the selection set  
   AcGePoint3d final_pt;
     // Call DragGen with the callback function 
   ret = acedDragGen(ss, 
      L"\\nSpecify second point" , 
      0, 
      dragGenCallback, 
      asDblArray(final_pt));
     if (ret == RTNONE || ret == RTCAN)
   {// enter key hit or cancelled 
    break ;
   }
     // get the final matirx and do your work  
   // such as copy with the value of final_pt  
   AcDbDatabase* pDb 
    = acdbHostApplicationServices()
    ->workingDatabase();
   AcDbObjectIdArray idArr;
   {
    long  l=0, lNumber=0;
    ads_sslength(ss, &lNumber);
    idArr.setPhysicalLength(lNumber);
    for  (; l<lNumber; ++l)
    {
     ads_name ent;
     ads_ssname(ss, l, ent);
     AcDbObjectId idEnt;
     if  (Acad::eOk 
      == acdbGetObjectId(idEnt,ent))
     {
      idArr.append(idEnt);
     }
    }
      AcDbIdMapping idMapping;
    AcDbObjectId idOwner 
     =acdbSymUtil()->blockModelSpaceId (pDb);
    Acad::ErrorStatus es = curDoc()->database()
     ->deepCloneObjects(idArr, 
     idOwner, idMapping);
      if (es == Acad::eOk)
    {
     AcDbIdMappingIter iter2 (idMapping) ;
     AcDbIdPair idPair2 ;
     for  ( iter2.start ();
      !iter2.done ();
      iter2.next () ) 
     {
      if  ( !iter2.getMap (idPair2) )
       continue  ;
        if  ( !idPair2.isCloned () )
       continue  ;
        AcDbObjectId keyId = idPair2.key();
      AcDbObjectId valueId = idPair2.value();
        // Transform the cloned entity based on the 
      // chosen target point 
        //open the entity for write 
      AcDbEntity *pEnt;
      acdbOpenAcDbEntity(pEnt, 
       valueId, AcDb::kForWrite);
        AcGeMatrix3d dispmat 
       = AcGeMatrix3d::kIdentity;
      dispmat.setToTranslation(
       AcGeVector3d(final_pt[0]-basePt[0], 
       0, 0));
      pEnt->transformBy(dispmat);
      pEnt->close();
     }
    }
   }
   }while (TRUE);
     ads_ssfree(ss);
    return  0;
 }
   class  CMyTest1App : public  AcRxArxApp 
 {
 public :
  CMyTest1App () : AcRxArxApp () 
  {
  }
    virtual  AcRx::AppRetCode On_kInitAppMsg (void  *pkt) 
  {
   AcRx::AppRetCode retCode 
    =AcRxArxApp::On_kInitAppMsg (pkt) ;
   acedDefun(_T("CopyMultiple" ), 1000);
   acedRegFunc(CopyMultipleEntitiesFunc, 1000);
   return  (retCode) ;
  }
    virtual  AcRx::AppRetCode On_kUnloadAppMsg (void  *pkt) 
  {
   AcRx::AppRetCode retCode 
    =AcRxArxApp::On_kUnloadAppMsg (pkt) ;
   acedUndef(_T("CopyMultiple" ),1000);
   return  (retCode) ;
  }
     virtual  void  RegisterServerComponents() 
  {
  }
 };
  Here is a recording showing the copy behavior :

