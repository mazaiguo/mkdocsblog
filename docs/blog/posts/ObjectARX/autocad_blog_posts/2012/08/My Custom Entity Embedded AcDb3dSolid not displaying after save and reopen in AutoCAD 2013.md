---
title: "My Custom Entity Embedded AcDb3dSolid not displaying after save and reopen in AutoCAD 2013"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - DWG
  - Solid
  - Surface
description: "In AutoCAD 2013 and RealDWG 2013 based applications, ASM based entities (AcDb3dSolid, AcDbRegion, AcDbBody, AcDbSurface and classes derived from it..."
author: Autodesk
---
# My Custom Entity Embedded AcDb3dSolid not displaying after save and reopen in AutoCAD 2013

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/my-custom-entity-embedded-acdb3dsolid-not-displaying-after-save-and-reopen-in-autocad-2013.html

## 文章内容

by Fenton Webb
In AutoCAD 2013 and RealDWG 2013 based applications, ASM based entities (AcDb3dSolid, AcDbRegion, AcDbBody, AcDbSurface and classes derived from it) have their ASM data stored separately from the entity.  ASM based entities without an ObjectId were not saving their ASM data to a file.  For entities added to a BlockTableRecord this isn't a problem since they have ObjectIds.
The problem is with entities embedded within other custom entities; embedded entities do not have ObjectIds.
To address this, we have added a new protocol extension class:
class AcDbEmbeddedASMEntPropsPE : public AcRxObject
{
public:
  ACRX_DECLARE_MEMBERS(AcDbEmbeddedASMEntPropsPE);
  ACDB_PORT virtual void setIsEmbeddedEnt(AcDbObject* pObj, bool bIsEmbedded = true);
};
  This new protocol extension class is only present on the ASM based entity classes.  Custom entities that embed ASM based entities, should use this new protocol extension class to set a flag in the embedded ASM based entities indicating that they are embedded.  During a save, when this flag is set, the ASM data will be saved as part of the ASM based entity as was done prior to the 2013 release.
That takes care of the saving part.  BUT, for reading in, some additional checking must be done to determine if the host application's acdb19.dll has the new protocol extension class.  If it does not, then that host application cannot properly read in the saved data of the embedded ASM based entity, so the custom entity should return an ErrorStatus of Acad::eMakeMeAProxy from its dwgInFields() instead of calling dwgInFields() on the embedded ASM based entity.  This will cause the custom entity to become a proxy and the ASM based entity will remain as an unprocessed data blob within the proxy.
For dxfInFields(), there is no way to force the custom entity to be made a proxy, so the custom entity should return any non-eOk ErrorStatus instead of calling dxfInFields() on the embedded ASM based entity.  This will abort the dxfin operation. Here's a very simple example of a custom entity class with an embedded AcDb3dSolid that has the necessary changes to make use of the new protocol extension:
class EmbeddedSolidWrapper : public AcDbEntity
{
public:
  ACRX_DECLARE_MEMBERS(EmbeddedSolidWrapper);
  EmbeddedSolidWrapper();
  virtual ~EmbeddedSolidWrapper();
  virtual Acad::ErrorStatus   dwgInFields(AcDbDwgFiler* filer);
  virtual Acad::ErrorStatus   dwgOutFields(AcDbDwgFiler* filer) const;
  virtual Adesk::Boolean subWorldDraw(AcGiWorldDraw* pWd);
  virtual Acad::ErrorStatus dxfInFields (AcDbDxfFiler* pFiler);
  virtual Acad::ErrorStatus dxfOutFields(AcDbDxfFiler* pFiler) const;
  void initializeSolid()
  {
    if (mpSolid) {
      mpSolid->setDatabaseDefaults();
      mpSolid->createSphere(400);
    }
  }
  static AcDbEmbeddedASMEntPropsPE* getEmbedPE();
private:
  AcDb3dSolid* mpSolid;
};
AcDbEmbeddedASMEntPropsPE* EmbeddedSolidWrapper::getEmbedPE()
{
  static AcDbEmbeddedASMEntPropsPE* pPE = NULL;
  static bool bInit = true;
  // We only need to do this once per session because the protocol extension
  // is loaded at AcDb initialization, so if it isn't already present, it won't
  // be for the rest of the session.
  //
  if (bInit) {
    bInit = false;
    AcRxClass* pCls = AcDb3dSolid::desc();
    // We get the AcDbEmbeddedASMEntityPropsPE AcRxClass object pointer from the
    // dictionary instead of using AcDbEmbeddedASMEntityPropsPE::desc() so that we
    // don't have a dependency on AcDbEmbeddedASMEntityPropsPE::desc() that would
    // prevent loading our app into a host application that does not have the
    // fixed acdb19.dll.
    //
    AcRxClass* pPECls = AcRxClass::cast(acrxClassDictionary->at(L"AcDbEmbeddedASMEntPropsPE"));
    if (pCls && pPECls) {
      pPE = (AcDbEmbeddedASMEntPropsPE*)pCls->queryX(pPECls);
    }
  }
  return pPE;
}
ACRX_DXF_DEFINE_MEMBERS (EmbeddedSolidWrapper,
  AcDbEntity,
  AcDb::kDHL_CURRENT,
  AcDb::kMReleaseCurrent,
  AcDbProxyEntity::kNoOperation,
  EmbeddedSolidWrapper,
  EmbeddedSolidTest);
