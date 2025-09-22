---
title: WPF中读取DWG显示图片
date: 2024-10-08
categories:
  - windows程序
tags:
  - WPF
  - DWG
  - 图像处理
  - CAD显示
description: 在WPF应用中读取DWG文件并转换为图片显示的实现方法
author: JerryMa
---

# wpf中读取dwg显示图片

## [Csharp预览DWG文件方法（一）直接读取文件结构](https://www.cnblogs.com/cadlife/articles/2246257.html)

要在WPF中读取DWG文件并将其转换为Bitmap，可以使用一些第三方库来解析DWG文件，然后将其内容绘制到Bitmap上。以下是一个基本的步骤概述：

1. **使用第三方库解析DWG文件**：
   - 例如，您可以使用Teigha或Aspose.CAD等库来读取DWG文件。
2. **将DWG内容绘制到Bitmap**：
   - 使用解析库提供的绘图功能，将DWG文件的内容绘制到Bitmap对象上。
3. **将Bitmap转换为WPF中的ImageSource**：
   - 使用`System.Windows.Interop.Imaging.CreateBitmapSourceFromHBitmap`方法将Bitmap转换为ImageSource，以便在WPF中显示。

以下是一个示例代码，展示了如何将Bitmap转换为ImageSource：

用如下方式使用，有部分图纸显示有问题

`ImageSource img = BitmapToImageSource(ShowDWG(128, 128, file.FullName))`

