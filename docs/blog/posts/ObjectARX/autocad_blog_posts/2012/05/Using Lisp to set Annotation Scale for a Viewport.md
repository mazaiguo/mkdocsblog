---
title: "Using Lisp to set Annotation Scale for a Viewport"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoLISP
  - C++
  - COM
description: "There is no AutoLISP function or ActiveX method to set the Annotation scale for a viewport. It is not possible to do this by manipulating the XReco..."
author: Autodesk
---
# Using Lisp to set Annotation Scale for a Viewport

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/using-lisp-to-set-annotation-scale-for-a-viewport.html

## 文章内容

By Gopinath Taget
There is no AutoLISP function or ActiveX method to set the Annotation scale for a viewport. It is not possible to do this by manipulating the XRecord named “ASDK_XREC_ANNOTATION_SCALE_INFO” of the Extension dictionary of the viewport either. The way the annotation scale is controlled is by a DXF code on the XRecord with a hard pointer to an AcDbScale object.  Because entmod is unsupported for objects in a dictionary there is not a way to change the scale for a viewport using AutoLISP.
A work around is to use ObjectARX or the .NET API to change the annotation scale of the viewport. The function to use is in ObjectARX is AcDbViewport::setAnnotationScale().  In .NET this is wrapped in the Viewport.AnnotationScale Property. You can create a function that can be called from your LISP code to set the scale. Here is a VB.NET example:
<LispFunction("ChangeVPScale")> _
Public Shared Function changeVPScale(ByVal myLispArgs As ResultBuffer) _
As ResultBuffer
    Dim rbfResult As ResultBuffer = Nothing
  Dim db As Database = 
   HostApplicationServices.WorkingDatabase
  Dim tm As Transaction =
   db.TransactionManager.StartTransaction
    Try
    Dim doc as Document =
     Autodesk.AutoCAD.ApplicationServices.Application.
                          DocumentManager.MdiActiveDocument
      Dim ed As Editor = doc.Editor
    If myLispArgs Is Nothing Then
      ' Write a message on the AutoCAD command line
      ed.WriteMessage("No Arguments passed in" & vbLf)
      Return myLispArgs
    Else
      Dim myArgs As TypedValue() = myLispArgs.AsArray()
      ' Ensure that an ObjectId was passed in
      If myArgs(0).TypeCode = LispDataType.ObjectId Then
        ' Ensure that a Viewport was selected by the user   
        Dim dbObj As DBObject
        Dim objID As ObjectId = myArgs(0).Value
        dbObj = tm.GetObject(objID, OpenMode.ForWrite)
        If TypeOf dbObj Is Viewport Then
          Dim viewPrt As Viewport
          viewPrt = CType(dbObj, Viewport)
            If myArgs(1).TypeCode = LispDataType.Text Then
              Dim contextManager As ObjectContextManager =
              db.ObjectContextManager
            If contextManager <> Nothing Then
              'now get the Annotation Scaling context
              'collection (named
              'ACDB_ANNOTATIONSCALES_COLLECTION)
              Dim contextCollection As  
              ObjectContextCollection =
                contextManager.GetContextCollection
                ("ACDB_ANNOTATIONSCALES")
              '
              If contextCollection <> Nothing Then
                Dim objCol As ObjectContext
                For Each objCol In contextCollection
                  If objCol.Name = myArgs(1).Value Then
                    ed.WriteMessage(objCol.Name.ToString())
                    viewPrt.AnnotationScale = objCol
                      tm.Commit()
                    rbfResult = New ResultBuffer( _
                                New TypedValue(CInt(5005), _
                              "Changed the Annotation scale
                               of the ViewPort"))
                    Return rbfResult
                    Exit For
                  End If
                Next
                Else
                tm.Abort()
                rbfResult = New ResultBuffer( _
                New TypedValue(CInt(5005), "Problem getting
                               scale collection"))
                Return rbfResult
              End If
            End If
          Else
            rbfResult = New ResultBuffer( _
                        New TypedValue(CInt(5005), "second
                                       argument not text"))
            Return rbfResult
          End If
        Else
          ' Return do not have a Viewport
          rbfResult = New ResultBuffer( _
                      New TypedValue(CInt(5005),
                 "Selected entity not ViewPort"))
          tm.Abort()
          Return rbfResult
        End If
      Else
        ' Return do not have a Viewport
        rbfResult = New ResultBuffer( _
                    New TypedValue(CInt(LispDataType.Text),
                      "Argument passed in not an ObjectId"))
        tm.Abort()
        Return rbfResult
      End If
    End If
  Catch ex As System.Exception
    System.Diagnostics.Debug.Write(ex.ToString())
  Finally
    tm.Dispose()
  End Try
  Return rbfResult
End Function
  And the LISP function:
<code_Begin>
(defun changescale ( / ename-ViewPort )
  (setq ename-ViewPort(car (entsel "\nPick a Viewport: ")))
  (changevpscale ename-ViewPort "1:2")
  (command "REGENALL")
  )

## 评论

**内容**: Emmanuel Garcia said...
Gopinath, Has this changed since 2012? Warm regards from Los Angeles, Emmanuel
Reply
02/13/2015 at 12:19 PM

---
**内容**: Marcin Ciechomski said...
Thank you Gopinath for your post. Because I'm not familiar with ObjectARX I had to dig deeper an I have found the way to change it with ActiveX and Visual Lisp. Emmanuel, take a look here: http://u-cad.eu/tips/how-to-set-annotation-scale-of-the-viewport-with-visual-lisp/
Reply
11/03/2015 at 11:02 AM

---
