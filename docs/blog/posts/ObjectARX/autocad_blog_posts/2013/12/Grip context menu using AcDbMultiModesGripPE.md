---
title: "Grip context menu using AcDbMultiModesGripPE"
date: 2013-12-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Unicode
description: "Here is a sample project that implements a grip context menu for a custom entity using the AcDbMultiModesGripPE. It demonstrates the use of multi-m..."
author: Autodesk
---
# Grip context menu using AcDbMultiModesGripPE

发布日期: 2013-12-01

原始链接: https://adndevblog.typepad.com/autocad/2013/12/grip-context-menu-using-acdbmultimodesgrippe.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample project that implements a grip context menu for a custom entity using the AcDbMultiModesGripPE. It demonstrates the use of multi-mode grips to acquire inputs that is relevant to the custom entity.
To make it fun, I have created a custom entity that resembles a tree. Its grip context menu displays two modes - "Spring" and "Winter". After the tree custom entity is created, the context menu will appear when the grip turns warm. Selecting "Spring" will ensure that the tree has leaves and selecting "Winter" will make the tree shed its leaves.
In this case, the modes are not relevant to grip editing and since we do not want the grip to start dragging when clicked, the action type of the modes are set as command. After the mode is selected, the command gets invoked by AutoCAD. In the command implementation, we ensure that the tree updates its display based on the mode that was selected. I would have liked to have a check mark next to the current mode, but the API does not have a way to do that at present and we have a wish-list item created for it with our engineering team.
Here is the relevant code and the complete sample project can be downloaded from the link below :
// Header
// TreeMultiModesGripPE.h
  #pragma once
  #include "dbMultiModesGrip.h"
  class AdskTreeMultiModesGripPE : public AcDbMultiModesGripPE
{
private:
    static AcDbMultiModesGripPE::GripMode _currentGripMode;
    static AcDbObjectId _lastModifiedEntId;
  public:
    ACRX_DECLARE_MEMBERS(AdskTreeMultiModesGripPE);
      AdskTreeMultiModesGripPE();
    ~AdskTreeMultiModesGripPE();
    static AcDbObjectId getLastModifiedEntId();
      virtual bool getGripModes(AcDbEntity* pThis,
                              AcDbGripData* pGripData,
                              AcArray<GripMode>& modes,
                              unsigned int& curMode) const;
      virtual unsigned int mode(AcDbEntity* pThis,
                              AcDbGripData* pGripData) const;
      virtual AcDbMultiModesGripPE::GripMode modeEx(
                AcDbEntity* pThis,
                AcDbGripData* pGripData) const;
      virtual bool setMode(
                AcDbEntity* pThis,
                AcDbGripData* pGripData,
                unsigned int newMode);
      virtual AcDbMultiModesGripPE::GripType gripType(
            AcDbEntity* pThis, AcDbGripData* pGripData) const;
      virtual void reset(AcDbEntity* pThis);
};
    // Implementation
// TreeMultiModesGripPE.cpp
  #include "StdAfx.h"
#include "dbMultiModesGrip.h"
#include "TreeMultiModesGripPE.h"
#include "AdskTree.h"
  ACRX_CONS_DEFINE_MEMBERS(AdskTreeMultiModesGripPE,
                         AcDbMultiModesGripPE, 1);
  AcDbMultiModesGripPE::GripMode
                    AdskTreeMultiModesGripPE::_currentGripMode;
  AcDbObjectId AdskTreeMultiModesGripPE::_lastModifiedEntId
                                        = AcDbObjectId::kNull;
  AdskTreeMultiModesGripPE::AdskTreeMultiModesGripPE()
{
    // Default grip mode
    _currentGripMode.Mode = 0;
    _currentGripMode.DisplayString = AcString("Spring");
}
  AdskTreeMultiModesGripPE::~AdskTreeMultiModesGripPE()
{
}
  // Returns the possible grip modes
