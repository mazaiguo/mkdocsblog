---
title: 使用七牛云api下载图片
date: 2025-09-23
categories:
  - windows程序
tags:
  - python
description: 使用Python和ezdxf库将DWG文件转换为SVG格式的详细实现方法
author: JerryMa

---

# 使用七牛云api下载图片

## 先安装七牛云sdk

```bash
pip install qiniu
```



```bash
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
pathlib2>=2.3.7; python_version < '3.4'
```

## 修改config数据为个人数据

??? success

     ```python
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
    
        """
        使用七牛云API获取文件列表并下载图片文件
    
        这是推荐的方式，比解析HTML页面更可靠
        需要七牛云的AccessKey和SecretKey
        """
    
        import os
        import sys
        import time
        import requests
        from pathlib import Path
        from urllib.parse import urljoin
    
        try:
            from qiniu import Auth, BucketManager
            QINIU_SDK_AVAILABLE = True
        except ImportError:
            QINIU_SDK_AVAILABLE = False
            print("警告：未安装qiniu SDK，请运行: pip install qiniu")
    
        class QiniuAPIDownloader:
            def __init__(self, access_key, secret_key, bucket_name, download_dir="downloaded_images"):
                """
                初始化七牛云API下载器
    
                Args:
                    access_key: 七牛云AccessKey
                    secret_key: 七牛云SecretKey  
                    bucket_name: bucket名称
                    download_dir: 本地下载目录
                """
                self.access_key = access_key
                self.secret_key = secret_key
                self.bucket_name = bucket_name
                self.download_dir = Path(download_dir)
    
                # 支持的图片格式
                self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif'}
    
                # 创建下载目录
                self.download_dir.mkdir(parents=True, exist_ok=True)
    
                # 初始化七牛云认证
                if QINIU_SDK_AVAILABLE:
                    self.auth = Auth(access_key, secret_key)
                    self.bucket_manager = BucketManager(self.auth)
                else:
                    self.auth = None
                    self.bucket_manager = None
    
            def get_file_list(self, prefix="", limit=1000):
                """
                获取bucket中的文件列表
    
                Args:
                    prefix: 文件前缀过滤
                    limit: 获取文件数量限制
    
                Returns:
                    list: 文件信息列表
                """
                if not QINIU_SDK_AVAILABLE:
                    print("错误：需要安装qiniu SDK")
                    return []
    
                try:
                    print(f"正在获取bucket '{self.bucket_name}' 中的文件列表...")
                    if prefix:
                        print(f"前缀过滤: {prefix}")
    
                    all_files = []
                    marker = None
    
                    while True:
                        ret, eof, info = self.bucket_manager.list(
                            self.bucket_name, 
                            prefix=prefix, 
                            marker=marker,
                            limit=limit
                        )
    
                        if ret is None:
                            print(f"获取文件列表失败: {info}")
                            break
    
                        files = ret.get('items', [])
                        all_files.extend(files)
    
                        if eof:
                            break
    
                        marker = ret.get('marker')
    
                    print(f"找到 {len(all_files)} 个文件")
                    return all_files
    
                except Exception as e:
                    print(f"获取文件列表失败: {e}")
                    return []
    
            def filter_image_files(self, file_list):
                """
                筛选出图片文件
    
                Args:
                    file_list: 文件信息列表
    
                Returns:
                    list: 图片文件信息列表
                """
                image_files = []
    
                for file_info in file_list:
                    filename = file_info.get('key', '')
                    file_ext = Path(filename).suffix.lower()
    
                    if file_ext in self.image_extensions:
                        image_files.append(file_info)
    
                print(f"筛选出 {len(image_files)} 个图片文件")
                return image_files
    
            def get_download_url(self, filename, domain=None, expires=3600):
                """
                获取文件下载URL
    
                Args:
                    filename: 文件名
                    domain: 绑定的域名，如果为None则使用默认域名
                    expires: URL过期时间（秒）
    
                Returns:
                    str: 下载URL
                """
                if not QINIU_SDK_AVAILABLE:
                    return None
    
                try:
                    if domain:
                        # 使用自定义域名
                        if not domain.startswith('http'):
                            domain = f"http://{domain}"
                        base_url = domain.rstrip('/')
                        download_url = self.auth.private_download_url(f"{base_url}/{filename}", expires=expires)
                    else:
                        # 使用默认域名（需要配置）
                        # 这里需要替换为实际的域名
                        print("警告：未指定下载域名，请提供bucket绑定的域名")
                        return None
    
                    return download_url
    
                except Exception as e:
                    print(f"生成下载URL失败 {filename}: {e}")
                    return None
    
            def download_file(self, file_info, domain=None):
                """
                下载单个文件
    
                Args:
                    file_info: 文件信息字典
                    domain: 下载域名
    
                Returns:
                    bool: 下载是否成功
                """
                filename = file_info.get('key', '')
                filesize = file_info.get('fsize', 0)
    
                try:
                    # 获取下载URL
                    download_url = self.get_download_url(filename, domain)
                    if not download_url:
                        print(f"无法获取下载URL: {filename}")
                        return False
    
                    print(f"正在下载: {filename} ({filesize} bytes)")
    
                    # 下载文件
                    response = requests.get(download_url, stream=True, timeout=60)
                    response.raise_for_status()
    
                    # 创建本地文件路径
                    local_path = self.download_dir / filename
                    local_path.parent.mkdir(parents=True, exist_ok=True)
    
                    # 保存文件
                    with open(local_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
    
                    print(f"下载完成: {local_path}")
                    return True
    
                except Exception as e:
                    print(f"下载失败 {filename}: {e}")
                    return False
    
            def download_images(self, prefix="images/", domain=None):
                """
                下载所有图片文件
    
                Args:
                    prefix: 文件前缀过滤
                    domain: 下载域名
                """
                if not QINIU_SDK_AVAILABLE:
                    print("错误：请安装qiniu SDK: pip install qiniu")
                    return
    
                print("=== 七牛云API图片下载器 ===\n")
    
                # 1. 获取文件列表
                file_list = self.get_file_list(prefix)
                if not file_list:
                    print("未找到任何文件")
                    return
    
                # 2. 筛选图片文件
                image_files = self.filter_image_files(file_list)
                if not image_files:
                    print("未找到图片文件")
                    return
    
                print(f"\n找到的图片文件:")
                for i, file_info in enumerate(image_files, 1):
                    filename = file_info.get('key', '')
                    filesize = file_info.get('fsize', 0)
                    print(f"{i:3d}. {filename} ({filesize} bytes)")
    
                if not domain:
                    print("\n错误：请提供bucket绑定的域名")
                    print("例如: your-bucket.domain.com")
                    return
    
                # 3. 下载文件
                print(f"\n开始下载到: {self.download_dir.absolute()}")
    
                downloaded_count = 0
                failed_count = 0
    
                for file_info in image_files:
                    if self.download_file(file_info, domain):
                        downloaded_count += 1
                    else:
                        failed_count += 1
    
                    # 添加延迟避免请求过快
                    time.sleep(0.2)
    
                print(f"\n下载总结:")
                print(f"成功下载: {downloaded_count} 个文件")
                print(f"下载失败: {failed_count} 个文件")
                print(f"文件保存在: {self.download_dir.absolute()}")
    
        def main():
            """主函数"""
            print("七牛云API下载器")
            print("=" * 30)
    
            # 配置信息 - 请填入您的七牛云密钥信息
            config = {
                'access_key': '',  # 请填入您的AccessKey
                'secret_key': '',  # 请填入您的SecretKey  
                'bucket_name': '',  # bucket名称
                'prefix': 'images/',  # 文件前缀
                'domain': '',  # 请填入bucket绑定的域名，如: example.com
            }
    
            # 检查配置
            if not config['access_key'] or not config['secret_key']:
                print("请配置七牛云密钥信息:")
                print("1. 登录七牛云控制台")
                print("2. 在个人中心 -> 密钥管理中获取AccessKey和SecretKey")
                print("3. 将密钥信息填入此脚本的config字典中")
                return
    
            if not config['domain']:
                print("请配置bucket的访问域名:")
                print("1. 在七牛云控制台的bucket设置中找到绑定的域名")
                print("2. 将域名填入此脚本的config字典中")
                print("   格式如: example.com 或 cdn.example.com")
                return
    
            # 创建下载器并执行下载
            downloader = QiniuAPIDownloader(
                access_key=config['access_key'],
                secret_key=config['secret_key'], 
                bucket_name=config['bucket_name']
            )
    
            downloader.download_images(
                prefix=config['prefix'],
                domain=config['domain']
            )
    
        if __name__ == "__main__":
            main()
    
     ```





`def main():`函数中config数据根据实际情况填写。