---
title: "Migration After Fiber is Removed in AutoCAD 2015"
date: 2014-04-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - Migration
description: "There’s not that much work needed to port your apps to AutoCAD 2015(Longbow), unless you are using acedCommand or acedCmd."
author: Autodesk
---
# Migration After Fiber is Removed in AutoCAD 2015

发布日期: 2014-04-01

原始链接: https://adndevblog.typepad.com/autocad/2014/04/migration-after-fiber-is-removed-in-autocad-2015.html

## 文章内容

By Xiaodong Liang
There’s not that much work needed to port your apps to AutoCAD 2015(Longbow), unless you are using acedCommand or acedCmd.
The following is extracted from our DevDays PPT. If you feel tedious on my repeating the PPT, I’d recommend with the article written by our Blog Master Kean Walmsley : AutoCAD 2015: calling commands, or the video on the migration, or the demo samples codes which is availble at GitHub.
  For this release, we’ve re-architected AutoCAD to completely strip out the use of Fibers and Fiber switching. Fibers are an old technology used in Windows that Microsoft stopped supporting several years ago. AutoCAD made heavy use of fibers and they are what allowed users to switch easily between drawings without interrupting commands. You’ve probably all seen this in action in old versions of AutoCAD – start a LINE command in one drawing, switch to another and draw a CIRCLE, then switch back to the first drawing and the LINE command is still active.
But using fibers was causing a lot of problems for us that we were spending more and more effort working around. For example, the .NET Framework has never supported Fiber Switching, and this is why when you switched documents in AutoCAD when debugging a .NET application, you’d often find that Visual Studio would fail to stop at a breakpoint– or it did break, but couldn’t display your code. That was Visual Studio getting confused by AutoCAD switching Fibers. You won’t experience that problem in Longbow now that we’ve removed Fibers. It also allows us to expose more of the ObjectARX SDK to .NET – the most exciting of which is that we now have a .NET version of acedCommand ((command) in LISP). That wasn’t possible before due to the problems caused by Fibers.
Migration in ObjectARX
That means ObjectARX has more significant migration requirements. There are two migration areas of concern: the MDI API and use of acedCommand/acedCmd. Then you’ll have to make changes. How big a change depends on how you’re using it.
If you’re passing a complete set of command tokens to the AutoCAD commandline, then all you have to do is add an ‘S’ to the end of acedCommand or acedCmd. S stands for subroutine. This is when you’re sending an entire command, and not pausing for user input.
If you’re sending a PAUSE, or if you’re sending an incomplete set of command tokens (for example starting a line command and leaving it for the user to finish) then you have a lot more work to do. In this situation, you’ll be using acedCommandC – the coroutine version of the command – and you’ll now have to pass a pointer to a callback function as a command parameter. It’s a lot more complicated – so much so that you might even consider migrating your code that needs this to .NET instead.
Here’s an example of the most basic acedCommand usage – its also the most popular use case – where we’re invoking a complete command in a single call to acedCommand. All you have to do here is change acedCommand to acedCommandS.
void foo(void)
{
         acedCommandS(RTSTR,
_T("_Line"),
RTSTR,
_T("0,0"),
 RTSTR,
 _T("111,111"),
RTSTR, _T(""),
RTNONE);
         acutPrintf(_T("\nFinished LINE command -  \
                 control returned to addin\n"));
}
  But a lot of people use acedCommand like this. Starting a command and then prompting for user input until the command ends. In this case we’re starting the LINE command and issuing PAUSEs to allow the user to keep drawing additional line segments. When we migrate this code for Longbow, we have to use acedCommandC, because acedCommandS doesn’t support partial command token stacks or PAUSEs.
  void foo(void){
         //Invoke partial command and leave command active.
         acedCommandC(RTSTR,
                   _T("_Line"),
                   RTSTR,
                    _T("0,0"),
                    RTSTR,
                   _T("111,111"),
                     RTNONE);
     while(isLineActive())
                  acedCommandC(RTSTR,
                        PAUSE,
                         RTNONE);
     acutPrintf(_T("\nFinished LINE command -  \
                 control returned to addin\n"));
}
The migrated code will look something like this. We’ve defined a callback function, which we pass to acedCommandC. Now when AutoCAD is ready to pass control from the user back to you, it will do so by calling the callback function you provided. In this example, the callback function keeps passing itself as a callback until the command ends. If the user cancels the command you invoked using acedCommand, then AutoCAD will also cancel your command that called it. Otherwise, control is handed back to your code when the command invoked by acedCommand ends.
void foo(void){
         //Invoke partial command and leave command active.
         acedCommandC(&myCallbackFn,
                   NULL, RTSTR,
                   _T("_Line"),
                   RTSTR,
 _T("0,0"),
                   RTSTR,
_T("111,111"),
RTNONE);
           //Control is passed to myCallbackFn1 from AutoCAD
}

//Your callback function
int myCallbackFn(void * pData){
         int nReturn = RTNONE;
         //Keep command active until user ends it.
      if (isLineActive())
                  nReturn = acedCommandC(&myCallbackFn,
NULL, RTSTR,
PAUSE, RTNONE);
         else
         {
         //This is never reached if the user cancels the command –
// that cancels your command as well.It is reached if command is ended
//(e.g. by hitting ENTER)    
   acutPrintf(_T("\nFinished LINE command -  \
              control returned to addin\n"));
         }
   return nReturn;
}
  Migration in .NET
