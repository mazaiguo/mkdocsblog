---
title: "Using AutoLISP to filter specific extended entity xdata"
date: 2013-03-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Selection
description: "How do I create a selection set filter in AutoLISP for a specific xdata value ?"
author: Autodesk
---
# Using AutoLISP to filter specific extended entity xdata

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/using-autolisp-to-filter-specific-extended-entity-xdata.html

## 文章内容

By Xiaodong Liang
Issue
How do I create a selection set filter in AutoLISP for a specific xdata value ?
Solution
A wiki help introduces in details on how to manipulate xdata by LISP:
Extended Data – xdata
Following is a small code demo. It assumes some entities have been added the xdata named “TEST_APP”. The code wants to filter the entities with the xdata and the data contains one value whose type is 1070 and value is 44.

(defun GetSpecificXdata (appName XdataType XdataValue / ss1 ssr indx sl entLst
theXdata i xl xdatav xdatal)
 (setq ss1 (ssget "X" (list (cons -
3 (list (list appName))))))
 (if ss1
   (progn
     (setq ssr (ssadd))
     (setq indx 0 sl (sslength ss1))
     (princ (strcat "\nOriginal Xdata Selection Set Length: " (itoa sl)))
     (while (< indx sl)

    (setq entLst (entget (ssname ss1 indx) (list appName)))
    (setq theXdata (cdr (assoc '-3 entLst)))
    (setq  i 0 xl (length (setq xdatal (car theXdata))))
    (while (< i xl)
        (if (= (type (setq xdatav (car xdatal))) 'LIST)
         (if (= (car xdatav) XdataType)
              (if (= (cdr xdatav) XdataValue)
               (ssadd (ssname ss1 indx) ssr)
              )
         )
        )
        (setq i (1+ i) xdatal (cdr xdatal) ) 
      )
      (setq indx (1+ indx))
    )
   )
 )
ssr
)
 
(defun TestXdataSelection (/ ss2)
 (setq ss2 (GetSpecificXdata "TEST_APP" 1070  44))
 (if ss2
     (progn
    (princ (strcat "\nSearched for Application: " "TEST_APP" ",
XData Type: " (itoa 1070) ", XData Value: " (itoa 44)))
    (princ (strcat "\nResultant Selection Set Length: " (itoa (sslength
ss2))))
     )
 )
 (princ)
)

(princ "\nTestXdataSelection loaded, type (TestXdataSelection) to run.")
(princ)

