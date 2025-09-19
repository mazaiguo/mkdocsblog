---
title: yaml-cpp读写yml文件
date: 2025-09-18
categories:
  - CPP
  - 开发工具
tags:
  - cpp
  - yaml-cpp
  - 文件操作
  - 配置文件
description: 使用yaml-cpp库在CPP中读写YAML配置文件的完整指南，包括编译配置和UTF-8字符处理
authors:
  - JerryMa
---



# yaml-cpp读写yml文件

## 代码处理

### 下载地址

[Github](https://github.com/jbeder/yaml-cpp)

主干版rebase到`Tag`0.8.0

### 编译版本

创建一个build文件夹，使用默认配置

![image-20241227155336653](http://image.jerryma.xyz//images/20241227-image-20241227155336653.png)

Debug编译debug版本

Release编译Release版本

使用的时候预处理器中需要填入`YAML_CPP_STATIC_DEFINE`

## 读写yaml文件

### UTF-8 和 `CString` 之间的转换函数

你可以定义一些辅助函数，用于在 UTF-8 和 `CString`（UTF-16）之间进行转换：

```cpp
#include <atlstr.h> // CString
#include <string>

// UTF-8 -> CString (UTF-16)
CString Utf8ToCString(const std::string& utf8Str) {
    int wideLength = MultiByteToWideChar(CP_UTF8, 0, utf8Str.c_str(), -1, nullptr, 0);
    CString wideStr;
    MultiByteToWideChar(CP_UTF8, 0, utf8Str.c_str(), -1, wideStr.GetBuffer(wideLength), wideLength);
    wideStr.ReleaseBuffer();
    return wideStr;
}

// CString (UTF-16) -> UTF-8
std::string CStringToUtf8(const CString& cstr) {
    int utf8Length = WideCharToMultiByte(CP_UTF8, 0, cstr, -1, nullptr, 0, nullptr, nullptr);
    std::string utf8Str(utf8Length, 0);
    WideCharToMultiByte(CP_UTF8, 0, cstr, -1, &utf8Str[0], utf8Length, nullptr, nullptr);
    return utf8Str;
}
```

###  读取 YAML 文件支持 `CString`

使用 `yaml-cpp` 读取 YAML 文件时，将读取的 UTF-8 字符串转换为 `CString`：

```cpp
#include <iostream>
#include <yaml-cpp/yaml.h>
#include <atlstr.h> // CString

// 上述 Utf8ToCString 和 CStringToUtf8 函数应定义在此

int main() {
    try {
        // 加载 YAML 文件
        YAML::Node config = YAML::LoadFile("config.yaml");

        // 读取 UTF-8 编码的字符串，并转换为 CString
        CString name = Utf8ToCString(config["name"].as<std::string>());
        CString description = Utf8ToCString(config["description"].as<std::string>());

        std::wcout << L"Name: " << name.GetString() << std::endl;
        std::wcout << L"Description: " << description.GetString() << std::endl;
    } catch (const YAML::Exception& e) {
        std::cerr << "Error reading YAML file: " << e.what() << std::endl;
    }

    return 0;
}
```

###  写入 YAML 文件支持 `CString`

在写入 YAML 文件时，将 `CString` 转换为 UTF-8：

```cpp
#include <iostream>
#include <yaml-cpp/yaml.h>
#include <atlstr.h> // CString

// 上述 Utf8ToCString 和 CStringToUtf8 函数应定义在此

int main() {
    try {
        YAML::Node config;

        // 设置 CString 内容并转换为 UTF-8
        CString name = _T("小明");
        CString description = _T("这是一个包含 Unicode 字符的 YAML 文件。");

        config["name"] = CStringToUtf8(name);
        config["description"] = CStringToUtf8(description);

        // 写入 YAML 文件
        std::ofstream fout("output.yaml");
        fout << config;
        fout.close();

        std::wcout << L"YAML file written successfully!" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error writing YAML file: " << e.what() << std::endl;
    }

    return 0;
}
```