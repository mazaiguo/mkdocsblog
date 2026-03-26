---
title: "How to add dimension entities to a block object using VBA?"
date: 2013-01-01
categories:
  - AutoCAD VBA
tags:
  - Block
  - Dimension
  - Plugin
  - VBA
description: "The AddDimAligned method of Block object produces incorrect dimension objects. How can I add dimension entities to a Block object?"
author: Autodesk
---
# How to add dimension entities to a block object using VBA?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-add-dimension-entities-to-a-block-object-using-vba.html

## 文章内容

By Daniel Du
Issue
The AddDimAligned method of Block object produces incorrect dimension objects. How can I add dimension entities to a Block object?
Solution
The AddDimAligned method as well as other AddDimxxx methods of adding dimension entities to a Block object results in dimension objects that are incorrect.
This is a known problem. Use the following workaround to add dimension entities to a block object:
1. Create a Dimension entity in model space.
2. Use the CopyObject method to copy the Dimension entity to a Block object.
3. Delete the original Dimension entity from model space.
The following sample code creates a block "test", adds a DimRotated entity to the block, and then inserts the block into model space.
Sub f_SolAddDiminBlocks()
    'Workaround for Adding dimensions to block AutoCAD
     Dim po_rotDim As AcadDimAligned
     Dim po_block As AcadBlock
     Dim pd_ext1(0 To 2) As Double
     Dim pd_ext2(0 To 2) As Double
     Dim pd_lineLoc(0 To 2) As Double
     Dim po_array(0) As Object
 
     pd_ext1(0) = 3 : pd_ext1(1) = 3 : pd_ext1(2) = 0
     pd_ext2(0) = 10 : pd_ext2(1) = 3 : pd_ext2(2) = 0
     pd_lineLoc(0) = 5 : pd_lineLoc(1) = 4 : pd_lineLoc(2) = 0
     'create dimeionsion object
     po_rotDim = ThisDrawing.ModelSpace.AddDimAligned(pd_ext1, pd_ext2,
     pd_lineLoc)
 
     'create a new block by name test
     po_block = ThisDrawing.Blocks.Add(pd_ext1, "test")
     'insert a block reference
     ThisDrawing.ModelSpace.InsertBlock(pd_ext1, "test", 1, 1, 1, 0)
     'copy dimension object
     po_array(0) = po_rotDim
     ThisDrawing.CopyObjects(po_array, po_block)
     po_rotDim.Delete()
     'release the references
     po_block = Nothing
     po_rotDim = Nothing
End Sub

## 评论

**内容**: Rizoff said...
It doesn't works
Reply
04/15/2020 at 11:36 PM

---
