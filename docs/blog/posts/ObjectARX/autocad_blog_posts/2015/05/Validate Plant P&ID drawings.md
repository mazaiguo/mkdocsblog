---
title: "Validate Plant P&ID drawings"
date: 2015-05-01
categories:
  - AutoCAD
tags:
  - API
description: "Inside Plant P&ID we can Validate, via ribbon Home>Validate>Run Validation or right-click on a drawing and select “Validate”. More details here."
author: Autodesk
---
# Validate Plant P&ID drawings

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/validate-plant-pid-drawings.html

## 文章内容

By Augusto Goncalves
Inside Plant P&ID we can Validate, via ribbon Home>Validate>Run Validation or right-click on a drawing and select “Validate”. More details here.
Using APIs there is a ValidationSingleton object that has a ValidateDrawings or ValidareProject method. After run this, the Errors property will contain a list of validation errors. Actually there is one class for each type, so you’ll need to cast or, like in the sample below, simply get the error name.
Important: this API method will *only* show the validation errors after you run it via built-in command.
[CommandMethod("validateDrawings")]
public static void CmdValidateDrawings()
{
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
 
  // Validation manager
  AcPpValidationManager vmgr = ValidationSingleton.Manager;
 
  // prepare a list of drawings
  AcPpValidationAllOpenedDrawingManager dsd =
    new AcPpValidationAllOpenedDrawingManager();
  foreach (Document doc in Application.DocumentManager)
  {
    dsd.Add(doc.Database);
  }
 
  // clear the list of error 
  // (in case you're running several times)
  vmgr.Errors.Clear();
 
  // the actual validation occurs here
  vmgr.ValidateProject(dsd);
 
  // now check the list of errors
  if (vmgr.Errors.Count > 0)
  {

    AcPpValidationErrorCollection errorList = vmgr.Errors;
    foreach (IAcPpValidationError item1 in errorList)
    {
      // can be classes from namespace
      // Autodesk.ProcessPower.PnIDDwgValidation          
 
 
      // for now, let's write the error class name
      ed.WriteMessage("\n{0}", 
        item1.GetType().Name.PascalCaseToText());
    }
  }
}

// nice sample Regular expression from here. 
public static string PascalCaseToText(this string text)
{
  return System.Text.RegularExpressions.Regex.Replace(
    text, "([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))", "$1 ");
}

## 评论

**内容**: Artem said...
Augusto, thank you very much for the article!
Please, anybody help me! Is there any programmatic way to validate PnID Pipe Line Segments and P3D Pipe Run Elements (pipe, elbows, tees, reducers, ect.). There is no "Validate" column for PnID Pipe Line Segments in Project Setup.
I've written about it here
http://forums.autodesk.com/t5/autocad-plant-3d-forum/validation-mapping/m-p/6574957#M23539
and here
http://forums.autodesk.com/t5/autocad-plant-3d-p-id-ideas/validation-mapping/idi-p/6597784
But I have not got a useful information. I really need to realize it.
Thanks in advance.
Reply
12/16/2016 at 01:10 AM

---
**内容**: Aayushi Verma said...
Such great information you have shared with us. Can you share the details of the latest flats in Bhopal?
Reply
02/27/2020 at 11:07 PM

---
