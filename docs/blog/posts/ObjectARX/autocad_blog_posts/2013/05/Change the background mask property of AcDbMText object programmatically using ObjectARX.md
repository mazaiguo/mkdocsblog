---
title: "Change the background mask property of AcDbMText object programmatically using ObjectARX"
date: 2013-05-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - ObjectARX
  - Unicode
description: "I need to create (or set) an AcDbMText object with the background mask turned on. How can I do so programmatically?"
author: Autodesk
---
# Change the background mask property of AcDbMText object programmatically using ObjectARX

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/change-the-background-mask-property-of-acdbmtext-object-programmatically-using-objectarx.html

## 文章内容

by Fenton Webb
Issue
I need to create (or set) an AcDbMText object with the background mask turned on. How can I do so programmatically?
Solution
We can do this both in ObjectARX and LISP.
In ObjectARX, we can use setBackgroundFill() member function of class AcDbMText to do the job. Please find the following code which toggles the background mask property of an MText entity.
void test_setBackgroundFill_MText()
{
  ads_name ename;
  ads_point p;
  // select the entity
  int res = acedEntSel(_T("Please pick an MText entity: "), ename, p );
  // if ok
  if (res == RTNORM)
  {
    AcDbObjectId oId;
    acdbGetObjectId( oId, ename );
    AcDbObjectPointer<AcDbMText> pMText(oId, AcDb::kForWrite);
      if(pMText.openStatus() == Acad::eOk)
    {
      AcCmColor color;
      if(pMText->backgroundFillOn())
      {
        pMText->setUseBackgroundColor(false);
        pMText->setBackgroundFill(false);
      }
      else
      {
        pMText->setBackgroundFill(true);
        color.setColorIndex(1);
        pMText->setBackgroundFillColor(color);
        pMText->setUseBackgroundColor(false);
      }
    }
    else
      acutPrintf(_T("\nError - you need to select an MText entity..."));
  }
}
  In LISP, we can add group code 90 and set it as 1 to turn on the background mask. If we want to use a different color than the one used last time we can add group code 63 such as (63 . 1) - RED color - as well. We can turn off the mask by removing group code 90 and all related ones such as 63, 45, 441 and 421 (if applicable). A small tip here, we can substitute the original sub list of group code 90 with (90 . 2) to turn the mask off successfully and do not need to care about other related group codes. The following LISP code demonstrates how to do so…
  (defun toggleBackgroundMaskOfAMText (en / ed)
  (setq ed (entget en))   ; Sets ed to the entity data
  (setq atom90 (assoc 90 ed))
  (if (= atom90 nil)
    ;; no 90 groud code at all
    (progn
      (setq lst90 (cons 90 1))
      (setq atom63 (cons 63 1))
      (setq ed (append ed (list atom63 lst90)))
      ;; Add the 63 group code to set the background color as 1 (RED)
    )
    (progn
      (setq maskProp (cdr atom90))
      (if (= (boole 1 maskProp 1) 1)
(setq new90 (cons 90 2))
(setq new90 (cons 90 1))
      )
      (setq ed
      (subst new90
      (assoc 90 ed) ; Toggle the value of 90 group in ed.
      ed
      )
      )
    )
  )
  (entmod ed)
  (princ)
)
(defun c:testBGMask ()
  (toggleBackgroundMaskOfAMText
    (car (entsel))
  )
)
  Here is some information about the DXF group codes related to Background Mask of MTEXT entities.
** Group code 90: Bit flags for background Mask
The possible values can be:
        kFillTextBox            = 0x1
        kFillTextBoxBackground  = 0x2
        kUseWordBreak           = 0x4
        kCheckedForUseWordBreak = 0x8
In the Background Mask dialog UI (while in the text editor or double click on the text --> right click context menu -->  [Background Mask..]), we can check the 'Use background mask' option to set the kFillTextBox bit and 'Use drawing background color' option in the 'Fill Color' group to set the kFillTextBoxBackground bit. In ARX API, We can use AcDbMText::backgroundFillOn() AcDbMText::setBackgroundFill() to get and set the kFillTextBoxBackground bit.
** Group code 63:  Fill Color
Specifies the color for the background. If it is a true color, Group code 63 gives the ACI color value and the corresponding Group code 421 gives the AcCmColor’s value.
We can specify the background color of the MTEXT in the Background Mask dialog UI. In ARX API, we can use AcDbMText::getBackgroundFillColor and AcDbMText::setBackgroundFillColor to get and read the value.
** Group code 45:  Border Offset Factor
Specifies the margin around the text for the opaque background. The value is based on the text height. A factor of 1.0 exactly fits the multiline text object. A factor of 1.5 extends the background by 0.5 times the text height.
In the Background Mask dialog UI, we can specify it in the 'Border offset factor' field. In ARX API, We can use AcDbMText::getBackgroundScaleFactor and AcDbMText::setBackgroundScaleFactor to get and set the value.
** Group code 441: Transparency color. 
The corresponding data member is of AcCmTransparency Type. This can not be controlled by the Background Mask dialog UI. But we can get or set this value using AcDbMText::getBackgroundTransparency and AcDbMText::setBackgroundTransparency methods.

## 评论

**内容**: John said...
How about LISP to toggle background mask for a dimension object? I had a routine to do this that worked a few releases ago but now it does not work (it puts a white background on the dimension text).
Reply
05/15/2013 at 01:22 PM

---
