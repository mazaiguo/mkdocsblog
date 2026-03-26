---
title: "Get the size of a rectangular clipped image"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Dimension
description: "A short explanation of the raster image group codes is useful for this task.  The group code is followed by an explanation of what it means:"
author: Autodesk
---
# Get the size of a rectangular clipped image

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/get-the-size-of-a-rectangular-clipped-image.html

## 文章内容

By Augusto Goncalves
A short explanation of the raster image group codes is useful for this task.  The group code is followed by an explanation of what it means:
11:
This the the U-vector of a single image pixel in x direction.  The length of this vector is the size of a pixel in x-direction.
12:
This is the so called V-vector.  It's the same as group code 11 for the y-direction.
13:
This is the size of the raster image, specified in pixels.  To get the size of the image in AutoCAD coordinates, you have to multiply the x-size and y-size with the length of the U- and V-vector.
280:
This flag specifies if the raster image is clipped. 0 = not clipped; 1 = clipped
71:
This is the type of clipping: '1' = rectangular clipped, '2' = clipped with a polyline
14:
This group code contains the clipping coordinates in image pixels.  There can be more than one group code 14 attached to a raster image.  If the raster image's clipping mode is rectangular, group code 14 exists twice.  The first group code 14 defines the upper left corner, and the second group code 14 defines the lower right corner of the clipping rectangle, in terms of image pixels.
If the raster image is clipped with an polyline, then the group code 14 is repeated a minimum of three times and contains the vertices (sequential order) of the clipping polyline.  The following information is needed to extract the clipping rectangle coordinates:
1. The clipping coordinates, defined by group code 14, are moved by -0.5, -0.5.
    To get the correct AutoCAD coordinates, you have to add 0.5, 0.5 to the coordinates.
2. The x coordinate defined in group code 14 are measured from the left side of
    the image and the y coordinate of group code 14 are measured from the top of the image.
The following AutoLISP function extracts the size of a rectangular clipped raster image. Note: This function only works with raster images in which the Object Coordinate Systems (OCS) is aligned with the AutoCAD World Coordinate System (WCS). Please make sure that the current User Coordinate System (UCS) is set to the World Coordinate System (WCS) before executing this routine.
(defun c:getimagesize ()
   (setq img (entget (car (entsel "Select image: "))))
   (if (/= img NIL)
      (progn
         (if (equal (cdr (assoc 0 img)) "IMAGE")
            (progn
               (setq u (nth 0 (cdr (assoc 11 img)))
                     v (nth 1 (cdr (assoc 12 img)))
                     isClipped (cdr (assoc 280 img))
                     pos (cdr (assoc 10 img))
                     posX (nth 0 pos)
                     posY (nth 1 pos)
               )
               (if (= isClipped 1)
                  (progn
                     (princ "\nImage is clipped.")
                     (setq isRectClipped (cdr (assoc 71 img)))
                     (if (= isRectClipped 1)
                        (progn
                           (setq clip1 
                                   (cdr (assoc 14 img))
                                 clip2
                                   (cdr (last img))
                                 ySize
                                   (car (cdr (cdr (assoc 13 img))))
                           )
                           (setq p1x
                               (+ (* (+ (nth 0 clip1) 0.5) u) posX)
                               p1y
                               (* (+ (nth 1 clip1) 0.5) v)
                               p2x
                               (+ (* (+ (nth 0 clip2) 0.5) u) posX)
                               p2y
                               (* (+ (nth 1 clip2) 0.5) v)
                               p1y 
                               (+ (- (* v ySize) p1y) posY)
                               p2y
                               (+ (- (* v ySize) p2y) posY)
                           )
                           (princ "\nCoordinates of image: ")
                           (princ p1x)
                           (princ ", ")
                           (princ p1y)
                           (princ "  ")
                           (princ p2x)
                           (princ ", ")
                           (princ p2y)
                        )
                        (princ 
                         "\nCannot handle polygonal clipped images."
                        )
                     )
                  )
                  (progn
                     (princ "\nImage not clipped.")
                     (setq size (cdr (assoc 13 img)))
                     (setq p1x posX
                           p1y posY
                           p2x (+ (* (nth 0 size) u) p1x)
                           p2y (+ (* (nth 1 size) v) p1y)
                     )
                     (princ "\nCoordinates of image: ")
                     (princ p1x)
                     (princ ", ")
                     (princ p1y)
                     (princ "    ")
                     (princ p2x)
                     (princ ", ")
                     (princ p2y)
                  )
               )
            )
            (princ "\nNot an image selected.")
         )
      )
   )
   (princ)
)

