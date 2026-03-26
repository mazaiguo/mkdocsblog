---
title: "Register Lisp defined function for use with 'command' function"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - COM
description: "Using the Visual LISP ActiveX interface we can register the LISP function like this:"
author: Autodesk
---
# Register Lisp defined function for use with 'command' function

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/register-lisp-defined-function-for-use-with-command-function.html

## 文章内容

By Balaji Ramamoorthy
Using the Visual LISP ActiveX interface we can register the LISP function like this:
; Register the myfunc command in the same command
; registry that Lisp (command) uses
(vlax-add-cmd "myfunc" 'myfunc)
  (defun myfunc ()
   (setq str (getstring "\nEnter string : "))
   (setq int (getint "\nEnter int : "))
)
We can now use (command "myfunc") to call the function.

## 评论

**内容**: Matus Brlit said...
Is there any difference between your example and the following? Other than my is not using Visual LISP.
(defun c:myfunc() (myfunc))
Reply
06/22/2012 at 05:12 AM

---
**内容**: Balaji said...
Hi Matus,
"c:myfunc" is a VLisp command but (defun c:) registers the command in a different command registry than the one Lisp '(command)' uses.
For this reason, (command "c:myfunc") does not work.
The post explains a way to make a function callable using (command "name of the func")
Reply
06/22/2012 at 05:58 AM

---
**内容**: Kerry Brown said...
Balaji,
Would you , or one of your cohorts, please have a look at this issue ;
https://www.theswamp.org/index.php?topic=51409.0
Relating to registered Lisp functions in MDI.
Regards,
Kerry.
Reply
05/15/2016 at 07:23 PM

---
