---
title: "Change help file and topic associated to a given command"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
description: "When the user hovers over a ribbon button then the tooltip that pops up says "Press F1 for more help". I would like to change the help file and top..."
author: Autodesk
---
# Change help file and topic associated to a given command

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/change-help-file-and-topic-associated-to-a-given-command.html

## 文章内容

By Adam Nagy
When the user hovers over a ribbon button then the tooltip that pops up says "Press F1 for more help". I would like to change the help file and topic that is shown when the user presses F1 while the tooltip is displayed.
Solution
You can use acedSetFunHelp() from ARX or P/Invoke it from .NET:
// In case of AutoCAD 2013 and above
// replace "acad.exe" with "accore.dll"
[DllImport("acad.exe", CharSet = CharSet.Auto,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "acedSetFunHelp")]
private static extern int acedSetFunHelp(
    string functionName,
    string helpFile,
    string helpTopic,
    int cmd);
  [CommandMethod("AEN1Cmd1")]
static public void Cmd1()
{
    acedSetFunHelp("C:LINE", "acad_acg.chm", "ACG.01.008", 0);
}
This only has effect for the current AutoCAD session and is not persisted in the CUIx file.
This and other ToolTip related settings cannot be changed at the moment using the CUI API for AutoCAD.Customization.Macro.ToolTip is internal.

## 评论

**内容**: Yuji Suzuki said...
This code works on AutoCAD 2012, but it does not work on 2013.
Something was changed on 2013 ?
Reply
09/05/2012 at 11:28 PM

---
**内容**: Andrey said...
Hi Adam.
Data:
Windows XP SP3 x86,
AutoCAD 2013 x86 Enu.
Error message:
System.EntryPointNotFoundException
Message: Unable to find an entry point named 'acedSetFunHelp' in DLL 'acad.exe'.
Reply
09/05/2012 at 11:53 PM

---
**内容**: Andrey said...
Now I wrote for AutoCAD 2009 x86 SP3. Now I don't get errors when I run AEN1Cmd1 and Line commands. But if I press F1, when Line command in process, then I don't get my help. Was opened standard help file, with info about Line command. Why my help file was not open?
My code sampe such:
[CommandMethod("AEN1Cmd1")]
static public void Cmd1() {
acedSetFunHelp("C:LINE", @"C:\Documents and Settings\developer\Рабочий стол\myHelp.chm", "plotting_layouts", 0);
}
Reply
09/06/2012 at 12:08 AM

---
**内容**: Andrey said...
"sample" to read like "example". :)
Reply
09/06/2012 at 12:10 AM

---
**内容**: Adam Nagy said...
Hi guys,
Thank you for the comments.
I've updated the code comments to take AutoCAD 2013 into consideration :)
Cheers,
Adam
Reply
09/06/2012 at 12:47 AM

---
**内容**: Andrey said...
What about my post at 09/06/2012 at 12:08 AM, for AutoCAD 2009?
Reply
09/06/2012 at 01:04 AM

---
**内容**: Adam Nagy said in reply to Andrey...
Hi Andrey,
One thing I started wondering about was the cyrillic characters in the folder name. I created a folder named "C:\Рабочий стол", copied the acadauto.chm file there from "C:\Program Files\AutoCAD 2009\Help" folder and tried to use that, and then I could reproduce the problem that it was not taken into account and still the old help file popped up when I pressed F1 while the tooltip was showing.
However, even if I just double-click on the chm file in Explorer it comes up with the error message:
"Cannot open file: C:\??????? ????\acadauto.chm"
So the error does not seem specific to AutoCAD but has to do with the help file (*.chm file) you are using.
If I copied the access.chm file from "C:\Windows\Help" to this other folder I created, then both double-clicking it in Explorer worked fine and also using it in acedSetFunHelp worked fine:
acedSetFunHelp("C:LINE", @"C:\Рабочий стол\access.chm", "AccessOptions_ct", 0);
So you would need to find out how to make your chm file work in a folder with cyrillic (or I guess any other non-latin) characters in it, and then you could use that in acedSetFunHelp as well.
I hope this helps.
Cheers,
Adam
Reply
09/06/2012 at 03:14 AM

---
**内容**: Andrey said in reply to Adam Nagy...
Thank you for answer.
I thought about it problem and I have tried other variant:
I copied myHelp.chm into "C:\Program Files\AutoCAD 2009\Help" but it ain't working (was opened standard help info for Line command). I wrote it:
acedSetFunHelp("C:LINE", "myHelp.chm", "plotting_layouts", 0);
:(((
Reply
09/06/2012 at 03:35 AM

---
**内容**: Andrey said in reply to Adam Nagy...
I tried to use "native" CHM files by AutoCAD:
acedSetFunHelp("C:LINE", "acad_acr.chm", "WS1a9193826455f5ffa23ce210c4a30acaf-4a8b-reference", 0);
It ain't working too. :(
Reply
09/06/2012 at 03:45 AM

---
**内容**: Adam Nagy said in reply to Andrey...
I'm really sorry Andrey but now I'm running low on ideas. :(
Could you please post this issue on the AutoCAD API forum?
I hope someone already has run into this issue and can help you solve it.
Good luck!
Reply
09/06/2012 at 03:56 AM

---
**内容**: Andrey said in reply to Adam Nagy...
Ok, thank you. :)
Reply
09/06/2012 at 05:11 AM

---
**内容**: Andrey said...
AutoCAD 2013.
Adam, which page must to open your code?
acedSetFunHelp("C:LINE", "acad_acg.chm", "ACG.01.008", 0);
Alwais opened usual help page for Line command. Even if instead of "acad_acg.chm", to "ACG.01.008" to specify another.
Reply
09/06/2012 at 03:21 AM

---
**内容**: Adam Nagy said in reply to Andrey...
acad_acg.chm does not seem to be part of "C:\Program Files\Autodesk\AutoCAD 2013\Help" so just select another chm file that does exist in the help folder. Or if it exists in another folder then provide the full path.
Reply
09/06/2012 at 03:54 AM

---
**内容**: Denica said...
Hi Adam,
thank you for the post, its really helpful! I have tried it and it works great when the command is running or when the mouse is hovering over a ribbon button.
I was wondering, is there a way to do the same for the toolbar buttons?
Reply
06/04/2013 at 02:24 AM

---
**内容**: Adam Nagy said...
Hi Denica,
It seems to be working for toolbar buttons as well as long as they are c:xxx type commands: http://docs.autodesk.com/ACDMAC/2011/ENU/ObjectARX%20Reference/acedSetFunHelp@ACHAR_@ACHAR_@ACHAR_@int.html
Here is a video I made: http://www.screencast.com/t/c3KHYDaEjyhw
If you cannot figure out the problem then you could post some more info on the AutoCAD customization forum.
Cheers,
Adam
Reply
06/07/2013 at 11:20 AM

---
**内容**: Alexander Rivilis said...
Hi, Adam!
What about that LINE is not Autolisp-definded command and so you have to use not "C:LINE", but "LINE" in your's code?
Reply
12/26/2013 at 04:58 AM

---
