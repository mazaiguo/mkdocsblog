---
title: "ADN DevLab, Autodesk HQ, San Rafael, CA"
date: 2012-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Migration
description: "Gopi and I are busy this week at DevLab here in sunny CA! We’ve got 10 developers here (full class) all doing their everyday work, asking questions..."
author: Autodesk
---
# ADN DevLab, Autodesk HQ, San Rafael, CA

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/adn-devlab-autodesk-hq-san-rafael-ca.html

## 文章内容

by Fenton Webb
Gopi and I are busy this week at DevLab here in sunny CA! We’ve got 10 developers here (full class) all doing their everyday work, asking questions as they go.
In case you didn’t know, our ADN DevLab is a class with no set agenda you just turn up and program as you normally would back home – the idea is that when you get stuck or have questions, instead of spending hours (sometimes days) to resolve something, you just casually turn and ask your friendly Autodesk ADN buddy for help. We usually have an answer or some good advice, so it really works well.
As an example, one developer we have here was using StartTransaction() inside of his objectModified() event handler, this is a no no. As soon as I saw it, I told him that doing a StartTransaction() there “would trash the Redo command – you’ll get a ‘there’s nothing to redo’ message at the command line’ issue” to which he replied, “YES! that’s my exact problem, now how do I fix it”. The solution is to use the StartOpenCloseTransaction() instead as that version wraps the Open()/Close() methods directly, and in turn avoids the Undo filer initialization - which ultimately wipes out the Undo/Redo filer when Undo is executed, and, the objectModified() is called while Undo is running – sorry for the mouthful there. I should also mention that the StartOpenCloseTransaction() does solve the initial problem, however, if you subsequently open an object for Write, then that will also wipe the Redo filer so best to open the object first for read, check isUndoing == false, and if it is, then upgradeOpen() to write (there’s no need to write an object when isUndoing == true because, well, the Undo will put it back for you.
Another example, Hyrdatec who are here from New Hampshire and who are avid DevLab attendees, they have a very cool Fire Protection Sprinkler piping application called HydraCAD which has a set of C++ Custom object enablers – I mentioned to them about the new Autodesk Exchange App Store and they asked if they could post their object enablers there as a free app, I said yes, and we promptly built their enabler app (which supports Win32/Win64 for AutoCAD 2012/2013) in 5 minutes flat!
Anyway, here’s a little snapshot of us working hard!

