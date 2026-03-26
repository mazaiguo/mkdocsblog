---
title: "Converting custom entity to std Acad entity and vice-versa upon open/save"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - DWG
description: "Lets say, you have a custom entity derived from AcDbEntity. When your application is not loaded into AutoCAD, AutoCAD turns that entity into a 'pro..."
author: Autodesk
---
# Converting custom entity to std Acad entity and vice-versa upon open/save

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/converting-custom-entity-to-std-acad-entity-and-vice-versa-upon-opensave.html

## 文章内容

By Gopinath Taget
Lets say, you have a custom entity derived from AcDbEntity. When your application is not loaded into AutoCAD, AutoCAD turns that entity into a 'proxy', which doesn't allow your customers to share their drawings with others who are not using your application. So, is there a way to automatically convert your custom entities into standard AutoCAD entities when the drawing is saved and when the drawing is loaded?
To do this, you need to plant an AcEditorReactor to trap any disk file operation to convert your custom entities into standard AutoCAD entities or convert them from standard AutoCAD entities. The custom AcEditorReactor object must implement the beginSave() notification to convert the custom entities into standard AutoCAD entities, and the dwgFileOpened()/saveComplete() to reverse that operation.
To reverse that operation, store some information that your application can use later to retrieve the standard AutoCAD entity (or group of entity). XData was used in the code snippets provided below and is one approach; you can use any other method that allows information such as Extended Dictionary, Named Object Dictionary or AcDbXRecord to be stored.
In the AcEditorReactor notification handlers, your application will iterate through all the drawing AcDbBlockTableRecord objects and their content to find any instance of a custom entity or a converted custom entity to convert them into their new appropriate state.
In addition to this, also convert the entity instances when your application loads and unloads. To achieve that goal, call the saveBegin() and saveComplete() AcEditorReactor method during the kInitAppMsg and kUnloadAppMsg statement of the acrxEntryPoint() function.
The last important thing to note is that because this improve the performance of these operations and because they are automatically handled via our editor reactor, Undo recording can be turned off.
Here is the code of a simple custom entity:
Header:
#ifndef _MKRCIRCLE_H_
#define _MKRCIRCLE_H_
  ///////////////////////////////////////////////////////////////////////////////
// Custom entity: MkrCircle
class MkrCircle : public AcDbEntity
{
public:
    ACRX_DECLARE_MEMBERS( MkrCircle );
                        MkrCircle    ();
    virtual           ~MkrCircle   ();
      AcGePoint3d       center       () const;
    double            radius       () const;
    const TCHAR*       name         () const;
      void              setCenter    (const AcGePoint3d&);
    void              setRadius    (double);
    void              setName      (const TCHAR*);
  Adesk::Boolean    subWorldDraw    (AcGiWorldDraw*);
      Acad::ErrorStatus dwgInFields  (AcDbDwgFiler*);
    Acad::ErrorStatus dwgOutFields (AcDbDwgFiler*) const;
    Acad::ErrorStatus subTransformBy  (const AcGeMatrix3d&);
  private:
    AcGePoint3d m_center;
    double      m_radius;
    TCHAR*       m_name;
};
  #endif // _MKRCIRCLE_H_
  Implementation:
////////////////////////////////////////////
// Custom entity: MkrCircle
#include "StdAfx.h"
#include "StdArx.h"
#include <acgi.h>
#include "mkrcircle.h"
  ACRX_DXF_DEFINE_MEMBERS( MkrCircle, AcDbEntity, AcDb::kDHL_CURRENT,
AcDb::kMReleaseCurrent, 0, MKRCIRCLE, Mkr);
//MAKE_ACDBOPENOBJECT_FUNCTION( MkrCircle );
    MkrCircle::MkrCircle() : m_center( 0, 0, 0 ),
m_radius( 0 ), m_name( NULL )
{  }
  MkrCircle::~MkrCircle()
{
    if (NULL != m_name)
        free( m_name );
}
  AcGePoint3d
MkrCircle::center() const
{
    assertReadEnabled();
    return m_center;
}
  void
MkrCircle::setCenter( const AcGePoint3d& pt )
{
    assertWriteEnabled();
    m_center = pt;
}
  double
MkrCircle::radius() const
{
    assertReadEnabled();
    return m_radius;
}
  void
