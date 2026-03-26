---
title: "Forcing the GC to run on the Main Thread"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "Recently I posted this blog entry on Performance, as you can see at the bottom it drove a lot of comments."
author: Autodesk
---
# Forcing the GC to run on the Main Thread

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/forcing-the-gc-to-run-on-the-main-thread.html

## 文章内容

by Fenton Webb
Recently I posted this blog entry on Performance, as you can see at the bottom it drove a lot of comments.
One question that came up was when to call Dispose(). The thing is that all of our .NET code wraps ObjectARX, in turn, all of our ObjectARX code is single threaded and the .NET Garbage Collector runs on a background thread... What this means is, if you don't call Dispose() on our AutoCAD .NET objects (the ones you create in your code) you run the high risk of the GC garbage collecting our objects on a background thread, which in turn may cause AutoCAD to crash.
That said, a crash happening really does depend on what the AutoCAD implementation of the Dispose code does under the hood. If the Dispose() simply does a memory free for which any destructors do nothing, then you’re probably going to be fine. However, if the dispose does other things like fire events, update UI, etc etc, then you are most likely looking at a crash. Therefore, I recommend you Dispose() all AutoCAD .NET objects (the ones you create in your code) using the .NET 'using' statement – that way you are not relying on the GC to clean up after yourself.
Now, say you are at a customer site where they are experiencing random crashes with your app, or you are running behind schedule and just can’t seem to find the place where the random crash is happening then here’s a quick fix for you – try forcing the GC to run on the Main Thread…
There is a setting that can be applied to the acad.exe.config file called gcConCurrent. See http://msdn.microsoft.com/en-us/library/yhwwzef8.aspx
An example of this being implemented in the acad.exe.config file is shown thus:
<configuration>
  <startup useLegacyV2RuntimeActivationPolicy="true">
    <supportedRuntime version="v4.0"/>
  </startup>
  <!--All assemblies in AutoCAD are fully trusted so there's no point generating publisher evidence-->
   <runtime>       
       <generatePublisherEvidence enabled="false"/>   
       <gcConcurrent enabled="false" />
   </runtime>
</configuration>

## 评论

**内容**: Loic Jourdan said...
btw, is there any plan to bring some multi thread abilities within acad apis?
Wouldn't it be valuable regarding modern processor architecture?
Thank you
Reply
07/30/2012 at 11:06 PM

---
**内容**: Fenton Webb said...
The internal product is slowly turning multi-threaded, however, it won't be available to access through the API's for a long time to come. This is because it's such a huge code base.
Reply
07/31/2012 at 09:07 AM

---
**内容**: Loic Jourdan said...
I can imagine indeed
In a way, this isn't a bad news, if core acad turns multi-threaded (even slowly), we'll get those threads for free!
thanks
Reply
07/31/2012 at 11:40 PM

---
**内容**: pseudonym said...
" Therefore, I recommend you Dispose() all AutoCAD .NET objects using the .NET 'using' statement – that way you are not relying on the GC to clean up after yourself."
Sorry, I must be missing something here.
I thought the whole point to writing code that runs in a 'managed' execution environment, was so that the programmer could rely on the GC to clean up after themself, and offload tasks that C/C++ programmers must routinely do manually (e.g, free memory and call d'tors) or with the help of smart pointers.
When we write managed code, we are *always* relying on the GC to clean up the managed objects we create and use (whether they implement IDisposable or not), and we do not need to be concerned with deallocating those objects or the memory they consume, calling d'tors, etc.
Given that, I'm somewhat bewildered by your statement, and you can read more about that here:your advice:
http://www.theswamp.org/index.php?topic=42399.0
Reply
08/03/2012 at 10:46 AM

---
**内容**: Fenton Webb said in reply to pseudonym...
Hey Pseudonym
Actually, I think you misunderstood what I said...
I do mention at the end of that sentence "to cleanup after yourself" - meaning, that you should clean up *YOUR* objects not AutoCAD's.
I noted your comments on the link you posted and I really think it's fairly obvious that you should not dispose of master property objects such as MdiActiveDocument? As common in any computer language, you don't dispose/delete/free objects that are not under your control.
Yes .NET is super cool, but you should still think about what you are doing a bit. Also, the bottom like is that the AutoCAD .NET API wraps ObjectARX, that means you absolutely cannot rely on the GC to Dispose AutoCAD Database objects, and, you shouldn't rely on the GC to Dispose all other AutoCAD .NET classes.
Thanks for pointing this out though, I appreciate your comments. Keep them coming!
Reply
08/03/2012 at 01:27 PM

---
**内容**: pseudonym said...
"Actually, I think you misunderstood what I said."
Well in that case, I don't think I'm alone in that regards.
Reply
08/05/2012 at 12:43 AM

---
