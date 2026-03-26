---
title: "How to prevent certain entities from being saved to a DWG file using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DWG
  - ObjectARX
description: "If you want to be able to prevent certain entities from being saved out to a DWG file, or rather, exclude certain entities from a DWG Save operatio..."
author: Autodesk
---
# How to prevent certain entities from being saved to a DWG file using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-prevent-certain-entities-from-being-saved-to-a-dwg-file-using-objectarx.html

## 文章内容

by Fenton Webb
If you want to be able to prevent certain entities from being saved out to a DWG file, or rather, exclude certain entities from a DWG Save operation you can use an AcEdEditorReactor to do the job…
Here’s some code which shows how you might do it…
// not MDI aware, use CDocData for MSI document aware global vars
static AcDbObjectIdArray gEntityIdsNotToSave;
// test command
void test()
{
  ads_name ss,ename;
  // select some entities to "not" save
  if (ads_ssget(NULL,NULL,NULL,NULL,ss) != RTNORM)
    return;
    // if the selection was successful
  long len;
  // get the total number of items selected in the selection set
  ads_sslength(ss,&len);
  AcDbObjectId id;
  // now loop through them all
  for (long i=0; i<len; ++i)
  {
    // get the ename from the selection set
    if (ads_ssname(ss, i, ename) != RTNORM)
      continue;
    // now convert the ename to an ObjectARX ObjectId
    if (acdbGetObjectId(id,ename)!=Acad::eOk)
      continue;
      // now remember
    gEntityIdsNotToSave.append(id);
  }
}
  // derive am EditorReactor to hook into the relavant save event
class NoSave : public AcEditorReactor
{
public:
    NoSave()
  {
    acedEditor->addReactor(this);
  }
  ~NoSave()
  {
    acedEditor->removeReactor(this);
  }
    virtual void beginSave(AcDbDatabase* pDwg, const TCHAR* pIntendedName);
  virtual void saveComplete(AcDbDatabase* pDwg, const TCHAR* pActualName);
  void HideEntities(Adesk::Boolean hide)
  {
    // make sure we have some entities to "not" save
    if (gEntityIdsNotToSave.length() == 0)
      return;
      // do a quick check if we are saving the database of interest
    bool bTheOne = gEntityIdsNotToSave[0].database() == pDwg;
    // if not the one
    if (!bTheOne)
      return;
      // otherwise loop our entities and erase them
    for (int i=0; i<gEntityIdsNotToSave.length(); ++i)
    {
      // open eachfor write
      AcDbObjectPointer<AcDbObject> pObj(gEntityIdsNotToSave[i],
        AcDb::kForWrite);
      // make sure it opened ok
      if (pObj.openStatus() == Acad::eOk)
        pObj->erase(hide);
    }
      // make sure that the graphics pipeline is updated
    // because AutoCAD isn't expecting the display list to have
    // changed at this point
    actrTransactionManager->flushGraphics();
    acedUpdateDisplay();
  }
};
  // beginSave:erase the entities in question so they don't get saved
void NoSave::beginSave(AcDbDatabase* pDwg, const TCHAR* pIntendedName)
{
  HideEntities(true);
}
  // saveComplete: restore the entities by un-erasing them
void NoSave::saveComplete(AcDbDatabase* pDwg, const TCHAR* pActualName)
{
  HideEntities(false);
}
  // create global instance of the editor reactor
static NoSave g_noSave;