MkrCircle::setRadius( double rad )
{
    assertWriteEnabled();
    m_radius = rad;
}
  const TCHAR*
MkrCircle::name() const
{
    assertReadEnabled();
    return m_name;
}
  void
MkrCircle::setName( const TCHAR* pName )
{
    assertWriteEnabled();
    if (NULL != m_name)
        free( m_name );
    m_name = _tcsdup( pName );
}
  Adesk::Boolean
MkrCircle::subWorldDraw( AcGiWorldDraw* mode )
{
assertReadEnabled();
    mode->geometry().circle ( m_center, m_radius,
  AcGeVector3d( 0.0, 0.0, 1.0 ) );
    mode->geometry().text( m_center,
                           AcGeVector3d( 0.0, 0.0, 1.0 ),
                           AcGeVector3d( 1.0, 0.0, 0.0 ),
                           0.7,
                           0.7,
                           0.0,
                           m_name );
    return Adesk::kTrue;
}
  Acad::ErrorStatus
MkrCircle::dwgInFields( AcDbDwgFiler* filer )
{
    assertWriteEnabled();
      Acad::ErrorStatus es;
    if (Acad::eOk != (es = AcDbEntity::dwgInFields( filer )))
        return es;
      if (NULL != m_name)
        free( m_name );
      filer->readItem( &m_center );
    filer->readItem( &m_radius );
    filer->readItem( &m_name );
      return filer->filerStatus();
}
  Acad::ErrorStatus
MkrCircle::dwgOutFields( AcDbDwgFiler* filer ) const
{
    assertReadEnabled();
      Acad::ErrorStatus es;
    if (Acad::eOk != (es = AcDbEntity::dwgOutFields( filer )))
        return es;
      filer->writeItem( m_center );
    filer->writeItem( m_radius );
    filer->writeItem( m_name );
      return filer->filerStatus();
}
  Acad::ErrorStatus
MkrCircle::subTransformBy( const AcGeMatrix3d& xform )
{
    assertWriteEnabled();
    m_center.transformBy( xform );
      AcGeScale3d s;
    s.extractScale( xform );
    m_radius *= s[0];
    return Acad::eOk;
}
  Here is the code of the reactor:
Header:
/////////////////////////////////////////////
// AcEditorReactor reactors.
  #if !defined(ARX__EDREACT_H__20011221_025043)
#define ARX__EDREACT_H__20011221_025043
  #if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
  #include "dbidmap.h"
#include "aced.h"
#include "mkrfiler.h"
class Asdkedreact : public AcEditorReactor
{
public:
   // Constructor / Destructor
Asdkedreact(const bool autoInitAndRelease = true);
 virtual ~Asdkedreact();
   //{{AFX_ARX_METHODS(Asdkedreact)
 virtual void saveComplete(AcDbDatabase* x0,
                           const TCHAR* pActualName);
 virtual void dwgFileOpened(AcDbDatabase* x0,
                            TCHAR* fileName);
 virtual void beginSave(AcDbDatabase* x0,
                        const TCHAR* pIntendedName);
 //}}AFX_ARX_METHODS
  private:
 // Auto initialization and release flag.
 bool m_autoInitAndRelease;
};
  typedef void (*ApplyFunc)(AcDbEntity*&);
extern Asdkedreact *pEditorReactor ;
  #endif // !defined(ARX__EDREACT_H__20011221_025043)
  Implementation:
/////////////////////////////////////////////
// AcEditorReactor reactors.
#include "StdAfx.h"
#include "StdArx.h"
#include <dbents.h>
#include "mkrcircle.h"
  Asdkedreact *pEditorReactor =NULL ;
  void MkrCircleToCircle( AcDbEntity*& pEnt )
{
    MkrCircle* pMkr = MkrCircle::cast( pEnt );
    // no reason why this should fail, but anyway ...
    //
    if (NULL == pMkr)
        return;
      MkrDwgFiler filer;
    pMkr->dwgOutFields( &filer );
      AcDbCircle* pCir = new AcDbCircle;
    if (NULL == pCir)
        return;
      pCir->setPropertiesFrom( pMkr );
    pCir->setCenter( pMkr->center() );
    pCir->setRadius( pMkr->radius() );
    if (Acad::eOk == pMkr->upgradeOpen() &&
  Acad::eObjectToBeDeleted == pMkr->handOverTo( pCir ))
{
  pCir->setXData( filer.getResbuf() );
        delete pMkr;
        pEnt = pCir;
    }
    else
        delete pCir;
}
  void CircleToMkrCircle( AcDbEntity*& pEnt )
{
    AcDbCircle* pCir = AcDbCircle::cast( pEnt );
    // no reason why this should fail, but anyway ...
    //
    if (NULL == pCir)
        return;
      resbuf* pRb = pCir->xData( _T("MKRDWGFILER") );
    if (NULL == pRb)
        return;
      MkrCircle* pMkr = new MkrCircle;
    if (NULL == pMkr)
        return;
      MkrDwgFiler filer( pRb );
    pMkr->dwgInFields( &filer );
    pMkr->setPropertiesFrom( pCir );
    pMkr->setCenter( pCir->center() );
    pMkr->setRadius( pCir->radius() );
      if (   Acad::eOk == pCir->upgradeOpen()
        && Acad::eObjectToBeDeleted == pCir->handOverTo( pMkr ) )
    {
        delete pCir;
        pEnt = pMkr;
          // handOverTo copies xData as well,
        // so we need to delete the xdata bag from
        // the newly created circle.
        //
        resbuf* pRbClear = acutNewRb( AcDb::kDxfRegAppName );
        pRbClear->resval.rstring = _tcsdup( _T("MKRDWGFILER") );
        pEnt->setXData( pRbClear );
        acutRelRb( pRbClear );
    }
    else
        delete pMkr;
}
    void forEach( AcDbDatabase* pDwg, AcRxClass* pClass,
ApplyFunc pFunc )
{
    AcDbBlockTable* pBT;
    if (Acad::eOk != pDwg->getBlockTable( pBT, AcDb::kForRead ))
        return;
    AcDbBlockTableIterator *pBTi;
    if (Acad::eOk != pBT->newIterator( pBTi )) {
        pBT->close();
        return;
    }
      for ( ; !pBTi->done(); pBTi->step()) {
        AcDbBlockTableRecord* pBTR;
        if (Acad::eOk != pBTi->getRecord( pBTR, AcDb::kForRead ))
            continue;
          AcDbBlockTableRecordIterator* pBTRi;
        if (Acad::eOk != pBTR->newIterator( pBTRi )) {
            pBTR->close();
            continue;
        }
          for ( ; !pBTRi->done(); pBTRi->step()) {
            AcDbEntity* pEnt;
            if (Acad::eOk != pBTRi->getEntity( pEnt,
    AcDb::kForRead ))
                continue;
            if (pEnt->isKindOf( pClass ))
                (*pFunc)( pEnt );
            pEnt->close();
        }
        delete pBTRi;
        pBTR->close();
    }
    delete pBTi;
    pBT->close();
}
    Asdkedreact::Asdkedreact(const bool autoInitAndRelease)
{
m_autoInitAndRelease = autoInitAndRelease;
 if (m_autoInitAndRelease)
  if (NULL != acedEditor)
   acedEditor->addReactor(this);
  else
   m_autoInitAndRelease = false;
}
  Asdkedreact::~Asdkedreact()
{
 if (m_autoInitAndRelease)
  if (NULL != acedEditor)
   acedEditor->removeReactor(this);
}
  void Asdkedreact::beginSave(AcDbDatabase* pDwg,
                            const TCHAR* pIntendedName)
{
   // TODO: implement this function.
    acutPrintf( _T("[Converting to Circle ...]") );
    acdbHostApplicationServices()->
  workingDatabase()->disableUndoRecording( Adesk::kTrue );
    acdbRegApp( _T("MKRDWGFILER") );
    forEach( pDwg, MkrCircle::desc(), MkrCircleToCircle );
    acdbHostApplicationServices()->
  workingDatabase()->disableUndoRecording( Adesk::kFalse );
    acutPrintf( _T("[done.]\n") );
    acedRedraw( NULL, 0 );
}
  void Asdkedreact::dwgFileOpened(AcDbDatabase* pDwg,
                                TCHAR* fileName)
{
 // TODO: implement this function.
    saveComplete( pDwg, fileName );
}
  void Asdkedreact::saveComplete(AcDbDatabase* pDwg,
                               const TCHAR* pActualName)
{
 // TODO: implement this function.
    acutPrintf( _T("[Converting to MkrCircle ...]") );
    acdbHostApplicationServices()->
  workingDatabase()->disableUndoRecording( Adesk::kTrue );
    forEach( pDwg, AcDbCircle::desc(), CircleToMkrCircle );
    acdbHostApplicationServices()->
  workingDatabase()->disableUndoRecording( Adesk::kFalse );
    acutPrintf( _T("[done.]\n") );
    acedRedraw( NULL, 0 );
}
    Here is the code for the filer used to store data in XData:
Header:
#ifndef _MKRDWGFILER_H_
#define _MKRDWGFILER_H_
/////////////////////////////////////////////////////////////////
// Custom DWG Filer class
class MkrDwgFiler: public AcDbDwgFiler
{
public:
    ACRX_DECLARE_MEMBERS( MkrDwgFiler );
                          MkrDwgFiler ();
                        MkrDwgFiler (resbuf*);
    virtual             ~MkrDwgFiler ();
      const resbuf*       getResbuf () const;
      Acad::ErrorStatus   filerStatus () const;
    AcDb::FilerType     filerType () const;
    void                setFilerStatus (Acad::ErrorStatus) ;
    void                resetFilerStatus ();
      //  readXxx() and writeXxx() functions
      Acad::ErrorStatus readHardOwnershipId (AcDbHardOwnershipId*);
    Acad::ErrorStatus writeHardOwnershipId (const AcDbHardOwnershipId&);
      Acad::ErrorStatus readSoftOwnershipId (AcDbSoftOwnershipId*);
    Acad::ErrorStatus writeSoftOwnershipId (const AcDbSoftOwnershipId&);
      Acad::ErrorStatus readHardPointerId (AcDbHardPointerId*);
    Acad::ErrorStatus writeHardPointerId (const AcDbHardPointerId&);
      Acad::ErrorStatus readSoftPointerId (AcDbSoftPointerId*);
    Acad::ErrorStatus writeSoftPointerId (const AcDbSoftPointerId&);
      Acad::ErrorStatus readChar (TCHAR*);
    Acad::ErrorStatus writeChar (TCHAR);
  Acad::ErrorStatus readBChunk (ads_binary *);
    Acad::ErrorStatus writeBChunk (const ads_binary&);
      Acad::ErrorStatus readAcDbHandle (AcDbHandle*);
    Acad::ErrorStatus writeAcDbHandle (const AcDbHandle&);
      Acad::ErrorStatus readInt32 (Adesk::Int32*);
    Acad::ErrorStatus writeInt32 (Adesk::Int32);
      Acad::ErrorStatus readInt16 (Adesk::Int16*);
    Acad::ErrorStatus writeInt16 (Adesk::Int16);
      Acad::ErrorStatus readUInt32 (Adesk::UInt32*);
    Acad::ErrorStatus writeUInt32 (Adesk::UInt32);
      Acad::ErrorStatus readUInt16 (Adesk::UInt16*);
    Acad::ErrorStatus writeUInt16 (Adesk::UInt16);
      Acad::ErrorStatus readUInt8 (Adesk::UInt8*);
    Acad::ErrorStatus writeUInt8 (Adesk::UInt8);
      Acad::ErrorStatus readBoolean (Adesk::Boolean*);
    Acad::ErrorStatus writeBoolean (Adesk::Boolean);
  Acad::ErrorStatus readBool(bool*);
    Acad::ErrorStatus writeBool(bool);
      Acad::ErrorStatus readDouble (double*);
    Acad::ErrorStatus writeDouble (double);
      Acad::ErrorStatus readPoint2d (AcGePoint2d*);
    Acad::ErrorStatus writePoint2d (const AcGePoint2d&);
      Acad::ErrorStatus readPoint3d (AcGePoint3d*);
    Acad::ErrorStatus writePoint3d (const AcGePoint3d&);
      Acad::ErrorStatus readVector2d (AcGeVector2d*);
    Acad::ErrorStatus writeVector2d (const AcGeVector2d&);
      Acad::ErrorStatus readVector3d (AcGeVector3d*);
    Acad::ErrorStatus writeVector3d (const AcGeVector3d&);
      Acad::ErrorStatus readScale3d (AcGeScale3d*);
    Acad::ErrorStatus writeScale3d (const AcGeScale3d&);
      Acad::ErrorStatus readBytes (void *, Adesk::UIntPtr);
    Acad::ErrorStatus writeBytes (const void *, Adesk::UIntPtr);
      //Acad::ErrorStatus seek (long offset, int method);
Acad::ErrorStatus seek (Adesk::Int64 offset, int method);
    //long              tell () const;
Adesk::Int64 tell () const;
  Acad::ErrorStatus readInt64(Adesk::Int64 *);
    Acad::ErrorStatus writeInt64(Adesk::Int64);
Acad::ErrorStatus readUInt64(Adesk::UInt64 *);
    Acad::ErrorStatus writeUInt64(Adesk::UInt64);
  private:
    resbuf             *m_rb,
                      **m_ppwalk;
    Acad::ErrorStatus   m_status;
public:
 // ------------------------------------------------------
 virtual Acad::ErrorStatus readInt8(Adesk::Int8 * param2);
 // ------------------------------------------------------
 virtual Acad::ErrorStatus writeInt8(Adesk::Int8 param2);
 virtual Acad::ErrorStatus readString(AcString &);
 virtual Acad::ErrorStatus writeString(const AcString &);
 virtual Acad::ErrorStatus readString(ACHAR **);
 virtual Acad::ErrorStatus writeString(const ACHAR *);
} ;
  #endif // _MKRDWGFILER_H_
  Implementation:
////////////////////////////////////////////
// Custom DWG Filer class
#include "StdAfx.h"
#include "StdArx.h"
#include "mkrfiler.h"
  ACRX_CONS_DEFINE_MEMBERS( MkrDwgFiler, AcDbDwgFiler, 0 ) ;
  MkrDwgFiler::MkrDwgFiler() : m_rb( NULL ), m_ppwalk( &m_rb ),
    m_status( Acad::eOk )
{
    *m_ppwalk = acutNewRb( AcDb::kDxfRegAppName );
    (*m_ppwalk)->resval.rstring = _tcsdup( _T("MKRDWGFILER") );
    m_ppwalk = &(*m_ppwalk)->rbnext;
}
  MkrDwgFiler::MkrDwgFiler( resbuf* pRb ) : m_rb( pRb ),
    m_ppwalk( &m_rb ), m_status( Acad::eOk )
{
    // skip kDxfRegAppName record
    m_ppwalk = &(*m_ppwalk)->rbnext;
}
  MkrDwgFiler::~MkrDwgFiler()
{
    if (NULL != m_rb)
        acutRelRb( m_rb );
}
  const resbuf*
MkrDwgFiler::getResbuf() const
{
    return m_rb;
}
  Acad::ErrorStatus
MkrDwgFiler::filerStatus() const
{
    return m_status;
}
  AcDb::FilerType
MkrDwgFiler::filerType() const
{
    return AcDb::kCopyFiler;
}
  void
MkrDwgFiler::setFilerStatus( Acad::ErrorStatus es )
{
    m_status = es;
}
  void
MkrDwgFiler::resetFilerStatus()
{
    m_status = Acad::eOk;
}
  //  readXxx() and writeXxx() functions
  Acad::ErrorStatus
MkrDwgFiler::readHardOwnershipId( AcDbHardOwnershipId* id )
{
    return readSoftPointerId( (AcDbSoftPointerId*)id );
}
  Acad::ErrorStatus
MkrDwgFiler::writeHardOwnershipId( const AcDbHardOwnershipId& id )
{
    return writeSoftPointerId( id );
}
  Acad::ErrorStatus
MkrDwgFiler::readSoftOwnershipId( AcDbSoftOwnershipId* id )
{
    return readSoftPointerId( (AcDbSoftPointerId*)id );
}
  Acad::ErrorStatus
MkrDwgFiler::writeSoftOwnershipId( const AcDbSoftOwnershipId& id )
{
    return writeSoftPointerId( id );
}
  Acad::ErrorStatus
MkrDwgFiler::readHardPointerId( AcDbHardPointerId* id )
{
    return readSoftPointerId( (AcDbSoftPointerId*)id );
}
  Acad::ErrorStatus
MkrDwgFiler::writeHardPointerId( const AcDbHardPointerId& id )
{
    return writeSoftPointerId( id );
}
  Acad::ErrorStatus
