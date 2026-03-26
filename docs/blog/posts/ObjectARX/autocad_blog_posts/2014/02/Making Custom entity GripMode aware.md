---
title: "Making Custom entity GripMode aware"
date: 2014-02-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "Here is a sample project that implements a custom entity which embeds a Polyline. The custom entity enables GripModes that operate on the embedded ..."
author: Autodesk
---
# Making Custom entity GripMode aware

发布日期: 2014-02-01

原始链接: https://adndevblog.typepad.com/autocad/2014/02/making-custom-entity-gripmode-aware.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample project that implements a custom entity which embeds a Polyline. The custom entity enables GripModes that operate on the embedded entity by making the implementation of "subMoveGripPointsAt" method GripMode aware. In the attached project, the grip modes for the custom entity are same as that of the embedded Polyline, but if your custom entity has multiple embedded entities, you can extend the implementation to expose more GripModes for the custom entity on similar lines.
Here is a portion of the relevant code and the sample project can be downloaded from here : MultiModeGrip_EmbeddedPolyline
//ContainerEntity.h
  // Custom grip app data to identify the grips
class MyGripAppData : public AcDbObject
{
public:
   ACRX_DECLARE_MEMBERS(MyGripAppData) ;
     Adesk::UInt32 m_GripNumber;
     MyGripAppData(){ m_GripNumber = 0; }
     MyGripAppData(int gripNumber){ m_GripNumber = gripNumber; }
};
  // Container custom entity that embeds a polyline
