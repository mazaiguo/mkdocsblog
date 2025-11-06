---
title: Vue应用部署指南 
date: 2025-11-06
categories:
  - Tools
  - deploy
  - VUE
tags:
  - VUE
description: Vue静态页面网上部署
author: JerryMa

---

# Vue应用部署指南 🚀

## 免费托管平台推荐

### 1. Vercel ⭐⭐⭐⭐⭐（强烈推荐）

**优点**：
- ✅ 完全免费
- ✅ 自动HTTPS
- ✅ 全球CDN加速
- ✅ 支持自定义域名
- ✅ 与GitHub集成（自动部署）
- ✅ 构建速度快

**使用步骤**：

#### 方法A：通过GitHub（推荐）

1. **创建GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **登录Vercel**
   - 访问 https://vercel.com
   - 使用GitHub账号登录

3. **导入项目**
   - 点击"Add New" → "Project"
   - 选择你的GitHub仓库
   - Vercel会自动检测Vue项目

4. **配置构建**
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

5. **部署**
   - 点击"Deploy"
   - 等待构建完成
   - 获得免费域名：`your-project.vercel.app`

#### 方法B：通过Vercel CLI

```bash
# 安装Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
vercel

# 生产环境部署
vercel --prod
```

**更新**：每次push到GitHub，Vercel会自动重新部署

---

### 2. Netlify ⭐⭐⭐⭐⭐

**优点**：
- ✅ 完全免费
- ✅ 自动HTTPS
- ✅ 全球CDN
- ✅ 自定义域名
- ✅ 表单处理功能

**使用步骤**：

1. **登录Netlify**
   - 访问 https://www.netlify.com
   - 使用GitHub账号登录

2. **部署项目**
   ```bash
   # 方法1：拖拽dist文件夹到Netlify网站
   npm run build
   # 然后在Netlify网站拖拽dist文件夹

   # 方法2：通过Netlify CLI
   npm install -g netlify-cli
   netlify login
   netlify init
   netlify deploy --prod
   ```

3. **配置构建**
   - Base directory: 留空
   - Build command: `npm run build`
   - Publish directory: `dist`

---

### 3. GitHub Pages ⭐⭐⭐⭐

**优点**：
- ✅ 完全免费
- ✅ 与GitHub集成
- ✅ 简单易用

**限制**：
- ⚠️ 仅支持静态站点
- ⚠️ 需要配置history模式

**使用步骤**：

1. **修改vite.config.js**
   ```javascript
   export default defineConfig({
     plugins: [vue()],
     base: '/your-repo-name/', // 添加这一行
     resolve: {
       alias: {
         '@': fileURLToPath(new URL('./src', import.meta.url))
       }
     }
   })
   ```

2. **修改router/index.js**
   ```javascript
   const router = createRouter({
     history: createWebHashHistory(), // 改用Hash模式
     routes: [...]
   })
   ```

3. **部署脚本**
   
   创建 `deploy.sh`：
   ```bash
   #!/usr/bin/env sh
   
   # 构建
   npm run build
   
   # 进入构建文件夹
   cd dist
   
   # 如果有自定义域名
   # echo 'your-domain.com' > CNAME
   
   git init
   git add -A
   git commit -m 'deploy'
   
   # 推送到GitHub Pages
   git push -f git@github.com:username/repo.git main:gh-pages
   
   cd -
   ```

4. **运行部署**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

5. **启用GitHub Pages**
   - 进入GitHub仓库 → Settings → Pages
   - Source选择"gh-pages"分支
   - 保存

访问：`https://username.github.io/repo-name/`

---

### 4. Cloudflare Pages ⭐⭐⭐⭐

**优点**：
- ✅ 完全免费
- ✅ 无限带宽
- ✅ 全球CDN（非常快）
- ✅ 支持自定义域名

**使用步骤**：

1. **登录Cloudflare**
   - 访问 https://pages.cloudflare.com

