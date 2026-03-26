---
title: "Accessing Support Files and Project Files Search Paths"
date: 2015-08-01
categories:
  - AutoCAD COM
tags:
  - API
  - COM
description: "I have received a recent query on how to programmatically accessing support and project files which are available in Options\Files tab."
author: Autodesk
---
# Accessing Support Files and Project Files Search Paths

发布日期: 2015-08-01

原始链接: https://adndevblog.typepad.com/autocad/2015/08/accessing-support-files-and-project-files-search-paths.html

## 文章内容

By Madhukar Moogala
I have received a recent query on how to programmatically accessing support and project files which are available in Options\Files tab.
We can leverage ActiveX API  AcadPreferences.Files to get access on support and project files.
To get information on Support Files Search Path either we can using Acad system variable “ACADPREFIX” or following code:
void TestProj()
{
HRESULT hr;
try
{
  AutoCAD::IAcadApplication *pAcad =NULL;
hr = NOERROR;
LPUNKNOWN pUnk = NULL;
LPDISPATCH pAcadDisp = acedGetIDispatch(TRUE);
if(pAcadDisp==NULL)
return ;
  hr = pAcadDisp->QueryInterface(AutoCAD::IID_IAcadApplication,
                               (void**)&pAcad);
pAcadDisp->Release();
if (FAILED(hr))
return;
  if (pAcad)
{
AutoCAD::IAcadPreferences* pPreferences  = NULL;
hr = pAcad->get_Preferences(&pPreferences);
if(FAILED(hr))  return;
pAcad->Release();
AutoCAD::IAcadPreferencesFiles* pPreferencesFiles = NULL;
hr = pPreferences->get_Files(&pPreferencesFiles);
if(FAILED(hr)) return;
  if(pPreferencesFiles)
{
/*To access Project file path*/
BSTR projectFilePath,supportPath;
/*Created a Testproject interactively and added path to "C:/Temp*/
pPreferencesFiles->GetProjectFilePath(_bstr_t("TESTPROJECT"),
                                      &projectFilePath);
std::wstring ps(projectFilePath,SysStringLen(projectFilePath));
acutPrintf(_T("\nProject Search Path File : %s"),ps.c_str());
  /*To get list of paths in Support Search*/
pPreferencesFiles->get_SupportPath(&supportPath);
std::wstring ws(supportPath,SysStringLen(supportPath));
acutPrintf(_T("\nSupport Search Path : %s"),ws.c_str());
    }
  }
}
catch(...)
{
return;
}
}
Above code only helps to get file path of mentioned Projects created in Applications, there is no API to get list of Projects created in the Application, following is way to read “Project Settings” key from Registry.
The mechanism to read registries is borrowed from here
/*Enumerating List of Projects available*/
#define MAX_KEY_LENGTH 255
#define MAX_VALUE_NAME 16383
void QueryKey(HKEY hKey)
{
TCHAR    achKey[MAX_KEY_LENGTH];   // buffer for subkey name
DWORD    cbName;                   // size of name string
TCHAR    achClass[MAX_PATH] = TEXT("");  // buffer for class name
DWORD    cchClassName = MAX_PATH;  // size of class string
DWORD    cSubKeys = 0;               // number of subkeys
DWORD    cbMaxSubKey;              // longest subkey size
DWORD    cchMaxClass;              // longest class string
DWORD    cValues;              // number of values for key
DWORD    cchMaxValue;          // longest value name
DWORD    cbMaxValueData;       // longest value data
DWORD    cbSecurityDescriptor; // size of security descriptor
FILETIME ftLastWriteTime;      // last write time
  DWORD i, retCode;
  TCHAR  achValue[MAX_VALUE_NAME];
DWORD cchValue = MAX_VALUE_NAME;
  // Get the class name and the value count.
retCode = RegQueryInfoKey(
hKey,                    // key handle
achClass,                // buffer for class name
&cchClassName,           // size of class string
NULL,                    // reserved
&cSubKeys,               // number of subkeys
&cbMaxSubKey,            // longest subkey size
&cchMaxClass,            // longest class string
&cValues,                // number of values for this key
&cchMaxValue,            // longest value name
&cbMaxValueData,         // longest value data
&cbSecurityDescriptor,   // security descriptor
&ftLastWriteTime);       // last write time
  // Enumerate the subkeys, until RegEnumKeyEx fails.
  if (cSubKeys)
{
printf("\nNumber of subkeys: %d\n", cSubKeys);
  for (i = 0; i<cSubKeys; i++)
{
    cbName = MAX_KEY_LENGTH;
    retCode = RegEnumKeyEx(hKey, i,
        achKey,
        &cbName,
        NULL,
        NULL,
        NULL,
        &ftLastWriteTime);
    if (retCode == ERROR_SUCCESS)
    {
        acutPrintf(TEXT("(%d) %s\n"), i + 1, achKey);
    }
}
}
  // Enumerate the key values.
  if (cValues)
{
printf("\nNumber of values: %d\n", cValues);
  for (i = 0, retCode = ERROR_SUCCESS; i<cValues; i++)
{
    cchValue = MAX_VALUE_NAME;
    achValue[0] = '\0';
    retCode = RegEnumValue(hKey, i,
        achValue,
        &cchValue,
        NULL,
        NULL,
        NULL,
        NULL);
      if (retCode == ERROR_SUCCESS)
    {
        acutPrintf(TEXT("(%d) %s\n"), i + 1, achValue);
    }
}
}
}
void TestList()
{
HKEY hTestKey;
/*Hardcoded path, r20.1 is release numberfor ACAD 2016 version
ACAD-F001:409 : Product code for Acad vanilla
*/
/*Full product information, plz refer :
http://adndevblog.typepad.com/autocad/2013/08/registry-values-for-productid-and-localeid-for-autocad.html */
    if (RegOpenKeyEx(HKEY_CURRENT_USER,
TEXT("Software\\Autodesk\\AutoCAD\\R20.1\\ACAD-F001:409\\Profiles\\acad\\Project Settings"),
0,
KEY_READ,
&hTestKey) == ERROR_SUCCESS
)
{
QueryKey(hTestKey);
}
RegCloseKey(hTestKey);
}
Output running following programs:
You may also refer to change path of Project file :
http://adndevblog.typepad.com/autocad/2012/12/setting-the-project-file-search-path.html
Same mechanism is applied to change path of Support file, use
virtual HRESULT __stdcall put_SupportPath (
    /*[in]*/ BSTR orient ) = 0;

