---
title: "The Right Tools for the Job – AutoCAD Part 4"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Migration
  - ObjectARX
description: "Leading on from Part 3 I wanted to talk to you about the importance of ObjectARX compiler settings."
author: Autodesk
---
# The Right Tools for the Job – AutoCAD Part 4

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/the-right-tools-for-the-job-autocad-part-4.html

## 文章内容

by Fenton Webb
Leading on from Part 3 I wanted to talk to you about the importance of ObjectARX compiler settings.
As I mentioned before, the code I used to test the performance of the various languages was all written a while ago and that I had decided to port them to AutoCAD 2011 in order to rerun the tests.
When I ported the Visual Studio 2005 ObjectARX and .NET projects to Visual Studio 2008 I simply recompiled in Release mode and started testing.
What I found very strange was that the Release mode .NET tests were running about 35% *faster* than the Release mode ObjectARX tests?!?!? Obviously, this could never be the case because .NET wraps ObjectARX so ObjectARX will always be faster that .NET in the AutoCAD world.
I found that the problem was that the Release mode ObjectARX Compiler Optimization settings were way off, probably due to some Visual Studio project migration issue or maybe even a bug in the old ObjectARX wizard that created the project settings. Once I updated the settings, everything started to work as expected, as you can see in the results that I posted previously.
At this point, I decided to take some time to try and see which settings affected the performance best.
What I found was that, for my test harness code, the Visual Studio Project Property page settings “Optimization=Max Speed” and “Favor Size or Speed=Favor Fast Code” settings displayed in Red below in made the greatest *difference* in performance time, without those set correctly .NET ran faster! Also, you should set the other settings as you can see below - Let’s call is Stage 1 - It got me to around 8.51 seconds for 1,000,000 Xrecords, taken as an average from 3 different test runs…
Notice that I’m not using “Whole Program Optimization” yet. With that setting turned on (and also inside of the Linker Optimization page “Link Time Code Generation” (see just below)),  let’s call this Stage 2, the time went down again to 8.047 seconds, taken as an average from 3 different test runs…
You could be confused by this given that my test harness code is in one .cpp file, but remember that we are linking many ObjectARX modules, so that’s where the optimization comes in.
Next, setting “Enable String pooling=Yes” and “Buffer Security Check=No” surprisingly slowed things down to 8.96. I say surprisingly because I considered that my loop contained items which I figured turning off the Buffer Security Check switch would affect, must be the String pooling that is affecting it…
Changing back “Enable String pooling=No” and keeping “Buffer Security Check=No” did make things run slightly quicker with a time of 8.54, but still not quicker than its default setting, I find this strange…
So it seems that Stage 2 is the best settings for performance on AutoCAD 2011 with Visual Studio 2008, running my specific test harness.
Now to talk a little bit. I’m sure a lot of you out there have read the results of the settings and have not been too surprised about the results, am I right? But how many of your ObjectARX programmers have assumed that the your ObjectARX Release mode settings are optimal as I speak? Do you take time with every release to examine what new settings are and consider what each one might do (or not do) for your application? Did you double check the settings that the Visual Studio Project migration wizard created for you? I know that I don’t
So here’s some basic advice for all you ObjectARX programmers with regards AutoCAD ObjectARX Visual Studio Release mode project settings…
Never assume you have the best Visual Studio Release mode performance settings for your ObjectARX application.
Never trust the migration wizards, always check what they have done.
Visual Studio is always being enhanced, make sure your migrated project has all of the latest, relevant project settings setup – especially for Release mode.
We take a lot of time creating the best Visual Studio project settings for your ObjectARX applications, you should check the ObjectARX samples to see what performance settings you should use.
Next I’m going to look at .NET performance and reveal some performance coding techniques that I use. See Part 5 here

## 评论

**内容**: Owen Wengerd said...
When you use the VS 2008 migration wizard, it inserts a special "Inherited project property sheet" (in the top section of the General configuration properties) that intends to create the same project defaults that were active in the older version of VS. You may find that simply removing that inherited property sheet in your migrated project will result in new default settings that are more optimal, and therefore require fewer project specific overrides.
Reply
07/24/2012 at 11:54 AM

---
**内容**: petcon said...
that is a great post
Reply
07/24/2012 at 10:10 PM

---
**内容**: Fenton Webb said...
Thanks Petcon
Reply
07/25/2012 at 02:00 PM

---
**内容**: Fenton Webb said...
Owen it seems you are 'spamming' us :-)
Reply
07/25/2012 at 02:02 PM

---
**内容**: Owen Wengerd said in reply to Fenton Webb...
Only you, Fenton. You're my favorite spam target. ;)
Reply
07/27/2012 at 06:51 AM

---
**内容**: Loic Jourdan said...
"Never assume you have the best Visual Studio Release mode performance settings for your ObjectARX application."
That's a very good advice indeed!
I've just spent a few time looking at samples optimization and tuning my projects properties, I've so realized how bad they were. I've still not sized gain precisely but it seems it improved some processes slightly.
Thanks
Reply
07/26/2012 at 11:53 PM

---
