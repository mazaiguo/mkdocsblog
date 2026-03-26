---
title: "Solving problems associated with custom entities as persistent reactors"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Database
description: "Attaching a custom entity as a persistent reactor is as easy, however, working with COPY/MOVE/WBLOCK/INSERT and other AutoCAD events are more chall..."
author: Autodesk
---
# Solving problems associated with custom entities as persistent reactors

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/solving-problems-associated-with-custom-entities-as-persistent-reactors.html

## 文章内容

By Gopinath Taget
Attaching a custom entity as a persistent reactor is as easy, however, working with COPY/MOVE/WBLOCK/INSERT and other AutoCAD events are more challenging. This is mainly because you can't easily distinguish among individual modifications to the custom entity among the group activities, especially just with the object reactor itself. In other words, you need to find the way to tell whether the custom entity (or the associated entity) is modified alone or if they were modified together. This is a common scenario in many of the Acad command activities/events, such as COPY, MOVE, ROTATE, BLOCK, WBLOCK, INSERT, SCALE, ARRAY, COPYCLIP/PASTECLIP, to name a few.
Therefore, other type of reactors, such as AcEditorReactor and AcDbDatabaseReactor are needed. Together, with the appropriate callback overrides and the appropriate event control during different callbacks, these problems can be solved.
The following code shows how to do this:
The custom entity and reactor headers:
  #include <dbents.h>
#include <aced.h>
#include <acgi.h>
#include <acgiutil.h>
#include <gemat3d.h>
#include <dbidmap.h>
#include <adscodes.h>
#include <math.h>
#include "dbproxy.h"
#include "migrtion.h"
#include "dbapserv.h "
  #include <TCHAR.h>
  #define ErrStat Acad::ErrorStatus
#define CopyPoint(a, b) a[X] = b[X]; a[Y] = b[Y]; a[Z] = b[Z]
  #ifndef PI
#define PI    3.14159265358979323846
#endif
  BOOL rx_wcs2ecs(const AcGePoint3d& a_p, AcGePoint3d& a_q,
    const AcGeVector3d& norm, BOOL vec);
BOOL rx_ecs2wcs(const AcGePoint3d& a_p, AcGePoint3d& a_q,
    const AcGeVector3d& norm, BOOL vec);
int PrintReactors(); //for debug purposes only
///////////////////////////////////////////////////////////
//
class CMyArc : public AcDbCurve
{
public:
ACRX_DECLARE_MEMBERS(CMyArc);
CMyArc() : AcDbCurve(), m_selfModified(FALSE) {}
~CMyArc() { m_selfModified = FALSE; }
   // essential entity methods override
Adesk::Boolean subWorldDraw(AcGiWorldDraw *pWd);
ErrStat subExplode(AcDbVoidPtrArray& entSet) const;
  ErrStat dwgInFields (AcDbDwgFiler*);
    ErrStat dwgOutFields(AcDbDwgFiler*) const;
ErrStat subGetGripPoints(AcGePoint3dArray& gripPoints,
        AcDbIntArray& osnapMasks,
        AcDbIntArray& geomIds) const;
ErrStat subMoveGripPointsAt(const AcDbIntArray& indices,
  const AcGeVector3d& offset);
ErrStat subGetStretchPoints(AcGePoint3dArray& stretchPts) const;
ErrStat subMoveStretchPointsAt(const AcDbIntArray& indices,
  const AcGeVector3d& offset);
  ErrStat subGetOsnapPoints(AcDb::OsnapMode osnapMode,
         Adesk::GsMarker gsSelectionMark,
         const AcGePoint3d& pickPoint,
         const AcGePoint3d& lastPoint,
         const AcGeMatrix3d& viewXform,
         AcGePoint3dArray& snapPoints,
         AcDbIntArray& geomIds) const;
ErrStat subGetTransformedCopy(const AcGeMatrix3d& xform,
  AcDbEntity*& pEnt) const;
ErrStat subTransformBy(const AcGeMatrix3d &xfm);
ErrStat subGetGeomExtents(AcDbExtents& extents) const;
/*----------------------------------------------------------*/
public: // the reactor methods
// void openedForModify(const AcDbObject* pDbObj);
 void copied(const AcDbObject* pDbObj,
  const AcDbObject* pNewObj);
    void modified(const AcDbObject* pObj);
/*----------------------------------------------------------*/
public: // utility functions
BOOL arcIsTheOpposite(const AcDbArc* pArc);
 void get2Points(AcGePoint3d& stp,
       AcGePoint3d& end,
       const AcGePoint3d& ctr,
       const double& r,
       const AcGeVector3d& norm,
       const double& sAng,
       const double& eAng);
 void get3Points(AcGePoint3d& stp, AcGePoint3d& mid,
  AcGePoint3d& end) const;
 void get3Points(AcGePoint3d& stp, AcGePoint3d& mid,
     AcGePoint3d& end, double& midAng) const;
 void get3GripPoints(AcGePoint3d& stp, AcGePoint3d& mid,
  AcGePoint3d& end) const;
/*-----------------------------------------------------------*/
public: // data member functions
AcGePoint3d& center() { assertReadEnabled(); return m_center; }
 void setCenter(AcGePoint3d& pt) {
  assertWriteEnabled(); m_center = pt; }
AcGeVector3d& normal() {
  assertReadEnabled(); return m_normal; }
 void setNormal(AcGeVector3d& norm) {
  assertWriteEnabled(); m_normal = norm; }
 double radius() {
  assertReadEnabled(); return m_radius; }
 void setRadius(double r) {
  assertWriteEnabled(); m_radius = r; }
 double strAng() {
  assertReadEnabled(); return m_strAng; }
 void setStrAng(double ang) {
  assertWriteEnabled(); m_strAng = ang; }
 double endAng() {
  assertReadEnabled(); return m_endAng; }
 void setEndAng(double ang) {
  assertWriteEnabled(); m_endAng = ang; }
 double getOffset() {
  assertReadEnabled(); return m_offset; }
 void setOffset(double off) {
  assertWriteEnabled(); m_offset = off; }
 short side() {
  assertReadEnabled(); return m_side; }
 void setSide(short i) {
  assertWriteEnabled(); m_side = i; }
AcDbObjectId& arcId() {
  assertReadEnabled(); return m_arcId; }
 void setArcId(AcDbObjectId& id) {
  assertWriteEnabled(); m_arcId = id; }
   //AcDbObjectId& getClonedArcId() {return m_clonedArcId;}
 //void setSelfTransFlag(BOOL bFlag) { m_selfTransformed = bFlag; }
private:
AcGePoint3d  m_center;
AcGeVector3d m_normal;
 double   m_radius;
 double   m_strAng;
 double   m_endAng;
   double   m_offset;
 short   m_side;
AcDbSoftPointerId m_arcId;
  protected:
BOOL m_selfModified;
};
/////////////////////////////////////////////////////////////////////
class CMyArcEdReactor : public AcEditorReactor
{
 friend class CMyArc;
 friend class CMyArcDbReactor;
public:
CMyArcEdReactor() : m_bProcessing(Adesk::kFalse) {}
 void commandWillStart(const ACHAR* pCmd);
 void commandCancelled(const ACHAR* pCmd);
 void commandEnded(const ACHAR* pCmd);
 void endDeepClone(AcDbIdMapping& idMap);
   // void modifyPartner(AcDbObjectId& myId);
 void setProcessingFlag(Adesk::Boolean tf) {m_bProcessing = tf;}
  private:
 void checkIfArcIsModifiedAlone(AcDbObjectIdArray& arcsIdArray,
           AcDbObjectIdArray& myArcsIdArray);
 void checkIfMyArcIsModifiedAlone(AcDbObjectIdArray& arcsIdArray,
          AcDbObjectIdArray& myArcsIdArray);
 void checkIfArcIsModifiedAlone();
 void checkIfMyArcIsModifiedAlone();
 void removePersistentReactorFromArc(const AcDbObjectId& arcId,
          const AcDbObjectId& reactorId);
 void cleanUpArrays();
  Adesk::Boolean m_bProcessing;
BOOL isMyArcPersistentReactor(const AcDbObjectId& id);
AcDbObjectIdArray m_modifiedMyArcsIdArray; //CMyArc
// AcDbObjectIdArray m_refArcIdArray;   //reference
AcDbObjectIdArray m_modifiedArcsIdArray; //Arc
  public:
// AcDbObjectIdArray m_clonedArcsIdArray,
//       m_clonedMyArcsIdArray;
};
  inline
