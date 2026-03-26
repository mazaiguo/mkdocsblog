---
title: "Using the AcadAppInfo class to read and write registry information"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - ObjectARX
description: "How do I use AcadAppInfo class to read and write registry information?"
author: Autodesk
---
# Using the AcadAppInfo class to read and write registry information

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/using-the-acadappinfo-class-to-read-and-write-registry-information.html

## 文章内容

By Xiaodong Liang
Issue
How do I use AcadAppInfo class to read and write registry information?
Solution
The following code assumes you have loaded POLYSAMP sample into AutoCAD. (You can find POLYSAMP in the ObjectARX  SDK\Samples\entity\). Change the application name in the argument of setAppName() function in order to retrieve your own application's registry information.
You can use RegEdit tool to see the effect this test code on AutoCAD's registry entries.
NOTES:
- You have to create your application-specific command demand loading entries and sub keys and assign correct values as outlined below in the code fragment. Otherwise, an error message will occur when you use the first block of code to retrieve it. This is done in the code segment that follows labeled 'Create application specific command demand load keys and value'.
- An application cannot create a key under HKEY_USERS or HKEY_LOCAL_MACHINE. Refer to the MSDN documentation on RegCreateKeyEx() function for more details.
static void testregisterinfo()
{  
    /////////////////
    // Read registry information of POLYSAMP ARX sample.
   ////////////////////////////////////////////
   AcadAppInfo info ;
    //  Set the application name
   info.setAppName (L"AsdkPolyCAD");  
    //  Read its details from the registry
   assert( Acad::eOk == info.readFromRegistry () ); 
   //  Output application's file path
   acutPrintf(L"The module name is :%s",
                    info.moduleName()); 
       ////////////////////////////////////// /
   // Create application specific command
   // demand load keys and values
   /////////////////////////////////////
   const char pAppRegPath[] =
       "SOFTWARE\\MyComany\\MyProduct\\MyApp\\";
   HKEY rkey;
   DWORD result;
   LONG status = RegCreateKeyEx(
       HKEY_LOCAL_MACHINE,
       (LPCWSTR)pAppRegPath, 0, L"",
       REG_OPTION_NON_VOLATILE,
       KEY_WRITE,
       NULL,
        &rkey,
       &result);
   if (status != ERROR_SUCCESS)
    return;
   MessageBox(NULL,L"dad",L"dad",0);
     HKEY prodKey;
   status = RegCreateKeyEx(rkey,
       L"TestApp1",
       0,
       L"",
       REG_OPTION_NON_VOLATILE,
       KEY_WRITE,
       NULL,
       &prodKey,
       &result);
   RegCloseKey(rkey);
   if (status != ERROR_SUCCESS)
    return;
     HKEY cmdKey;
   status = RegCreateKeyEx(prodKey,
                        L"Commands",
                        0,
                        L"",
                    REG_OPTION_NON_VOLATILE,
                    KEY_WRITE,
                    NULL,
                    &cmdKey,
                    &result);
   if (status == ERROR_SUCCESS) {
    RegSetValueEx(cmdKey,
        L"MyCommand1",
        0,
        REG_SZ,
        (const unsigned char*)"CMD1",
        5);
    RegSetValueEx(cmdKey, L"MyCommand2",
        0,
        REG_SZ,
        (const unsigned char*)"CMD2",
        5);
    RegCloseKey(cmdKey);
   }
   HKEY loaderKey;
   status = RegCreateKeyEx(prodKey,
                    L"Loader",
                    0,
                    L"",
                  REG_OPTION_NON_VOLATILE,
                  KEY_WRITE,
                  NULL,
                  &loaderKey,
                  &result);
     if (status == ERROR_SUCCESS) {
    RegSetValueEx(loaderKey,
        L"MODULE",
        0,
        REG_SZ,
        (const unsigned char*)"C:\\TEMP\\MyApp.ARX",
        sizeof("C:\\TEMP\\MyApp.ARX")+1);
    RegCloseKey(loaderKey);
   }
     HKEY nameKey;
   status = RegCreateKeyEx(prodKey,
                    L"Name",
                    0,
                    L"",
                REG_OPTION_NON_VOLATILE,
                KEY_WRITE,
                NULL,
                &nameKey,
                &result);
   RegCloseKey(prodKey);
   if (status != ERROR_SUCCESS)
    return;
     RegSetValueEx(nameKey,
       L"MyApp Name",
       0,
       REG_SZ,
       (const unsigned char*)"MyCAD", 6);
     RegCloseKey(nameKey);
     //////////////////////////////////////////
   // Write our own registry information.
   /////////////////////////////////////////
   AcadAppInfo info2 ;
   // AppName is under AutoCAD\Applications key.
    //    Set the application name 
   info2.setAppName (L"TestApp1");  
   // just a data string, so whatever doesn't matter.
   info2.setAppDesc(L"My Application Description.");
   // Set loader path.
   info2.setModuleName(L"C:\\TEMP\\MyApp.ARX");
   // specifies when APP should be automatically loaded.
   info2.setLoadReason( AcadApp::LoadReasons(   
                    AcadApp::kOnProxyDetection |
                    AcadApp::kOnCommandInvocation |
                  AcadApp::kOnLoadRequest) );
     assert( Acad::eOk == info2.writeToRegistry() );
  }

## 评论

**内容**: Rod Lucas said...
I think that these registry calgary are great ideas. They really make things so much easier to read. It's one of the simplest ways to view a list of names.
Reply
04/02/2013 at 04:10 PM

---
