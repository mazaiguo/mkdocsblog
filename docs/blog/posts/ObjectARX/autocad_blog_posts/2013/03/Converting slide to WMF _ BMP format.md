---
title: "Converting slide to WMF / BMP format"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - COM
description: "Slides can be converted to WMF / BMP format which is often useful if you want to display it in a picturebox control. To do this conversion, the Sli..."
author: Autodesk
---
# Converting slide to WMF / BMP format

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/converting-slide-to-wmf-bmp-format.html

## 文章内容

By Balaji Ramamoorthy
Slides can be converted to WMF / BMP format which is often useful if you want to display it in a picturebox control. To do this conversion, the SlideLibrary COM object comes very handy.
This COM object is available for use after you have registered the slide.ocx from the AutoCAD Utilities.
To register the control, open the command prompt and type :
regsvr32 /c "C:\Program Files\Autodesk\ADNUtilities2013_X64\AutoCADControls\Slide.ocx"
Use of late-binding calls will avoid the need for any additional references in our project.
Here is a sample code in C# and VB.Net that makes late-bound calls to the SlideLibrary COM object :
1) C# code using the "InvokeMember" :
//using System.Reflection;
try
{
    const string progID = "AutoCAD.SlideLib";
      Type slideLibType = Type.GetTypeFromProgID(progID);
    object slidLibObj = Activator.CreateInstance(slideLibType, true);
      if (slidLibObj != null)
    {
        object[] dataArry1 = new object[1];
        dataArry1[0] = @"C:\Temp\Solids.sld";
        slidLibObj.GetType().InvokeMember(
                                            "Append",
                                            BindingFlags.InvokeMethod,
                                            null,
                                            slidLibObj,
                                            dataArry1
                                         );
          object[] dataArry2 = new object[2];
          // Index to the slide in the slide library
        dataArry2[0] = 0;
        // Path of the bitmap to generate
        dataArry2[1] = @"C:\Temp\MySlideImage.bmp";
          slidLibObj.GetType().InvokeMember(
                                            "SaveToBmp",
                                            BindingFlags.InvokeMethod,
                                            null,
                                            slidLibObj,
                                            dataArry2
                                         );
    }
}
catch (System.Exception ex)
{
    System.Windows.Forms.MessageBox.Show(ex.Message);
}
2) C# code using the "dynamic" keyword (available in .Net 4.0 onwards) :
// Using the .Net 4.0 dynamic keyword, it is easier
// to make late-bound calls to COM objects
try
{
    const string progID = "AutoCAD.SlideLib";
    Type slideLibType = Type.GetTypeFromProgID(progID);
    dynamic slidLibObj = Activator.CreateInstance(slideLibType, true);
    slidLibObj.Append(@"C:\Temp\Solids.sld");
    slidLibObj.SaveToBmp(0, @"C:\Temp\MySlideImage.bmp");
}
catch (System.Exception ex)
{
    System.Windows.Forms.MessageBox.Show(ex.Message);
}
3) VB.Net code :
Try
Dim slb As Object
    slb = CreateObject("AutoCAD.SlideLib")
    slb.Append("C:\Temp\Solids.sld")
    slb.SaveToBmp(0, "C:\Temp\MySlideImage.bmp")
Catch ex As System.Exception
    System.Windows.Forms.MessageBox.Show(ex.Message)
End Try
The slidelibrary object also provides a method to convert it to a WMF format. For this, please use "SaveToWmf" instead of the "SaveToBmp" in the above code.

## 评论

**内容**: Eric said...
I don't know why, is the lib version changed or something else, but this line:
const string progID = "AutoCAD.SlideLib";
should be changed to:
const string progID = "AutoCAD.SlideLib.5";
Reply
03/31/2014 at 05:22 PM

---
**内容**: Balaji said...
Hi Eric,
Thanks for mentioning this.
You are right. I see that the 2013 version of the slide library has a progId "AutoCAD.SlideLib.5".
Regards,
Balaji
Reply
04/01/2014 at 05:42 PM

---
**内容**: bieresCad said...
Hola
Estoy usando autocad 2016, no funciona con AutoCAD.SlideLib.5 ni con AutoCAD.SlideLib
Reply
11/25/2015 at 06:23 AM

---
