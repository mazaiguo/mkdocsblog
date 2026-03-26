---
title: "How to use the Autodesk.AutoCAD.Publishing.Publisher.PublishDsd API in .Net?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C#
  - DWG
description: "Here is a common request from ADN developers:"
author: Autodesk
---
# How to use the Autodesk.AutoCAD.Publishing.Publisher.PublishDsd API in .Net?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-use-the-autodeskautocadpublishingpublisherpublishdsd-api-in-net.html

## 文章内容

By Philippe Leefsma
Here is a common request from ADN developers:
Is there any sample showing how to create programmatically a configuration dsd file and use the Publisher.PublishDsd API ?
Solution
Here is a C# example that shows you how to publish to a dwf sheet set two layouts from differents drawings. It also create programmatically a dsd file and write it on the disk. You could also use an existing dsd file that was created previously and provide it directly to the PublishDsd method.
For the sample to work, you need to have two drawings, named "Drawing1.dwg" and "Drawing2.dwg", that are stored at the location: "C:\Temp\". Each drawing needs to have a layout named "Layout1".
[CommandMethod("PublisherDSD")]
static public void PublisherDSD()
{
    try
    {
        DsdEntryCollection collection = new DsdEntryCollection();
        DsdEntry entry;
          entry = new DsdEntry();
        entry.Layout = "Layout1";
        entry.DwgName = "c:\\Temp\\Drawing1.dwg";
        entry.Nps = "Setup1";
        entry.Title = "Sheet1";
        collection.Add(entry);
          entry = new DsdEntry();
        entry.Layout = "Layout1";
        entry.DwgName = "c:\\Temp\\Drawing2.dwg";
        entry.Nps = "Setup1";
        entry.Title = "Sheet2";
        collection.Add(entry);
          DsdData dsd = new DsdData();
                dsd.SetDsdEntryCollection(collection);
                dsd.ProjectPath = "c:\\Temp\\";
        dsd.LogFilePath = "c:\\Temp\\logdwf.log";
        dsd.SheetType = SheetType.MultiDwf;
        dsd.NoOfCopies = 1;
        dsd.DestinationName = "c:\\Temp\\PublisherTest.dwf";
        dsd.SheetSetName = "PublisherSet";
        dsd.WriteDsd("c:\\Temp\\publisher.dsd");
            int nbSheets = collection.Count;
          using (PlotProgressDialog progressDlg =
            new PlotProgressDialog(false, nbSheets, true))
        {
            progressDlg.set_PlotMsgString(
                PlotMessageIndex.DialogTitle,
                "Plot API Progress");
            progressDlg.set_PlotMsgString(
                PlotMessageIndex.CancelJobButtonMessage,
                "Cancel Job");
            progressDlg.set_PlotMsgString(
                PlotMessageIndex.CancelSheetButtonMessage,
                "Cancel Sheet");
            progressDlg.set_PlotMsgString(
                PlotMessageIndex.SheetSetProgressCaption,
                "Job Progress");
            progressDlg.set_PlotMsgString(
                PlotMessageIndex.SheetProgressCaption,
                "Sheet Progress");
              progressDlg.UpperPlotProgressRange = 100;
            progressDlg.LowerPlotProgressRange = 0;
              progressDlg.UpperSheetProgressRange = 100;
            progressDlg.LowerSheetProgressRange = 0;
              progressDlg.IsVisible = true;
              Autodesk.AutoCAD.Publishing.Publisher publisher =
                Application.Publisher;
              Autodesk.AutoCAD.PlottingServices.PlotConfigManager.
                SetCurrentConfig("DWF6 ePlot.pc3");
              publisher.PublishDsd(
                "c:\\Temp\\publisher.dsd", progressDlg);
        }
    }
    catch (Autodesk.AutoCAD.Runtime.Exception ex)
    {
        System.Windows.Forms.MessageBox.Show(ex.Message);
    }
}

## 评论

**内容**: Ken Washburn said...
How do you make this produce a 3D DWF file?
Reply
09/07/2012 at 10:57 AM

---
**内容**: Gilles Chanteau said...
Ken,
You can have a look here:
http://www.theswamp.org/index.php?topic=31897.msg474069#msg474069
Reply
09/07/2012 at 11:38 PM

---
**内容**: Andrey said...
Hi Philippe.
I apologise for my bad English.
Sorry, but it ain't working in AutoCAD 2013 x64 for me.
I created c:\Temp directory, created two DWG files. In each DWG I created "Setup1" in Page Setup Manager dialog. Each drawing has Layout1 with some primitives. I have "DWF6 ePlot.pc3".
In the program runtime I get an error of AutoCAD and the application is closed.
If I open c:\Temp, then I see the new files: logdwf.txt and publisher.dsd, but execution of the program is interrupted.
Regards
Reply
09/08/2012 at 07:36 AM