I would say the most exciting new API in Longbow is the introduction of .NET versions of acedCommand ((command) in LISP). This hasn’t been possible before because of AutoCAD’s use of Fibers – and because the .NET Framework doesn’t support Fibers. So these new APIs – synchronous and asynchronous versions of acedCommand – are now possible for the first time.
acedCommand is probably the most powerful API in ObjectARX. It allows you to embed entire AutoCAD commands within your own commands; and even to invoke partial commands, and then programmatically respond to how the user interacts with those commands. This saves ObjectARX and LISP developers a huge amount of work where otherwise they’d have to reproduce all the native command behavior in their own code – and now .NET developers get the same benefit.
The synchronous version of Command is Editor.Command, the equivalent of the subroutine version of acedCommand. This is how you invoke a complete command from your code. As you can see, the code is very similar to the ObjectARX version – you pass a full set of command tokens to the AutoCAD commandline (the editor), AutoCAD completes the command and immediately returns control back to your code.
//simple use of Editor.Command
//most popular case - invoke a whole command with no user interaction
[CommandMethod(“MyCommand")]
publicstaticvoid MyMethod()
{
    Editor ed =
Application.DocumentManager.MdiActiveDocument.Editor;
ed.Command(newObject[] {
"_.LINE", "0,0,0", "10,10,0", "" });
  }
There is also the asynchronous version of Command Editor.CommandAsync. This is the equivalent of the coroutine version of acedCommand. You’ll recall that acedCommandC required you to pass in a reference to a callback function. The .NET version is a little simpler. Because we’re using .NET Framework 4.5, we can make use of the async and await keywords to greatly simplify our asyncronous code. We mark our .NET commandmethod with the async keyword, and we can then use the await keyword inside that method. The await keyword tells AutoCAD where in your code to return control to after it has finished gathering user input. In this example, we’re simply starting the circle comamnd, using a PAUSE to let the user specify the circle center, and then specifying the circle radius in our code.
  //Invoke a partial command with user interaction
[CommandMethod("DotNetType2")]
publicstaticasyncvoid DotNetType2()
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    //create a circle of radius 2.0 at chosen location.
    await ed.CommandAsync("_.CIRCLE");
    //wait for user input
    await ed.CommandAsync(Editor.PauseToken);
    //provide radius input
    await ed.CommandAsync(2.0);
}

## 评论

**内容**: fixo said...
Could not rest in A2015, just interestingly would be this work in there:
Autodesk.AutoCAD.Internal.Utils.CancelAndRunCmds("_line 0,0,0 10,10,0 " );
Reply
04/18/2014 at 01:37 PM

---
**内容**: Gilles Chanteau said...
Hi,
I noticed that calling the LISP function command (or vl-cmdf) within a function passed as argument to mapcar (either lambda or defun) failed with AutoCAD 2015.
Using command-s instead seems to fix this issue.
Reply
04/27/2014 at 10:28 AM

---
**内容**: Moacir said...
I'm having trouble migrating this command to arx 2015
acedCommand to acedCommandS or acedCommandC, please help-me:

static int ads_mycommad(void)
{
struct resbuf *rb = acedGetArgs () ;
int osmodo;
ACHAR auxt[30];
struct resbuf rb1;

acedGetVar(_T("OSMODE"), &rb1);
osmodo = rb1.resval.rint;
rb1.resval.rint = 0;
acedSetVar(_T("OSMODE"), &rb1);

while (rb != NULL) {
if(rb->restype == RTREAL) {
acdbRToS(rb->resval.rreal,2,8,auxt);
acedCommand(RTSTR, auxt, RTNONE);
}
if(rb->restype == RTPOINT) acedCommand(rb->restype, rb->resval.rpoint, RTNONE);
if(rb->restype == RTSHORT) {
acdbRToS((ads_real)rb->resval.rint,2,0,auxt);
acedCommand(RTSTR, auxt, RTNONE);
}
if(rb->restype == RTANG) {
acdbRToS(rb->resval.rreal,2,8,auxt);
acedCommand(RTSTR, auxt, RTNONE);
}
if(rb->restype == RTSTR) acedCommand(rb->restype, rb->resval.rstring, RTNONE);
if(rb->restype == RTENAME) acedCommand(rb->restype, rb->resval.rlname, RTNONE);
if(rb->restype == RTPICKS) acedCommand(rb->restype, rb->resval.rlname, RTNONE);
if(rb->restype == RTORINT) {
acdbRToS(rb->resval.rreal,2,8,auxt);
acedCommand(RTSTR, auxt, RTNONE);
}
if(rb->restype == RT3DPOINT) acedCommand(rb->restype, rb->resval.rpoint, RTNONE);
if(rb->restype == RTLONG) {
acdbRToS(rb->resval.rlong,2,0,auxt);
acedCommand(RTSTR, auxt, RTNONE);
}
rb = rb->rbnext;
}
rb1.resval.rint = osmodo;
acedSetVar(_T("OSMODE"), &rb1);
if ( rb != NULL )
acutRelRb (rb) ;

return (RSRSLT) ;
}
Reply
07/10/2014 at 12:04 PM

---
**内容**: Iacopo Vettori said in reply to Moacir...
Because your code does not use the PAUSE token, you may build a rb chain and pass it as the argument of a single acedCmdS() call. Also, you don't need to translate double in string, if you specify RTREAL instead of RTSTR as type.
Reply
09/04/2014 at 10:01 AM

---
**内容**: Joao Batista said...
Anything equivalent for A_2017???
Reply
06/05/2016 at 01:19 PM

---
**内容**: xiaodong liang said in reply to Joao Batista...
hi Joao,
if you are migrating from old release before 2015 to 2017, the process is same to what is mentioned in this blog
Reply
06/06/2016 at 08:55 AM

---
**内容**: Jason Huffine said...
I hate to be late to this party, but does this mean that AutoCAD is now truly multi-threaded? Or is there something else in place of fibers? If the latter, then are there any implications worth noting?
Reply
09/21/2016 at 05:03 AM

---
