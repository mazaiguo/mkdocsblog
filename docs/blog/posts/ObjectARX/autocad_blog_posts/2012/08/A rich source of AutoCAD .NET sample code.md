---
title: "A rich source of AutoCAD .NET sample code"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C#
  - Layer
description: "One of the top requests whenever we survey programmers on their needs is “more sample code”. And I agree this is important – its what I want too wh..."
author: Autodesk
---
# A rich source of AutoCAD .NET sample code

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/a-rich-source-of-autocad-net-sample-code.html

## 文章内容

By Stephen Preston
One of the top requests whenever we survey programmers on their needs is “more sample code”. And I agree this is important – its what I want too when I’m learning an API. One oft overlooked source of sample code is AutoCAD itself. We don’t obfuscate our .NET code, and so the AutoCAD components written in .NET (mostly the UI components) provide good usage and (hopefully ) also best practice examples of how to use the various APIs we expose. This is one of the advantages of ‘eating your own dog food’ – another advantage is obviously that it provides additional ‘on the job’ testing for the APIs. To access this sample code, you just need a .NET decompiler, like RedGate Reflector. Simply open the DLL you think might be a .NET assembly and let Reflector do its thing. In this example, I’ve opened the AutoCAD 2012 AcLayer.dll assembly:
Expanding the assembly allows you to drill down into the namespaces and classes it contains:
In this case, I’m looking at the AutoCAD Commands defined by the assembly:
I can drill down into the implementation of each command:
I can even view the code in different .NET languages. The above image is C#, now I’ve changed to VB.NET:
The MSIL doesn’t include comments, of course, so you’re on your own working out exactly what the code is doing.  As an additional aid, Kean has already demonstrated on his blog  how to use Reflector Pro to debug into the AutoCAD .NET API layer.

## 评论

**内容**: PDOTeam said...
Don't forget about dotPeek:
http://www.jetbrains.com/decompiler/
Also, I believe the Plant 3D .net modules are obfuscated.
Reply
08/14/2012 at 04:06 PM

---
**内容**: Madhukar Moogala said...
Thanks for adding the JetBrains link.
I should also have said in the post that I'm not recommending Reflector over any alternatives - I just happen to have a license for it (thanks for that Kean :-)).
Reply
08/14/2012 at 05:22 PM

---
**内容**: JeffH said...
Hey Stephen,
I have not tried them in a while but dotPeek, JustDecompile, etc.. and other free decompilers would throw errors and would not be able to see anything.
ILSpy which is FREE does just a good as reflector, and have recieved no errors. I have reflector and it is better at navigating a bit but definitely would not of paid for it if I knew of ILSpy earlier
http://wiki.sharpdevelop.net/ILSpy.ashx
How I found out.
http://www.theswamp.org/index.php?topic=41354.msg464710#msg464710
Reply
08/14/2012 at 05:59 PM

---
**内容**: Khoa Ho said...
Hi Stephen,
I tried to use dotPeek, JustDecompile and ILSpy to decompile acmgd.dll and acdbmgd.dll. However, none of them can see exactly the implementation of class "Module", which is the core of all unmanaged code. So I don't know if those assembly files are partial obfuscated or not. How can I see the full implementation? Thank you.
Reply
08/15/2012 at 07:41 AM

---
**内容**: Madhukar Moogala said...
Acmgd, acdmgd and accoremgd are simple (generally quite shallow) .NET wrappers on top of our unmanaged C++ ObjectARX API, so a .NET decompiler isn't going to let you drill down into core (unmanaged) AutoCAD implementation. I deliberately didn't refer to those assemblies in the post because (for usage examples) the assemblies that consume the .NET API are more interesting than these assemblies that define the APIs by wrapping the C++. (With Reflector, at least), you can get as far as seeing which ObjectARX API the .NET API is P/Invoking. But I'm not going to go any further down that path.
If you are looking at those three DLLs, you'll find that this is a case where looking at the versions in the AutoCAD installation tells you more than the 'liposuctioned' versions in the ObjectARX SDK.
Reply
08/15/2012 at 09:02 AM

