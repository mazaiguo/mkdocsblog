---
title: "Parallel Aggregation using AccoreConsole"
date: 2015-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "In a comment to this blog post, a developer had enquired about the possibility of using AccoreConsole to gather information from multiple drawings ..."
author: Autodesk
---
# Parallel Aggregation using AccoreConsole

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/parallel-aggregation-using-accoreconsole.html

## 文章内容

By Balaji Ramamoorthy
In a comment to this blog post, a developer had enquired about the possibility of using AccoreConsole to gather information from multiple drawings without having to launch AccoreConsole for each drawing. AccoreConsole can only work on the drawing passed to it using the "/i" startup switch. This prevents it from working on other drawings. But to considerably speed up the processing, parallel aggregation can be used to launch multiple instances of AccoreConsole. This leverages the multi-core capabilities of the system to perform and easily aggregate the results.
Here are two versions of a code that gathers the entity type of all the entities from drawings. In my Oct-core system, the serial version completed its processing for 5 drawings in about 8 seconds, while the parallel version completed it in 1.9 seconds. The results may vary at your end, but this should provide an idea of the performance enhancement that can be expected.
 // Serial version 
 Dictionary<String, String> entityBreakUp 
             = new  Dictionary<String, String>();
   DirectoryInfo di = 
     new  DirectoryInfo(@"D:\Temp\TestDrawings" );
 FileInfo[] fiCollection = di.GetFiles("*.dwg" );
   DateTime startTime = DateTime.Now;
   foreach  (FileInfo fi in  fiCollection)
 {
     String consoleOutput = String.Empty;
     String entityNames = String.Empty;
     using  (Process coreprocess = new  Process())
     {
         coreprocess.StartInfo.UseShellExecute 
                                     = false ;
         coreprocess.StartInfo.CreateNoWindow 
                                     = true ;
         coreprocess.StartInfo.RedirectStandardOutput 
                                     = true ;
         coreprocess.StartInfo.FileName =
         @"C:\Program Files\Autodesk\ 
         AutoCAD 2015\accoreconsole.exe" ;
           coreprocess.StartInfo.Arguments =
             string .Format("/i \"{0}\" /s \"{1}\" /l en-US" ,
             fi.FullName,
             @"C:\Temp\RunCustomNETCmd.scr" );
           coreprocess.Start();
           // Max wait for 5 seconds 
         coreprocess.WaitForExit(5000); 
           StreamReader outputStream 
                 = coreprocess.StandardOutput;
         consoleOutput = outputStream.ReadToEnd();
         String cleaned = 
             consoleOutput.Replace("\0" , string .Empty);
           int  first = cleaned.IndexOf("BreakupBegin" ) 
                             + "BreakupBegin" .Length;
           int  last = cleaned.IndexOf("BreakupEnd" );
         if  (first != -1 && last != -1)
             entityNames = 
                 cleaned.Substring(first, last - first);
           outputStream.Close();
     }
       entityBreakUp.Add(fi.FullName, entityNames);
 }
   Console.WriteLine(string .Format(
         "*** Serial processing : {0:0.0} seconds ***" , 
         DateTime.Now.Subtract(startTime).TotalSeconds));
   foreach  (KeyValuePair<String, String> kvp in  entityBreakUp)
 {
     Console.WriteLine(String.Format("{0} - {1}" , 
                 kvp.Key.ToString(), kvp.Value.ToString()));
 }
   // Parallel version 
 Dictionary<String, String> entityBreakUp 
         = new  Dictionary<String, String>();
   DirectoryInfo di = 
     new  DirectoryInfo(@"D:\Temp\TestDrawings" );
 FileInfo[] fiCollection = di.GetFiles("*.dwg" );
   entityBreakUp.Clear();
 startTime = DateTime.Now;
 entityBreakUp = GetEntityBreakUp(fiCollection);
   Console.WriteLine(string .Format(
 "*** Parallel processing : {0:0.0} seconds ***" , 
 DateTime.Now.Subtract(startTime).TotalSeconds));
   foreach  (KeyValuePair<String, String> kvp 
                         in  entityBreakUp)
 {
     Console.WriteLine(String.Format("{0} - {1}" , 
         kvp.Key.ToString(), kvp.Value.ToString()));
 }
   // Launches multiple instance of AccoreConsole 
 static  Dictionary<String, String> 
             GetEntityBreakUp(FileInfo[] fiCollection)
 {
     object  lockObject = new  object ();
     Dictionary<String, String> entBreakup 
         = new  Dictionary<String, String>();
         Parallel.ForEach(
         // The values to be aggregated  
         fiCollection,
               // The local initial partial result 
         () => new  Dictionary<String, String>(),
           // The loop body 
         (x, loopState, partialResult) =>
         {
             // Lauch AccoreConsole and find the  
             // entity breakup  
             FileInfo fi = x as  FileInfo;
               String consoleOutput = String.Empty;
             String entityBreakup = String.Empty;
             using (Process coreprocess = new  Process())
             {
                 coreprocess.StartInfo.UseShellExecute 
                                             = false ;
                 coreprocess.StartInfo.CreateNoWindow 
                                             = true ;
                 coreprocess.StartInfo.RedirectStandardOutput 
                                             = true ;
                 coreprocess.StartInfo.FileName = 
                 @"C:\Program Files\ 
                 Autodesk\AutoCAD 2015\accoreconsole.exe" ;
                   coreprocess.StartInfo.Arguments = 
                 string .Format("/i \"{0}\" /s \"{1}\" /l en-US" , 
                 fi.FullName, 
                 @"C:\Temp\RunCustomNETCmd.scr" );
                   coreprocess.Start();
                   // Max wait for 5 seconds 
                 coreprocess.WaitForExit(5000); 
                   StreamReader outputStream 
                         = coreprocess.StandardOutput;
                 consoleOutput = outputStream.ReadToEnd();
                 String cleaned = 
                 consoleOutput.Replace("\0" , string .Empty);
                   int  first = cleaned.IndexOf("BreakupBegin" ) 
                                     + "BreakupBegin" .Length;
                 int  last = cleaned.IndexOf("BreakupEnd" );
                 if (first != -1 && last != -1)
                     entityBreakup = 
                        cleaned.Substring(first, last - first);
                   outputStream.Close();
             }
               Dictionary<String, String> partialDict 
                 = partialResult as  Dictionary<String, String>;
               partialDict.Add(x.FullName, entityBreakup);
             return  partialDict;
         },
           // The final step of each local context             
         (partialEntBreakup) =>
         {
             // Enforce serial access to single, shared result 
             lock  (lockObject)
             {
                 Dictionary<String, String> partialDict 
                 = partialEntBreakup as  Dictionary<String, String>;
                   foreach  (KeyValuePair<String, String> kvp 
                                             in  partialDict)
                 {
                     entBreakup.Add(kvp.Key, kvp.Value);
                 }
             }
         });
       return  entBreakup;
 }
  Here is the code from the custom .Net plugin for "EntBreakup" command which lists the entities in a drawing.
 [CommandMethod("MyCommands" , 
                 "EntBreakup" , 
                 CommandFlags.Modal)]
 public  void  EntBreakupMethod()
 {
     DocumentCollection docs = Autodesk.AutoCAD
         .ApplicationServices.Core.Application.DocumentManager;
     Document activeDoc = docs.MdiActiveDocument;
     Editor ed = activeDoc.Editor;
       // Obtain the selection set of all the entities  
     // in the drawing. 
     PromptSelectionResult psr1 = ed.SelectAll();
     if  (psr1.Status == PromptStatus.OK)
     {
         PrintSelectionSet("SelectAll" , psr1.Value);
     }
 }
   private  void  PrintSelectionSet(string  Title, SelectionSet ss)
 {
     DocumentCollection docs = Autodesk.AutoCAD
         .ApplicationServices.Core.Application.DocumentManager;
     Document activeDoc = docs.MdiActiveDocument;
     Editor ed = activeDoc.Editor;
       ed.WriteMessage(string .Format("{0}BreakupBegin" , 
                                 Environment.NewLine));
     foreach  (ObjectId oid in  ss.GetObjectIds())
     {
         ed.WriteMessage(string .Format("{0}{1}" , 
             Environment.NewLine, oid.ObjectClass.Name));
     }
     ed.WriteMessage(string .Format("{0}BreakupEnd" , 
                                     Environment.NewLine));
 }
  The sample project can be donwnloaded here :
