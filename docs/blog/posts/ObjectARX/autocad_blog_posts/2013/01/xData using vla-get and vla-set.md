---
title: "xData using vla-get and vla-set"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - COM
  - VBA
description: "You can use the (vla-GetXData) and (vla-SetXData) functions. These functions are not documented in the Visual LISP online help."
author: Autodesk
---
# xData using vla-get and vla-set

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/xdata-using-vla-get-and-vla-set.html

## 文章内容

By Augusto Goncalves
You can use the (vla-GetXData) and (vla-SetXData) functions. These functions are not documented in the Visual LISP online help.
To get more information about these functions, look at the function description of GetXData and SetXData in the ACADAUTO.CHM help file (the AutoCAD ActiveX and VBA Reference).
Here is a short description of the functions:
(vla-GetXData entity appName 'codes 'datas)
entity:
This is the entity name of an AutoCAD entity.
appName:
This is a string with the application name. The functions returns all XDatas belonging to the specified application. If appName is "", the functions returns all XDatas attached to 'entity'.
codes:
This list receives the XData group codes.
datas:
This list receives the data of the group codes specified in 'codes'
(vla-SetXData entity codes datas)
entity:
This is the entity name of an AutoCAD entity.
codes:
This list defines the XData group codes.
datas:
This list contains the data for the specified group codes
The following is a sample code which attaches some XData to every entity in model space.After this, it extracts the XData of every entity from every application:
(defun c:setandgetxdatas ()
    (vl-load-com)

  ;; Get objects
  (setq acadApp (vlax-get-acad-object)
        acadDoc (vla-get-ActiveDocument acadApp)
        mspace (vla-get-ModelSpace acadDoc)
  )

  ;; Register an application name
  (regapp "MYAPP")

  ;; Attach some xdatas:
  ;; 1001: application name  ;; 1000: string ;; 1010: 3D point ;; 1040: real 
 
  ;; 1070: 16bit integer
  (setq codes  '(1001 1000 1010 1040 1070)
        values '("MYAPP" "XDATA String" (1.0 1.0 0.0) 5.0 4)
  )


  ;; Create the Safe and Variant Arrays needed for vla-SetXData
  (setq ListLength (1- (length codes)))
  (setq ArrayTypes
     (vlax-make-safearray
        vlax-vbInteger
        (cons 0 ListLength)
     )
  )
  (setq ArrayValues
     (vlax-make-safearray
        vlax-vbVariant
        (cons 0 ListLength)
     )
  )
  (vlax-safearray-fill ArrayTypes codes)
 ; simple list works
 ; A more complex list needs to be constructed one element at a time:
  (setq i 0)
  (while (< i ListLength)
    (if (equal (type (setq lstElem (nth i values))) 'LIST)
      (vlax-safearray-put-element
         ArrayValues
         i
         (vlax-3d-point lstElem)
      )
      (vlax-safearray-put-element ArrayValues i (nth i values))
    )
    (setq i (1+ i))
  )
  
  (setq VarTypes (vlax-make-variant ArrayTypes))
  (setq VarValues (vlax-make-variant ArrayValues))
  (vlax-for ent mspace (vla-SetXData ent VarTypes VarValues))
  (princ "\nFinished storing XData on All Drawing entities.\n")

  (setq EntIndx 0)
  ;; Get all xdatas from entities
  (princ "\nReading XData from drawing entities.\n")
  (vlax-for ent mspace
    (princ (strcat "\n\nEntity(" (itoa EntIndx) "): "))
    (princ (vla-get-ObjectName ent))
    (princ "\nXData: ")

    ;; Deconstruct the Variant Array return of
    ;; vla-GetXData to SafeArrays, 

    ;;and thento a list
    (setq VarDataTypes nil
          VarDataValues nil
    )
    (vla-GetXData ent "" 'VarDataTypes 'VarDataValues)
    (if (/= VarDataTypes nil)
      (progn
         (setq LispList nil)
         ;; Get the dimension of the safearray
         (setq lBound (vlax-safearray-get-l-bound VarDataTypes 1))
         (setq uBound (vlax-safearray-get-u-bound VarDataTypes 1))
         (setq aCounter lBound)
         (while (<= aCounter uBound)
            (setq dataCode (vlax-safearray-get-element
                               VarDataTypes
                               aCounter
                           )
            )
            (setq VarValue (vlax-safearray-get-element
                               VarDataValues
                               aCounter
                           )
            )
            ;; VarValue contains the variant, but we need the Lisp value of it
            (if (and (> dataCode 1009) (< dataCode 1040))
               ;; Test to see if it's a point Variant
               (progn (setq saValue (vlax-variant-value VarValue))
                      (setq Value (vlax-safearray->list saValue))
               )
               (setq Value (vlax-variant-value VarValue))
            )
            ;; Create the list
            (setq LispList (append LispList (list (cons dataCode Value))))
            (setq aCounter (1+ aCounter))
         ) ;_ end of while
      ) ;_ end of progn
      (setq LispList nil)
    ) ;_ end of if
    (if LispList
      (progn (princ "\n\tCodes: ")
             (foreach LstItem LispList
                (princ (car LstItem))
                (princ "  ")
             )
             (princ "\n\tData: ")
             (foreach LstItem LispList
                (princ (cdr LstItem))
                (princ "  ")
             )
      )
    )

    (setq EntIndx (1+ EntIndx))
  ) ;vlax-for
  (princ)
)

(princ "\nc:setandgetxdatas loaded, type setandgetxdatas to run.")
(princ)

## 评论

**内容**: joseph paik said...
Hi~
I executed the sample code in AutoCAD2010(32bit version)
But I got the return value "0" instead of "4" in code 1070.
Result was...
=============================================
Entity(0): AcDbCircle
XData:
Codes: 1001 1000 1010 1040 1070
Data: MYAPP XDATA String (1.0 1.0 0.0) 5.0 0
Entity(1): AcDbLine
XData:
Codes: 1001 1000 1010 1040 1070
Data: MYAPP XDATA String (1.0 1.0 0.0) 5.0 0
=============================================
What happend?
Please, let me know the reason..
thanks..
Reply
02/25/2013 at 06:08 AM

---
**内容**: Tito said...
change the WHILE statement
from
(while (< i ListLength)
(if (equal (type (setq lstElem (nth i values))) 'LIST)
TO
(while (<= i ListLength)
(if (equal (type (setq lstElem (nth i values))) 'LIST)
Reply
10/05/2016 at 07:05 PM

---
**内容**: Tito said...
Thanks Augusto for this very USEFUL routine
Reply
10/05/2016 at 07:07 PM

---
