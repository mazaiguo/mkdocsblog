---
title: "Determine in which line of AutoLISP code an error exists"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "In much previous versions of AutoLISP and Visual LISP (VLISP), when an AutoLISP function terminated unexpectedly in the drawing editor, the entire ..."
author: Autodesk
---
# Determine in which line of AutoLISP code an error exists

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/determine-in-which-line-of-autolisp-code-an-error-exists.html

## 文章内容

By Xiaodong Liang
In much previous versions of AutoLISP and Visual LISP (VLISP), when an AutoLISP function terminated unexpectedly in the drawing editor, the entire expression would display on the screen, which made it easy to locate the exact line which
contained the error. When this situation occurs In recent AutoCAD versions, locating the error is not as easy because only a message such as "Bad argument type: lentityp' (or stringp)" displays. The error message unfortunately does not state
in which line of code the error exists.
How errors in AutoLISP code are handled has been changed. Now, to locate the error in the code, you will need to use the Visual Lisp IDE. Although it may require that you learn about the IDE debug features, you'll find that it's a much better environment to debug AutoLISP code than in previous releases of AutoCAD. What you need to do to enable this facility is to perform the following steps:
1. Open the Visual Lisp IDE at the beginning of your AutoCAD session by typing VLISP or VLIDE at the command line.

2. Select the Debug menu in the IDE, and select 'Break On Error'.

3. Load your AutoLISP code and run it.
When an error in your code occurs, you'll be put back into the Visual LISP IDE. All you then need to do, to find the line in the code that contains the error is to select the 'Last Break' option on the Debug Toolbar, or the 'Last Break Source' from the Debug menu.
There are many more powerful tools available to debug yourAutoLISP code using the Visual Lisp IDE, To learn about them, refer to the Visual LISP Developer's Guide >> Debugging Programs for more information about the IDE and its debugging features.

## 评论

**内容**: Tony Tanzillo said...
There's no need to use the Visual LISP IDE to find errors. I haven't used the Visual LISP IDE for close to 10 years.
This will show the source of the error:
(defun *error* (msg)
(vl-bt)
)
Example:
Command: (defun *error* (s) (vl-bt))
*ERROR*
Command: (defun C:BUGGY()
(_> (setq a (getint "\nEnter a number: "))
(_> (setq b (/ a 0))
(_> (princ))
C:BUGGY
Command: BUGGY
Enter a number: 3
Backtrace:
[0.48] (VL-BT)
[1.44] (*ERROR* "divide by zero")
[2.39] (_call-err-hook # "divide by zero")
[3.33] (sys-error "divide by zero")
:ERROR-BREAK.28 nil
[4.25] (/ 3 0)
[5.19] (C:BUGGY)
[6.15] (#)
[7.12] (# "(C:BUGGY)" T #)
:CALLBACK-ENTRY.6 (:CALLBACK-ENTRY)
:ARQ-SUBR-CALLBACK.3 (nil 0)
Command:
Reply
09/24/2012 at 01:12 PM

---
**内容**: Craig Dobyns said in reply to Tony Tanzillo...
Thanks Tony, I use it now, makes hunting down issues much easier
Reply
09/11/2014 at 02:35 PM

---
**内容**: Robert said...
How do i use that error function?
Reply
11/24/2020 at 06:20 PM

---
