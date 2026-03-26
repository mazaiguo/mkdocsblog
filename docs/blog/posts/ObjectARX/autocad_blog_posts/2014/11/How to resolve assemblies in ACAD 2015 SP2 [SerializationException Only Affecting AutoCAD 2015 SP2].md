---
title: "How to resolve assemblies in ACAD 2015 SP2 [SerializationException Only Affecting AutoCAD 2015 SP2]"
date: 2014-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Plugin
description: "With ACAD 2015 SP2 , application no longer resolves assemblies that is if an application is using any dependent DLL and are not located in host app..."
author: Autodesk
---
# How to resolve assemblies in ACAD 2015 SP2 [SerializationException Only Affecting AutoCAD 2015 SP2]

发布日期: 2014-11-01

原始链接: https://adndevblog.typepad.com/autocad/2014/11/how-to-resolve-assemblies-in-acad-2015-sp2-serializationexception-only-affecting-autocad-2015-sp2.html

## 文章内容

By Madhukar Moogala
With ACAD 2015 SP2 , application no longer resolves assemblies that is if an application is using any dependent DLL and are not located in host application directory ,the plugin application may crash as it is failed to load those dlls
I came to know from my engineering colleague Art, recently he has responded a query on similar issue on forum Serialization Exception
This blog intention is to target larger audience.
Imports System
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.Geometry
Imports Autodesk.AutoCAD.EditorInput
'dependent assembly
Imports ThreadSafe
Imports System.Reflection
  ' This line is not mandatory, but improves loading performances
<Assembly: CommandClass(GetType(TestVB15.MyCommands))>
Namespace TestVB15
  Public Class MyCommands  <CommandMethod("MyGroup", "MyCommand", "MyCommandLocal", CommandFlags.Modal)> _
        Public Sub MyCommand()
  AddHandler AppDomain.CurrentDomain.AssemblyResolve, _
AddressOf OnAssemblyResolve
  'TestObject is class from custom made ThreadSafe dll namespace
Dim TstObj As New TestObject
Dim TstObjBts As Byte() = TstObj.ToBytes
Dim TstObj2 As TestObject = _
ThreadSafeDataClass.FromBytes(Of TestObject)(TstObjBts)
Dim TstObjs As New TestObjects
TstObjs.Add(TstObj)
TstObjs.Add(TstObj2)
Dim TstObjsBts As Byte() = TstObjs.ToBytes
Dim TstObjs2 As TestObjects =
ThreadSafeDataClass.FromBytes(Of TestObjects)(TstObjsBts)
TstObjs2.Add(New TestObject)
End Sub
       Private Shared Function OnAssemblyResolve(
sender As Object, args As ResolveEventArgs) As Assembly
 Dim assembly As Assembly = Nothing
 Dim assems As [Assembly]() =_ AppDomain.CurrentDomain.GetAssemblies()
Dim shortName As String = _
args.Name.Split(New [Char]() {","}).GetValue(0)
'ThreasSafe dependent Assembly
Dim threadSafe As String = "ThreadSafe"
   'check that the assembly being asked for is one of ours and if it is not, then return nothing
If shortName <> threadSafe Then
 Return assembly
End If
  For Each assem In assems
If assem.GetName.Name = shortName Then
Return assem
End If
Next assem
 'if assembly is not loaded ,we 'll explictly load this may\may not be required
Dim an = New AssemblyName(args.Name)
If an.Name <> args.Name Then
assembly = DirectCast(sender, AppDomain).Load(an.Name)
End If
Return assembly
End Function
End Class
End Namespace