```csharp
using System; using System.Drawing; 
using System.Windows; 
using System.Windows.Media; 
using System.Windows.Media.Imaging;
using System.Windows.Interop; 

 struct BITMAPFILEHEADER
        {
            public short bfType;
            public int bfSize;
            public short bfReserved1;
            public short bfReserved2;
            public int bfOffBits;
        }
        public static System.Drawing.Image GetDwgImage(string FileName)
        {
            if (!(File.Exists(FileName)))
            {
                throw new FileNotFoundException("文件没有被找到");
            }

            FileStream DwgF = null;   //文件流
            int PosSentinel;   //文件描述块的位置
            BinaryReader br = null;   //读取二进制文件
            int TypePreview;   //缩略图格式
            int PosBMP;    //缩略图位置 
            int LenBMP;    //缩略图大小
            short biBitCount; //缩略图比特深度 
            BITMAPFILEHEADER biH; //BMP文件头，DWG文件中不包含位图文件头，要自行加上去
            byte[] BMPInfo;    //包含在DWG文件中的BMP文件体
            MemoryStream BMPF = new MemoryStream(); //保存位图的内存文件流
            BinaryWriter bmpr = new BinaryWriter(BMPF); //写二进制文件类
            System.Drawing.Image myImg = null;
            try
            {

                DwgF = new FileStream(FileName, FileMode.Open, FileAccess.Read); //文件流

                br = new BinaryReader(DwgF);
                DwgF.Seek(13, SeekOrigin.Begin); //从第十三字节开始读取
                PosSentinel = br.ReadInt32();   //第13到17字节指示缩略图描述块的位置
                DwgF.Seek(PosSentinel + 30, SeekOrigin.Begin);   //将指针移到缩略图描述块的第31字节
                TypePreview = br.ReadByte();   //第31字节为缩略图格式信息，2 为BMP格式，3为WMF格式
                if (TypePreview == 1)
                {
                }
                else if (TypePreview == 2 || TypePreview == 3)
                {
                    PosBMP = br.ReadInt32(); //DWG文件保存的位图所在位置
                    LenBMP = br.ReadInt32(); //位图的大小
                    DwgF.Seek(PosBMP + 14, SeekOrigin.Begin); //移动指针到位图块
                    biBitCount = br.ReadInt16(); //读取比特深度
                    DwgF.Seek(PosBMP, SeekOrigin.Begin); //从位图块开始处读取全部位图内容备用
                    BMPInfo = br.ReadBytes(LenBMP); //不包含文件头的位图信息
                    br.Close();
                    DwgF.Close();
                    biH.bfType = 19778; //建立位图文件头
                    if (biBitCount < 9)
                    {
                        biH.bfSize = 54 + 4 * (int)(Math.Pow(2, biBitCount)) + LenBMP;
                    }
                    else
                    {
                        biH.bfSize = 54 + LenBMP;
                    }
                    biH.bfReserved1 = 0; //保留字节
                    biH.bfReserved2 = 0; //保留字节
                    biH.bfOffBits = 14 + 40 + 1024; //图像数据偏移
                                                    //以下开始写入位图文件头
                    bmpr.Write(biH.bfType); //文件类型
                    bmpr.Write(biH.bfSize);   //文件大小
                    bmpr.Write(biH.bfReserved1); //0
                    bmpr.Write(biH.bfReserved2); //0
                    bmpr.Write(biH.bfOffBits); //图像数据偏移
                    bmpr.Write(BMPInfo); //写入位图
                    BMPF.Seek(0, SeekOrigin.Begin); //指针移到文件开始处 
                    myImg = System.Drawing.Image.FromStream(BMPF); //创建位图文件对象                    
                    bmpr.Close();
                    BMPF.Close();
                }
                return myImg;
            }
            catch (EndOfStreamException)
            {
                throw new EndOfStreamException("文件不是标准的DWG格式文件，无法预览！");
            }
            catch (IOException ex)
            {
                if (ex.Message == "试图将文件指针移到文件开头之前。/r/n")
                {
                    throw new IOException("文件不是标准的DWG格式文件，无法预览！");
                }
                else if (ex.Message == "文件“" + FileName + "”正由另一进程使用，因此该进程无法访问该文件。")
                {
                    //复制文件，继续预览
                    //File.Copy(FileName, System.Windows.Forms.Application.StartupPath + @"/linshi.dwg", true);
                    //System.Drawing.Image image = GetDwgImage(Application.StartupPath + @"/linshi.dwg");
                    //File.Delete(Application.StartupPath + @"/linshi.dwg");
                    //return image;
                    throw new IOException("文件“" + FileName + "”正由另一进程使用，因此该进程无法访问该文件。");
                }
                else
                {
                    throw new Exception(ex.Message);
                }
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
            finally
            {
                if (DwgF != null)
                {
                    DwgF.Close();
                }
                if (br != null)
                {
                    br.Close();
                }
                bmpr.Close();
                BMPF.Close();

            }
        }



        ///读取出来的背景色为白色，效果比较差，很多颜色显示不出来，当时认为显示DWG文件出错误了，问了些高手，（呵呵，别人告诉自己本身取出的就是白色背景，需要自己改变背景色，在此鄙视一下自己）所以继续用C#操作返回的IMAGE对象，改变背景色
        ///<summary>
        ///显示DWG文件
        ///</summary>
        ///<param name="Pwidth">要显示的宽度</param>
        ///<param name="PHeight">要显示的高度</param>
        ///<returns></returns>
        public static System.Drawing.Image ShowDWG(int Pwidth, int PHeight, string FilePath)
        {
            System.Drawing.Image image = GetDwgImage(FilePath);
            Bitmap bitmap = new Bitmap(image);
            int Height = bitmap.Height;
            int Width = bitmap.Width;
            Bitmap newbitmap = new Bitmap(Width, Height);
            Bitmap oldbitmap = (Bitmap)bitmap;
            System.Drawing.Color pixel;
            for (int x = 1; x < Width; x++)
            {
                for (int y = 1; y < Height; y++)
                {

                    pixel = oldbitmap.GetPixel(x, y);
                    int r = pixel.R, g = pixel.G, b = pixel.B;
                    if (pixel.Name == "ffffffff" || pixel.Name == "ff000000")
                    {
                        r = 255 - pixel.R;
                        g = 255 - pixel.G;
                        b = 255 - pixel.B;
                    }

                    newbitmap.SetPixel(x, y, Color.FromArgb(r, g, b));
                }
            }
            Bitmap bt = new Bitmap(newbitmap, Pwidth, PHeight);

            return newbitmap;
        }
		/// <summary>
        /// Bitmap转ImageSource
        /// </summary>
        /// <param name="hObject"></param>
        /// <returns></returns>
        [DllImport("gdi32.dll", SetLastError = true)]
        private static extern bool DeleteObject(IntPtr hObject);
        public static ImageSource ToImageSource( Bitmap bitmap)
        {
            IntPtr hBitmap = bitmap.GetHbitmap();
            ImageSource wpfBitmap = Imaging.CreateBitmapSourceFromHBitmap(hBitmap, IntPtr.Zero, Int32Rect.Empty, BitmapSizeOptions.FromEmptyOptions());
            // 记得要进行内存释放。否则会有内存不足的报错。
            if (!DeleteObject(hBitmap))
            {
                throw new Win32Exception();
            }
            return wpfBitmap;
        }

        public static ImageSource BitmapToImageSource(System.Drawing.Image processImage)
        {
            Bitmap bmp = new Bitmap(processImage);
            IntPtr hBitmap = bmp.GetHbitmap();
            ImageSource wpfBitmap = Imaging.CreateBitmapSourceFromHBitmap(hBitmap, IntPtr.Zero, Int32Rect.Empty, BitmapSizeOptions.FromEmptyOptions());
            return wpfBitmap;
        }
```



