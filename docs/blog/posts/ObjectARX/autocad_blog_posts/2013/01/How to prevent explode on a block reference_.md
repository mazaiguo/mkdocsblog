---
title: "How to prevent explode on a block reference?"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Unicode
description: "The EXPLODE command works on a Block reference by deepcloning the contents of the referenced block in kDcExplode context, and finally erasing the b..."
author: Autodesk
---
# How to prevent explode on a block reference?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-prevent-explode-on-a-block-reference.html

## 文章内容

By Gopinath Taget
The EXPLODE command works on a Block reference by deepcloning the contents of the referenced block in kDcExplode context, and finally erasing the block reference itself. So, one solution to prevent explode is to exclude the block's contents from deepClone operation and un-erase the block reference after the explode command ends. A similar approach could be found in this blog post. By modifying the code in that blog post, we can disable EXPLODE command for block references (sample attached). The sample code below works as follows:
1. Issue DISABLEEXPLODE command. This will ask you to select block references you want to prevent exploding. The referenced blocks are then iterated, and the IDs of contents of the block are remembered in a list.
2. In the editor reactor's beginDeepClone() notification, the above collected ids are placed in the objectId map. This will trick AutoCAD into thinking they have already been copied, and so will not clone them. These fake ids are removed during beginDeepCloneXlation().
3. At the commandEnded() notification for explode command, we un-erase the block reference.
You can enable exploding with ENABLEEXPLODE command. Here is the relevant code:
Header of the reactor:
/////////////////////////////////////////////
// AcEditorReactor reactors.
  #if !defined(ARX__REDITORREACTOR_H__20020123_132949)
#define ARX__REDITORREACTOR_H__20020123_132949
  #if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
  #include "dbidmap.h"
#include "aced.h"
    class ADCGEditorRctr : public AcEditorReactor
{
public:
   // Constructor / Destructor
ADCGEditorRctr(const bool autoInitAndRelease = true);
 virtual ~ADCGEditorRctr();
   //{{AFX_ARX_METHODS(ADCGEditorRctr)
 virtual void commandEnded(const TCHAR* cmdStr);
 virtual void beginDeepCloneXlation(AcDbIdMapping& x0,
  Acad::ErrorStatus* x1);
 virtual void beginDeepClone(AcDbDatabase* pTo,
  AcDbIdMapping& x0);
 //}}AFX_ARX_METHODS
    // other
  public:
    Adesk::Boolean addObject(const AcDbObjectId& id);
  Adesk::Boolean removeObject(const AcDbObjectId& id);
  Adesk::Boolean addBlRefId(const AcDbObjectId& id);
  Adesk::Boolean removeBlRefId(const AcDbObjectId& id);
  private:
 // Auto initialization and release flag.
 bool m_autoInitAndRelease;
AcDbObjectIdArray m_ids;
AcDbObjectIdArray m_blRefIds;
 bool dcActiveDuringExplode;
};
  #endif // !defined(ARX__REDITORREACTOR_H__20020123_132949)
  Implementation of the reactor:
/////////////////////////////////////////////
// AcEditorReactor reactors.
  #include "StdAfx.h"
#include "rEditorReactor.h"
  ADCGEditorRctr::ADCGEditorRctr(const bool autoInitAndRelease)
{
m_autoInitAndRelease = autoInitAndRelease;
 if (m_autoInitAndRelease)
  if (NULL != acedEditor)
   acedEditor->addReactor(this);
  else
   m_autoInitAndRelease = false;
  dcActiveDuringExplode = false;
}
  ADCGEditorRctr::~ADCGEditorRctr()
{
 if (m_autoInitAndRelease)
  if (NULL != acedEditor)
   acedEditor->removeReactor(this);
}
  //
// Overrides
//
  void ADCGEditorRctr::beginDeepClone(AcDbDatabase* pTo,
AcDbIdMapping& x0)
{
    // Only for Explode Context
  if(  AcDb::kDcExplode != x0.deepCloneContext() )
    return;
    // Mock up a fake clone: place our ids in the map
  for(int i=0; i<m_ids.length(); i++)
    x0.assign(AcDbIdPair(m_ids[i],m_ids[i],
Adesk::kTrue, Adesk::kTrue));
  }
  void ADCGEditorRctr::beginDeepCloneXlation(AcDbIdMapping& x0,
Acad::ErrorStatus* x1)
{
  // Only for Explode Context
 if(AcDb::kDcExplode != x0.deepCloneContext())
    return;
  dcActiveDuringExplode = true;
    // Remove them here
  for(int i=0; i<m_ids.length(); i++)
    x0.del(m_ids[i]);
}
  //
