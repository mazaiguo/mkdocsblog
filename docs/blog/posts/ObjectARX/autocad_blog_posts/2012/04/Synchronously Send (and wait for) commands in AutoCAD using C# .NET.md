---
title: "Synchronously Send (and wait for) commands in AutoCAD using C# .NET"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - C#
  - C++
description: "I’m really sorry to say, but anyone who tells me that acedCommand() and acedCmd() are not good C++ functions for driving AutoCAD, are crazy! These ..."
author: Autodesk
---
# Synchronously Send (and wait for) commands in AutoCAD using C# .NET

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/synchronously-send-and-wait-for-commands-in-autocad-using-c-net.html

## 文章内容

By Fenton Webb
I’m really sorry to say, but anyone who tells me that acedCommand() and acedCmd() are not good C++ functions for driving AutoCAD, are crazy! These functions have existed since the original R11 ADS development system in C and have always been used to synchronously send commands to the AutoCAD Command line. This means you can drive AutoCAD from your program code and expect things to be finished and done by the time the function returns.
These functions can literally save hours of work – instead of programmatically creating your own INSERT routine, just send the command and let AutoCAD do it – problem is, sometimes, you need to wait for the user to before carrying on, for example waiting for the user to place the block or enter the scales etc.
The code below shows how to PInvoke acedCmd() from .NET, and it shows the secret behind programmatically waiting for the user to finish the command using acedCmd(). Be warned though, we are changing/have changed the way these functions work, partly due to the AutoCAD for Mac port and now on Windows the Fiber removal project. Instead, you’ll need to use the acedCmdS() and acedCmdC() versions. Here’s some documentation on the subject
In the meantime, here’s the code showing how to call INSERT using acedCmd() synchronously
// call the insert command and wait until the user has finished, by Fenton Webb, DevTech
[DllImport("acad.exe", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedCmd")]
private static extern int acedCmd(System.IntPtr vlist);
[CommandMethod("Test7")]
public void Test7()
{
  ResultBuffer rb = new ResultBuffer();
  // RTSTR = 5005
  rb.Add(new TypedValue(5005, "_.INSERT"));
  // start the insert command
  acedCmd(rb.UnmanagedObject);
    bool quit = false;
  // loop round while the insert command is active
  while (!quit)
  {
    // see what commands are active
    string cmdNames = (string)Autodesk.AutoCAD.ApplicationServices.Application.GetSystemVariable("CMDNAMES");
    // if the INSERT command is active
    if (cmdNames.ToUpper().IndexOf("INSERT") >= 0)
    {
      // then send a PAUSE to the command line
      rb = new ResultBuffer();
      // RTSTR = 5005 - send a user pause to the command line
      rb.Add(new TypedValue(5005, "\\"));
      acedCmd(rb.UnmanagedObject);
    }
    else
      // otherwise quit
      quit = true;
  }
}

## 评论

**内容**: Account Deleted said...
Thanks Fenton!
But why 'CharSet = CharSet.Ansi' ? It is true for AutoCAD 2006 but 'CharSet = CharSet.Unicode' for AutoCAD 2007...
Also "acad.exe" is for AutoCAD 2006...2012 but "accore.dll" for AutoCAD 2013.
Reply
04/18/2012 at 11:00 PM

---
**内容**: Fenton Webb said...
You're right, that's a bug for sure, sorry about that.
That said, I don't think it causes a problem because the parameters are passed via an IntPtr linked list, not strings, so the Marshaler doesn't affect them.
Because we aren't specifically passing strings through the parameter list, probably best to omit that setting altogether...
e.g.
[DllImport("acad.exe", EntryPoint = "acedCmd")]
Reply
04/19/2012 at 09:39 AM

---
**内容**: Matus Brlit said...
how is the "Fiber removal project" going? this is the first time I found evidence that you are working on it, since Kean's post in 2011 :)
Reply
06/01/2012 at 05:52 AM

---
**内容**: Mona said...
Hello Fenton,
Kindly, I tried the code but with replacing the "INSERT" command with the following:
rb.Add(New TypedValue(5005, "_.AECTOACAD" & vbLf & "bind" & vbLf & "No" & vbLf & "" & vbLf & AecToAcadFileName & vbLf))
The problem is: cmdNames is always resturning only the "TEST7" command name & not AECtoACAD.
Please advise. Thanks
Reply
04/15/2013 at 12:00 AM

---
**内容**: Fenton Webb said...
Hi Mono
you don't add vbLf to a typedvalue string, you create new typed values... e.g
rb.Add(New TypedValue(5005, "_.AECTOACAD");
rb.Add(New TypedValue(5005, "_bind");
rb.Add(New TypedValue(5005, "_no");
rb.Add(New TypedValue(5005, AecToAcadFileName);
acedCmd(rb.UnmanagedObject);
Reply
04/15/2013 at 08:32 AM

---
**内容**: James Morris said in reply to Fenton Webb...
Fenton,
I have set up a pedit method like the above example.If I call "Test7" from the command line it works but if I call the method from code it goes through the motions but never sends the commands to the command line.I can use SendStringToExecute("test7 ",true,false,false) and that works but then its asynchronous.Any Ideas?
Reply
07/30/2014 at 05:10 AM

---
**内容**: James Morris said...
Fenton,
I have set up a pedit method like the above example.If I call "Test7" from the command line it works but if I call the method from code it goes through the motions but never sends the commands to the command line.I can use SendStringToExecute("test7 ",true,false,false) and that works but then its asynchronous.Any Ideas?
Reply
07/29/2014 at 10:48 AM

---
**内容**: Hal Perison said...
I realize that this post is old but it is still relevant today.
How is this to be implemented on newer software such as AutoCAD 2020 or newer.
On these packages I do no think that it works any longer as the entry points are not the same.
Reply
08/02/2023 at 06:55 AM

---