---
**内容**: Andrey said...
P.S. My operation system: Windows 8 x64.
Reply
09/08/2012 at 07:37 AM

---
**内容**: Andrey said...
---------------------------
AutoCAD Error Aborting
---------------------------
FATAL ERROR: Unhandled Access Violation Reading 0xffffffff Exception at a21d8d92h
---------------------------
ОК
---------------------------
Reply
09/08/2012 at 08:02 AM

---
**内容**: Philippe said...
Hi Andrey, sorry about that but AutoCAD 2013 is not a supported product on a Windows 8 environment. If you are able to reproduce the issue under Windows 7, XP or Vista, let me know.
Reply
09/10/2012 at 03:44 AM

---
**内容**: Andrey said in reply to Philippe...
Ok. I does it again on other computer:
=============
Windows XP x86 SP3 Rus
AutoCAD 2009 x86 SP3 Enu
.Net Framework 2.0, 3.0, 3.5 SP1.
MS Visual Studio 2010 SP1 x86
=============
But it ain't work again:
---------------------------
AutoCAD Error Aborting
---------------------------
FATAL ERROR: Unhandled Access Violation Reading 0xbbd7a58b Exception at 6329c8d7h
---------------------------
ОК
---------------------------
Reply
09/10/2012 at 05:36 AM

---
**内容**: Andrey said in reply to Philippe...
I tried to do it and on third computer:
=============
Windows XP x86 SP3 Rus
AutoCAD 2013 x86 Enu
.Net Framework 2.0, 3.0, 3.5 SP1.
MS Visual Studio 2010 SP1 x86
=============
But it ain't working again:
acad.exe process died without messages.
Reply
09/10/2012 at 05:48 AM

---
**内容**: Andrey said in reply to Philippe...
Have You tried to run it code on your computer?
Reply
09/10/2012 at 05:56 AM

---
**内容**: Philippe said...
So far I do not reproduce the issue with that code. Did you make sure your testing files have been physically saved on the disk, I remember issues link to that...
Reply
09/11/2012 at 04:21 AM

---
**内容**: Andrey said in reply to Philippe...
Yes, I sure.
Philippe, look please at this, please: https://skydrive.live.com/redir?resid=51B3145B64E05FEF!538&authkey=!AH9SMEznd1kbZfw
It an archive contains projects with your code for autocad 2009 and autocad 2013, and directory "temp" with DWG files. Try it run, please.
Regards
Reply
09/11/2012 at 06:59 AM

---
**内容**: elpanov@gmail.com said...
Hi Andery!
It ain't working for me too (Windows 7 x86 Acad 2013 x86).
Reply
09/11/2012 at 07:28 AM

---
**内容**: elpanov@gmail.com said...
see screenshot of error:
https://skydrive.live.com/redir?resid=100A6A4D2F10BA72!124&authkey=!AKWNDMptlh_yNpg
Reply
09/11/2012 at 07:35 AM

---
**内容**: Philippe said...
Alright, testing under 2013 and I could reproduce the behavior... The following code seems to work fine and produces nearly the same result, can you check if it addresses your needs?
[CommandMethod("PublishExecute")]
static public void PublishExecute()
{
try
{
string dsdFilePath = "c:\\Temp\\publisher.dsd";
string dsdLogPath = "c:\\Temp\\logdwf.log";
string dwfDestPath = "c:\\Temp\\PublisherTest.dwf";
DsdEntryCollection collection = new DsdEntryCollection();
DsdEntry entry;
entry = new DsdEntry();
entry.Layout = "Layout1";
entry.DwgName = "c:\\Temp\\Drawing1.dwg";
entry.NpsSourceDwg = entry.DwgName;
entry.Title = "Sheet1";
collection.Add(entry);
entry = new DsdEntry();
entry.Layout = "Layout1";
entry.DwgName = "c:\\Temp\\Drawing2.dwg";
entry.NpsSourceDwg = entry.DwgName;
entry.Title = "Sheet2";
collection.Add(entry);
DsdData dsd = new DsdData();
dsd.SetDsdEntryCollection(collection);
dsd.IsSheetSet = true;
dsd.LogFilePath = dsdLogPath;
dsd.SheetType = SheetType.MultiDwf;
dsd.NoOfCopies = 1;
dsd.DestinationName = dwfDestPath;
dsd.SheetSetName = "PublisherSet";
dsd.WriteDsd(dsdFilePath);
//Workaround to avoid promp for dwf file name
//set PromptForDwfName=FALSE in dsdData using StreamReader/StreamWriter
System.IO.StreamReader sr = new System.IO.StreamReader(dsdFilePath);
string str = sr.ReadToEnd();
sr.Close();
str = str.Replace("PromptForDwfName=TRUE", "PromptForDwfName=FALSE");
System.IO.StreamWriter sw = new System.IO.StreamWriter(dsdFilePath);
sw.Write(str);
sw.Close();
dsd.ReadDsd(dsdFilePath);
Autodesk.AutoCAD.PlottingServices.PlotConfigManager.SetCurrentConfig(
"DWF6 ePlot.pc3");
Application.Publisher.AboutToBeginPublishing +=
new Autodesk.AutoCAD.Publishing.AboutToBeginPublishingEventHandler(
Publisher_AboutToBeginPublishing);
Application.Publisher.PublishExecute(
dsd,
Autodesk.AutoCAD.PlottingServices.PlotConfigManager.CurrentConfig);
System.IO.File.Delete(dsdFilePath);
}
catch (Autodesk.AutoCAD.Runtime.Exception ex)
{
Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(ex.Message);
}
}
Reply
09/11/2012 at 09:03 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said in reply to Philippe...
Hi Philippe.
Yes, your 2-nd a code variant is working fine (at AutoCAD 2013 x64).
Thank you.
Reply
09/11/2012 at 10:05 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said in reply to Philippe...
Hi again, Philippe.
Why in your 2-nd code variant you wrote such a code rows:

System.IO.StreamWriter sw = new System.IO.StreamWriter(dsdFilePath);
sw.Write(str);
sw.Close();

Why you didn't use it:

dsd.PromptForDwfName = false;

???
It is much simpler and more clear.
Regards
Reply
09/11/2012 at 10:35 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
But...
Why not working your 1-st a code variant, with PlotProgressDialog? How can I write a code with PlotProgressDialog, which will working fine?
Regards
Reply
09/11/2012 at 10:22 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
I incorrectly quoted your code.
Instead of this code:
//Workaround to avoid promp for dwf file name
//set PromptForDwfName=FALSE in dsdData using StreamReader/StreamWriter
System.IO.StreamReader sr = new System.IO.StreamReader(dsdFilePath);
string str = sr.ReadToEnd();
sr.Close();
str = str.Replace("PromptForDwfName=TRUE", "PromptForDwfName=FALSE");
System.IO.StreamWriter sw = new System.IO.StreamWriter(dsdFilePath);
sw.Write(str);
sw.Close();
you could write more simply:
dsd.PromptForDwfName = false;
Regards
Reply
09/11/2012 at 10:40 AM

---
**内容**: Philippe said...
Thanks for pointing this out. I wasn't aware of this new property, at the time I initially wrote the code it didn't exist.
I'm afraid at the moment I don't see a workaround to get the publish dialog, considering "PublishDsd" does not produce the expected result. I would need to log a change request against it under 2013 and it will hopefully get fixed in a future SP or release.
Reply
09/11/2012 at 11:19 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
>I'm afraid at the moment I don't see a workaround to get the publish dialog, considering "PublishDsd" does not produce the expected result.
What AutoCAD version you used earlier, when this a code worked successfully?
> I would need to log a change request against it under 2013 and it will hopefully get fixed in a future SP or release.
Do it, please.
Regards
Reply
09/11/2012 at 11:47 AM

---
**内容**: Dale Bartlett said...
I use these two lines in 2013 which work perfectly:
PlotConfigManager.SetCurrentConfig("DWG To PDF.pc3");
AcadApp.Publisher.PublishDsd(lstrFileNameDsd, progressDlg);
Your suggested two lines fail to publish with no intelligible error:
PlotConfig pcfg = PlotConfigManager.SetCurrentConfig("DWG To PDF.pc3");
AcadApp.Publisher.PublishExecute(dsd, pcfg);
I must say I am not clear on the difference between PublishDsd and PublishExecute. Regards
Reply
03/27/2013 at 04:48 AM

---
**内容**: Matthias Mueller said...
Thanks for the script. One thing: is there a way to avoid the resulting PDF files to be opened afterwards?
Reply
09/09/2016 at 05:46 AM

---
**内容**: SixCode said...
I'm a developer working on a Windows forms application for a client. My client's users are using AutoCAD 2016 to create DWG files. They have an existing Windows application that creates batch plot lists as ".bp3" files, but they don't have the source code for the app. The new app I'm writing will replace their existing app, and needs to create batch plot list files outside of AutoCAD. I have the dlls from the ObjectARX SDK included in my Windows project and I've got some C# code that compiles, but fails at runtime (System.InvalidProgramException). I'm trying to use DsdEntryCollection and DsdEntry objects.
The app I'm working on will be installed on PCs that also have AutoCAD installed. Am I approaching this from the wrong angle? Is there an easier way to create batch plot list files that can be opened and plotted from in AutoCAD? My experience with AutoCAD is about 20 years old - so any input here would be greatly appreciated.
Using Visual Studio 2015.
Reply
10/13/2016 at 06:13 PM

---