EmbeddedSolidWrapper::EmbeddedSolidWrapper()
{
  mpSolid = new AcDb3dSolid();
  AcDbEmbeddedASMEntPropsPE* pPE = getEmbedPE();
  if (pPE && mpSolid)
    pPE->setIsEmbeddedEnt(mpSolid);
}
EmbeddedSolidWrapper::~EmbeddedSolidWrapper()
{
  if(mpSolid)
    delete mpSolid;
}
Acad::ErrorStatus EmbeddedSolidWrapper::dwgInFields(AcDbDwgFiler* filer)
{
  if (!mpSolid)
    return Acad::eOutOfMemory;
  // If the embeddedASM protocol extension is not present, then we cannot
  // read in from file because the necessary code is not present in acdb.
  // So, we return the error eMakeMeAProxy to force acdb to make us a proxy
  // and not require reading in the data on a per-class basis.
  //
  if (!getEmbedPE() && filer->filerType() == AcDb::kFileFiler)
    return Acad::eMakeMeProxy;
  assertWriteEnabled();
  Acad::ErrorStatus es = AcDbEntity::dwgInFields(filer);
  if (es != Acad::eOk)
    return es;
  es = mpSolid->dwgInFields(filer);
  return es;
}
Acad::ErrorStatus EmbeddedSolidWrapper::dwgOutFields(AcDbDwgFiler* filer) const
{
  if (!mpSolid)
    return Acad::eOutOfMemory;
  assertReadEnabled();
  Acad::ErrorStatus es = AcDbEntity::dwgOutFields(filer);
  if (es != Acad::eOk)
    return es;
  es = mpSolid->dwgOutFields(filer);
  return es;
}
Acad::ErrorStatus EmbeddedSolidWrapper::dxfInFields (AcDbDxfFiler* filer)\
{
  if (!mpSolid)
    return Acad::eOutOfMemory;
  // If the embeddedASM protocol extension is not present, then we cannot
  // read in from file because the necessary code is not present in acdb.
  // So, we return an error.  Unfortunately, we can't get dxf to turn us
  // into a proxy - any return other than eOk will just cause the dxf to
  // be aborted.
  //
  if (!getEmbedPE()) {
    filer->setError(Acad::eMissingDxfField, L"Missing necessary ASM protocol extension");
    return Acad::eInvalidContext;
  }
  assertWriteEnabled();
  Acad::ErrorStatus es = AcDbEntity::dxfInFields(filer);
  if (es != Acad::eOk)
    return es;
  if (filer->atEmbeddedObjectStart())
    mpSolid->dxfInFields(filer);
  else
    filer->setError(Acad::eMissingDxfField, L"Missing expected embeddedObject marker");
  return filer->filerStatus();
}
Acad::ErrorStatus EmbeddedSolidWrapper::dxfOutFields(AcDbDxfFiler* filer) const
{
  if (!mpSolid)
    return Acad::eOutOfMemory;
  assertReadEnabled();
  Acad::ErrorStatus es = AcDbEntity::dxfOutFields(filer);
  if (es != Acad::eOk)
    return es;
  filer->writeEmbeddedObjectStart();
  return mpSolid->dxfOutFields(filer);
}
Adesk::Boolean EmbeddedSolidWrapper::subWorldDraw(AcGiWorldDraw* pWd)
{
  pWd->geometry().draw(mpSolid);
  return Adesk::kTrue;
}
void creatCustomEnt()
{
  // If we don't have the necessary support to save the ASM data,
  // then don't allow creatining one of our entities.
  //
  if (!EmbeddedSolidWrapper::getEmbedPE())
    return;
  EmbeddedSolidWrapper* pTestSolid = new EmbeddedSolidWrapper();
  pTestSolid->initializeSolid();
  AcDbBlockTable* pBlockTable = NULL;
  Acad::ErrorStatus es = acdbHostApplicationServices()->workingDatabase()->getBlockTable(pBlockTable, AcDb::kForRead);
  if (es != Acad::eOk)
    return;
  AcDbBlockTableRecord* pRecord = NULL;
  es = pBlockTable->getAt(ACDB_MODEL_SPACE, pRecord, AcDb::kForWrite);
  if (es != Acad::eOk)
    return;
  pBlockTable->close();
  AcDbObjectId retId;
  es = pRecord->appendAcDbEntity(retId, pTestSolid);
  pRecord->close();
  if (es != Acad::eOk) {
    return;
  }
  pTestSolid->close();
}

