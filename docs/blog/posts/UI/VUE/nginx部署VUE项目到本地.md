---
title: Nginx部署VUE项目到本地
date: 2023-12-08
categories:
  - Web部署
  - 前端开发
tags:
  - Nginx
  - Vue
description: 使用Nginx在本地部署Vue项目的详细配置步骤和注意事项
author: JerryMa
---

# Nginx部署VUE项目到本地

## 下载nginx

下载链接：http://nginx.org/en/download.html

随便找一个，目前安装的是1.16.1

![](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/8_10_26_17_20231208-20231208102616.png)

## 修改nginx配置

进入`nginx的 conf/nginx.conf`

修改Location的值，设为vue的路径

![](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/8_10_27_52_20231208-20231208102751.png)

## 新建bat脚本，本地启动服务

```bash
@echo off
start /d "D:\Program Files\Redis-x64-5.0.14.1" redis-server.exe
start /d "E:\Gitee\JAVA\Project\myblog\BlogWeb\target" java -jar BlogWeb-1.0-SNAPSHOT.jar
start /d "E:\download\nginx-1.16.1\nginx-1.16.1" nginx.exe
pause
```




