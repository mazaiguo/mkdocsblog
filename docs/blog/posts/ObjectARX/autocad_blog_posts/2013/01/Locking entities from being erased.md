---
title: "Locking entities from being erased"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Database
description: "Consider this: You create entities in drawings that you may or may not want users to erase. If the user tries to erase an object, you want to check..."
author: Autodesk
---
# Locking entities from being erased

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/locking-entities-from-being-erased.html

## 文章内容

By Gopinath Taget
Consider this: You create entities in drawings that you may or may not want users to erase. If the user tries to erase an object, you want to check and see if it is allowed: if it is allowed,
the object will be erased, if not the object should not be erased. So, what is the recommended way of preventing objects from being erased?
You cannot veto the entities removal, but you can unerase the entities afterwards. The solution to this can be divided into two parts: first detect if the entity has been erased, and undo it. For the detection stage there are two choices:
1) Attach an object reactor (either transient or persistent) to the entities and implementing the erased() notification callback:
virtual void AcDbObject::erased (const AcDbObject* dbObj, Adesk::Boolean
pErasing = Adesk::kTrue);
2) Use a database reactor to check for objects being erased:
virtual void AcDbDatabaseReactor::objectErased (const AcDbDatabase* dwg, const AcDbObject* dbObj, Adesk::Boolean pErased = Adesk::kTrue);
The sample snippets below use the second approach because this is more efficient and easier to maintain. In this callback, the AcDbObjectIds of the entities are cached. These have been decided by checking a list of "locked" entities (stored in the database reactor), which can be maintained by a set of commands to lock and unlock entities. If the object erased is one of the entities in a list, then add it to a list of entities to unerase (see later).
For the second stage (unerasing), the best method for safely erasing the entities without starting a notification loop is to use the editor reactor commandEnded() notification to wait for the current command to complete, and then check the cached list of objects to unerase (and then unerase them, if there are any). You can attempt this from the objectClosed() notification, but this is very dangerous and is not recommended.
An editor reactor is used to do this - also check for lispEnded() if you want to check for (entdel) or ads_entdel(). There is one important issue to note: some AutoCAD commands keep one entity open for write until the command has truly finished, so you cannot open it "for write" via acdbOpenAcDbEntity(). To work around this, the transaction manager's getObject() was used to open up the entities, which were then unerased.
Database reactor header:
// dbreact.h
/////////////////////////////////////////////////////////
  // databasereactor-definitions
//
// ATTENTION: do not modify this code.
//
  /////////////////////////////////////////////////////////
// functions for AcDcDbReactor
void create_AcDcDbReactor();
void erase_AcDcDbReactor();
  // declaration of AcDcDbReactor
class AcDcDbReactor : public AcDbDatabaseReactor {
public:
    virtual void objectErased(const AcDbDatabase* dwg,
        const AcDbObject* dbObj,
        Adesk::Boolean pErased = Adesk::kTrue);
    AcDbObjectIdArray m_lockedObjects;
};
Database reactor implementation:
// dbreact.cpp
/////////////////////////////////////////////////////////
    // includes from ObjectARX Wizard
#include "acdb.h"             // acdb definitions
#include "adslib.h"           // ads defs
#include "aced.h"             // aced stuff
#include "dbmain.h"           // object and entity reactors
#include "Unerase.h"
#include "dbreact.h"
#include "edreact.h"
#include "migrtion.h"
#include "dbapserv.H"
  ///////////////////////////////////////////////////////
// database reactor AcDcDbReactor
  AcDcDbReactor* pAcDcDbReactor = NULL;
extern AcDcEdReactor* pAcDcEdReactor;
  // call this function to create the reactor AcDcDbReactor
void create_AcDcDbReactor()
{
    if ( !pAcDcDbReactor ){
        pAcDcDbReactor = new AcDcDbReactor();
        acdbCurDwg()->addReactor(pAcDcDbReactor);
    }
    pAcDcDbReactor->m_lockedObjects.setLogicalLength( 0 );
}
  // call this function to erase the reactor AcDcDbReactor
void erase_AcDcDbReactor()
{
    if (acdbCurDwg() != NULL) {
        acdbCurDwg()->removeReactor(pAcDcDbReactor);
        delete pAcDcDbReactor;
        pAcDcDbReactor = NULL;
    }
}
  void AcDcDbReactor::objectErased(const AcDbDatabase* dwg,
                                 const AcDbObject* dbObj,
                                 Adesk::Boolean pErased)
{
    if ( pErased ){
        if ( m_lockedObjects.contains( dbObj->objectId() )
           && !pAcDcEdReactor->m_objectsToUnerase.contains(
     dbObj->objectId() )){
            // Locked object erased!
            pAcDcEdReactor->m_objectsToUnerase.append(
    dbObj->objectId() );
        }
    }
}
  Editor reactor header:
  // edreact.h
