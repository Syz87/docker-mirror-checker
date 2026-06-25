# API 参考文档

本文档详细介绍了 Docker Mirror Checker 使用的各个镜像站 API。

## 1. 渡渡鸟容器同步站 (docker.aityp.com)

### 查询镜像

**端点：** `GET https://docker.aityp.com/api/v1/image`

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| search | string | 是 | 镜像名，支持模糊搜索 |
| site | string | 否 | 来源站点：`All`/`docker.io`/`ghcr.io`/`quay.io` 等 |
| platform | string | 否 | 平台：`linux/amd64`/`linux/arm64` 等 |

**请求示例：**

```bash
curl -sL "https://docker.aityp.com/api/v1/image?search=nginx" | python3 -m json.tool
```

**响应示例：**

```json
{
  "count": 2,
  "results": [
    {
      "source": "docker.io/library/nginx:latest",
      "mirror": "swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/nginx:latest",
      "platform": "linux/amd64",
      "size": "187.69MB",
      "createdAt": "2024-08-25T17:25:00.706+08:00"
    }
  ],
  "search": "nginx"
}
```

**响应字段说明：**

| 字段 | 说明 |
|------|------|
| source | 原始镜像地址 |
| mirror | 镜像站同步地址 |
| platform | 平台架构 |
| size | 镜像大小 |
| createdAt | 镜像站同步时间 |

### 其他 API

| 端点 | 说明 |
|------|------|
| `GET /api/v1/latest` | 获取最新同步的镜像 |
| `GET /api/v1/today` | 获取今日同步的镜像 |
| `GET /api/v1/wait` | 获取等待同步的镜像 |
| `GET /api/v1/health` | 健康检查 |

---

## 2. Docker.1panel.live

### 查询 Tag 列表

**端点：** `GET https://docker.1panel.live/v2/<镜像名>/tags/list`

**注意：** 需要带 `User-Agent` 头，否则返回 403

**请求示例：**

```bash
curl -sL "https://docker.1panel.live/v2/library/nginx/tags/list" \
    -H "User-Agent: Mozilla/5.0" | python3 -m json.tool
```

**响应示例：**

```json
{
  "name": "library/nginx",
  "tags": [
    "latest",
    "1.25.3",
    "1.25.4",
    "alpine",
    "mainline",
    "stable"
  ]
}
```

**响应字段说明：**

| 字段 | 说明 |
|------|------|
| name | 镜像名称 |
| tags | 所有可用标签列表 |

---

## 3. DockerHub API

### 查询 Tag 详情

**端点：** `GET https://hub.docker.com/v2/repositories/<namespace>/<name>/tags/`

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page_size | int | 否 | 每页数量，默认 10 |
| page | int | 否 | 页码 |

**请求示例：**

```bash
curl -sL "https://hub.docker.com/v2/repositories/library/nginx/tags/?page_size=10" | python3 -m json.tool
```

**响应示例：**

```json
{
  "count": 100,
  "results": [
    {
      "name": "latest",
      "last_updated": "2024-08-25T17:25:00.706Z",
      "images": [
        {
          "architecture": "amd64",
          "size": 187690000
        }
      ]
    }
  ]
}
```

---

## 4. GHCR API

### 查询 Tag 列表

**端点：** `GET https://ghcr.io/v2/<owner>/<repo>/tags/list`

**注意：** 部分仓库需要认证

**请求示例：**

```bash
curl -sL "https://ghcr.io/v2/owner/repo/tags/list" | python3 -m json.tool
```

---

## 5. 镜像站拉取地址

| 镜像站 | 拉取地址格式 | 认证 |
|--------|--------------|------|
| Docker.1panel.live | `docker.1panel.live/<镜像>:<tag>` | 无需 |
| Docker.1ms.run | `docker.1ms.run/<镜像>:<tag>` | 需 Docker |
| Hub.rat.dev | `hub.rat.dev/<镜像>:<tag>` | 需 Docker |
| Docker-registry.nmqu.com | `docker-registry.nmqu.com/<镜像>:<tag>` | 需 Docker |
| GHCR.njuedu.cn | `ghcr.nju.edu.cn/<镜像>:<tag>` | 无需 |

---

## 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 403 | 禁止访问 | 检查是否需要 User-Agent 或认证 |
| 404 | 未找到 | 检查镜像名是否正确 |
| 429 | 请求过多 | 稍后重试 |

### 错误响应示例

```json
{
  "errors": [
    {
      "code": "UNAUTHORIZED",
      "message": "authentication required"
    }
  ]
}
```
