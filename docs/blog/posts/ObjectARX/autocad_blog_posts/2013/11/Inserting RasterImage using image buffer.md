---
title: "Inserting RasterImage using image buffer"
date: 2013-11-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "The AcDbRasterImageDef::setImage can be used, if you do not want to include the image file path while inserting a raster image. This can be conside..."
author: Autodesk
---
# Inserting RasterImage using image buffer

发布日期: 2013-11-01

原始链接: https://adndevblog.typepad.com/autocad/2013/11/inserting-rasterimage-using-image-buffer.html

## 文章内容

By Balaji Ramamoorthy
The AcDbRasterImageDef::setImage can be used, if you do not want to include the image file path while inserting a raster image. This can be considered another approach to accomplish what is explained in this blog post. The AcDbRasterImageDef::setImage method requires a pointer to an ATIL image. In this sample code, the image buffer is read from the image and is used to create an ATIL image. The ATIL image pointer is used with the AcDbRasterImageDef::setImage to create a raster image definition. To build this sample code, you will need the include and library files from the ObjectARX SDK folder under "\utils\Atil".
static void AdskInsertImage(void)
{
    // Image path to use for the RasterImageDef
    AcString imagePath(ACRX_T("C:\\Temp\\Test.png"));
      // Load the image to get access to its image buffer
    AcTcImage tc;
    tc.Load(imagePath);
      HBITMAP bmp=0;
    tc.GetHBITMAP(RGB(0xff,0xff,0xff),bmp);
      if (bmp == NULL)
        return;
      BITMAP _bmp={0};
    GetObject(bmp,sizeof BITMAP,&_bmp);
      HDC hdcScr=GetDC(NULL);
    HDC    hdcMem=CreateCompatibleDC(hdcScr);
    SelectObject(hdcMem,bmp);
      // Create an Atil::Image.
    // The AcDbRasterImageDef::setImage requires it
    Atil::ImagePixel initialImage;
    initialImage.setToZero();
    initialImage.type = Atil::DataModelAttributes::kRgba;
    initialImage.value.rgba = 0xff000000;
      Atil::Size size(_bmp.bmWidth, _bmp.bmHeight);
    const Atil::RgbModel *pDm = new Atil::RgbModel(
        Atil::RgbModelAttributes::k4Channels,
        Atil::DataModelAttributes::kBlueGreenRedAlpha);
      Atil::Image *pAtilImage = new Atil::Image(
                                     size, pDm, initialImage);
      // Write the image data on to the Atil image
    // using an Image Context
    Atil::Offset upperLeft(0,0);
    Atil::ImageContext *pImgContext
        = pAtilImage->createContext(
                                    Atil::ImageContext::kWrite,
                                    size,
                                    upperLeft
                                    );
    if (pImgContext != NULL)
    {
        for (int xf=0;xf<_bmp.bmWidth;xf++)
        {
            for (int yf=0;yf<_bmp.bmHeight;yf++)
            {
                BYTE alpha=0x0;
                  COLORREF pix=GetPixel(hdcMem,xf,yf);
                  BYTE rr = (pix&0xff);
                BYTE gg = (pix>>8)&0xff;
                BYTE bb = (pix>>16)&0xff;
                  // Alpha channel to account for transparency
                if ((rr!=0xff) || (gg!=0xff) || (bb!=0xff))
                    alpha=0xff;
                  Atil::RgbColor p;
                p.set(rr, gg, bb, alpha);
                pImgContext->put32(xf, yf, p);
            }
        }
      }
    pImgContext->flush();
    delete pImgContext;
      bool isImageValid = pAtilImage->isValid();
    ASSERT(isImageValid);
      // Create a RasterImageDef and set the image
    // from the Atil image
    AcDbRasterImageDef *pImageDef = new AcDbRasterImageDef();
    Acad::ErrorStatus es = pImageDef->setImage(
                                            pAtilImage, NULL);
      // Insert the RasterImageDef and create a RasterImage
    // using it
    es = InsertImageInDwg(pImageDef);
    if(es != Acad::eOk)
    {
        delete pImageDef;
        return;
    }
      // Cleanup
    DeleteDC(hdcMem);
    ReleaseDC(NULL,hdcScr);
      DeleteObject( bmp);
}
  static Acad::ErrorStatus InsertImageInDwg(
                                AcDbRasterImageDef *pImageDef)
{
    Acad::ErrorStatus es;
    if(! pImageDef->isLoaded())
    {
        es = pImageDef->load();
        if(es != Acad::eOk)
            return es;
    }
      AcApDocument *pActiveDoc = acDocManager->mdiActiveDocument();
    AcDbDatabase *pDB = pActiveDoc->database();
      // Get the image dictionary
    // Create it if not available already
    AcDbObjectId dictID
                    = AcDbRasterImageDef::imageDictionary(pDB);
    if(dictID == AcDbObjectId::kNull)
    {
        es = AcDbRasterImageDef::createImageDictionary(
                                                  pDB, dictID);
        if(es != Acad::eOk)
            return es;
    }
      AcDbDictionary* pDict;
    es = acdbOpenObject(pDict, dictID, AcDb::kForWrite);
    if(es != Acad::eOk)
            return es;
      ACHAR *DICT_NAME = ACRX_T("ISM_RASTER_IMAGE_DICT_VIEW");
    BOOL bExist = pDict->has(DICT_NAME);
    AcDbObjectId objID = AcDbObjectId::kNull;
    if (!bExist)
    {
        es = pDict->setAt(DICT_NAME, pImageDef, objID);
        if(es != Acad::eOk)
            return es;
    }
    else
    {
        pDict->getAt(DICT_NAME,
                    (AcDbObject*&)pImageDef,
                    AcDb::kForWrite);
        objID = pImageDef->objectId();
    }
      // close Dictionary and Definition.
    pDict->close();
    pImageDef->close();
      // Create a raster image using the RasterImage Def
    AcDbRasterImage* pImage = new AcDbRasterImage;
    es = pImage->setImageDefId(objID);
    if (es != Acad::eOk)
    {
        delete pImage;
        return es;
    }
      // Add the raster image to the model space
    AcDbBlockTable* pBlockTable;
    AcDbBlockTableRecord* pBTRecord;
    es = acdbCurDwg()->getBlockTable(pBlockTable,
                                     AcDb::kForRead);
    assert(es == Acad::eOk);
    es = pBlockTable->getAt(ACDB_MODEL_SPACE,
                            pBTRecord,
                            AcDb::kForWrite);
    assert(es == Acad::eOk);
      es = pBTRecord->appendAcDbEntity(pImage);
    assert(es == Acad::eOk);
      pBTRecord->close();
    pBlockTable->close();
      AcDbObjectId entID = pImage->objectId();
      // Set the transparency options
    pImage->setDisplayOpt(    AcDbRasterImage::kTransparent,
                            Adesk::kTrue);
      pImage->setImageTransparency(true);
    pImage->setDisplayOpt(AcDbRasterImage::kShow, Adesk::kTrue);
      AcDbObjectPointer<AcDbRasterImageDefReactor>
                                        rasterImageDefReactor;
    rasterImageDefReactor.create();
      es = rasterImageDefReactor->setOwnerId(pImage->objectId());
    if (es == Acad::eOk)
    {
        AcDbObjectId defReactorId;
        es = curDoc()->database()->addAcDbObject(
                            defReactorId,
                            rasterImageDefReactor.object());
          if (es == Acad::eOk)
        {
            pImage->setReactorId(defReactorId);
            AcDbObjectPointer<AcDbRasterImageDef> rasterImagedef
                      (pImage->imageDefId(), AcDb::kForWrite);
            if (rasterImagedef.openStatus() == Acad::eOk)
            {
                rasterImagedef->addPersistentReactor
                                               (defReactorId);
            }
        }
    }
      pImageDef->close();
    pImage->close();
}