Download SampleProject

## 评论

**内容**: Wouter said...
Hi Balaji,
Thank you for this example. What would the contents of RunCustomNETCmd.scr be?
Reply
02/24/2015 at 01:08 AM

---
**内容**: Balaji said...
Hi Wouter,
That script would netload the custom .net plugin and invoke the custom command.
;Load the .Net module
(command "_.Netload" "C:\\Temp\\EntityBreakup.dll")
; Run the command
EntBreakup
Regards,
Balaji
Reply
02/24/2015 at 01:11 AM

---
**内容**: Jeff said...
hi,
really useful post. Stupid question, is there a problem here : coreprocess.StartInfo.Arguments = string .Format("/i \\"{0}\\" /s \\"{1}\\" /l en-US" ,fi.FullName,
@"C:\\Temp\\RunCustomNETCmd.scr" );
my visual trudio express 2013 doesn't like this line.
Reply
02/24/2015 at 01:44 AM

---
**内容**: Balaji said...
Hi Jeff,
Thanks for pointing that out. It seems the tool that converts the code to html format for posting it in typepad has messed it up.
It should be :
coreprocess.StartInfo.Arguments = string .Format("/i \"{0}\" /s \"{1}\" /l en-US" ,fi.FullName, @"C:\Temp\RunCustomNETCmd.scr" );
I will fix the post
Thanks
Balaji
Reply
02/24/2015 at 01:54 AM