## 评论

**内容**: Loic Jourdan said...
Issue fixed before I get it!
more than efficient,
thank you
Reply
08/28/2012 at 04:26 AM

---
**内容**: RasmusB said...
Thanks a lot! Saved my day/week/month...I was afraid I had introduced a serious dwg filing bug into my project after upgrading it to 2013, although no error statuses suggested that this was the case. Please update the docs!
Reply
12/05/2012 at 12:03 AM

---
**内容**: sonev said...
Hi, I don't understand one thing. Part about wrapper is OK, but I don't understand where should I define that new protocol extension class (AcDbEmbeddedASMEntPropsPE)or is it already defined in acdb19.dll, because in version of my acdb19 I don't have that class.
Thank you
Reply
03/25/2013 at 12:58 AM

---
**内容**: Fenton Webb said...
Hey Sonev!
yeah, you need the 2013 sp installed to see the new API...
Reply
03/25/2013 at 08:48 AM

---
**内容**: sonev said...
Hi,
Thank you for help. It worked great with AutoCad 2013.
Now I have problem with AutoCad 2014. I created and saved file with my entity that contains AcDb3dSolid. Then program failed when I tried to open that file, when AcDb3dSolid::dwgInFields was called. Of course, I use EmbeddedSolidWrapper like before, and AcDb3dSolid::dwgOutFields returnd eOK during save. Everything is OK for AutoCad 2013, but it doesnt work for AutoCad 2014, so I woluld just like to know is anything changed for AutoCad 2014?
Reply
04/11/2013 at 05:25 AM

---
**内容**: Fenton Webb said...
Try this
http://usa.autodesk.com/getdoc/id=DL21484847
Reply
04/11/2013 at 09:00 AM

---
**内容**: sonev said...
Great, it solved problem. Thanks a lot.
Reply
04/11/2013 at 11:16 PM

---
**内容**: Knigus said...
EmbeddedSolidWrapper are not included in viewbase command.
It is possibly to fix that?
Reply
05/14/2014 at 12:18 PM

---
**内容**: Knigus said...
Is anyone able to help with the following problem?
I have custom object derived from AcDbEntity. Custom object has embedded AcDb3dSolid. I would like to use the embedded solid with viewbase command to generate 2D drawings.
How can I achieve that?
Reply
05/15/2014 at 03:39 PM

---
**内容**: Madhukar Moogala said in reply to Knigus...
I'm pretty sure VIEWBASE doesn't support custom objects (even more so for something derived from AcDbEntity). You could implement explode for your custom entity to explode it to an AcDb3dSolid and use VIEWBASE on that.
Reply
05/15/2014 at 07:45 PM

