---
title: "Using an ARX ActiveX server to update the block description from LISP"
date: 2013-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - AutoLISP
  - Block
  - C++
  - COM
description: "How can I update the Description Field in the Block Definition using lisp ? Using the Lisp entmod function does not seem to work."
author: Autodesk
---
# Using an ARX ActiveX server to update the block description from LISP

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/using-an-arx-activex-server-to-update-the-block-description-from-lisp.html

## 文章内容

By Xiaodong Liang
Issue
How can I update the Description Field in the Block Definition using lisp ? Using the Lisp entmod function does not seem to work.
Solution
The only way to do this at present is to use the ActiveX server exposed in the adskUnSupp arx utility, the latest utility for AutoCAD 2013 is available at
ADN AutoCAD Utilities
With that ARX, and the following lisp code which loads the ARX module, connects to the ActiveX interface from adskUnSupp ARX, and loads it's type library to enable the Block Description Property to be set directly via a lisp function call.
;assume the utilities are installed at
; C:\Program Files\Autodesk\ADNUtilities2013_X64\AutoCADControls\

(defun RunAcadUnSupp (/ rtn )
 (if (null (setq rtn (member "AsdkUnsupp2013.arx" (arx)))) (setq rtn (arxload
"asdkunsupp2007.arx")))
 (if (null rtn)
   (progn
     (princ "\nAsdkUnsupp2013.arx Not Loaded, Exiting.")
     (exit)
   )
 )
 (vl-load-com)
 (setq AcadApp (vlax-get-acad-object))
;;; Change the Path to adskUnSupp2007 here ->
 (setq unSupp_ARXPath "C:\\Program Files\\Autodesk\\ADNUtilities2013_X64\\AutoCADControls\\\")
 (if (null unsupM-AddAnonymousGroup)
    (if (findfile (strcat unSupp_ARXPath "AsdkUnsupp2013.arx"))
    (vlax-import-type-library
     :tlb-filename
     (strcat unSupp_ARXPath "AsdkUnsupp2013.arx")
     :methods-prefix
     "unsupM-"
     :properties-prefix
     "unsupP-"
     :constants-prefix
     "unsupC-"
    )
   (progn
     (alert (strcat "Exiting - Can't find \"" unSupp_ARXPath
"asdkunsupp2007.arx" "\""))
     (exit)
   )
 )
)
 (setq unSuppX (vla-GetInterfaceObject acadApp "Asdkunsupp2007.Application.1"))
 (setq AcadDoc (vla-Get-ActiveDocument AcadApp))
 (setq UtilObj (vla-Get-Utility AcadDoc))
 (setq Blocks (vla-Get-Blocks AcadDoc))
 (vla-GetEntity UtilObj 'BlockRefObj 'selPt "\nSelect a Inserted Block: ")
 (if (equal
    (setq ObjType (vla-Get-ObjectName BlockRefObj))
    "AcDbBlockReference"
     )
      (progn
     (setq BlkName (vla-Get-Name BlockRefObj))
     (setq BlkObject (vla-Item Blocks BlkName))
     (setq exBlkDescriptn (unsupP-Get-BlockDescription unSuppX BlkObject))
     (setq aNewDescriptn (getString T (strcat "\nEnter New Block
Description<" exBlkDescriptn ">:")))
     (if (and aNewDescriptn (not (equal aNewDescriptn "")))
        (unsupP-Put-BlockDescription unSuppX BlkObject aNewDescriptn)
     ) 
      )
   )
   (CleanUpOnExit)
)

(defun CleanUpOnExit ()

(if BlockRefObj (progn (vlax-Release-Object BlockRefObj) (setq BlockRefObj
nil)))
(if Blocks (progn (vlax-Release-Object Blocks) (setq Blocks nil)))
(if UtilObj (progn (vlax-Release-Object UtilObj) (setq UtilObj nil)))
(if AcadDoc (progn (vlax-Release-Object AcadDoc) (setq AcadDoc nil)))
(if unSuppX (progn (vlax-Release-Object unSuppX) (setq unSuppX nil)))
(if AcadApp (progn (vlax-Release-Object AcadApp) (setq AcadApp nil)))
(princ)
)

(princ "\nRunAcadUnSupp, CleanUpOnExit loaded, type (RunAcadUnSupp), or
(CleanUpOnExit) to run.")
(princ)

