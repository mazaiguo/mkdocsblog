---
title: "Using AutoCAD WPF Data binding collection properties to export to Excel in VB.NET"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Hatch
  - Layer
description: "I recently saw Kean’s blog posting on Getting the list of hatch patterns available in the current AutoCAD drawing using .NET and wondered if I shou..."
author: Autodesk
---
# Using AutoCAD WPF Data binding collection properties to export to Excel in VB.NET

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/using-autocad-wpf-data-binding-collection-properties-to-export-to-excel-in-vbnet.html

## 文章内容

By Fenton Webb
I recently saw Kean’s blog posting on Getting the list of hatch patterns available in the current AutoCAD drawing using .NET and wondered if I should try to use the AutoCAD WPF data binding UIBindings.Collections class to do something similar.
You may have already started using WPF inside of AutoCAD and in your travels hooked your WPF UI data binding into the Autodesk.AutoCAD.ApplicationServices.Application.UIBindings.Collections namespace. If you haven’t, it’s definitely time to check it out. What it provides is a list of commonly used AutoCAD data type collections, primarily used by the AutoCAD Ribbon. These collections can be very easily bound to your own UI using WPF data binding making UI programming amazingly beautiful to create and work with, and super easy (once you have climbed over the fairly large learning curve )
  Just as a WPF background task for you, here are my Using Windows Presentation Foundation in AutoCAD and the Part 2 from Autodesk University which talk about  WPF inside of AutoCAD and also binding your own UI to UIBindings.Collections.
  Anyway, I figured this UIBindings.Collections layer could be utilized in the same way that Kean did for his Hatch patterns listing, but this time, for a little utility which exports to Microsoft Excel. I got the idea from a recent case submitted to our ADN DevHelp online system, in VB.NET though so as I’m a C kind of guy please excuse any VB.NET inefficiencies
Now I think you may find that it’s not quite as easy as you’d think to explore these name spaces by hand, a fairly deep understanding of the underlying interfaces is needed, so let me try and explain by looking at UIBindings.Collections.Layers.
We’re going to try and loop all of the Layers in the current drawing in order to extract the Layer Name property from them, how can we do this. So, the Layers property is of type Autodesk.AutoCAD.Windows.Data.DataItemCollection. This contains an array of System.ComponentModel.ICustomTypeDescriptor. Next is where exploring with IntelliSense may become a little tricky, what you need to do is from your ICustomTypeDescriptor is, you need to get all the properties from it, find the property name that you want the value of, and then extract the value…
Here’s how it’s done with code:
' get all of the Layer Names in the current DWG
For Each desc As System.ComponentModel.ICustomTypeDescriptor In dataItemCollection
  ' extract the layer table record property we want
  Dim propertyValue = desc.GetProperties()("Name").GetValue(desc)
  As you can see, it’s super simple when you know how, and with just two lines of code – very cool!
So onto the exporting of the data held in the UIBindings.Collections namespace to Excel. To connect my little AutoCAD VB.NET application to a currently running Excel application, or if one does not exist, to then start one up I use this code:
Try
  If Process.GetProcessesByName("Excel").Length > 0 Then
    app = CType(GetObject(, "Excel.Application"), Excel.Application)
    ' Else createObject
  Else
    app = New Excel.Application
  End If
  app.Visible = True
  workbook = app.Workbooks.Add(1)
  worksheet = DirectCast(workbook.Sheets(1), Excel.Worksheet)
  Catch e As Exception
    Console.Write("Error")
  Finally
End Try
  Actually, I have to confess, as always I managed to find some sample code online which really helped developing this App. I’ve used it in my project as an Excel Helper class, modifying it to suit my needs. As usual CodeProject and this link on CodeProject.com was a perfect template even though it was in C# (I simply converted it to VB.NET using this tool)
So now finally, to the completed project source code… First of all, here’s my ExcelHelper.vb source file which provides the Excel functionality
Imports Excel = Microsoft.Office.Interop.Excel
Imports Microsoft.Office.Interop
  Public Class ExcelHelper
    Class CreateExcelDoc
    Private app As Excel.Application = Nothing
    Private workbook As Excel.Workbook = Nothing
    Private worksheet As Excel.Worksheet = Nothing
    Private workSheet_range As Excel.Range = Nothing
    Public Sub New()
      createDoc()
    End Sub
    Public Sub createDoc()
      Try
        If Process.GetProcessesByName("Excel").Length > 0 Then
          app = CType(GetObject(, "Excel.Application"), Excel.Application)
          ' Else createObject
        Else
          app = New Excel.Application
        End If
        app.Visible = True
        workbook = app.Workbooks.Add(1)
        worksheet = DirectCast(workbook.Sheets(1), Excel.Worksheet)
      Catch e As Exception
        Console.Write("Error")
      Finally
      End Try
    End Sub
      Public Sub createHeaders(row As Integer, col As Integer, htext As String, cell1 As String, cell2 As String, mergeColumns As Integer, _
                             cellColor As System.Drawing.Color, isBold As Boolean, columnWidth As Integer, fontSize As Integer, fontColor As System.Drawing.Color)
      worksheet.Cells(row, col) = htext
      workSheet_range = worksheet.Range(cell1, cell2)
      workSheet_range.Merge(mergeColumns)
      workSheet_range.Interior.Color = cellColor
      workSheet_range.Font.Bold = isBold
      workSheet_range.Font.Size = fontSize
      workSheet_range.ColumnWidth = columnWidth
      workSheet_range.Font.Color = fontColor
    End Sub
      Public Sub addData(row As Integer, col As Integer, data As String, cell1 As String, cell2 As String, format As String)
      worksheet.Cells(row, col) = data
      workSheet_range = worksheet.Range(cell1, cell2)
      workSheet_range.Borders.Color = System.Drawing.Color.Black.ToArgb()
      workSheet_range.NumberFormat = format
    End Sub
  End Class
  End Class
  and then, the AutoCAD code, which contains the command “ExcelExample”, that actually extracts the data from the UIBindings