---
**内容**: Knigus said in reply to Madhukar Moogala...
Stephen,
Explode is not a good solution because it require to create new 2d drawings every time I modify 3d model made of custom objects. My current solution is creating in constructor new AcDb3dSolid, adding it to database and store its Id as a class member. Then in modeldraw function I copy the geometry of my embedded AcDb3dSolid to the one store in database. This solution however is not the best because each element is duplicated and users has possibility to delete the duplicated object that can cause a problem. Do you think is there any other solution such as writing command myViewBase that unhide AcDb3dSolids, run viewBase command and finally hide AcDb3dSolids?
Thanks in advance
Reply
05/16/2014 at 02:25 PM

---
**内容**: Michal said in reply to Knigus...
I have similar issue.
Is anyone solved the problem?
Reply
06/12/2014 at 05:15 AM

---
**内容**: Virupaksha Aithal said in reply to Michal...
VIEWBASE does not support embedded solids. Solids need to be in database for VIEWBASE command. So as suggested above, you may have to try exploding custom entity.
Viru
Reply
06/13/2014 at 06:25 AM

---
**内容**: Mike said...
Is this fixed with AutoCAD 2017? I have tried the above fix with a similar situation using a custom entity with embedded region and I cannot figure out what to do with it.
Reply
02/02/2017 at 04:28 AM

---
**内容**: Scott Maness said...
We had an issue exactly like this years ago (where the solid was kept as an AcDb3dSolid* inside of another custom entity), and this solution was just what we needed.
With the introduction of AutoCAD 2018, tho, it seems that somehow AcDb3dSolid entities that are appended to Anonymous blocks somehow lose their ASM data. (Or at this this is what I'm assuming is happening, since there is no way that I know of for a 3rd party developer to determine if the ASM data is there or not.) What I can say is this - we have drawings that are coming back from customers which have no 3D representations any longer. Looking through one of their drawings I discovered that the anonymous blocks that contain AcDb3dSolid entities are still present (along with the expected AcDb3dSolid entities themselves), everything is filing in and out as expected, yet AcDb3dSolids do not have geometry. (I verified this by opening them up and calling getGeomExtents on them. Everything I get back from that call is basically zeros).
I've never seen anything like this before. And it seems to be happening only to entities that our app added to the drawing, yet there is nothing in the app to clear out geometries. (In fact I don't even know of a way to clear AcDb3dSolid objects of their geometric information without deleting them entirely and replacing them with empty solids, which to my knowledge we don't do).
Any ideas why ASM data would disappear like that on entities appended to an anonymous block?
Reply
08/14/2017 at 10:03 AM

---
**内容**: Fenton Webb said in reply to Scott Maness...
Best to create a sample app with reproducible steps, then send to us for debugging...
Reply
08/22/2017 at 03:40 PM

---
**内容**: Rob said...
It should be emphasized that setIsEmbeddedEnt must be called on the embedded entity(s) both
1) Before the entity is written out to the DWG/DXF file
2) After the new entity is created but before dwgInFields/dxfInFields is called on the entity.
In our application, the type of the embedded entity is not fixed (it could be AcDbRegion, AcDbLoftedSurface, etc.), and the type is determined by reading in an enum before the object. For this reason the embedded entity can't be created and the embedded flag set in the custom entity constructor, as in the sample code. The flag was being set before writing out the entity, but not on the newly created embedded entity prior to calling dwgInFields. When trying to read a DXF, this would cause a message about an incorrect field in the DXF file. For a DWG, the program would take OVER A MINUTE PER EMBEDDED ENTITY trying to read the file, and then the import would fail anyway.
Reply
12/18/2018 at 01:43 PM

---
**内容**: Rob said...
On a related note, if in the sample code you replace the embedded AcDbSolid with an AcDbLoftedSurface (I just created a simple one between 2 skew lines), the saving and loading from a DWG works fine, but trying to save to a DXF causes an exception (Access violation reading location) during the call to dxfOutFields on the embedded entity. Has anyone else run into this?
Reply
12/18/2018 at 03:04 PM

---