BOOL CMyArcEdReactor::isMyArcPersistentReactor(const AcDbObjectId& id)
{
AcDbObject* pObj;
BOOL b = FALSE;
 if(acdbOpenObject(pObj, id, AcDb::kForRead) == Acad::eOk)
{
  if(pObj->isKindOf(CMyArc::desc()))
   b = TRUE;
  else
   b = FALSE;
  pObj->close();
}
 return b;
}
/////////////////////////////////////////////////////////////////////
class CMyArcDbReactor : public AcDbDatabaseReactor
{
public:
    void objectOpenedForModify(const AcDbDatabase* pDb,
  const AcDbObject* pObj);
// void objectModified(const AcDbDatabase* pDb, const AcDbObject* pObj);
};
Custom entity Implementation:
//////////////////////////////////////////////////////////////
#include "myArc.h"
  extern CMyArcEdReactor *gpEdReactor;
  // this is necessary for custom classes
ACRX_DXF_DEFINE_MEMBERS(CMyArc, AcDbCurve, AcDb::kDHL_CURRENT,
AcDb::kMReleaseCurrent, AcDbProxyEntity::kAllButCloningAllowed,
CMYARC, CMyArc);
MAKE_ACDBOPENOBJECT_FUNCTION(CMyArc);
  ///////////////////////////////////////////////////////////////
