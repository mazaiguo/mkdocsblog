---
title: "How to Unload an ActiveX COM Server to load a newer version in the same AutoCAD session"
date: 2012-12-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
description: "We are using in-process ActiveX servers. To use the component, we call GetInterfaceObject(). When developing it, we are changing the code and need ..."
author: Autodesk
---
# How to Unload an ActiveX COM Server to load a newer version in the same AutoCAD session

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-unload-an-activex-com-server-to-load-a-newer-version-in-the-same-autocad-session.html

## 文章内容

by Fenton Webb
Issue
We are using in-process ActiveX servers. To use the component, we call GetInterfaceObject(). When developing it, we are changing the code and need to load newer version, and to save time, preferably within the same AutoCAD session. Sometimes we can load the new version using GetInterfaceObject() with newer version, but other times it fails.
Is there any method to unload the interface object to load newer version of the component?
Solution
The COM unloading mechanism requires that a COM client from "time to time" calls the function CoFreeUnusedLibraries() in order to free up the memory and unload the libraries which are loaded but not used by any client in the system. AutoCAD being a COM client also makes calls to this function but you cannot anticipate the time when this call is being made.
The fact that sometimes you can easily GetInterfaceObject with newer version but sometimes it fails means that the old library is still loaded, and AutoCAD didn't call CoFreeUnusedLibraries() yet.
To solve the problem and unload the old library you only have to make a call to CoFreeUnusedLibraries().
Tip - be sure to check out CoFreeUnusedLibrariesEx() also…

