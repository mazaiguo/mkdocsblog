---
title: 处理dimstyle相关功能，包括读取，创建，保存
date: 2024-04-08
categories:
  - CAD开发
  - ObjectARX
  - CPP
tags:
  - ObjectARX
  - DimStyle
  - CAD标注
  - AutoCAD
description: ObjectARX中处理标注样式的各种操作，包括读取、创建和保存功能
author: JerryMa
---

			strOutPut.Format(_T("\n\"setDimalttd\":%d,"), pRecord->dimalttd());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimatfit\":%d,"), pRecord->dimatfit());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimaunit\":%d,"), pRecord->dimaunit());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimazin\":%d,"), pRecord->dimazin());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimdec\":%d,"), pRecord->dimdec());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimfrac\":%d,"), pRecord->dimfrac());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtad\":%d,"), pRecord->dimtad());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtdec\":%d,"), pRecord->dimtdec());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtmove\":%d,"), pRecord->dimtmove());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtolj\":%d,"), pRecord->dimtolj());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtzin\":%d,"), pRecord->dimtzin());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimzin\":%d,"), pRecord->dimzin());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimadec\":%d,"), pRecord->dimadec());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimalttz\":%d,"), pRecord->dimalttz());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimaltu\":%d,"), pRecord->dimaltu());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimaltz\":%d,"), pRecord->dimaltz());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimarcsym\":%d,"), pRecord->dimarcsym());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimjust\":%d,"), pRecord->dimjust());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimlunit\":%d,"), pRecord->dimlunit());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtfill\":%d,"), pRecord->dimtfill());
			tmpVec.push_back(strOutPut);
			// bool
			tmpVec.push_back(_T("\nbool-------------------------------"));
			strOutPut.Format(_T("\n\"setDimtih\":%d,"), pRecord->dimtih());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtix\":%d,"), pRecord->dimtix());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtofl\":%d,"), pRecord->dimtofl());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtoh\":%d,"), pRecord->dimtoh());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtol\":%d,"), pRecord->dimtol());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimupt\":%d,"), pRecord->dimupt());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimalt\":%d,"), pRecord->dimalt());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimlim\":%d,"), pRecord->dimlim());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimsah\":%d,"), pRecord->dimsah());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimsd1\":%d,"), pRecord->dimsd1());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimsd2\":%d,"), pRecord->dimsd2());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimse1\":%d,"), pRecord->dimse1());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimse2\":%d,"), pRecord->dimse2());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimsoxd\":%d,"), pRecord->dimsoxd());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimfxlenOn\":%d,"), pRecord->dimfxlenOn());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtxtdirection\":%d,"), pRecord->dimtxtdirection());
			tmpVec.push_back(strOutPut);
	
			tmpVec.push_back(_T("\ndouble-------------------------------"));
			//double
			strOutPut.Format(_T("\n\"setDimlfac\":%f,"), pRecord->dimlfac());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimaltf\":%f,"), pRecord->dimaltf());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimaltrnd\":%f,"), pRecord->dimaltrnd());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimasz\":%f,"), pRecord->dimasz());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimcen\":%f,"), pRecord->dimcen());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtp\":%f,"), pRecord->dimtp());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtsz\":%f,"), pRecord->dimtsz());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtvp\":%f,"), pRecord->dimtvp());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtxt\":%f,"), pRecord->dimtxt());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimdle\":%f,"), pRecord->dimdle());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimdli\":%f,"), pRecord->dimdli());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimexe\":%f,"), pRecord->dimexe());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimexo\":%f,"), pRecord->dimexo());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimgap\":%f,"), pRecord->dimgap());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtm\":%f,"), pRecord->dimtm());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimjogang\":%f,"), pRecord->dimjogang());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimrnd\":%f,"), pRecord->dimrnd());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimscale\":%f,"), pRecord->dimscale());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimtfac\":%f,"), pRecord->dimtfac());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimfxlen\":%f,"), pRecord->dimfxlen());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimmzf\":%f,"), pRecord->dimmzf());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimaltmzf\":%f,"), pRecord->dimaltmzf());
			tmpVec.push_back(strOutPut);
	
			/*strOutPut.Format(_T("\n\"setDimapost\":%s,"), pRecord->dimapost());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimmzs\":%s,"), pRecord->dimmzs());
## ��ӡ��ǰdimstyleid��Ӧ����Ϣ

```cpp
AcDbObjectId             styleId = acdbCurDwg()->dimstyle();
		if (acdbOpenObject((AcDbObject *&)pRecord, styleId, AcDb::kForRead) != Acad::eOk)
		{
			return;
		}
		acutPrintf(_T("\ndimadec:%d"), pRecord->dimadec());
		acutPrintf(_T("\ndimalt:%d"), pRecord->dimalt());
		acutPrintf(_T("\ndimaltd:%d"), pRecord->dimaltd());
		acutPrintf(_T("\ndimaltf:%f"), pRecord->dimaltf());
		acutPrintf(_T("\ndimclrd:%d"), pRecord->dimclrd().colorIndex());
		acutPrintf(_T("\ndimclre:%d"), pRecord->dimclre().colorIndex());
		acutPrintf(_T("\ndimclrt:%d"), pRecord->dimclrt().colorIndex());
		acutPrintf(_T("\ndimaltrnd:%f"), pRecord->dimaltrnd());
		acutPrintf(_T("\ndimalttd:%d"), pRecord->dimalttd());
		acutPrintf(_T("\ndimalttz:%d"), pRecord->dimalttz());
		acutPrintf(_T("\ndimaltu:%d"), pRecord->dimaltu());
		acutPrintf(_T("\ndimaltz:%d"), pRecord->dimaltz());
		acutPrintf(_T("\ndimarcsym:%d"), pRecord->dimarcsym());
		acutPrintf(_T("\ndimasz:%f"), pRecord->dimasz());
		acutPrintf(_T("\ndimatfit:%d"), pRecord->dimatfit());
		acutPrintf(_T("\ndimaunit:%d"), pRecord->dimaunit());
		acutPrintf(_T("\ndimazin:%d"), pRecord->dimazin());
		acutPrintf(_T("\ndimcen:%f"), pRecord->dimcen());
		acutPrintf(_T("\ndimdec:%d"), pRecord->dimdec());
		acutPrintf(_T("\ndimdle:%f"), pRecord->dimdle());
		acutPrintf(_T("\ndimdli:%f"), pRecord->dimdli());
		acutPrintf(_T("\ndimexe:%f"), pRecord->dimexe());
		acutPrintf(_T("\ndimexo:%f"), pRecord->dimexo());
		acutPrintf(_T("\ndimfrac:%d"), pRecord->dimfrac());
		acutPrintf(_T("\ndimgap:%f"), pRecord->dimgap());
		acutPrintf(_T("\ndimjogang:%f"), pRecord->dimjogang());
		acutPrintf(_T("\ndimjust:%d"), pRecord->dimjust());
		acutPrintf(_T("\ndimlim:%d"), pRecord->dimlim());
		acutPrintf(_T("\ndimlunit:%d"), pRecord->dimlunit());
		acutPrintf(_T("\ndimrnd:%f"), pRecord->dimrnd());
		acutPrintf(_T("\ndimsah:%d"), pRecord->dimsah());
		acutPrintf(_T("\ndimscale:%f"), pRecord->dimscale());
		acutPrintf(_T("\ndimsd1:%d"), pRecord->dimsd1());
		acutPrintf(_T("\ndimsd2:%d"), pRecord->dimsd2());
		acutPrintf(_T("\ndimse1:%d"), pRecord->dimse1());
		acutPrintf(_T("\ndimse2:%d"), pRecord->dimse2());
		acutPrintf(_T("\ndimsoxd:%d"), pRecord->dimsoxd());
		acutPrintf(_T("\ndimtad:%d"), pRecord->dimtad());
		acutPrintf(_T("\ndimtdec:%d"), pRecord->dimtdec());
		acutPrintf(_T("\ndimtfac:%f"), pRecord->dimtfac());
		acutPrintf(_T("\ndimtfill:%d"), pRecord->dimtfill());
		acutPrintf(_T("\ndimtih:%d"), pRecord->dimtih());
		acutPrintf(_T("\ndimtix:%d"), pRecord->dimtix());
		acutPrintf(_T("\ndimtm:%f"), pRecord->dimtm());
		acutPrintf(_T("\ndimtmove:%d"), pRecord->dimtmove());
		acutPrintf(_T("\ndimtofl:%d"), pRecord->dimtofl());
		acutPrintf(_T("\ndimtoh:%d"), pRecord->dimtoh());
		acutPrintf(_T("\ndimtol:%d"), pRecord->dimtol());
		acutPrintf(_T("\ndimtolj:%d"), pRecord->dimtolj());
		acutPrintf(_T("\ndimtp:%f"), pRecord->dimtp());
		acutPrintf(_T("\ndimtsz:%f"), pRecord->dimtsz());
		acutPrintf(_T("\ndimtvp:%f"), pRecord->dimtvp());
		acutPrintf(_T("\ndimtxt:%f"), pRecord->dimtxt());
		acutPrintf(_T("\ndimtzin:%d"), pRecord->dimtzin());
		acutPrintf(_T("\ndimupt:%d"), pRecord->dimupt());
		acutPrintf(_T("\ndimzin:%d"), pRecord->dimzin());
		acutPrintf(_T("\ndimfxlenOn:%d"), pRecord->dimfxlenOn());
		acutPrintf(_T("\ndimfxlen:%f"), pRecord->dimfxlen());
		acutPrintf(_T("\ndimtxtdirection:%d"), pRecord->dimtxtdirection());
		acutPrintf(_T("\ndimmzf:%f"), pRecord->dimmzf());
		acutPrintf(_T("\ndimaltmzf:%f"), pRecord->dimaltmzf());
		acutPrintf(_T("\ndimapost:%s"), pRecord->dimapost());
		acutPrintf(_T("\ndimdsep:%s"), pRecord->dimdsep());
		acutPrintf(_T("\ndimmzs:%s"), pRecord->dimmzs());
		acutPrintf(_T("\ndimaltmzs:%s"), pRecord->dimaltmzs());

		pRecord->close();
```

## ����ǰ�ĵ������еı�ע��ʽ��Ϣ����

### ����λ�õ��ļ���

```cpp
CString strFileName = CUtility::GetAppPath() + _T("\\dim\\") + strLayerName + _T(".md");
```

```cpp
CString strFailPath = CUtility::GetAppPath() + _T("\\dim\\");
if (!PathIsDirectory(strFailPath))
{
    CUtility::MakeDirectory(strFailPath);
}
```

```cpp
BOOL CUtility::MakeDirectory(CString dd)
{
	HANDLE	fFile;	// File Handle
	WIN32_FIND_DATA	fileinfo;	// File Information Structure
	CStringArray	m_arr;	// CString Array to hold Directory Structures

	int x1 = 0;	// Counter
	CString tem = _T("");	// Temporary CString Object

	fFile = FindFirstFile(dd, &fileinfo);

	// if the file exists and it is a directory
	if (fileinfo.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY)
	{
		//  Directory Exists close file and return
		FindClose(fFile);
		return FALSE;
	}
	m_arr.RemoveAll();

	// Parse the supplied CString Directory String
	for (x1 = 0; x1 < dd.GetLength(); x1++)	// Parse the supplied CString Directory String
	{
		if (dd.GetAt(x1) != _T('\\'))	// if the Charachter is not a \ 
			tem += dd.GetAt(x1);	// add the character to the Temp String
		else
		{
			m_arr.Add(tem);	// if the Character is a \ 
			tem += _T("\\");	// Now add the \ to the temp string
		}
		if (x1 == dd.GetLength() - 1)	// If we reached the end of the String
			m_arr.Add(tem);
	}

	// Close the file
	FindClose(fFile);

	// Now lets cycle through the String Array and create each directory in turn
	for (x1 = 1; x1 < m_arr.GetSize(); x1++)
	{
		tem = m_arr.GetAt(x1);
		BOOL tt = CreateDirectory(tem, NULL);// BOOL used to test if Create Directory was successful

		// If the Directory exists it will return a false
		if (tt)
			SetFileAttributes(tem, FILE_ATTRIBUTE_NORMAL);
		// If we were successful we set the attributes to normal
	}
	//  Now lets see if the directory was successfully created
	fFile = FindFirstFile(dd, &fileinfo);

	m_arr.RemoveAll();
	if (fileinfo.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY)
	{
		//  Directory Exists close file and return
		FindClose(fFile);
		return TRUE;
	}
	else
	{
		// For Some reason the Function Failed  Return FALSE
		FindClose(fFile);
		return FALSE;
	}
	return TRUE;
}
```



### ����ĵ����������£�

```cpp
	static void MyGroupTEST()
	{
		AcDbDimStyleTable *pStyleTable = nullptr;
		if (acdbCurDwg()->getDimStyleTable(pStyleTable, AcDb::kForRead) != Acad::eOk)
		{
			return;
		}

		AcDbDimStyleTableIterator *pItr = nullptr;
		pStyleTable->newIterator(pItr);
		AcDbDimStyleTableRecord *pRecord = nullptr;

		vector<CString> tmpVec;
		for (pItr->start(); !pItr->done(); pItr->step())
		{
			tmpVec.clear();
			Acad::ErrorStatus es = pItr->getRecord(pRecord, AcDb::kForRead);
			if (es != Acad::eOk)
			{
				return;
			}
			TCHAR *layerName = NULL;
			pRecord->getName(layerName);
			CString strLayerName;
			strLayerName = layerName;
			acutDelString(layerName);
			CString strOutPut;
			strOutPut.Format(_T("\n\"setDimclrd\":%d,"), pRecord->dimclrd().colorIndex());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimclre\":%d,"), pRecord->dimclre().colorIndex());
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimclrt\":%d,"), pRecord->dimclrt().colorIndex());
			tmpVec.push_back(strOutPut);
			tmpVec.push_back(_T("\nint-------------------------------"));
			strOutPut.Format(_T("\n\"setDimaltd\":%d,"), pRecord->dimaltd());
			tmpVec.push_back(strOutPut);
			tmpVec.push_back(strOutPut);
			strOutPut.Format(_T("\n\"setDimaltmzs\":%s,"), pRecord->dimaltmzs());
			tmpVec.push_back(strOutPut);*/
			pRecord->close();

			CStdioFile file;
			CString    strFileName = CUtility::GetAppPath() + _T("\\dim\\") + strLayerName + _T(".md");
			if (!file.Open(strFileName, CFile::modeCreate | CFile::modeReadWrite | CFile::typeText))
			{
				return;
			}
			for (auto iter : tmpVec)
			{
				file.WriteString(iter);
			}
			file.Close();
		}
		delete pItr;
		pStyleTable->close();
	}
