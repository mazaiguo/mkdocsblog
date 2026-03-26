---
title: "Register an application in a database for xdata access"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
description: "Registered applications are stored in the AcDbRegAppTable. You may create a new"
author: Autodesk
---
# Register an application in a database for xdata access

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/register-an-application-in-a-database-for-xdata-access.html

## 文章内容

By Virupaksha Aithal
Registered applications are stored in the AcDbRegAppTable. You may create a new
AcDbRegAppTableRecord with your application name and add it to the AcDbRegAppTable. Below code shows the procedure to add the AcDbRegAppTableRecord to AcDbRegAppTable. Note, below code takes a database as input, which could be a side database too (database which is not opened in AutoCAD editor)
Acad::ErrorStatus registerApp(AcDbDatabase* pDb,
                                    const ACHAR * pAppName)
{
    AcDbRegAppTable* pAppTable = NULL;
    Acad::ErrorStatus es;
      // get the RegAppTable
    if((es = pDb->getRegAppTable(pAppTable,
                            AcDb::kForRead)) != Acad::eOk)
        return es;
      // if RegAppTable has application already - fine
    if(pAppTable->has(pAppName))
    {
        pAppTable->close();
        return Acad::eOk;
    }
      AcDbRegAppTableRecord* pAppTableRecord =
                                new AcDbRegAppTableRecord();
    pAppTableRecord->setName(pAppName);
      pAppTable->upgradeOpen();
    if((es = pAppTable->add(pAppTableRecord)) != Acad::eOk)
    {
        delete pAppTableRecord;
        pAppTable->close();
        return es;
    }
      pAppTableRecord->close();
    pAppTable->close();
    return es;
}