bool AdskTreeMultiModesGripPE::getGripModes(
                                AcDbEntity* pThis,
                                AcDbGripData* pGripData,
                                AcArray<GripMode>& modes,
                                unsigned int& curMode) const
{
    GripMode gripMode1;
    gripMode1.Mode = 0;
    gripMode1.DisplayString = AcString("Spring");
    gripMode1.ActionType = GripActionType::kCommand;
    gripMode1.CommandString = AcString("ModeSwitchCmd ");
      modes.append(gripMode1);
      GripMode gripMode2;
    gripMode2.Mode = 1;
    gripMode2.DisplayString = AcString("Winter");
    gripMode2.ActionType = GripActionType::kCommand;
    gripMode2.CommandString = AcString("ModeSwitchCmd ");
      modes.append(gripMode2);
      curMode = 0;
      return true;
}
  // Gets the current mode identifier.
unsigned int AdskTreeMultiModesGripPE::mode(
                                AcDbEntity* pThis,
                                AcDbGripData* pGripData) const
{
    return _currentGripMode.Mode;
}
  // Return the current mode.
AcDbMultiModesGripPE::GripMode
    AdskTreeMultiModesGripPE::modeEx(
            AcDbEntity* pThis, AcDbGripData* pGripData) const
{
    return _currentGripMode;
}
  // Sets the current mode.
bool AdskTreeMultiModesGripPE::setMode(
            AcDbEntity* pThis,
            AcDbGripData* pGripData,
            unsigned int newMode)
{
    _currentGripMode.Mode = newMode;
      AcDbObjectId entId = pThis->id();
    AdskTree *pTree = AdskTree::cast(pThis);
      switch(newMode)
    {
        case 0:
            acutPrintf(ACRX_T("\nSpring season, growing leaves !"));
              _currentGripMode.DisplayString = AcString("Spring");
            pTree->setSeason(AcString("Spring"));
            // For graphics update
            _lastModifiedEntId = pTree->id();
              break;
          case 1:
            acutPrintf(ACRX_T("\nWinter season, shedding leaves !"));
              _currentGripMode.DisplayString = AcString("Winter");
            pTree->setSeason(AcString("Winter"));
            // For graphics update
            _lastModifiedEntId = pTree->id();
              break;
    }
    return true;
}
  // Gets the grip type of a given grip.
AcDbMultiModesGripPE::GripType
AdskTreeMultiModesGripPE::gripType(
            AcDbEntity* pThis, AcDbGripData* pGripData) const
{
    return AcDbMultiModesGripPE::GripType::kPrimary; 
}
  // To retrieve the objectId of the tree entity
// for graphics update
AcDbObjectId AdskTreeMultiModesGripPE::getLastModifiedEntId()
{
    return _lastModifiedEntId;
}
  // resets current mode to default
void AdskTreeMultiModesGripPE::reset(AcDbEntity* pThis)
{
    _currentGripMode.Mode = 0;
    _currentGripMode.DisplayString = AcString("Spring");
}
      // Header for custom entity
// AsdkTree.h
  #pragma once
  #ifdef MULTIMODEGRIPSIMPLESAMPLE_MODULE
#define DLLIMPEXP __declspec(dllexport)
#else
#define DLLIMPEXP
#endif
  //-----------------------------------------------------------------------------
#include "dbmain.h"
  //-----------------------------------------------------------------------------
class DLLIMPEXP AdskTree : public AcDbEntity
{
  public:
    ACRX_DECLARE_MEMBERS(AdskTree) ;
  protected:
    static Adesk::UInt32 kCurrentVersionNumber ;
  private:
    AcGePoint3d _basePoint;
    AcString _season;
      void BuildSubTree(
        AcGeLineSeg3d *pMainBranch,
        int level,
        AcGiWorldDraw *mode,
        Adesk::Boolean flower = Adesk::kFalse);
  public:
    AdskTree () ;
    virtual ~AdskTree () ;
      // Sets the season status
    void setSeason(AcString season);
      // Sets the insertion point
    void setBasePoint(AcGePoint3d basePoint);
      //----- AcDbObject protocols
    //- Dwg Filing protocol
    virtual Acad::ErrorStatus
                    dwgOutFields (AcDbDwgFiler *pFiler) const ;
    virtual Acad::ErrorStatus
                        dwgInFields (AcDbDwgFiler *pFiler) ;
      //----- AcDbEntity protocols
    //- Graphics protocol
protected:
    virtual Adesk::Boolean subWorldDraw (AcGiWorldDraw *mode) ;
    virtual Acad::ErrorStatus
                    subTransformBy(const AcGeMatrix3d& xform);
      //- Grip points protocol
    virtual Acad::ErrorStatus subGetGripPoints (
                                AcDbGripDataPtrArray &grips,
                                const double curViewUnitSize,
                                const int gripSize,
                                const AcGeVector3d &curViewDir,
                                const int bitflags) const ;
      virtual Acad::ErrorStatus subMoveGripPointsAt (
        const AcDbVoidPtrArray &gripAppData,
        const AcGeVector3d &offset, const int bitflags) ;
};
  #ifdef MULTIMODEGRIPSIMPLESAMPLE_MODULE