​              

## 可以直接使用Database.ThumbnailBitmap接口来处理

```csharp
 [System.Runtime.InteropServices.DllImport("gdi32.dll", SetLastError = true)]
        private static extern bool DeleteObject(IntPtr hObject);
        public static ImageSource ToImageSource(System.Drawing.Bitmap bitmap)
        {
            IntPtr hBitmap = bitmap.GetHbitmap();
            ImageSource wpfBitmap = Imaging.CreateBitmapSourceFromHBitmap(hBitmap, IntPtr.Zero, Int32Rect.Empty, BitmapSizeOptions.FromEmptyOptions());
            // 记得要进行内存释放。否则会有内存不足的报错。
            if (!DeleteObject(hBitmap))
            {
                throw new Win32Exception();
            }
            return wpfBitmap;
        }
        public static System.Drawing.Bitmap GetDwgImage(string fileName)
        {
            System.Drawing.Bitmap outBM = null;
            ZwSoft.ZwCAD.DatabaseServices.Database sourceDb = new ZwSoft.ZwCAD.DatabaseServices.Database(false, true);
            try
            {
                //把DWG文件读入到一个临时的数据库中
                if (File.Exists(fileName))
                {
                    sourceDb.ReadDwgFile(fileName, FileShare.Read, false, String.Empty);
                    outBM = sourceDb.ThumbnailBitmap;
                }
            }
            catch (ZwSoft.ZwCAD.Runtime.Exception ex)
            {
                ZwSoft.ZwCAD.ApplicationServices.Application.ShowAlertDialog("复制错误: " + ex.Message);
            }
            //操作完成，销毁源数据库
            sourceDb.Dispose();
            return outBM;
        }

        ///读取出来的背景色为白色，效果比较差，很多颜色显示不出来，当时认为显示DWG文件出错误了，问了些高手，（呵呵，别人告诉自己本身取出的就是白色背景，需要自己改变背景色，在此鄙视一下自己）所以继续用C#操作返回的IMAGE对象，改变背景色
        ///<summary>
        ///显示DWG文件
        ///</summary>
        ///<param name="Pwidth">要显示的宽度</param>
        ///<param name="PHeight">要显示的高度</param>
        ///<returns></returns>
        public static System.Drawing.Bitmap ShowDWG(int Pwidth, int PHeight, string FilePath)
        {
            System.Drawing.Bitmap bitmap = GetDwgImage(FilePath);
            int Height = bitmap.Height;
            int Width = bitmap.Width;
            System.Drawing.Bitmap newbitmap = new System.Drawing.Bitmap(Width, Height);
            System.Drawing.Bitmap oldbitmap = (System.Drawing.Bitmap)bitmap;
            System.Drawing.Color pixel;
            for (int x = 1; x < Width; x++)
            {
                for (int y = 1; y < Height; y++)
                {

                    pixel = oldbitmap.GetPixel(x, y);
                    int r = pixel.R, g = pixel.G, b = pixel.B;
                    if (pixel.Name == "ffffffff" || pixel.Name == "ff000000")
                    {
                        r = 255 - pixel.R;
                        g = 255 - pixel.G;
                        b = 255 - pixel.B;
                    }

                    newbitmap.SetPixel(x, y, System.Drawing.Color.FromArgb(r, g, b));
                }
            }
            System.Drawing.Bitmap bt = new System.Drawing.Bitmap(newbitmap, Pwidth, PHeight);

            return newbitmap;
        }
```

效果不好，还是直接选用读取bmp文件的方式来处理。