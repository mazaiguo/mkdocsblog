---
title: "Use EXPORTPDF / EXPORTDWF / EXPORTDWFX programmatically"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - PDF
description: "I'm wondering if I could use EXPORTPDF directly to create a PDF file."
author: Autodesk
---
# Use EXPORTPDF / EXPORTDWF / EXPORTDWFX programmatically

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/use-exportpdf-exportdwf-exportdwfx-programmatically.html

## 文章内容

By Adam Nagy
I'm wondering if I could use EXPORTPDF directly to create a PDF file.
Solution
EXPORTPDF does not have a command line version, but just like EXPORTDWF and EXPORTDWFX as well, this command also builds on the EXPORT command functionality, which does have a command line version.
Here is a sample showing how to use it:
(command "_-EXPORT" "_PDF" "_D" "_NO" "C:\\my.pdf")
Also, the EXPORT command is using the Publish API in the background so you might be interested in using that - have a look at blog post "How to use Autodesk.AutoCAD.Publishing.Publisher.PublishExecute?"

## 评论

**内容**: Adil said...

Hi, thanks a lot for this interesting post.
Can i use this command in DWG TRURVIEW 2013(or other version) ?
When i make this command i have : Unknown Command :(
Any HELP please.
Thank You.
Reply
05/02/2014 at 03:22 AM

---
**内容**: Bob said...
Hello.
I am trying to use the following VBA in order to export all the layouts in a pdf file.
ThisDrawing.SendCommand ("-EXPORT" & vbCr & "PDF" & vbCr & "ALL" & vbCr & varFile & vbCr)
Unfortunately this does not work. After a while a plot error comes up, but it does not give any message.
When I execute the commands one by one in the command line it works.
I tried as well to indicate the file name instead of the variable (which is a string) but no luck eather.
Any ideas?

Bob
Reply
01/22/2015 at 01:49 AM

---
**内容**: Balaji said...
Hi Bob,
Sorry, I could not reproduce the error. It worked ok with the following VBA code :
Public Sub Test()
ThisDrawing.SendCommand ("filedia 0 ")
Dim varFile As String
varFile = "D:\Temp\VBA.pdf"
ThisDrawing.SendCommand ("-EXPORT" & vbCr & "PDF" & vbCr & "ALL" & vbCr & varFile & vbCr)
End Sub
Can you please try running Lisp code from the command prompt ? The publish result popup in AutoCAD can help provide more information on the error.
Please try this, if you are using AutoCAD 2015 :
(command-s "_-EXPORT" "_PDF" "_ALL" "D:\\Temp\\my.pdf")
or this one for the earlier releases :
(command "_-EXPORT" "_PDF" "_ALL" "D:\\Temp\\my.pdf")
Regards,
Balaji
Reply
01/23/2015 at 04:29 PM

---
**内容**: Cesar Hernandez said in reply to Balaji...
Hello Balaji,
I ran the code and it works great! Thank you! I am having a problem with trying to get the file name from the file to insert into the newly created PDF as a file name. I used the "getfilename" but it seems not to work or I am not calling correctly. Any help you could provide would be greatly appreciated. Below is the code:
Public Sub Test()
ThisDrawing.SendCommand ("filedia 0 ")
Dim varFile As String
varFile = "P:\Instrument Group\PDFs\Test\" + getfilename + ".pdf"
ThisDrawing.SendCommand ("_-EXPORT" & vbCr & "PDF" & vbCr & "" & vbCr & "" & vbCr & varFile & vbCr)
End Sub
Thank you!
Reply
02/21/2017 at 06:39 AM

---
**内容**: Dave said in reply to Cesar Hernandez...
I haven't used getfilename but you can use the Active document properties to get what you need.

Sub ActiveFileName()
MsgBox Application.ActiveDocument.Path
MsgBox Application.ActiveDocument.Name
MsgBox Application.ActiveDocument.FullName
End Sub
Reply
03/15/2017 at 11:18 AM

---
**内容**: Cesar Hernandez said in reply to Dave...
Dave - That worked great! Thank you so much!
Reply
03/23/2017 at 01:40 PM

---
**内容**: Nirantar Vidyarthee said...
I ran this code in AutoCAD 2014 but it does not generate the pdf file.
AutoCAD says errors and warning found but it is blank.
Public Sub Test()
ThisDrawing.SendCommand ("filedia 0 ")
Dim varFile As String
varFile = "D:\PDftry\Angletry.pdf"
ThisDrawing.SendCommand ("_-EXPORT" & vbCr & "PDF" & vbCr & "Extents" & vbCr & "No" & vbCr & varFile & vbCr)
End Sub
When I run the same command on command line it works.
Reply
03/19/2018 at 01:06 PM

---