ACDB_REGISTER_OBJECT_ENTRY_AUTO(AdskTree)
#endif
    // Implementation of the custom entity
// AdskTree.cpp
  #include "StdAfx.h"
#include "AdskTree.h"
  Adesk::UInt32 AdskTree::kCurrentVersionNumber =1 ;
  ACRX_DXF_DEFINE_MEMBERS (
    AdskTree, AcDbEntity,
    AcDb::kDHL_CURRENT, AcDb::kMReleaseCurrent,
    AcDbProxyEntity::kNoOperation, ADSKTREE,
ADSKMULTIMODEGRIPSIMPLESAMPLEAPP
|Product Desc:     A description for your object
|Company:          Your company name
|WEB Address:      Your company WEB site address
)
  AdskTree::AdskTree () : AcDbEntity ()
{
    _basePoint = AcGePoint3d::kOrigin;
    _season = AcString("Spring");
}
  AdskTree::~AdskTree ()
{
}
  //----- AcDbObject protocols
//- Dwg Filing protocol
Acad::ErrorStatus AdskTree::dwgOutFields(AcDbDwgFiler *pFiler)
                                                    const {
    assertReadEnabled () ;
    //----- Save parent class information first.
    Acad::ErrorStatus es =AcDbEntity::dwgOutFields (pFiler) ;
    if ( es != Acad::eOk )
        return (es) ;
    //----- Object version number needs to be saved first
    if ( (es =pFiler->writeUInt32
            (AdskTree::kCurrentVersionNumber)) != Acad::eOk )
        return (es) ;
      //----- Output params
    pFiler->writePoint3d(_basePoint);
      return (pFiler->filerStatus ()) ;
}
  Acad::ErrorStatus AdskTree::dwgInFields(AcDbDwgFiler *pFiler)
{
    assertWriteEnabled () ;
    //----- Read parent class information first.
    Acad::ErrorStatus es =AcDbEntity::dwgInFields (pFiler) ;
    if ( es != Acad::eOk )
        return (es) ;
    //----- Object version number needs to be read first
    Adesk::UInt32 version =0 ;
    if ( (es =pFiler->readUInt32 (&version)) != Acad::eOk )
        return (es) ;
    if ( version > AdskTree::kCurrentVersionNumber )
        return (Acad::eMakeMeProxy) ;
      //----- Read params
    pFiler->readPoint3d(&_basePoint);
      return (pFiler->filerStatus ()) ;
}
    //----- AcDbEntity protocols
