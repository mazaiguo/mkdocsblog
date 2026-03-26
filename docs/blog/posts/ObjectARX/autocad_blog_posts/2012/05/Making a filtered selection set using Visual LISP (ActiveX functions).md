---
title: "Making a filtered selection set using Visual LISP (ActiveX functions)"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Block
  - COM
  - Database
  - Selection
description: "The ActiveX method SelectionSet.Select to create a filtered set of database objects that meet this criteria:"
author: Autodesk
---
# Making a filtered selection set using Visual LISP (ActiveX functions)

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/making-a-filtered-selection-set-using-visual-lisp-activex-functions.html

## 文章内容

By Balaji Ramamoorthy
The ActiveX method SelectionSet.Select to create a filtered set of database objects that meet this criteria:
Block references, such as INSERT entities, and that have extended entity data that is registered under application name "MYAPP"
The plain AutoLISP expression is: (ssget "X" '((0 . "INSERT") (-3 ("MYAPP"))))
Here is the code using the ActiveX call :
(defun c:myappSet ()
      (vl-load-com)
      (setq loAcad    (vlax-get-acad-object)
          loDoc        (vla-get-activedocument loAcad)
          loSelectionSet (vla-add (vla-get-selectionsets loDoc) "filtSet")
    )
      (setq filtArray (vlax-make-safearray vlax-vbInteger '(0 . 1))
          filtVar   (vlax-safearray-fill filtArray (list 0 1001))
          filtType  (vlax-make-variant
                        filtVar
                        (logior vlax-vbarray vlax-vbInteger)
                    )
    )
      (setq filtArray (vlax-make-safearray vlax-vbVariant '(0 . 1))
          filtVar   (vlax-safearray-fill filtArray (list "INSERT" "MYAPP"))
          filtData  (vlax-make-variant
                        filtVar
                        (logior vlax-vbarray vlax-vbVariant)
                    )
    )
      (vla-select
                loSelectionSet
                acSelectionSetAll
                nil
                nil
                filtType
                filtData
    )
      (setq count (vla-get-count loSelectionSet))
    (princ count)
      (setq ssets (vla-get-selectionsets loDoc))
    (vla-delete (vla-item ssets "filtSet"))
      (princ)
)
It is tempting for a Visual LISP developer to supply list arguments for the parameters filtType and filtData in the vla-select call, but ActiveX does not comprehend lists. The filtType parameter requires an array of integers while filtData is permitted to be a array of variant types.
For a closer examination of safearrays and variants, see the Visual LISP Developer's Guide. Refer to the section entitled "Converting AutoLISP Data Types to ActiveX Data Types".
Also, the group code designating xdata is 1001 instead of -3. This is different, of course, from the Visual LISP approach to filtering xdata, which makes use of the -3 extended data sentinel rather than group code.

## 评论

**内容**: Anonymoose said...
I think your sample LISP code contains a bug.
Let's see if you can find it
Reply
05/31/2012 at 08:22 PM

---
**内容**: Balaji said in reply to Anonymoose...
Fixed. Thanks :)
Reply
06/01/2012 at 08:19 AM

---
**内容**: Vinay Kumar said in reply to Balaji...
Hi Brother
How to attach xdata to insert ?
Regards
Reply
12/23/2016 at 02:15 AM

---
