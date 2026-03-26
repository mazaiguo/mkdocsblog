---
title: "Warning on opening a drawing in which an entity with a persistent LISP reactor got erased"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Plugin
description: "I'm adding a persistent reactor to an entity using LISP, but the problem is that if the entity with the reactor attached gets deleted, then on reop..."
author: Autodesk
---
# Warning on opening a drawing in which an entity with a persistent LISP reactor got erased

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/warning-on-opening-a-drawing-in-which-an-entity-with-a-persistent-lisp-reactor-got-erased.html

## 文章内容

By Adam Nagy
I'm adding a persistent reactor to an entity using LISP, but the problem is that if the entity with the reactor attached gets deleted, then on reopening the drawing I get this warning:
; warning:erased VLA-object restored to NIL
Here is the code I'm testing with:
(defun pers-modified (notifier-object reactor-object parameter-list)
  (cond
    (
     (vlax-read-enabled-p notifier-object)
     (vlax-property-available-p
       notifier-object
       "Radius"
     )
     (princ "The radius is ")
     (princ (vla-get-radius notifier-object))
    )
  ) ;_ cond
) ;_ defun

(defun c:startReactor (/ circle reactor)
  (vl-load-com)
  (setq circle (car (entsel 
    "\nSelect a circle to add persistent reactor to: ")))
  (setq circle (vlax-ename->vla-object circle))
  (setq g-object-reactor
    (vlr-object-reactor
      (list circle) ; list of objects
      nil ; reactor data
      '(
        (:vlr-modified . pers-modified)
       )
    )
  )
  (vlr-pers g-object-reactor)
) ;_ defun
I also tried removing the reactor from the entity when it gets deleted, but then in case of UNDO the reactor does not get reattached and I do not get notified when the entity gets unerased. Not sure what to try next.
Solution
1. If the same reactor is watching multipe entities
You could create another non-persistent/transient object reactor that could keep track of the erased or unappended objects and then add them back to the persistent reactor.
This way when the drawing gets saved the erased objects only have a transient reactor which does not get saved in the drawing.
Unfortunately, it seems you cannot modify the reactor owners list from object erased, unerased, reappended and unappended. So you need to create a list that stores the objects that need to be moved from one reactor to the other and do the actual modification inside e.g. the documentLockModeWillChange event.
;;; PERSISTENT REACTOR PART ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; the objectModified handler prints some info about the circle
(defun pers-modified (notifier-object reactor-object parameter-list)
  (cond
    (
     (vlax-read-enabled-p notifier-object)
     (vlax-property-available-p
       notifier-object
       "Radius"
     )
     (princ "The radius is ")
     (princ (vla-get-radius notifier-object))
    )
  ) ;_ cond
) ;_ defun

;;; handles UnAppended and Erased events
(defun pers-objectRemoved (notifier-object reactor-object
   parameter-list /
   owners index
  )
  ;; we cannot modify the owners of a reactor from here
  ;; so we just create a list and postpone the modification
  ;; till docmanager-document-lock-mode-will-change
  (if (/= g-erased-objects nil)
    (setq g-erased-objects
      (append g-erased-objects (list notifier-object))
    )
    (setq g-erased-objects (list notifier-object))
  )
)

;;; DUSTBIN REACTOR PART ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; handles ReAppended and UnErased events
(defun dustbin-objectAdded (notifier-object reactor-object
    parameter-list /
    owners index
   )
  ;; we cannot modify the owners of a reactor from here
  ;; so we just create a list and postpone the modification
  ;; till docmanager-document-lock-mode-will-change
  (if (/= g-unerased-objects nil)
    (setq g-unerased-objects
      (append g-unerased-objects (list notifier-object))
    )
    (setq g-unerased-objects (list notifier-object))
  )
)

