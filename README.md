# Docker Mirror Checker

[![GitHub](https://img.shields.io/github/license/Syz87/docker-mirror-checker.svg?label=LICENSE&logo=github&logoColor=%20)](https://github.com/Syz87/docker-mirror-checker/blob/main/LICENSE)
![GitHub Stars](https://img.shields.io/github/stars/Syz87/docker-mirror-checker.svg?style=flat&logo=appveyor&label=Stars&logo=github)
![GitHub Forks](https://img.shields.io/github/forks/Syz87/docker-mirror-checker.svg?style=flat&logo=appveyor&label=Forks&logo=github)
![GitHub Release](https://img.shields.io/github/v/release/Syz87/docker-mirror-checker?logo=github&labelColor=green&style=flat)

## 🤔 这是什么？

Docker 镜像多站版本检查与拉取工具。当 `docker pull` 失败或需要检查镜像在不同镜像站的同步状态时使用。

## ✨ 功能特性

- 🔍 **多镜像站检查**：支持渡渡鸟、Docker.1panel.live 等多个镜像站
- 📊 **版本对比**：对比本地镜像与远程镜像版本
- 🏷️ **Tag 列表查询**：获取镜像的所有可用标签
- 📦 **通用支持**：支持任意 Docker 镜像（Docker Hub、GHCR 等）
- 🚀 **拉取建议**：自动推荐可用的镜像站
- 🔨 **构建方案**：提供从源码构建镜像的完整方案

## 📦 安装

### 方式一：直接下载

```bash
# 下载脚本
wget https://raw.githubusercontent.com/Syz87/docker-mirror-checker/main/scripts/check_mirrors.py

# 添加执行权限
chmod +x check_mirrors.py
```

### 方式二：Git 克隆

```bash
git clone https://github.com/Syz87/docker-mirror-checker.git
cd docker-mirror-checker
chmod +x scripts/check_mirrors.py
```

## 🚀 使用方法

### 基本用法

```bash
python3 check_mirrors.py <镜像名>
```

### 示例

```bash
# 检查 Docker Hub 官方镜像
python3 check_mirrors.py nginx
python3 check_mirrors.py redis:alpine
python3 check_mirrors.py ubuntu:22.04

# 检查用户镜像
python3 check_mirrors.py owner/image

# 检查 GHCR 镜像
python3 check_mirrors.py ghcr.io/owner/repo
```

## 📋 决策流程图

```
需要 Docker 镜像
    │
    ├─→ 镜像站有最新版？ ──是──→ 直接拉取
    │
    └─→ 否
            │
            ├─→ 需要修改源码？ ──是──→ 从源码构建
            │
            └─→ 否
                    │
                    ├─→ 内网环境？ ──是──→ DockerTarBuilder 打包离线
                    │
                    └─→ 否 ──→ 等待镜像站同步
```

## 📚 方案对比

| 方案 | 适用场景 | 复杂度 | 能力 |
|------|----------|--------|------|
| **A: 镜像站拉取** | 镜像站有可用镜像 | ⭐ | 拉取已有镜像 |
| **B: 从源码构建** | 需要最新代码或自定义修改 | ⭐⭐⭐ | 构建新镜像 |
| **C: DockerTarBuilder** | 内网环境离线传输 | ⭐⭐ | 打包已有镜像 |

### 方案 A：镜像站拉取（推荐）

```bash
# 尝试从不同镜像站拉取
for mirror in "docker.1panel.live" "ghcr.nju.edu.cn" "docker.1ms.run"; do
    echo "尝试: $mirror"
    docker pull $mirror/nginx:latest 2>&1 | grep -E "(Digest|Status|Error)"
    echo "---"
done
```

### 方案 B：从源码构建

```bash
# 克隆项目
git clone https://github.com/owner/repo.git
cd repo

# 构建镜像
docker build -t my-image:latest .
```

### 方案 C：DockerTarBuilder 打包

```bash
# 1. Fork DockerTarBuilder 仓库
# 2. 触发工作流，输入镜像名
# 3. 下载 Release 中的 tar.gz 文件
# 4. 导入 Docker
docker load -i nginx_latest-amd64.tar.gz
```

## 📚 文档

- [API 参考文档](docs/api-reference.md)
- [使用指南](docs/usage-guide.md)
- [更新日志](CHANGELOG.md)

## 🔧 依赖

- Python 3.6+
- Docker（可选，用于拉取镜像）

## 🤝 贡献

欢迎贡献代码、提交 Issue 或 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [渡渡鸟容器同步站](https://docker.aityp.com/) - 提供镜像同步 API
- [Docker.1panel.live](https://docker.1panel.live/) - 提供 Tag 列表查询
- [DockerTarBuilder](https://github.com/wukongdaily/DockerTarBuilder) - 镜像打包方案
