---
title: "Understanding ObjectDBX and RealDWG"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - DWG
  - Database
description: "ObjectARX is the C++ API exposed by AutoCAD. An ObjectARX application can access all the functionality exposed by the ObjectARX API, and listed in ..."
author: Autodesk
---
# Understanding ObjectDBX and RealDWG

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/understanding-objectdbx-and-realdwg.html

## 文章内容

By Augusto Goncalves
ObjectARX is the C++ API exposed by AutoCAD. An ObjectARX application can access all the functionality exposed by the ObjectARX API, and listed in the ObjectARX Reference Guide. This includes accessing AutoCAD specific functionality (e.g. selection set, editor reactor, document manager, plot manager, etc.), or objects in a DWG database (custom entities, standard AutoCAD entities, dictionaries, etc.). An ObjectARX DLL will have a .arx extension.
AutoCAD is a type of RealDWG Host Application - this means that it is an application that can read or write the contents of a DWG file (the DWG database). Other examples of RealDWG Host Applications are the AutoCAD verticals (such as ADT, MDT), AutoCAD LT, Revit, and Inventor.
These applications are created using RealDWG, which is a technology available under license from Autodesk to allow standalone applications to read or write DWG files without the requirement for AutoCAD (for example) to be installed on the user's machine. More details of RealDWG can be found at www.autodesk.com/realdwg
One of the most powerful features of the ObjectARX API is that it allows developers to create their own custom entities that behave in AutoCAD as if they were native entities. The polysamp project in the ObjectARX SDK samples folder is an example of a custom entity.
In order for a RealDWG Host Applications (e.g. Inventor) to be able to correctly display a custom object, it is necessary to create an 'object enabler' or 'ObjectDBX module' for that entity. An object enabler is created using the ObjectARX SDK, but makes use of the subset of ObjectARX functionality that does not depend on accessing AutoCAD editor functionality. (In general, this means deriving from and accessing AcDb classes, but not using selection set, editor reactor, document manager, plot manager, etc.). An object enabler DLL has a .dbx extension.
Object enabler/ObjectDBX modules can link to the following libraries:
acdbXX.lib
AcDbMPolygonXX.lib
acgeXX.lib
acgiapi.lib
achapiXX.lib
acISMobjXX.lib
axdb.lib
rxapi.lib
rxheap.lib
Where XX stand for the major version, e.g. 19 for AutoCAD 2013. Linking to any other ObjectARX library will introduce a dependency on AutoCAD.
Summary
If you are creating an ObjectARX application, or creating a custom object/entity, you should use the ObjectARX SDK. (The ObjectARX Wizard will set up your object enabler project for you).
If you want to read/write a DWG file from your own application with no dependency on AutoCAD, then you should find your local RealDWG sales contact from www.autodesk.com/RealDWG and ask them about licensing.

## 评论

**内容**: EAG said...
Hi there,
you seem to be a specialist for Real DWG.
At the moment we are a bit confused about "Real DWG" and "Inventor DWG" (and so seems Autodesk sometimes).
Techsoft 3D: "RealDWG will read all Autodesk generated DWG files"
Autodesk support: "Inventor DWG is not a Real DWG. You need to export from Inventor to AutoCAD DWG format".
Is it possible to read Inventor DWG with Real DWG API?
Reply
07/21/2014 at 01:20 AM

---
**内容**: passer by said in reply to EAG...
looks like you've been ignored..
Reply
09/29/2015 at 06:10 AM

---
**内容**: Erik Gilsdorf said...
No worries. InventorDWG can be read and modified by RealDWG API.
Reply
09/29/2015 at 06:23 AM

---
