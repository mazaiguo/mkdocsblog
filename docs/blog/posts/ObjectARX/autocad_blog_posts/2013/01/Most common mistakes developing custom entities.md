---
title: "Most common mistakes developing custom entities"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - DXF
description: "Please check the most common errors made from developers while creating custom"
author: Autodesk
---
# Most common mistakes developing custom entities

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/most-common-mistakes-developing-custom-entities.html

## 文章内容

By Augusto Goncalves
Please check the most common errors made from developers while creating custom
objects/entities
Do you use appropriate macros ACRX_DECLARE_MEMBERS / ACRX_DXF_DEFINE_MEMBERS ?
From cut and paste of other source code you may declare a wrong parent object in ACRX_DXF_DEFINE_MEMBERS. e.g. a custom class may be derived from AcDbEntity but in the macro AcDbObject is written.
Do you initialize the custom classes while your ObjectDBX module is loaded ?
MyClass::rxInit();
acrxBuildClassHierarchy();

Unregister custom classes
Make also sure that you unregister your class if you unload your application deleteAcRxClass(MyClass::desc()). Otherwise you may encounter a crash later on.
Read/write permissions on dwgIn/OutFields
Do you call assertWriteEnabled() in dwgInFields and assertReadEnabled() in
dwgOutFields first?
Do you call dwgIn/OutFields of the correct parent object ?
If you have a member variable declared as "int" make sure that you write it out
as Adesk::UIntXX or declare your integer variable as such, otherwise will be written on other format, as shown below:
int m_mumber;
pFiler->writeItem(m_number) // will be written as boolean

When cut/copy and paste code, check that you don't write out an address.

double m_value;
dwgInFields(AcDbDwgFiler *pFiler)
...
pFiler->(&m_value)
dwgOutFields(AcDbDwgFiler *pFiler)
...
pFiler->(&m_value) // copied from dwgInFields - remove & operator

A function which you override is not called?
Check that you use the correct syntax. e.g. explode() is defined as
Acad::ErrorStatus explode(AcDbVoidPtrArray& entitySet) const
if you miss the const declaration your explode() function will not be called.
Please consider an extra member variable which stores the version of your object.
You might get problems later on if you have to expand the member variables of your custom entity.

