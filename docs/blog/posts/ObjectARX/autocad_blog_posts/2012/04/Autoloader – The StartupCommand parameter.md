---
title: "Autoloader – The StartupCommand parameter"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "Autoloader was added in AutoCAD 2012 to simplify the deployment of AutoCAD plug-ins, and is extensively used by apps in the Autodesk Exchange Store..."
author: Autodesk
---
# Autoloader – The StartupCommand parameter

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/autoloader-the-startupcommand-parameter.html

## 文章内容

By Stephen Preston
Autoloader was added in AutoCAD 2012 to simplify the deployment of AutoCAD plug-ins, and is extensively used by apps in the Autodesk Exchange Store. (You’ll find several articles about the general Autoloader features on Kean’s blog).
We introduced a few enhancements to Autoloader in AutoCAD 2013. One of which was the StartupCommand parameter. Use this if you have a plug-in that loads on AutoCAD startup and you want it to run a command as soon as its loaded. The benefit of using a StartupCommand is that the entire AutoCAD UI should be loaded when the command runs - which isn’t always the case when you run initialization code by implementing IExtensionApplication.Initialize in your plug-in.
Here is a Components section from an Autoloader PackageContents.xml that causes a command called RunMeFirst to be invoked at startup for AutoCAD 2013 or any AutoCAD 2013 vertical:
  <Components>
    <RuntimeRequirements OS="Win64|Win32" Platform="AutoCAD*" SeriesMin="R19.0" SeriesMax="R19.0" />
    <ComponentEntry AppName="ADN_StartupCommandTest" ModuleName=".\Contents\SimpleTest.dll">
      <Commands GroupName="ADN_StartupCommandTest">
        <Command Local="RunMeFirst" Global="RunMeFirst" StartupCommand="True" />
      </Commands>
    </ComponentEntry>
  </Components>
  To try this, download the sample bundle from here and unzip it into your %appdata%\Autodesk\ApplicationPlugins folder. The next time you launch AutoCAD 2013, it will run the command – which simply prints “Hello World” to the command line. (Note that the sample DLL is built for AutoCAD 2013, and the PackageContents.xml restricts loading to AutoCAD 2013 only – this is because StartupCommand was only introduced in the 2013 release).

## 评论

**内容**: Greg B said...
Thanks for giving an example for the startup command. Can you please give an example for loading custom content that doesn't need to be ran upon starting up?
I would like to test this new feature for loading some lisp files and a couple DLLs.
~Greg
Reply
04/23/2012 at 09:24 AM

---
**内容**: Madhukar Moogala said...
Hi Greg,
If you follow the link in the above post to the information on Kean's blog, then you should have all the information you need to create your XML. Please let me know if there's some information you need missing from there.
Unfortunately, this blog won't allow me to quote XML in a comment, so I can't post a specific example in this comment. But all you need to do in the example XML above is to remove the StartupCommand="True" parameter from the Command element and add a LoadOnCommandInvocation="True" parameter to the ComponentEntry element. That will work for ObjectARX and .NET DLLs from AutoCAD 2012, and for LISP from AutoCAD 2013.
Cheers,
Stephen
Reply
04/23/2012 at 09:47 AM

---
**内容**: Cattoor Robby said...
For some reason your bundle doesnt work for me in AutoCad 2013.
Intellisense recognizes the RunMeFirst command but when executed the command seems to be UNKNOWN.
Any idea what the problem could be?
Am I missing something here?
Reply
05/12/2012 at 04:22 PM

---
**内容**: Madhukar Moogala said in reply to Cattoor Robby...
Hi Cattoor,
Sorry for the late reply. I somehow overlooked this comment. Your problem could be due to this - http://labs.blogs.com/its_alive_in_the_lab/2011/05/unblock-net.html
Cheers,
Stephen
Reply
06/01/2012 at 05:53 PM

---
**内容**: Cattoor said in reply to Madhukar Moogala...
For some reason I thought I would 've been notified by mail once you answered on my post. Apparently not :) Not sure why I thought it would really. Good thing I accidently stumbled upon this thread again.
Thank you for replying, I will sure look into it and let you know if it resolved my problem.
Currently I am still developing on 2012 Autocad and Autocad Map + Topobase but slowly I am integrating some old projects into 2013.
This might come in handy...
Thanks again Stephen!
Robby
Reply
07/16/2012 at 03:21 PM

---
**内容**: AlexFielder said...
Hi Stephen,
Are you able to share the source for this bundle?
I'm having a hard time getting the AutoLoader to work for my latest application.
Thanks,
Alex.
Reply
05/18/2012 at 08:07 AM

---
**内容**: Madhukar Moogala said in reply to AlexFielder...
Hi Alex,
Do you mean the source code for the .NET DLL in the bundle? I think I threw it away because it was really simple - it just defines a single command. You're welcome to email me a simple bundle you're having trouble with and I'll take a look. I think you know my email address. (Or post the code on the Autodesk forum and tell me when its there).
Cheers,
Stephen
Reply
05/18/2012 at 08:36 AM

---
**内容**: AlexFielder said in reply to Madhukar Moogala...
An email is on its way. Thanks :)
Reply
05/18/2012 at 09:06 AM

---
**内容**: John Murray said...
Hmm... I have not been able to get this to work yet with autoloading. Even with the sample that you've provided. I am running AutoCAD R19.0.55.0. Is there anyone I can talk to about this?
Reply
10/17/2012 at 06:23 AM

---
**内容**: Madhukar Moogala said in reply to John Murray...
John and I discussed this offline. If you have the LAYER palette open, then it prevents the StartupCommand being invoked. Our engineering team have been informed.
Reply
10/25/2012 at 05:02 AM

---
**内容**: Daniel said...
Hello Stephen,
I'm using the Autoloader for my Apps. Since I tend to use several bundle's it's getting annoying to see all the balloon tips on loading them. Is there a way to turn off balloons? (ACA2012) Turning off the Infocenter is not an option. The Balloon setting in the reg for IC doesn't seem to impact Autoloader Balloons...
Thanks in advance,
Daniel
Reply
06/20/2013 at 05:02 AM

---
**内容**: John said in reply to Daniel ...
Hi,
I have the same issue with my custom bundles and our customer was asking if these balloons could be removed. Did you ever find a solution?
Cheers
John
Reply
08/22/2013 at 01:16 AM

---
**内容**: Daniel said...
Hello, it's me again :-)
so I noticed, that even if I change the IC-Balloon settings, they will set back to default on ACAD-Start...some config file somewhere...?
Regards,
Daniel
Reply
06/20/2013 at 05:05 AM

---
**内容**: Russell said...
Hi, It would be helpful if the ADNStartupCommandTest.bundle example included the source files used to create SimpleTest.dll. The xml definition of StartupCommand is only one part of the process. As it is, I don't know how to define the actual startupcommand such that AutoCAD finds and executes it.
Thanks, Russell S.
Reply
07/09/2015 at 11:54 AM

---
**内容**: Russell said in reply to Russell...
meant to include, a C++/ObjectARX example would be helpful.
Reply
07/09/2015 at 11:57 AM

---
