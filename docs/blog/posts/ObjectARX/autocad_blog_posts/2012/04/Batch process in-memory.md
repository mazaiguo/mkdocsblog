---
title: "Batch process in-memory"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "When we try batch process files in memory, we must take special attention to which transaction is in use, but the real trick is how to save the fil..."
author: Autodesk
---
# Batch process in-memory

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/batch-process-in-memory-1.html

## 文章内容

By Augusto Goncalves
When we try batch process files in memory, we must take special attention to which transaction is in use, but the real trick is how to save the file: AutoCAD will lock the file in use and therefore the SaveAs method is not available for the current file, so the trick could be save as a temporary file and then replace it. This approach can be used to batch process and is faster then open drawings “on scree” (visible). The trade-off is that some features may not be available, such as Layout Manager.
    1   Public Sub batchProcess()
    2     ' get all DWG files from a specific folder
    3     Dim directory As New System.IO.DirectoryInfo("C:\temp")
    4     Dim files As System.IO.FileInfo() = _
    5       directory.GetFiles("*.dwg")
    6 
    7     For Each file As System.IO.FileInfo In files
    8       ' generate a temp file location
    9       Dim tempFileName As String = _
   10         System.IO.Path.GetTempFileName()
   11 
   12       Using db As New Database(False, True)
   13         ' open the current file
   14         db.ReadDwgFile(file.FullName, _
   15                        System.IO.FileShare.ReadWrite, _
   16                        True, String.Empty)
   17 
   18         Using trans As Transaction = _
   19           db.TransactionManager.StartTransaction()
   20 
   21           ' ToDo:
   22           ' Do your processing here
   23 
   24 
   25           ' commit changes
   26           trans.Commit()
   27         End Using
   28 
   29         ' save as temp file
   30         db.SaveAs(tempFileName, DwgVersion.Current)
   31 
   32       End Using ' dispose the database
   33 
   34       ' now replace
   35       System.IO.File.Copy(tempFileName, file.FullName, True)
   36       ' and erase the temp file
   37       System.IO.File.Delete(tempFileName)
   38     Next
   39   End Sub

## 评论

**内容**: Will Hatch said...
Augusto,
I'm curious why there is no mention of the db.CloseInput method in this post. Is this to ease the pains of files which were open for write by another instance of AutoCAD?
Reply
06/07/2014 at 01:50 PM

---
**内容**: Augusto Goncalves said in reply to Will Hatch...
Will,
The CloseInput method is for internal use only, as mentioned on the documentation. If you have a scenario where the file is already opened, then this code may not work as changes are made to files...
Regards,
Augusto Goncalves
Reply
06/09/2014 at 05:23 AM

---
