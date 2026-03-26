---
title: "Arrange Ribbon buttons into columns"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - CUI
  - Plot
description: "I would like to organize my Ribbon buttons into 2 columns like this, similar to the "Manage - Applications" panel:"
author: Autodesk
---
# Arrange Ribbon buttons into columns

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/arrange-ribbon-buttons-into-columns.html

## 文章内容

By Adam Nagy
I would like to organize my Ribbon buttons into 2 columns like this, similar to the "Manage - Applications" panel:

How could I do it?
Solution
First of all, having a look at the panels in the CUI dialog gives you an idea how they are built up and also provides the id of the panel, which enables you to check through the API what exact components they contain:

The below sample also contains a function called IterateContent, which prints out the content of the Ribbon panel whose id you specify.
The list will be printed in the Output window of Visual Studio. Make sure that the "Exceptions" item is unticked in the context menu of that window, otherwise the result will be scattered and a bit difficult to read:

Now that you can see the structure of the panel, you can easily organize your items the same way. Here is the full source code:
Imports Autodesk.AutoCAD.Runtime
Imports acApp = Autodesk.AutoCAD.ApplicationServices.Application
Imports Autodesk.Windows
Imports System.Drawing
Imports System.IO
  Public Class Class1
  Implements IExtensionApplication
    Public Sub Initialize() Implements IExtensionApplication.Initialize
    IterateContent()
    CreateRibbon()
  End Sub
    Public Sub Terminate() Implements IExtensionApplication.Terminate
  End Sub
    Private Sub IterateContentRecursive(ByVal obj As Object)
    Debug.Indent()
      Dim t As Type = obj.GetType()
    Debug.Print(t.Name)
      Try
      Dim coll As RibbonItemCollection = _
        t.InvokeMember( _
          "Items", Reflection.BindingFlags.GetProperty, _
          Nothing, obj, Nothing)
        For Each item As RibbonItem In coll
        IterateContentRecursive(item)
      Next
    Catch ex As System.MissingMethodException
    End Try
      Debug.Unindent()
  End Sub
    Private Sub IterateContent()
    Dim ribCntrl As RibbonControl = ComponentManager.Ribbon
      ' get the "Manage - Applications" panel
    Dim panel As RibbonPanel = _
      ribCntrl.FindPanel("ID_PanelScriptsAndMacros", False)
      IterateContentRecursive(panel.Source)
  End Sub
    Private Sub CreateRibbon()
    Dim ribCntrl As RibbonControl = ComponentManager.Ribbon
    Dim ribTab As New RibbonTab()
    ribTab.Title = "TestRibbon"
    ribTab.Id = "TestRibbon"
    ribCntrl.Tabs.Add(ribTab)
    ribTab.IsActive = True
      addContent(ribTab)
  End Sub
    Private Sub addContent(ByVal ribTab As RibbonTab)
    Dim ribSourcePanelTest As New RibbonPanelSource
    ribSourcePanelTest.Title = "Test Panel"
      Dim ribPanel As New RibbonPanel()
    ribPanel.Source = ribSourcePanelTest
    ribTab.Panels.Add(ribPanel)
      '***Create buttons
    Dim ribButtonBig As RibbonButton = New RibbonButton
    ribButtonBig.IsToolTipEnabled = True
    ribButtonBig.ToolTip = "Big button vertical"
    ribButtonBig.Orientation = Windows.Controls.Orientation.Vertical
    ribButtonBig.LargeImage = LoadImage(My.Resources.question)
    ribButtonBig.Size = RibbonItemSize.Large
    ribButtonBig.Text = "Big button vertical"
    ribButtonBig.CommandParameter = "BigButtonCommand "
    ribButtonBig.ShowText = True
    ribButtonBig.Image = LoadImage(My.Resources.question)
    ribButtonBig.CommandHandler = New AdskCommandHandler()
      Dim ribButtonSmall1 As RibbonButton = New RibbonButton
    ribButtonSmall1.IsToolTipEnabled = True
    ribButtonSmall1.ToolTip = "Small button horizontal"
    ribButtonSmall1.Orientation = Windows.Controls.Orientation.Horizontal
    ribButtonSmall1.LargeImage = LoadImage(My.Resources.question)
    ribButtonSmall1.Size = RibbonItemSize.Standard
    ribButtonSmall1.Text = "Small button horizontal"
    ribButtonSmall1.CommandParameter = "SmallButton1 "
    ribButtonSmall1.ShowText = True
    ribButtonSmall1.Image = LoadImage(My.Resources.questionsmall)
    ribButtonSmall1.CommandHandler = New AdskCommandHandler()
      Dim ribButtonSmall2 As RibbonButton = ribButtonSmall1.Clone()
    ribButtonSmall2.CommandParameter = "SmallButton2 "
      Dim ribButtonSmall3 As RibbonButton = ribButtonSmall1.Clone()
    ribButtonSmall3.CommandParameter = "SmallButton3 "
      Dim ribButtonSmall4 As RibbonButton = ribButtonSmall1.Clone()
    ribButtonSmall4.CommandParameter = "SmallButton4 "
      Dim ribButtonSmall5 As RibbonButton = ribButtonSmall1.Clone()
    ribButtonSmall5.CommandParameter = "SmallButton5 "
      Dim ribButtonSmall6 As RibbonButton = ribButtonSmall1.Clone()
    ribButtonSmall6.CommandParameter = "SmallButton6 "
      'add the buttons in an organized way:
    ' first the big button then the small ones placed in two separate columns
      Dim subPanel1 As New RibbonRowPanel
    subPanel1.Items.Add(ribButtonSmall1)
    subPanel1.Items.Add(New RibbonRowBreak)
    subPanel1.Items.Add(ribButtonSmall2)
    subPanel1.Items.Add(New RibbonRowBreak)
    subPanel1.Items.Add(ribButtonSmall3)
      Dim subPanel2 As New RibbonRowPanel
    subPanel2.Items.Add(ribButtonSmall4)
    subPanel2.Items.Add(New RibbonRowBreak)
    subPanel2.Items.Add(ribButtonSmall5)
    subPanel2.Items.Add(New RibbonRowBreak)
    subPanel2.Items.Add(ribButtonSmall6)
      ribSourcePanelTest.Items.Add(ribButtonBig)
    ribSourcePanelTest.Items.Add(subPanel1)
    ribSourcePanelTest.Items.Add(subPanel2)
  End Sub
    Private Shared Function LoadImage(ByVal imageToLoad As Bitmap) _
  As Windows.Media.Imaging.BitmapImage
    Dim pic As Bitmap = imageToLoad
    Dim ms As New MemoryStream()
    pic.Save(ms, Imaging.ImageFormat.Png)
    Dim bi As New Windows.Media.Imaging.BitmapImage()
    bi.BeginInit()
    bi.StreamSource = ms
    bi.EndInit()
    Return bi
  End Function
End Class
  Public Class AdskCommandHandler
  Implements System.Windows.Input.ICommand
    Public Function CanExecute(ByVal parameter As Object) _
  As Boolean Implements System.Windows.Input.ICommand.CanExecute
    Return True
  End Function
    Public Event CanExecuteChanged( _
    ByVal sender As Object, ByVal e As System.EventArgs) _
  Implements System.Windows.Input.ICommand.CanExecuteChanged
    Public Sub Execute(ByVal parameter As Object) _
  Implements System.Windows.Input.ICommand.Execute
    Dim ribBtn As RibbonButton = TryCast(parameter, RibbonButton)
    If ribBtn IsNot Nothing Then
      acApp.DocumentManager.MdiActiveDocument.SendStringToExecute( _
          ribBtn.CommandParameter, True, False, True)
    End If
  End Sub
End Class
And here is the result:

## 评论

**内容**: Craig said...
Thanks Adam, this helped me layout and create my ribbon.
Reply
05/01/2014 at 06:54 AM

---