/////////////////////////////////////////////////////////
  // editor-reactor-definitions
//
// ATTENTION: do not modify this code.
//
  /////////////////////////////////////////////////////////
// functions for AdDcEdReactor
void create_AcDcEdReactor();
void erase_AcDcEdReactor();
  // declaration of AdDcEdReactor
class AcDcEdReactor : public AcEditorReactor {
public:
    virtual void commandEnded(const TCHAR* cmdStr);
    virtual void commandWillStart(const TCHAR* cmdStr);
      AcDbObjectIdArray m_objectsToUnerase;
};
    Editor reactor implementation:
// edreact.cpp
/////////////////////////////////////////////////////////
    // includes from ObjectARX Wizard
#include "acdb.h"             // acdb definitions
#include "adslib.h"           // ads defs
#include "aced.h"             // aced stuff
#include "dbmain.h"           // object and entity reactors
#include "dbidmap.h"          // id mapping
#include "Unerase.h"
#include "edreact.h"
#include "dbreact.h"
#include "actrans.h"
#include "tchar.h"
  ///////////////////////////////////////////////////////
// editor reactor AcDcEdReactor
  AcDcEdReactor* pAcDcEdReactor = NULL;
extern AcDcDbReactor *pAcDcDbReactor;
  // call this function to create the reactor AcDcEdReactor
void create_AcDcEdReactor()
{
    if ( !pAcDcEdReactor ){
        pAcDcEdReactor = new AcDcEdReactor();
        acedEditor->addReactor( pAcDcEdReactor);
    }
}
  // call this function to erase the reactor AcDcEdReactor
void erase_AcDcEdReactor()
{
    acedEditor->removeReactor(pAcDcEdReactor);
    delete pAcDcEdReactor;
    pAcDcEdReactor = NULL;
}
  void AcDcEdReactor::commandWillStart(const TCHAR* cmdStr)
{
    // Clear the cache at the beginning of each command
    m_objectsToUnerase.setLogicalLength( 0 );
}
  void AcDcEdReactor::commandEnded(const TCHAR* cmdStr)
{
    // If object IDs were cached during the last command,
    // unerase the objects identified in the cache
    if ( m_objectsToUnerase.length() > 0 ){
        AcDbObjectId objId;
        AcDbObject *pObj = NULL;
        actrTransactionManager->startTransaction();
        for ( int i = 0; i < m_objectsToUnerase.length(); i++ ){
            // Use the transaction manager to open the objects
            // as one entity is held open for read by AutoCAD
            if ( Acad::eOk != actrTransactionManager->getObject(
    pObj,
    m_objectsToUnerase.at( i ), AcDb::kForWrite,
    Adesk::kTrue )){
                ads_printf( _T("\nCannot open object for write!") );
            }
            else
                pObj->erase( Adesk::kFalse );
        }
        actrTransactionManager->endTransaction();
        ads_printf( _T("\n%d entities unerased."),
   m_objectsToUnerase.length() );
        m_objectsToUnerase.setLogicalLength( 0 );
    }
}
  Utilities and commands header:
// Unerase.h
/////////////////////////////////////////////////////////
    // function declaration of your new AutoCAD functions
void uneraselock ();
void uneraseunlockall ();
void uneraseunlock ();
void uneraseshowlocked ();
  // TODO: add other functions and variables
  // END
  Utilities and commands implementation:
// Unerase.cpp
/////////////////////////////////////////////////////////
    // includes from ObjectARX Wizard
#include "acdb.h"             // acdb definitions
#include "adslib.h"           // ads defs
#include "aced.h"             // aced stuff
#include "dbmain.h"           // object and entity reactors
#include "Unerase.h"          // this project
#include "edreact.h"          // the editor reactor
#include "dbreact.h"          // the database reactor
#include "dbapserv.h"
#include "tchar.h"
  // entry point for this application
extern "C" AcRx::AppRetCode acrxEntryPoint( AcRx::AppMsgCode msg,
 void* );
// message handlers
  // helper functions
static void initApp  (void);
static void unloadApp(void);
static void initDwg  (void);
static void unloadDwg(void);
  extern AcDcDbReactor* pAcDcDbReactor;
extern AcDcEdReactor* pAcDcEdReactor;
  /////////////////////////////////////////////////////////////////////
