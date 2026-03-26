---
title: "Acad::eWrongObjectType error with AcDbDictionary::setAt()"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "So what could cause the AcDbDictionary::setAt() to return Acad::eWrongObjectType error?"
author: Autodesk
---
# Acad::eWrongObjectType error with AcDbDictionary::setAt()

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/acadewrongobjecttype-error-with-acdbdictionarysetat.html

## 文章内容

By Gopinath Taget
So what could cause the AcDbDictionary::setAt() to return Acad::eWrongObjectType error?
Unfortunately, this error is not documented for the AcDbDictionary::setAt method but there could be a couple of reasons why you could encounter this error.
If you are adding a custom object to the dictionary, you need to register that class with AutoCAD. If not, this could be the source of error.
In the acrxEntryPoint's kInitAppMsg handler of the application, add:
<custom_object_name here>::rxInit () ;
acrxBuildClassHierarchy () ;
Within the kUnloadAppMsg handler:
deleteAcRxClass (<custom_object_name here>::desc ()) ;
If you adding another object which isn't a custom object, or if you did what is explained above, then it means you are trying to add an object which can't sit into a AcDbDictionary object such as an entity (a graphical object).

