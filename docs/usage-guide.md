# 使用指南

本文档介绍 Docker Mirror Checker 的常见使用场景和最佳实践。

## 场景一：Docker Pull 失败

当 `docker pull` 超时或失败时，使用本工具检查可用的镜像站。

### 步骤

1. **检查镜像可用性**
   ```bash
   python3 check_mirrors.py nginx
   ```

2. **查看输出结果**
   - 查看哪些镜像站有该镜像
   - 选择同步时间最新的镜像站

3. **从镜像站拉取**
   ```bash
   docker pull docker.1panel.live/nginx:latest
   ```

---

## 场景二：检查镜像版本

当需要确认本地镜像是否为最新版本时。

### 步骤

1. **运行检查脚本**
   ```bash
   python3 check_mirrors.py nginx:latest
   ```

2. **对比版本信息**
   - 查看本地镜像的创建时间
   - 对比远程镜像的同步时间
   - 确认是否需要更新

3. **更新镜像（如需要）**
   ```bash
   docker pull nginx:latest
   ```

---

## 场景三：批量检查多个镜像

当需要检查多个镜像的可用性时。

### 方法一：循环检查

```bash
for image in nginx redis postgres mysql; do
    echo "=== 检查 $image ==="
    python3 check_mirrors.py $image
    echo ""
done
```

### 方法二：使用脚本

创建 `check_all.sh`：

```bash
#!/bin/bash
images=("nginx" "redis" "postgres" "mysql" "mongo")

for image in "${images[@]}"; do
    echo "=========================================="
    echo "检查: $image"
    echo "=========================================="
    python3 check_mirrors.py $image
    echo ""
done
```

---

## 场景四：检查特定版本

当需要检查特定版本的镜像时。

### 示例

```bash
# 检查特定版本
python3 check_mirrors.py nginx:1.25.3

# 检查 Alpine 版本
python3 check_mirrors.py redis:alpine

# 检查特定架构
python3 check_mirrors.py ubuntu:22.04
```

---

## 场景五：GHCR 镜像检查

当需要检查 GitHub Container Registry 的镜像时。

### 注意事项

GHCR 镜像的 API 支持有限，建议：

1. **使用脚本检查**
   ```bash
   python3 check_mirrors.py ghcr.io/owner/repo
   ```

2. **直接拉取尝试**
   ```bash
   # 尝试从镜像站拉取
   docker pull ghcr.nju.edu.cn/ghcr.io/owner/repo:latest
   
   # 尝试直接拉取
   docker pull ghcr.io/owner/repo:latest
   ```

---

## 场景六：从源码构建镜像

当需要最新代码或自定义修改时，必须从源码构建。

### 方案 B1：本地 Docker Build

```bash
# 克隆项目
git clone https://github.com/owner/repo.git
cd repo

# 构建镜像
docker build -t my-image:latest .

# 或使用 docker-compose
docker compose build
docker compose up -d
```

**适用场景：**
- ✅ 单机部署、快速测试
- ✅ 需要修改源码
- ✅ 需要自定义配置

### 方案 B2：GitHub Actions 自动构建

在项目中添加 `.github/workflows/docker-build.yml`：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
```

**适用场景：**
- ✅ 多人协作、CI/CD
- ✅ 需要自动构建
- ✅ 需要多架构支持

### 方案 B3：多阶段构建（优化镜像大小）

```dockerfile
# 第一阶段：构建
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt
COPY . .
RUN python -m py_compile main.py

# 第二阶段：运行
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

**适用场景：**
- ✅ 需要优化镜像大小
- ✅ 生产环境部署
- ✅ 安全敏感场景

---

## 场景七：内网环境离线传输

当内网环境无法直接访问外网时，使用 DockerTarBuilder 打包镜像。

### ⚠️ 重要说明

DockerTarBuilder **只能拉取已有镜像并打包**，**不能从源码构建**。

### 使用步骤

1. **Fork DockerTarBuilder 仓库**
   ```bash
   # 在 GitHub 上 fork wukongdaily/DockerTarBuilder
   ```

2. **触发工作流**
   - 进入 Actions 页面
   - 选择对应架构的工作流
   - 输入镜像名称

3. **下载并导入镜像**
   ```bash
   # 下载 Release 中的 tar.gz 文件
   wget https://github.com/<你的用户名>/DockerTarBuilder/releases/download/DockerTarBuilder-AMD64/nginx_latest-amd64.tar.gz
   
   # 导入 Docker
   docker load -i nginx_latest-amd64.tar.gz
   
   # 验证
   docker images | grep nginx
   ```

---

## 最佳实践

### 1. 镜像拉取优先级

推荐按以下顺序尝试拉取：

1. **镜像加速器**（国内用户）
   - `docker.1panel.live`
   - `ghcr.nju.edu.cn`

2. **官方源**
   - `docker.io`
   - `ghcr.io`

3. **自建镜像**
   - 从源码构建（方案 B）
   - DockerTarBuilder 打包（方案 C）

### 2. 版本锁定

在生产环境中，建议锁定镜像版本：

```bash
# 不推荐
docker pull nginx:latest

# 推荐
docker pull nginx:1.25.3
```

### 3. 定期检查

定期运行检查脚本，确保镜像同步状态：

```bash
# 每周检查一次
python3 check_mirrors.py nginx:latest
```

### 4. 多架构支持

当需要特定架构时，检查平台信息：

```bash
# 查看镜像支持的平台
curl -sL "https://docker.aityp.com/api/v1/image?search=nginx&platform=linux/arm64" | python3 -m json.tool
```

### 5. 选择正确的方案

根据需求选择合适的方案：

| 需求 | 推荐方案 |
|------|----------|
| 镜像站有最新版 | 方案 A：镜像站拉取 |
| 需要最新代码 | 方案 B：从源码构建 |
| 需要自定义修改 | 方案 B：从源码构建 |
| 内网环境 | 方案 C：DockerTarBuilder 打包 |
| 只是镜像站没同步 | 等待同步 |

---

## 常见问题

### Q: 为什么某些镜像在 API 中找不到？

A: 可能的原因：
- 镜像名输入错误
- 镜像未被镜像站同步
- 镜像已被删除

### Q: 镜像站的同步时间比官方晚怎么办？

A: 这是正常现象，镜像站需要时间同步。可以：
- 等待镜像站同步
- 从源码构建（方案 B）
- 使用 DockerTarBuilder 打包（方案 C）

### Q: DockerTarBuilder 能从源码构建吗？

A: 不能。DockerTarBuilder 只能拉取已有镜像并打包，不能修改镜像内容。如果需要从源码构建，请使用方案 B。

### Q: 如何贡献代码？

A: 欢迎贡献！请：
1. Fork 仓库
2. 创建特性分支
3. 提交更改
4. 创建 Pull Request

---

## 获取帮助

- 查看 [API 参考文档](api-reference.md)
- 提交 [Issue](https://github.com/Syz87/docker-mirror-checker/issues)
