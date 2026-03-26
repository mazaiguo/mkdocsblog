---
title: "readDwgFile Displays DBX CAS 4 When Called From A DBX Module"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - API
  - C++
  - DWG
  - Database
  - Layer
description: "DBX modules, or 'Object Enablers' are designed for for the sole purpose of defining a custom object/entity in ObjectARX.  The module should define ..."
author: Autodesk
---
# readDwgFile Displays DBX CAS 4 When Called From A DBX Module

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/readdwgfile-displays-dbx-cas-4-when-called-from-a-dbx-module.html

## 文章内容

By Gopinath Taget
DBX modules, or 'Object Enablers' are designed for for the sole purpose of defining a custom object/entity in ObjectARX.  The module should define one or more custom object classes that each contain custom members and override the required methods to suit particular purpose.  In general, interacting with external databases or objects in the same database that are not directly related (via ObjectID link) to the custom object is not supported.
The theory is that an entity's definition or behavior should not be dependent on objects outside the database, but just a few key objects in the same database.  For instance, a LINE entity should be fully defined within its module, and its behavior not be dependent on any outside data other than objects such as layer and linetype, whose relationships are established via AcDbObjectId derivatives.  There are, of course, exceptions to this rule but it is important to try to adhere to the protocol.
The only direct workaround for this is to call readDwgFile() from an ARX module.  You can export a global function in the ARX which you can call from the DBX module, assuming it is loaded (test using using Win32 API: GetModuleHandle()).

