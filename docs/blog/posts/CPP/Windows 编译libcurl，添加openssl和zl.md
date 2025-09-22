---
title: Windows 编译libcurl，添加openssl和zlib支持
date: 2023-07-12
categories:
  - windows程序
tags:
  - LIBCURL
  - OpenSSL
  - CPP
description: Windows平台下编译libcurl库并添加OpenSSL和zlib支持的详细步骤
author: JerryMa
---

# Windows 编译libcurl，添加openssl和zlib支持

## 编译zlib

https://zlib.net/

[下载地址](https://zlib.net/zlib1213.zip)

### 编译win32

#### 使用CMake编译程序

![img](https://raw.githubusercontent.com/mazaiguo/blogimg/main/20230712220029.png)

#### 选中zlibstatic项目，构建zlib的静态库。（win32 release）

在E:\Gitee\Tool\zlib-1.2.13\build\Release下生成了`zlibstaticd.lib`文件，修改名为`zlib.lib`。

将`zlib.h`、`zconf.h`文件复制到`E:\Gitee\Tool\include`目录下

### 编译x64

E:\Gitee\Tool\include\zlib ├─x64 │ ├─include │ │ zconf.h │ │ zlib.h │ └─lib │ zlib.lib └─x86 ├─include │ zconf.h │ zlib.h └─lib zlib.lib

## 编译openssl

- [perl下载地址](https://platform.activestate.com/JerryMa/ActivePerl-5.28?cli-instructions=windows)
- [下载strawberry perl](https://strawberryperl.com/releases.html)，可以选择ZIP edition版，解压即可用，免安装。
- **[下载5.16.3,这版本有完整的信息，不需要从网上再下，国内下载太慢了](http://dl.softmgr.qq.com/original/Development/ActivePerl-5.16.3.1604-MSWin32-x64-298023.msi)**
- 下载[openssl源码](https://github.com/openssl/openssl.git)
- 一份给x86用，一份给x64用，两份代码目录不同，不然编译的时候会冲突

编译步骤：

```cpp
1.安装ActivePerl-5.16.3.1604-MSWin32-x64-298023.msi
2.下载openssl  https://www.openssl.org/source/，解压，如：E:\GDAL\openssl
3.打开Developer Command Prompt for VS2015命令行工具，cd进入E:\GDAL\openssl
4.perl Configure VC-WIN64A no-asm no-shared --prefix=E:\GDAL\dev           
（可选项：VC-WIN32 | VC-WIN64A | VC-WIN64I | VC-CE，--prefix是最终拷贝的目录；添加no-shared参数可生成静态库）
（VC-WIN32生成32位的，VC-WIN64A生成64位）
5.nmake 
6.nmake test #很慢，可选
7.nmake install
```

CPP

### 打开`x86 Native Tools Command Prompt for VS 2017`工具，切换到openssl源码目录

- `perl Configure VC-WIN64A --release no-asm no-shared --prefix="E:\Gitee\Tool\include\openssl\x86"`
- nmake
- nmake install
- 新建安装目录`E:\Gitee\Tool\include\openssl\x86`。

![img](https://raw.githubusercontent.com/mazaiguo/blogimg/main/20230712225249.png)

### 打开`x64 Native Tools Command Prompt for VS 2017`工具，切换到openssl源码目录

- 新建安装目录`E:\Gitee\Tool\include\openssl\x64`。
- `perl Configure VC-WIN64A --release no-asm no-shared --prefix="E:\Gitee\Tool\include\openssl\x64"`
- nmake
- nmake install
- 与X86操作类似，不再演示

## 编译libcurl

### 编译32位

打开`x86 Native Tools Command Prompt for VS 2017`工具，切换到`E:\Gitee\Tool\curl\winbuild`目录。

==问题==

```
NMAKE : fatal error U1073: 不知道如何生成“..\src\tool_hugehelp.c”
```

回退到目录:`E:\Gitee\Tool\curl`，运行buildconf.bat

![img](https://raw.githubusercontent.com/mazaiguo/blogimg/main/20230713091745.png)

```
nmake /f Makefile.vc mode=static VC=15 MACHINE=x86 DEBUG=no WITH_SSL=static WITH_ZLIB=static WITH_PREFIX=E:\Gitee\Tool\include\curl\x86\ SSL_PATH=E:\Gitee\Tool\include\openssl\x86\ ZLIB_PATH=E:\Gitee\Tool\include\zlib\x86\
```

选项说明：

- `mode=<static/dll>`：编译静态/动态库
- `VC=<10/11/12/14/15/16>`：VisualStudio版本
- `MACHINE=<x86/x64>`：生成32/64位库
- `DEBUG=<yes/no>`：生成debug/release版本
- `WITH_SSL=<static/dll>`：openssl的库类型
- `WITH_ZLIB=<static/dll>`：zlib的库类型
- `WITH_PREFIX=<path>`：编译结果输出路径。必须以反斜杠\结尾
- `SSL_PATH=<path>`：openssl路径
- `ZLIB_PATH=<path>`：zlib路径

| VC版本 | _MSC_VER宏的值                | VS版本 | MSVC toolset version |
| :----- | :---------------------------- | :----- | :------------------- |
| VC6.0  | 1200                          | VS 6.0 |                      |
| VC7.0  | 1300                          | VS2002 |                      |
| VC7.1  | 1310                          | VS2003 |                      |
| VC8.0  | 1400                          | VS2005 | 80                   |
| VC9.0  | 1500                          | VS2008 | 90                   |
| VC10.0 | 1600                          | VS2010 | 100                  |
| VC11.0 | 1700                          | VS2012 | 110                  |
| VC12.0 | 1800                          | VS2013 | 120                  |
| VC14.0 | 1900                          | VS2015 | 140                  |
| VC15.0 | [ 1910 , 1916 ]               | VS2017 | 141                  |
| VC16.0 | [ 1920 , 1929 ] [][1920,1929] | VS2019 | 142                  |
| VC17.0 | [1930,)                       | VS2022 | 143                  |

### 编译64

打开`x64 Native Tools Command Prompt for VS 2017`工具，切换到`E:\Gitee\Tool\curl\winbuild`目录。

==问题==

```
NMAKE : fatal error U1073: 不知道如何生成“..\src\tool_hugehelp.c”
```

回退到目录:`E:\Gitee\Tool\curl`

![img](https://raw.githubusercontent.com/mazaiguo/blogimg/main/20230713091745.png)

```
nmake /f Makefile.vc mode=static VC=15 MACHINE=x64 DEBUG=no WITH_SSL=static WITH_ZLIB=static WITH_PREFIX=E:\Gitee\Tool\include\curl\x64\ SSL_PATH=E:\Gitee\Tool\include\openssl\x64\ ZLIB_PATH=E:\Gitee\Tool\include\zlib\x64\
```

## 合并多个库

代码中使用[libcurl](https://github.com/curl/curl.git)库，编译的时候，需要同时链接`libcurl.lib`，`zlib.lib`，`libssl.lib`，`libcrypto.lib`4个库。

可以将这4个库文件合并为1个`libcurl.lib`。

### 编译32位

新建文件夹`E:\Gitee\Tool\include\curl\x86\lib_merge`。

打开x86 Native Tools Command Prompt for VS 2017工具，切换到`E:\Gitee\Tool\include\curl\x86\lib_merge`目录。

```
lib.exe E:\Gitee\Tool\include\curl\x86\lib\libcurl_a.lib E:\Gitee\Tool\include\openssl\x86\lib\libcrypto.lib E:\Gitee\Tool\include\openssl\x86\lib\libssl.lib E:\Gitee\Tool\include\zlib\x86\lib\zlib.lib   /out:E:\Gitee\Tool\include\curl\x86\lib_merge\libcurl.lib
```

### 编译64位

新建文件夹`E:\Gitee\Tool\include\curl\x64\lib_merge`。

打开`x64 Native Tools Command Prompt for VS 2017`工具，切换到`E:\Gitee\Tool\include\curl\x64\lib_merge`目录。

```
lib.exe E:\Gitee\Tool\include\curl\x64\lib\libcurl_a.lib E:\Gitee\Tool\include\openssl\x64\lib\libcrypto.lib E:\Gitee\Tool\include\openssl\x64\lib\libssl.lib E:\Gitee\Tool\include\zlib\x64\lib\zlib.lib   /out:E:\Gitee\Tool\include\curl\x64\lib_merge\libcurl.lib
```

## 测试代码

```
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include <curl/curl.h>


struct memory {
    char* response;
    size_t size;
};

static size_t callback(void *data, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct memory *mem = (struct memory *)userp;

    char *ptr = (char*)realloc((void*)mem->response, mem->size + realsize + 1);
    if(ptr == NULL) {
        return 0;  /* out of memory! */
    }

    mem->response = ptr;
    memcpy(&(mem->response[mem->size]), data, realsize);
    mem->size += realsize;
    mem->response[mem->size] = '\0';

    return realsize;
}

int main() {
    /* 1. 初始化 */
    CURL* curl = curl_easy_init();
    if (!curl) {
        printf("curl_easy_init failed\n");
        return 1;
    }

    struct memory chunk = {0};
    chunk.response = NULL;
    chunk.size = 0;

    /* 2. 发送请求 */
    curl_easy_setopt(curl, CURLOPT_URL, "https://www.baidu.com");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&chunk);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYSTATUS, 0L);
    curl_easy_perform(curl);

    /* 3. 查看请求返回结果 */
    printf("%s\n", chunk.response);

    /* 4. 清理 */
    if (chunk.response) {
        free(chunk.response);
        chunk.response = NULL;
        chunk.size = 0;
    }
    curl_easy_cleanup(curl);
    curl = NULL;

    return 0;
}
```

添加如下lib

- ws2_32.lib
- wldap32.lib
- crypt32.lib
- Normaliz.lib
- –
- libcurl.lib （如果已经合并，就不需要下面3个了）
- libcrypto.lib
- libssl.lib
- zlib.lib 编译运行程序，输出百度首页的html说明测试通过。 ———————————————— 版权声明：本文为CSDN博主「Leopard-C」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。 原文链接：https://blog.csdn.net/weixin_41701847/article/details/131300414

## 问题

### 问题一

```
error LNK2001: 无法解析的外部符号 __imp__curl_easy_setopt
error LNK2001: 无法解析的外部符号 __imp__curl_easy_init
error LNK2001: 无法解析的外部符号 __imp__curl_easy_cleanup
error LNK2001: 无法解析的外部符号 __imp__curl_slist_append
error LNK2001: 无法解析的外部符号 __imp__curl_slist_free_all
error LNK2001: 无法解析的外部符号 __imp__curl_easy_strerror
error LNK2001: 无法解析的外部符号 __imp__curl_easy_perform
error LNK2001: 无法解析的外部符号 __imp__curl_easy_getinfo
```

- 通过在测试程序的“CPP ---> 预处理”中增加 BUILDING_LIBCURL（或者CURL_STATICLIB），问题得以解决。

### 问题二

```
libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_init referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_unbind_s referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_set_option referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_simple_bind_s referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_search_s referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_msgfree referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_err2string referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_first_entry referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_next_entry referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_first_attribute referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_next_attribute referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_get_values_len referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_value_free_len referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_get_dn referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ldap_memfree referenced in function __ldap_free_urldesc
1>libcurl.lib(ldap.obj) : error LNK2019: unresolved external symbol __imp__ber_free referenced in function __ldap_free_urldesc
```

需要添加Ws2_32.lib和Wldap32.lib。

### 问题3

```
error LNK2019: 无法解析的外部符号 __imp__IdnToAscii
```

需要添加Normaliz.lib

### 问题4

```
无法解析的外部符号 __imp_CertOpenStore解决方案
```

在 项目属性 - 链接器 - 输入 - 附加依赖项 中加入： Crypt32.lib

[参考](https://blog.csdn.net/weixin_41701847/article/details/131300414)

[How to Build OpenSSL, zlib, and cURL libraries on Windows](https://developers.refinitiv.com/en/article-catalog/article/how-to-build-openssl--zlib--and-curl-libraries-on-windows)https://developers.refinitiv.com/en/article-catalog/article/how-to-build-openssl--zlib--and-curl-libraries-on-windows)