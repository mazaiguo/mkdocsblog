---
title: "Asking for a password on the command line of AutoCAD using ObjectARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "I have a command line that is asking the user for a password. In this situation I need to display a  for each entered character by the user. How is..."
author: Autodesk
---
# Asking for a password on the command line of AutoCAD using ObjectARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/asking-for-a-password-on-the-command-line-of-autocad-using-objectarx.html

## 文章内容

by Fenton Webb
Issue
I have a command line that is asking the user for a password. In this situation I need to display a * for each entered character by the user. How is it possible to do it?
Solution
It would not help to use acedGetString, as it always echoes the characters as they are typed. If you don't want to use a dialog, you can create your own function in ObjectARX to prompt the user for a password in AutoCAD, yet have the console show only "*" for each character typed, much like password entry in Windows.
The basic idea is to set a Windows Hook which can monitor any keyboard input to a normal call to acedGetString() before AutoCAD gets it. From there you can record what has been typed in your own buffer, and replace the keystroke with a generic "*". When the function is done, you can return your buffer instead of what AutoCAD has actually received (i.e. a string of "****"s).
This example creates the function adskGetPassword() which has the identical signature and return type as acedGetString(), and it can be used interchangeably, however any typed input will appear as '*' in adskGetPassword(). For questions about the arguments, have a look at the ObjectARX online help under acedGetString() for details.
As far as security is concerned, the routine is safe to use except if any applications have set hooks in the chain before this one, or if any application has sub classed the AutoCAD frame window. These applications may be able to monitor the keystrokes before our function is able to change them. If more security is desired, take a look at the Password Dialog available from Microsoft.
Here is the code:
ACHAR*pResult; // a global pointer to the result...
int resultLen; // a global lengh
int crTerminated;// a global flag for cronly
  int adskGetPassword(int cronly,ACHAR* prompt,ACHAR* result)
{
  ACHAR tempResult[256];
  pResult=result;// set our global pointer...
  resultLen=0;// and reset our length.
  int resultVal;// this is what acedGetString returns (ie escape etc)
  crTerminated=cronly;// set our global flag for cronly
    acedRegisterFilterWinMsg(MessageFilter);// Set the Hook.
  resultVal=acedGetString(cronly,prompt,tempResult);// Call GetString...
  acedRemoveFilterWinMsg(MessageFilter);// Remove the Hook.
  result[resultLen]='\0';// Null terminate the result
  return resultVal;
}
  // Here is the callback...it will be called for many types of messages sent to AutoCAD.
BOOL MessageFilter(MSG *pMsg)
{
  if(pMsg->message==WM_CHAR)// a char has been typed...
  {
    int keyCode=pMsg->wParam;
    if(keyCode!=8 && keyCode!=13 && keyCode!=27 && ((keyCode!=32)||crTerminated))
    {
      // keyCode 8 is Backspace
      // Keycode 27 is Escape
      // Keycode 32 is Space (only avoided if cronly is used)
      pMsg->wParam=42;// For Security against subsequent hooks, and display,
      pMsg->lParam=589825;// Set these two to reflect '*' keystroke
      pResult[resultLen]=keyCode;// but keep the real keycode.
      resultLen++;
    }
    if(keyCode==8 && resultLen)
      resultLen--;
  }
  return FALSE;
}

## 评论

**内容**: Thierry Prince said...
Hi Fenton,
Do you test it with AutoCAD 2013 ?
For example with the password "aaaa" :
1. Without dynamic input activated and if the focus is in the command line window, the string shown is "aaaa" and the result stored is "".
2. Without dynamic input activated and if the focus is in the AutoCAD window, the string shown is "*aaa" and the result stored is "a".
3. With dynamic input activated and if the focus is in the command line window, the string shown is "aaaa" and the result stored is "".
4. With dynamic input activated and if the focus is in the AutoCAD window, the string shown is "****" and the result stored is "aaaa".
The only good result is for case 4, when the input is made from the dynamic input tool window.
I think the use of acedRegisterFilterWinMsg function (and also the acedRegisterWatchWinMsg) is incorrect when the command window get the focus (after the first character is typed).
If you find an "easy" workaround, I would be happy to have it, because we use these functions for similary processes.
Cheers.
Thierry
Reply
08/13/2012 at 04:56 AM

---
**内容**: Balaji said in reply to Thierry Prince...
Hi Thierry,
I have replied to a similar query in the forum.
Hope it helps.
http://forums.autodesk.com/t5/Autodesk-ObjectARX/How-to-ask-for-a-password-on-the-command-line-of-AutoCAD-2013/m-p/3649184/highlight/false#M29539
Cheers,
Balaji
Reply
10/13/2012 at 09:40 AM

---
