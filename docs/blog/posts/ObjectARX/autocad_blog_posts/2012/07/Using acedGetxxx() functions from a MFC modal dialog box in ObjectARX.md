---
title: "Using acedGetxxx() functions from a MFC modal dialog box in ObjectARX"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - C++
  - CUI
  - ObjectARX
  - Plugin
description: "When showing a modal dialog box, your plug-in may require the use of acedGetxxx() functions to accept user input."
author: Autodesk
---
# Using acedGetxxx() functions from a MFC modal dialog box in ObjectARX

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-acedgetxxx-functions-from-a-mfc-modal-dialog-box-in-objectarx.html

## 文章内容

By Balaji Ramamoorthy
When showing a modal dialog box, your plug-in may require the use of acedGetxxx() functions to accept user input.
Here are the steps to get user input from the button click of a modal dialog :
1) Derive your MFC dialog from one of the inbuilt ObjectARX MFC dialog classes such as CAcUiBaseDialog
2) Use the "BeginEditorCommand" and "CompleteEditorCommand" methods of the CAcUiBaseDialog class. As an example, when a button in the modal dialog is clicked, you may accept the point input as shown in the following code snippet from the button clicked handler :
void MyInputDlg::OnPickPointButtonClicked()
{
    // call the CAdUiBaseDialog derived method...
    BeginEditorCommand();
      // Accept input...
    ads_point pt ;
      acedGetPoint
    (
        NULL,
        ACRX_T("\nPick a point: "),
        pt
    );
      acutPrintf
    (
        ACRX_T("\nYou picked (%.2lf, %.2lf, %.2lf,)\n"),
        pt [X],
        pt [Y],
        pt [Z]
    ) ;
      // Restore the dialog
    CompleteEditorCommand();
}