---
**内容**: Jeff said...
hi,
It was pleasure!
Thanks for your script. I use it to purge the RegsApp in my files. It increases the speed, you can't imagine!
Reply
02/24/2015 at 05:42 AM

---
**内容**: Balaji said...
Thanks for the update.
Glad to know that this helped.
Reply
02/24/2015 at 10:47 PM

---
**内容**: Matthias said...
Hi Balaji,
Works like a charm. But could it be, if I use the parallel code to run the publish command, that sometimes the pdf files are corrupt or the content of one PDF file is from the wrong drawing?
Does AutoCAD use the same temporary files for the different processes while publishing?
Reply
02/25/2015 at 04:47 AM

---
**内容**: Balaji said...
Hi Matthias,
I am not aware of any known issue with AccoreConsole that would cause this. I tried publishing PDF out of 500 drawings in parallel and it worked ok. I did not notice any mix up. If you are facing such an issue, can you please share the steps and non-confidential drawings for me to reproduce the behavior ?
Thanks
Balaji
Reply
02/26/2015 at 12:25 AM

---
**内容**: Matthias said...
Hi Balaji,
The problem doesn't occur all the time. Sometimes the documents are ok, but sometimes some of them are corrupt.
I've used the Subscription Center to offer you some sample files and a sample project (#10499576).
Regards
Matthias
Reply
02/26/2015 at 08:34 AM

---
**内容**: Balaji said in reply to Matthias...
Hi Matthias,
Thanks for sending me the sample project.
I can reproduce the problem intermittently. It appears that the publish does rely on some shared resource.
Unfortunately, I do not know if this can be resolved. AccoreConsole was developed as an internal tool and not for public use. So, unfortunately i cannot log this behavior for our engineering team to analyze it.
When plotting the drawings as PDF using PLOT command from a script does not seem to have such issues. I have shared a sample script file, but you may need to modify it to suit your needs. Hope this helps.
https://www.dropbox.com/s/6pr9npppk74bdte/PDFGen_EN.zip?dl=0
Regards,
Balaji
Reply
02/27/2015 at 05:26 AM

