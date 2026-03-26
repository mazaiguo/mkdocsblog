---
title: "How to turn an ARX Application into a Managed C++ Application?"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "You can directly create a mixed manage project using ObjectARX wizard. The steps below apply to projects which are being migrating from old release..."
author: Autodesk
---
# How to turn an ARX Application into a Managed C++ Application?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-turn-an-arx-application-into-a-managed-c-application.html

## 文章内容

By Philippe Leefsma
You can directly create a mixed manage project using ObjectARX wizard. The steps below apply to projects which are being migrating from old releases or converting a unmanaged ObjectARX project to a mixed managed.
  The first thing to do is to turn on the /CLR compiler setting to compile as managed.
In the project properties window, under the Property Pages for the project, make the following modifications:
C++ :  General:

    Compile As Managed
     From: Not using managed extensions
     To: Assembly Support (/clr)
    Debug Information Format: (Debug only)
    From: Program Database for Edit & Continue (/ZI)
    To: Program Database (/Zi)

Code Generation (Debug only):

   Basic runtime checks
     From: Both (/RTC1, equip, to /RTC Su...)
     To: default
  Precompiled Header:  

    Create/Use Precompiled Header
     From: Automatically Generate (/YX)
     To: Create Precompiled Header (/Yc)
  Code Generation:

    Enable Minimal Rebuild
     From: Yes (/Gm)
     To: No
  Link with the /NOENTRY flag
  In stdafx.h add:
#using <mscorlib.dll>
#using <System.dll>
#using <System.Drawing.dll>
#using <system.windows.forms.dll>
  In the CPP file where you're going to use managed code, add the following after the compiler references through to stdafx.h
using namespace System;
using namespace System::Reflection;
using namespace System::Collections;
using namespace System::ComponentModel;
using namespace System::Drawing;
using namespace System::Windows::Forms;
using namespace System::Security::Policy;
using namespace System::Runtime::InteropServices;
  See attached sample for more details.
ArxDotNetSample.zip