## 评论

**内容**: Youssef Zniber said...
Good day Sir,
I have a large raster image(10000*10000px) attached to a drawing, that I want to crop multiples times automatically. I read in the documentation that I have to use RasterImagDef.OpenImage() witch returns an IntPtr to an Atil ::Image class, I searched all over the internet for days for some clues on how to work with the Atil library in C#, I write in C# by the way, C++ exceeds my abilities.
Do you have any idea on how to that Sir?
Any help would be greatly appreciated.
Reply
11/30/2013 at 03:28 PM

---
**内容**: Balaji said in reply to Youssef Zniber...
Hi Youssef,
Good day to you too.
ATIL is a C++ library and I do not find a way to use it to crop images using C#.
It would be much easier to retrieve the path of the raster image file and crop it using the image processing capabilities provided by .Net. The cropped image file can then be used to modify the RasterImageDef.
The other way could be to save the ATIL image to disk using C++. Your C# code can do the cropping and use the cropped image to redefine the RasterImageDef.
Regards,
Balaji
Reply
12/01/2013 at 02:57 AM

---
**内容**: Youssef Zniber said in reply to Balaji...
Hi Mr. Balaji,
Thank you for taking the time to answer.
The problem is not the cropping, it's that I can't load the image into memory because it is so large (10000*10000px). When I try to do so, I get a runtime out of memory exception. the only way I can access the image is through autocad using the Atil library.
I'll try to write the code with c++, create a dll, and then call it from c#.
Regards,
Youssef
Reply
12/01/2013 at 10:12 AM

