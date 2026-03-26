---
title: "Changing the application name in XDATA"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The following code changes the name of the registered application listed in the xdata by removing the old xdata and re-appending it with the new ap..."
author: Autodesk
---
# Changing the application name in XDATA

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/changing-the-application-name-in-xdata.html

## 文章内容

By Gopinath Taget
The following code changes the name of the registered application listed in the xdata by removing the old xdata and re-appending it with the new application name. Be aware that this approach will overwrite the xdata if you already have xdata attached to that entity by the application:
AcDbEntity* selectEntity( const TCHAR *prompt, AcDbObjectId& id,
AcGePoint3d& pick, AcDb::OpenMode openMode )
{
AcDbEntity *ent = NULL;
ads_name ename;
 if ( RTNORM == acedEntSel(prompt, ename, (ads_real*)&pick )){
  if ( Acad::eOk == acdbGetObjectId( id, ename )){
   if ( Acad::eOk == acdbOpenAcDbEntity( ent, id, openMode))
    return ent;
  }
}
 return ent;
}
  void renameXdata( const TCHAR *oldName, const TCHAR *newName )
{
AcDbObjectId entId;
AcGePoint3d pick;
AcDbEntity *pEnt = NULL;
 if ( NULL == ( pEnt = selectEntity( _T("\nSelect entity: "),
  entId, pick,
  AcDb::kForRead )))
  return;
 struct resbuf *pRb = pEnt->xData( oldName );
 if ( NULL == pRb )
  acutPrintf( _T("\nEntity has no ")_T("%s")_T(" xdata!"),
  oldName );
 else {
  // Change Xdata name to new name and set it back
  pEnt->upgradeOpen();
  acad_free( pRb->resval.rstring );
  pRb->resval.rstring = acad__strdup( newName );
  acdbRegApp( newName );
  if ( Acad::eOk != pEnt->setXData( pRb ))
   acutPrintf( _T("\nProblem renaming xdata.") );
  else {
   acutPrintf(
    _T("\nRenamed ")_T("%s")_T(" to ")_T("%s")_T("."),
    oldName, newName );
   // Clear old Xdata
   acutRelRb( pRb );
   pRb = acutBuildList( 1001, oldName, RTNONE );
   if ( Acad::eOk != pEnt->setXData( pRb ))
    acutPrintf( _T("\nProblem removing xdata for %s."),
    oldName);
  }
}
pEnt->close();
acutRelRb( pRb );
}

