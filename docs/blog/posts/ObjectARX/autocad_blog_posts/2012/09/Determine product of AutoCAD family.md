---
title: "Determine product of AutoCAD family"
date: 2012-09-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
description: "When I use an ActiveX client application on a computer that has AutoCAD based products installed, I don't know which 'AutoCAD' I am accessing. Is t..."
author: Autodesk
---
# Determine product of AutoCAD family

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/determine-product-of-autocad-family.html

## 文章内容

By Xiaodong Liang
Issue
When I use an ActiveX client application on a computer that has AutoCAD based products installed, I don't know which 'AutoCAD' I am accessing. Is there a way of determining this?
Solution
The following code obtains the running (or creates a new instance if none exists) of AutoCAD. Its version is determined by the registry key.
HKEY_CLASSES_ROOT\AutoCAD.Application
CComQIPtr<IAcadApplication, &IID_IAcadApplication> gpApp;
  HRESULT startAcad()
{
    HRESULT hr = S_OK;
    CLSID clsid;
    //get the current version's CLSID
    hr = CLSIDFromProgID(L"AutoCAD.Application", &clsid);
    if(FAILED(hr))
        return hr;
    CComPtr<IUnknown> pIUnk;
    hr = GetActiveObject(clsid, NULL, &pIUnk);
    if(!pIUnk)
    {
        hr = CoCreateInstance(clsid, NULL, CLSCTX_LOCAL_SERVER,
            IID_IAcadApplication, (void**)&gpApp);
    }
    else
        gpApp = pIUnk;
    if(FAILED(hr) || !gpApp)
        return hr;
    gpApp->put_Visible(VARIANT_TRUE);
    return hr;
}
  Therefore, if CoCreateInstance() on the CLSID we got from CLSIDFromProgID() of "AutoCAD.Application" succeeded, we know AutoCAD is running.
The problem is that all the other family products that have an
AutoCAD engine use the same ProID, "AutoCAD.Application" thus one can't tell which family member receives the client's request.
However, each family product has its own Automation Extension with specific interface progID, and it's this information that determines which AutoCAD based program is running.
For example, once you have the IAcadApplication object, you can call its GetInterfaceObject() method.
IAcadApplication.GetInterfaceObject("AutoCADMap.Application")
  If it succeeded, the application is AutoCAD Map. if GetInterfaceObject("Aecc.Application") succeeded, the application is Architectrual Desktop or Land Development Desktop. if GetInterfaceObject("Mcad.Application") succeeded, the application is Mechanical Desktop.

## 评论

**内容**: Jason said...
I am trying to do something similar in .Net. I want to determine what product my C# code is running in, and also what product authored the current drawing.
Reply
11/27/2012 at 10:39 AM

---
**内容**: Adnan said in reply to Jason...
Did you find solution?
Reply
09/10/2013 at 11:40 PM

---
**内容**: Augusto Goncalves said in reply to Adnan...
Please check this new post: http://adndevblog.typepad.com/infrastructure/2015/03/is-a-civil-3d-instance.html
Regards,
Augusto Goncalves
Reply
03/24/2015 at 10:36 AM

---
