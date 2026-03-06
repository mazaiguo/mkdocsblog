---
title: 飞牛NAS图床搭建指南
date: 2026-03-05
categories:
  - NAS
  - 运维
tags:
  - 飞牛NAS
  - MinIO
  - PicGo
  - Cloudflare Tunnel
  - 图床
description: 使用飞牛NAS + MinIO + PicGo + Cloudflare Tunnel 搭建无公网IP图床的完整操作指南
author: JerryMa
---

# 飞牛 NAS 图床搭建完整指南

**方案架构**

```
PicGo（本地工具）
    ↓ 上传图片
MinIO（运行在飞牛NAS的Docker容器）
    ↓ 存储文件
Cloudflare Tunnel（反向代理，无需公网IP）
    ↓ 暴露服务
https://img.yourdomain.com（外网可访问的图片链接）
```

**前提条件**

- 飞牛 NAS 已开机并可访问外网
- 拥有一个域名（可在 [Cloudflare](https://www.cloudflare.com/) 购买，也可从阿里云/腾讯云等转入）
- 安装了 PicGo（[下载地址](https://github.com/Molunerfinn/PicGo/releases)）

---

## 第一步：将域名托管到 Cloudflare

如果域名在其他服务商（阿里云、腾讯云等），需要将 DNS 解析迁移到 Cloudflare。

**操作步骤**

1. 登录 [Cloudflare 控制台](https://dash.cloudflare.com/) → 注册或登录账号（免费）
2. 点击**添加站点** → 输入你的域名 → 选择 **Free 计划**
3. Cloudflare 会扫描现有 DNS 记录，确认无误后点击**继续**
4. 复制 Cloudflare 提供的**两个 NS 服务器地址**（形如 `xxx.ns.cloudflare.com`）
5. 登录原域名服务商控制台 → **域名管理** → 修改 **NS 服务器**为 Cloudflare 提供的地址
6. 等待 DNS 生效（通常 5 分钟到 1 小时，最长 48 小时）

**验证**：在 Cloudflare 控制台看到域名状态变为**活动中**表示生效成功。

> 如果域名已经在 Cloudflare 托管，直接跳过此步骤。

---

## 第二步：飞牛 NAS 部署 MinIO

MinIO 是兼容 S3 协议的对象存储服务，PicGo 通过 S3 插件连接。

### 创建 Docker Compose 文件

在飞牛 NAS 上，通过文件管理器在合适位置创建目录（如 `/vol1/1000/docker/minio`），然后创建 `docker-compose.yml`：

```yaml
services:
  minio:
    image: minio/minio:latest
    container_name: minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"   # API 端口，PicGo 上传用
      - "9001:9001"   # Web 管理控制台
    volumes:
      - /vol1/1000/minio/data:/data    # 图片存储路径，根据实际调整
    environment:
      MINIO_ROOT_USER: admin            # 管理员账号
      MINIO_ROOT_PASSWORD: 你的密码123  # 至少8位
    restart: unless-stopped
```

在飞牛 NAS 的 Docker 管理界面 → **Compose** → 创建并启动。

### 初始化 MinIO（全部使用命令行，适配新版）

新版 MinIO Docker 镜像（2023+）控制台 UI 精简了部分功能，推荐直接通过命令行完成所有初始化操作，步骤更稳定。

#### 前提：在哪里执行命令？

以下所有 `docker exec` 命令，可以在以下任一位置执行：
- **飞牛 NAS 的 SSH 终端**（推荐）：`ssh root@NAS的IP`，然后执行命令
- **飞牛 NAS 的内置终端**：在飞牛管理界面找到终端工具
- **Portainer 容器控制台**：Portainer → 找到 minio 容器 → **控制台** → 连接

#### 第一步：创建 Bucket（桶）

```bash
# 进入 MinIO 容器内的 shell
docker exec -it minio /bin/sh

# 配置 mc 连接（替换 admin 和 你的密码 为实际值）
mc alias set local http://localhost:9000 admin 你的密码

# 创建 images 桶
mc mb local/images

# 退出容器
exit
```

#### 第二步：设置桶为公开只读

```bash
# 设置 images 桶允许匿名访问（公开读）
docker exec -it minio mc alias set local http://localhost:9000 admin 你的密码
docker exec -it minio mc anonymous set public local/images

# 验证设置（应输出 public）
docker exec -it minio mc anonymous get local/images
```

#### 第三步：创建 Access Key 和 Secret Key

新版 MinIO UI 中 Access Keys 可能需要通过**服务账户**创建，命令行更可靠：

```bash
# 为 admin 用户创建一个服务账户（即 Access Key / Secret Key 对）
docker exec -it minio mc admin user svcacct add local admin
```

**输出示例**：

```
Access Key: ********
Secret Key: ********
Expiration: no-expiry
```

**务必立即保存这两个值**，Secret Key 只显示一次，之后无法再查看。

> 如果 UI 中确实能找到 **Access Keys** 入口（左侧菜单或账户设置），也可在 UI 中创建，效果相同。

---

## 第三步：创建 Cloudflare Tunnel

### 进入 Zero Trust 控制台

1. 在 Cloudflare 控制台，选择你的域名
2. 左侧菜单 → **Zero Trust**（首次进入需填写团队名称，随意填写）
3. 左侧**网络** → **隧道** → **创建隧道**

### 创建 Tunnel

1. 连接器类型选择 **Cloudflared** → 点击**下一步**
2. 输入隧道名称（如 `fnnas`）→ **保存隧道**
3. 在**安装并运行连接器**页面，选择 **Docker**
4. 复制显示的命令中的**令牌**（`--token` 后面那一长串字符），保存备用

   Token 形如：`eyJhIjoiYTNjMGMxY...`（很长的字符串）

---

## 第四步：飞牛 NAS 运行 cloudflared

在飞牛 NAS 上部署 cloudflared 容器。

创建 `docker-compose.yml`：

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    restart: unless-stopped
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=粘贴你的Token到这里
```

启动容器后，回到 Cloudflare 控制台，隧道状态变为**正常运行**（绿色）表示连接成功。

---

## 第五步：配置公开主机名（路由规则）

告诉 Cloudflare，访问哪个域名时转发到 NAS 上的哪个服务。

1. 在隧道详情页，点击**公共主机名**标签
2. 点击**添加公共主机名**
3. 填写路由规则：

**MinIO 图床路由（必须）**

| 配置项 | 填写值 |
|---|---|
| Subdomain | `img` |
| Domain | `yourdomain.com` |
| Type | `HTTP` |
| URL | `NAS内网IP:9000` |

保存后，`https://img.yourdomain.com` 即可访问 MinIO API。

**可选：飞牛 NAS 管理界面路由**

| 配置项 | 填写值 |
|---|---|
| Subdomain | `nas` |
| Domain | `yourdomain.com` |
| Type | `HTTPS` |
| URL | `NAS内网IP:5001` |
| 勾选 | **禁用 TLS 验证**（飞牛默认自签名证书） |

---

## 第六步：配置 PicGo

### 安装 S3 插件

1. 打开 PicGo → **插件设置** → 搜索 `s3`
2. 安装 **`picgo-plugin-s3`** 插件

### 配置 S3 图床

在 **图床设置** → **Amazon S3** 中填写：

| 配置项 | 填写值 | 说明 |
|---|---|---|
| 应用密钥ID | 你的 Access Key | MinIO 创建的 Key |
| 应用密钥 | 你的 Secret Key | MinIO 创建的 Secret |
| 存储桶名称 | `images` | MinIO 中创建的桶名 |
| 文件路径 | `{year}/{month}/{fileName}.{extName}` | 按年月分类存储 |
| 自定义节点(内网) | `http://NAS内网IP:9000` | NAS 内部 API 端口 |
| 自定义节点(外网) | `https://img.yourdomain.com` | Cloudflare 外网域名 |
| 存储区域 | `us-east-1` | 随便填，MinIO 不校验 |
| 路径样式 | 勾选（Endpoint路径样式） | MinIO 必须勾选 |

点击 **确定** → 设为默认图床。

### 测试上传

**方式一**：直接拖拽图片到 PicGo 上传区域

**方式二**：截图后使用快捷键上传（PicGo 设置中可配置快捷键，如 `Ctrl+Shift+P`）

上传成功后，PicGo 会自动复制 Markdown 格式的图片链接到剪贴板：

```markdown
![图片名称](https://img.yourdomain.com/images/2026/03/screenshot.png)
```

---

## 第七步：配合 Typora/Obsidian 使用

### Typora 配置

1. **文件** → **偏好设置** → **图像**
2. 插入图片时选择 **上传图片**
3. 上传服务选择 **PicGo(app)**
4. 设置 PicGo 的路径

配置后，在 Typora 中粘贴图片时自动上传到图床并替换为外网链接。

### Obsidian 配置

安装 **Image Auto Upload Plugin** 插件 → 设置 PicGo 服务器地址为 `http://127.0.0.1:36677`（PicGo 的上传服务端口）。

---

## 常见问题

### 上传失败：Connection refused

- 检查 MinIO 容器是否正常运行：`http://NAS_IP:9001` 能否访问
- 检查 PicGo 中自定义节点是否填写正确（注意是内网 IP）

### 图片链接无法访问（403 Forbidden / Access Denied）

- 检查 Cloudflare 隧道状态是否为**正常运行**
- 检查 MinIO Bucket 是否设置为公开：

  ```bash
  docker exec -it minio mc anonymous get local/images
  ```

  如果输出 `private`，执行以下命令修复：

  ```bash
  docker exec -it minio mc alias set local http://localhost:9000 admin 你的密码
  docker exec -it minio mc anonymous set public local/images
  ```

- 检查路由规则中的 URL 是否正确

### Cloudflare Tunnel 连接不上

- 确认飞牛 NAS 能访问外网（可 ping cloudflare.com 测试）
- 确认 Token 粘贴完整，没有多余空格

### cloudflared 容器提示自签名证书错误

如果访问飞牛 NAS 服务时出现证书问题，在路由规则中勾选**禁用 TLS 验证**。

---

## 扩展：多服务统一访问

一个 Cloudflare Tunnel 可以配置多个路由，所有服务都通过同一个 cloudflared 容器转发：

| 外网域名 | 内网地址 | 用途 |
|---|---|---|
| `img.yourdomain.com` | `NAS_IP:9000` | MinIO 图床 |
| `nas.yourdomain.com` | `NAS_IP:5001` | 飞牛管理界面 |
| `portainer.yourdomain.com` | `NAS_IP:9443` | Docker 管理 |
| `code.yourdomain.com` | `NAS_IP:8443` | VS Code Server |

全部配置完成后，在任何地方通过域名即可安全访问 NAS 的各项服务，**无需公网 IP，无需端口转发，自动 HTTPS**。

---

> 文档生成时间：2026-03-05
> 适用版本：MinIO RELEASE.2025+、PicGo 2.4+、cloudflared 2025+
