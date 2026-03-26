---
title: "New 2014 Configurable AutoCAD Installation Structure"
date: 2013-06-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
description: "In case you haven’t spotted it yet, AutoCAD and verticals have started adopting the ‘Configurable AutoCAD Structure’ for 2014."
author: Autodesk
---
# New 2014 Configurable AutoCAD Installation Structure

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/new-2014-configurable-autocad-installation-structure.html

## 文章内容

by Fenton Webb
In case you haven’t spotted it yet, AutoCAD and verticals have started adopting the ‘Configurable AutoCAD Structure’ for 2014.
What this means is that verticals no longer install to separate program files folders, but instead install off a child folder of AutoCAD… e.g.
C:\Program Files\Autodesk\AutoCAD Plant3d 2013
Is now
C:\Program Files\Autodesk\AutoCAD 2014\PLNT3d
  Status
Default Folder Name
AutoCAD
Adopted
(Parent)
AutoCAD Electrical
Adopted
AcadE
AutoCAD Mechanical
Adopted
Acadm
AutoCAD MEP
Adopted
ACA and MEP
AutoCAD Plant 3D
Adopted
PLNT3D
AutoCAD P&ID
Adopted
PNID
AutoCAD Utility Design
Future Adoption
  AutoCAD Architecture
Adopted
ACA
AutoCAD Structural Detailing
Adopted
ASD
AutoCAD Civil 3D
Adopted
C3D
AutoCAD Map 3D
Adopted
Map
AutoCAD ecscad
Future Adoption
  NOTE: This change affects all developers who target vertical install folders.
Update (April 2016): The above table was updated to include Civil 3D, Map 3D and Mechanical that also adopted configurable installation.

## 评论

**内容**: Jeremy Tammik said...
Hi Fenton,
I see from your post that Plant 3D is magically converted into an abbreviated string PLNT3d.
Is it up to each developer to guess the appropriate string for her product?
Or is a list of these abbreviations provided somewhere?
Thank you!
Cheers, Jeremy.
Reply
06/28/2013 at 10:54 AM

---
**内容**: Dave Wolfe said...
The way I found it was installing the program.
Fenton, is the purpose for the switch to cut down on installation/installer size? I think it'd be great if there were some system variables we could retrieve these values from. For both Acad files, and then plant/vertical specific files. It is more awkward having dependencies in two places.
Reply
06/30/2013 at 04:15 AM

---
**内容**: Fenton Webb said...
Hey David
the purpose is:
1) Reduce size
2) Reduce sp logistics. Example, currently, there is a separate 'AutoCAD' related sp with every vertical.
3) Reduce version creep incompatibilities. Example, where verticals use updated AutoCAD modules
4) Reduce side-by-side issues
Reply
07/01/2013 at 11:27 AM

---
**内容**: Fenton Webb said...
Hey Jeremy
I have updated the table to suit!
Reply
07/01/2013 at 11:27 AM

---
**内容**: Dave Wolfe said...
So, does the mean we'll have to setup the AppDomain.AssemblyResolve and handle loading our dependencies through there?
Reply
07/19/2013 at 08:28 AM

---
**内容**: Fenton Webb said...
Hey Dave!
not at all... You only need to subscribe to that event if your DLL resides completely away from the parent exe, child folders of the main exe folder are fine.
Reply
07/19/2013 at 09:06 AM

---
**内容**: Dave Wolfe said...
Thanks!
Reply
07/22/2013 at 05:45 AM

---
**内容**: Steve B said...
Hi Fenton,
I've ran into one major problem with this new model. I have a .net application that starts AutoCAD. The machine has both AutoCAD and Plant 3D 2014 installed on it. When I start AutoCAD from my application it opens the last AutoCAD product that was used. I use the /product switch and that works, but the problem is if Plant 3D was the last application opened it pulls a Plant 3D license. This a very expensive problem. I did notice that if I use the basic AutoCAD shortcut then basic AutoCAD starts and pulls a basic AutoCAD licenses. Here's my line of code I use to start AutoCAD:
Shell("C:\Program Files\Autodesk\autocad 2014\acad.exe /product ACAD /nologo /p " & Chr(34) & "<>" & Chr(34), AppWinStyle.NormalFocus)
I've used the procces.start as well, but I get the same results.
Can you help????
Reply
03/31/2014 at 10:55 AM

---
**内容**: Fenton Webb said...
I don't have AutoCAD installed at the moment, but can't you just use the normal AutoCAD Shortcut command line params? Basically, I can't test this myself right now, sorry...
Reply
03/31/2014 at 12:51 PM

---
**内容**: Steve B said in reply to Fenton Webb...
Not trying to be smart, but If you look at the line of code I posted you'll see I am using the AutoCAD Shortcut command line params. I'm setting the /product key to ACAD. That part works great. The problem is it's still pulling a Plant 3D license... Thanks for the response. If I get this resolved, I'll post the fix here if you would like.
Reply
04/01/2014 at 05:26 AM

---
**内容**: Balaji said in reply to Steve B...
Hi Steve,
I have AutoCAD 2014 and Plant3D 2014 installed in my system. Using "/product ACAD", AutoCAD launches as expected. But I am unable to figure out which license its using. Do you use a network license ?
Sorry if this is a dumb question : How do you see that AutoCAD is pulling the Plant3D license in your case ?
If you have posted this query in the discussion forum, please do let me know. I will follow it up there.
Regards,
Balaji
Reply
04/02/2014 at 12:32 AM

---
**内容**: Fenton Webb said...
No problem, I didn't realize it was the same thing :-)
You might be better off posting this question to the forums - have you tried that?
Reply
04/01/2014 at 08:53 AM

---
