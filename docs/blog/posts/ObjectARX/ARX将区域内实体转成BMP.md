---
title: ARX将区域内实体转成BMP
date: 2024-02-25
categories:
  - windows程序
tags:
  - ObjectARX
  - BMP
description: ObjectARX中将选定区域内的CAD实体转换为BMP图像文件的完整实现
author: JerryMa
---

# ARX将区域内实体转成BMP

```cpp
static void MyGroupTEST()
{
    //框选区域
    AcGePoint3d pt1, pt2;
    if (RTNORM != acedGetPoint(NULL, _T("\n第一角点"), asDblArray(pt1)))
        return;
    if (RTNORM != acedGetCorner(asDblArray(pt1), _T("\n第二角点"), asDblArray(pt2)))
        return;
    //用户坐标系转世界坐标系
    pt1 = TransformPoint(pt1, 1, 0);
    pt2 = TransformPoint(pt2, 1, 0);

    //pt1 = PublicFunction::TransUcs2Wcs(pt1);
    //pt2 = PublicFunction::TransUcs2Wcs(pt2);
    ads_name sset;
    if (RTNORM != acedSSGet(_T("W"), p1, p2, NULL, sset))
    {
        return;
    }
    Adesk::Int32 sslen;
    acedSSLength(sset, &sslen);
    ads_name ename;
    AcDbObjectId entId = AcDbObjectId::kNull;
    AcDbObjectIdArray idArray;
    idArray.removeAll();
    for (int i=0; i<sslen; i++)
    {
        acedSSName(sset, i, ename);
        acdbGetObjectId(entId, ename);
        idArray.append(entId);
    }

    ads_ssfree(sset);
    if (idArray.isEmpty())
        return;
    //bmp
    POINT cp1 = GetPointInAcadCoordinate(pt1);
    POINT cp2 = GetPointInAcadCoordinate(pt2);
    if (cp1.x > cp2.x)
        std::swap(cp1, cp2);
    WriteToBmp(cp1, cp2);
    //wblock
    AcDbDatabase* pShortCutDwg = NULL;
    acdbCurDwg()->wblock(pShortCutDwg, idArray, AcGePoint3d(0.0, 0.0, 0.0));
    pShortCutDwg->saveAs(_T("D:\\a.dwg"));
    delete pShortCutDwg;
    pShortCutDwg = NULL;

}
```

工具代码：