class DLLIMPEXP AdskContainerEntity : public AcDbEntity
{
  public:
    ACRX_DECLARE_MEMBERS(AdskContainerEntity) ;
  protected:
    static Adesk::UInt32 kCurrentVersionNumber ;
  public:
    AdskContainerEntity () ;
    virtual ~AdskContainerEntity () ;
      AcDbPolyline *m_pPolyline; // Embedded Polyline
      // GripMode for use in "subMoveGripPointsAt"
    // which is GripMode aware.
    Adesk::UInt32 m_pCurrentGripMode;
      // To remove or to add after depending on the GripMode
    Adesk::UInt32 m_iVertexNumber;   
      // Coordinates of the new vertex point to
    // add if the GripMode is "Add Vertex"
    AcGePoint2d m_NewVertexCoord;    
  protected:
    virtual Adesk::Boolean subWorldDraw (AcGiWorldDraw *mode) ;
    virtual Acad::ErrorStatus subTransformBy
                                (const AcGeMatrix3d& xform);
      Acad::ErrorStatus dwgInFields (AcDbDwgFiler *pFiler);
    Acad::ErrorStatus dwgOutFields (AcDbDwgFiler *pFiler) const;
      //- Grip points protocol
    virtual Acad::ErrorStatus subGetGripPoints (
                                AcDbGripDataPtrArray &grips,
                                const double curViewUnitSize,
                                const int gripSize,
                                const AcGeVector3d &curViewDir,
                                const int bitflags) const ;
      virtual Acad::ErrorStatus subMoveGripPointsAt(
                            const AcDbVoidPtrArray& gripAppData,
                            const AcGeVector3d& offset,
                            const int bitflags);
};
    // ContainerEntity.cpp : Implementation of AdskContainerEntity
  AdskContainerEntity::AdskContainerEntity () : AcDbEntity ()
{
    m_pPolyline = NULL;
    m_pCurrentGripMode = 0;
    m_iVertexNumber = 0;
}
  AdskContainerEntity::~AdskContainerEntity ()
{
    if (m_pPolyline)
    {
        delete m_pPolyline;
        m_pPolyline = 0;
    }
}
  Acad::ErrorStatus AdskContainerEntity::dwgInFields
                                        (AcDbDwgFiler *pFiler)
{
    assertWriteEnabled () ;
      Acad::ErrorStatus es = AcDbEntity::dwgInFields (pFiler) ;
    if ( es != Acad::eOk )
        return (es) ;
      Adesk::UInt32 version =0 ;
    if ( (es =pFiler->readUInt32 (&version)) != Acad::eOk )
        return (es) ;
      if ( version > AdskContainerEntity::kCurrentVersionNumber)
        return (Acad::eMakeMeProxy) ;
      // Read params
    Adesk::UInt32 numVerts = 0;
    pFiler->readUInt32(&numVerts);
      AcGePoint3dArray points;
    for(int i = 0; i < numVerts; i++)
    {
        AcGePoint3d pt;
        pFiler->readPoint3d(&pt);
        points.append(pt);
    }
      if (m_pPolyline)
    {
        delete m_pPolyline;
        m_pPolyline = 0;
    }
      m_pPolyline = new AcDbPolyline(numVerts);        
    m_pPolyline->setDatabaseDefaults();
      for(int i = 0; i < numVerts; i++)
    {
        AcGePoint3d pt(points[i]);
        m_pPolyline->addVertexAt(i, AcGePoint2d(pt.x, pt.y));
    }
      return (pFiler->filerStatus ()) ;
}
    Acad::ErrorStatus AdskContainerEntity::dwgOutFields
                                (AcDbDwgFiler *pFiler) const
{
    assertReadEnabled () ;
      Acad::ErrorStatus es = AcDbEntity::dwgOutFields (pFiler) ;
    if ( es != Acad::eOk )
        return (es) ;
      if ( (es =pFiler->writeUInt32
        (AdskContainerEntity::kCurrentVersionNumber))
                                                != Acad::eOk )
        return (es) ;
      // Output params
    if(m_pPolyline)
    {
        Adesk::UInt32 numVerts = m_pPolyline->numVerts();
          pFiler->writeUInt32(numVerts);
          for(int i = 0; i < numVerts; i++)
        {
            AcGePoint3d pt;
            m_pPolyline->getPointAt(i, pt);
            pFiler->writePoint3d(pt);
        }
    }
      return (pFiler->filerStatus ()) ;
}
  Adesk::Boolean AdskContainerEntity::subWorldDraw
                                        (AcGiWorldDraw *mode)
{
    assertReadEnabled () ;
      // Draw the polyline
    if(m_pPolyline)
        mode->geometry().pline (*m_pPolyline);
      return (AcDbEntity::subWorldDraw (mode)) ;
}
  Acad::ErrorStatus AdskContainerEntity::subGetGripPoints(
                     AcDbGripDataPtrArray &grips,
                     const double curViewUnitSize,
                     const int gripSize, 
                     const AcGeVector3d &curViewDir,
                     const int bitflags ) const
{
    assertReadEnabled () ;
      // Return the vertices of the embedded polyline as
    // grip points
    if(m_pPolyline)
    {
        Adesk::UInt32 numVerts = m_pPolyline->numVerts();
        for(int i = 0; i < numVerts; i++)
        {
            AcGePoint3d pt;
            m_pPolyline->getPointAt(i, pt);
              AcDbGripData * pGripData = new AcDbGripData();
            pGripData->setAppData(new MyGripAppData(i));
            pGripData->setGripPoint(pt);
            grips.append(pGripData);
        }
    }
    return Acad::eOk;
}
  // Grip mode aware implementation of subMoveGripPointsAt
// Depending on the current grip mode, it stretches / adds or
// removes vertices from the embedded polyline
 Acad::ErrorStatus AdskContainerEntity::subMoveGripPointsAt(
                         const AcDbVoidPtrArray& gripAppData,
                         const AcGeVector3d& offset,
                         const int bitflags)
 {
    assertWriteEnabled () ;
      if(m_pPolyline)
    {
        switch(m_pCurrentGripMode)
        {
            case 0: // Stretch
            {
                for (int i = 0; i < gripAppData.length(); i++)
                {
                    MyGripAppData *pMyGripAppData
                        = static_cast<MyGripAppData *>
                                        (gripAppData.at(i));
                    if(pMyGripAppData != NULL)
                    {
                        int num = pMyGripAppData->m_GripNumber;
                          AcGePoint3d pt;
                        m_pPolyline->getPointAt(num, pt);
                          AcGeMatrix3d mat
                                    = AcGeMatrix3d::kIdentity;
                        mat = mat.translation(offset);
                          pt = pt.transformBy(mat);
                          m_pPolyline->setPointAt(
                                num, AcGePoint2d(pt.x, pt.y));
                    }
                }
                break;
            }
              case 1: // Add Vertex
            {
                m_pPolyline->addVertexAt(
                    m_iVertexNumber+1,
                    AcGePoint2d(m_NewVertexCoord.x,
                                m_NewVertexCoord.y)
                                        );
                  // Reset to default GripMode
                m_pCurrentGripMode = 0;
                break;
            }
              case 2: // Remove Vertex
            {
                if(m_iVertexNumber < m_pPolyline->numVerts())
                    m_pPolyline->removeVertexAt(m_iVertexNumber);
                  // Reset to default GripMode
                m_pCurrentGripMode = 0;
                break;
            }
        }
    }
    return Acad::eOk;
 }
  Acad::ErrorStatus AdskContainerEntity::subTransformBy(const AcGeMatrix3d& xform)
{
    assertWriteEnabled();
      // Transform the polyline
    if(m_pPolyline)
        m_pPolyline->transformBy(xform);
      return (AcDbEntity::subTransformBy(xform));
}
    // ContainerEntityMultiModesGripPE.h
  #include "dbMultiModesGrip.h"
  // GripModePE implementation for the custom entity