---
**内容**: Joao said...
Hi Balaji
I have tried to run your example as a command on Autocad 2015 (Windows 7, 64-bit), but it throws an exception at the line below:
Atil::Image *pAtilImage = new Atil::Image(...)
The exception details and stack trace only point to TiledImage::construct, no further help here.
Any idea what could be causing that?
Regards,
Joao
Reply
09/12/2014 at 11:40 AM

---
**内容**: Joao said in reply to Joao...
Sorry, I forgot to mention the exception type:
Atil::ImageConstructionException
Also, my png image has 640x640 pixels.
Reply
09/12/2014 at 11:45 AM

---
**内容**: Balaji said in reply to Joao...
Hi Joao,
Sorry for the delay. We had a App hackathon last week and did not find time to investigate this issue.
AutoCAD 2015 seems very particular about the type of the initial image, while the previous versions were ok with it. Changing initialImage.type to "Atil::DataModelAttributes::kBgra" resolves the issue.
Regards,
Balaji
Reply
09/24/2014 at 01:28 AM

---
**内容**: Jürgen Maier said...
Hello Balaji,
Thanks for sharing this awesome code.
Just trying this in AutoCAD 2015 and have issues at the point where you add pImageDef to the Dictionary.
es = pDict->setAt(DICT_NAME, pImageDef, objID);
It returns error code 409 (NoClassID).
I have exactly copied your source and double checked but don't see any writing mistake. Also set initalImage.type to Atil::DataModelAttributes::kBgra as you mentioned in your last post.
Would it be possible to give me just a little hint where or what to check to get this solved or where the issue could be?
Thanks in advance for any reply
Jürgen
Reply
06/30/2015 at 08:35 AM

---
**内容**: Balaji said...
Hi Jürgen,
Please try including this in the "On_kInitAppMsg" method :
acrxDynamicLinker->loadModule
(L"acismobj20.dbx",true);
Regards,
Balaji
Reply
06/30/2015 at 10:57 PM

---
**内容**: Jürgen Maier said...
Hi Balaji,
Thanks for your fast reply - it works now! However I added it not to "On_kInitAppMsg" yet but directly in InsertImageInDWG - just for now and testing.
BUT I have another problem now. When I save and close the drawing and reopen it - the picture is there but not shown. It's just showing the border of the picture.
Any idea how this could happen! Sorry for bothering you again.

Warmest regards
Jürge
Reply
07/01/2015 at 04:11 AM

---
**内容**: Balaji said...
Hi Jürgen,
That is because the raster image definition does not write the image data to the drawing file when saved. At present, it only stores the file path if that was used to create the definition.
Here is another blog post that should help overcome it :
http://adndevblog.typepad.com/autocad/2015/04/embedding-an-image-in-a-drawing.html
It relies on a custom object to do the file save.
Regards,
Balaji
Reply
07/01/2015 at 09:10 PM

---
**内容**: Jürgen Maier said...
Hello Balaji,
Again - thank you so much for your quick and good help!
Kind regards from Germany
Jürgen
Reply
07/02/2015 at 12:52 AM

---
**内容**: Fred Senior said...
Deal Balaji Ramamoorthy, really appreciate you code above, but I meet a problem using it.
My Autocad crash when creating a new Atil::Image, my code is as follow:
--------------------------------------------------------
Atil::Image* pAtilImage = NULL;
Atil::ImagePixel initialImage;
initialImage.setToZero();
initialImage.type = Atil::DataModelAttributes::kBgra;
initialImage.value.rgba = 0xff000000;
Atil::Size size(1, 1);
const Atil::RgbModel *pDm = new Atil::RgbModel(Atil::RgbModelAttributes::k4Channels,
Atil::DataModelAttributes::kBlueGreenRedAlpha);
pAtilImage = new Atil::Image(size, pDm, initialImage);
-------------------------------------------------------
Autocad will crash at line new Atil::Image. Even I set size to (0,0), it crash too.
But, I can create an Atil::Image using its defult construction function as follow:
-------------------------------
pAtilImage = new Atil::Image();
-------------------------------
Program works ok this time, but the image size is (0,0), this doesn’t meet my requirement.
My environment is win7 + vs2010 + autocad 2013.
Have you any ideal about this? Really appreciate your response!
Reply
12/07/2015 at 12:03 AM

---
**内容**: Fred Senior said in reply to Fred Senior...
sorry to interrupt you Balaji, my problem solved by changing kBgra to kRgba, really appreciate your answer above, thanks!
Reply
12/07/2015 at 04:38 AM

---
**内容**: Balaji said...
Hi Fred,
Thanks for the update.
Glad you resolved the issue on your own.
Regards,
Balaji
Reply
12/07/2015 at 04:53 AM

---
