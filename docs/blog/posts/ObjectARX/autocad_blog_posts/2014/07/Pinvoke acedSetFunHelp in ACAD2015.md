---
title: "Pinvoke acedSetFunHelp in ACAD2015"
date: 2014-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "We have been recieving few queries from our ADN partners regarding setting help message display on F1 click on custom commands that"
author: Autodesk
---
# Pinvoke acedSetFunHelp in ACAD2015

发布日期: 2014-07-01

原始链接: https://adndevblog.typepad.com/autocad/2014/07/pinvoke-acedsetfunhelp-in-acad2015.html

## 文章内容

By Madhukar Moogala
    We have been recieving few queries from our ADN partners regarding setting help message display on F1 click on custom commands that
    The call to the function acedSetFunHelp always passes the value 0 (zero) as the cmd parameter.
     Has the call to the acedSetFunHelp function changed in the 2015 release and is it different between the 32bit and 64bit versions?
Yes, there has been change in the entry points of the function acedSetFunHelp and is different between 32/64 bit machines.
I have already answered this in forum post acedSetFunHelp , as to reach larger audience I planned to blog this with minor additions ,thanks to Alexander Rivilis for bringing up this issue ,used his part of code.
  #define AUTOCAD_NEWER_THAN_2012
#define AUTOCAD_NEWER_THAN_2014
using System;
using System.Reflection;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using cad = Autodesk.AutoCAD.ApplicationServices.Application;
using Ap = Autodesk.AutoCAD.ApplicationServices;
using Db = Autodesk.AutoCAD.DatabaseServices;
using Ed = Autodesk.AutoCAD.EditorInput;
using Rt = Autodesk.AutoCAD.Runtime;
[assembly: Rt.CommandClass(typeof(Help.Commands))]
namespace Help
{
    ///<summary>
    /// Help File
    ///</summary>
    public sealed class Commands
    {
        #region PInvoke
        #if AUTOCAD_NEWER_THAN_2012
        const String fnc_location = "accore.dll";
        #else
        const String fnc_location = "acad.exe";
        #endif
        #if AUTOCAD_NEWER_THAN_2014
        const String x86_Prefix = "_";
        #else
        const String x86_Prefix = "";
        #endif
        #region acedSetFunHelp
        const String acedSetFunHelp_Name = "acedSetFunHelp";
        [DllImport(fnc_location, CharSet = CharSet.Auto,
        CallingConvention = CallingConvention.Cdecl,
        EntryPoint = "acedSetFunHelp")]
        private static extern Int32 acedSetFunHelp_x64(
        String functionName,
        String helpFile,
        String helpTopic,
        Int32 cmd);
        [DllImport(fnc_location, CharSet = CharSet.Auto,
        CallingConvention = CallingConvention.Cdecl,
        EntryPoint = x86_Prefix + "acedSetFunHelp")]
        private static extern Int32 acedSetFunHelp_x86(
                                    String functionName,
                                    String helpFile,
                                    String helpTopic,
                                    Int32 cmd);
        internal static Int32 acedSetFunHelp(
                                    String functionName,
                                    String helpFile,
                                    String helpTopic,
                                    Int32 cmd)
        {
            if (IntPtr.Size == 4)
                return acedSetFunHelp_x86(functionName,
                                          helpFile,
                                          helpTopic,
                                          cmd);
            else
                return acedSetFunHelp_x64(functionName,
                                          helpFile,
                                          helpTopic,
                                          cmd);
        }
        #endregion // acedSetFunHelp
        #endregion // PInvoke
        const String commandGroup = "MyCommand";
        internal const String throughAcedSetFunHelp =         "ThroughAcedSetFunHelp";
        const String helpPageExtension = ".htm";
        /*Place the Chm file where .NET dll is resourced*/
        const String chmFileName = "MyHelp.chm";
        internal static readonly String asm_location =
        Path.GetDirectoryName(Assembly.GetExecutingAssembly()
        .Location);
        // chm-file is in the directory of dll-file.
        internal static readonly String chmFileFullName =
        Path.Combine(asm_location, chmFileName);
        const String f1_msg =
        "\nPress F1 for opening of " +
        "help system.\n";
        ///<summary>
        ///<summary>
        /// Registaration with calling acedSetFunHelp
        ///</summary>
        [Rt.CommandMethod(commandGroup,
                          throughAcedSetFunHelp,
                          Rt.CommandFlags.Session
                          )]
        public void ThroughAcedSetFunHelp_Command()
        {
            Ap.Document doc =
            cad.DocumentManager.MdiActiveDocument;
            if (null == doc)
            {
                return;
            }
            string CmdName = "c:" +
                             throughAcedSetFunHelp.ToUpper();
            acedSetFunHelp(CmdName, chmFileFullName, "", 0);
            doc.Editor.GetPoint(f1_msg);
        }
    }
}

## 评论

**内容**: Alexander Rivlis said...
Hi Madhukar!
This code by Andrey Bushman. I only relayed it. A full discussion and code choices (in Russian) here: http://adn-cis.org/forum/index.php?topic=819.0
Reply
07/24/2014 at 11:36 AM

---