// This exposes 3 gripmodes.
// Stretch vertex
// Add Vertex
// Remove Vertex
class AdskContainerEntityMultiModesGripPE : public AcDbMultiModesGripPE
{
private:
    static AcDbMultiModesGripPE::GripMode _currentGripMode;
  public:
    ACRX_DECLARE_MEMBERS(AdskContainerEntityMultiModesGripPE);
      AdskContainerEntityMultiModesGripPE();
    ~AdskContainerEntityMultiModesGripPE();
      static AcDbObjectId getLastModifiedEntId();
    static Adesk::UInt32 getVertexNumberToAdd();
      virtual bool getGripModes(    AcDbEntity* pThis,
                                AcDbGripData* pGripData,
                                AcArray<GripMode>& modes,
                                unsigned int& curMode
                             ) const;
      virtual unsigned int mode(    AcDbEntity* pThis,
                                AcDbGripData* pGripData
                             ) const;
      virtual AcDbMultiModesGripPE::GripMode modeEx(
            AcDbEntity* pThis, AcDbGripData* pGripData) const;
      virtual bool setMode(    AcDbEntity* pThis,
                            AcDbGripData* pGripData,
                            unsigned int newMode);
      virtual AcDbMultiModesGripPE::GripType gripType(
            AcDbEntity* pThis, AcDbGripData* pGripData) const;
      virtual void reset(AcDbEntity* pThis);
};
  // ContainerEntityMultiModesGripPE.cpp
// GripModePE implementation for the custom entity
// This exposes 3 gripmodes.
// Stretch vertex
// Add Vertex
// Remove Vertex
  AdskContainerEntityMultiModesGripPE::
                        AdskContainerEntityMultiModesGripPE()
{
    // Default grip mode : Stretch Vertex
    _currentGripMode.Mode = 0;
    _currentGripMode.DisplayString = AcString("Stretch Vertex");
}
  AdskContainerEntityMultiModesGripPE::
                        ~AdskContainerEntityMultiModesGripPE()
{
}
  // Returns the possible grip modes
// Stretch vertex
// Add Vertex
// Remove Vertex
bool AdskContainerEntityMultiModesGripPE::getGripModes(
                                AcDbEntity* pThis,
                                AcDbGripData* pGripData,
                                AcArray<GripMode>& modes,
                                unsigned int& curMode) const
{
    // "Stretch Vertex" mode
    GripMode gripMode1;
    gripMode1.Mode = 0;
    gripMode1.DisplayString = AcString("Stretch Vertex");
    gripMode1.ActionType = AcDbMultiModesGripPE::kDragOn;
      modes.append(gripMode1);
      // "Add Vertex" mode
    GripMode gripMode2;
    gripMode2.Mode = 1;
    gripMode2.DisplayString = AcString("Add Vertex");
    gripMode2.ActionType = AcDbMultiModesGripPE::kImmediate;
      modes.append(gripMode2);
      // "Remove Vertex" mode to be available only if there are
    // more than 2 vertices in the polyline.
    AdskContainerEntity *pContEnt
                           = AdskContainerEntity::cast(pThis);
    if(pContEnt->m_pPolyline != NULL)
    {
        if(pContEnt->m_pPolyline->numVerts() > 2)
        {
            GripMode gripMode3;
            gripMode3.Mode = 2;
            gripMode3.DisplayString = AcString("Remove Vertex");
            gripMode3.ActionType
                        = AcDbMultiModesGripPE::kImmediate;
              modes.append(gripMode3);
        }
    }
      // "Stretch Vertex" is the current mode
    curMode = 0;
      return true;
}
  // Gets the current mode identifier.
