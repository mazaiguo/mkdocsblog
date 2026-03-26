---
title: "Reacting to the cursor keys properly (without affecting AutoCAD) using .NET?"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "Leading on from this post How to react to the cursor keys properly (without affecting AutoCAD) using ObjectARX? I thought I’d show you guys how to ..."
author: Autodesk
---
# Reacting to the cursor keys properly (without affecting AutoCAD) using .NET?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/reacting-to-the-cursor-keys-properly-without-affecting-autocad-using-net.html

## 文章内容

by Fenton Webb
Leading on from this post How to react to the cursor keys properly (without affecting AutoCAD) using ObjectARX? I thought I’d show you guys how to do the same in .NET, mainly because I had originally done something very similar back in 2006.
So, back when I was using AutoCAD 2007, I got a question from a developer asking if it was possible to call acedRegisterWinFilterMsg() from .NET. The answer was yes of course, but, if I remember correctly, it was only supported using .NET 2.0. The reason was because the PInvoke attribute I mention just below did not exist prior to 2.0, here it is:
[UnmanagedFunctionPointer(CallingConvention.Cdecl)]
I remember back then that it took a little playing around with to get it working, because at that time there wasn’t much documentation on the subject, don’t be put off by the unusual keywords, take note of the syntax – it’ll be useful for you in the future.
Here’s the code, I hope you like it…
// calling acedRegisterFilterWinMsg() and acedRemoveFilterWinMsg
// from .NET by Fenton Webb, DevTech, Autodesk 08/06/2012
// (derived from original example implemented back in 2006)
bool cursDone = false;
[UnmanagedFunctionPointer(CallingConvention.Cdecl)]
public delegate int WindowHookProc(ref System.Windows.Forms.Message msg);
private WindowHookProc callBackFunc = null;
[CommandMethod("curskeys")]
public void curskeys()
{
  // if already hooked
  if (cursDone == true)
    return;
    // get the editor object
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  ed.WriteMessage("\nCursor filtering enabled...");
    callBackFunc = new WindowHookProc(this.WindowsHook);
  if (acedRegisterFilterWinMsg(callBackFunc) == 0)
    ed.WriteMessage("\nCan't register Windows cursor-key msg hook");
  else
    cursDone = true;
}
// Stop using filterCurs() for processing key presses
[CommandMethod("nocurskeys")]
public void nocurskeys()
{
  if (cursDone == true)
  {
    acedRemoveFilterWinMsg(callBackFunc);
    cursDone = false;
  }
}
public enum WndMsg
{
  WM_ACTIVATE = 0x6,
  WM_ACTIVATEAPP = 0x1c,
  WM_AFXFIRST = 0x360,
  WM_AFXLAST = 0x37f,
  WM_APP = 0x8000,
  WM_ASKCBFORMATNAME = 0x30c,
  WM_CANCELJOURNAL = 0x4b,
  WM_CANCELMODE = 0x1f,
  WM_CAPTURECHANGED = 0x215,
  WM_CHANGECBCHAIN = 0x30d,
  WM_CHANGEUISTATE = 0x127,
  WM_CHAR = 0x102,
  WM_CHARTOITEM = 0x2f,
  WM_CHILDACTIVATE = 0x22,
  WM_CLEAR = 0x303,
  WM_CLOSE = 0x10,
  WM_COMMAND = 0x111,
  WM_COMPACTING = 0x41,
  WM_COMPAREITEM = 0x39,
  WM_CONTEXTMENU = 0x7b,
  WM_COPY = 0x301,
  WM_COPYDATA = 0x4a,
  WM_CREATE = 0x1,
  WM_CTLCOLORBTN = 0x135,
  WM_CTLCOLORDLG = 0x136,
  WM_CTLCOLOREDIT = 0x133,
  WM_CTLCOLORLISTBOX = 0x134,
  WM_CTLCOLORMSGBOX = 0x132,
  WM_CTLCOLORSCROLLBAR = 0x137,
  WM_CTLCOLORSTATIC = 0x138,
  WM_CUT = 0x300,
  WM_DEADCHAR = 0x103,
  WM_DELETEITEM = 0x2d,
  WM_DESTROY = 0x2,
  WM_DESTROYCLIPBOARD = 0x307,
  WM_DEVICECHANGE = 0x219,
  WM_DEVMODECHANGE = 0x1b,
  WM_DISPLAYCHANGE = 0x7e,
  WM_DRAWCLIPBOARD = 0x308,
  WM_DRAWITEM = 0x2b,
  WM_DROPFILES = 0x233,
  WM_ENABLE = 0xa,
  WM_ENDSESSION = 0x16,
  WM_ENTERIDLE = 0x121,
  WM_ENTERMENULOOP = 0x211,
  WM_ENTERSIZEMOVE = 0x231,
  WM_ERASEBKGND = 0x14,
  WM_EXITMENULOOP = 0x212,
  WM_EXITSIZEMOVE = 0x232,
  WM_FONTCHANGE = 0x1d,
  WM_GETDLGCODE = 0x87,
  WM_GETFONT = 0x31,
  WM_GETHOTKEY = 0x33,
  WM_GETICON = 0x7f,
  WM_GETMINMAXINFO = 0x24,
  WM_GETOBJECT = 0x3d,
  WM_GETTEXT = 0xd,
  WM_GETTEXTLENGTH = 0xe,
  WM_HANDHELDFIRST = 0x358,
  WM_HANDHELDLAST = 0x35f,
  WM_HELP = 0x53,
  WM_HOTKEY = 0x312,
  WM_HSCROLL = 0x114,
  WM_HSCROLLCLIPBOARD = 0x30e,
  WM_ICONERASEBKGND = 0x27,
  WM_IME_CHAR = 0x286,
  WM_IME_COMPOSITION = 0x10f,
  WM_IME_COMPOSITIONFULL = 0x284,
  WM_IME_CONTROL = 0x283,
  WM_IME_ENDCOMPOSITION = 0x10e,
  WM_IME_KEYDOWN = 0x290,
  WM_IME_KEYLAST = 0x10f,
  WM_IME_KEYUP = 0x291,
  WM_IME_NOTIFY = 0x282,
  WM_IME_REQUEST = 0x288,
  WM_IME_SELECT = 0x285,
  WM_IME_SETCONTEXT = 0x281,
  WM_IME_STARTCOMPOSITION = 0x10d,
  WM_INITDIALOG = 0x110,
  WM_INITMENU = 0x116,
  WM_INITMENUPOPUP = 0x117,
  WM_INPUTLANGCHANGE = 0x51,
  WM_INPUTLANGCHANGEREQUEST = 0x50,
  WM_KEYDOWN = 0x100,
  WM_KEYFIRST = 0x100,
  WM_KEYLAST = 0x108,
  WM_KEYUP = 0x101,
  WM_KILLFOCUS = 0x8,
  WM_LBUTTONDBLCLK = 0x203,
  WM_LBUTTONDOWN = 0x201,
  WM_LBUTTONUP = 0x202,
  WM_MBUTTONDBLCLK = 0x209,
  WM_MBUTTONDOWN = 0x207,
  WM_MBUTTONUP = 0x208,
  WM_MDIACTIVATE = 0x222,
  WM_MDICASCADE = 0x227,
  WM_MDICREATE = 0x220,
  WM_MDIDESTROY = 0x221,
  WM_MDIGETACTIVE = 0x229,
  WM_MDIICONARRANGE = 0x228,
  WM_MDIMAXIMIZE = 0x225,
  WM_MDINEXT = 0x224,
  WM_MDIREFRESHMENU = 0x234,
  WM_MDIRESTORE = 0x223,
  WM_MDISETMENU = 0x230,
  WM_MDITILE = 0x226,
  WM_MEASUREITEM = 0x2c,
  WM_MENUCHAR = 0x120,
  WM_MENUCOMMAND = 0x126,
  WM_MENUDRAG = 0x123,
  WM_MENUGETOBJECT = 0x124,
  WM_MENURBUTTONUP = 0x122,
  WM_MENUSELECT = 0x11f,
  WM_MOUSEACTIVATE = 0x21,
  WM_MOUSEFIRST = 0x200,
  WM_MOUSEHOVER = 0x2a1,
  WM_MOUSELAST = 0x20d,
  WM_MOUSELEAVE = 0x2a3,
  WM_MOUSEMOVE = 0x200,
  WM_MOUSEWHEEL = 0x20a,
  WM_MOUSEHWHEEL = 0x20e,
  WM_MOVE = 0x3,
  WM_MOVING = 0x216,
  WM_NCACTIVATE = 0x86,
  WM_NCCALCSIZE = 0x83,
  WM_NCCREATE = 0x81,
  WM_NCDESTROY = 0x82,
  WM_NCHITTEST = 0x84,
  WM_NCLBUTTONDBLCLK = 0xa3,
  WM_NCLBUTTONDOWN = 0xa1,
  WM_NCLBUTTONUP = 0xa2,
  WM_NCMBUTTONDBLCLK = 0xa9,
  WM_NCMBUTTONDOWN = 0xa7,
  WM_NCMBUTTONUP = 0xa8,
  WM_NCMOUSEMOVE = 0xa0,
  WM_NCPAINT = 0x85,
  WM_NCRBUTTONDBLCLK = 0xa6,
  WM_NCRBUTTONDOWN = 0xa4,
  WM_NCRBUTTONUP = 0xa5,
  WM_NEXTDLGCTL = 0x28,
  WM_NEXTMENU = 0x213,
  WM_NOTIFY = 0x4e,
  WM_NOTIFYFORMAT = 0x55,
  WM_NULL = 0x0,
  WM_PAINT = 0xf,
  WM_PAINTCLIPBOARD = 0x309,
  WM_PAINTICON = 0x26,
  WM_PALETTECHANGED = 0x311,
  WM_PALETTEISCHANGING = 0x310,
  WM_PARENTNOTIFY = 0x210,
  WM_PASTE = 0x302,
  WM_PENWINFIRST = 0x380,
  WM_PENWINLAST = 0x38f,
  WM_POWER = 0x48,
  WM_POWERBROADCAST = 0x218,
  WM_PRINT = 0x317,
  WM_PRINTCLIENT = 0x318,
  WM_QUERYDRAGICON = 0x37,
  WM_QUERYENDSESSION = 0x11,
  WM_QUERYNEWPALETTE = 0x30f,
  WM_QUERYOPEN = 0x13,
  WM_QUEUESYNC = 0x23,
  WM_QUIT = 0x12,
  WM_RBUTTONDBLCLK = 0x206,
  WM_RBUTTONDOWN = 0x204,
  WM_RBUTTONUP = 0x205,
  WM_RENDERALLFORMATS = 0x306,
  WM_RENDERFORMAT = 0x305,
  WM_SETCURSOR = 0x20,
  WM_SETFOCUS = 0x7,
  WM_SETFONT = 0x30,
  WM_SETHOTKEY = 0x32,
  WM_SETICON = 0x80,
  WM_SETREDRAW = 0xb,
  WM_SETTEXT = 0xc,
  WM_SETTINGCHANGE = 0x1a,
  WM_SHOWWINDOW = 0x18,
  WM_SIZE = 0x5,
  WM_SIZECLIPBOARD = 0x30b,
  WM_SIZING = 0x214,
  WM_SPOOLERSTATUS = 0x2a,
  WM_STYLECHANGED = 0x7d,
  WM_STYLECHANGING = 0x7c,
  WM_SYNCPAINT = 0x88,
  WM_SYSCHAR = 0x106,
  WM_SYSCOLORCHANGE = 0x15,
  WM_SYSCOMMAND = 0x112,
  WM_SYSDEADCHAR = 0x107,
  WM_SYSKEYDOWN = 0x104,
  WM_SYSKEYUP = 0x105,
  WM_TCARD = 0x52,
  WM_TIMECHANGE = 0x1e,
  WM_TIMER = 0x113,
  WM_UNDO = 0x304,
  WM_UNINITMENUPOPUP = 0x125,
  WM_USER = 0x400,
  WM_USERCHANGED = 0x54,
  WM_VKEYTOITEM = 0x2e,
  WM_VSCROLL = 0x115,
  WM_VSCROLLCLIPBOARD = 0x30a,
  WM_WINDOWPOSCHANGED = 0x47,
  WM_WINDOWPOSCHANGING = 0x46,
  WM_WININICHANGE = 0x1a,
  WM_XBUTTONDBLCLK = 0x20d,
  WM_XBUTTONDOWN = 0x20b,
  WM_XBUTTONUP = 0x20c
}
  [DllImport("accore.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.Cdecl, EntryPoint = "?acedRegisterFilterWinMsg@@YAHQ6AHPEAUtagMSG@@@Z@Z")]
private static extern int acedRegisterFilterWinMsg(WindowHookProc callBackFunc);
[DllImport("accore.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.Cdecl, EntryPoint = "?acedRemoveFilterWinMsg@@YAHQ6AHPEAUtagMSG@@@Z@Z")]
private static extern int acedRemoveFilterWinMsg(WindowHookProc callBackFunc);
// hook message filter callback function
private int WindowsHook(ref System.Windows.Forms.Message msg)
{
  // if we get a left button double click message
  if (msg.Msg == (int)WndMsg.WM_LBUTTONDBLCLK)
  {
  }
  // check to see if we are getting a WM_PAINT message
  if (msg.Msg == (int)WndMsg.WM_PAINT)
  {
  }
  // if we are getting a keydown
  if (msg.Msg == (int)WndMsg.WM_KEYDOWN && (int)msg.WParam >= 37 && (int)msg.WParam <= 40)
  {
    // get the editor object
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    switch ((int)msg.WParam)
    {
      case 37: // left
        ed.WriteMessage("\nLeft");
        break;
        case 38: // up
        ed.WriteMessage("\nUp");
        break;
        case 39: // right
        ed.WriteMessage("\nRight");
        break;
        case 40: // down
        ed.WriteMessage("\nDown");
        break;
      }
      return 1; // filter message
  }
    return 0;
}

## 评论

**内容**: Kerry Brown said...

Fenton,
Is there any public documentation for acedRegisterWinFilterMsg()
Regards
Kerry
Reply
08/28/2012 at 10:19 PM

---
**内容**: Owen Wengerd said in reply to Kerry Brown...
The correct name is acedRegisterFilterWinMsg.
Reply
08/29/2012 at 12:22 PM

---
**内容**: Kerry Brown said in reply to Owen Wengerd...
Thanks Owen,
DUH! me.
Mum used to say it was because my fingers worked faster than my brain.
Reply
08/29/2012 at 12:56 PM

---
**内容**: Fenton Webb said...
Hey Kerry
simply check out the arxref.chm in the ObjectARX SDK. That's where you will find detailed documentation for ObjectARX AND the corresponding .NET functions.
Reply
08/29/2012 at 10:57 AM

---
**内容**: Kerry Brown said...

[quote - J.R.R. Tolkien, The Hobbit, Ch. 4]
There is nothing like looking, if you want to find something.
[/quote]
.. as Owen pointed out, my dyslexia caught up with me :(
Thanks
Reply
08/29/2012 at 01:03 PM

---
**内容**: Kerry Brown said...
Ahhhhhh ... caught by cut and paste
[quote]
So, back when I was using AutoCAD 2007, I got a question from a developer asking if it was possible to call acedRegisterWinFilterMsg() from .NET.
[/quote]
... but I still feel silly :-D
Reply
08/29/2012 at 01:28 PM

---
**内容**: Fenton Webb said...
I think now we will all never forget this function name ever again! :-)
Reply
08/29/2012 at 01:32 PM

---
**内容**: Peter said...
Hi Fenton,
I used your code to show a dialog box if an object is doubleclicked in the drawing. Everything works fine but if there is a button at the point the user doubleclicked, the button respectively the dialogbox gets a click event. Have you an idea to suppress this?
Regards,
Peter
Reply
11/27/2012 at 01:19 AM

---
**内容**: Peter said...
Hi Fenton,
I did some more research about the problem and found the solution. Unfortunately I used the MouseUp event instead the Click event. After change of the event type, erverthing works fine! Nevertheless, thank you for the helpful code sample!
Regards,
Peter
Reply
12/07/2012 at 01:59 AM

---
**内容**: ASP.Net Development uk said...
I truly enjoy looking at on this web site , it has got fantastic blog posts.
Reply
01/08/2013 at 05:50 AM

---
