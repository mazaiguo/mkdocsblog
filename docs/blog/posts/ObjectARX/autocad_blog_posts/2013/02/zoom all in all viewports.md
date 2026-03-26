---
title: "zoom all in all viewports"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How can I do a "zoom all" in all viewports?"
author: Autodesk
---
# zoom all in all viewports

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/zoom-all-in-all-viewports.html

## 文章内容

By Xiaodong Liang
Issue
How can I do a "zoom all" in all viewports?
Solution
You can easily do this by using the CVPORT system variable:
Type: Integer
Saved in: Drawing
Initial value: 2
Sets the identification number of the current viewport. You can change this value, thereby changing the current viewport, if the following conditions are met:
-- The identification number you specify is that of an active viewport.
-- A command in progress has not locked cursor movement to that viewport.
-- Tablet mode is off.
The number of current viewports can be determined using the AutoLISP function (vports) that returns something similar to:
((4 (0.0 0.5) (0.5 1.0)) (5 (0.0 0.0) (0.5 0.5)) (2 (0.5 0.0) (1.0 0.5)) (3 (0.5 0.5) (1.0 1.0)))
(setq nv (length (vports))) will give you the number of vports. If you have four vports, they are numbered 2 to 5.
An AutoLISP routine to zoom in for all vports can look like this:

(defun c:zoomall ( / i nv)

    (setq i 1)   ;initialise counter
    (setq nv (length (vports)))    ;get number of vports

    (repeat nv
         (setq i (1+ i))  ;start counting vports at 2
         (setvar "CVPORT" i)     ;set vport
         (command "_zoom" "all")     ;zoom all
    )

   (princ)
   )
This works for tilemode on or off but if you define vports within vports, this will only "zoom all" for the vports within the current one.
If you want to do different operation for different viewports, examine the information in the list returned by (vports). This is from the AutoCAD help file:
Each viewport descriptor is a list consisting of the viewport identification number and the coordinates of the viewport's lower-left and upper-right corners. If the AutoCAD system variable TILEMODE is set to 1 (on), the returned list describes the viewport configuration created with the AutoCAD VPORTS command. The corners of the viewports are expressed in values between 0.0 and 1.0, with (0.0, 0.0) representing the lower-left corner of the display screen's graphics area, and (1.0, 1.0) the upper-right corner. If TILEMODE is 0 (off), the returned list describes the viewport objects created with the MVIEW command. The viewport object corners are expressed in paper space coordinates. Viewport number 1 is always paper space when TILEMODE is off.
For example, given a single-viewport configuration with TILEMODE on, the vports function might return this:
((1 (0.0 0.0) (1.0 1.0)))
Similarly, given four equal-sized viewports located in the four corners of the screen when TILEMODE is on, the vports function might return this:
( (5 (0.5 0.0) (1.0 0.5))
(2 (0.5 0.5) (1.0 1.0))
(3 (0.0 0.5) (0.5 1.0))
(4 (0.0 0.0) (0.5 0.5)) )
The current viewport's descriptor is always first in the list. In the previous example, viewport number 5 is the current viewport.

