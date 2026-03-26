---
title: "Creating transparent image using ATIL"
date: 2015-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
description: "Here is a sample code that implements a custom ATIL image filter to create transparent images. The implementation sets the Alpha channel for Red co..."
author: Autodesk
---
# Creating transparent image using ATIL

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/creating-transparent-image-using-atil.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code that implements a custom ATIL image filter to create transparent images. The implementation sets the Alpha channel for Red color pixels in the image. You can modify it to use any other RGB value if you choose. The complete sample project can be downloaded here :
Download TransparentSnapShotUsingATIL
The sample project uses the "getSnapShot" to capture a snap shot of the entities selected. To try it,  build the attached sample project and load it in AutoCAD 2015. Open any drawing and run “GenImg” command and select the entity when prompted. The red background is intentionally set to the AcGsDevice while generating the screenshot. This is because, we can then use Red as the color to turn transparent from the image filter. The transparent image is generated under “D:\Temp\Test_Arx.png”.
Here is the relevant code :
//MyRgbaTransparency.h
   #ifndef  MYRGBATRANSPARENCY_H
 #define  MYRGBATRANSPARENCY_H
   class  MyRgbaTransparency 
  : public  Atil::ImageFilter
 {
 public :
  MyRgbaTransparency ( 
   Atil::RowProviderInterface* pInput, 
   int  nKeyColors, 
   Atil::RgbColor* paKeyColors);
    virtual  ~MyRgbaTransparency ();
    virtual  int  rowsRemaining ();
    virtual  void  getNextRow
   (Atil::DataBuffer &oneRow);
    virtual  void  convertColor
   (Atil::ImagePixel& color) const ;
   private :
  enum  By { kQuad, kTreble, kNon };
  By mBy;
  int  mnRows;
  int  mnColumns;
  int  mnKeyColors;
  int  mnRowsRemaining;
  Atil::RgbColor* mpKeyColors;
 };
   #endif
   //MyRgbaTransparency.cpp
 #include  "stdafx.h"
 #include  "MyRgbaTransparency.h"
   MyRgbaTransparency::MyRgbaTransparency
  (Atil::RowProviderInterface* pInput, 
  int  nKeyColors, 
  Atil::RgbColor* paKeyColors )
 {
  connectInput( pInput );
    Atil::Size size(input(0)->size());
  mnColumns = size.width;;
  mnRows = size.height;
  mnRowsRemaining = size.height;
  mnKeyColors = nKeyColors;
    switch (input(0)->dataModel().dataModelType())
  {
   case  Atil::DataModelAttributes
    ::DataModelType::kRgbModel:
   {
    mBy = kTreble;
    init( size );
    break ;
   }
     default :
   {
    mBy = kQuad;
    init( size );
    break ;
   }
  }
 }
   MyRgbaTransparency::~MyRgbaTransparency ()
 {
 }
   int  MyRgbaTransparency::rowsRemaining ()
 {
  return  mnRowsRemaining;
 }
   void  MyRgbaTransparency::getNextRow
  (Atil::DataBuffer &oneRow)
 {
  input(0)->getNextRow(oneRow);
    if  ( mnRowsRemaining > 0 ) 
  {
   if  ( mBy == kTreble ) 
   {
    Atil::RgbColor *pColor = 
     (Atil::RgbColor*) oneRow.dataPtr();
    for  (int  i=0; i<mnColumns; ++i) 
    {
     if ( pColor[i].rgba.red == 255 && 
      pColor[i].rgba.blue == 0 && 
      pColor[i].rgba.green == 0)
     {// Turn alpha to 0 only for Red values
      pColor[i].rgba.alpha = 0;
     }
    }
   } 
   --mnRowsRemaining;
  }
 }
   void  MyRgbaTransparency::convertColor
  (Atil::ImagePixel& color) const
 {
  ImageFilter::convertColor(color);
  switch  ( color.type )
  {
   case  Atil::DataModelAttributes::PixelType::kRgba:
   {
    Atil::RgbColor rgb( color.value.rgba );
    if ( rgb.rgba.red == 255 
     && rgb.rgba.blue == 0 
     && rgb.rgba.green == 0)
    {// Turn alpha to 0 only for Red values
     rgb.packed = rgb.packed;
     rgb.rgba.alpha = 0;
     color.value.rgba = rgb;
    }
    break ;
   }
  }
 }
   // Usage of the Transparency Image filter
   Atil::RgbModel rgbModel(
  Atil::RgbModelAttributes::k4Channels, 
  Atil::DataModelAttributes::kRedGreenBlueAlpha);
   Atil::ImagePixel initialColor(
  Atil::DataModelAttributes::PixelType::kRgba);
   initialColor.setToZero();
 initialColor.type = Atil::DataModelAttributes::kRgba;
 initialColor.value.rgba = 0xff000000;
 Atil::Image imgSource(
  Atil::Size(width, height), 
  &rgbModel, initialColor);
   // get a snapshot of the GsView
 pView->getSnapShot(&imgSource, screenRect.m_min);
   Atil::RowProviderInterface *pPipe 
  = imgSource.read(
   imgSource.size(), 
   Atil::Offset(0,0),Atil::kBottomUpLeftRight);
   if (pPipe != NULL)
 {
  Atil::RgbColor aColors[1];
  COLORREF crBkg = RGB(255, 0, 0); 
    aColors[0] = Atil::RgbColor(
   GetRValue(crBkg), 
   GetGValue(crBkg & 0xffff), 
   GetBValue(crBkg), 0);
    pPipe = new  MyRgbaTransparency(
   pPipe, 
   1, 
   aColors);
  if  (pPipe != NULL && pPipe->isValid()) 
  {
   TCHAR drive[_MAX_DRIVE];
   TCHAR dir[_MAX_DIR];
   TCHAR fname[_MAX_FNAME];
   TCHAR ext[_MAX_EXT]; 
   // find out what extension we have
   _tsplitpath_s(
    pFileName, 
    drive, dir, fname, ext);
     Atil::ImageFormatCodec *pCodec = NULL;
     if  (CString(ext) == _T(".png" ))
    pCodec = new  PngFormatCodec();
     if  (pCodec != NULL)
   {
    // and it is compatible
    if  (Atil::FileWriteDescriptor::
     isCompatibleFormatCodec(
     pCodec, &(pPipe->dataModel()), 
     pPipe->size())) 
    {
    // create a new file output object
    Atil::FileWriteDescriptor fileWriter(pCodec);
    Atil::FileSpecifier fs(
     Atil::StringBuffer((lstrlen(pFileName)+1) 
     * sizeof (TCHAR), 
     (const  Atil::Byte *)pFileName, 
     Atil::StringBuffer::kUTF_16), 
     Atil::FileSpecifier::kFilePath);
      // if the file already exists
    // we better delete it because setFileSpecifier 
    // will fail otherwise
    _tremove(pFileName);
      if  (fileWriter.setFileSpecifier(fs))
    {
     fileWriter.createImageFrame(
      pPipe->dataModel(), 
      pPipe->size());
       // At any rate you want to fetch the property
     // from the write file descriptor then alter 
     // it and set it in\uc1\u8230?
     Atil::FormatCodecPropertyInterface *pProp 
      = fileWriter.getProperty(
     Atil::FormatCodecPropertyInterface::kCompression);
     if  (pProp != NULL) 
     {
     if  (CString(ext) == _T(".png" )) 
     {
      PngCompression *pComp = 
       dynamic_cast <PngCompression*>(pProp);
      if  (pComp != NULL) 
      {
      pComp->selectCompression(
       PngCompressionType::kHigh);
        fileWriter.setProperty(pComp);
      }
     }
       // clean up
     delete  pProp; 
     pProp = NULL;
     }
    }
      Atil::FormatCodecPropertySetIterator* pPropsIter
     = fileWriter.newPropertySetIterator();
    if  (pPropsIter)
    {
     for  (pPropsIter->start(); 
      !pPropsIter->endOfList(); 
      pPropsIter->step())
     {
      Atil::FormatCodecPropertyInterface* pProp
       = pPropsIter->openProperty();
      if  (pProp->isRequired())
      {
       fileWriter.setProperty(pProp);
      }
      pPropsIter->closeProperty();
     }
     delete  pPropsIter;
    }
      Atil::FormatCodecPropertyInterface 
     *pTransparencyProp
    = fileWriter.getProperty(
    Atil::FormatCodecPropertyInterface::kTransparency);
      if (pTransparencyProp)
    {
     fileWriter.setProperty(pTransparencyProp);
    }
      // ok - ready to write it
    fileWriter.writeImageFrame(pPipe);
      done = true ;
    }
   }
   delete  pCodec;
   }
  }
 }

## 评论

**内容**: RANJAN said...
Is it possible convert .CAL to Tiff using ATIL in .NET ?
Reply
11/16/2015 at 02:10 AM

---
**内容**: Balaji said in reply to RANJAN...
Hi Ranjan,
I do not think, ATIL can read a .cal image format. The list of codecs in the ATIL folder does not have a codec for it. I can only find JFIF, JPG, PNG, TIFF and BMP codecs.
Also, ATIL is a C++ only libary. If you want to use ATIL, you may need to create a C++ module and have it loaded in AutoCAD. You can then have your wrapper function invoked from .Net.
Regards,
Balaji
Reply
11/16/2015 at 02:57 AM

---
**内容**: Sun Lingyun said...
Hi Balaji:
The Atil library is so big, where should I start learning? The SDK_DOC only have specification, but do not have any demo code.
Reply
07/13/2018 at 01:33 AM

---
**内容**: leehao said...
Hi, Balaji,
this doesn't work on arx23. I received the black image.
Reply
11/03/2022 at 12:55 AM

---
