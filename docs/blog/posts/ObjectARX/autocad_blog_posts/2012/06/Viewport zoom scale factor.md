---
title: "Viewport zoom scale factor"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - C++
  - DXF
  - ObjectARX
description: "To get the viewport zoom scale factor, you can query for the 'CustomScale' property on the paper space viewport entity. Alternatively, get the view..."
author: Autodesk
---
# Viewport zoom scale factor

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/viewport-zoom-scale-factor-.html

## 文章内容

To get the viewport zoom scale factor, you can query for the 'CustomScale' property on the paper space viewport entity. Alternatively, get the viewport paperspace height, which is DXF group code 41. The model space viewport height is contained in the viewport's extended entity data and is the 2nd DXF group code1040. Extended entity data can be extracted into 'resbuf' result buffers, however, ObjectARX provides AcDbViewport::viewHeight() that gets this value directly. Therefore, the viewport entity (AcDbViewport) zoom scale factor is calculated as :
group_41 / 2nd_group_1040 (or pspace_height / mspace_height).
The following code fragments demonstrates how to calculate the zoom scale factor for an AcDbViewport entity:
(defun c:ZoomScaleFactor (/ a_app a_doc obj a_pvp msp_ht )
    (vl-load-com)
    (setq    a_app (vlax-get-acad-object)
            a_doc (vla-get-ActiveDocument a_app)
            obj   (vlax-ename->vla-object (car (entsel "Select a pviewport entity: ")))
    )
    (vla-put-mspace a_doc :vlax-true)
      (setq    a_pvp  (vla-get-ActivePViewport a_doc)
            pvp_ht (vla-get-height a_pvp)
            msp_ht (GETVAR "VIEWSIZE")
            zsf   (vla-get-customscale a_pvp)
    )
      (princ (strcat "pvp height : " (rtos pvp_ht)))
    (princ (strcat "msp height : " (rtos msp_ht)))
      (vla-put-mspace a_doc :vlax-false)
      (print (strcat "Viewport Zoom scale factor = " (rtos (/ pvp_ht msp_ht) 2 2)))
      (print (strcat "Viewport Zoom scale factor = " (rtos zsf)))
      (princ)
)
Here is the ObjectARX equivalent of the same code :
ads_name ename;
ads_point pt;
int rc = acedEntSel(_T("\nSelect Viewport entity "), ename, pt);
if(rc != RTNORM)
{
    acutPrintf(_T("\nError selecting entity "));
    return;
}
  AcDbObjectId entId;
Acad::ErrorStatus es = acdbGetObjectId(entId, ename);
  AcDbEntity* pEnt;
es = acdbOpenObject(pEnt, entId, AcDb::kForRead);
AcDbViewport* pVPEnt = AcDbViewport::cast(pEnt);
if(!pVPEnt)
{
    acutPrintf(_T("\nEntity is not a Viewport entity "));
    pEnt->close();
    return;
}
  // Get the paper space viewport's height
// DXF group code 41
double psht = pVPEnt->height();
  // Get the model space viewport's height
// Extended Entity Data 2nd 1040 DXF group code under 'ACAD'
double msht = pVPEnt->viewHeight();
  // Calculate the viewport entity zoom factor
// The ZOOM factor is calculated with the following formula:
// group_41 / 2nd_group_1040 (or pspace_height / mspace_height).
double xpsf = psht / msht;
  acutPrintf(_T("\nViewport Zoom scale factor = %.2lf "), xpsf);
  // OR
  acutPrintf(_T("\nViewport Zoom scale factor = %.2lf"), pVPEnt->customScale());
  pVPEnt->close();

## 评论

**内容**: Irné Barnard said...
The 2 codes are not exactly equivalent. In the Lisp version you're setting the ActiveSpace to model space and then obtaining the active viewport. This might not be the same viewport as selected if there's more than one VP on the current layout. For that you have to ensure that the CVPort system variable matches the selected viewport's index number (as in the 69 DXF code of the viewport).
Unfortunately the ActiveX object doesn't seem to have a property to the "Viewport ID". So you'd need the entget DXF list as well as the vla-object to go about it this route. In which case I think you could simply have used the XData in any case - quite easy to get at by adding the optional argument to entget to obtain xdata as well.
Also there's some error checking you do in the C++ version but not in Lisp. What if the user picks an empty spot, presses enter or picks an entity which is not a viewport?
Reply
06/26/2012 at 06:32 AM

---
**内容**: Balaji said in reply to Irné Barnard...
Hi Irné,
Thanks for your comments.
By "equivalent code", I did not mean a 1:1 correspondence. Only the core idea of getting the zoom scale factor remains.
The intention of the post is to demonstrate a way to get the zoom scale factor and all surrounding error checks that might be needed to make it complete is usally very limited.
There is usually very less/no error checking in the code snippets that we post.
Reply
06/26/2012 at 06:29 PM

---