Imports System
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.Geometry
Imports Autodesk.AutoCAD.EditorInput
  ' This line is not mandatory, but improves loading performances
<Assembly: CommandClass(GetType(ExcelSample.MyCommands))>
  Namespace ExcelSample
    Public Class MyCommands
      ' command to show how to fill an excel work book with data from the currently active DWG inside of AutoCAD
    <CommandMethod("FentonWebbDevTechAutodesk", "ExcelExample", "ExcelExample", CommandFlags.Modal)> _
    Public Sub MyCommand()
        Dim ed As Editor = Application.DocumentManager.MdiActiveDocument.Editor
        ' create or get existing Excel app
      Dim excelHelper As ExcelHelper.CreateExcelDoc = New ExcelHelper.CreateExcelDoc()
      ' create dwg file details header
      excelHelper.createHeaders(1, 1, "Overview Data for AutoCAD Drawing: " _
                                + Application.DocumentManager.MdiActiveDocument.Name, "A1", "Z1", _
                                2, System.Drawing.Color.LightBlue, True, 80, 16, _
                                System.Drawing.Color.Black)
        ' create the hatches header
      excelHelper.createHeaders(2, 1, "Hatch Patterns", "A2", "A2", _
                                2, System.Drawing.Color.LightGray, True, 40, 12, _
                                System.Drawing.Color.Black)
      ' export all of the Hatch patterns using Kean's way, cool
      Dim y As Integer = 3
      Dim str As String
      For Each str In Autodesk.AutoCAD.Windows.Data.HatchPatterns.Instance.AllPatterns
        excelHelper.addData(y, 1, str, "A" + y.ToString(), "A" + y.ToString(), "")
        y = y + 1
      Next
        AddDataBoundEntry(excelHelper, 2, 2, "B", "Layers", Application.UIBindings.Collections.Layers, "Name")
      AddDataBoundEntry(excelHelper, 2, 3, "C", "Layer States", Application.UIBindings.Collections.LayerStates, "Name")
      AddDataBoundEntry(excelHelper, 2, 4, "D", "Layer Filters", Application.UIBindings.Collections.LayerFilters, "Name")
      AddDataBoundEntry(excelHelper, 2, 5, "E", "Line Types", Application.UIBindings.Collections.Linetypes, "Name")
      AddDataBoundEntry(excelHelper, 2, 6, "F", "MLeader Styles", Application.UIBindings.Collections.MleaderStyles, "Name")
      AddDataBoundEntry(excelHelper, 2, 7, "G", "Dimension Styles", Application.UIBindings.Collections.DimensionStyles, "Name")
      AddDataBoundEntry(excelHelper, 2, 8, "H", "Plot Styles", Application.UIBindings.Collections.PlotStyles, "Name")
      AddDataBoundEntry(excelHelper, 2, 9, "I", "Visual Styles", Application.UIBindings.Collections.VisualStyles, "Name")
      AddDataBoundEntry(excelHelper, 2, 10, "J", "Ucs Planes", Application.UIBindings.Collections.UcsPlanes, "Name")
      AddDataBoundEntry(excelHelper, 2, 11, "K", "Text Styles", Application.UIBindings.Collections.TextStyles, "Name")
      AddDataBoundEntry(excelHelper, 2, 12, "L", "Table Styles", Application.UIBindings.Collections.TableStyles, "Name")
      AddDataBoundEntry(excelHelper, 2, 13, "M", "Render Presets", Application.UIBindings.Collections.RenderPresets, "Name")
      AddDataBoundEntry(excelHelper, 2, 14, "N", "Named Views", Application.UIBindings.Collections.NamedViews, "Name")
      End Sub
      Private Sub AddDataBoundEntry( _
                  excelHelper As ExcelHelper.CreateExcelDoc, _
                  row As Integer, col As Integer, colStr As String, headerName As String, _
                  dataItemCollection As Autodesk.AutoCAD.Windows.Data.DataItemCollection, _
                  propertyName As String)
        ' create the Layers dump
      excelHelper.createHeaders(row, col, headerName, _
                                colStr + row.ToString(), colStr + row.ToString(), _
                                2, System.Drawing.Color.LightGray, True, 40, 12, _
                                System.Drawing.Color.Black)
      ' export all of the Hatch patterns
      Dim y As Integer = 3
      ' loop all of the entries
      For Each desc As System.ComponentModel.ICustomTypeDescriptor In dataItemCollection
        ' extract the layer table record property we want
        Dim propertyValue = desc.GetProperties()(propertyName).GetValue(desc)
        ' add it to the sheet
        excelHelper.addData(y, col, propertyValue, colStr + y.ToString(), colStr + y.ToString(), "")
        y = y + 1
      Next
      End Sub
      End Class
  End Namespace
  and finally, the output seen in Excel
  Until the next time
Fenton

## 评论

**内容**: Ben said...
Hi Fenton
I could not find your materials: "Using Windows Presentation Foundation in AutoCAD" and the part II portion as well inside the autocad university.
any ideas where they are?
rgds
BK
Reply
11/08/2015 at 08:03 PM

---
