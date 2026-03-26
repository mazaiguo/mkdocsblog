---
title: "How to load a .MLN file using LISP"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoLISP
  - C++
  - VBA
description: "There isn't a ready-to-use API function that loads a .MLN file in Lisp, VBA and ARX. Normally you can do this only by using the MLSTYLE dialog."
author: Autodesk
---
# How to load a .MLN file using LISP

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/how-to-load-a-mln-file-using-lisp.html

## 文章内容

By Augusto Goncalves
There isn't a ready-to-use API function that loads a .MLN file in Lisp, VBA and ARX. Normally you can do this only by using the MLSTYLE dialog.
Of course, it's possible to create the dictionary entry of a multiline style definition programmatically with either API. The following code shows how to read the .MLN file in Lisp and how to create the MLINESTYLE objects defined in it.
(defun c:LoadMlStyles (/ mlFileName)
   (setq mlFileName (getstring "\nEnter MLN file name: "))
   (if (/= nil mlFileName)
      (LoadMln mlFileName)
   )
   (princ)
)


(defun LoadMln (mlnFile / f mlineDict same newStyle xName)
   (setq mlnFile (findfile mlnFile))
   (setq f (open mlnFile "r"))
   ;;(setq f (open mlnFile "r"))
   (if (= NIL f)
      (princ "\nInvalid MLN file.\n")
      (progn
         ;; Get the MLINESTLYE dictionary.
         (setq mlineDict (dictsearch
               (namedobjdict) "ACAD_MLINESTYLE"))
         ;; Create the beginning of an MLINESTYLE object.
         (setq same (list (cons 0 "MLINESTYLE")
                             ;;(cons 102 "{ACAD_REACTORS")
                             ;;(cons 330 (cdr (assoc -1 mlineDict)))
                             ;;(cons 102 "}")
                             ;;(cons 330 (cdr (assoc -1 mlineDict)))
                                 (cons 100 "AcDbMlineStyle")
                          )
         )
         ;;
         ;; Read the data of the MLINESTYLE
         ;;
         (while (/= nil (setq mlStyle (ReadObject f)))
            ;; Create the complete MLINESTYLE object.
            (setq newStyle (append same mlStyle)
                     xName    (entmakex newStyle)
            )
            ;; Append it to the MLINESTYLE dictionary.
            (dictadd (cdr (assoc -1 mlineDict))
               (cdr (assoc 2 newStyle))
               xName
            )
         )
      )
   )
   (close f)
   (princ)
)

(defun ReadObject (f / ObjectList firstLine code value)
  (setq ObjectList nil)
  ;; Skip the 'MLSTYLE'.
  (setq firstLine (read-line f))
  (if (/= nil firstLine)
   (progn
     (while (/= 0 (setq code (atoi (read-line f))))
        (setq value (vl-string-trim " " (read-line f)))
        (if (or (= code 2)
                  (= code 3)
                  (= code 6)
            )
           (setq ObjectList (append ObjectList
           (list (cons code value))))
        )
        (if (or (= code 70)
                  (= code 62)
                  (= code 71)
             )
           (setq ObjectList (append ObjectList
           (list (cons code (atoi value)))))
        )
        (if (or (= code 51)
                (= code 52)
          )
          ;; Code 51 and 52 must be converted into degrees.
          (setq ObjectList 
            (append ObjectList 
            (list (cons code 
            (angtof value 0)))))
          )
          (if (= code 49)
           (setq ObjectList 
           (append ObjectList
           (list (cons code (atof value)))))
          )
       )
   )
  )
  ObjectList
)
You can load a .MLN file from the AutoCAD command line by using the LOADMLSTYLES command. This command asks for the MLN file name. If you want to call this function from Lisp, you can use the (LOADMLN) function. There you can specify the MLN file name.
Once you've loaded a .MLN file, you can set the AutoCAD variable CMLSTYLE to one of the loaded styles, so the next created MLINE will use the style.

## 评论

**内容**: JM Choi said...
@Augusto Goncalves
Thanks a lot !!!
Reply
12/17/2013 at 11:57 PM

---
**内容**: Eduardo said...
Great!
Thank you very much!
Reply
05/29/2014 at 01:35 PM

---