MkrDwgFiler::readSoftPointerId( AcDbSoftPointerId* id )
{
AcDbDatabase* pDb = acdbHostApplicationServices()->
  workingDatabase();
    AcDbHandle handle;
    Acad::ErrorStatus es = readAcDbHandle( &handle );
      if (Acad::eOk != es)
        return es;
      if (Acad::eOk != pDb->getAcDbObjectId( *id,
  Adesk::kFalse, handle ))
    {
        *id = 0;
    }
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeSoftPointerId( const AcDbSoftPointerId& id )
{
    AcDbObject* pObj;
    AcDbHandle handle;
      if (Acad::eOk == acdbOpenObject( pObj, id, AcDb::kForRead ))
    {
        pObj->getAcDbHandle( handle );
        pObj->close();
    }
    else
        handle = (Adesk::UInt32)0;
    return writeAcDbHandle( handle );
}
  Acad::ErrorStatus
MkrDwgFiler::readChar( TCHAR* c )
{
    TCHAR *pTmp;
    Acad::ErrorStatus es = readString( &pTmp );
    if (Acad::eOk != es)
        return es;
      *c = *pTmp;
    free( pTmp );
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeChar( TCHAR c )
{
    // Convert it to a string in order to
    // allow code page translations.
    //
    TCHAR tmp[2];
    tmp[0] = c;
    tmp[1] = _T('\0');
    return writeString( tmp );
}
    Acad::ErrorStatus
MkrDwgFiler::readBChunk( ads_binary *buf )
{
    if (AcDb::kDxfXdBinaryChunk != (*m_ppwalk)->restype)
    {
        acedAlert( _T("Sequence Error in readBChunk !") );
        return Acad::eInvalidResBuf;
    }
      buf->clen = (*m_ppwalk)->resval.rbinary.clen;
    buf->buf = (char*)malloc( buf->clen );
    memcpy( buf->buf, (*m_ppwalk)->resval.rbinary.buf, buf->clen );
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeBChunk( const ads_binary& buf )
{
    *m_ppwalk = acutNewRb( AcDb::kDxfXdBinaryChunk );
    (*m_ppwalk)->resval.rbinary.clen = buf.clen;
    (*m_ppwalk)->resval.rbinary.buf = (char*)malloc( buf.clen );
    memcpy( (*m_ppwalk)->resval.rbinary.buf, buf.buf, buf.clen );
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::readAcDbHandle( AcDbHandle* handle )
{
    if (AcDb::kDxfXdHandle != (*m_ppwalk)->restype)
    {
        acedAlert( _T("Sequence Error in readAcDbHandle !") );
        return Acad::eInvalidResBuf;
    }
      *handle = (*m_ppwalk)->resval.rstring;
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeAcDbHandle( const AcDbHandle& handle )
{
      *m_ppwalk = acutNewRb( AcDb::kDxfXdHandle );
    (*m_ppwalk)->resval.rstring =
  (TCHAR*)malloc( 17*sizeof(TCHAR) );
    handle.getIntoAsciiBuffer( (*m_ppwalk)->resval.rstring );
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus MkrDwgFiler::readInt64(Adesk::Int64 *)
{
 return Acad::ErrorStatus();
}
Acad::ErrorStatus MkrDwgFiler::writeInt64(Adesk::Int64)
{
 return Acad::ErrorStatus();
}
Acad::ErrorStatus MkrDwgFiler::readUInt64(Adesk::UInt64 *)
{
 return Acad::ErrorStatus();
}
Acad::ErrorStatus MkrDwgFiler::writeUInt64(Adesk::UInt64)
{
 return Acad::ErrorStatus();
}
  Acad::ErrorStatus
MkrDwgFiler::readInt32( Adesk::Int32* i )
{
    return readUInt32( (Adesk::UInt32*)i );
}
  Acad::ErrorStatus
MkrDwgFiler::writeInt32( Adesk::Int32 i )
{
    return writeUInt32( i );
}
  Acad::ErrorStatus
MkrDwgFiler::readInt16( Adesk::Int16* i )
{
    return readUInt16( (Adesk::UInt16*)i );
}
  Acad::ErrorStatus
MkrDwgFiler::writeInt16( Adesk::Int16 i )
{
    return writeUInt16( i );
}
  Acad::ErrorStatus
MkrDwgFiler::readUInt32( Adesk::UInt32* i )
{
AcDbDatabase* pDb = acdbHostApplicationServices()->
  workingDatabase();
    AcDbObjectId id;
    AcDbHandle handle;
    Acad::ErrorStatus es;
      switch ((*m_ppwalk)->restype) {
      case AcDb::kDxfXdInteger32:
        *i = (*m_ppwalk)->resval.rlong;
        m_ppwalk = &(*m_ppwalk)->rbnext;
        es = Acad::eOk;
        break;
      case AcDb::kDxfXdHandle:
        // Surprised ?
        // ACAD sometimes writes NULL-ObjectId's as longs.
        //
        if (Acad::eOk != (es = readAcDbHandle( &handle )))
            return es;
          if (Acad::eOk == pDb->getAcDbObjectId( id,
   Adesk::kFalse, handle ))
        {
            *i = id.asOldId();
        }
        else
            *i = 0;
        es = Acad::eOk;
        break;
      default:
        acedAlert( _T("Sequence Error in readUInt32 !") );
        es = Acad::eInvalidResBuf;
        break;
    }
      return es;
}
  Acad::ErrorStatus
MkrDwgFiler::writeUInt32( Adesk::UInt32 i )
{
    *m_ppwalk = acutNewRb( AcDb::kDxfXdInteger32 );
    (*m_ppwalk)->resval.rlong = i;
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::readUInt16( Adesk::UInt16* i )
{
    if (AcDb::kDxfXdInteger16 != (*m_ppwalk)->restype)
    {
        acedAlert( _T("Sequence Error in readUInt16 !") );
        return Acad::eInvalidResBuf;
    }
      *i = (*m_ppwalk)->resval.rint;
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeUInt16( Adesk::UInt16 i )
{
    *m_ppwalk = acutNewRb( AcDb::kDxfXdInteger16 );
    (*m_ppwalk)->resval.rint = i;
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::readUInt8( Adesk::UInt8* i )
{
    Adesk::UInt16 i16;
    Acad::ErrorStatus es = readUInt16( &i16 );
    if (Acad::eOk != es)
        return es;
      *i = (Adesk::UInt8)i16;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeUInt8( Adesk::UInt8 i )
{
    Adesk::UInt16 i16 = i;
    return writeUInt16( i16 );
}
  Acad::ErrorStatus
MkrDwgFiler::readBoolean( Adesk::Boolean* b )
{
    Adesk::UInt16 i;
    Acad::ErrorStatus es = readUInt16( &i );
    if (Acad::eOk != es)
        return es;
      *b = i;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeBoolean( Adesk::Boolean b )
{
    Adesk::UInt16 i = b;
    return writeUInt16( i );
}
  Acad::ErrorStatus
MkrDwgFiler::readBool(bool* b)
{
    return readBoolean((Adesk::Boolean*)b);
}
  Acad::ErrorStatus
MkrDwgFiler::writeBool(bool b)
{
    return writeBoolean(b);
}
  Acad::ErrorStatus
MkrDwgFiler::readDouble( double* d )
{
    if (AcDb::kDxfXdReal != (*m_ppwalk)->restype)
    {
        acedAlert( _T("Sequence Error in readDouble !") );
        return Acad::eInvalidResBuf;
    }
      *d = (*m_ppwalk)->resval.rreal;
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeDouble( double d )
{
    *m_ppwalk = acutNewRb( AcDb::kDxfXdReal );
    (*m_ppwalk)->resval.rreal = d;
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::readPoint2d( AcGePoint2d* p )
{
    AcGePoint3d p3d;
    Acad::ErrorStatus es = readPoint3d( &p3d );
    if (Acad::eOk != es)
        return es;
    (*p)[0] = p3d[0];
    (*p)[1] = p3d[1];
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writePoint2d( const AcGePoint2d& p )
{
    AcGePoint3d p3d( p[0], p[1], 0.0 );
    return writePoint3d( p3d );
}
  Acad::ErrorStatus
MkrDwgFiler::readPoint3d( AcGePoint3d* p )
{
    if (AcDb::kDxfXdXCoord != (*m_ppwalk)->restype)
    {
        acedAlert( _T("Sequence Error in readPoint3d !") );
        return Acad::eInvalidResBuf;
    }
      (*p)[0] = (*m_ppwalk)->resval.rpoint[0];
    (*p)[1] = (*m_ppwalk)->resval.rpoint[1];
    (*p)[2] = (*m_ppwalk)->resval.rpoint[2];
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writePoint3d( const AcGePoint3d& p )
{
    *m_ppwalk = acutNewRb( AcDb::kDxfXdXCoord );
    (*m_ppwalk)->resval.rpoint[0] = p[0];
    (*m_ppwalk)->resval.rpoint[1] = p[1];
    (*m_ppwalk)->resval.rpoint[2] = p[2];
    m_ppwalk = &(*m_ppwalk)->rbnext;
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::readVector2d( AcGeVector2d* vec )
{
    return readPoint2d( (AcGePoint2d*)vec );
}
  Acad::ErrorStatus
MkrDwgFiler::writeVector2d( const AcGeVector2d& vec )
{
    return writePoint2d( *(AcGePoint2d*)&vec );
}
  Acad::ErrorStatus
MkrDwgFiler::readVector3d( AcGeVector3d* vec )
{
    return readPoint3d( (AcGePoint3d*)vec );
}
  Acad::ErrorStatus
MkrDwgFiler::writeVector3d( const AcGeVector3d& vec )
{
    return writePoint3d( *(AcGePoint3d*)&vec );
}
  Acad::ErrorStatus
MkrDwgFiler::readScale3d( AcGeScale3d* s )
{
    return readPoint3d( (AcGePoint3d*)s );
}
  Acad::ErrorStatus
MkrDwgFiler::writeScale3d( const AcGeScale3d& s )
{
    return writePoint3d( *(AcGePoint3d*)&s );
}
  Acad::ErrorStatus
MkrDwgFiler::readBytes( void *buf,
/*Adesk::UInt32*/Adesk::UIntPtr len )
{
    ads_binary bin;
    Acad::ErrorStatus es = readBChunk( &bin );
    if (Acad::eOk != es)
        return es;
      memcpy( buf, bin.buf, bin.clen );
    free( bin.buf );
    return Acad::eOk;
}
  Acad::ErrorStatus
MkrDwgFiler::writeBytes( const void *buf,
/*Adesk::UInt32*/Adesk::UIntPtr len )
{
    // TODO!
    // ads_binary is limited to max. 127 bytes,
    // while writeBytes is not.
    //
    if (len > 127) {
  acedAlert(
   _T("writeBytes: len is currently limited to 127 !") );
        return Acad::eNotImplementedYet;
    }
      ads_binary bin = { (short)len, (char*)buf };
    return writeBChunk( bin );
}
  Acad::ErrorStatus
MkrDwgFiler::seek( /*long*/ Adesk::Int64 offset, int method )
{
    return Acad::eNotImplementedYet;
}
  //long
Adesk::Int64
MkrDwgFiler::tell() const
{
    return 0;
}
  // -----------------------------------------------------------
Acad::ErrorStatus MkrDwgFiler::readInt8(Adesk::Int8 * param2)
{
 return Acad::ErrorStatus();
}
  // -----------------------------------------------------------
Acad::ErrorStatus MkrDwgFiler::writeInt8(Adesk::Int8 param2)
{
 return Acad::ErrorStatus();
}
  Acad::ErrorStatus MkrDwgFiler::readString(AcString &)
{
 return Acad::ErrorStatus();
}
  Acad::ErrorStatus MkrDwgFiler::writeString(const AcString &)
{
 return Acad::ErrorStatus();
}
  Acad::ErrorStatus MkrDwgFiler::readString(ACHAR **ppStr)
{
 if (AcDb::kDxfXdAsciiString != (*m_ppwalk)->restype)
{
  acedAlert( _T("Sequence Error in readString !") );
  return Acad::eInvalidResBuf;
}
  *ppStr = _tcsdup( (*m_ppwalk)->resval.rstring );
m_ppwalk = &(*m_ppwalk)->rbnext;
 return Acad::eOk;
}
  Acad::ErrorStatus MkrDwgFiler::writeString(const ACHAR *pStr)
{
*m_ppwalk = acutNewRb( AcDb::kDxfXdAsciiString );
(*m_ppwalk)->resval.rstring = _tcsdup( pStr );
m_ppwalk = &(*m_ppwalk)->rbnext;
 return Acad::eOk;
}
    Some place holder

