---
title: "Performance – perception versus reality"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoLISP
  - Block
  - DWG
  - Database
description: "A good comment on performance to my ObjectId.GetObject post by Anonymoose (a.k.a. Tony Tanzillo) reminded me of some fun discussions I had with Fen..."
author: Autodesk
---
# Performance – perception versus reality

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/performance-perception-versus-reality.html

## 文章内容

By Stephen Preston
A good comment on performance to my ObjectId.GetObject post by Anonymoose (a.k.a. Tony Tanzillo) reminded me of some fun discussions I had with Fenton a while ago about how important it is (or not) to optimize your code to squeeze it for every possible nanosecond of performance that I thought was worth summarizing here. (Thanks for the prod, Tony).
The answer to the question, of course, is that it depends.
For real-time trading systems, it is claimed that a microsecond latency and processing delay can ‘cost’ a company approximately $1million per day in unrealized profits.
Then there’s the apocryphal tale of the development team who profiled their software and found that it spent over 90% of its time executing one loop. After weeks of optimization effort, the profiling showed the program was still spending the same fraction of its time in that same loop. That was when they realized that they’d just invested several $100,000 in optimizing their idle loop. (This is probably the same apocryphal company that paid its testers a bonus for every new bug they found and paid its programmers a bonus for every bug they fixed) .
If you’re performing a long operation, or a batch operation, that is tying up the users machine for minutes, hours, or even days, then its definitely worth investing in speeding up your batch process. A good example of this was an ADN partner (hi Jack, if you’re reading this ) who came to our very first DevLab. He had a LISP routine that batch processed (a lot of) drawings to update their title blocks, and had come to DevLab to find out if converting the routine to .NET would speed things up. It did – he used Database.ReadDwgFile() in .NET to open each DWG as a side database instead of opening each in a document as he’d done in LISP – the result was that a batch process that previously took all night completed in just a few minutes.
If you can’t significantly speed up a long operation, then you may be able to move the process to the cloud so your user can carry on using their computer as the process runs.
The benefits of optimization or ‘cloudification’ (I made up that word ) are very clear for these long, uninterruptable operations. But many of us are writing applications that require interaction with the user. Once you have a human involved, its not just about stopwatches – psychology plays a big part in the user’s perception of whether your software ‘feels’ fast or slow. Something simple like adding a well designed progress indicator can make the user feel that the application is faster without you having to optimize any code at all. Conversely, if you do optimize your code, there is a threshold you have to exceed before the user actually notices. And if your code is stopping to ask the user to pick points on the screen, it doesn’t matter how long the code that processes those points takes to run – as long as the user doesn’t ‘perceive’ a delay. Any optimization work over and above removing the ‘perception’ of a delay is essentially wasted effort.
An example: If you have a VMWare (or similar), try installing AutoCAD (or any other application that uses a progress bar in its installer). Then reset the VMWare and run the installation again, but with a piece of sticky tape covering the progress indicator. Which ‘feels’ quicker'?
There are lots of books, studies, white papers etc. on this topic. Go ahead and Google, or ask your friendly neighborhood user experience designer. My quick search uncovered these two straightforward blog posts that summarize the blogger’s takeaways from reading this book. The book’s author has posted a handy public cheat sheet here. Some of the points made are very interesting, and (for me at least) not at all intuitive.
Finally, I promise to ask Fenton to write up a blog post on the relative speeds of different AutoCAD APIs and API constructs based on the work he did for an AU class several years ago. (Whether he agrees to do it is another matter, of course ).

