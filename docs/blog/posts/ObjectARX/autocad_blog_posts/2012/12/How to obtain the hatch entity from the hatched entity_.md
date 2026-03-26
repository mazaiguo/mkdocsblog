---
title: "How to obtain the hatch entity from the hatched entity?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Hatch
description: "You might wonder, when an entity is hatched, is there is an associative entity created that is the hatch (an AcDbHatch)? And how do I locate this o..."
author: Autodesk
---
# How to obtain the hatch entity from the hatched entity?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-obtain-the-hatch-entity-from-the-hatched-entity.html

## 文章内容

By Gopinath Taget
You might wonder, when an entity is hatched, is there is an associative entity created that is the hatch (an AcDbHatch)? And how do I locate this object?
The way the hatch responds to changes in the entity is through notification. The hatch is actually made a persistent reactor of the entity in the hatch. You can then obtain the hatch entity in this way. The following code sample demonstrates this:
void getHatchEntity()
{
ads_name eName;
ads_point pt;
   if( RTNORM != acedEntSel(_T("\nSelect the entity"), eName, pt ) )
  return;
AcDbObjectId id;
acdbGetObjectId( id, eName );
  AcDbEntity* pEnt;
acdbOpenObject(pEnt, id, AcDb::kForRead );
 if( pEnt == NULL )
  return;
  AcDbHatch* pHatch = NULL;
AcDbVoidPtrArray* pReactors = pEnt->reactors();
 for( int i=0; pHatch == NULL &&
  i<pReactors->length(); i++ ) {
  if( acdbIsPersistentReactor( pReactors->at(i) )) {
   AcDbObjectId id =
    acdbPersistentReactorObjectId( pReactors->at(i));
   acdbOpenObject(pHatch, id, AcDb::kForRead );
  }
}
 if( pHatch != NULL ) {
  pHatch->highlight();
  pHatch->close();
}
pEnt->close();
}

