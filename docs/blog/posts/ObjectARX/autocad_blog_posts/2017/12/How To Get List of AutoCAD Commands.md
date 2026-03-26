---
title: "How To Get List of AutoCAD Commands"
date: 2017-12-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
description: "I have received a query from customer to retrieve list of AutoCAD Commands loaded in to AutoCAD Domain."
author: Autodesk
---
# How To Get List of AutoCAD Commands

发布日期: 2017-12-01

原始链接: https://adndevblog.typepad.com/autocad/2017/12/how-to-get-list-of-autocad-commands.html

## 文章内容

By Madhukar Moogala
I have received a query from customer to retrieve list of AutoCAD Commands loaded in to AutoCAD Domain.
I don't think there is a single API which can fetch you list of AutoCAD BuiltIn Commands.
here are few attempts:
You can use _.ARX with Commands flag to retrieve the list of commands of all registered  arx programs with AutoCAD.
Best way to do this, create a arx.scr script file with following contents
_.ARX
_Commands
*
or,
In CLI, use
D:\Program Files\Autodesk\AutoCAD 2017>accoreconsole /s arx.scr > D:\Temp\cmds.txt
PGP files stores alias keys for all ACAD commands irrespective of technology used to create them.
           You can find other PGP file like Synonyms in this folder
           C:\Users\<user>\AppData\Roaming\Autodesk\AutoCAD 20xx\Rxx.x\enu\Support
            or
          On the command line in all versions of AutoCAD except AutoCAD LT, type the following:
(findfile "acad.pgp")
AcEdCommandIterator is not exposed in .NET, but you can use following code in C++ and
I would like to emphasis that commands of only loaded modules can retrieved, for example using above workflow CAMERA command can't be found, because AcCamera.arx modules has not been loaded into ACAD domain, hence it is not yet registered with AcEdCommandStack.
void cmdExtract()
{
AcEdCommandIterator* iter = acedRegCmds->iterator();
if (iter == NULL)
{
return;
}
int n = 0;
FILE *fptr;
fopen_s(&fptr,"D:\\Temp\\Commands.txt","a");
for (;!iter->done(); iter->next())
{
const AcEdCommand* pp = iter->command();
fwprintf(fptr,_T("%s\n"), pp->globalName());
n++;
}
fclose(fptr);
}
I would like to emphasis that commands of only loaded modules can retrieved, for example using above workflow CAMERA command can't be found, because AcCamera.arx modules has not been loaded into ACAD domain, hence it is not yet registered with AcEdCommandStack.
For .NET, Pinvoke required little bit work.
C++ code
//We need size to allocate memory
extern "C" __declspec(dllexport) int getSizeOfCmds()
{
 AcEdCommandIterator* iter = acedRegCmds->iterator();
 if (iter == NULL)
 {
  return -1;
 }
 int size = 0;
 for (; !iter->done(); iter->next())
 {
  const AcEdCommand* pp = iter->command();
  size++;
 }
 return size;

}
/*
Using BSTR allows us to allocate the strings in the native code,
and have them deallocated in the managed code. That's because BSTR is allocated on the shared COM heap,
and the p / invoke marshaller understands them*/
extern "C" __declspec(dllexport) Acad::ErrorStatus cmdExtract(BSTR* comStringCmdNames)
{
 
 AcEdCommandIterator* iter = acedRegCmds->iterator();
 if (iter == NULL)
 {
  return Acad::eCreateFailed;
 }
 int i = 0;
 for (;!iter->done();iter->next())
 {
  const AcEdCommand* pp = iter->command();
  //the beauty is here, sometimes COM is nice 
  //Allocate here and DeAllocate in C#
  comStringCmdNames[i]  = ::SysAllocString(pp->globalName());
     i++;
 }

 return Acad::eOk;
}
.NET code
  public class MyCommands
    {
        [DllImport("D:\\Arxprojects\\ListOfCommands\\extractCommands_ARX\\x64\\Debug\\extractCommands.arx",
            CallingConvention = CallingConvention.Cdecl,
            CharSet = CharSet.Unicode,
            EntryPoint = "cmdExtract")]

        private static extern ErrorStatus cmdExtract([Out] IntPtr[] cmdNames);

        [DllImport("D:\\Arxprojects\\ListOfCommands\\extractCommands_ARX\\x64\\Debug\\extractCommands.arx",
          CallingConvention = CallingConvention.Cdecl,
          CharSet = CharSet.Unicode,
          EntryPoint = "getSizeOfCmds")]

        private static extern int getSizeOfCmds();


        [CommandMethod("ExtCmd")]
        public static void cmd()
        {
            int count = getSizeOfCmds();
            IntPtr[] cmdNames = new IntPtr[count];
            ErrorStatus es = cmdExtract(cmdNames);
            string[] names = new string[count];
            for (int i = 0; i < count; i++)
            {
                names[i] = Marshal.PtrToStringBSTR(cmdNames[i]);
                Marshal.FreeBSTR(cmdNames[i]);
            }
        }
    }
 
Full source code is available here

## 评论

**内容**: Pedro Aljinta said...
Hi. Why P/Invoke?
What's wrong with mixed-mode C++/CLI for this?
Reply
03/04/2018 at 09:53 PM

---
**内容**: Fernando said...
It is so hard this way, but actually i have been looking again and again and
i realized there is not other way, neither easier nor harder.
Thanks anyway.
Reply
12/08/2018 at 01:57 AM

---
**内容**: Ben Epp said...
You can go to CUI and there's a full command list, also with the option of listing controls in addition.
Reply
08/15/2019 at 08:29 AM

---
**内容**: Deepika said...
TrueCAD http://truecad.com/download-truecad-intellicad-software.php" target="_blank" rel="nofollow">intellicad Software.One of the best AutoCAD alternative cad software at affordable price.
Reply
05/06/2021 at 11:12 PM

---
**内容**: Deepika said...
Use TrueCAD-intellicad Software.One of the best AutoCAD alternative cad software at affordable price. here is reference link "https://http://truecad.com/download-truecad-intellicad-software.php"
Reply
05/06/2021 at 11:12 PM

---
