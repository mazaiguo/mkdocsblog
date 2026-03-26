---
title: "AutoCAD 2020: Quick Overview"
date: 2019-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Alert: 32-bit version is no longer available."
author: Autodesk
---
# AutoCAD 2020: Quick Overview

发布日期: 2019-03-01

原始链接: https://adndevblog.typepad.com/autocad/2019/03/autocad-2020-quick-overview.html

## 文章内容

By Madhukar Moogala

Alert: 32-bit version is no longer available.
  

Overview
AutoCAD 2020 provides a set of enhancements based on customer feedback, surveys, and analytic data that prioritize our efforts. Several features are the result of the need to modernize and streamline frequently used features across many customer disciplines.
New Dark Theme
Block Palettes

Purge Dialog box Redesign
DWG Compare Enhancements
Measure Geometry Option–Quick Measure
       
Save to Web & Mobile Enhancements

To get detailed overview on AutoCAD 2020 product I encourage you to follow Autodesk AutoCAD Blog

API Updates:
ObjectARX : No New APIs.
.NET : No New APIs
Activex:
AcadApplication now supports the progIds "AutoCAD.Application.23" and "AutoCAD.Application.23.1" and AcadComparedReference has been added.
The AcadComparedReference object represents the drawing in which you are comparing the current drawing against. AcadComparedReference inherits from the AcadExternalReference object. The following is a basic example how you might go about determining whether an Xref is of the AcadComparedReference type:


' Checks to see if an object is of the ComparedReference type
Sub CheckForComparedReference()
Dim ent As AcadEntity
Dim comRef As AcadComparedReference
On Error Resume Next
' Step through all the objects in model space
For Each ent In ThisDrawing.ModelSpace
' Check to see if the object is a Block Reference
If ent.ObjectName = "AcDbBlockReference" Then
' Try to cast the entity (Block Reference) to a ComparedReference
Set comRef = ent
' If an occurs, then the entity is not a ComparedReference
If Err <> 0 Then
MsgBox "Not a Compared Reference"
Else
MsgBox "Xref Name: " + comRef.Name + vbLf + "Compared Reference"
End If
' Clear the Error object
Err.Clear
End If
Next ent
End Sub
AutoLISP:
There are no new functions or additions.
Xrefs related to the Drawing Compare feature are known as ComparedReference objects. The following is a basic statement that demonstrates how to return the IsComparedReference property of an external reference to determine whether it’s a ComparedReference object

(getpropertyvalue (car (entsel)) "IsComparedReference")
ObjectARX and Managed .NET
AutoCAD 2020 is a binary compatible release, so ObjectARX and Managed .NET applications built for AutoCAD 2019 should load and function without any problems in AutoCAD 2020. The following configuration is officially supported to develop

ObjectARX and/or Managed .NET applications for AutoCAD 2020:
Microsoft Visual Studio 2017 with Update 2 (version 15.7.5 and earlier)
Microsoft .NET Framework 4.7
Note: The product release value used in the Windows Registry and the ObjectARX API version has been updated from R23.0 to R23.1.
For additional information, refer to the ObjectARX Reference Guide as well as the Readme for the latest changes.

Getting ObjectARX 2020 SDK

Fill up  your details and agree to terms and conditions.
It will take you downloads page.

