---
title: "Mouse right button click and grips when using grread?"
date: 2013-01-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Selection
description: "Using (grread) in a Lisp application to track user input. How to determine if the right mouse button has been pressed, and how get AutoCAD to displ..."
author: Autodesk
---
# Mouse right button click and grips when using grread?

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/mouse-right-button-click-and-grips-when-using-grread.html

## 文章内容

By Augusto Goncalves
Using (grread) in a Lisp application to track user input. How to determine if the right mouse button has been pressed, and how get AutoCAD to display the grips of entities that were previously selected while (grread) is active?
If you right click, (grread) returns a list beginning with '25', so there should be no problem getting this information.
If you want to display the grip points of some entities, use (sssetfirst). There you can specify a selection set. AutoCAD then displays the grip points of every entity specified in the selection set.
Look at the following function to see how to get the right mouse button click is handled and how the grips of some entities are displayed. The function tests if there is an entity under the current cursor position and, if there is an entity, it displays the grips .To exit the (grread) loop, you have to press the right mouse button.
(defun c:test ()
   (setq run T)
   (while (equal run T)
      (setq res (grread T))
      (setq code (car res))

      ;; 'normal' mouse move?
      (if (equal code 5)
         (progn
            ;; get the current cursor position
            (setq pt (car (cdr res)))
            ;; is there something at the
            ;; current position?
            (setq ss (ssget pt))
            (if (/= ss nil)
               ;; yes, there is something.
               ;; show the grip points.
               (sssetfirst nil ss)
            )
         )
      )

      ;; right mouse click?
      (if (equal code 25)
         (progn
            ;; right mouse button clicked.
            ;; exit the loop.
            (princ "\nRight mouse click.\n")
            (setq run nil)
         )
      )
   )
)
If (grread) returns a list beginning with 25 (right mouse button click), the function ends. If the returned list begins with 5, the rest of the list is the current coordinate.

## 评论

**内容**: MP said...
HI,
Iam looking for a help. My application is like below,
If I press a key input from the keyboard it should print say hello until I press another key or same keyinput from the keyboard. I tried using while loop with grread function I can able to print hello only after I press the key every time. I don't want to press and hold the key , once I press the key it should keep printing hello until I press another or same key input. can you please send me the required code.
Thanks
Reply
05/05/2017 at 12:37 PM

---
**内容**: Madhukar Moogala said...
Hi,
Thanks for dropping by,
Can you please redirect your query to forum ? Your query will attract large audience with Lisp expertise.
https://forums.autodesk.com/t5/visual-lisp-autolisp-and-general/bd-p/130
Currently I'm busy with some other tasks, 'll get back to you on this.
Reply
05/07/2017 at 09:45 PM

---
