---
title: "Getting started with AccoreConsole"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "AutoCAD 2013 has a command line version of AutoCAD that can help you with significantly faster batch processing of drawings. Please note that the u..."
author: Autodesk
---
# Getting started with AccoreConsole

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/getting-started-with-accoreconsole.html

## 文章内容

By Balaji Ramamoorthy
AutoCAD 2013 has a command line version of AutoCAD that can help you with significantly faster batch processing of drawings. Please note that the use of this utility is not officially supported by Autodesk. Here is a quick introduction to get you started with it.
In the AutoCAD 2013 install folder, you can find the "AccoreConsole.exe". Just running it will display the command line switches that can be used with it.
It accepts four command line switches :
1) /i : Used to specify the drawing file path on which to run the script file
2) /s : Used to specify the path to the script file.
3) /l : If language packs are installed, you have the choice to invoke the language version of accoreconsole. The commands in the script file can then be in one of the languages that you have installed in your system.
4) /isolate : Used to prevent the changes to the system variables from affecting regular AutoCAD.
As an example, it is most common to set the "FILEDIA" system variable to 0 in your script files.
But if you do not want this system variable change to take effect when you start regular AutoCAD the next time, then you can use the "isolate" switch. This ensures that changes are kept local to accoreconsole.
Finally, if you need more details regarding AccoreConsole, have a look at the DevTV.
AccoreConsole DevTV
Happy batch processing !

## 评论

**内容**: Ted said...
Hi Balaji,
I was testing the AccoreConsoleDemo application and on the custom tab I am trying to netload a custom .dll from the network but getting the error:
Could not load file or assembly.
Is loading from network not supported?
Thanks,
Ted
Reply
09/12/2012 at 02:39 PM

---
**内容**: Andrey said in reply to Ted...
Error not in it. Read the link which I specified below, then you will understand a cause of error.
Reply
09/13/2012 at 07:04 AM

---
**内容**: Ben said in reply to Ted...
the .net dll has to be in a "trusted" autocad location. perhaps that is your issue? please google how to add that particular folder to autocad's trusted list --- open autocad and get to options, and find trusted locations and then add it there.
Reply
01/17/2017 at 04:14 AM

---
**内容**: Balaji said...
Hi Ted,
Sorry, I haven't tried this with accoreconsole.
I will give it a try and let you know based on what I find.
Meanwhile, can you please try this suggestion and see it helps ?
http://adndevblog.typepad.com/autocad/2012/09/error-netloading-plugin-from-network-location.html
Thanks
Balaji
Reply
09/13/2012 at 05:39 AM

---
**内容**: Andrey said in reply to Balaji...
>Happy batch processing !
I think, you early promote AcCoreConsole. Sorry, but it is very curve program. Read about this bugs there: http://www.theswamp.org/index.php?topic=41918.msg471067#msg471067
Reply
09/13/2012 at 07:00 AM

---
**内容**: Ted said in reply to Balaji...
Yes, I have that setting in my acad.exe.config file.
Reply
09/13/2012 at 09:08 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said in reply to Ted...
> Ted
Maybe your dll file name (or its path) are contains one or more not English chars?
Reply
09/13/2012 at 10:42 AM

---
**内容**: Balaji said in reply to Ted...
Hi Ted,
I tried providing a network path in a script file and then using it with accoreconsole.exe and it worked ok. Are you trying it from the command prompt ? When I tried it with the demo app, although it works, it does not display the output in the window.
So, I suggest trying to use the accoreconsole from the command prompt. I have attached the screenshots that might be of some help.
https://www.dropbox.com/s/27gp11wfkt0sawc/1.png
https://www.dropbox.com/s/7ewzqnf21qybrf6/2.png
Reply
09/14/2012 at 01:24 AM

---
**内容**: Ted said in reply to Balaji...
Thanks Balaji,
Can you try using the path to a dll file like this...
\\servername\folder\dll
Reply
09/14/2012 at 09:51 AM

---
**内容**: Balaji said in reply to Ted...
Hi Ted,
I tried it and it works ok.
Here are the screenshots that might be of some help. Have you used it like ""\\\\bancnd0300n12\\Cases\\NetTest1.dll" ?
Pleae note the extra \ that is needed.
Here are the screenshots :
https://www.dropbox.com/s/2ok54ilkqdnolex/3.png
https://www.dropbox.com/s/bnzjq38zxer5g00/4.png

Reply
09/17/2012 at 03:54 AM

---
**内容**: Ted said in reply to Balaji...
Hi Balaji,
I tried as you said, it works when I am in autocad 2013, but when I am in the accoreconsole I get an error:
Cannot load assembly. Error details: System.IO.FileLoadException: Could not load file or assembly
I'm typing exactly what I typed into the AutoCAD 2013 command line as I am the accoreconsole... any ideas why it would not work?
Thanks for the help
Reply
09/18/2012 at 06:15 AM