---
**内容**: Khoa Ho said...
Thank you for your reply. The decompilers do not show the DllImport file (acad.exe, acdbxx.dll...) and EntryPoint, so we have to use other tools to find them out. It would be better to view all of those values on the decompiler.
I chose Autodesk.AutoCAD.DatabaseServices.Database.ReadDwgFile() for my test, see the decompiled code:
public unsafe void ReadDwgFile(IntPtr drawingFile, [MarshalAs(UnmanagedType.U1)] bool allowCPConversion, string password)
{
byte* ptr = password;
if (ptr != null)
{
ptr = (ulong)RuntimeHelpers.OffsetToStringData + ptr;
}
Char modopt(System.Runtime.CompilerServices.IsConst)& char modopt(System.Runtime.CompilerServices.IsConst)& = ptr;
Acad.ErrorStatus errorStatus = (Acad.ErrorStatus).AcDbDatabase.readDwgFile(this.GetImpObj(), (AcDwgFileHandle*)drawingFile.ToPointer(), allowCPConversion, char modopt(System.Runtime.CompilerServices.IsConst)&);
if (errorStatus != (Acad.ErrorStatus)0)
{
throw new Exception((ErrorStatus)errorStatus);
}
}
If I go futher to the wrapper of unmanaged code: .AcDbDatabase.readDwgFile(), see the following results from three compilers:
ILSpy:
[SuppressUnmanagedCodeSecurity]
[DllImport("", CallingConvention = CallingConvention.Cdecl, SetLastError = true)]
[MethodImpl(MethodImplOptions.Unmanaged)]
public unsafe static extern Acad.ErrorStatus readDwgFile(AcDbDatabase*, AcDwgFileHandle*, [MarshalAs(UnmanagedType.U1)] bool, char*);
dotPeek:
[SuppressUnmanagedCodeSecurity]
[DllImport("", EntryPoint = "", CallingConvention = CallingConvention.Cdecl, SetLastError = true)]
[MethodImpl(MethodImplOptions.Unmanaged, MethodCodeType = MethodCodeType.Native)]
public static Acad.ErrorStatus AcDbDatabase\u002EreadDwgFile([In] AcDbDatabase* obj0, [In] char* obj1, [In] int obj2, [MarshalAs(UnmanagedType.U1)] bool _param4, [In] char* obj4)
{
// ISSUE: unable to decompile the method.
}
JustDecompile:
[DllImport("", CharSet=CharSet.None)]
[SuppressUnmanagedCodeSecurity]
public static extern unsafe ErrorStatus modopt(System.Runtime.CompilerServices.CallConvCdecl) AcDbDatabase.readDwgFile(AcDbDatabase* modopt(System.Runtime.CompilerServices.IsConst) modopt(System.Runtime.CompilerServices.IsConst) , Char modopt(System.Runtime.CompilerServices.IsConst)* , Int32 modopt(System.Runtime.CompilerServices.IsConst) , bool , Char modopt(System.Runtime.CompilerServices.IsConst)* );
I see ILSpy has the best readable code. My RedGate Reflector was expired so I did not test it. Anyway, it is so fun to play with the decompiler. Thanks for your post.
Reply
08/15/2012 at 04:50 PM

---
**内容**: BJHuffine said...
I used to use Reflector myself until they began charging for their product. Then I found out about Telerik's JustDecompile and it's supposed to be free forever. http://www.telerik.com/products/decompiler.aspx
Reply
08/16/2012 at 11:10 AM

---
**内容**: Madhukar Moogala said in reply to BJHuffine...
Nice! This is turning into a "what's the best decompiler" conversation. Really useful info.
Reply
08/16/2012 at 11:17 AM

---
**内容**: CAD bloke said...
The best decompiler is ... https://github.com/0xd4d/dnSpy - that guy/gal (nobody knows) sure knows a lot about .NET & IL code.
Reply
02/28/2016 at 02:01 AM

---
**内容**: CAD bloke said in reply to CAD bloke...
Actually, I'd say use a couple of decompilers and compare the results. Presently, DotPeek seems better at identifying Events and Reactive Extensions than dnSpy. Telerik's tool is also worth trying. I didn't try Reflector because, well, 3 free ones will do for now.
There is no "best" for situations, perhaps only "best for this line of code"
Reply
03/01/2016 at 12:59 AM

---