2. **连接GitHub**
   - 选择你的仓库

3. **配置构建**
   - Framework preset: Vue
   - Build command: `npm run build`
   - Build output directory: `dist`

4. **部署**
   - 点击"Save and Deploy"

---

### 5. Firebase Hosting ⭐⭐⭐⭐

**优点**：
- ✅ Google提供
- ✅ 免费额度充足
- ✅ 全球CDN
- ✅ 可以集成后端服务

**使用步骤**：

```bash
# 安装Firebase CLI
npm install -g firebase-tools

# 登录
firebase login

# 初始化
firebase init hosting

# 选择:
# - Use an existing project or create a new one
# - What do you want to use as your public directory? dist
# - Configure as a single-page app? Yes
# - Set up automatic builds and deploys with GitHub? (可选)

# 构建
npm run build

# 部署
firebase deploy
```

---

### 6. Railway ⭐⭐⭐⭐

**优点**：
- ✅ 免费额度
- ✅ 支持后端
- ✅ 数据库集成
- ✅ 简单易用

**使用步骤**：

1. 访问 https://railway.app
2. 连接GitHub
3. 选择仓库
4. 自动检测并部署

---

### 7. Surge ⭐⭐⭐

**优点**：
- ✅ 超级简单
- ✅ 命令行部署
- ✅ 免费自定义域名

**使用步骤**：

```bash
# 安装Surge
npm install -g surge

# 构建
npm run build

# 部署
cd dist
surge
```

---

## 推荐方案对比

| 平台 | 难度 | 速度 | 功能 | 推荐度 |
|------|------|------|------|--------|
| Vercel | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Netlify | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Cloudflare Pages | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| GitHub Pages | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Firebase | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Railway | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Surge | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

## 🏆 最佳选择

**对于本项目（儿童学习应用），推荐：**

### 方案1：Vercel（最推荐）
- 速度最快
- 配置最简单
- GitHub自动部署
- 免费HTTPS和CDN

### 方案2：Netlify（备选）
- 功能丰富
- 速度也很快
- 界面友好

### 方案3：Cloudflare Pages（国内访问快）
- 国内访问速度好
- 无限带宽
- Cloudflare的CDN很强大

## 部署前检查清单

- [ ] 确保`npm run build`成功
- [ ] 检查`dist`文件夹已生成
- [ ] 测试构建后的应用（`npm run preview`）
- [ ] 确保所有资源路径正确
- [ ] 如使用路由，确保配置正确

## 部署后优化

### 1. 添加自定义域名
- 在域名提供商设置CNAME记录
- 指向平台提供的域名

### 2. 性能优化
```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia']
        }
      }
    }
  }
})
```

### 3. 启用压缩
- Vercel和Netlify自动启用Gzip
- 可以配置Brotli压缩

## 常见问题

### Q: 页面刷新404？
A: 需要配置SPA fallback

**Vercel** - 创建`vercel.json`：
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

**Netlify** - 创建`public/_redirects`：
```
/*  /index.html  200
```

### Q: 静态资源加载失败？
A: 检查`vite.config.js`的`base`配置

### Q: 构建失败？
A: 检查Node.js版本，建议使用Node 18+

## 国内替代方案

如果上述国外平台访问慢：

### 1. Gitee Pages
- 类似GitHub Pages
- 国内访问快
- 需要实名认证

### 2. 腾讯云静态网站托管
- 免费额度
- 国内CDN
- 需要备案域名（非必须）

### 3. 阿里云OSS + CDN
- 成本极低
- 速度快
- 需要配置

---

**建议流程**：

1. **开发阶段**：本地运行`npm run dev`
2. **测试阶段**：构建并预览`npm run build && npm run preview`
3. **部署阶段**：选择Vercel/Netlify，连接GitHub
4. **维护阶段**：push到GitHub自动部署

祝部署顺利！🎉

如有问题，请查看对应平台的官方文档。

