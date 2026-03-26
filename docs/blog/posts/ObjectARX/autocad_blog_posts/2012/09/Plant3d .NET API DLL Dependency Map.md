---
title: "Plant3d .NET API DLL Dependency Map"
date: 2012-09-01
categories:
  - Plant 3D
tags:
  - .NET
  - API
  - Plant 3D
description: "I was looking into the DLL dependency list of the Plant3d 2013 .NET API and thought you guys might need to refer to it also, so I have posted it he..."
author: Autodesk
---
# Plant3d .NET API DLL Dependency Map

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/plant3d-net-api-dll-dependency-map.html

## 文章内容

by Fenton Webb
I was looking into the DLL dependency list of the Plant3d 2013 .NET API and thought you guys might need to refer to it also, so I have posted it here for you to enjoy!
Acdbmgd
    Depends On
        Microsoft.VisualBasic
        Microsoft.VisualC
        mscorlib
        PresentationCore
        PresentationFramework
        System
        System.Core
        System.Drawing
        System.Xml
        WindowsBase
   
PnIDDwgValidation
    Depends On
        accoremgd
        Acdbmgd
        Acmgd
        AdWindows
        mscorlib
        PnIDmgd
        PnIDMgdInternal
        PnPCommonDbxMgd
        PnPCommonMgd
        PnPCommonUIMgd
        PnPCommonUIMgdCs
        PnPDataLinks
        PnPDataObjects
        PnPHelpHookup
        PnPProjectManagerMgd
        PnPValidation
        System
        System.Core
        System.Drawing
        System.Windows.Forms
   
PnIDmgd
    Depends On
        Acdbmgd
        Microsoft.VisualC
        mscorlib
        PnPCommonDbxMgd
        System
   
PnIDProjectPartsMgd
    Depends On
        Acdbmgd
        mscorlib
        PnIDmgd
        PnPCommonMgd
        PnPDataLinks
        PnPDataObjects
        PnPProjectManagerMgd
        System
        System.Xml
   
PnP3dConnectionManager
    Depends On
        Microsoft.VisualC
        mscorlib
        PnP3dPartsRepository
        PnPCommonMgd
        PnPDataObjects
        System
        System.Xml
   
PnP3dDataLinkManager
    Depends On
        Microsoft.VisualC
        mscorlib
        PnP3dPartsRepository
        PnPDataLinks
        PnPDataObjects
        System
   
PnP3dObjectsMgd
    Depends On
        Acdbmgd
        Microsoft.VisualC
        mscorlib
        PnP3dDataLinkManager
        PnP3dPartsRepository
        PnPDataLinks
        System
   
PnP3dOrthoProjectPart
    Depends On
        accoremgd
        Acdbmgd
        Acmgd
        Autodesk.AutoCAD.Interop
        mscorlib
        PnPDataLinks
        PnPDataObjects
        PnPDwg2dDef
        PnPProjectManagerMgd
   
PnP3dPartsRepository
    Depends On
        mscorlib
        PnPCommonMgd
        PnPDataObjects
        System
        System.Data
        System.Xml
        WindowsBase
   
PnP3dProjectPartsMgd
    Depends On
        accoremgd
        Acdbmgd
        mscorlib
        PnP3dConnectionManager
        PnP3dDataLinkManager
        PnP3dPartsRepository
        PnPCommonDbxMgd
        PnPCommonMgd
        PnPDataLinks
        PnPDataObjects
        PnPProjectManagerMgd
        System
        System.Data
        System.Xml
   
PnPCommonDbxMgd
    Depends On
        Acdbmgd
        Microsoft.VisualC
        mscorlib
        PnPDataLinks
        System
   
PnPCommonMgd
    Depends On
        mscorlib
        PresentationFramework
        System
        System.Windows.Forms
        System.Xml
   
PnPDataLinks
    Depends On
        Acdbmgd
        Microsoft.VisualC
        mscorlib
        PnPCommonMgd
        PnPDataObjects
        System
        System.Data
   
PnPDataObjects
    Depends On
        Microsoft.VisualC
        mscorlib
        PnPCommonMgd
        System
        System.Data
        System.Xml
   
PnPDwg2dAnno
    Depends On
        Acdbmgd
        Microsoft.VisualC
        mscorlib
        PnPCommonDbxMgd
        PnPDataLinks
        PnPDwg2dUtil
        PnPProjectManagerMgd
   
PnPProjectManagerMgd
    Depends On
        accoremgd
        Acdbmgd
        Acmgd
        Autodesk.AutoCAD.Interop
        mscorlib
        PnPCommonDbxMgd
        PnPCommonMgd
        PnPDataLinks
        PnPDataObjects
        PnPSchemaConverter
        System
        System.Drawing
        System.Management
        System.Windows.Forms
        System.Xml
        WindowsBase
   
PnPSQLiteEngine
    Depends On
        Microsoft.VisualC
        mscorlib
        mscorlib
        PnPDataObjects
        System
        System.Data
        System.Data
        System.Data.SQLite
   
PnPValidation
    Depends On
        Acdbmgd
        mscorlib
        System
   
System.Data.SQLite
    Depends On
        mscorlib
        System
        System.Data
        System.Transactions
   
accoremgd
    Depends On
        Acdbmgd
        Microsoft.VisualC
        mscorlib
        PresentationCore
        PresentationFramework
        System
        System.Core
        WindowsBase
   
Acmgd
    Depends On
        accoremgd
        AcCui
        Acdbmgd
        AcDx
        AcMr
        AcTcMgd
        AcWelcomeScreen
        AcWindows
        AdWindows
        Microsoft.VisualC
        mscorlib
        PresentationCore
        PresentationFramework
        System
        System.Core
        System.Data
        System.Drawing
        System.Web
        System.Windows.Forms
        System.Xaml
        WindowsBase

## 评论

**内容**: dave said...
Thank you, Fenton! Do you have some samples to post? I have tried a couple C# examples from the samples folder but none seem to work. Although, they don't error either. :S - I am trying to write out the extended data to a database. I can connect to the db, just not the extended data. If this has no place here please kindly disregard. :)
Reply
09/25/2012 at 10:58 AM

---
**内容**: Fenton Webb said...
Hey Dave
What samples do you want exactly?
Reply
09/25/2012 at 11:38 AM

---
