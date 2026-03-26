---
title: "Jig more than one entity with AcEdJig class in ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "The AcEdJig class ﻿﻿only supports the update ﻿﻿﻿﻿of one ﻿﻿entity ﻿﻿at a time. However, there is a useful trick you can use to jig more than one ent..."
author: Autodesk
---
# Jig more than one entity with AcEdJig class in ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/jig-more-than-one-entity-with-acedjig-class-in-objectarx.html

## 文章内容

By Gopinath Taget
The AcEdJig class ﻿﻿only supports the update ﻿﻿﻿﻿of one ﻿﻿entity ﻿﻿at a time. However, there is a useful trick you can use to jig more than one entity in ObjectARX.
To do this, you need to define a custom entity class and use it as a *temporary﻿﻿﻿﻿﻿﻿﻿﻿﻿* jig entity which will be used with to maintain a list of real entities that need to be jigged. You will use this custom entity with your custom AcEdJig class to update your list of Jigged entities. Following this, you simply need to override the *temporary* jig entity's subWorldDraw﻿() and inside it,  you can iterate through ﻿﻿your recorded entities ﻿﻿and call worldDraw() on each. This will give the impression of multiple entity update.
Please find here a sample application (available for download and migrated to use ARX 2013 libraries) which has been written in such a way that it will Jig any number of entities. You can also provide your own input and update functions for entity that is required to be jigged. Here is the relevant source:
Header for Jig custom entity and and custom jig declaration:
#ifndef ASDKMULTIJIG__H
#define ASDKMULTIJIG__H
  #endif // ASDKMULTIJIG__H
  ////////////////////////////////////////////////////////
class asdkEntityList : public AcDbEntity
{
public:
   // constructor
asdkEntityList ();
 // destructor
~asdkEntityList ();
   // flag to indicate that we have
 // assigned some entities to the entity list
 bool m_calledSetEntityList;
   // array of AcDbEntities
AcDbVoidPtrArray m_entities;
     typedef Adesk::Boolean (*updateFunction) (int mode,
  asdkEntityList &entityList);
 // array of update Functions
AcArray<updateFunction> m_updateFuncs;
   // entity input data
AcArray<AcGePoint3d> m_pnts;
   // sets what entities are to be jigged
Acad::ErrorStatus setEntityList(
  const AcDbVoidPtrArray &entities);
   // loop through m_entities and display the data
 virtual Adesk::Boolean subWorldDraw(AcGiWorldDraw *wd);
};
  /////////////////////////////////////////////////////////////
class asdkMultiJig : public AcEdJig
{
public:
 // constructor
asdkMultiJig ();
 // destructor
~asdkMultiJig ();
   // mode of input, starts at 0 then
 // increments until all entities have been
 // input, indexes m_entityList
 int m_mode;
   // class containing the list of entities to jig
asdkEntityList m_entityList;
ads_real m_distance;
AcGePoint3d m_originalPnt;
   typedef AcEdJig::DragStatus
  (*inputFunction) (asdkMultiJig &jig);
 // array of input Functions
AcArray<inputFunction> m_inputFuncs;
   // get the jig data
 virtual AcEdJig::DragStatus sampler();
 // return the jig entity
 virtual AcDbEntity *entity() const;
 // update the sampler data to the jig entity
 virtual Adesk::Boolean update();
 // add the object to the space
AcDbObjectId append(AcDbDatabase *dwg=NULL,
  const ACHAR *requiredSpace = ACDB_MODEL_SPACE);
  private:
};
  Implementation of the custom jig and jig custom entity:
#include "StdAfx.h"
#include "StdArx.h"
  ///////////////////////////////////////////////////////
Acad::ErrorStatus postToDwg (AcDbEntity *pEnt,
AcDbDatabase *pDb=NULL,
 const ACHAR *requiredSpace=ACDB_MODEL_SPACE);
  ///////////////////////////////////////////////////////
// constructor
asdkMultiJig::asdkMultiJig ()
{
m_mode = 0;
m_distance = 0.0;
}
///////////////////////////////////////////////////////
// destructor
asdkMultiJig::~asdkMultiJig ()
{
}
///////////////////////////////////////////////////////
// get the jig data
AcEdJig::DragStatus asdkMultiJig::sampler()
{
 // set the cursor to invisible
setSpecialCursorType(AcEdJig::kInvisible);
   // call the update function
 return ((*this->m_inputFuncs[m_mode])(*this));
}
///////////////////////////////////////////////////////
// return the jig entity
AcDbEntity *asdkMultiJig::entity() const
{
 // check to make sure we called setEntityList
 if (!m_entityList.m_calledSetEntityList)
  AfxMessageBox (L"Error - You must call setEntityList \
  before calling asdkMultiJig::drag()");
   return (const_cast<asdkEntityList *>(&m_entityList));
}
  ///////////////////////////////////////////////////////