---
**内容**: Balaji said in reply to Ted...
Hi Ted,
Can you please share the script file, the drawing file and any other step that will help me in reproducing the issue ?
I have come across such issues where a netload doesnt work inside AutoCAD. In such cases, running the caspol solves the issue.
CasPol.exe -m -ag 1.2 -url X://Acad/TrustedAssemblies/* FullTrust
Because it is working inside AutoCAD, I am not sure what else to suggest.
If you can help me reproduce the problem, I can investigate this.
Also it might help if you can try with another network share to see if it specific to a network location.
Reply
09/21/2012 at 05:22 AM

---
**内容**: Ted said in reply to Balaji...
Balaji I got it figured out finally. I didn't realize there was a separate config file for accoreconsole (accoreconsole.exe.config). I added this to the config file and it worked.
Reply
09/25/2012 at 03:31 PM

---
**内容**: Balaji said in reply to Ted...
Hi Ted,
I am glad you resolved the issue and thanks for sharing the solution with us.

Reply
09/25/2012 at 10:01 PM

---
**内容**: Ben said in reply to Balaji...
Hello Balaji
thank you for this great utility.
Is it possible to show simple examples of it netloading a .net file.
I tried using your example which you attached in the samples provided but I could not get it to work - here is the relevant post in the forums: http://forums.autodesk.com/t5/net/netloading-dll-from-a-script-file-for-batch-processing/td-p/5944940
and I could not find much documentation on the AccoreConsole
any knowledge would be invaluable to me and to folks who will want to do the same thing.
rgds
Ben
Reply
12/10/2015 at 03:57 AM

---
**内容**: Andrey said...
If this errors will corrected, then a program will be very useful. But today it is bad program...
Reply
09/13/2012 at 07:03 AM

---
**内容**: Balaji said in reply to Andrey...
Hi Andrey,
I understand your frustration :(
We have logged these requests with our engineering team based on your feedback and they will be prioritized.
I agree that at present it does not work with localized version of AutoCAD but it still has its capabilities.
Reply
09/14/2012 at 01:29 AM

---
**内容**: fred said...
Can we load and defun lisp in accoreconsole?
I try to plot all layout with accoreconsole. I can't find a way to load a lisp in accoreconsole.
Reply
12/04/2014 at 01:39 PM

---
**内容**: Balaji said...
Hi Fred
Sorry for the delay.
you can load Lisp, but the COM API (vla) functions do not work in acccoreconsole.
Plotting of all layouts should be possible using a custom .Net / crx plugin loaded in accoreconsole.
Please do let me know if you need any help with this.
Regards,
Balaji
Reply
12/11/2014 at 01:27 AM

---
**内容**: Fred said in reply to Balaji...
Hi,
Thanks for your reply,
I find a way to plot all my layouts. I use publish and a DSD botch created with a batch.
The main problem is I can't use Diesel Commands (nor Xpress Tools Rtext). I try to load Rtext in a accoreconsole, but I can't plot where rtext with Diesel commands inside. Autocad makes me a white rectangle.
But I love accoreconsole, when I use it, I increase my speed x2.
Reply
12/16/2014 at 05:58 AM

---
**内容**: Andrea Andreetti said in reply to Balaji...
Hi,
sorry to interrupt this...
accoreconsole work great with LISP/VLISP application....you must think different and use coreconsole only to open file and not run script.
Reply
03/18/2015 at 12:00 PM

---
**内容**: Balaji said in reply to Andrea Andreetti...
Hi Andrea,
If you can please share more details on how you got the vla functions to work with accoreconsole, we will all learn. Thanks
Regards,
Balaji
Reply
03/19/2015 at 10:36 PM

---
**内容**: NewGirl said in reply to Andrea Andreetti...
I am having trouble with VLISP commands. Do you have any helpful tips?
Reply
06/04/2018 at 11:16 AM

---
**内容**: Sergio Aviles said in reply to Andrea Andreetti...
Just stumble in to this, Would you be so kind to elaborate as to How did you make Accoconsole to work with Vlisp?
Reply
07/27/2023 at 09:07 PM

---
**内容**: Balaji said...
Hi Fred,
Sorry, that would not be possible in Accoreconsole. RText is a custom entity from the Express tools implemented in a .arx module and is not available for loading in coreconsole.
If possible, you can have Rtext in such drawings exploded as regular text and then use them with accoreconsole.
Regards,
Balaji
Reply
12/18/2014 at 02:47 AM

---
