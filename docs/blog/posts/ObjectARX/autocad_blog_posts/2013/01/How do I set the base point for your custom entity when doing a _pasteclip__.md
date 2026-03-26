---
title: "How do I set the base point for your custom entity when doing a "pasteclip"?"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When you use the "copyclip", then "pasteclip", AutoCAD assumes the insertion point as the bottom left hand corner of the extents of the objects cop..."
author: Autodesk
---
# How do I set the base point for your custom entity when doing a "pasteclip"?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-do-i-set-the-base-point-for-your-custom-entity-when-doing-a-pasteclip.html

## 文章内容

By Gopinath Taget
When you use the "copyclip", then "pasteclip", AutoCAD assumes the insertion point as the bottom left hand corner of the extents of the objects copied, this is as designed and there is no custom entity function that we can override to achieve this.
However, it can be accomplished using reactors. You will need to implement an AcEditorReactor which watches for the commandWillStart() "pasteclip", if the "pasteclip" command is started then set a flag which in turn is watched for in the AcDbEntity::transformBy() function. In the AcDbEntity::transformBy() you can modify the "pasteclip" insertion point of your object.