```

## ������׼��ʽ

```cpp
AcDbObjectId CGetDimStyleInfoFromJson::getDimStyleIdByName(CString strName)
{
	AcDbDimStyleTable *pTable = nullptr;
	if (acdbCurDwg()->getDimStyleTable(pTable, AcDb::kForWrite) != Acad::eOk)
		return AcDbObjectId::kNull;

	AcDbDimStyleTableRecord *pRecord = nullptr;
	Acad::ErrorStatus        es;
	if (!pTable->has(strName)) //�����û����
	{
		//����һ��
		pRecord = new AcDbDimStyleTableRecord();
		pRecord->setName(strName);

		//��json�л�ȡ����
		getInfoFromJsonKeyName(strName);
		AcCmColor color;
		color.setColorIndex(m_nDimclrd);
		pRecord->setDimclrd(color);
		color.setColorIndex(m_nDimclre);
		pRecord->setDimclre(color);
		color.setColorIndex(m_nDimclrt);
		pRecord->setDimclrt(color);

		pRecord->setDimaltd(m_nDimaltd);
		pRecord->setDimalttd(m_nDimalttd);
		pRecord->setDimatfit(m_nDimatfit);
		pRecord->setDimaunit(m_nDimaunit);
		pRecord->setDimazin(m_nDimazin);
		pRecord->setDimdec(m_nDimdec);
		pRecord->setDimfrac(m_nDimfrac);
		pRecord->setDimtad(m_nDimtad);
		pRecord->setDimtdec(m_nDimtdec);
		pRecord->setDimtmove(m_nDimtmove);
		pRecord->setDimtolj(m_nDimtolj);
		pRecord->setDimtzin(m_nDimtzin);
		pRecord->setDimzin(m_nDimzin);
		pRecord->setDimadec(m_nDimadec);
		pRecord->setDimalttz(m_nDimalttz);
		pRecord->setDimaltu(m_nDimaltu);
		pRecord->setDimaltz(m_nDimaltz);
		pRecord->setDimarcsym(m_nDimarcsym);
		pRecord->setDimjust(m_nDimjust);
		pRecord->setDimlunit(m_nDimlunit);
		pRecord->setDimtfill(m_nDimtfill);

		pRecord->setDimtih(m_bDimtih);
		pRecord->setDimtix(m_bDimtix);
		pRecord->setDimtofl(m_bDimtofl);
		pRecord->setDimtoh(m_bDimtoh);
		pRecord->setDimtol(m_bDimtol);
		pRecord->setDimupt(m_bDimupt);
		pRecord->setDimalt(m_bDimalt);
		pRecord->setDimlim(m_bDimlim);
		pRecord->setDimsah(m_bDimsah);
		pRecord->setDimsd1(m_bDimsd1);
		pRecord->setDimsd2(m_bDimsd2);
		pRecord->setDimse1(m_bDimse1);
		pRecord->setDimse2(m_bDimse2);
		pRecord->setDimsoxd(m_bDimsoxd);
		pRecord->setDimfxlenOn(m_bDimfxlenOn);
		pRecord->setDimtxtdirection(m_bDimtxtdirection);

		pRecord->setDimlfac(m_dDimlfac);
		pRecord->setDimaltf(m_dDimaltf);
		pRecord->setDimaltrnd(m_dDimaltrnd);
		pRecord->setDimasz(m_dDimasz);
		pRecord->setDimcen(m_dDimcen);
		pRecord->setDimtp(m_dDimtp);
		pRecord->setDimtsz(m_dDimtsz);
		pRecord->setDimtvp(m_dDimtvp);
		pRecord->setDimtxt(m_dDimtxt);
		pRecord->setDimdle(m_dDimdle);
		pRecord->setDimdli(m_dDimdli);
		pRecord->setDimexe(m_dDimexe);
		pRecord->setDimexo(m_dDimexo);
		pRecord->setDimgap(m_dDimgap);
		pRecord->setDimtm(m_dDimtm);
		pRecord->setDimjogang(m_dDimjogang);
		pRecord->setDimrnd(m_dDimrnd);
		pRecord->setDimscale(m_dDimscale);
		pRecord->setDimtfac(m_dDimtfac);
		pRecord->setDimfxlen(m_dDimfxlen);
		pRecord->setDimmzf(m_dDimmzf);
		pRecord->setDimaltmzf(m_dDimaltmzf);

		pTable->add(pRecord);
		pRecord->close();
	}
	pTable->close();
	acdbCurDwg()->getDimStyleTable(pTable, AcDb::kForRead);
	AcDbObjectId DimstyleId;
	pTable->getAt(strName, DimstyleId);
	pTable->close();
	return DimstyleId;
}
```


