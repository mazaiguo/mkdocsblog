---
title: "Displaying a DCL dialog at the last location"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Dimension
description: "Is it possible to display a DCL dialog at the last location it was closed at, rather than having it always open in the center of the screen ?"
author: Autodesk
---
# Displaying a DCL dialog at the last location

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/displaying-a-dcl-dialog-at-the-last-location.html

## 文章内容

By Xiaodong Liang
Issue
Is it possible to display a DCL dialog at the last location it was closed at, rather than having it always open in the center of the screen ?
Solution
Yes, just feed the value of the last coordinate location of the dialog which is returned via done_dialog, to the new_dialog call. Here's some lisp code that demonstrates this, please ensure that the DCL file is on the AutoCAD search path.

(defun C:Move_the_DCL (/ dcl_id notenum1)

;; 1) loadup the Move_DCL.DCl file Dialogue Box, if it's on the path
  (setq DCLFileName "Move_DCL.dcl")
 
  (setq DCLfile (findfile DCLFileName))
  (if (null DCLfile)
     (progn
       (alert (strcat "\nDCL file:    "  DCLFileName " was Not Found !
Exiting."))
       (exit)
     )
  )
 
  (setq dcl_id (load_dialog DCLfile))


;; check to see if it's loaded, and display at last box location, if available


  (if lastpt
      (if (not (new_dialog "note" dcl_id "3" lastpt)) (progn (alert (strcat
"\nDCL file:  "  DCLFileName " was Not Found ! Exiting.")) (exit)) )
      (if (not (new_dialog "note" dcl_id "3" '(-1 -1))) (exit))
  )


;; 2) setup for return values/keys from DCL


(action_tile "cancel" "(done_dialog) (setq gperr \"\")(exit)")


(action_tile "accept"
    (strcat "(progn (setq ChkBoxReturnValue (atoi (get_tile \"note1\")))" 
    " (setq lastpt (done_dialog)))" 
    ) 
)    


;; 3) now start the dialogue box


  (start_dialog)


;; 4) unload the box


  (unload_dialog dcl_id)


;; print out the value returned


  (if ChkReturnValue
      (progn (princ "\nThe ChkBoxReturnValue is: ") (princ ChkBoxReturnValue))
  )
  (if lastpt
      (progn (princ "\nDialogue Box Location: ") (princ (car lastpt)) (princ ",
") (princ (cadr lastpt)) )
  )
(princ)
)
(princ "\nLoaded Move_DCL.lsp, type Move_the_DCL to run.")
(princ)
Here's the DCL Dialog the lisp file uses:
note : dialog {
  label = "Simple Dialog Example";
  : boxed_column {
     alignment =  centered;
     children_alignment =  centered;
    :text {
     alignment =  centered;
     is_bold = true;
     key = "label1";
     label = "This is a Centered Label";
     width = 8;
     }
    : spacer { width = 1; }
  : row {
    : spacer { width = 1; }
    :toggle {
     label = "Note Number 1";
     key = "note1";
     mnemonic = "C";
     alignment = right;
     }   
    }
    : spacer { width = 1; }
    }
  : row {        // defines the OK/Cancel button row
    : spacer { width = 1; }
    : button {    // defines the OK button

          label = "OK";
          key = "accept";
          width = 8;
          fixed_width = true;
        }
    : button {    // defines the Cancel button
        label = "Cancel";
        is_cancel = true;
        key = "cancel";
        width = 8;
        fixed_width = true;
        }
       }
}

