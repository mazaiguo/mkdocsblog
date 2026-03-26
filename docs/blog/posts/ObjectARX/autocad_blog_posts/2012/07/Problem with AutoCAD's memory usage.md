---
title: "Problem with AutoCAD's memory usage"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - DWG
  - Database
description: "An application has to process a lot of data in approximately 50,000 drawings, collect information from every drawing with a recursive function that..."
author: Autodesk
---
# Problem with AutoCAD's memory usage

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/problem-with-autocads-memory-usage.html

## 文章内容

By Augusto Goncalves
An application has to process a lot of data in approximately 50,000 drawings, collect information from every drawing with a recursive function that calls itself for every subdirectory, looking for DWG files in the directory, something similar to this blog post Batch process in-memory.
After processing the DWG file, the Database variable gets out of scope and the
destructor is called. This should release all memory associated with this instance of Database. However, the destructor does not release all memory assigned to the instance of Database. When processing all these drawings, about 50 MB memory is lost. Is it possible to release all the memory or is there a memory leak in AutoCAD?
This is a general problem of the C++ memory manager, that also happens to .NET languages, and happens due to memory fragmentation, and it probably cannot be avoided.
If an (internal) AutoCAD function needs memory, AutoCAD asks the operating
system for it. Normally, if the function has finished, AutoCAD releases the used
memory and the memory manager gives it back to the operating system. The problem is that the memory manager can release the memory (gives it back to the
operating system) only if it is not fragmented.
Let's say the function 'a' allocates 1 MB, and another function 'b' allocates 100 KB. The operating system assigns a 1.1 MB memory block to the application. If the function 'a' releases its 1 MB, the memory manager cannot give the memory back to the operating system because there is still 100 KB in use. The memory manager marks the 1 MB as free. If a third function 'c' allocates now less than 1 MB, the memory manager knows that it has already 1 MB of free memory and assigns the needed memory to the calling function. It does not ask the operating system for more memory. If function 'b' now releases its 100 KB, the memory manager cannot give the memory back to the operating system, because function 'c' uses now memory from the original 1,1 MB memory block.
If function 'c' allocates 500 KB, there is still 500 KB available. If the first function now needs 1 MB again, the memory manager needs to allocate a new memory block from the operating system (with a size of 1 MB; it's not possible to get 500 KB from one memory block and the other 500 KB from a second memory block).
To release all memory you have to quit AutoCAD. Therefore, it is safe to say that it is not possible to read up to 50,000 drawing files in one session without incurring any memory loss.
There are only two possible work-arounds. The first is to increase the amount of
physical RAM installed on the computer. The second one is to close AutoCAD after
processing some files. Restart AutoCAD and use your functions again. You could
write your current application status into a file. When restarting, you could analyze your previous application state and continue from it.
Starting on 2013, AutoCAD can run on console mode, which makes easier to restart the process and therefore better use release the memory.

## 评论

**内容**: Yvon Bourgouin said...
Hi Augusto, could you tell me what you mean by "Starting on 2013, AutoCAD can run on console mode, which makes easier to restart the process and therefore better use release the memory.". We have an autolisp which is running perfectly fine but when we translated in .NET to do the same thing, the memory is growing real until we have to restart AutoCAD. We don't have that problem in the autolisp version.
At the moment, we have to stay with the autolisp version even if it is slower. Any help? We are part of ADN
Reply
07/12/2012 at 12:36 PM

---
**内容**: Augusto Goncalves said in reply to Yvon Bourgouin...
Hi Yvon,
Until AutoCAD 2012 we had to restart the full acad.exe process, which is quite heavy, but now on 2013 we have a faster/lighter version with the console, that we can restart quite fast. Have you tried that already?
Finally, if you have a specific issue, you can post using ADN DevHelp so we can investigate it further.
Regards,
Augusto Goncalves
Reply
07/12/2012 at 12:42 PM

---
**内容**: Yvon Bourgouin said in reply to Augusto Goncalves...
Hi Augusto, could you give some tips about doing that in C#.
Thanks
Yvon
Reply
07/13/2012 at 07:53 AM

---
**内容**: Augusto Goncalves said in reply to Yvon Bourgouin...
Hi Yvon,
Not sure if this was replied...but anyway, this is not C# related. Actually you can create a .bat file to open AutoCAD 2013 console and execute .src files. This .src can contain any custom or built-in command.
Below is a sample for the .bat file to process files on a folder
>>>
for %%f IN (c:\SampleDrawings\*.dwg) DO accoreconsole.exe /i "%%f" /s "C:\SampleDrawings\SampleScript.scr" /l en-US
<<<
It starts one AutoCAD console for each drawing on the folder.
Regards,
Augusto Goncalves
Reply
08/16/2012 at 07:49 AM

---
**内容**: anonymous said in reply to Augusto Goncalves...
Hi. Is there no other way to resolve this constant crashes and memory leaks using autocad api?
Reply
04/23/2014 at 08:56 AM

---
**内容**: Augusto Goncalves said in reply to anonymous...
By the way Windows allocate memory, you need to close the application in order to fully restore the memory. That's why the AutoCAD Console is the main alternative here.
Regards,
Augusto Goncalves
Reply
04/25/2014 at 11:52 AM

---
**内容**: Umesh Worlikar said...
The Database class derives from DisposableWrapper, which in turn implements IDisposable. It is caller functions responsibility to call Dispose() immediately after usage of Database. (just before it goes out of scope.)
For C#, cleaner way would be to wrap the database variable within using statement.
using(Database)
{
//read it and do stuff.
}
Reply
08/10/2014 at 10:56 PM

---
**内容**: Augusto Goncalves said in reply to Umesh Worlikar...
Umesh,
This is true, but remember the AutoCAD types are actually defined on C++ level and the .NET class is just a wrapper.
Also, this post describes a more complex scenario, related to how Windows OS allocates memory.
Regards,
Augusto Goncalves
Reply
08/11/2014 at 05:56 AM

---
