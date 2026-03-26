---
title: "create a view with a twist angle using a paper space vport?"
date: 2013-03-01
categories:
  - AutoCAD COM
tags:
  - COM
description: "I need to create a view with ActiveX that shows our drawing in a twisted view. I do not see any type of property of a view object that will create ..."
author: Autodesk
---
# create a view with a twist angle using a paper space vport?

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/create-a-view-with-a-twist-angle-using-a-paper-space-vport.html

## 文章内容

By Xiaodong Liang
Issue
I need to create a view with ActiveX that shows our drawing in a twisted view. I do not see any type of property of a view object that will create a view and rotate the view at a specified twist angle.
Solution
The View object does not have a Twist property, and the Center, Target and Direction of a View object will not allow the same effect as a Twist (With DVIEW). There is a logged wishlist to add this property.
One workaround is to use a paper space viewport and use its TwistAngle property. The following is an example that uses a paper space view port to create a view with a twist angle.
    Sub createViewWithTwistAngle(AcadApp As AcadApplication)
' This example creates a new paperspace viewport.
' It then sets the viewdirection, and the TwistAngle
' Then view is then created using SendCommand (VIEW)
' The viewport erased it is only created to set the
' TwistAngle
            Dim viewportObj As AcadViewport
        Dim myView As AcadView
        Dim int1 As Integer
        Dim ThisDrawing As AcadDocument
        ThisDrawing = AcadApp.ActiveDocument
            ' Define the pviewport
        Dim center(0 To 2) As Double
        center(0) = 3 : center(1) = 3 : center(2) = 0
          Dim width As Double
        Dim height As Double
        width = 4
        height = 4
          ' Change from model space to paperspace
        ThisDrawing.ActiveSpace =  
                  AcActiveSpace.acPaperSpace
          ' Create the pviewport
        Dim pviewportObj As AcadPViewport
        pviewportObj = 
     ThisDrawing.PaperSpace.AddPViewport(center,
                                         width,
                                        height)
        pviewportObj.Display(True)
        pviewportObj.ViewportOn = True
        ThisDrawing.MSpace = True
        ThisDrawing.ActivePViewport = pviewportObj
          ' Change the viewing direction of the ViewPort
        Dim NewDirection(0 To 2) As Double
        NewDirection(0) = -1 :
        NewDirection(1) = -1 :
        NewDirection(2) = 1
        pviewportObj.Direction = NewDirection
          ' Set the twist angle for the viewport
        pviewportObj.TwistAngle = 0.56999999999999995
            ' Remove view named test1
        For int1 = 0 To ThisDrawing.Views.Count - 1
            If ThisDrawing.Views(int1).Name = "my_test_view" Then
                ThisDrawing.Views(int1).Delete()
            End If
        Next int1
            ThisDrawing.Application.ZoomExtents()
          ' Create a view
        ThisDrawing.SendCommand("-view" & Chr(13) &
                                "Save" & Chr(13) &
                                "my_test_view" &
                                Chr(13))
          ' Erase the paper space view port
        pviewportObj.Delete()
          ThisDrawing.ActiveSpace =  
                  AcActiveSpace.acModelSpace
          ' Reference model space viewport and set the
          view to the one
        ' created above
        viewportObj = ThisDrawing.ActiveViewport
        myView =
            ThisDrawing.Views.Item("my_test_view")
        viewportObj.SetView(myView)
        ThisDrawing.ActiveViewport = viewportObj
      End Sub