```cpp
AcGePoint3d TransformPoint(const AcGePoint3d &point, int nFromType, int nToType)
{
	AcGePoint3d pt;
	//从ucs转到wcs
	struct resbuf rbFrom, rbTo;
	rbFrom.restype = RTSHORT;
	rbFrom.resval.rint = nFromType; // from wcs
	rbTo.restype = RTSHORT;
	rbTo.resval.rint = nToType;     // from ucs
	acedTrans(asDblArray(point), &rbFrom, &rbTo, Adesk::kFalse, asDblArray(pt));
	return pt;
}

POINT GetPointInAcadCoordinate(const AcGePoint3d &pt)
{
	ads_point pnt;
	ads_point_set(asDblArray(pt), pnt);
	//获取视口编号
	int wndNum = 0;
	struct resbuf v;
	if (acedGetVar(_T("cvport"), &v) == RTNORM)
	{
		wndNum = v.resval.rint;
	}
	//将pt坐标转为pixel屏幕坐标
	CPoint ptInScreen;
	acedCoordFromWorldToPixel(wndNum, pnt, ptInScreen);
	//将ptInScreen转为在view上的点p3
	POINT p3;
	p3.x = ptInScreen.x; p3.y = ptInScreen.y;
	::ClientToScreen(acedGetAcadDwgView()->m_hWnd, &p3);
	return p3;
}

void WriteToBmp(const POINT& pt1, const POINT& pt2)
{
	//获得屏幕的HWND
	HWND hWnd = ::GetDesktopWindow();
	//获得屏幕的HDC
	HDC hScreenDC = ::GetDC(hWnd);
	HDC MemDC = ::CreateCompatibleDC(hScreenDC);
	RECT rect;
	::GetWindowRect(hWnd, &rect);
	SIZE screensize;
	screensize.cx = abs(pt1.x - pt2.x);
	screensize.cy = abs(pt1.y - pt2.y);
	HBITMAP hBitmap = ::CreateCompatibleBitmap(hScreenDC, screensize.cx, screensize.cy);
	HGDIOBJ hOldBMP = ::SelectObject(MemDC, hBitmap);
	::BitBlt(MemDC, 0, 0, screensize.cx, screensize.cy, hScreenDC, pt1.x, pt1.y, SRCCOPY);
	::SelectObject(MemDC, hOldBMP);
	::DeleteObject(MemDC);
	::ReleaseDC(hWnd, hScreenDC);

	HDC hDC = ::CreateDC(_T("DISPLAY"), NULL, NULL, NULL);
	//当前分辨率下每个像素所占字节数
	int iBits = ::GetDeviceCaps(hDC, BITSPIXEL) * ::GetDeviceCaps(hDC, PLANES);
	::DeleteDC(hDC);
	//位图中每个像素所占字节数
	WORD wBitCount;
	if (iBits <= 1)
		wBitCount = 1;
	else if (iBits <= 4)
		wBitCount = 4;
	else if (iBits <= 8)
		wBitCount = 8;
	else if (iBits <= 24)
		wBitCount = 24;
	else
		wBitCount = iBits;
	//调色板大小， 位图中像素字节大小 
	DWORD dwPaletteSize = 0;
	if (wBitCount <= 8)
		dwPaletteSize = (1 << wBitCount) * sizeof(RGBQUAD);

	//位图属性结构
	BITMAP bm;
	::GetObject(hBitmap, sizeof(bm), (LPSTR)&bm);

	//位图信息头结构
	BITMAPINFOHEADER bi;
	bi.biSize = sizeof(BITMAPINFOHEADER);
	bi.biWidth = bm.bmWidth;
	bi.biHeight = bm.bmHeight;
	bi.biPlanes = 1;
	bi.biBitCount = wBitCount;
	//BI_RGB表示位图没有压缩
	bi.biCompression = BI_RGB;
	bi.biSizeImage = 0;
	bi.biXPelsPerMeter = 0;
	bi.biYPelsPerMeter = 0;
	bi.biClrUsed = 0;
	bi.biClrImportant = 0;

	DWORD dwBmBitsSize = ((bm.bmWidth * wBitCount + 31) / 32) * 4 * bm.bmHeight;
	//为位图内容分配内存
	HANDLE hDib = ::GlobalAlloc(GHND, dwBmBitsSize + dwPaletteSize + sizeof(BITMAPINFOHEADER));
	LPBITMAPINFOHEADER lpbi = (LPBITMAPINFOHEADER)GlobalLock(hDib);
	*lpbi = bi;
	// 处理调色板 
	HANDLE hPal = ::GetStockObject(DEFAULT_PALETTE);
	HANDLE  hOldPal = NULL;
	if (hPal)
	{
		hDC = ::GetDC(NULL);
		hOldPal = SelectPalette(hDC, (HPALETTE)hPal, FALSE);
		RealizePalette(hDC);
	}
	// 获取该调色板下新的像素值
	::GetDIBits(hDC, hBitmap, 0, (UINT)bm.bmHeight, (LPSTR)lpbi + sizeof(BITMAPINFOHEADER) + dwPaletteSize, (BITMAPINFO*)lpbi, DIB_RGB_COLORS);
	//恢复调色板
	if (hOldPal)
	{
		SelectPalette(hDC, (HPALETTE)hOldPal, TRUE);
		RealizePalette(hDC);
		::ReleaseDC(NULL, hDC);
	}
	//位图文件头结构
	BITMAPFILEHEADER bmfHdr;
	// "BM"
	bmfHdr.bfType = 0x4D42;
	// 设置位图文件头
	DWORD dwDIBSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + dwPaletteSize + dwBmBitsSize;
	bmfHdr.bfSize = dwDIBSize;
	bmfHdr.bfReserved1 = 0;
	bmfHdr.bfReserved2 = 0;
	bmfHdr.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER) + dwPaletteSize;
	//创建位图文件
	HANDLE hFile = CreateFile(_T("D:\\a.bmp"), GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL | FILE_FLAG_SEQUENTIAL_SCAN, NULL);
	DWORD dwWritten;
	// 写入位图文件头
	WriteFile(hFile, (LPSTR)&bmfHdr, sizeof(BITMAPFILEHEADER), &dwWritten, NULL);
	// 写入位图文件其余内容
	WriteFile(hFile, (LPSTR)lpbi, dwDIBSize, &dwWritten, NULL);
	//清除
	GlobalUnlock(hDib);
	GlobalFree(hDib);
	CloseHandle(hFile);
}
```

