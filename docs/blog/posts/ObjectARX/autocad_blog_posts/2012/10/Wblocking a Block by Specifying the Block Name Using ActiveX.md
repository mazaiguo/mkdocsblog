---
title: "Wblocking a Block by Specifying the Block Name Using ActiveX"
date: 2012-10-01
categories:
  - AutoCAD VBA
tags:
  - Block
  - COM
  - Selection
  - VBA
description: "Is there a way to WBLOCK a block by specifying the block name using ActiveX?"
author: Autodesk
---
# Wblocking a Block by Specifying the Block Name Using ActiveX

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/wblocking-a-block-by-specifying-the-block-name-using-activex.html

## 文章内容

By Balaji Ramamoorthy
Issue
Is there a way to WBLOCK a block by specifying the block name using ActiveX?
Solution
There is not a method in ActiveX to WBLOCK a block by passing the block name as is done at the command line. A workaround is to pass a selection set which contains the entities of the desired block to the Wblock method. To do this, a selection set is created with the entities contained in the block.
Note: These examples do not include error handling for simplicity.
Here is a VBA example which illustrates the process of wblocking by using a block name:
        Sub TestWblockWithName()
            Dim ss As AcadSelectionSet
            Dim blk As AcadBlock
            Dim i As Integer
            Dim obj() As Object
            Dim blkname As String
              blkname = ThisDrawing.Utility.GetString(True, "Enter block name: ")
            fname = ThisDrawing.Utility.GetString(True, "Enter Wblock file name: ")
            blk = ThisDrawing.Blocks(blkname)
              cnt = blk.Count
            ReDim obj(0 To cnt - 1) As Object
              'Populate an object array with entities of the desired block
            For i = 0 To cnt - 1
                obj(i) = blk(i)
            Next
              'We are using CopyObjects as it replaces the need to insert and then explode the blockreference.
            obj_arr = ThisDrawing.CopyObjects(obj, ThisDrawing.ModelSpace)
              'Create a seleciton set and populate it with the desired entities.
            ss = ThisDrawing.SelectionSets.Add("tt")
            ss.AddItems(obj_arr)
              'Wblock the selection set.
            ThisDrawing.Wblock(fname, ss)
            ss.Delete()
              'Delete those entities that CopyObjects created.
            For Each itm In obj_arr
                itm.Delete()
            Next
        End Sub
Here is a VLisp example :
(defun c:TestWblock ()
  (vl-load-com)
  (setq a_app  (vlax-get-acad-object)
 a_doc  (vla-get-ActiveDocument a_app)
 a_msp  (vla-get-modelspace a_doc)
 a_blks (vla-get-blocks a_doc)
 blknam (getstring t "Enter block name: ")
 fname  (getstring t "Enter Wblock file name: ")
 a_blk  (vla-item a_blks blknam)
 a_sss  (vla-get-SelectionSets a_doc)
 a_ss   (vla-add a_sss "myset")
 i      0
  )
  (setq sa (vlax-make-safearray
      vlax-vbobject
      (cons 0 (- (vla-get-count a_blk) 1))
    )
  )
  (vlax-for itm a_blk
    (vlax-safearray-put-element sa i itm)
    (setq i (1+ i))
  )

  (setq obj_arr (vla-copyobjects a_doc sa a_msp))
  (vla-additems a_ss obj_arr)

  (vla-Wblock a_doc fname a_ss)
  (vla-delete a_ss)
  (foreach itm (vlax-safearray->list (vlax-variant-value obj_arr))
    (vla-delete itm)
  )
  (princ)
)
Posted at 09:49 PM in ActiveX, AutoCAD, Balaji Ramamoorthy, LISP | Permalink

