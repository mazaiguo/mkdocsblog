---
title: "AutoCAD developer update for 2024"
date: 2023-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "The AutoCAD Developer Center has been updated with the following:"
author: Autodesk
---
# AutoCAD developer update for 2024

发布日期: 2023-06-01

原始链接: https://adndevblog.typepad.com/autocad/2023/06/autocad-developer-update-for-2024.html

## 文章内容

By Sreeparna Mandal
The AutoCAD Developer Center has been updated with the following:
Wizards
ObjectARX 2024 Wizard
AutoCAD 2024 .NET Wizard
Training Material
ObjectARX 2024 Training Labs
AutoCAD 2024 .NET Training Labs
My First AutoCAD Plug-In tutorial for AutoCAD 2024

Important updates for AutoCAD 2024
DWG file format compatibility
No Change

API binary compatibility
Maintained for AutoCAD 2024
AutoCAD 2024 is a binary compatibility release. ObjectARX applications developed for AutoCAD 2021, AutoCAD 2022, or AutoCAD 2023 shouldn't need to be recompiled. Applications developed for AutoCAD 2020 and earlier releases will need to be recompiled.

Development Environment
Visual Studio 2022 v17.2.6
New ObjectARX applications built for AutoCAD 2024 will use VC143 toolset, however applications built with previous toolset VC142 is also compatible with AutoCAD 2024
.NET Framework v4.8

LISP Support for AutoCAD LT
We are enabling end-user LISP support for AutoCAD LT

API changes post ObjectARX 2024 migration

Moved Files in ObjectARX API
class AcCmColor

Deprecated ObjectARX APIs
AcDbGripData::AcDbGripData () Constructor
AcDbGripData::AcDbGripData (AcGePoint3d&, void*, AcRxClass*, GripOperationPtr, GripOperationPtr, GripRtClkHandler, GripWorldDrawPtr, GripViewportDrawPtr, GripOpStatusPtr, GripToolTipPtr, GripDimensionPtr, GripDimensionPtr, unsigned int, AcGePoint3d*, GripInputPointPtr) Constructor

The alternate API to be used instead of the above deprecated API is:
AcDbGripData(const AcGePoint3d&, void* AppData);

Modified structures/API in ObjectARX
AcadApp structure declaration
AcDbAssocTransInfo structure declaration
AcDbMultiModesGripPE::GripMode structure declaration
AcDbMultiModesGripPE::GripMode::ActionType Data Member
AcDbMultiModesGripPE::GripMode::CursorType Data Member
AcDbMultiModesGripPE::GripMode::GripMode Constructor
AcGsKernelDescriptor::hasRequirement Method

For detailed information on Moved/Deprecated/Modified API, refer to the documentations(arxref.chm) in the ObjectARX 2024 SDK

## 评论

**内容**: capybara clicker said...
This is, in my opinion, one of the best posts that you have made. Your work is quite outstanding in both quality and quantity. I am grateful to you for it.
Reply
07/02/2023 at 08:17 PM

---
**内容**: geometry dash said...
These training labs are likely instructional materials and exercises aimed at teaching developers how to use ObjectARX to develop applications for AutoCAD 2024.
Reply
09/12/2023 at 07:33 PM

---
**内容**: mr mine said...
A technology worth looking forward to next year.
Reply
09/12/2023 at 08:35 PM

---
**内容**: pizza tower said...
thanks
Reply
09/13/2023 at 11:50 PM

---
**内容**: foodle said...
This tutorial can be a helpful starting point for developers looking to create their first AutoCAD plugin.
Reply
10/17/2023 at 09:15 PM

---
**内容**: retro bowl college said...
The AutoCAD Developer Center has been updated with the following: Wizards. ObjectARX 2024 Wizard.
Reply
11/02/2023 at 06:41 PM

---
**内容**: driving directions said...
This is an excellent article. This is, in my opinion, one of the best posts ever written. Your work is excellent and inspiring. Thank you very much.
Reply
11/07/2023 at 01:52 AM

---
**内容**: Geometry Dash said...
it symbolizes the spirit of cooperation and ingenuity that defines the future of space exploration.
Reply
02/18/2024 at 07:53 PM

---
**内容**: Ramsey Morgan said...
New ObjectARX applications built for AutoCAD 2024 will use VC143 toolset thank you, PALMY Varsity Jacket
Reply
02/22/2024 at 11:23 AM

---
**内容**: Kinitopet said...
Kinitopet stands as a testament to the power of imagination and innovation in the world of gaming.
Reply
03/17/2024 at 08:52 PM

---
**内容**: Dan said...
we need versions AutoCAD 2025
cheers : )
Reply
06/17/2024 at 05:03 AM

---
**内容**: Texas Outfits said...
"It's amazing how well you can simplify complicated concepts. Without a doubt, I'll use these suggestions. Hollister Red Bull Jacket
Reply
11/08/2024 at 04:05 PM

---
