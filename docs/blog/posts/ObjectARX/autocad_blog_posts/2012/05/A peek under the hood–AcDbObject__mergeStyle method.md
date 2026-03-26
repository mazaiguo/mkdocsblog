---
title: "A peek under the hood–AcDbObject::mergeStyle method"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - XREF
description: "The AcDbObject::mergeStyle method determines the way objects contained in dictionaries are handled during INSERT, XREF/BIND and XREF/INSERT operati..."
author: Autodesk
---
# A peek under the hood–AcDbObject::mergeStyle method

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/a-peek-under-the-hoodacdbobjectmergestyle-method.html

## 文章内容

By Gopinath Taget
The AcDbObject::mergeStyle method determines the way objects contained in dictionaries are handled during INSERT, XREF/BIND and XREF/INSERT operations. The typical return values for this method can be:
kDrcIgnore
kDrcReplace
kDrcMangleName
There are a couple of other return values specific to XRef mangling (kDrcXrefMangleName) and unmangling (kDrcUnmangleName).
The default implementation at AcDbObject level is to return kDrcIgnore, which means that these objects are ignored during merging of dictionaries. There is no way of overruling this behavior at AcDbObject level and there's no public data member or method in AcDbObject that will let you modify the merge style.
However, an application that derives from AcDbObject can freely override the virtual mergeStyle method to return any of the other valid merge styles.
If an object returns AcDb::kDrcReplace, the object will replace an object that is stored under the same key in the target database of an INSERT, XREF/BIND or XREF/INSERT operation. On the other hand, AcDb::kDrcMangleName means that the object will be merged into the existing entries of the target dictionary, creating entries with the $0$ string.
Also, the virtual function 'mergeStyle()' is overridden for the following classes:
AcDbXRecord
AcDbDictionary
AcDbProxyObject
AcDbXrecord and AcDbDictionary store an associated data member that can be set via a call to their new method setMergeStyle() and AcDb::DuplicateRecordCloning).
AcDbProxyObject has the following proxy flags that control the merge style of a proxy object:
kMergeIgnore (the default)
kMergeReplace
kMergeMangleName
These flags can be defined in ACRX_DXF_DEFINE_MEMBERS macro of an entity’s class definition. The value returned by AcDbProxyObject::mergeStyle() depends on these proxy flags.

