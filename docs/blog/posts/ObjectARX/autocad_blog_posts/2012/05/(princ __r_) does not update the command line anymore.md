---
title: "(princ "\r") does not update the command line anymore"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "I've been using (princ "\r") to update the command line inside my LISP command, but in AutoCAD 2011 it does not seem to work anymore."
author: Autodesk
---
# (princ "\r") does not update the command line anymore

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/princ-r-does-not-update-the-command-line-anymore.html

## 文章内容

By Adam Nagy
I've been using (princ "\r") to update the command line inside my LISP command, but in AutoCAD 2011 it does not seem to work anymore.
You can use the following code to reproduce the issue:
(defun pause(mili / time)
  (setq time (getvar "date"))
  (while (< (* (- (getvar "date") time) 100000000) mili))
  nil
)
(defun c:printtest ()
  (princ "\n")
  (setq num 1)
  (repeat 100
    (pause 100)
    (setq num (1+ num))
    (princ "\r")
    (princ num)
  )
)
As you can see in AutoCAD 2011 only the last number (101) appears in the command line once the command finished, but nothing in between. This used to work fine before.
Solution
The workaround is to use an additional (princ):
(defun pause(mili / time)
  (setq time (getvar "date"))
  (while (< (* (- (getvar "date") time) 100000000) mili))
  nil
)
(defun c:printtest ()
  (princ "\n")
  (setq num 1)
  (repeat 100
    (pause 100)
    (setq num (1+ num))
    (princ "\r")
    (princ num)
    (princ) ; with the addition of this the command line gets updated
  )
)

## 评论

**内容**: John Vogt said...
First, anybody experimenting using this code, be careful about redefining the "pause" symbol. You might temporarily mess up the (command ...) statements in the rest of your code.
Second, this still doesn't work for me. It works for a while, randomly stopping (with a small flash of the screen) the update to the command line; one time it will get to 63, then another time to 57. I had been thinking that the various print functions were going to background processing, and that a pause to catch up between the code and the printing might work. But if my function is reading 80k lines of a data file, it already takes quite a while, that's why I need to show the user a status so they don't think it's locked up. So I don't want to use a pausing mechanism that makes it take even longer. But, as I said, that doesn't make it work for me, even using your sample code. And even the doslib (get_progress ...)progress bar stops updating after a while. So I now I'm thinking that all of alisp gets pushed to background processing after a certain point of memory use? Any more ideas?
Reply
06/05/2012 at 09:57 AM

---