//
// This world draw is simple.
// However, it is important to notice that it is almost the last
// method that is going to be called in the custom entity. That's
// why we can reset flag for sure.
//
Adesk::Boolean CMyArc::subWorldDraw(AcGiWorldDraw *pWd)
{
m_selfModified = FALSE; //reset
AcGePoint3d stp, mid, end;
get3Points(stp, mid, end);
pWd->geometry().circularArc(stp, mid, end, kAcGiArcSimple);
    return Adesk::kTrue; // only one view method
}
//
// When the custom arc is exploded, it is turned into an AcDbArc.
//
ErrStat CMyArc::subExplode(AcDbVoidPtrArray& entSet) const
{
assertReadEnabled();
AcDbArc* pArc = new AcDbArc(m_center, m_radius,
  m_strAng, m_endAng);
pArc->setNormal(m_normal);
entSet.append(pArc);
    return Acad::eOk;
}
//
// Read in all the data members.
//
ErrStat CMyArc::dwgInFields(AcDbDwgFiler* pf)
{
assertWriteEnabled();
ErrStat es;
 if((es = AcDbEntity::dwgInFields(pf)) != Acad::eOk)
  return es;
  pf->readItem(&m_center);
pf->readItem(&m_normal);
pf->readItem(&m_radius);
pf->readItem(&m_strAng);
pf->readItem(&m_endAng);
pf->readItem(&m_offset);
pf->readItem(&m_side);
pf->readItem(&m_arcId); // read in as softPointerId
      return pf->filerStatus();
}
//
// Write all the data members to the hard storage.
//
ErrStat CMyArc::dwgOutFields(AcDbDwgFiler* pf) const
{
assertReadEnabled();
ErrStat es;
 if((es = AcDbEntity::dwgOutFields(pf)) != Acad::eOk)
  return es;
  pf->writeItem(m_center);
pf->writeItem(m_normal);
pf->writeItem(m_radius);
pf->writeItem(m_strAng);
pf->writeItem(m_endAng);
pf->writeItem(m_offset);
pf->writeItem(m_side);
   // file softpointid instead of hardpointid
pf->writeSoftPointerId(m_arcId);
      return pf->filerStatus();
}
//
// 3 grip points just like an arc.
//
ErrStat CMyArc::subGetGripPoints(AcGePoint3dArray& gripPoints,
        AcDbIntArray& osnapMasks,
        AcDbIntArray& geomIds) const
{
assertReadEnabled();
AcGePoint3d stp, mid, end;
get3GripPoints(stp, mid, end);
gripPoints.append(end);
gripPoints.append(mid);
gripPoints.append(stp);
    return Acad::eOk;
}
//
// The user can move each grip point implemented, so each one
// of the offsets has to be caculated.
//
ErrStat CMyArc::subMoveGripPointsAt(const AcDbIntArray& indices,
        const AcGeVector3d& offset)
{
    assertWriteEnabled();
      AcGeMatrix3d mat;
    mat.entry[0][3] = offset.x;
    mat.entry[1][3] = offset.y;
    mat.entry[2][3] = offset.z;
  AcGePoint3d stp, mid, end, newPt;
ads_point ctr, pt;
get3Points(stp, mid, end);
   for (int i = 0; i < indices.length(); i++)
{
  switch(indices[i])
  {
   case 0:
    newPt = end.transformBy(mat);
    continue;
   case 1:
    newPt = mid.transformBy(mat);
    continue;
   case 2:
    newPt = stp.transformBy(mat);
    continue;
  }
}
  CopyPoint(ctr, m_center);
CopyPoint(pt, newPt);
 double d = m_center.distanceTo(newPt);
 if(d >= m_radius)
{
  m_offset = d - m_radius;
  m_side = 1;
}
 else
{
  m_offset = m_radius - d;
  m_side = 2;
}
   return Acad::eOk;
}
//
// Make it the same as getGripPoints().
//
ErrStat CMyArc::subGetStretchPoints(
AcGePoint3dArray& stretchPts) const
{
    AcDbIntArray osnapModes;
    AcDbIntArray geomIds;
      assertReadEnabled();
    return getGripPoints(stretchPts, osnapModes, geomIds);
}
//
// Make it the same as moveGripPointsAt().
//
ErrStat CMyArc::subMoveStretchPointsAt(const AcDbIntArray& indices,
           const AcGeVector3d& offset)
{
    assertWriteEnabled();
    return moveGripPointsAt(indices, offset);
}
//
// We determine what kind of the osnap points that are applicable.
//
ErrStat CMyArc::subGetOsnapPoints(AcDb::OsnapMode osnapMode,
         Adesk::GsMarker gsSelectionMark,
         const AcGePoint3d& pickPoint,
         const AcGePoint3d& lastPoint,
         const AcGeMatrix3d& viewXform,
         AcGePoint3dArray& snapPoints,
         AcDbIntArray& geomIds) const
{
    assertReadEnabled();
  AcGePoint3d stp, mid, end;
get3Points(stp, mid, end);
   switch (osnapMode)
{
    case AcDb::kOsModeEnd:
  snapPoints.append(stp);
  snapPoints.append(end);
  break;
    case AcDb::kOsModeMid:
  snapPoints.append(mid);
  break;
    case AcDb::kOsModeCen:
        snapPoints.append(m_center);
        break;
      case AcDb::kOsModeIns:
    case AcDb::kOsModeNear:
    case AcDb::kOsModeQuad:
    case AcDb::kOsModeNode:
    case AcDb::kOsModePerp:
    case AcDb::kOsModeTan:   
     return Acad::eInvalidInput;
   default:
        break;
    }
    return Acad::eOk;
}
//
// The cloned entity is transformed and transformBy() is called.
//
ErrStat CMyArc::subGetTransformedCopy(const AcGeMatrix3d& xform,
AcDbEntity*& pEnt) const
{
    assertReadEnabled();
    if (!xform.isUniScaledOrtho())
        return Acad::eCannotScaleNonUniformly;
      pEnt = (CMyArc*)this->clone();
 if (pEnt->transformBy(xform) != Acad::eOk)
{
  delete pEnt;
  pEnt = 0;
}
 return Acad::eOk;
}
//
// We have to override this to make
// our custom entity to be transformable.
// Notice that we don't need to transform
// the entity is modified() have
// done something on it.
//
ErrStat CMyArc::subTransformBy(const AcGeMatrix3d &xform)
{
assertWriteEnabled();
   if (!xform.isUniScaledOrtho())
{
  m_center.transformBy(xform);
  m_normal.transformBy(xform); //don't miss this one
  m_normal.normalize();
  return Acad::eCannotScaleNonUniformly;
}
   if(!m_selfModified)
{
  AcGePoint3d org(0,0,0);
  AcGePoint3d str(cos(m_strAng), sin(m_strAng), 0);
  AcGePoint3d end(cos(m_endAng), sin(m_endAng), 0);
    rx_ecs2wcs(str, str, m_normal, FALSE);
  rx_ecs2wcs(end, end, m_normal, FALSE);
    str.transformBy(xform);
  end.transformBy(xform);
  org.transformBy(xform);
    m_center.transformBy(xform);
  m_normal.transformBy(xform); //don't miss this one
  m_normal.normalize();
    str -= org.asVector();
  rx_wcs2ecs(str, str, m_normal, FALSE);
  setStrAng(atan2(str[Y], str[X]));
  end -= org.asVector();
  rx_wcs2ecs(end, end, m_normal, FALSE);
  setEndAng(atan2(end[Y], end[X]));
    // Mirroring xform, switch start & end angles
  if (xform.det() < 0)
  {
   double ang = m_strAng;
   m_strAng = m_endAng;
   m_endAng = ang;
  }
    // We are scaling the entity so radius and offset are affected.
  AcGeScale3d s;
  s.extractScale(xform);
  assert(s.sx > 0.0);
  if (s.sx != 1.0)
  {
   m_radius *= s.sx;
   m_offset *= s.sx;
  }
}
   return Acad::eOk;
}
//
// Define the bounding box.
//
ErrStat CMyArc::subGetGeomExtents(AcDbExtents& extents) const
{
    assertReadEnabled();
  AcGePoint3d stp, mid, end;
get3Points(stp, mid, end);
  extents.addPoint(stp);
extents.addPoint(mid);
extents.addPoint(end);
      return Acad::eOk;
}
///////////////////////////////////////////////////////////////
// Although we know that we can't rely on the notification
// firing sequence, we do know (through testing) that
// Object reactor notifications definitely happens
// before the database reactor nofications.
//
// This is not necessary because
// we've done the endDeepClone() override.
// It is here to reveal another option which
// you can track the cloned objects.
// It has limitations however.
//
void CMyArc::copied(const AcDbObject* pDbObj,
 const AcDbObject* pNewObj)
{
 if(!pDbObj->isErased() && !pNewObj->isErased())
{
  //gpEdReactor->m_clonedArcsIdArray.append(pNewObj->objectId());
}
}
//
// There are couple of important issues here:
// 1. if transformBy() was used, we definitely want to avoid
//   redundant self-modification here. The solution is to
//   set a flag;
// 2. Usually, the party receiving the notification is in a
//    read only state, however, if extreme caution is taken,
//   it is possible to modify itself.
//
//
void CMyArc::modified(const AcDbObject* pObj)
{
 if(gpEdReactor->m_bProcessing) //safe guard
  return;
assert(pObj);
AcDbArc* pArc = AcDbArc::cast(pObj);
 if(!pArc)
  return;
   // This is runtime identification.
 if(m_arcId == pArc->objectId())
{
  Adesk::Boolean wasWritable;
  ErrStat es = upgradeFromNotify(wasWritable);
  if((es != Acad::eOk) && (es != Acad::eWasOpenForWrite))
   return; // Try again later
    assertWriteEnabled(); // jump to openedForModify()
  if(arcIsTheOpposite(pArc) == 1)
   m_side = 3 - m_side;
    m_center = pArc->center();
  m_radius = pArc->radius();
  m_strAng = pArc->startAngle();
  m_endAng = pArc->endAngle();
  m_normal = pArc->normal();
    recordGraphicsModified();
  es = downgradeToNotify(wasWritable);
  assert(es == Acad::eOk);
  m_selfModified = TRUE;
}
 else
  m_selfModified = FALSE;
}
///////////////////////////////////////////////////////////////
// ** Some utility functions **
//
// This is key to tell that the arc dir has changed.
//
BOOL CMyArc::arcIsTheOpposite(const AcDbArc* pArc)
{
AcGePoint3d a_center = pArc->center();
AcGeVector3d a_normal = pArc->normal();
 double a_radius = pArc->radius();
 double a_startAng = pArc->startAngle();
 double a_endAng = pArc->endAngle();
AcGePoint3d a_stp, a_end, t_stp, t_end;
get2Points(a_stp, a_end, a_center, a_radius,
      a_normal, a_startAng, a_endAng);
get2Points(t_stp, t_end, m_center, m_radius,
      m_normal, m_strAng, m_endAng);
   if(a_stp == t_end || a_end == t_stp)
  return TRUE;
 else
  return FALSE;
}
//
// Get the start point and the end point of an arc.
//
void CMyArc::get2Points(AcGePoint3d& stp,
        AcGePoint3d& end,
        const AcGePoint3d& ctr,
        const double& r,
        const AcGeVector3d& norm,
        const double& sAng,
        const double& eAng)
{
ads_point ptCtr, ptStp, ptEnd;
AcGePoint3d w_ctr;
w_ctr = ctr;
rx_wcs2ecs(w_ctr, w_ctr, norm, FALSE);
CopyPoint(ptCtr, w_ctr);
ads_polar(ptCtr, sAng, r, ptStp);
ads_polar(ptCtr, eAng, r, ptEnd);
  CopyPoint(stp, ptStp);
CopyPoint(end, ptEnd);
rx_ecs2wcs(stp, stp, m_normal, FALSE);
rx_ecs2wcs(end, end, m_normal, FALSE);
}
//
// Overloaded function.
//
void CMyArc::get3Points(AcGePoint3d& stp,
        AcGePoint3d& mid,
        AcGePoint3d& end) const
{
 double midAng = 0;
get3Points(stp, mid, end, midAng);
}
//
// Overloaded function.
//
void CMyArc::get3Points(AcGePoint3d& stp,
        AcGePoint3d& mid,
        AcGePoint3d& end,
        double& midAng) const
{
ads_point ptCtr, ptStp, ptMid, ptEnd;
 double incAng = m_endAng - m_strAng;
 if(incAng < 0)
  incAng += 2 * PI;
midAng = m_strAng + incAng/2;
 double radius;
 if(m_side == 1)
  radius = m_radius + m_offset;
 else
  radius = m_radius - m_offset;
  AcGePoint3d w_ctr, entNorm;
w_ctr = m_center;
rx_wcs2ecs(w_ctr, w_ctr, m_normal, FALSE);
CopyPoint(ptCtr, w_ctr);
ads_polar(ptCtr, m_strAng, radius, ptStp);
ads_polar(ptCtr, midAng, radius, ptMid);
ads_polar(ptCtr, m_endAng, radius, ptEnd);
  CopyPoint(stp, ptStp);
CopyPoint(mid, ptMid);
CopyPoint(end, ptEnd);
rx_ecs2wcs(stp, stp, m_normal, FALSE);
rx_ecs2wcs(mid, mid, m_normal, FALSE);
rx_ecs2wcs(end, end, m_normal, FALSE);
}
//
// Caculate (3) points in WCS.
//
void CMyArc::get3GripPoints(AcGePoint3d& stp,
         AcGePoint3d& mid,
         AcGePoint3d& end) const
{
ads_point ptCtr, ptStp, ptMid, ptEnd;
   double incAng = m_endAng - m_strAng;
 if(incAng < 0)
  incAng += 2 * PI;
 double midAng = m_strAng + incAng/2;
 double radius;
 if(m_side == 1)
  radius = m_radius + m_offset;
 else
  radius = m_radius - m_offset;
  AcGePoint3d w_ctr, entNorm;
w_ctr = m_center;
rx_wcs2ecs(w_ctr, w_ctr, m_normal, FALSE);
CopyPoint(ptCtr, w_ctr);
ads_polar(ptCtr, m_strAng, radius, ptStp);
ads_polar(ptCtr, midAng, radius, ptMid);
ads_polar(ptCtr, m_endAng, radius, ptEnd);
  CopyPoint(stp, ptStp);
CopyPoint(mid, ptMid);
CopyPoint(end, ptEnd);
rx_ecs2wcs(stp, stp, m_normal, FALSE);
rx_ecs2wcs(mid, mid, m_normal, FALSE);
rx_ecs2wcs(end, end, m_normal, FALSE);
}
//
// Common transformation utility functions.
//
BOOL rx_wcs2ecs(const AcGePoint3d& a_p, AcGePoint3d& a_q,
    const AcGeVector3d& norm, BOOL vec)
{
ads_point p, q;
CopyPoint(p, a_p);
      struct resbuf rbfrom, rbto;
    int status;
      rbfrom.restype = RTSHORT;
    rbfrom.resval.rint = 0;             // from world
      rbto.restype = RT3DPOINT;
    rbto.resval.rpoint[X] = norm[X];    // to ecs
    rbto.resval.rpoint[Y] = norm[Y];
    rbto.resval.rpoint[Z] = norm[Z];
      status = ads_trans(p, &rbfrom, &rbto, vec, q);
    if (status != RTNORM)
        return FALSE;
CopyPoint(a_q, q);
    return TRUE;
}
//
// Common transformation utility functions.
//
BOOL rx_ecs2wcs(const AcGePoint3d& a_p,
    AcGePoint3d& a_q,
    const AcGeVector3d& norm,
    BOOL vec)
{
ads_point p, q;
CopyPoint(p, a_p);
      struct resbuf rbfrom, rbto;
    int status;
      rbfrom.restype = RT3DPOINT;
    rbfrom.resval.rpoint[X] = norm[X];  // from ecs
    rbfrom.resval.rpoint[Y] = norm[Y];
    rbfrom.resval.rpoint[Z] = norm[Z];
      rbto.restype = RTSHORT;
    rbto.resval.rint = 0;               // to world
      status = ads_trans(p, &rbfrom, &rbto, vec, q);
    if (status != RTNORM)
        return FALSE;
CopyPoint(a_q, q);
    return TRUE;
}
  Reactors Implementation:
#include "myArc.h"
//
//
//
//
extern CMyArcEdReactor* gpEdReactor;
//////////////////////////////////////////////////////////////
//
// There is a timing issue. Sometimes commandEnded() is called before
// objectModified(), but sometimes, vise versa.
//
// However, objectOpenedForModify() definitely
// happens before commandEnded().
//
//
void CMyArcDbReactor::objectOpenedForModify(const AcDbDatabase* pDb,
           const AcDbObject* pObj)
{
 if(gpEdReactor->m_bProcessing)
  return;
AcDbObjectId id = pObj->objectId();
 // Arcs that has reactors attached need to be recorded.
 if(pObj->isA() == AcDbArc::desc())
{
  if(AcDbArc::cast(pObj)->reactors() &&
   !gpEdReactor->m_modifiedArcsIdArray.contains(id))
  {
   gpEdReactor->m_modifiedArcsIdArray.append(id);
  }
}
 // Now if we are sure that myArc is modified, record it. 
 if(pObj->isA() == CMyArc::desc())
{
  if(!gpEdReactor->m_modifiedMyArcsIdArray.contains(id))
   gpEdReactor->m_modifiedMyArcsIdArray.append(id);
}
}
/////////////////////////////////////////////////////////////////
//
// Within endDeepClone(), we'll find out myArcs that are cloned.
// If they are, record them in the m_clonedMyArcsIdArray.
//
void CMyArcEdReactor::endDeepClone(AcDbIdMapping& idMap)
{
AcDb::DeepCloneType cloneType = idMap.deepCloneContext();
 switch(cloneType)
{
  //case AcDb::kDcWblock:
  //case AcDb::kDcExplode:
  case AcDb::kDcCopy:
  {
   AcDbIdMappingIter* pIter = new AcDbIdMappingIter(idMap);
   assert(pIter);
   AcDbIdPair idPair;
   for(pIter->start(); !pIter->done(); pIter->next())
   {
    if(!(pIter->getMap(idPair) && idPair.isPrimary() &&
     idPair.isOwnerXlated()))
     continue;
      AcDbObjectId idPrimary = idPair.key();
    AcDbObject* pObj;
    if(acdbOpenObject(pObj, idPrimary, AcDb::kForRead) ==
     Acad::eOk)
    {
     AcDbObjectId idCloned = idPair.value();
     assert(idCloned != AcDbObjectId::kNull);
     AcDbIdPair tempIdPair;
     if(pObj->isKindOf(CMyArc::desc()))
     {
      CMyArc* pMyArc = CMyArc::cast(pObj);
      AcDbObjectId arcId = pMyArc->arcId();
      if(arcId == AcDbObjectId::kNull)
      {
       pMyArc->close();
       continue;
      }
      pMyArc->close(); //close the primary one
      tempIdPair.setKey(arcId);
      // check if the referenced arc is cloned as well
      if(idMap.compute(tempIdPair) != Adesk::kTrue)
      {
       CMyArc* pCloned;
       if(acdbOpenObject((AcDbObject*&)pCloned,
        idCloned, AcDb::kForWrite) == Acad::eOk)
       {
        pCloned->setArcId(AcDbObjectId(0));
        pCloned->close();
       }
      }
     }
     else if(pObj->isKindOf(AcDbArc::desc()))
     {
      AcDbArc* pArc = AcDbArc::cast(pObj);
      BOOL b = m_bProcessing; //save the original value
      m_bProcessing = Adesk::kTrue; // set the flag
      AcDbVoidPtrArray* pArray = pArc->reactors();
      if(pArray && pArray->length() > 0)
      {
       for(int i=0; i<pArray->length(); i++)
       {
        void* pVoid = pArray->at(i);
        if(acdbIsPersistentReactor(pVoid))
        {
         AcDbObjectId reactorId =
         acdbPersistentReactorObjectId(pVoid);
         AcDbEntity* pEnt;
         if(acdbOpenObject(pEnt, reactorId,
          AcDb::kForRead) == Acad::eOk)
         {
          if(pEnt->isKindOf(CMyArc::desc()))
          {
           tempIdPair.
            setKey(pEnt->objectId());
           pEnt->close();
           // If the reactor entity
           // is not cloned
           // the arc is cloned alone.
           // We'll need to remove
           // the persistent reactor
           // attached to it
           if(idMap.compute(tempIdPair) !=
            Adesk::kTrue)
           {
            AcDbArc* pCloned;
            if(acdbOpenObject
             (pCloned, idCloned,
             AcDb::kForWrite) ==
             Acad::eOk)
            {
             pCloned->
             removePersistentReactor(
             reactorId);
             pCloned->close();
            }
           }
          }
         }
        }
       }
      }
      pArc->close();
      m_bProcessing = b; //restore
     }
     else  
      pObj->close();
    }
   } // end for
   delete pIter;
   break;
  }
  default:
   break;
}
}
//
// Make sure the flag is reset.
//
void CMyArcEdReactor::commandWillStart(const ACHAR* pCmd)
{
m_bProcessing = Adesk::kFalse;
}
//
// Make sure the flag is reset.
//
void CMyArcEdReactor::commandCancelled(const ACHAR * pCmd)
{
m_bProcessing = Adesk::kFalse;
}
//
// This is the place to modify things safely because all the
// nofications have finished. However, if we modify an entity
// that has an reactor attached, notification is triggered.
// That's why we need to set the flag so the nofications are
// ignored when we're processing the modifications.
//
void CMyArcEdReactor::commandEnded(const ACHAR* pCmd)
{
 if(_tcscmp(pCmd, L"MYARC") == 0 ||
    _tcscmp(pCmd, L"ARX") == 0 ||
    _tcscmp(pCmd, L"ARC") == 0 ||
    _tcscmp(pCmd, L"GRIP_STRETCH") == 0) // This one is really needed.
{
  m_bProcessing = Adesk::kFalse;
  cleanUpArrays();
  return;
}
  m_bProcessing = Adesk::kTrue;
 // When the arc or myArc is modified alone, all is left here,
 // is to remove the unnecessary references.
checkIfArcIsModifiedAlone(m_modifiedArcsIdArray,
  m_modifiedMyArcsIdArray);
checkIfMyArcIsModifiedAlone(m_modifiedArcsIdArray,
  m_modifiedMyArcsIdArray);
// checkIfMyArcIsModifiedAlone(m_clonedArcsIdArray,
// m_clonedMyArcsIdArray);
cleanUpArrays();
  m_bProcessing = Adesk::kFalse;
}
  //
