---
title: "LISP: How do I convert a Polygon Mesh into polylines?"
date: 2012-09-01
categories:
  - AutoLISP
tags:
  - AutoLISP
  - Dimension
  - Plugin
  - Polyline
description: "Using Visual LISP, is there a way to reduce Polygon Meshs (3D Meshs) into regular polylines or lines?"
author: Autodesk
---
# LISP: How do I convert a Polygon Mesh into polylines?

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/lisp-how-do-i-convert-a-polygon-mesh-into-polylines.html

## 文章内容

By Philippe Leefsma
Q:
Using Visual LISP, is there a way to reduce Polygon Meshs (3D Meshs) into regular polylines or lines?
A:
While Visual LISP has no built-in method for converting a polygon mesh to polylines (or lines), you can explode it, and then draw polylines using the coordinates of the resulting 3dFaces.  The sample code below demonstrates this.  It searches modelspace for polygon mesh objects, explodes them into 3dFaces, draws polylines (adding vertices to the the 3dFace coordinates), and deletes the original mesh (and faces):
(defun c:XplPgMesh
(/ oApp oDoc oMSp oObj vXplObj aXplObj oObjLst oObj2 vCoords o3dPline)
   (VL-LOAD-COM)
   (setq oApp (vlax-get-acad-object)
           oDoc (vla-get-activedocument oApp)
           oMSp (vla-get-modelspace oDoc)
   ) ;setq
   (vlax-for oObj oMsp
    (if (= (vla-get-objectname oObj) "AcDbPolygonMesh")
     (if (setq vXplObj (vla-explode oObj))
       (progn
         (setq aXplObj (vlax-variant-value vXplObj))
          (if (not (minusp (vlax-safearray-get-u-bound aXplObj 1)))
           (progn
              (setq oObjLst (vlax-safearray->list aXplObj))
               (foreach oObj2 oObjLst
                 (if (= (vla-get-objectname oObj2) "AcDbFace")
                   (progn
                     (setq vCoords (vla-get-coordinates oObj2)
                           o3dPline (vla-Add3DPoly oMSp vCoords)
                     ) ;setq
                     (vlax-put-property o3dPline 'Closed :vlax-true)
                   (vla-delete oObj2)
                  (vlax-release-object o3dPline)
                 ) ;progn
                ) ;if
              ) ;foreach
            (foreach itm oObjLst (vlax-release-object itm))
           ) ;progn
          ) ;if
        (vla-delete oObj)
       ) ;progn
      ) ;if
      ) ;if
   ) ;vlax-for
   (princ)
)