// acrxEntryPoint(internal)
// This function is the entry point for your application.
/////////////////////////////////////////////////////////////////////
AcRx::AppRetCode acrxEntryPoint(AcRx::AppMsgCode msg, void*appId)
{
    switch (msg) {
    case AcRx::kInitAppMsg:
        acrxDynamicLinker->registerAppMDIAware(appId);
        initApp();
        break;
    case AcRx::kUnloadAppMsg:
        unloadApp();
        break;
    case AcRx::kLoadDwgMsg:
        initDwg();
        break;
    case AcRx::kUnloadDwgMsg:
        unloadDwg();
        break;
    case AcRx::kPreQuitMsg:
        unloadDwg();
        break;
    default:
        break;
    }
    return AcRx::kRetOK;
}
  static void initApp(void)
{
    // register your autocad commands
    acedRegCmds->addCommand(_T("UNERASE"),
  _T("LOCK"), _T("LOCK"), ACRX_CMD_MODAL, uneraselock);
    acedRegCmds->addCommand(_T("UNERASE"),
  _T("UNLOCKALL"), _T("UNLOCKALL"),
  ACRX_CMD_MODAL, uneraseunlockall);
    acedRegCmds->addCommand(_T("UNERASE"), _T("UNLOCK"),
  _T("UNLOCK"), ACRX_CMD_MODAL, uneraseunlock);
    acedRegCmds->addCommand(_T("UNERASE"), _T("SHOWLOCKED"),
  _T("SHOWLOCKED"), ACRX_CMD_MODAL, uneraseshowlocked);
      create_AcDcEdReactor();
} // END initApp()
  static void initDwg(void)
{
    create_AcDcDbReactor();
} // END initDwg()
  static void unloadApp(void)
{
    // unregister your autocad commands
    acedRegCmds->removeGroup(_T("UNERASE"));
      erase_AcDcDbReactor();
    erase_AcDcEdReactor();
}   // END unloadApp()
  static void unloadDwg(void)
{
    erase_AcDcDbReactor();
}   // END unloadDwg()
        // Here are your new AutoCAD functions. Add your code.
//////////////////////////////////////////////////////
  void uneraselock()
{
    // Lock specified entities
    ads_name ss;
      if ( RTNORM == ads_ssget( NULL, NULL, NULL, NULL, ss )){
          long sslen = 0,
             locked = 0,
             relocked = 0;
          ads_sslength( ss, &sslen );
          ads_name ename;
        AcDbObjectId entId;
        for ( long ssidx = 0; ssidx < sslen; ssidx++ ){
            ads_ssname( ss, ssidx, ename );
            acdbGetObjectId( entId, ename );
            if ( pAcDcDbReactor->m_lockedObjects.contains( entId ))
                // Entity already locked!
                relocked++;
            else {
                // Lock entity
                pAcDcDbReactor->m_lockedObjects.append( entId );
                locked++;
            }
        }
        ads_ssfree( ss );
        ads_printf( _T("\nLocked %d entities."), locked );
        if ( relocked )
            ads_printf( _T(" %d entities already locked."),
   relocked );
    }
}
  void uneraseunlockall()
{
    // Clear the locking list
    pAcDcDbReactor->m_lockedObjects.setLogicalLength( 0 );
    ads_printf( _T("\nUnlocked all entities.") );
}
  void uneraseunlock()
{
    // Unlock specified entites
    ads_name ss;
      if ( RTNORM == ads_ssget( NULL, NULL, NULL, NULL, ss )){
          long sslen = 0,
             notlocked = 0,
             unlocked = 0;
          ads_sslength( ss, &sslen );
          ads_name ename;
        AcDbObjectId entId;
        for ( long ssidx = 0; ssidx < sslen; ssidx++ ){
            ads_ssname( ss, ssidx, ename );
            acdbGetObjectId( entId, ename );
            if ( pAcDcDbReactor->m_lockedObjects.contains( entId )){
                // Unlocked entity
                pAcDcDbReactor->m_lockedObjects.remove( entId );
                unlocked++;
            }
            else
                // Entity not locked!
                notlocked++;
        }
        ads_ssfree( ss );
        ads_printf( _T("\nUnlocked %d entities."), unlocked );
        if ( notlocked )
            ads_printf( _T(" %d entities were not locked."),
   notlocked );
    }
}
  void uneraseshowlocked()
{
    // Highlight each entity identified in the "locked" array
    AcDbObjectId objId;
    AcDbEntity *pEnt = NULL;
    for ( int i = 0; i < pAcDcDbReactor->m_lockedObjects.length();
  i++ ){
        objId = pAcDcDbReactor->m_lockedObjects.at( i );
        if ( Acad::eOk != acdbOpenAcDbEntity( pEnt, objId,
   AcDb::kForRead )){
            ads_printf(
   _T("\nCannot open entity for read - removing lock.") );
            pAcDcDbReactor->m_lockedObjects.removeAt( i );
        }
        else {
            pEnt->highlight();
            pEnt->close();
        }
    }
}

## 评论

**内容**: Zafer Gurbuz said...
Is this code MDI safe? My application with similar code crashes after closing the second drawing. Only one pAcDcDbReactor defined for all opened drawings.
Reply
01/13/2016 at 07:48 AM

---
