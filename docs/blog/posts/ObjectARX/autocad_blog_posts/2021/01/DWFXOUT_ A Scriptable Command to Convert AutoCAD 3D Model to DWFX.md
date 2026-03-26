---
title: "DWFXOUT: A Scriptable Command to Convert AutoCAD 3D Model to DWFX"
date: 2021-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "There is an internal discussion that came up about scripting 3DDWF, the current command 3DDWF invokes a dialog to save the filename of the export m..."
author: Autodesk
---
# DWFXOUT: A Scriptable Command to Convert AutoCAD 3D Model to DWFX

发布日期: 2021-01-01

原始链接: https://adndevblog.typepad.com/autocad/2021/01/dwfxout-a-scriptable-command-to-convert-autocad-3d-model-to-dwfx.html

## 文章内容

There is an internal discussion that came up about scripting 3DDWF, the current command 3DDWF invokes a dialog to save the filename of the export model. The dialogs interrupt automation flow, to bypass and enable automation fluidity, here is the simple scriptable command.
The code employees function pointer (getSymbolAddress ) technique allows retrieving the address of an exported function from the specified dynamic-link library (DLL).
#define PUBLISH_DLL     _T("AcPublish.crx")
#define PUBLISH_SVC _T("AdskPublish")
typedef void (*EXPORT3DDWF)(bool, const ACHAR*, int);
 void dwgoutcli(){
TCHAR fileName[MAX_PATH] = _T("");
int res = acedGetString(1, _T("\nPlease input the DWFX file name: "), fileName);
if (res != RTNORM){
return;
}
bool bCancelled = false;
int isFromCLI = 1;
if (!acrxServiceIsRegistered(PUBLISH_SVC)) {
    if (!acrxDynamicLinker->loadModule(PUBLISH_DLL, false, true))
    return;
    }
// Get the address of the export3dDWF service.
  EXPORT3DDWF pFunc = (EXPORT3DDWF) acrxDynamicLinker->
getSymbolAddress(PUBLISH_SVC, "export3dDWF");
if (pFunc == NULL) {
assert(FALSE);
return;
}
pFunc(bCancelled, fileName, isFromCLI);
}
 Github Source

## 评论

**内容**: pizza tower said...
Nice sharing! The article is useful
Reply
05/18/2023 at 04:26 AM

---