//
//
void CMyArcEdReactor::checkIfArcIsModifiedAlone(
AcDbObjectIdArray& arcsIdArray,
AcDbObjectIdArray& myArcsIdArray)
{
 for(int ii=0; ii < arcsIdArray.length(); ii++)
{
  AcDbObjectId id = arcsIdArray[ii];
  assert(id != AcDbObjectId::kNull);
  // We want to make sure that the arc is modified alone.
  // If that's the case, we'll need to remove the reactor
  // from the reactor list.
  AcDbArc* pArc;
  if(acdbOpenObject(pArc, id, AcDb::kForRead) == Acad::eOk)
  {
   assert(pArc);
   AcDbVoidPtrArray* pArray = pArc->reactors();
   if(pArray && pArray->length() > 0)
   {
    for(int i=0; i<pArray->length(); i++)
    {
     void* pVoid = pArray->at(i);
     if(acdbIsPersistentReactor(pVoid))
     {
      AcDbObjectId reactorId =
       acdbPersistentReactorObjectId(pVoid);
      if(myArcsIdArray.isEmpty() ||
       !myArcsIdArray.contains(reactorId))
      {
       if(pArc->upgradeOpen() == Acad::eOk)
       {
        if(isMyArcPersistentReactor(reactorId))
         pArc->removePersistentReactor(
         reactorId);
        pArc->downgradeOpen();
       }
      }
     }
    }
   }
   pArc->close();
  }
}
}
//
// If there are only myArcs that are modified, we need to
// reset our references to null.
//
//
void CMyArcEdReactor::checkIfMyArcIsModifiedAlone(
AcDbObjectIdArray& arcsIdArray,
AcDbObjectIdArray& myArcsIdArray)
{
 for(int ii=0; ii<myArcsIdArray.length(); ii++)
{
  AcDbObjectId id = myArcsIdArray[ii];
  CMyArc* pMyArc;
  if(acdbOpenObject((AcDbObject*&)pMyArc,
   id, AcDb::kForRead) == Acad::eOk)
  {
   assert(pMyArc);
   AcDbObjectId arcId = (AcDbObjectId)pMyArc->arcId();
   if(arcsIdArray.isEmpty() || !arcsIdArray.contains(arcId))
   {
    removePersistentReactorFromArc(arcId, id);
    if(pMyArc->upgradeOpen() == Acad::eOk)
    {
     pMyArc->setArcId(AcDbObjectId(0));
     pMyArc->downgradeOpen();
    }
   }
   pMyArc->close();
  }
}
}
//
// Remove the persistent reactor attached to an entity.
//
void CMyArcEdReactor::removePersistentReactorFromArc(
 const AcDbObjectId& arcId,
 const AcDbObjectId& reactorId)
{
AcDbEntity* pArc;
 if(acdbOpenObject(pArc, arcId, AcDb::kForWrite) == Acad::eOk)
{
  pArc->removePersistentReactor(reactorId);
  pArc->close();
}
}
//
// Clean up our storage so we don't process the wrong info.
//
void CMyArcEdReactor::cleanUpArrays()
{
// while(!m_clonedArcsIdArray.isEmpty())
//  m_clonedArcsIdArray.removeFirst();
// while(!m_clonedMyArcsIdArray.isEmpty())
//  m_clonedMyArcsIdArray.removeFirst();
 while(!m_modifiedArcsIdArray.isEmpty())
  m_modifiedArcsIdArray.removeFirst();
 while(!m_modifiedMyArcsIdArray.isEmpty())
  m_modifiedMyArcsIdArray.removeFirst();
}
Defining commands and other utilities:
///////////////////////////////////////////////////////////////////////
#include "myArc.h"
#include <dbsymtb.h>
#include <new.h>
  BOOL purePaperSpace();
