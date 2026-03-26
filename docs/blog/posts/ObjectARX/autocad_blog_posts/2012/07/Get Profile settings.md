---
title: "Get Profile settings"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - CUI
description: "I'd like to find out what the Current Profile is and get its settings, e.g. the main CUIx file it is using."
author: Autodesk
---
# Get Profile settings

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/get-profile-settings.html

## 文章内容

I'd like to find out what the Current Profile is and get its settings, e.g. the main CUIx file it is using.
Solution
The Current Profile's name can be retrieved from CPROFILE variable and the profile settings can be accessed through the Registry.
static void Command1(void)
{
  // Get current profile's name
    struct resbuf resBuf;
  acedGetVar(_T("CPROFILE"), &resBuf);
  ACHAR profile[MAX_PATH];
  _tcscpy(profile, resBuf.resval.rstring);
  free(resBuf.resval.rstring);
    // Get the profile's CUIx file from the registry
    const ACHAR * regRoot =
    acdbHostApplicationServices()->getRegistryProductRootKey();
    ACHAR keyPath[MAX_PATH];
  _stprintf(keyPath,
    _T("%s\\Profiles\\%s\\General Configuration"), regRoot, profile);
    HKEY key;
  DWORD ret = RegOpenKeyEx(
    HKEY_CURRENT_USER,
    keyPath,
    NULL,
    KEY_READ,
    &key
  );
    if (ret != ERROR_SUCCESS || key == NULL)
    return;
    ACHAR result[MAX_PATH];
  DWORD length = MAX_PATH;
  DWORD keyType;
  ret = RegQueryValueEx(
    key,
    _T("MenuFile"),
    NULL,
    &keyType,
    (LPBYTE)(result),
    &length
  );
  RegCloseKey(key);
    ACHAR menuPath[MAX_PATH];
  ret = ExpandEnvironmentStrings(result, menuPath, MAX_PATH);
    _tcscat(menuPath, _T(".cuix"));
    // Write the result to the Command Line
    acutPrintf(
    _T("The current profile is \"%s\" and its CUIx file is \"%s\""),
    profile,
    menuPath
  );
}
In case of the Current Profile, the MenuFile property is the same as the MENUNAME variable.
static void Command2(void)
{
  // Get main CUIx file
    struct resbuf resBuf;
  acedGetVar(_T("MENUNAME"), &resBuf);
  ACHAR cuiPath[MAX_PATH];
  _stprintf(cuiPath, _T("%s.cuix"), resBuf.resval.rstring);
  free(resBuf.resval.rstring);
    // Write the result to the Command Line
    acutPrintf(
    _T("The CUIx file used by the current profile is \"%s\""),
    cuiPath
  );
}