unsigned int AdskContainerEntityMultiModesGripPE::mode(
            AcDbEntity* pThis, AcDbGripData* pGripData) const
{
    return _currentGripMode.Mode;
}
  // Return the current mode.
AcDbMultiModesGripPE::GripMode
AdskContainerEntityMultiModesGripPE::modeEx(
            AcDbEntity* pThis, AcDbGripData* pGripData) const
{
    return _currentGripMode;
}
  // Sets the current mode.
bool AdskContainerEntityMultiModesGripPE::setMode(
                AcDbEntity* pThis,
                AcDbGripData* pGripData, unsigned int newMode)
{
    bool retStatus = true;
      _currentGripMode.Mode = newMode;
      AcDbObjectId entId = pThis->id();
    AdskContainerEntity *pContEnt
                            = AdskContainerEntity::cast(pThis);
    pContEnt->m_pCurrentGripMode = newMode;
      switch(newMode)
    {
        case 0:
        {
            _currentGripMode.DisplayString
                                 = AcString("Stretch Vertex");
            break;
        }
          case 1:
        {
            _currentGripMode.DisplayString
                                     = AcString("Add Vertex");
              // Create a temporary copy of the embedded Polyline for jigging purposes
            AcDbPolyline *pPolyTemp = AcDbPolyline::cast(pContEnt->m_pPolyline->clone());
              MyGripAppData *pMyGripAppData = static_cast<MyGripAppData *>(pGripData->appData());
            if(pMyGripAppData != NULL)
            {
                // Adding vertex requires a Jig
                PolyLineVertexAddJig *pPolyAddVertedJig
                    = new PolyLineVertexAddJig(
                      pPolyTemp, pMyGripAppData->m_GripNumber);
                AcEdJig::DragStatus status = pPolyAddVertedJig->doIt();
                if(status != AcEdJig::kCancel)
                {
                    pContEnt->m_iVertexNumber
                                = pMyGripAppData->m_GripNumber;
                    pContEnt->m_NewVertexCoord
                           = pPolyAddVertedJig->AddedVertex();
                }
                else
                {
                    // Cancel setting the GripMode as the
                    // Jig was canceled
                    retStatus = false;
                }
                  delete pPolyAddVertedJig;
            }
              break;
        }
          case 2:
        {
            _currentGripMode.DisplayString
                                  = AcString("Remove Vertex");
              MyGripAppData *pMyGripAppData
                = static_cast<MyGripAppData *>(
                                        pGripData->appData());
            if(pMyGripAppData != NULL)
            {
                pContEnt->m_iVertexNumber
                               = pMyGripAppData->m_GripNumber;
            }
            break;
        }
    }
      return retStatus;
}
  // Gets the grip type of a given grip.
AcDbMultiModesGripPE::GripType
    AdskContainerEntityMultiModesGripPE::gripType(
            AcDbEntity* pThis, AcDbGripData* pGripData) const
{
    return AcDbMultiModesGripPE::kPrimary; 
}
  // resets current mode to default
void AdskContainerEntityMultiModesGripPE::reset(AcDbEntity* pThis)
{
    _currentGripMode.Mode = 0;
    _currentGripMode.DisplayString = AcString("Stretch Vertex");
}
    // PolyLineVertexAddJig.h
