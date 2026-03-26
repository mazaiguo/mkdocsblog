---
title: "Making a non database resident copy of a complex object"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - Database
  - ObjectARX
description: "In ObjectARX you can do a non database-resident copy of a single object using the clone() or copyFrom() methods. But these two methods do not opera..."
author: Autodesk
---
# Making a non database resident copy of a complex object

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/making-a-non-database-resident-copy-of-a-complex-object.html

## 文章内容

By Balaji Ramamoorthy
In ObjectARX you can do a non database-resident copy of a single object using the clone() or copyFrom() methods. But these two methods do not operate on complex entities such as an AcDbBlockReference with AcDbAttributes. As is explained in the documentation, the clone() method calls the copyFrom() method that does a shallow clone/copy of the object. In other words, it does not copy the owned objects (AcDbAttribute). There is no direct method available to do this in ObjectARX.
The solution is to copy each object individually and to reattach the newly created attributes with the block-reference object. Be aware of a special case where the block-definition of the block has constant attributes. These attributes are not sub-entities of the block-reference entity, instead they are AcDbAttributeDefinitions in the block table record (the block definition).
If you want a database resident copy of such complex objects, do not use the deepClone() method directly: you should call the AcDbDatabase::deepCloneObjects() method, ensuring the AcDbObjectId of the block-reference is in the array argument. As deepCloneObjects() follows the AcDbHardOwnerShipId and AcDbHardPointerId relationships, the AcDbAttributes will be copied as well.

