---
title: "Copy a leader using Visual LISP"
date: 2014-03-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Unicode
description: "Recently I had a case where the question was how to create a new leader based on an existing leader using AutoLISP. Here is an example that I came ..."
author: Autodesk
---
# Copy a leader using Visual LISP

发布日期: 2014-03-01

原始链接: https://adndevblog.typepad.com/autocad/2014/03/copy-a-leader-using-visual-lisp.html

## 文章内容

By Wayne Brill
Recently I had a case where the question was how to create a new leader based on an existing leader using AutoLISP. Here is an example that I came up with. When you run this example you select a leader and the MText annotation for the leader. After you run the function you will need to move the Leader manually to see that there are are two leaders at the same location.
Another way to do this would be to use the Copy method and set the annotation property. This example is just getting the points from the existing leader, the MText, and then creating a new Leader at the same location.   
  (defun C:copyLeaderTest (/ vla_ldr vla_mtx coords numberOfPoints
           arrayForPoints points attachPointFromExistingMText
           textForMText widthForMText insertioinPointForMText
           acadObj doc modelSpace newMText
               drawingDirectionForMText newLeader verticalTextPosition)
  (vl-load-com)
  (setvar "osmode" 0)
  (setvar "orthomode" 0)
  ; Get Leader and MText
  (while (setq ss1 (ssget (list (cons -4 "<OR")
    (cons 0 "LEADER") (cons 0 "MTEXT")(cons -4 "OR>"))))
   ; Ensure selection set has two entities
  (if (/= (sslength ss1) 2)
    (alert "Select 1 MText and 1 leader.")
    ; Have a Leader and MText get the ActiveX Object
    (progn
      (if (= (cdr (assoc 0 (entget (ssname ss1 0)))) "LEADER")
    (setq vla_ldr (vlax-ename->vla-object (ssname ss1 0))
          vla_mtx (vlax-ename->vla-object (ssname ss1 1))
    )
    (setq vla_ldr (vlax-ename->vla-object (ssname ss1 1))
          vla_mtx (vlax-ename->vla-object (ssname ss1 0))
    )
      )
         
      ; Get the coordinates from the existing leader
      ; and make an array of doubles
      (setq coords (vlax-get vla_ldr 'Coordinates))
      (setq numberOfPoints (1- (length coords)))
      (setq arrayForPoints (cons 0 numberOfPoints))
      (setq points (vlax-make-safearray vlax-vbDouble
                             arrayForPoints))
      (vlax-safearray-fill points coords)
     
    ; Store the current attachmentpoint of the existing MText 
    (setq attachPointFromExistingMText (vla-get-attachmentpoint vla_mtx))
    ; change the attachmentPoint for existing leader to Top Left
    ; This is will make the insertion point correct for the new MText
    (vla-put-AttachmentPoint vla_mtx acAttachmentPointTopLeft)
   
    (setq textForMText (vla-get-TextString vla_mtx))
    (setq widthForMText (vla-get-width vla_mtx))
    (setq insertioinPointForMText (vla-get-insertionpoint vla_mtx))
    ; Get modelspace and add the new MText
    (setq acadObj (vlax-get-acad-object))
    (setq doc (vla-get-ActiveDocument acadObj))
    (setq modelSpace (vla-get-ModelSpace doc)) 
    (setq newMText (vla-AddMText modelSpace
          insertioinPointForMText widthForMText textForMText))
    (vla-put-AttachmentPoint newMText attachPointFromExistingMText)
    ; make the attachmentPoint what it was
    (vla-put-AttachmentPoint vla_mtx attachPointFromExistingMText)
    (setq drawingDirectionForMText (vla-get-drawingdirection vla_mtx))
    (vla-put-drawingdirection newMText drawingDirectionForMText)
     
    ;; Create the leader object in model space
    (setq newLeader (vla-AddLeader modelSpace points newMText acLineWithArrow))
    (setq verticalTextPosition(vla-get-VerticalTextPosition vla_ldr))
    (vla-put-VerticalTextPosition newLeader verticalTextPosition)
     
    (vla-put-ArrowheadBlock
        newLeader
        (vla-get-ArrowheadBlock vla_ldr)
    )
    (vla-put-layer newLeader (vla-get-layer vla_ldr))
    (vla-put-layer newMText (vla-get-layer vla_mtx))
   ; (vla-Erase vla_ldr)
   ; (vla-Erase vla_mtx)
     )
  )
)
  (princ)
)