Adesk::Boolean postToDb(CMyArc*& pMyArc);
  CMyArcDbReactor *gpDbReactor;
CMyArcEdReactor *gpEdReactor;
///////////////////////////////////////////////////////////////////////
//
// Create the custom arc and have it attached
// to the arc as a persistent reactor.
//
void createMyArc()
{
ads_name enam;
ads_point pt;
 if(ads_entsel(L"Select an arc: ", enam, pt) != RTNORM)
{
  ads_printf(L"\nError selecting an entity.");
  return;
}
AcDbObjectId id;
 if(acdbGetObjectId(id, enam) != Acad::eOk)
{
  ads_printf(L"\nError converting objectId. ");
  return;
}
AcDbEntity* pEnt = NULL;
 if(acdbOpenObject(pEnt, id, AcDb::kForWrite) != Acad::eOk)
{
  ads_printf(L"\nError opening entity.");
  return;
}
 if(pEnt->isA() != AcDbArc::desc())
{
  ads_printf(L"\nEntity selected is not an arc. ");
  pEnt->close();
  return;
}
  CMyArc* pMyArc = new CMyArc;
AcDbArc* pArc = AcDbArc::cast(pEnt);
assert(pArc);
  pMyArc->setCenter(pArc->center());
pMyArc->setRadius(pArc->radius());
pMyArc->setNormal(pArc->normal());
pMyArc->setStrAng(pArc->startAngle());
pMyArc->setEndAng(pArc->endAngle());
pMyArc->setLayer(pArc->layer());
pMyArc->setLinetype(pArc->linetype());
pMyArc->setColorIndex(1 /*pArc->colorIndex()*/);
   // CMyArc specifics
pMyArc->setOffset(pArc->radius() / 20);
pMyArc->setSide(1);
pMyArc->setArcId(pArc->objectId()); // reference to the arc
  postToDb(pMyArc);
  gpEdReactor->setProcessingFlag(Adesk::kTrue);
pArc->addPersistentReactor(pMyArc->objectId());
pMyArc->close();
pArc->close();
gpEdReactor->setProcessingFlag(Adesk::kFalse);
}
//
// The user can start our command in model or paper space,
// thus we need to distinguish them.
//
BOOL purePaperSpace()
{
 struct resbuf res;
 int tilemode, cvport;
ads_getvar(L"tilemode", &res);
    tilemode = res.resval.rint;
  ads_getvar(L"cvport", &res);
cvport = res.resval.rint;
 if(tilemode == 0 && cvport == 1)
  return TRUE;
 else
  return FALSE;
}
//
// Append our entity to the database.
//
Adesk::Boolean postToDb(CMyArc*& pMyArc)
{
    AcDbBlockTable *pBlockTable;
    ErrStat es;
    es = acdbCurDwg()->getBlockTable(pBlockTable, AcDb::kForRead);
    if (es != Acad::eOk)
{
        ads_alert(L"Failed to get the block table!");
        pBlockTable->close();
        return Adesk::kFalse;
    }
      AcDbBlockTableRecord *pBlockRec;
 if(purePaperSpace())
  es = pBlockTable->getAt(ACDB_PAPER_SPACE,
  pBlockRec, AcDb::kForWrite);
 else
  es = pBlockTable->getAt(ACDB_MODEL_SPACE,
  pBlockRec, AcDb::kForWrite);
      if (es != Acad::eOk)
{
        ads_alert(L"Failed to get the block table record!");
        pBlockRec->close();
        return Adesk::kFalse;
    }
  AcDbObjectId objId;
    if(pBlockRec->appendAcDbEntity(objId,
  (AcDbEntity*)pMyArc) != Acad::eOk)
{
        ads_alert(L"Can't add entity to the blockTableRecord!");
  pBlockRec->close();
        return Adesk::kFalse;
}
      es = pBlockTable->close();
assert(es == Acad::eOk);
    es = pBlockRec->close();
assert(es == Acad::eOk);
    return Adesk::kTrue;
}
  //