---
**内容**: Jordan said in reply to Balaji...
Hi Balaji,
I have some troubles using AcCoreConsole with printing and threading.
I use BackGroundWorkers instead of the Parallel functionality.
I am using a script file to plot to PNG and I get "missing required property" errors when doing this plot. I am also using a pc3 file in this script. Is this maybe the issue?
Can you please post your sample project again? So I can investigate your sample?
Reply
06/18/2015 at 02:52 AM

---
**内容**: Balaji said in reply to Jordan...
Hi Jordan,
I have attached the sample project to the post.
Regards,
Balaji
Reply
06/19/2015 at 01:58 AM

---
**内容**: Balaji said...
Hello,
I am adding below an update from Thomas Brammer, who kindly shared the results of his tests for publishing drawings in parallel using AccoreConsole. I hope this will help many others using it for a similar workflow.
<<<
I added a thread-dependant user name to the /isolate switch as you suggested. But I still saw some AccoreConsole failing. Then I also added a thread-dependant working directory path to the /isolate switch:
/isolate user c:\temp\acc\
Now all my AccoreConsole calls work like a charm!
AccoreConsole even creates the directories if they don’t exist!
>>>
Regards,
Balaji
Reply
12/08/2015 at 09:12 PM

---
**内容**: Ben said...
Hello Bajali
if one uses ScriptPro 2.0 - does this not employ parallel processing of drawings? I mean this post and ScriptPro do virtually the same things in terms of parallel processing correct?
with thanks and kind regards
Ben
Reply
02/02/2016 at 08:21 PM

---
**内容**: Devin said...
Hello,
I've been using this method and it works great as a plotting tool. Is there anyway to modify the .net code to search multiple directories for dwg files?
Reply
02/22/2017 at 06:22 PM

---
**内容**: Nik said...
Hey everyone,
I recently discovered a VERY fast method of processing dwg files using accorconsole (or AutoCAD if that is what you prefer). For example, running a search and replace operation of dbtext and mtext on a batch of dwg files runs at around 15 drawings/second on a single process. Setting up 5 or 6 in parallel will process close to 5000 drawings/minute! I thought I would share this with the community as this discovery has been a game-changer for my company when it comes to processing large batches of dwg files.
For this you have to use the .NET API. I did all the code for processing in C#, and the only 2 lines in the lisp script file is to NETLOAD my dll and call the command that does the processing.
Turns out, you can work on multiple dwg files in the same instance of accoreconsole. The idea here is to just load the dwg database without actually opening the drawing (takes ~70ms), manipulate the database, then save it. For the i/ switch, you can use any dummy drawing file as it will have no effect on your batch. Then in C# in your command method, you would do something like this:
foreach(string drawingFilePath in dwgFiles)
{
database = new Database(false, true);
database.ReadDwgFile(drawingFilePath, FileShare.ReadWrite, true, String.Empty);
using(Transaction transaction = database.TransactionManager.StartTransaction())
{
//DO STUFF HERE
transaction.Commit();
database.SaveAs(drawingFilePath, DwgVersion.Current);
}
database.Dispose();
}
Let me know if you have any questions or need more detail,
Reply
06/28/2017 at 07:30 PM

---
**内容**: Chuck Dodson said...
@Nik,
I'm doing something very similar where my .net code prompts for a filename and the .script file calls the command and supplies the filenames. I know the original post is 8 years old, but I'm also not supplying an initial drawing to open using the /i switch. The issue I'm running into is the profile. Once the profile is set in the .bat, it remains the next time I open AutoCAD. Would you happen to know a way of stopping this? Or to get the profile set back to none? The CProfile variable is read-only, so....
Reply
06/22/2023 at 02:33 PM

---