(defun docmanager-document-lock-mode-will-change
       (reactor-object parameter-list /)
  (setq command-name (cadr (cdddr parameter-list)))
  ;; we only check in case of command-ended event
  ;; i.e. command name starts with #
  (if (and (= (substr command-name 1 1) "#")
   (> (strlen command-name) 1)
      )
    (progn
      (foreach erased-object g-erased-objects
        (progn
          (vlr-owner-remove g-pers-reactor erased-object)
          (vlr-owner-add g-dustbin-reactor erased-object)
        ) ;_ progn
      ) ;_ foreach
      (setq g-erased-objects nil)
      (foreach unerased-object g-unerased-objects
        (progn
          (vlr-owner-remove g-dustbin-reactor unerased-object)
          (vlr-owner-add g-pers-reactor unerased-object)
        ) ;_ progn
      ) ;_ foreach 
      (setq g-unerased-objects nil)
    ) ;_ progn
  ) ;_ if 
)

;;; MAIN FUNCTION ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun c:startReactor (/ circle reactor)
  (vl-load-com)
  (setq circle (car 
    (entsel "\nSelect a circle to add persistent reactor to: ")))
  (setq circle (vlax-ename->vla-object circle))
  (setq g-pers-reactor
    (vlr-object-reactor
      (list circle) ; objects
      nil ; reactor data
      '(
        (:vlr-modified . pers-modified)
        (:vlr-erased . pers-objectRemoved)
        (:vlr-unappended . pers-objectRemoved)
       )
    )
  )
  (vlr-pers g-pers-reactor)

  (setq g-dustbin-reactor
    (vlr-object-reactor
      nil
      nil
      '(
        (:vlr-unerased . dustbin-objectAdded)
        (:vlr-reappended . dustbin-objectAdded)
       )
    )
  )

  (setq reactor
    (vlr-docmanager-reactor
      nil
      '(
        (:vlr-documentLockModeWillChange
         .
         docmanager-document-lock-mode-will-change
        )
       )
    )
  )
) ;_ defun

;;; JUST FOR TESTING ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun c:get-pers-owners (/)
  (princ (vlr-owners (car (vlr-pers-list))))
  (princ)
)
2. If there is a separate reactor for each entity
In this case things are easier, because you can just use (vlr-pers-release) on the reactor that is associated with the given entity when it gets erased or unappended, hereby making the reactor transient. If a reactor is transient it is not saved in the drawing. Unlike the act of modifying the list of objects associated with a given reactor, this operation is logged in the undo buffer, so if the user clicks UNDO after erasing the entity, then the (vlr-pers-release) operation will be undone as well.
;;; PERSISTENT REACTOR PART ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;; the objectModified handler prints some info about the circle
(defun pers-modified (notifier-object reactor-object parameter-list)
  (cond
    (
     (vlax-read-enabled-p notifier-object)
     (vlax-property-available-p
       notifier-object
       "Radius"
     )
     (princ "The radius is ")
     (princ (vla-get-radius notifier-object))
    )
  ) ;_ cond
) ;_ defun

;;; handles objectUnAppended and objectErased
(defun pers-objectRemoved (notifier-object reactor-object
                           parameter-list)
  (vlr-pers-release reactor-object)   
)

;;; MAIN FUNCTION ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun c:startReactor (/ pers-reactor circle)
  (vl-load-com)
  (setq circle (car 
    (entsel "\nSelect a circle to add persistent reactor to: ")))
  (setq circle (vlax-ename->vla-object circle))
  (setq pers-reactor
    (vlr-object-reactor
      (list circle) ; objects
      nil ; reactor data
      '(
        (:vlr-modified . pers-modified)
        (:vlr-erased . pers-objectRemoved)
        (:vlr-unappended . pers-objectRemoved)
      )
    )
  )
  (vlr-pers pers-reactor)
) ;_ defun

;;; JUST FOR TESTING ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun c:get-pers-owners (/)
  (princ (vlr-owners (car (vlr-pers-list))))
  (princ)
)