// Initialization.
//
void InitApp()
{
CMyArc::rxInit();
acrxBuildClassHierarchy();
    acedRegCmds->addCommand(L"RX_CMDS",L"MYARC", L"MYARC",
  ACRX_CMD_MODAL, createMyArc);
gpEdReactor = new CMyArcEdReactor;
acedEditor->addReactor(gpEdReactor);
}
//
// Memory cleanup.
//
void cleanUp()
{
 if(gpEdReactor)
{
  acedEditor->removeReactor(gpEdReactor);
  delete gpEdReactor;
  gpEdReactor = NULL;
}
deleteAcRxClass(CMyArc::desc());
    acedRegCmds->removeGroup(L"RX_CMDS");
}
  /////////////////////////////////////////////////////
// ObjectARX EntryPoint
extern "C" AcRx::AppRetCode
acrxEntryPoint(AcRx::AppMsgCode msg, void *pkt)
{
 switch(msg)
{
  case AcRx::kInitAppMsg:                                                                               
   acrxDynamicLinker->unlockApplication(pkt);
   acrxDynamicLinker->registerAppMDIAware(pkt);
   InitApp();
   break;
     case AcRx::kUnloadAppMsg:
   cleanUp();
   break;
  case AcRx::kLoadDwgMsg:
   if(ads_defun(L"C:Reactors", 0) == RTNORM)
    ads_regfunc(PrintReactors, 0);
   gpDbReactor = new CMyArcDbReactor();
   acdbCurDwg()->addReactor(gpDbReactor);
   break;
  case AcRx::kUnloadDwgMsg:
   ads_undef(L"C:Reactors", 0);
   if(gpDbReactor && acdbCurDwg())
   {
    acdbCurDwg()->removeReactor(gpDbReactor);
    delete gpDbReactor;
    gpDbReactor = NULL;
   }
   break; 
  default:
   break;
}
 return AcRx::kRetOK;
}
/////////////////////////////////////////////////////
//
// for debugging purposes only
//
//
int PrintReactors()
{
ads_name eNam;
ads_point pt;
 if (ads_entsel(L"\nSelect an entity: ",eNam, pt) != RTNORM)
{
  ads_printf(L"\nError selecting an entity.");
  return 0;
}
AcDbObjectId eId;
 if(acdbGetObjectId(eId, eNam) != Acad::eOk)
{
  ads_alert(L"Error obtaining the object Id.");
  return 0;
}
AcDbEntity* pEnt;
 if(acdbOpenObject(pEnt, eId, AcDb::kForRead) != Acad::eOk)
{
  ads_alert(L"Error opening entity.");
  return 0;
}
ads_printf(L"\nThis is the entity ObjectId: %i\t",
  pEnt->objectId());
AcDbVoidPtrArray* ptrArray = pEnt->reactors();
 if(!ptrArray)
{
  pEnt->close();
  return 0;
}
 int len = ptrArray->length();
ads_printf(L"\nReactor objectId(s) are: \t");
   for(int i=0; i<len; i++)
  ads_printf(L"%i\t",
  acdbPersistentReactorObjectId(ptrArray->at(i)));
  pEnt->close();
  ads_retvoid();
 return 1;
}

