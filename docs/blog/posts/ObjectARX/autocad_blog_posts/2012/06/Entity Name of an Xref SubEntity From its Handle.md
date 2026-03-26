---
title: "Entity Name of an Xref SubEntity From its Handle"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
  - XREF
description: "You can't access an xref'd sub-entity by passing its handle.  There could be a conflict with an object in the drawing which already has that handle..."
author: Autodesk
---
# Entity Name of an Xref SubEntity From its Handle

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/entity-name-of-an-xref-subentity-from-its-handle.html

## 文章内容

By Balaji Ramamoorthy
You can't access an xref'd sub-entity by passing its handle.  There could be a conflict with an object in the drawing which already has that handle assigned.  Instead it is necessary to check each block (after verifying that it is an xref) to see if one of its sub-entities' handle matches the handle argument which you passed to the lisp function.  The following examples prompt the user to type in a handle at the command-line, although it could just as easily have been passed in from another program:
;;;This example examines each xref in the blocks collection
;;;for a sub-entity whose handle matches the argument.
;;;Function (Get_XREF_SubEn)
(defun Get_XREF_SubEnt (sHandleID docCurrent / colBlocks isFound objBlk objSub xrDb)
   ;;get the blocks collection
   (setq colBlocks (vla-get-blocks docCurrent))
   (vlax-for objBlk colBlocks
      ;;Is the block an xref?
      (if (and
             (= (vlax-get-property objBlk 'IsXref) :vlax-true)
             (not isFound)
          ) ;and
         (vlax-for objSub objBlk
            ;;Does the sub-entity handle match the
            ;;handle passed to the function?
            (if (and
                   (= (vlax-get-property objSub 'Handle) sHandleID)
                   (not result)
                ) ;and
               ;;Then get the xref database
               (setq isFound T
                     xrDb (vlax-get-property objBlk 'XRefDatabase)
                     ;;Get the vla-object# of the sub-entity
                     result (vlax-invoke-method xrDb 'HandleToObject sHandleID)
               ) ;setq
            )
            (vlax-release-object objSub)
         ) ;vlax-for
      ) ;if
      (vlax-release-object objBlk)
   ) ;vlax-for
   (vlax-release-object colBlocks)
     ;;return value to calling function
   result
) ;Get_XREF_SubEnt
  ;;;Calling function
(defun c:Find_Subents ( / appAcad docActive sHandle objSubEnt result)
   (vl-load-com) ;load ActiveX
   (setq appAcad (vlax-get-acad-object)
         docActive (vla-get-ActiveDocument appAcad)
         sHandle (strcase (getstring "\Enter a handle: "))
   ) ;setq
   ;;call the function
   (setq objSubEnt(Get_XREF_SubEnt sHandle docActive))
   ;;display the result
   (if (/= objSubEnt nil)
   (alert
      (strcat "Handle \"" sHandle "\" = AutoCAD Object: "
              (vlax-get-property objSubEnt 'ObjectName)
      ) ;strcat
   ) ;alert
   )
   ;;release objects from memory
   (vlax-release-object docActive)
   (vlax-release-object appAcad)
) ;c:Find_Subents