// Custom methods
//
  Adesk::Boolean ADCGEditorRctr::addObject(const AcDbObjectId& id)
{
  int at;
    if(!m_ids.find(id,at))
  {
m_ids.append(id);
    return Adesk::kTrue;
  }
    return Adesk::kFalse;
}
  Adesk::Boolean ADCGEditorRctr::removeObject(const AcDbObjectId& id)
{
  int at;
    if(m_ids.find(id,at))
  {
    m_ids.removeAt(at);
    return Adesk::kTrue;
  }
    return Adesk::kFalse;
}
    Adesk::Boolean ADCGEditorRctr::addBlRefId(const AcDbObjectId& id)
{
  int at;
    if(!m_blRefIds.find(id,at))
  {
    m_blRefIds.append(id);
    return Adesk::kTrue;
  }
    return Adesk::kFalse;
}
  Adesk::Boolean ADCGEditorRctr::removeBlRefId(const AcDbObjectId& id)
{
  int at;
    if(m_blRefIds.find(id,at))
  {
    m_blRefIds.removeAt(at);
    return Adesk::kTrue;
  }
    return Adesk::kFalse;
}
    //---------------------------------------------------------------
void ADCGEditorRctr::commandEnded(const TCHAR* cmdStr)
{
 // Unerase the BlRef after EXPLODE command
 if( _tcscmp(_T("EXPLODE"), cmdStr) == 0 &&
  dcActiveDuringExplode)
{
  for(int i = 0; i < m_blRefIds.length(); i++)
  {
   AcDbEntity *pEnt;
   if(Acad::eOk == acdbOpenAcDbEntity(pEnt, m_blRefIds[i],
    AcDb::kForWrite, true))
   {
    // Unerase blref
    pEnt->erase(false);
    pEnt->close();
   }
  }
}
  dcActiveDuringExplode = false;
}
    Implementation of commands:
  //-------------------------------------------------------------------
//----- acrxEntryPoint.h
//-------------------------------------------------------------------
#include "StdAfx.h"
#include "resource.h"
#include "rEditorReactor.h"
  //-------------------------------------------------------------------
#define szRDS _RXST("asdk")
  //-------------------------------------------------------------------
