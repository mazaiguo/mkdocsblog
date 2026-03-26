---
title: "Visual LISP: Importing Page Setups from another drawing?"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - DWG
  - Plot
description: "While the following technique takes longer to run than (command " -PSETUPIN"  ), the example demonstrates how to use the (vla-CopyFrom) method to i..."
author: Autodesk
---
# Visual LISP: Importing Page Setups from another drawing?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/visual-lisp-importing-page-setups-from-another-drawing.html

## 文章内容

By Gopinath Taget
While the following technique takes longer to run than (command " -PSETUPIN"  ), the example demonstrates how to use the (vla-CopyFrom) method to import pagesetups.
NOTE:  This example assumes that a PaperSpace pagesetup named "MyEPlotTest" exists in a drawing named "MyPageSetups.dwg".Also run this code in a non-production drawing as it deletes all page setups. The example can be modified so that it would not try to import a PageSetup into a drawing that already has a PageSetup named "MyEPlotTest".
(vl-load-com)
(setq *doc* (vla-get-activedocument (vlax-get-acad-object)))
  (defun ImpPgSetups (psname / psfile doc2 colPgSetups1 colPgSetups2 objPgSetup objPgSetup2 sName)
    ; if page setup source file is found,
   (if (setq psfile (findfile "MyPageSetups.dwg"))
      (progn
         ;; delete all existing page setups.
         (DelPgSetups)
         ;; import page setups
         (setq doc2 (vla-open
         (vla-get-documents (vlax-get-acad-object)) psfile)
              colPgSetups1 (vla-get-PlotConfigurations *doc*)
              colPgSetups2 (vla-get-PlotConfigurations doc2)
         ) ;setq
        ;;get each page setup in the ACAD_PLOTSETTINGS dictionary
         (vlax-for objPgSetup colPgSetups2
            (setq sName (vlax-get-property objPgSetup 'Name))
            (if (= sName psname)
               (progn
                  ;;add the page setup to the current doc
                  ;:vlax-true = Model tab only
                  (setq objPgSetup2
                  (vla-add colPgSetups1 sName :vlax-false))
                  (vla-CopyFrom objPgSetup2 objPgSetup)
               )
            ) ;if
            ;release the page setup
           (vlax-release-object objPgSetup)
         ) ;vlax-for
         (vlax-release-object colPgSetups1)
         (vlax-release-object colPgSetups2)
         (vla-close doc2)
         (vlax-release-object doc2)
      ) ;progn
   ) ;if
)
    (defun DelPgSetups (/ colPgSetups objPgSetup)
   (vl-load-com)
   ;;get the ACAD_PLOTSETTINGS dictionary
   (setq colPgSetups (vla-get-PlotConfigurations *doc*))
   ;;get each page setup in the ACAD_PLOTSETTINGS dictionary
   (vlax-for objPgSetup colPgSetups
      ;delete the page setup from the dictionary
      (vla-delete objPgSetup) 
      ;release the page setup
      (vlax-release-object objPgSetup)
   ) ;vlax-for
   (vlax-release-object colPgSetups)
   (princ)
)
    (defun C:TEST()
   (ImpPgSetups "MyEPlotTest")
)

