---
title: "Entitlement: How To Display Autodesk Sign In Dialog"
date: 2018-04-01
categories:
  - AutoCAD
tags:
  - Entitlement
description: "This is a small post which will be useful by App publishers, in case if user is not logged, app developers can display Autodesk Sign In Dialog."
author: Autodesk
---
# Entitlement: How To Display Autodesk Sign In Dialog

发布日期: 2018-04-01

原始链接: https://adndevblog.typepad.com/autocad/2018/04/entitlement-how-to-display-autodesk-sign-in-dialog.html

## 文章内容

By Madhukar Moogala
This is a small post which will be useful by App publishers, in case if user is not logged, app developers can display Autodesk Sign In Dialog.
bool bIsUserLoggedIn = true;
#define CONNECTTOWEB _T("CONNECTWEBSERVICES")
void onlineUI()
{
 //if user isn't logged, onlineuserid will be empty
 struct resbuf rb;
 acedGetVar(_T("ONLINEUSERID"), &rb);
 if (rb.resval.rstring != NULL) {

  CString userId(rb.resval.rstring);
  if (userId.IsEmpty()) bIsUserLoggedIn = false;
  // Release memory acquired for string:
  free(rb.resval.rstring);
 }
 // pop once only
 if (!bIsUserLoggedIn) {
  // prompt user to login
  // ensure unload-able from ui
  acrxLoadModule(_T("AcConnectWebServices.arx"), false, true);
  acrxLoadModule(_T("AcConnectWebServices.arx"), false, false);

  ASSERT(acrxServiceIsRegistered(CONNECTTOWEB));
  if (acrxServiceIsRegistered(CONNECTTOWEB))
  {
   typedef void(*ADSKLOGIN) ();
   ADSKLOGIN pAdskLogin = (ADSKLOGIN)
    acrxDynamicLinker->getSymbolAddress(CONNECTTOWEB,
     _T("AcConnectWebServicesLogin"));
   ASSERT(pAdskLogin);
   if (pAdskLogin != NULL)
    pAdskLogin();
  }
  acrxUnloadModule(_T("AcConnectWebServices.arx"), false);
 }

}
namespace MgdOnlineUI
{
    public class WebUtils
    {
        [DllImport("AcConnectWebServices.arx", EntryPoint = "AcConnectWebServicesLogin")]
            public static extern bool AcConnectWebServicesLogin();
    }
    public class Class1
    {
        [CommandMethod("ONLINEUI")]
        public void Onlineui()
        {
            //If ONLINEUSERID is empty or null, user is not logged in to system.
            if(String.IsNullOrEmpty((string)Application.GetSystemVariable("ONLINEUSERID")))
            {
                WebUtils.AcConnectWebServicesLogin();
            }
        }
    }
}
via GIPHY

