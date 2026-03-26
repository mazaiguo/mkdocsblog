---
title: "Image command from visual LISP?"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - COM
  - DXF
description: "To use the RELOAD, UNLOAD and DETACH options of the IMAGE command, it is not possible to use the AutoCAD ActiveX interface. Instead, you have to 'r..."
author: Autodesk
---
# Image command from visual LISP?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/image-command-from-visual-lisp.html

## 文章内容

By Augusto Goncalves
To use the RELOAD, UNLOAD and DETACH options of the IMAGE command, it is not possible to use the AutoCAD ActiveX interface. Instead, you have to 'rebuild' these options using AutoLISP and Visual LISP functions.
-IMAGE RELOAD:
This command options works on the raster image definition object that is stored in the dictionary "ACAD_IMAGE_DICT". This object uses the DXFgroup code 280 as a 'loaded' flag. If the value of group code 280 is 1, the image file is currently loaded; if the value is 0, the image file is unloaded.
In order to get the correct entry in the image dictionary (to get the right image definition object) and set this flag to 1, use the IMAGERELOAD function (see below).
-IMAGE UNLOAD:
This command options uses the flag previously mentioned. Set the value of group code 280 to 0 to unload the image file. The function IMGUNLOAD does this.
-IMAGE DETACH:
This command options removes the specified image definition object and removes every raster image entity from the current drawing that uses the (deleted) image definition object. The IMGDETACH function does this.
You can use the following functions. They 'rebuild' the functionality of the IMAGE command options.  The functions (imgreload), (imgunload) and (imgdetach) need the image name as a parameter. For the image name, use the AutoCAD wildcard mechanism.
;;; Use the function 'imgunload' instead of
;;; calling the command
;;; -IMAGE _Unload
;;;
(defun imgunload (imgname)
  (imgloadstat (strcase imgname) 0)
  (princ)
)

;;; Use the function 'imgreload' instead of
;;; calling the command
;;; -IMAGE _Reload
;;;
(defun imgreload (imgname)
  (imgloadstat (strcase imgname) 1)
  (princ)
)

;;; Use the function 'imgdetach' instead of
;;; calling the command
;;; -IMAGE _Detach
;;;
(defun imgdetach (imgname / imgDict imgDictId dictLength counter
        dictName imgDefIds selSet imgDefId)

  ;; Iterate all dictionary entries and remove
  ;; the entries which matches 'imgname'.

  (setq imgname (strcase imgname)
    imgDict (dictsearch (namedobjdict) "ACAD_IMAGE_DICT")
  )
  (if (equal imgDict nil)
   (princ "\nNo images loaded.")
   (progn
    ;; Image dictionary is available.
    (setq imgDictId  (cdr (car imgDict))
       dictLength (length imgdict)
       counter  0
    )
    (while (< counter dictLength)
      (if (equal (car (nth counter imgDict)) 3)
       ;; Entry name found. Get it.
       (progn
        (setq dictName (strcase (cdr (nth counter imgDict))))
        ;; Compare the entry name.
        (if (wcmatch dictName imgname)
          (progn
           ;; Remove the dictionary entry...
           (dictremove imgDictId dictName)
           ;; ...and store the entity name of
           ;; the raster image definition object.
           (setq imgDefIds
            (append imgDefIds
                (list (cdr (nth (1+ counter) imgDict)))
            )
           )
          )
        )
       )
      )
      (setq counter (1+ counter))
    )
    ;; Finished iterating the dictionary.
    ;; Do we have to remove some raster image entities?
    (if (/= (length imgDefIds) 0)
      ;; Yes, we have to remove some raster image entities
      ;; (because the related image definition objects
      ;; have been removed).
      (progn
       ;; Select all image entities.
       (setq selSet  (ssget "X" '((0 . "IMAGE")))
          counter 0
       )
       (if (/= selSet nil)
        (progn
          ;; Iterate all image entities
          (while (< counter (sslength selSet))
           ;; Get the entity name of the referenced
           ;; image definition object.
           (setq imgDefId
            (cdr (assoc 340 (entget (ssname selSet counter))))
           )
           ;; Is the referenced definition object gone?
           (if (member imgDefId imgDefIds)
            ;; The definition for this image entity
            ;; have been removed, so let us remove
            ;; the image entity, as well.
            (entdel (cdr (car (entget (ssname selSet counter)))))
           )
           (setq counter (1+ counter))
          )
          ;; Empty the selection set
          (setq selSet nil)
        )
       )
      )
    )
   )
  )
  (princ)
)

;;; Internal function.
;;; This function is called by 'imgunload'
;;; and 'imgreload'.
;;;
(defun imgloadstat (imgname status / imgDict imgDictId
          dictLength counter dictName dictEntry next)

  ;; Get the image dictionary
  (setq imgDict (dictsearch (namedobjdict) "ACAD_IMAGE_DICT"))
  (if (equal imgDict nil)
   (princ "\nNo images loaded.")
   (progn
    ;; Image dictionary is available.
    (setq imgDictId  (cdr (car imgDict))
       dictLength (length imgdict)
       counter  0
       next  T
    )
    (while (< counter dictLength)
      (if (equal (car (nth counter imgDict)) 3)
       ;; Entry name found. Get it.
       (progn
        ;; Get dictionary entry name
        ;; and the dictionary entry
        (setq dictName (strcase (cdr (nth counter imgDict)))
           dictEntry (dictnext imgDictId next)
           next  nil
        )
        ;; Compare the entry name with the given name.
        (if (wcmatch dictName imgname)
          (progn
           ;; Entry found. Set the 'loaded' flag
           (setq dictEntry (subst (cons 280 status)
                      (assoc 280 dictEntry)
                      dictEntry
                  )
           )
           ;; There is a problem in AutoCAD
           ;; which is fixed by 'fixlist'.
           ;; Some entities / objects should
           ;; return on 'entget' 2D points,
           ;; but VisualLisp gets 3D points.
           ;; The (wrong) z value of thereturned
           ;; point contains a random value
           ;; which can break 'entmod'.
           ;; In case of an image definition
           ;; object we have to remove the
           ;; z value of group code 10 and
           ;; 11 before we can use 'entmod'.
           (entmod (fixlist dictEntry))
          )
        )
       )
      )
      (setq counter (1+ counter))
    )
   )
  )
)

;;; Internal function.
;;; This function avoids the problem with 2D / 3D points.
;;;
(defun fixlist (imgDef /)
  ;; Get the group code 10 and 11 list
  (setq pt1 (assoc 10 imgDef)
    pt2 (assoc 11 imgDef)
  )
  ;; Remove the z value of group code 10...
  (setq imgDef (subst (list 10 (nth 1 pt1) (nth 2 pt1))
           (assoc 10 imgDef)
           imgDef
        )
  )
  ;; ...and the z value of group code 11.
  (setq imgDef (subst (list 11 (nth 1 pt2) (nth 2 pt2))
           (assoc 11 imgDef)
           imgDef
        )
  )
  ;; Return the fixed list
  imgDef
)
(princ "\nNew lisp functions:")
(princ "\n(imgunload ), (imgreload ), (imgdetach)\n")
(princ)

