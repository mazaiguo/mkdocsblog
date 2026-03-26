---
title: "LISP (entmake)’ing a WipeOut object in AutoCAD gives different coordinates than expected"
date: 2012-05-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - Dimension
  - Plugin
description: "Here’s one from the past I thought you might all like to see."
author: Autodesk
---
# LISP (entmake)’ing a WipeOut object in AutoCAD gives different coordinates than expected

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/lisp-entmakeing-a-wipeout-object-in-autocad-gives-different-coordinates-than-expected.html

## 文章内容

by Fenton Webb
Here’s one from the past I thought you might all like to see.
Using LISP to (entmake) a Wipeout object inside of AutoCAD… Adding the x,y,z values for group code 10 and the coordinates for the boundary (group code 14) it seems that when the wipeout is created it is not located at the specified coordinates…
The reason is because some objects use the OCS (Object Coordinate System)
Here’s a couple of examples which show how to deal specifically with the WipeOut object so that it places in the drawing as you would expect.
(defun c:makewo (/ )
  (setq ins_pt (getpoint "select a point for lower left of 2x2 wipeout"))
  ; Add 1.5 to the x and subtract .5 from the Y point
  ; With this change to the point used for the lower left
  ; the wipeout is the same as the selected point.
  (setq xVal (nth 0 ins_pt))
  (setq xVal (+ xVal 1.5))
  (setq yVal (nth 1 ins_pt))
  (setq yVal (- yVal 0.5))
 
  (entmake
    (list
      '(0 . "WIPEOUT")
      '(100 . "AcDbEntity")
      '(8 . "0")
      '(100 . "AcDbWipeout")
      (cons 10 (list xVal yVal 0.0))
      (cons 11 '(0.0 1.0 0.0))
      (cons 12 '(1.0 0.0 0.0))
      (cons 13 '(1.0 1.0 0.0))
      '(70 . 7)
      '(280 . 1)
      '(281 . 50)
      '(282 . 50)
      '(283 . 0)
      '(71 . 2); 1=RECTANGLE 2=POLYGON
      '(91 . 5); NUMBER OF VERTICIES TO FOLLOW
      ; Note: X and Y are reversed compared to the UCS
      ; the origin of these points is the lower right
      ; This is the lower right corner
      (cons 14 '(0.0 0.0 0.0))
      ;x and y are reversed 2.0 is the first y coordinate
      ;on the upper right corner
      (cons 14 '(2.0 0.0 0.0))
      ;This is the upper left corner
      ; Notice that the second coordinate is the X value
      ; and that a positive value moves it to the left which is
      ; the opposite of the default UCS.
      (cons 14 '(2.0 2.0 0.0))
      ;This is the lower left corner
      (cons 14 '(0.0 2.0 0.0))
      ;This completes the boundary of the wipeout
      ;needs to be the same as the first coordinate
      (cons 14 '(0.0 0.0 0.0))
      )
    )
  )

(defun c:makewo2 ()
  (setq ins_pt (getpoint "select a point"))
  (setq xVal (nth 0 ins_pt))
  (setq xVal (+ xVal 1.5))
  (setq yVal (nth 1 ins_pt))
  (setq yVal (- yVal 0.5))
  (entmake
    (list
      '(0 . "WIPEOUT")
      '(100 . "AcDbEntity")
      '(8 . "0")
      '(100 . "AcDbWipeout")
      (cons 10 (list xVal yVal 0.0))
      (cons 11 '(0.0 1.0 0.0))
      (cons 12 '(1.0 0.0 0.0))
      (cons 13 '(1.0 1.0 0.0))
      '(70 . 7)
      '(280 . 1)
      '(281 . 50)
      '(282 . 50)
      '(283 . 0)
      '(71 . 2)
      '(91 . 9)
      (cons 14 '(0.7888 -0.9376 0.0))
      (cons 14 '(-0.9336 0.7792 0.0))
      (cons 14 '(-0.9376 3.2112 0.0))
      (cons 14 '(0.7792 4.9336 0.0))
      (cons 14 '(3.2112 4.9376 0.0))
      (cons 14 '(4.9336 3.2208 0.0))
      (cons 14 '(4.9376 0.7888 0.0))
      (cons 14 '(3.2208 -0.9336 0.0))
      (cons 14 '(0.7888 -0.9376 0.0))

      )
    )
  )