// update the sampler data to the jig entity
Adesk::Boolean asdkMultiJig::update()
{
 // call the update function
 return ((*m_entityList.m_updateFuncs[m_mode])
  (m_mode, this->m_entityList));
}
///////////////////////////////////////////////////////
// add the object to the space
AcDbObjectId asdkMultiJig::append(AcDbDatabase *dwg,
 const ACHAR *requiredSpace)
{
 // get the total number of entities registered
 int length = m_entityList.m_entities.length ();
 // loop round the registered
 // entities and add the to the space
 for (int i=0; i<length; ++i)
{
  postToDwg ((AcDbEntity *)m_entityList.m_entities[i],
   dwg, requiredSpace);
}
   // get the id of the first entity drawn
AcDbObjectId id =
  ((AcDbEntity *)m_entityList.m_entities[0])->id ();
   // close the entities added
 for (int i=0; i<length; ++i)
  ((AcDbEntity *)m_entityList.m_entities[i])->close ();
   // return the object id
 return (id);
}
  ///////////////////////////////////////////////////////
// constructor
asdkEntityList::asdkEntityList ()
{
m_calledSetEntityList = false;
}
///////////////////////////////////////////////////////
// destructor
asdkEntityList::~asdkEntityList ()
{
}
///////////////////////////////////////////////////////
// set what entities are to be jigged
Acad::ErrorStatus asdkEntityList::setEntityList (
 const AcDbVoidPtrArray &entities)
{
 // record that we have called this function correctly
m_calledSetEntityList = true;
   // setup our entity list
m_entities = entities;
 // if nothing in there then lets say!
 if (m_entities.length() == 0)
  return Acad::eInvalidInput;
   // setup our point storage
m_pnts.setLogicalLength (m_entities.length());
   // all ok
 return Acad::eOk;
}
///////////////////////////////////////////////////////
Adesk::Boolean asdkEntityList::subWorldDraw (AcGiWorldDraw * wd)
{
 int length = m_entities.length ();
 // loop the number of entities in the entity list
 for (int i=0; i<length; ++i)
{
  // lets get the entity out
  AcDbEntity *ent = (AcDbEntity *)m_entities[i];
  // if ok
  if (ent != NULL)
  {
   // then draw it
   wd->geometry ().draw (ent);
  }
}
   return (Adesk::kTrue);
}
  ///////////////////////////////////////////////////////
// adds an entity to the required space...
// default is current dwg and ACDB_MODEL_SPACE.
Acad::ErrorStatus postToDwg (AcDbEntity *pEnt, AcDbDatabase *pDb,
 const ACHAR *requiredSpace)
{
 // if the default database is to be used
 if (pDb == NULL)
  pDb = acdbHostApplicationServices()->workingDatabase ();
  AcDbBlockTable *blockTable = NULL;
 // get a pointer to the block table
Acad::ErrorStatus es = pDb->getBlockTable (blockTable,
  AcDb::kForRead);
 // if it failed then abort
 if (es != Acad::eOk)
  return (es);
  AcDbBlockTableRecord *blockTableRecord = NULL;
 // now get a pointer to the model space entity records
es = blockTable->getAt (requiredSpace,
  blockTableRecord, AcDb::kForWrite);
 // can close the block table
 // itself as we don't need it anymore
blockTable->close ();
 // if it failed then abort
 if (es != Acad::eOk)
  return (es);
 // otherwise put the entity into the model space
es = blockTableRecord->appendAcDbEntity (pEnt);
 // now close it up
blockTableRecord->close();
   return (es);
}

## 评论

**内容**: Khánh said...
Hi, Can you explain more about this?
typedef Adesk :: Boolean (* updateFunction) (int mode,asdkEntityList & entityList);
  // array of update Functions
AcArray m_updateFuncs;
I don't see any connection between this and subworldDraw function (the mechanism that triggers the update function?)
Reply
02/24/2020 at 06:50 PM

---
