---
title: "Create IsoSphereSymbol in Plant3d using ObjectARX"
date: 2012-09-01
categories:
  - Plant 3D
tags:
  - C++
  - DWG
  - Database
  - ObjectARX
  - Plant 3D
description: "Iso symbols are not represented in the project database like other piping model objects. They are “markers” that are only used by the Isometrics fe..."
author: Autodesk
---
# Create IsoSphereSymbol in Plant3d using ObjectARX

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/create-isospheresymbol-in-plant3d-using-objectarx.html

## 文章内容

by Fenton Webb
Iso symbols are not represented in the project database like other piping model objects. They are “markers” that are only used by the Isometrics feature and reside entirely within the DWG file.
Iso symbols are connected to existing fittings via a symbolic ports (not represented in project database) that must be added to the fitting AND to the Isometric symbol itself. No connector entity is involved with symbol connections.
Here is some pseudo code containing additional comments about what needs to be done:        
// ....
// ....
if(Endpoints.size() > 0)
{
  AcPpDb3dIsoSphereSymbol* isSymbol = new AcPpDb3dIsoSphereSymbol();
  isSymbol->setPosition(Endpoints.at(0).getAcGePoint3d());               
    AcDbObjectId curSpace = curDoc()->database()->currentSpaceId();
  AcDbBlockTableRecordPointer curSpace(curSpace, AcDb::kForWrite);
  pBlockTable->getAt(ACDB_MODEL_SPACE, pBlock, AcDb::kForWrite);               
  // TODO:
  // set isSymbol properties
  // setBlockId(), setPosition(), setRadius(), setLayer()
  // add a new symbolic port to
  // 
  AcPp3dPort port;
  port.setIsSymbolic(true);
  port.setPosition(isSymbol->position());
  port.setDirection(AcGeVector3d(0,0,1)); // set direction correctly
  port.setName(L"Symbolic");
  isSymbol->addPort(port);                
  AcDbObjectId isSymbolBlockId;
  int appendConnectorEntryError = pBlock->appendAcDbEntity(isSymbolBlockId, isSymbol);
    // TODO:
  // open the fitting you want to connect to kForWrite; AcPpDb3dPart derived
  //  open fitting denoted by pPart below
  //
    AcPp3dPort port1;
  port1.setIsSymbolic(true);
  AcString symbolicPortName = pPart->generateDynamicPortName(true);
  port1.setName(symbolicPortName.kACharPtr());
  port1.setPosition(pSymbol->position());
  // set direction correctly
  port1.setDirection(AcGeVector3d(0,0,-1));
  // this is the fitting the iso symbol is going to be connected to
    pPart->addPort(port1);    
    isSymbol->close();
    // TODO: use AcPpDb3dConnectionManager to connect iso symbol to fitting
    // port to port1 connection on respective objects

## 评论

**内容**: Albert said...
Hi, I trying to do the this procedure with no success. In my implementation the IsoSphereSymbol is added to the DB as well as the connection. I can save the document, reopen it and read these data via API. But this symbol is invisible (and inaccessible) via plant 3d. could you help me?
Reply
07/20/2015 at 08:09 AM

---
