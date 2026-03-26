---
title: "Visual Studio 2012 – First Impressions"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Unicode
description: "I’m a little late to the game here. I know using VS2012 for AutoCAD .NET development is being discussed on various forums. But hey - Its Friday aft..."
author: Autodesk
---
# Visual Studio 2012 – First Impressions

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/visual-studio-2012-first-impressions.html

## 文章内容

By Stephen Preston
I’m a little late to the game here. I know using VS2012 for AutoCAD .NET development is being discussed on various forums. But hey - Its Friday afternoon and I have a few minutes left before the weekend starts, so take this blog post for what it is – a displacement activity .
I installed Visual Studio 2012 Premium (from my MSDN account) to play with some time ago, but I’ve only just found the time to actually launch it this week. [Sigh – This is why my business card describes me as a manager these days, rather than a programmer ].
Installation went smoothly on my Bootcamped Win7 MacBook Pro (no glitches, crashes or lost data). Although the installer is a sign of what’s to come: its all white text on a black background – not very kind on my eyes.
I opened a VS 2010 .NET test project I had lying around and hit F5. It built without problem, AutoCAD 2013 launched as expected, and I could NETLOAD and use the DLL without problem. I changed the project to target .NET Framework 4.5. Again – the DLL worked with no problem – as expected. This in itself is not a good indicator that larger projects ‘will just work’ – most of the stuff I have lying around on my laptop these days are small samples and proofs of concept. So I pinged the internal email alias used by our AutoCAD development team for discussing .NET issues to see if anyone had come across any bugs in the IDE or issues related to writing and debugging .NET code in VS2012 (our engineering team have been testing VS 2012 throughout the Beta cycle). The answer came back loud and clear:
No problems here. Everything is working fine with VS2012.
There were a few issues during the Betas, but they all seem to have been ironed out now. So that’s the closest I can get at the moment to saying go ahead and use VS2012 for your AutoCAD 2013 .NET projects – it should work fine. (If you do find any issues, then please post a comment and I can document them here for others).
Follow these links for some information general Microsoft API compatibility issues:
http://msdn.microsoft.com/en-us/library/hh367887.aspx
 http://msdn.microsoft.com/en-us/library/ff602939.aspx
That said, I really have to add that my first impression of the UI is not positive. I hope to get used to it, but the uppercase menus and the black (and blue) icons look like very retro to me (and not in a good way). Kind of reminds me of using WordPerfect on DOS.
Eek!
BTW You can use VS2012 for for (C++) ObjectARX 2013 development too. You have to set the Platform Toolset for a project to VC100 (in a similar way you could use VS2010 with VC90). I’ve not checked whether VC100 comes with VS2012 or not. I have VS2010 installed so it was already there anyway.

## 评论

**内容**: Justin Ralston said...
Stephen
Can you confirm if Edit and Continue in debug still does not work on a 64 bit platform.
Justin
Reply
09/15/2012 at 02:24 AM

---
**内容**: Madhukar Moogala said in reply to Justin Ralston...
Alas - no. See the note on this MSDN page - http://msdn.microsoft.com/en-us/library/ms164926.aspx.
Reply
09/15/2012 at 09:38 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said in reply to Justin Ralston...
>Edit and Continue
What is it? I have MS VS 2012 x64 & AutoCAD 2013 SP1.1 - I can check it now.
Regards
Reply
09/15/2012 at 09:51 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
My previous question isn't so actual. :)
Reply
09/15/2012 at 09:54 AM

---
**内容**: Matus said...
I was putting so much hope in the Edit & Continue
I guess, I will have to stick with my old XP machine for development. But it also has advantages. It's so slow, that it forces me to look into optimization in the places, where it won't come to mind on a faster machine :)
Reply
09/16/2012 at 04:36 AM

---
**内容**: Huffine said...
Just curious... doesn't AutoCAD run on a three-year cycle regarding binary compatibility? And doesn't that affect the version of Visual Studios that you use as well? If that's so, then what is the next major release and when should we expect VS 2010 to become an issue?
Reply
09/17/2012 at 05:10 AM

---
**内容**: Madhukar Moogala said in reply to Huffine...
There's a difference between being forced to upgrade your compiler and being able to do so if you want to. VS2012 with Acad2013 is a case of the latter. For your specific question - sorry, but I can't talk about product futures in a public forum, but we'll be presenting information on futue releases through the ADN website and at our ADN DevDays conferences as usual.
Reply
09/17/2012 at 10:39 AM

---
**内容**: PDOTeam said...
For those bothered there is still no edit and continue for x64: https://connect.microsoft.com/VisualStudio/feedback/details/736684/edit-and-continue-is-not-supported-when-debugging-a-64-bit-application
Reply
09/17/2012 at 07:34 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
What is this?
https://skydrive.live.com/redir?resid=51B3145B64E05FEF!540
Reply
09/27/2012 at 10:10 AM

---
**内容**: Madhukar Moogala said in reply to Andrey Bushman (@AndreyBushman)...
If you hover your mouse over each one of those, you'll see that each is for a different language. That just means that the help text associated with the interfaces is localized for each one. AutoCAD installs all the language versions.
But you shouldn't be referencing these directly from a .NET application - you should be referencing the Interop DLLs shipped with the ObjectARX SDK, and using type embedding so you don't have to ship the Interop DLL with your application.
Reply
09/27/2012 at 10:28 AM

---
