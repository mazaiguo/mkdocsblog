---
title: "Behavior of M2P snap changed"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
description: "I am using this menu macro: M2P;ENDP;\ENDP; In AutoCAD 2010 and later, it does not work the same as it did in AutoCAD 2009 and previous versions. I..."
author: Autodesk
---
# Behavior of M2P snap changed

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/behavior-of-m2p-snap-changed.html

## 文章内容

By Wayne Brill
Issue
I am using this menu macro: _M2P;ENDP;\ENDP; In AutoCAD 2010 and later, it does not work the same as it did in AutoCAD 2009 and previous versions. In previous versions I can start the line command, click the menu item with the macro and I am prompted for the two points. The line is then started at the midpoint of the two selected points. In AutoCAD 2010 and later after selecting the points I am still prompted for another point. Is there a way to get the macro to start the line after selecting the two points? 
Solution
A way to get the behavior as in the previous releases is to use lisp transparently. Below is an example. The (command ...) function call below does not include a command name, so this can be used while any command is prompting for a point. The menu macro would be this: 'SNAPPY
NOTE: There is no preceding ^C and it also includes the leading single quote '.
(defun c:snappy ( / osm )
(if (not (equal (getvar "cmdnames") ""))
     (progn
       (setq osm (getvar "osmode"))
       (setvar "osmode" 1)
       (command "_m2p" pause)
       (setvar "osmode" osm)
     )
);if
(princ)
)
  There is one drawback to the approach above and that is: Lisp cannot be used transparently to run commands when another lisp routine is prompting for input. (not directly anyway)
(defun c:foo ()
  (command "_line" pause pause "")
)
This will not work properly due to re-entrancy issues with lisp.
(FOO
'snappy
There is a way around this but it involves more code. If you use the sample (link below) then the following macro can be used in conjunction with any command and/or any lisp routine.
'_midof;_endp;\_endp
or
'_thirdof;_endp;\_endp
Download Midof

