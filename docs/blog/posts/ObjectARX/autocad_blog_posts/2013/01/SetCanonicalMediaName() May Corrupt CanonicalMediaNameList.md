---
title: "SetCanonicalMediaName() May Corrupt CanonicalMediaNameList"
date: 2013-01-01
categories:
  - AutoCAD COM
tags:
  - COM
  - Plot
description: "The string array (in form of AcArray) returned by the AcDbPlotSettingsValidator::canonicalMediaNameList() method gets reset by the call to the AcDb..."
author: Autodesk
---
# SetCanonicalMediaName() May Corrupt CanonicalMediaNameList

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/setcanonicalmedianame-may-corrupt-canonicalmedianamelist.html

## 文章内容

By Gopinath Taget
The string array (in form of AcArray) returned by the AcDbPlotSettingsValidator::canonicalMediaNameList() method gets reset by the call to the AcDbPlotSettingsValidator::setCanonicalMediaName(). Therefore after the first call﻿﻿﻿, if you try to use the string values from the original string array you will find the values are corrupted.
The solution to this problem ﻿﻿﻿is to simply create your own copy of media names out of the AcArray returned by the canonicalMediaNameList().
Also, you can use the ActiveX interfaces. The code below will iterate through all of the canonicalMediaNames and set each one current.
Note: We have found that the PageSizes are corrupted if RefreshPlotDeviceIno is called and "None" is the current plotter. Another issue is the canonicalMediaNames are not returned when the current device is "None". This example returns if "None" is the current setting for the device. Here is the function from the attached project:
void fTest()
{
IAcadApplication *pApp =
  (IAcadApplication *)acedGetAcadWinApp()->GetIDispatch(TRUE);
IAcadDocument *pDoc = NULL;
pApp->get_ActiveDocument(&pDoc);
  IAcadLayout *pLay = NULL;
pDoc->get_ActiveLayout(&pLay);
   // check if "None" is the current device
BSTR deviceName;
 const ACHAR* nameCheck = L"None";
pLay->get_ConfigName(&deviceName);
 if (*nameCheck == *(ACHAR *)(_bstr_t)deviceName){
  acutPrintf(
  L"\nCurrent Plotter is \"None\" select \
   a device and try again\n");
  // uncomment this and the page sizes seen in the
  // Plot dialog are very strange
  //pLay->RefreshPlotDeviceInfo();
  return;
}
  pLay->RefreshPlotDeviceInfo();
  _variant_t vGetCanon;
VARIANT vTmp;
VariantInit(&vTmp);
pLay->GetCanonicalMediaNames(&vTmp);
vGetCanon.Attach(vTmp);
   if ((VT_ARRAY | VT_BSTR) != vGetCanon.vt) return;
  BSTR sCanonName;
acutPrintf(L"\nCanonical Media Names:");
 for(long nCtr = 0;
  nCtr < vGetCanon.parray->rgsabound->cElements;
  nCtr++)
{
  SafeArrayGetElement(vGetCanon.parray,&nCtr,&sCanonName);
  acutPrintf(L"\n%d) %s",nCtr,(ACHAR *)(_bstr_t)sCanonName);
  pLay->put_CanonicalMediaName(sCanonName);
}
  pDoc->Release();
pLay->Release();
pApp->Release();
}

