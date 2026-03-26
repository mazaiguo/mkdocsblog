---
title: "Deleting named page setup using Lisp"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoLISP
description: "Here is a Visual Lisp code to delete all the named page setup :"
author: Autodesk
---
# Deleting named page setup using Lisp

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/deleting-named-page-setup-using-lisp.html

## 文章内容

By Balaji Ramamoorthy
Here is a Visual Lisp code to delete all the named page setup :
(defun C:DelPgSetups ( / appAcad colPgSetups docCurrent objPgSetup)
    (vl-load-com)
      ;get the ACAD application object
    (setq appAcad (vlax-get-acad-object))
      ;get the current drawing
    (setq docCurrent (vla-get-ActiveDocument appAcad))
      ;get the ACAD_PLOTSETTINGS dictionary
    (setq colPgSetups (vla-get-PlotConfigurations docCurrent))
      ; ask for confirmation before deleting
    (initget 1 "Y YES N NO")
    (setq answer
        (substr
            (getkword
                "\nThis will erase all the named page setups ?
                Do you want to continue ? [Yes/No]: "
            )
            1 1
        )
    )
      ; if ok, continue to delete all the named page setups
    (if (= answer "Y")
        (progn
            ;;get each page setup in the
            ;ACAD_PLOTSETTINGS dictionary
            (vlax-for objPgSetup colPgSetups
                (princ
                    (strcat "\nDeleting " (vla-get-name objPgSetup))
                )
                  ;delete the page setup from the dictionary
                (vla-delete objPgSetup)
                  ;release the page setup
                (vlax-release-object objPgSetup)
            );vlax-for
            (princ "\n\nDone.")
        )
    )
      ;;release objects from memory
    (vlax-release-object colPgSetups)
    (vlax-release-object docCurrent)
    (vlax-release-object appAcad)
      (princ)
);End of defun DelPgSetups

## 评论

**内容**: Jimmy Bergmark (JTB World) said...
As far as I know vlax-release-object should not be needed in this case. According to documentation: "When an AutoLISP routine no longer uses an object outside AutoCAD, such as a Microsoft Excel object, call the (vlax-release-object) function to make sure that the associated application closes properly."
Reply
05/05/2012 at 10:17 PM

---
**内容**: Kerry Brown said...

That is my understanding too Jimmy.
The version I have also calls
vla-RefreshPlotDeviceInfo before the delete ....
Regards
Kerry
Reply
05/06/2012 at 12:43 AM

---
**内容**: Balaji said...
Thanks Jimmy and Kerry.
It really does no harm since it is only decrementing the reference count for the COM objects that we are using. Based on the reference count, the COM object should know how to handle it.
Yes, As you said, in this case it might be redundant and I attribute it to my background with C++ COM programming :)
Reply
05/06/2012 at 11:22 AM

---
**内容**: Quinn said...
Is there any possibility to eliminate the confirmation?
Thank you
Reply
10/07/2016 at 12:03 AM

---