//----- ObjectARX EntryPoint
    class CDisableExplodeApp : public AcRxArxApp
{
   static ADCGEditorRctr gEditorRctr;
    public:
CDisableExplodeApp () : AcRxArxApp () {}
   virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt) {
  // TODO: Load dependencies here
    // You *must* call On_kInitAppMsg here
  AcRx::AppRetCode retCode =AcRxArxApp::On_kInitAppMsg (pkt) ;
    // TODO: Add your initialization code here
    return (retCode) ;
}
   virtual AcRx::AppRetCode On_kUnloadAppMsg (void *pkt) {
  // TODO: Add your code here
    // You *must* call On_kUnloadAppMsg here
  AcRx::AppRetCode retCode =AcRxArxApp::On_kUnloadAppMsg (pkt) ;
    // TODO: Unload dependencies here
    return (retCode) ;
}
   virtual void RegisterServerComponents () {
}
  public:
   // - asdkDisableExplode._DISABLECOPY command (do not rename)
 static void asdkDisableExplode_DISABLECOPY(void)
{
   ads_name ss;
     if(acedSSGet(NULL,NULL,NULL,NULL,ss)==RTNORM) {
  ads_name ent;
  AcDbObjectId id;
  long length;
  if(acedSSLength(ss, &length)==RTNORM) {
    for(int i=0; i<length; i++) {
   if(ads_ssname(ss, i, ent)==RTNORM) {
     if(acdbGetObjectId(id,ent) == Acad::eOk)
    gEditorRctr.addObject(id);
   }
    }
  }
   }
     acedSSFree(ss);
}
    public:
   // - asdkDisableExplode._ENABLECOPY command (do not rename)
 static void asdkDisableExplode_ENABLECOPY(void)
{
   ads_name ss;
     if(acedSSGet(NULL,NULL,NULL,NULL,ss)==RTNORM) {
  ads_name ent;
  AcDbObjectId id;
  long length;
  if(acedSSLength(ss, &length)==RTNORM) {
    for(int i=0; i<length; i++) {
   if(ads_ssname(ss, i, ent)==RTNORM) {
     if(acdbGetObjectId(id,ent) == Acad::eOk)
    gEditorRctr.removeObject(id);
   }
    }
  }
   }
     acedSSFree(ss);
}
    public:
   // - asdkDisableExplode._DISABLEEXPLODE command (do not rename)
 static void asdkDisableExplode_DISABLEEXPLODE(void)
{
  ads_name ss;
    //Select block references
  if(acedSSGet(NULL,NULL,NULL,NULL,ss)==RTNORM)
  {
   ads_name ent;
   AcDbObjectId id;
   long length;
   if(acedSSLength(ss, &length)==RTNORM) {
     for(int i=0; i<length; i++) {
    if(ads_ssname(ss, i, ent)==RTNORM) {
      if(acdbGetObjectId(id,ent) == Acad::eOk)
      {
       AcDbObject *pObj;
       if(Acad::eOk == acdbOpenObject(pObj, id,
        AcDb::kForRead))
       {
        AcDbBlockReference *pBlRef;
        // Check if the object is a block ref
        if(pBlRef =
         AcDbBlockReference::cast(pObj))
        {
        // Add BlRef to editor reactor
        gEditorRctr.addBlRefId(pBlRef->objectId());
          AcDbObjectId blockId =
         pBlRef->blockTableRecord();
        //Open the blockId for read
        AcDbBlockTableRecordPointer pBTR(blockId,
         AcDb::kForRead);
        AcDbBlockTableRecordIterator *pIter;
        if(Acad::eOk == pBTR->newIterator(pIter))
        {
        for(; !pIter->done(); pIter->step())
        {
         AcDbObjectId entId;
         pIter->getEntityId(entId);
         gEditorRctr.addObject(entId);
        }
        delete pIter;
        }
       pBTR->close();
        }
        pObj->close();
       }
      }
    }
     }
   }
  }
     acedSSFree(ss);
  }
      public:
   // - asdkDisableExplode._ENABLEEXPLODE command (do not rename)
 static void asdkDisableExplode_ENABLEEXPLODE(void)
{
  ads_name ss;
    //Select block references
  if(acedSSGet(NULL,NULL,NULL,NULL,ss)==RTNORM)
  {
   ads_name ent;
   AcDbObjectId id;
   long length;
   if(acedSSLength(ss, &length)==RTNORM) {
     for(int i=0; i<length; i++) {
    if(ads_ssname(ss, i, ent)==RTNORM) {
      if(acdbGetObjectId(id,ent) == Acad::eOk)
      {
       AcDbObject *pObj;
       if(Acad::eOk == acdbOpenObject(pObj, id,
        AcDb::kForRead))
       {
        AcDbBlockReference *pBlRef;
        // Check if the object is a block ref
        if(pBlRef = AcDbBlockReference::cast(pObj))
        {
        // Remove BlRef from editor reactor
        gEditorRctr.removeBlRefId(
         pBlRef->objectId());
          AcDbObjectId blockId =
         pBlRef->blockTableRecord();
        //Open the blockId for read
        AcDbBlockTableRecordPointer pBTR(
         blockId, AcDb::kForRead);
        AcDbBlockTableRecordIterator *pIter;
        if(Acad::eOk == pBTR->newIterator(pIter))
        {
        for(; !pIter->done(); pIter->step())
        {
         AcDbObjectId entId;
         pIter->getEntityId(entId);
         gEditorRctr.removeObject(entId);
          }
        delete pIter;
        }
       pBTR->close();
        }
        pObj->close();
       }
      }
    }
     }
   }
  }
     acedSSFree(ss);
}
    } ;
    ADCGEditorRctr CDisableExplodeApp::gEditorRctr;
    //-----------------------------------------------------------------------------
IMPLEMENT_ARX_ENTRYPOINT(CDisableExplodeApp)
  ACED_ARXCOMMAND_ENTRY_AUTO(CDisableExplodeApp, asdkDisableExplode,
_DISABLECOPY, DISABLECOPY, ACRX_CMD_TRANSPARENT, NULL)
ACED_ARXCOMMAND_ENTRY_AUTO(CDisableExplodeApp, asdkDisableExplode,
_ENABLECOPY, ENABLECOPY, ACRX_CMD_TRANSPARENT, NULL)
ACED_ARXCOMMAND_ENTRY_AUTO(CDisableExplodeApp, asdkDisableExplode,
_DISABLEEXPLODE, DISABLEEXPLODE, ACRX_CMD_TRANSPARENT, NULL)
ACED_ARXCOMMAND_ENTRY_AUTO(CDisableExplodeApp, asdkDisableExplode,
_ENABLEEXPLODE, ENABLEEXPLODE, ACRX_CMD_TRANSPARENT, NULL)

## 评论

**内容**: Craig said...
Hi Gopinath,
Is this possible with the .Net API?
Reply
03/03/2014 at 08:17 AM

---
