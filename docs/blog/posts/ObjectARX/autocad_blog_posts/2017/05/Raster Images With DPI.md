---
title: "Raster Images With DPI"
date: 2017-05-01
categories:
  - AutoCAD
tags:
  - .NET
  - AutoCAD
description: "When Images with encoded DPI information under EXIF structure is attached in AutoCAD, application is not able to correctly detect the resolution in..."
author: Autodesk
---
# Raster Images With DPI

发布日期: 2017-05-01

原始链接: https://adndevblog.typepad.com/autocad/2017/05/raster-images-with-dpi.html

## 文章内容

By Madhukar Moogala
When Images with encoded DPI information under EXIF structure is attached in AutoCAD, application is not able to correctly detect the resolution information.
To understand this better, I have attached one such image with resolution in AutoCAD.
From above screenshot, the horizontal and vertical resolution are incorrect.
However if we use any EXIF library the DPI resolution in the image can be viewed.
For example, I have used
https://github.com/drewnoakes/metadata-extractor-dotnet Module to extract information from image. (Thanks a ton)
string imagePath = "D:\\Temp\\DPI_Resolution\\Rectified Scaled image.jpg";
IEnumerable<Directory> directories = ImageMetadataReader.ReadMetadata(imagePath);
foreach (var directory in directories)
foreach (var tag in directory.Tags)
Console.WriteLine($"{directory.Name} - {tag.Name} = {tag.Description}");
JPEG - Compression Type = Baseline
JPEG - Data Precision = 8 bits
JPEG - Image Height = 2212 pixels
JPEG - Image Width = 2949 pixels
JPEG - Number of Components = 3
JPEG - Component 1 = Y component: Quantization table 0, Sampling factors 2 horiz/2 vert
JPEG - Component 2 = Cb component: Quantization table 1, Sampling factors 1 horiz/1 vert
JPEG - Component 3 = Cr component: Quantization table 1, Sampling factors 1 horiz/1 vert
Exif IFD0 - Orientation = Top, left side (Horizontal / normal)
Exif IFD0 - X Resolution = 2 dots per inch
Exif IFD0 - Y Resolution = 2 dots per inch
Exif IFD0 - Resolution Unit = Inch
Exif IFD0 - Orientation = Top, left side (Horizontal / normal)
Exif SubIFD - Color Space = sRGB
Exif SubIFD - Exif Image Width = 2968 pixels
Exif SubIFD - Exif Image Height = 2226 pixels
Photoshop - Caption Digest = 212 29 140 217 143 0 178 4 233 128 9 152 236 248 66 126
File - File Name = Rectified Scaled image.jpg
File - File Size = 609338 bytes
File - File Modified Date = Thu May 18 16:25:33 +05:30 2017
  From the console output, under Exif IFDO (Image File Director Zero) header. Resolution for X and Y are coded to 2 dots per inch.
But unfortunately AutoCAD doesn’t recognizes EXIF structure, but AutoCAD is designed to read resolution and scale the image accordingly, excerpt from the knowledge article
If an image has resolution information, the program combines this information with the scale factor and the unit of measurement of the drawing to scale the image in your drawing. For example, if your raster image is a scanned blueprint on which the scale is 1 inch equals 50 feet, or 1:600, and your drawing is set up so that 1 unit represents 1 inch, then in the Image dialog box under Scale, select Specify On-Screen. To scale the image, you clear Specify On-Screen, and then enter 600 in Scale. The image is then attached at a scale that brings the geometry in the image into alignment with the geometry in the drawing.
Image resolution can be encoded as under JFIF structure or EXIF structure, currently AutoCAD can recognizes if the image resolution is encoded under JFIF structure.
As per Wikipedia,
JFIF provides resolution or aspect ratio information using an application segment extension to JPEG. It uses Application Segment #0, with a segment header consisting of the null-terminated string spelling "JFIF" in ASCII followed by a byte equal to 0, and specifies that this must be the first segment in the file, hence making it simple to recognize a JFIF file. Exif images recorded by digital cameras generally do not include this segment, but typically comply in all other respects with the JFIF standard.
So we need to encode resolution information under JFIF structure.
Encoding resolution under JFIF ?
Fortunately, Bitmap .NET API sets resolution in JFIF data structure, so we need not rely on any other library nor we need to do byte coding.
string imagePath = "D:\\Temp\\DPI_Resolution\\Rectified Scaled image.jpg";
Bitmap bitmap = new Bitmap(imagePath);
bitmap.SetResolution(2F, 2F);//2F resolution we would like to set in DPI, 2 Dots per Inch
bitmap.Save("D:\\Temp\\DPI_Resolution\\Rectified.jpg");
  After setting image resolution JFIF, and attaching image in AutoCAD,will display correct resolution.
  The images in the screenshot are taken from a customer, this is captured using Spike device.
Inserting image in AutoCAD in real world size is essential for Designer and can leverage AutoCAD tools efficiently if working on existing structure that has been scanned using any device.

## 评论

**内容**: James Maeding said...
in my experience, the .net approach runs out of memory fast for larger images. Things like imagemagick are more robust (and free) solutions, but not sure if they do the tagging like that. Either way, a very useful article so thank you!
Reply
06/01/2017 at 08:08 AM

---
**内容**: Madhukar Moogala said...
Hi James,
I agree, generally in image processing, most sort out approach is use ImageMagick like framework which are written in C++, they play at very low-level manipulating the bytes of Image buffer.
Reply
06/29/2017 at 11:15 PM

---
