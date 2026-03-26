---
title: "Disabling copy command for certain entities"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "You can disable the AutoCAD COPY command by installing an AcEditorReactor and overriding the beginDeepClone and beginDeepCloneXlation notifications..."
author: Autodesk
---
# Disabling copy command for certain entities

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/disabling-copy-command-for-certain-entities.html

## 文章内容

By Balaji Ramamoorthy
You can disable the AutoCAD COPY command by installing an AcEditorReactor and overriding the beginDeepClone and beginDeepCloneXlation notifications. Inside the beginDeepClone function put the object IDs of the objects that are not to be copied into the ID map. AutoCAD will then treat the objects as if they have already been copied. Then you can remove these fakeIDs during beginDeepCloneXlation.
See the sample code example that shows how any object that you add using DisableCopy command is prevented from being copied by the COPY command. You can re-enable object for COPY-ing using EnableCopy command. Note that the object ids are stored within the editor reactor, so they are persistent only during the given session.
Step 1 : In the header file of your editor reactor :
private:
  AcDbObjectIdArray m_ids;
  public:
    // overrides
    virtual void beginDeepCloneXlation(AcDbIdMapping& x0,
                                       Acad::ErrorStatus* x1);
    virtual void beginDeepClone(AcDbDatabase* pTo,
                                AcDbIdMapping& x0);
      // other custom methods
    Adesk::Boolean addObject(const AcDbObjectId& id);
    Adesk::Boolean removeObject(const AcDbObjectId& id);
Step 2 : In the implementation file of your editor reactor :
//
// Override method implementation
//
void ADSEditorRctr::beginDeepClone(AcDbDatabase* pTo,
                                    AcDbIdMapping& x0)
{
    // Only for Copy Context
    if(AcDb::kDcCopy != x0.deepCloneContext())
        return;
      // Mock up a fake clone: place our ids in the map
    for(int i=0; i<m_ids.length(); i++)
    {
        x0.assign(   
                    AcDbIdPair(   
                                m_ids[i],
                                m_ids[i],
                                Adesk::kTrue,
                                Adesk::kTrue
                              )
                 );
    }
}
//
// Override method implementation
//
void ADSEditorRctr::beginDeepCloneXlation(AcDbIdMapping& x0,
                                           Acad::ErrorStatus* x1)
{
    // Only for Copy Context
    if(AcDb::kDcCopy != x0.deepCloneContext())
        return;
      // Remove them here
    for(int i=0; i<m_ids.length(); i++)
    {
        x0.del(m_ids[i]);
    }
}
//
// Custom method implementation
//
Adesk::Boolean ADSEditorRctr::addObject(const AcDbObjectId& id)
{
    int at;
      if(!m_ids.find(id,at))
    {
        m_ids.append(id);
        return Adesk::kTrue;
    }
      return Adesk::kFalse;
}
//
// Custom method implementation
//
Adesk::Boolean ADSEditorRctr::removeObject(const AcDbObjectId& id)
{
    int at;
      if(m_ids.find(id,at))
    {
        m_ids.removeAt(at);
        return Adesk::kTrue;
    }
      return Adesk::kFalse;
}
Step 3 : Add commands to enable/disable the copy for certain entities :
// DISABLECOPY command
static void DISABLECOPY(void)
{
    ads_name ss;
      if(acedSSGet(NULL,NULL,NULL,NULL,ss)==RTNORM)
    {
        ads_name ent;
        AcDbObjectId id;
        long length;
        if(acedSSLength(ss, &length)==RTNORM)
        {
            for(int i=0; i<length; i++)
            {
                if(ads_ssname(ss, i, ent)==RTNORM)
                {
                    if(acdbGetObjectId(id,ent) == Acad::eOk)
                        DocVars.docData().gEditorRctr.addObject(id);
                }
            }
        }
    }
    acedSSFree(ss);
}
  // ENABLECOPY command
static void ENABLECOPY(void)
{
    ads_name ss;
      if(acedSSGet(NULL,NULL,NULL,NULL,ss)==RTNORM)
    {
        ads_name ent;
        AcDbObjectId id;
        long length;
        if(acedSSLength(ss, &length)==RTNORM)
        {
            for(int i=0; i<length; i++)
            {
                if(ads_ssname(ss, i, ent)==RTNORM)
                {
                    if(acdbGetObjectId(id,ent) == Acad::eOk)
                        DocVars.docData().gEditorRctr.removeObject(id);
                }
            }
        }
    }
    acedSSFree(ss);
}
Step 4 : Add an instance of the Editor reactor class to the CDocData class:
public:
    // Editor reactor
    ADSEditorRctr gEditorRctr;