Adesk::Boolean AdskTree::subWorldDraw (AcGiWorldDraw *mode)
{
    assertReadEnabled () ;
      AcGeLineSeg3d mainBranch(
        _basePoint,
        AcGePoint3d(_basePoint.x,_basePoint.y+10.0,_basePoint.z));
      AcDbLine *pLine1 = new AcDbLine(
            mainBranch.startPoint(), mainBranch.endPoint());
    mode->geometry().draw(pLine1);
    delete pLine1;
      int level = 0;
    BuildSubTree(&mainBranch, level, mode);
      return (AcDbEntity::subWorldDraw (mode)) ;
}
  void AdskTree::setBasePoint(AcGePoint3d basePoint)
{
    _basePoint = basePoint;
}
  void AdskTree::setSeason(AcString season)
{
    _season = season;
}
  void AdskTree::BuildSubTree(AcGeLineSeg3d *pMainBranch,
                            int level,
                            AcGiWorldDraw *mode,
                            Adesk::Boolean flower)
{
    if(mode->isDragging() && level >= 2)
        return; // Light weight for dragging
      if(level >= 3)
    {
        if(_season == AcString("Spring"))
        {
            AcDbCircle *pLeaf = new AcDbCircle(
                pMainBranch->endPoint(),
                AcGeVector3d::kZAxis,
                pMainBranch->length() * 0.2);
              if(flower)
                pLeaf->setColorIndex(1);
            else
                pLeaf->setColorIndex(2);
            mode->geometry().draw(pLeaf);
            delete pLeaf;
        }
        return;
    }
      int subLevel = level + 1;
    AcGePoint3d sp = AcGePoint3d::kOrigin;
    AcGePoint3d ep = AcGePoint3d::kOrigin;
    AcGeInterval intrvl;
    pMainBranch->getInterval(intrvl, sp, ep);
    double len = pMainBranch->length();
      AcGePoint3dArray pts;
    pMainBranch->getSamplePoints(5, pts);
      const double PI = 3.1415926535897932385;
    int cnt = 1;
    if(level == 0)
        cnt = 2;
    for(;cnt < 5; cnt++)
    {
        AcGeVector3d dir = pMainBranch->direction().normalize();
        AcGePoint3d refPt1 = pts[cnt];
          if(cnt == 4)
        {
            AcGePoint3d refPt2 = refPt1 + (len * 0.5) * dir;
              AcGeLineSeg3d branch1(refPt1, refPt2);
            AcDbLine *pBranchLine1 = new AcDbLine(refPt1, refPt2);
            mode->geometry().draw(pBranchLine1);
            delete pBranchLine1;
            BuildSubTree(&branch1, subLevel, mode, Adesk::kTrue);
        }
        else
        {
            AcGePoint3d refPt2 = refPt1 +
                (len * 0.5) * dir.transformBy(
                AcGeMatrix3d::rotation(    PI * 0.25,
                                        AcGeVector3d::kZAxis,
                                        refPt1
                                       ));
              AcGeLineSeg3d branch1(refPt1, refPt2);
            AcDbLine *pBranchLine1 = new AcDbLine(refPt1, refPt2);
            mode->geometry().draw(pBranchLine1);
            delete pBranchLine1;
            BuildSubTree(&branch1, subLevel, mode);
              dir = pMainBranch->direction().normalize();
            refPt2 = refPt1 + (len * 0.5) *
                dir.transformBy(AcGeMatrix3d::rotation(
                -PI * 0.25, AcGeVector3d::kZAxis, refPt1));
              AcGeLineSeg3d branch2(refPt1, refPt2);
            AcDbLine *pBranchLine2 = new AcDbLine(refPt1, refPt2);
            mode->geometry().draw(pBranchLine2);
            delete pBranchLine2;
            BuildSubTree(&branch2, subLevel, mode);
        }
    }
}
  Acad::ErrorStatus AdskTree::subGetGripPoints (
    AcDbGripDataPtrArray &grips,
    const double curViewUnitSize,
    const int gripSize, 
    const AcGeVector3d &curViewDir,
    const int bitflags ) const
{
    assertReadEnabled () ;
      AcDbGripData *pGripData = new AcDbGripData();
    pGripData->setGripPoint(_basePoint);
    grips.append(pGripData);
      return Acad::eOk;
}
  Acad::ErrorStatus AdskTree::subMoveGripPointsAt (
    const AcDbVoidPtrArray &gripAppData,
    const AcGeVector3d &offset,
    const int bitflags)
{
    assertWriteEnabled () ;
      _basePoint += offset;
      return Acad::eOk;
}
  Acad::ErrorStatus AdskTree::subTransformBy(
                                    const AcGeMatrix3d& xform)
{
    assertWriteEnabled();
    _basePoint.transformBy(xform);
    return (AcDbEntity::subTransformBy(xform));
}
      // acrxEntryPoint.cpp
// Usage
  #include "resource.h"
#include "AdskTree.h"
  #include "stdafx.h"
#include "dbMultiModesGrip.h"
#include "TreeMultiModesGripPE.h"
  static AdskTreeMultiModesGripPE *pMyMultiModeGrips = NULL;
  #define szRDS _RXST("Adsk")
  //----- ObjectARX EntryPoint
