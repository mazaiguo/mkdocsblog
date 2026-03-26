---
title: "Restore Previously Saved UCS Using ObjectARX"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - ObjectARX
  - UCS
description: "The ObjectARX function, acedSetCurrentUCS(), takes an AcGeMatrix3d. This matrix specifies the information about the UCS to set (origin, x-, y- and ..."
author: Autodesk
---
# Restore Previously Saved UCS Using ObjectARX

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/restore-previously-saved-ucs-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
The ObjectARX function, acedSetCurrentUCS(), takes an AcGeMatrix3d. This matrix specifies the information about the UCS to set (origin, x-, y- and z-direction). All you need to do is to get this matrix from a named UCS.
The code below does this task:
ACHAR name[133];
  // Get the UCS name to restore
if (RTNORM != acedGetString(0, ACRX_T("\nUCS to restore: "), name))
    return;
  AcDbDatabase *pDb
            = acdbHostApplicationServices()->workingDatabase();
  AcDbUCSTable *pTable = NULL;
if (Acad::eOk != pDb->getUCSTable(pTable, AcDb::kForRead))
    return;
  // Get the UCS table record knowing its name
AcDbUCSTableRecord *pUCS = NULL;
if (Acad::eOk != pTable->getAt(name, pUCS, AcDb::kForRead))
{
    acutPrintf(ACRX_T("\nCannot get UCS '%s'."), name);
    pTable->close();
    return;
}
pTable->close();
  // Get the UCS parameters
AcGePoint3d origin = pUCS->origin();
AcGeVector3d xDirection = pUCS->xAxis();
AcGeVector3d yDirection = pUCS->yAxis();
AcGeVector3d zDirection = xDirection.crossProduct(yDirection);
pUCS->close();
  // Create the matrix for the UCS
AcGeMatrix3d matrix;
matrix.setCoordSystem(origin, xDirection, yDirection, zDirection);
  // Activate the UCS
acedSetCurrentUCS(matrix);
Note : This solution does not change the UCS name that is displayed by AutoCAD using the UCSNAME system variable.

