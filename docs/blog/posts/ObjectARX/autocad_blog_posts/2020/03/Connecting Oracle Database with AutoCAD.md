---
title: "Connecting Oracle Database with AutoCAD"
date: 2020-03-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
description: "Q. Problems connecting AutoCAD to Oracle database, is Oracle database is supported. How to use to API to retrieve information from my Oracle databa..."
author: Autodesk
---
# Connecting Oracle Database with AutoCAD

发布日期: 2020-03-01

原始链接: https://adndevblog.typepad.com/autocad/2020/03/connecting-oracle-database-with-autocad.html

## 文章内容

By Madhukar Moogala

Q. Problems connecting AutoCAD to Oracle database, is Oracle database is supported. How to use to API to retrieve information from my Oracle database to AutoCAD.
A. From AutoCAD 2020 there is no 32 bit application, AutoCAD comes only in 64 bit application.
If you want to connect to Oracle, the Oracle client OLE Db drivers need to in 64 bit.
You need to install these based on your Oracle database installation, at my end I have Oracle 19c database, accordingly I need to install associated Oracle 19c OLE Db drivers.

Oracle Db
Oracle Ole Db

Now connecting to Oracle Db from AutoCAD VBAIDE
Step1: Setting necessary reference files.
AutoCAD 2021 Type Library
Ole Automation
Microsoft Activex Data Objects
Microsoft Activex Data Objects Recordset 
OraOLEDb 1.0 Type Library
Step2 : Preparing Connection String

"Provider=OraOLEDB.Oracle;User ID=<yourUserId>;Password=<yourPassword;Data Source=<yourDatabase>;"
For example:
"Provider=OraOLEDB.Oracle;User ID=SYSTEM;Password=Abcdef!23;Data Source=moogalm19;"
UserId : The User you have created for your Database
Password: The Password required to log in to Database
DataSource: The Database to which you would like to connect.
Step 3: Code to make a connection and open the Database.

 
Sub ReadOracleDB()
    Dim adoDbConn   As New ADODB.Connection
    Dim adoDbRs     As New ADODB.Recordset
    Dim selectCmd   As New ADODB.Command
    
    Dim strCon      As String
    Dim RC, CC      As Long
    
    ' connection string, same userId and password, which used to logon to with sqlplus'
    ' Data Source = name of your Database'
    
    strCon = "Provider=OraOLEDB.Oracle;User ID=SYSTEM;Password=Aut0desk!23;Data Source=moogalm19;"
    adoDbConn.Open (strCon)
    
    ' open the table with adOpenStatic, so we traverse to end of all recordses'
    adoDbRs.Open "SELECT * FROM EMPLOYEES", adoDbConn, adOpenStatic
    
    If IsNull(adoDbRs.RecordCount) Or (adoDbRs.RecordCount = 0) Then
        MsgBox "No Records Found!"
        Exit Sub
    End If
    
    RC = adoDbRs.RecordCount
    CC = adoDbRs.Fields.Count
    
    Dim MyModelSpace As AcadModelSpace
    Set MyModelSpace = ThisDrawing.ModelSpace
    Dim pt(2)       As Double
    Dim MyTable     As AcadTable
    
    ' RC+2 accounts for Title and Header rows'
    
    Set MyTable = MyModelSpace.AddTable(pt, RC + 2, CC, 10, 60)
    
    Dim i           As Integer
    Dim j           As Integer
    
    
    With MyTable
        .RegenerateTableSuppressed = True
        .RecomputeTableBlock False
        .TitleSuppressed = False
        .HeaderSuppressed = False
        .SetTextStyle AcRowType.acTitleRow, "Standard"
        .SetTextStyle AcRowType.acHeaderRow, "Standard"
        .SetTextStyle AcRowType.acDataRow, "Standard"
        
        Dim col         As New AcadAcCmColor
        col.SetRGB 255, 0, 255
        
        ' title'
        col.SetRGB 194, 212, 235
        .SetCellBackgroundColor 0, 0, col
        col.SetRGB 127, 0, 0
        .SetCellContentColor 0, 0, col
        .SetCellType 0, 0, acTextCell
        .SetText 0, 0, "MOOGALM19"
        
        ' headers'
        
        i = i + 1
        For j = 0 To .Columns - 1
            .SetCellType i, j, acTextCell
            .SetText i, j, CStr(adoDbRs.Fields(j).Name)
            
        Next
        
        ' dataRows'
        
        For i = 2 To .Rows - 1
            For j = 0 To .Columns - 1
                .SetCellType i, j, acTextCell
                .SetText i, j, adoDbRs.Fields(j).Value
                
            Next j
            adoDbRs.MoveNext
        Next i
        
        .RegenerateTableSuppressed = False
        .RecomputeTableBlock True
        .Update
        .GetBoundingBox minp, maxp
        ZoomWindow minp, maxp
        ZoomScaled 0.9, acZoomScaledRelative
        
    End With
    
    ' Close the connection and free the memory'
    
    adoDbRs.Close
    Set adoDbRs = Nothing
    Set selectCmd = Nothing
    adoDbConn.Close
    Set adoDbConn = Nothing
       
    ThisDrawing.SetVariable "LWDISPLAY", 1
    
End Sub
Demo

## 评论

**内容**: Chirag Oza said...
WOW WHAT A GREAT ARTICLE..I HAVE NOT SEEN SUCH GREAT CONTENT YET ON THE INTERNET
I REALLY APPRECIATE YOU FOR THIS GREAT INFORMATIVE IDEAS. YOU WILL DEFINITELY GO AHEAD IN YOUR LIFE SIR .. MY WARM WISHESH WITH YOU SIR.
Reply
07/17/2020 at 07:37 AM

---
**内容**: LEARN FREE AUTOCAD said...
THANK YOU SIR..
Reply
07/17/2020 at 07:38 AM

---
**内容**: Angrej Singh said...
Hi, do we have this coden referenced in c#. If not, can I please ask what references do we require to run this bit for AutoCAD 2018?
Thank you in advance.
Reply
11/15/2020 at 01:57 AM

---
**内容**: Graciliano Oliveira said...
Hi, Does Autocad Plant work with an Oracle database? is it possible to use the Oracle database with Plant?
Reply
09/27/2021 at 07:03 AM

---
**内容**: kürtaj said...
Thank you
Reply
10/10/2021 at 12:44 AM

---
**内容**: fethiye villa said...
nice article
Reply
10/10/2021 at 12:46 AM

---
**内容**: SALAH MOHAMMED MOQBEL said...
thank you very much
Reply
02/02/2024 at 10:57 PM

---