// Polyline jig for adding a new vertex
  class PolyLineVertexAddJig : public AcEdJig
{
public:
    PolyLineVertexAddJig();
    ~PolyLineVertexAddJig();
    PolyLineVertexAddJig(
              AcDbPolyline *pPoly, Adesk::UInt32 vertexToAdd);
      AcEdJig::DragStatus doIt();
    virtual DragStatus sampler();
    virtual Adesk::Boolean update();
      AcGePoint2d AddedVertex();
      virtual AcDbEntity* entity() const;
  private:
    AcDbPolyline *m_pPoly;
    Adesk::UInt32 m_nVertexToAdd;
      AcGePoint3d vertexPointTemp;
    AcGePoint3d vertexPoint;
      Adesk::Boolean addNew;
};
  // PolyLineVertexAddJig.cpp
  #include "StdAfx.h"
#include "PolyLineVertexAddJig.h"
  PolyLineVertexAddJig::PolyLineVertexAddJig()
{
    m_pPoly = NULL;
    vertexPointTemp = AcGePoint3d::kOrigin;
    vertexPoint = AcGePoint3d::kOrigin;
    addNew = Adesk::kTrue;
}
  PolyLineVertexAddJig::PolyLineVertexAddJig(
               AcDbPolyline *pPoly, Adesk::UInt32 vertexToAdd)
{
    // Polyline to jig
    m_pPoly = pPoly;
      // Index to mark the position of the new vertex
    m_nVertexToAdd = vertexToAdd;
      // To keep track of the coordinates during jigging
    vertexPointTemp = AcGePoint3d::kOrigin;
    vertexPoint = AcGePoint3d::kOrigin;
      // To know if we already added a vertex during jigging
    addNew = Adesk::kTrue;
}
  PolyLineVertexAddJig::~PolyLineVertexAddJig()
{
    // Cleanup
    if(m_pPoly)
    {
        delete m_pPoly;
        m_pPoly = NULL;
    }
}
  // Start the jig
AcEdJig::DragStatus PolyLineVertexAddJig::doIt()
{
    AcEdJig::DragStatus stat = AcEdJig::kCancel;
      if(m_pPoly)
    {
        setDispPrompt(ACRX_T("\n Select vertex point : "));
        stat = drag();
    }
      return stat;
}
  AcEdJig::DragStatus PolyLineVertexAddJig::sampler()
{
    DragStatus stat;
    setUserInputControls((UserInputControls)
        (AcEdJig::kAccept3dCoordinates
         | AcEdJig::kNoNegativeResponseAccepted
         | AcEdJig::kNoZeroResponseAccepted));
      // Get a point input for the coordinates
    stat = acquirePoint(vertexPoint);
    if (vertexPointTemp != vertexPoint)
        vertexPointTemp = vertexPoint;
    else if (stat == AcEdJig::kNormal)
        return AcEdJig::kNoChange;
      return stat;
}
  Adesk::Boolean PolyLineVertexAddJig::update()
{
    if(m_pPoly)
    {
        if(addNew)
        {// First time, add a new vertex
            m_pPoly->addVertexAt(
                m_nVertexToAdd+1,
                AcGePoint2d(vertexPoint.x, vertexPoint.y));
        }
        else
        { // Update the coordinates of the
          // previously added vertex
            if(m_nVertexToAdd < m_pPoly->numVerts())
            {
                m_pPoly->setPointAt(
                    m_nVertexToAdd+1,
                    AcGePoint2d(vertexPoint.x, vertexPoint.y));
            }
        }
    }
      if(addNew)
        addNew = Adesk::kFalse;
      return Adesk::kTrue;
}
  AcDbEntity* PolyLineVertexAddJig::entity() const
{
    return m_pPoly;
}
  // To get the coordinates of the vertex added by this jig
AcGePoint2d PolyLineVertexAddJig::AddedVertex()
{
    return AcGePoint2d(vertexPoint.x, vertexPoint.y);
}

## 评论

**内容**: Martin Miller said...
Hello Balaji,
I've been using your simpleSquare sample and this example to update a custom entity I developed over ten years ago. They have been a great a help in this effort. I still have a few wrinkles to iron out though. I have successfully created some custom grips based on this example and they perform as desired. However there is no command line menu like you normally see (and get with the old style grips). So I'm guessing that must be implemented and the functions added to the grip data. Are you aware of any examples of this? My searching has not turned up anything.
Thank You
Martin Miller
Reply
03/22/2016 at 02:19 PM

---
