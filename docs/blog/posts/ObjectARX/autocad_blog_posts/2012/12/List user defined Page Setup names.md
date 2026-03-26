---
title: "List user defined Page Setup names"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Plot
description: "User defined page setups are basically plotsettings objects that are stored in the dictionary "ACADPLOTSETTINGS". you can therefore iterate the dic..."
author: Autodesk
---
# List user defined Page Setup names

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/list-user-defined-page-setup-names.html

## 文章内容

By Gopinath Taget
User defined page setups are basically plotsettings objects that are stored in the dictionary "ACAD_PLOTSETTINGS". you can therefore iterate the dictionary for all the user defined page setup objects.
The following code lists all the Page Setup names that appear in the drop down list in "Page Setup Dialog" dialog:
//minimal error checking for code brevity
void fListPageSetup()
{
AcDbDictionary *pPageSetupDict = NULL;
AcDbDictionary *pNOD = NULL;
Acad::ErrorStatus es;
AcDbObject *pObj;
acdbHostApplicationServices()->workingDatabase()->
  getNamedObjectsDictionary(pNOD,AcDb::kForRead);
es = pNOD->getAt(L"ACAD_PLOTSETTINGS",pObj,AcDb::kForRead);
pNOD->close(); //unable to open the dictionary hence return
 if(Acad::eOk != es)return;
pPageSetupDict = AcDbDictionary::cast(pObj);
pObj = NULL;
AcDbDictionaryIterator *pIter;
AcDbPlotSettings *pPS;
 const char *pName;
pIter = pPageSetupDict->newIterator();
 for(;!pIter->done();pIter->next())
{
  pIter->getObject(pObj,AcDb::kForRead);
  pPS = AcDbPlotSettings::cast(pObj);
  pPS->getPlotSettingsName(pName);
  acutPrintf(L"\n-->%s",pName);
  pPS->close();
}
 //close the dictionary
pPageSetupDict->close();
 delete pIter;
}

