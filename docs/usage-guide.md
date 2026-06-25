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

3. **使用 DockerTarBuilder 自建**
   - Fork [DockerTarBuilder](https://github.com/wukongdaily/DockerTarBuilder)
   - 触发工作流构建镜像
   - 下载并导入

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
   - 使用 DockerTarBuilder

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
- 使用 DockerTarBuilder 自建镜像

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