class CMultiModeGripSimpleSampleApp : public AcRxArxApp {
  public:
    CMultiModeGripSimpleSampleApp () : AcRxArxApp () {}
      virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt) {
        // TODO: Load dependencies here
          // You *must* call On_kInitAppMsg here
        AcRx::AppRetCode retCode
                            =AcRxArxApp::On_kInitAppMsg(pkt) ;
          AdskTreeMultiModesGripPE::rxInit();
        AdskTree::rxInit();
        acrxBuildClassHierarchy();
          // TODO: Add your initialization code here
        if(pMyMultiModeGrips == NULL)
        {
            pMyMultiModeGrips = new AdskTreeMultiModesGripPE();
            AdskTree::desc()->addX(
                                AcDbMultiModesGripPE::desc(),
                                pMyMultiModeGrips);
        }
          return (retCode) ;
    }
      virtual AcRx::AppRetCode On_kUnloadAppMsg (void *pkt) {
        // TODO: Add your code here
          // You *must* call On_kUnloadAppMsg here
        AcRx::AppRetCode retCode
                        = AcRxArxApp::On_kUnloadAppMsg (pkt) ;
          // TODO: Unload dependencies here
        if(pMyMultiModeGrips != NULL)
        {
            delete pMyMultiModeGrips;
            pMyMultiModeGrips = NULL;
        }
        return (retCode) ;
    }
      virtual void RegisterServerComponents () {
    }
        // "Tree" command to create a tree
    static void AdskMultiModeGripSimpleSampleTREE(void)
    {
        ads_point pt;
        if (RTNORM != acedGetPoint(
                    NULL, L"\nSelect tree base point: ", pt))
            return;
          AcGePoint3d insertionPt = asPnt3d( pt );
          AdskTree *pTree = new AdskTree();
        pTree->setDatabaseDefaults();
        pTree->setBasePoint(insertionPt);
        PostToDb(pTree);
    }
      // Add the entity to DB
    static Acad::ErrorStatus PostToDb(AcDbEntity* pEnt)
    {
        AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
        AcDbObjectId objId;
          Acad::ErrorStatus      es;
        AcDbBlockTable*        pBlockTable;
        AcDbBlockTableRecord*  pSpaceRecord;
          pDb->getBlockTable(pBlockTable, AcDb::kForRead);
        pBlockTable->getAt( ACDB_MODEL_SPACE,
                            pSpaceRecord,
                            AcDb::kForWrite);
        es = pSpaceRecord->appendAcDbEntity(objId, pEnt);
        es = pEnt->close();
        es = pSpaceRecord->close();
        es = pBlockTable->close();
          return es;
    }
      // Command to update the graphics after the
    // grip mode was changed.
    // This will ensure a graphics is in sync with the
    // mode selected
    static void AdskMultiModeGripSimpleSampleModeSwitchCmd(void)
    {
        AcDbObjectId entId
            = AdskTreeMultiModesGripPE::getLastModifiedEntId();
          AcApDocument *pActiveDoc
                        = acDocManager->mdiActiveDocument();
        AcDbDatabase *pDb = pActiveDoc->database();
          if(entId.isNull())
            return;
          AcDbEntity* pEnt = NULL;
        acdbOpenAcDbEntity(pEnt, entId, AcDb::kForWrite);
        pEnt->recordGraphicsModified();
        pEnt->close();
        acedUpdateDisplay();
    }
} ;
  //-----------------------------------------------------------------------------
IMPLEMENT_ARX_ENTRYPOINT(CMultiModeGripSimpleSampleApp)
  ACED_ARXCOMMAND_ENTRY_AUTO(CMultiModeGripSimpleSampleApp,
                           AdskMultiModeGripSimpleSample,
                           TREE,
                           TREE,
                           ACRX_CMD_TRANSPARENT,
                           NULL)
ACED_ARXCOMMAND_ENTRY_AUTO(CMultiModeGripSimpleSampleApp,
                           AdskMultiModeGripSimpleSample,
                           ModeSwitchCmd,
                           ModeSwitchCmd,
                           ACRX_CMD_TRANSPARENT,
Download MultiModeGrip_SimpleSample
Here is an image of the "tree" custom entity in the two modes :

