# Changelog

本文档记录了 Docker Mirror Checker 的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-06-25

### 🎉 首次发布

#### ✨ 新功能

- **多镜像站检查**
  - 支持渡渡鸟容器同步站 API（docker.aityp.com）
  - 支持 Docker.1panel.live Tag 列表查询
  - 支持多个国内镜像加速器

- **通用镜像支持**
  - 支持 Docker Hub 官方镜像（自动添加 library/ 前缀）
  - 支持 Docker Hub 用户镜像
  - 支持 GHCR 镜像

- **版本对比功能**
  - 显示本地镜像版本
  - 对比远程镜像版本
  - 显示镜像创建时间

- **智能拉取建议**
  - 自动推荐可用的镜像站
  - 提供多种拉取方式

#### 📦 核心功能

- `check_mirrors.py` - 主检查脚本
  - 渡渡鸟 API 查询
  - Docker.1panel.live Tag 列表查询
  - 本地镜像信息获取
  - 可视化报告生成

#### 📚 文档

- README.md - 项目介绍和使用说明
- API 参考文档 - 详细的 API 说明
- 使用指南 - 常见使用场景

#### 🔧 技术特性

- 纯 Python 实现，无外部依赖
- 支持 Python 3.6+
- 跨平台支持（Linux/macOS/Windows）

---

## 版本号说明

- **主版本号（Major）**：不兼容的 API 修改
- **次版本号（Minor）**：向下兼容的功能性新增
- **修订号（Patch）**：向下兼容的问题修正
