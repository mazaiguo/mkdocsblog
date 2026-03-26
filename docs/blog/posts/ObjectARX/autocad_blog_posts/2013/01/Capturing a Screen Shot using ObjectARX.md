---
title: "Capturing a Screen Shot using ObjectARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "How to capture the screen shot of a Viewport to save it to an image file?"
author: Autodesk
---
# Capturing a Screen Shot using ObjectARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/capturing-a-screen-shot-using-objectarx.html

## 文章内容

By Fenton Webb
Issue
How to capture the screen shot of a Viewport to save it to an image file?
Is it possible to temporarily display an image over the Viewport or alter the Viewport display?
Solution
There are two AcGs functions in ObjectARX SDK that can be used to get the screen shot of the specified Viewport in AutoCAD and also to set an image to be displayed in a specified Viewport.
The functions are:
acgsGetScreenShot()
acgsDisplayImage()
The function acgsGetScreenShot() will get you the pointer to an AcGsScreenShot object for the specified viewport number. When in TILEMODE 1, just specify the Viewport that you are interested in or just specify “0” to get the entire ModelSpace (and same is the case with PaperSpace). Similarly just specify the Viewport number you are interested in if the TILEMODE is 0 (i.e. in PaperSpace). Also if you specify viewport number of 1 in TILEMODE 0 then you will get only the entities that exist in the PaperSpace.
You can get the image data using the method getScanline() of the AcGsScreenShot class. Using this you can fill in an array of truecolor long words which essentially will be the ARBG data. This data can be used to create an image file. You can use the ATIL SDK to create a bitmap or JPG easily from the image data.
The function acgsDisplayImage() on the other hand takes an array of truecolor long words and displays the image at the specified location on a specified Viewport. The image will stay till a redraw is called.
This function can be used to:
Show a temporary external image quickly.
Blank the entire view port temporarily.
Change the colors of the Viewport. Say inverting the colors of the Viewport.
Note:The acgsGetScreenShot() does not get you the shaded or rendered view.
Here’s some code which shows how to use the functions, to use the Atil libs you need to link with the headers and libs in the Atil folder of the ObjectARX SDK:
// by Fenton Webb, DevTech, 1/30/2013
// screen shoots the view details as a BMP
bool RecordViewDetails(double &fieldWidth, double &fieldHeight, AcGePoint3d &position, AcGePoint3d &target, AcGeVector3d &upVector, const TCHAR *imagePath)
{
  int iVP = getCVPort();
    // Compute the viewport dimensions.
  int nLeft, nBottom, nRight, nTop;
  int iImageWidth, iImageHeight;
  acgsGetViewportInfo (iVP, nLeft, nBottom, nRight, nTop);
    iImageWidth  = nRight - nLeft + 1;
  iImageHeight = nTop - nBottom + 1;
  Atil::Size size(iImageWidth, iImageHeight);
  int nBytesPerRow = Atil::DataModel::bytesPerRow(iImageWidth,
                                Atil::DataModelAttributes::k32);
  unsigned long nBufferSize = iImageHeight * nBytesPerRow;
    // Create an ATIL image for accepting the rendered image.
  std::auto_ptr<char> autoBuff = std::auto_ptr<char>(new char[nBufferSize]);
  char *pSnapshotData = autoBuff.get(); 
  Atil::Image * pImage = NULL;
  // see if there is a GS view created
  AcGsView *pView = acgsGetGsView(iVP, false);
  // if not
  if (NULL == pView)
  {
    // then we must be in 2D wireframe mode, so use acgsGetScreenShot
    std::auto_ptr<AcGsScreenShot> autoScreenShot(acgsGetScreenShot(iVP));
    AcGsScreenShot* screenShot = autoScreenShot.get(); // auto_ptr still owns the pointer.
    if (screenShot)
    {
      int w = 0, h = 0, d = 0;
      screenShot->getSize(w, h, d);
        char* pBufTemp = pSnapshotData;
      for (int row = 0; row < h; row++)
      {
        memcpy(pBufTemp, screenShot->getScanline(0, row), nBytesPerRow);
          // convert from RGBA to BGRA
        char* pColor = pBufTemp;
        for (int i = 0; i < w; i++)    // Slow but it works
        {
          char temp = *pColor;
          *pColor = *(pColor + 2);
          *(pColor + 2) = temp;
          pColor += 4;
        }
        pBufTemp += nBytesPerRow;
      }
      pImage = constructAtilImg(reinterpret_cast<char*>(pSnapshotData),
                    nBufferSize, nBytesPerRow, w, h, 32, 0);
      std::auto_ptr<Atil::Image> autodeleter = std::auto_ptr<Atil::Image>(pImage); // auto_ptr now owns the image
        if (!writeImageFile(pImage, kBMP, imagePath))
      {
        acutPrintf(_T("\nFailed to write image file %s"), imagePath);
        return false;
      }
      else
        acutPrintf(_T("\nSuccessfully written %s"), imagePath);
      }
      return true;
  }
  else
  {
    return snapGSView(pView, iImageWidth, iImageHeight, fieldHeight, fieldWidth, position, target, upVector, imagePath);
  }
}
  bool snapGSView(AcGsView *pView, int width, int height, double &fieldWidth, double &fieldHeight, AcGePoint3d &position, AcGePoint3d &target, AcGeVector3d &upVector, const TCHAR *imagePath)
{
  Atil::Size size(width, height);
  int nBytesPerRow = Atil::DataModel::bytesPerRow(width, Atil::DataModelAttributes::k32);
  unsigned long nBufferSize = height * nBytesPerRow;
    // Create an ATIL image for accepting the rendered image.
  std::auto_ptr<char> apCharBuffer = std::auto_ptr<char>(new char[nBufferSize]);
  char *pSnapshotData = apCharBuffer.get();  //  auto_ptr still owns the buffer.
    // in shaded mode (from GS)
  Atil::Image * pImage = NULL;
  pImage = constructAtilImg(pSnapshotData, nBufferSize, nBytesPerRow, width, height, 32, 0);
  std::auto_ptr<Atil::Image> autodeleter = std::auto_ptr<Atil::Image>(pImage); // auto_ptr now owns the image
  pView->getSnapShot(pImage, AcGsDCPoint(0, 0));
    // add a temp image to invert the image. do we have a better way to turn an image around?
  Atil::Image imgTempForInverted(pImage->read(pImage->size(), Atil::Offset(0, 0), Atil::kBottomUpLeftRight));
  *pImage = imgTempForInverted;
    if (!writeImageFile(pImage, kBMP, imagePath))
  {
    acutPrintf(_T("\nFailed to write image file %s"), imagePath);
    return false;
  }
  else
    acutPrintf(_T("\nSuccessfully written %s"), imagePath);
    // record the view data
  fieldHeight = pView->fieldHeight();
  fieldWidth = pView->fieldWidth();
  position = pView->position();
  target = pView->target();
  upVector = pView->upVector();
    return true;
}
  bool writeImageFile (Atil::Image *pImageSource, eFormatType formatType,
  wchar_t const *pFileName)
{
  _ASSERT(NULL != pImageSource);
  if(NULL == pImageSource)
    return false;
    _ASSERT(pImageSource->isValid());
  if(!pImageSource->isValid())
    return false;
    if(PathFileExists(pFileName))
    DeleteFile(pFileName);
    /*if(PathFileExists(pFileName)) {
  if(IsFileReadOnly(pFileName)) {
  RemoveReadonlyAttribute(pFileName);
  DeleteFile(pFileName);
  }
  }*/
    if(PathFileExists(pFileName))
    return false;
    Atil::RowProviderInterface* pPipe = pImageSource->read(pImageSource->size(),
    Atil::Offset(0,0));
  _ASSERTE(NULL != pPipe);
  if(!pPipe)
    return false;
    Atil::FileWriteDescriptor  *pFWD = NULL;
  Atil::ImageFormatCodec     *pCodec = NULL;
    if (formatType == kJPG)
    pCodec = new JfifFormatCodec();
  else if (formatType == kPNG)
    pCodec = new PngFormatCodec();
  else if (formatType == kTIF)
    pCodec = new TiffFormatCodec();
  else if (formatType == kBMP)
    pCodec = new BmpFormatCodec();
    _ASSERTE(NULL != pCodec);
  if(NULL == pCodec)
    return false;
    if(!Atil::FileWriteDescriptor::isCompatibleFormatCodec(pCodec,
    &(pPipe->dataModel()), pPipe->size())) {
      delete pCodec;
      return false;
  }
    pFWD = new Atil::FileWriteDescriptor(pCodec);
  _ASSERTE(NULL != pFWD);
  #ifdef UNICODE
#ifndef _ADESK_MAC_
  Atil::FileSpecifier fs(Atil::StringBuffer((lstrlen(pFileName) + 1) * sizeof(TCHAR),
    (const Atil::Byte *) pFileName, Atil::StringBuffer::kUTF_16),
    Atil::FileSpecifier::kFilePath);
#else
  Atil::FileSpecifier fs(Atil::StringBuffer((lstrlen(pFileName) + 1) * sizeof(TCHAR),
    (const Atil::Byte *) pFileName, Atil::StringBuffer::kUTF_32),
    Atil::FileSpecifier::kFilePath);
  #endif
#else
  Atil::FileSpecifier fs(Atil::StringBuffer(lstrlen(pFileName) + 1,
    (const Atil::Byte *) pFileName, Atil::StringBuffer::kASCII),
    Atil::FileSpecifier::kFilePath);
#endif
    if (!pFWD->setFileSpecifier(fs))
    return false;
    pFWD->createImageFrame(pPipe->dataModel(), pPipe->size());
    if (formatType == kPNG) {
    Atil::FormatCodecPropertyInterface* pProp = pFWD->getProperty(Atil::FormatCodecPropertyInterface::kCompression);
    if (pProp != NULL) {
      PngCompression* pPngComp = (PngCompression*)(pProp);
      if ( pPngComp != NULL ) {
        // Why not compress all we can?
        pPngComp->selectCompression(PngCompressionType::kHigh);
        pFWD->setProperty(pPngComp);
      }
      delete pProp;
      pProp = NULL;
    }
  }
  else if (formatType == kTIF) {
    Atil::FormatCodecPropertyInterface* pProp = pFWD->getProperty(Atil::FormatCodecPropertyInterface::kCompression);
    if (pProp != NULL) {
      TiffCompression* pComp = (TiffCompression*)(pProp);
      if ( pComp != NULL ) {
        // G4 is only valid for 1 bit images.
        if ( pComp->selectCompression(TiffCompressionType::kCCITT_FAX4) == false ) {
          // So if that fails, resort to LZW now that it is patent free
          if ( pComp->selectCompression(TiffCompressionType::kLZW) == false ) {
            // If that fails (and is shouldn't, be) then set none.
            pComp->selectCompression(TiffCompressionType::kNone);
          }
        }
        pFWD->setProperty(pComp);
      }
      delete pProp;
      pProp = NULL;
    }
  }
// get the current vp
int getCVPort()
{
  struct resbuf rb;
  ads_getvar(_T("CVPORT"), &rb);
  return rb.resval.rint;
}
  Atil::DataModel* colorSpace (char *&pRGBData, int colorDepth, int paletteSize)
{
  _ASSERT(NULL != pRGBData);
    // Setup a color space, with palette if needed
  Atil::DataModel *pDm = NULL;
  if (colorDepth == 8) {
    Atil::RgbColor space[256];
      Atil::RgbPaletteModel *pPM = new Atil::RgbPaletteModel();
    _ASSERT(NULL != pPM);
    if(!pPM)
      return NULL;
      pDm = pPM;
    char *palette = pRGBData;
    pRGBData += paletteSize;
    for (int i = 0; i < paletteSize; i += 4)
      space[i / 4] = Atil::RgbColor(palette[i+2],palette[i+1],palette[i], 255);
    pPM->setEntries(0, 256, (Atil::RgbColor *)&space);
  } else
    pDm = new Atil::RgbModel(32);
      _ASSERT(NULL != pDm);
  return pDm;
}
  Atil::Image *constructAtilImg(char *pRGBData,
  unsigned long bufferSize, unsigned long rowBytes,
  unsigned long xSize, unsigned long ySize, int colorDepth, int paletteSize)
{
  if ((8 != colorDepth) && (32 != colorDepth))
  {
    return NULL;
  }
    if (paletteSize)
  {
    if ((paletteSize < 0) || (paletteSize > 255))
    {
      return NULL;
    }
  }
    if ((xSize <= 0) || (ySize <= 0))
  {
    return NULL;
  }
    Atil::Image *pImg = NULL;
  Atil::Size size(xSize, ySize);
    // construct the Atil::Image object
  if (pRGBData) {
      // Check the buffer for size and definition
    if (bufferSize) {
      if (!rowBytes) {
        return NULL;
      }
        // did they allocate enough?
      if (rowBytes * ySize > bufferSize) {
        return NULL;
      }
    }
    else {
      return NULL;
    }       
      Atil::DataModel *pM = colorSpace(pRGBData, colorDepth, paletteSize);
    _ASSERT(NULL != pM);
    if(NULL == pM)
      return NULL;
      try {
      // BEWARE: pRGBData may be moved in colorSpace
      pImg = new Atil::Image(pRGBData, bufferSize,
        rowBytes, size, pM); 
    } catch (Atil::ATILException* pExpCon) {
      // image construction failure
      delete pExpCon;
      delete pM;
      pImg = NULL;
      _ASSERT(FALSE);
      return NULL;
    }
      delete pM;
  }
  else {
    Atil::RgbModel     rgbM(32);
    Atil::RgbGrayModel gM;
      Atil::ImagePixel initialColor(colorDepth == 32 ?
      Atil::DataModelAttributes::kRgba :
    Atil::DataModelAttributes::kGray);
    initialColor.setToZero();
      try {
      pImg = new Atil::Image(size,
        colorDepth == 32 ? &rgbM : &gM,
        initialColor);
    } catch (Atil::ATILException* pExpCon) {
      // image construction failure
      delete pExpCon;
      pImg = NULL;
      _ASSERT(FALSE);
      return NULL;
    }
  }
    _ASSERT(NULL != pImg);
  return pImg;
}
  bool getTempImgFile(TCHAR * fileName)
{
  // Here we create a temp bmp file as a transitional file
  TCHAR tempDic[MAX_PATH];
  ::memset(tempDic,0,MAX_PATH);
  DWORD nRetSize = ::GetTempPath(MAX_PATH,tempDic);
  if (nRetSize > MAX_PATH || nRetSize == 0)
  {
    const TCHAR * tempStr = _T("C:\\temp");
    if (wcscpy_s(tempDic,tempStr) != 0)
    {
      return false;
    }
      if (::PathFileExists(tempStr) == FALSE &&
      ::CreateDirectory(tempStr,NULL) == FALSE)
    {
      return false;
    }
  }
    // create the temp file whose prefix is "img"
  if (::GetTempFileName(tempDic,_T("tmp"),0,fileName) == 0)
  {
    return false;
  }
    // now split the filepath into its individual components
  TCHAR drive[_MAX_DRIVE], dir[_MAX_DIR], fname[_MAX_FNAME], ext[_MAX_EXT];
  _tsplitpath (fileName, drive, dir, fname, ext);
  _stprintf(fileName, _T("%s%s%s.bmp"), drive, dir, fname);
    return true;
}

## 评论

**内容**: tbrammer said...
Hi Fenton,
there are some lines missing at the end of writeImageFile():
pFWD->writeImageFrame(pPipe);
delete pFWD; //this also flushes and closes the file
return true;
You'll get no file output without these calls.
Below is the code ready to compile & link.
I added a function void cmdTestAtilOut() that can be registered as command.

#include "stdafx.h"
#include "AtilDefs.h"
#include "Image.h"
#include "RgbModel.h"
#include "RgbPaletteModel.h"
#include "PngCustomProperties.h"
#include "BitonalModel.h"
#include "atilformats.h"
#include "JFIFFormatCodec.h"
#include "TiffFormatCodec.h"
#include "TiffCustomProperties.h"
#include "BmpFormatCodec.h"
#include "FileSpecifier.h"
#include "FileWriteDescriptor.h"
#include "FileReadDescriptor.h"
#include "RowProviderInterface.h"
#pragma comment (lib ,"AdImaging.lib")
#pragma comment (lib ,"AdIntImgServices.lib")

enum eFormatType
{
kJPG,
kPNG,
kTIF,
kBMP
};
// get the current vp
int getCVPort()
{
struct resbuf rb;
ads_getvar(_T("CVPORT"), &rb);
return rb.resval.rint;
}
Atil::DataModel* colorSpace (char *&pRGBData, int colorDepth, int paletteSize)
{
_ASSERT(NULL != pRGBData);
// Setup a color space, with palette if needed
Atil::DataModel *pDm = NULL;
if (colorDepth == 8) {
Atil::RgbColor space[256];
Atil::RgbPaletteModel *pPM = new Atil::RgbPaletteModel();
_ASSERT(NULL != pPM);
if(!pPM)
return NULL;
pDm = pPM;
char *palette = pRGBData;
pRGBData += paletteSize;
for (int i = 0; i < paletteSize; i += 4)
space[i / 4] = Atil::RgbColor(palette[i+2],palette[i+1],palette[i], 255);
pPM->setEntries(0, 256, (Atil::RgbColor *)&space);
} else
pDm = new Atil::RgbModel(32);

_ASSERT(NULL != pDm);
return pDm;
}

Atil::Image *constructAtilImg(char *pRGBData,
unsigned long bufferSize, unsigned long rowBytes,
unsigned long xSize, unsigned long ySize, int colorDepth, int paletteSize)
{
if ((8 != colorDepth) && (32 != colorDepth))
{
return NULL;
}
if (paletteSize)
{
if ((paletteSize < 0) || (paletteSize > 255))
{
return NULL;
}
}
if ((xSize <= 0) || (ySize <= 0))
{
return NULL;
}
Atil::Image *pImg = NULL;
Atil::Size size(xSize, ySize);
// construct the Atil::Image object
if (pRGBData) {
// Check the buffer for size and definition
if (bufferSize) {
if (!rowBytes) {
return NULL;
}
// did they allocate enough?
if (rowBytes * ySize > bufferSize) {
return NULL;
}
}
else {
return NULL;
}
Atil::DataModel *pM = colorSpace(pRGBData, colorDepth, paletteSize);
_ASSERT(NULL != pM);
if(NULL == pM)
return NULL;
try {
// BEWARE: pRGBData may be moved in colorSpace
pImg = new Atil::Image(pRGBData, bufferSize,
rowBytes, size, pM);
} catch (Atil::ATILException* pExpCon) {
// image construction failure
delete pExpCon;
delete pM;
pImg = NULL;
_ASSERT(FALSE);
return NULL;
}
delete pM;
}
else {
Atil::RgbModel rgbM(32);
Atil::RgbGrayModel gM;
Atil::ImagePixel initialColor(colorDepth == 32 ?
Atil::DataModelAttributes::kRgba :
Atil::DataModelAttributes::kGray);
initialColor.setToZero();
try {
pImg = new Atil::Image(size,
colorDepth == 32 ? &rgbM : &gM,
initialColor);
} catch (Atil::ATILException* pExpCon) {
// image construction failure
delete pExpCon;
pImg = NULL;
_ASSERT(FALSE);
return NULL;
}
}
_ASSERT(NULL != pImg);
return pImg;
}
bool writeImageFile (Atil::Image *pImageSource, eFormatType formatType, wchar_t const *pFileName)
{
_ASSERT(NULL != pImageSource);
if(NULL == pImageSource)
return false;

_ASSERT(pImageSource->isValid());
if(!pImageSource->isValid())
return false;

if(PathFileExists(pFileName))
DeleteFile(pFileName);

/*if(PathFileExists(pFileName)) {
if(IsFileReadOnly(pFileName)) {
RemoveReadonlyAttribute(pFileName);
DeleteFile(pFileName);
}
}*/

if(PathFileExists(pFileName))
return false;

Atil::RowProviderInterface* pPipe = pImageSource->read(pImageSource->size(),
Atil::Offset(0,0));
_ASSERTE(NULL != pPipe);
if(!pPipe)
return false;

Atil::FileWriteDescriptor *pFWD = NULL;
Atil::ImageFormatCodec *pCodec = NULL;

if (formatType == kJPG)
pCodec = new JfifFormatCodec();
else if (formatType == kPNG)
pCodec = new PngFormatCodec();
else if (formatType == kTIF)
pCodec = new TiffFormatCodec();
else if (formatType == kBMP)
pCodec = new BmpFormatCodec();

_ASSERTE(NULL != pCodec);
if(NULL == pCodec)
return false;

if(!Atil::FileWriteDescriptor::isCompatibleFormatCodec(pCodec,
&(pPipe->dataModel()), pPipe->size())) {
delete pCodec;
return false;
}

pFWD = new Atil::FileWriteDescriptor(pCodec);
_ASSERTE(NULL != pFWD);

#ifdef UNICODE
#ifndef _ADESK_MAC_
Atil::FileSpecifier fs(Atil::StringBuffer((lstrlen(pFileName) + 1) * sizeof(TCHAR),
(const Atil::Byte *) pFileName, Atil::StringBuffer::kUTF_16),
Atil::FileSpecifier::kFilePath);
#else
Atil::FileSpecifier fs(Atil::StringBuffer((lstrlen(pFileName) + 1) * sizeof(TCHAR),
(const Atil::Byte *) pFileName, Atil::StringBuffer::kUTF_32),
Atil::FileSpecifier::kFilePath);

#endif
#else
Atil::FileSpecifier fs(Atil::StringBuffer(lstrlen(pFileName) + 1,
(const Atil::Byte *) pFileName, Atil::StringBuffer::kASCII),
Atil::FileSpecifier::kFilePath);
#endif

if (!pFWD->setFileSpecifier(fs))
return false;

pFWD->createImageFrame(pPipe->dataModel(), pPipe->size());

if (formatType == kPNG) {
Atil::FormatCodecPropertyInterface* pProp = pFWD->getProperty(Atil::FormatCodecPropertyInterface::kCompression);
if (pProp != NULL) {
PngCompression* pPngComp = (PngCompression*)(pProp);
if ( pPngComp != NULL ) {
// Why not compress all we can?
pPngComp->selectCompression(PngCompressionType::kHigh);
pFWD->setProperty(pPngComp);
}
delete pProp;
pProp = NULL;
}
}
else if (formatType == kTIF) {
Atil::FormatCodecPropertyInterface* pProp = pFWD->getProperty(Atil::FormatCodecPropertyInterface::kCompression);
if (pProp != NULL) {
TiffCompression* pComp = (TiffCompression*)(pProp);
if ( pComp != NULL ) {
// G4 is only valid for 1 bit images.
if ( pComp->selectCompression(TiffCompressionType::kCCITT_FAX4) == false ) {
// So if that fails, resort to LZW now that it is patent free
if ( pComp->selectCompression(TiffCompressionType::kLZW) == false ) {
// If that fails (and is shouldn't, be) then set none.
pComp->selectCompression(TiffCompressionType::kNone);
}
}
pFWD->setProperty(pComp);
}
delete pProp;
pProp = NULL;
}
}
//TB141111 this was missing:
int iRet = pFWD->writeImageFrame(pPipe);
delete pFWD;
pFWD = NULL;
return true;
}
bool snapGSView(eFormatType fmt, AcGsView *pView, int width, int height, double &fieldWidth, double &fieldHeight, AcGePoint3d &position, AcGePoint3d &target, AcGeVector3d &upVector, const TCHAR *imagePath)
{
Atil::Size size(width, height);
int nBytesPerRow = Atil::DataModel::bytesPerRow(width, Atil::DataModelAttributes::k32);
unsigned long nBufferSize = height * nBytesPerRow;

// Create an ATIL image for accepting the rendered image.
std::auto_ptr apCharBuffer = std::auto_ptr(new char[nBufferSize]);
char *pSnapshotData = apCharBuffer.get(); // auto_ptr still owns the buffer.

// in shaded mode (from GS)
Atil::Image * pImage = NULL;
pImage = constructAtilImg(pSnapshotData, nBufferSize, nBytesPerRow, width, height, 32, 0);
std::auto_ptr autodeleter = std::auto_ptr(pImage); // auto_ptr now owns the image
pView->getSnapShot(pImage, AcGsDCPoint(0, 0));

// add a temp image to invert the image. do we have a better way to turn an image around?
Atil::Image imgTempForInverted(pImage->read(pImage->size(), Atil::Offset(0, 0), Atil::kBottomUpLeftRight));
*pImage = imgTempForInverted;

if (!writeImageFile(pImage, fmt, imagePath))
{
acutPrintf(_T("\nFailed to write image file %s"), imagePath);
return false;
}
else
acutPrintf(_T("\nSuccessfully written %s"), imagePath);

// record the view data
fieldHeight = pView->fieldHeight();
fieldWidth = pView->fieldWidth();
position = pView->position();
target = pView->target();
upVector = pView->upVector();

return true;
}
bool getTempImgFile(TCHAR * fileName)
{
// Here we create a temp bmp file as a transitional file
TCHAR tempDic[MAX_PATH];
::memset(tempDic,0,MAX_PATH);
DWORD nRetSize = ::GetTempPath(MAX_PATH,tempDic);
if (nRetSize > MAX_PATH || nRetSize == 0)
{
const TCHAR * tempStr = _T("C:\\temp");
if (wcscpy_s(tempDic,tempStr) != 0)
{
return false;
}

if (::PathFileExists(tempStr) == FALSE &&
::CreateDirectory(tempStr,NULL) == FALSE)
{
return false;
}
}

// create the temp file whose prefix is "img"
if (::GetTempFileName(tempDic,_T("tmp"),0,fileName) == 0)
{
return false;
}

// now split the filepath into its individual components
TCHAR drive[_MAX_DRIVE], dir[_MAX_DIR], fname[_MAX_FNAME], ext[_MAX_EXT];
_tsplitpath (fileName, drive, dir, fname, ext);
_stprintf(fileName, _T("%s%s%s.bmp"), drive, dir, fname);

return true;
}
// by Fenton Webb, DevTech, 1/30/2013
// screen shoots the view details as a BMP
bool RecordViewDetails(eFormatType fmt, double &fieldWidth, double &fieldHeight, AcGePoint3d &position, AcGePoint3d &target, AcGeVector3d &upVector, const TCHAR *imagePath)
{
int iVP = getCVPort();
// Compute the viewport dimensions.
int nLeft, nBottom, nRight, nTop;
int iImageWidth, iImageHeight;
acgsGetViewportInfo (iVP, nLeft, nBottom, nRight, nTop);
iImageWidth = nRight - nLeft + 1;
iImageHeight = nTop - nBottom + 1;
Atil::Size size(iImageWidth, iImageHeight);
int nBytesPerRow = Atil::DataModel::bytesPerRow(iImageWidth,
Atil::DataModelAttributes::k32);
unsigned long nBufferSize = iImageHeight * nBytesPerRow;
// Create an ATIL image for accepting the rendered image.
std::auto_ptr autoBuff = std::auto_ptr(new char[nBufferSize]);
char *pSnapshotData = autoBuff.get();
Atil::Image * pImage = NULL;
// see if there is a GS view created
AcGsView *pView = acgsGetGsView(iVP, false);
// if not
if (NULL == pView)
{
// then we must be in 2D wireframe mode, so use acgsGetScreenShot
std::auto_ptr autoScreenShot(acgsGetScreenShot(iVP));
AcGsScreenShot* screenShot = autoScreenShot.get(); // auto_ptr still owns the pointer.
if (screenShot)
{
int w = 0, h = 0, d = 0;
screenShot->getSize(w, h, d);
char* pBufTemp = pSnapshotData;
for (int row = 0; row < h; row++)
{
memcpy(pBufTemp, screenShot->getScanline(0, row), nBytesPerRow);
// convert from RGBA to BGRA
char* pColor = pBufTemp;
for (int i = 0; i < w; i++) // Slow but it works
{
char temp = *pColor;
*pColor = *(pColor + 2);
*(pColor + 2) = temp;
pColor += 4;
}
pBufTemp += nBytesPerRow;
}
pImage = constructAtilImg(reinterpret_cast(pSnapshotData),
nBufferSize, nBytesPerRow, w, h, 32, 0);
std::auto_ptr autodeleter = std::auto_ptr(pImage); // auto_ptr now owns the image
if (!writeImageFile(pImage, fmt, imagePath))
{
acutPrintf(_T("\nFailed to write image file %s"), imagePath);
return false;
}
else
acutPrintf(_T("\nSuccessfully written %s"), imagePath);
}
return true;
}
else
{
return snapGSView(fmt, pView, iImageWidth, iImageHeight, fieldHeight, fieldWidth, position, target, upVector, imagePath);
}
}
void cmdTestAtilOut()
{
bool bSuccess=false;
eFormatType formatType = kJPG;
wchar_t const *pFileName = NULL;
double fieldWidth=800.0, fieldHeight=600.0;
AcGePoint3d position, target;
AcGeVector3d upVector(AcGeVector3d::kZAxis);
pFileName = _T("C:\\temp\\atil.bmp");
bSuccess=RecordViewDetails(kBMP, fieldWidth, fieldHeight, position, target, upVector, pFileName);
pFileName = _T("C:\\temp\\atil.png");
bSuccess=RecordViewDetails(kPNG, fieldWidth, fieldHeight, position, target, upVector, pFileName);
pFileName = _T("C:\\temp\\atil.jpg");
bSuccess=RecordViewDetails(kJPG, fieldWidth, fieldHeight, position, target, upVector, pFileName);
}
Reply
11/11/2014 at 01:41 AM

---
**内容**: tbrammer said...
Is it possible to create the images with a different background color?
Reply
11/11/2014 at 01:56 AM

---
**内容**: sudarshan d. said...
Image quality is poor so i assigned bits/pixel as k64 but getting an exception in converting rgba to bgra i think beacuse of buffer size, the data type used is char * .so it is throwing an exception.
at char* Pbufftemp=pSnapshotdata;in nested for loop
so please suggest me what should i do to get an image with good quality.
Reply
02/05/2016 at 03:54 AM

---
