---
title: "Drawing graphics from block table record in a custom entity's worlddraw"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
description: "You can use pushModelTransform() method to transform the graphics that is drawn at the desired location. The following psuedo code shows how to dra..."
author: Autodesk
---
# Drawing graphics from block table record in a custom entity's worlddraw

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/drawing-graphics-from-block-table-record-in-a-custom-entitys-worlddraw.html

## 文章内容

By Virupaksha Aithal
You can use pushModelTransform() method to transform the graphics that is drawn at the desired location. The following psuedo code shows how to draw graphics from a block table record.
//Call this function in the subWorldDraw()
//override of your custom entity
  // Implement a getBlockTableRecordId function that returns
// the id of the block table record you wish to draw
AcDbObjectId btrId = getBlockTableRecordId();
  AcDbBlockTableRecord *pBtr=NULL;
  if(acdbOpenObject(pBtr,btrId,AcDb::kForRead)==Acad::eOk)
{
    //Define you matrix here, currently set to translation
    AcGeMatrix3d mat;
    mat.setToTranslation(AcGeVector3d(10,10,0));
    mode->geometry().pushModelTransform(mat);
    mode->geometry().draw(pBtr);
    // pop the transform matrix
    mode->geometry().popModelTransform();
    pBtr->close();
}

## 评论

**内容**: schuepany said...
Hello Viru,
i have a problem, when a entity is set to invisible in the block,
than all plot style work correct, only plot style old hidden shows the invisible entity.
3d hidden is correct, 3dwireframe is correct.
Reply
01/25/2016 at 02:06 AM

---
