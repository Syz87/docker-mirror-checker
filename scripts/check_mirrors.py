#!/usr/bin/env python3
"""Docker 镜像多站版本检查脚本（通用版）

用法:
    python3 check_mirrors.py <镜像名>
    
示例:
    python3 check_mirrors.py nginx
    python3 check_mirrors.py redis:alpine
    python3 check_mirrors.py ghcr.io/owner/repo
    python3 check_mirrors.py ubuntu:22.04
    python3 check_mirrors.py library/nginx
    python3 check_mirrors.py zhulinsen/daily_stock_analysis
"""

import json
import subprocess
import sys
import urllib.request
from datetime import datetime


# 请求头（部分 API 需要 User-Agent）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}


def check_dobird_api(image_name):
    """检查渡渡鸟容器同步站 API"""
    url = f"https://docker.aityp.com/api/v1/image?search={image_name}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get('results', [])
    except Exception as e:
        return [{"error": str(e)}]


def check_1panel_tags(image_name):
    """检查 docker.1panel.live 的 tag 列表"""
    url = f"https://docker.1panel.live/v2/{image_name}/tags/list"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get('tags', [])
    except Exception as e:
        return []


def get_local_image_info(image_name, tag="latest"):
    """获取本地镜像信息"""
    try:
        result = subprocess.run(
            ["docker", "inspect", f"{image_name}:{tag}", 
             "--format", "{{.Id}}\n{{.Created}}\n{{index .RepoDigests 0}}"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return {
                "id": lines[0] if len(lines) > 0 else "N/A",
                "created": lines[1] if len(lines) > 1 else "N/A",
                "digest": lines[2] if len(lines) > 2 else "N/A"
            }
    except:
        pass
    return None


def normalize_image_name(name):
    """标准化镜像名称，添加默认前缀"""
    # 如果已经包含 / 或 .，可能是完整的镜像名
    if '/' in name or '.' in name:
        return name
    # 否则添加 library/ 前缀（Docker Hub 官方镜像）
    return f"library/{name}"


def extract_tag(image_name, default="latest"):
    """从镜像名中提取 tag"""
    if ':' in image_name:
        parts = image_name.rsplit(':', 1)
        # 确保 : 后面不是端口号（如 localhost:5000）
        if '/' not in parts[1]:
            return parts[0], parts[1]
    return image_name, default


def main():
    if len(sys.argv) < 2:
        print("用法: python3 check_mirrors.py <镜像名>")
        print("示例:")
        print("  python3 check_mirrors.py nginx")
        print("  python3 check_mirrors.py redis:alpine")
        print("  python3 check_mirrors.py ghcr.io/owner/repo")
        print("  python3 check_mirrors.py ubuntu:22.04")
        sys.exit(1)
    
    image_input = sys.argv[1]
    image_name, tag = extract_tag(image_input)
    normalized_name = normalize_image_name(image_name)
    
    print(f"{'='*60}")
    print(f"Docker 镜像多站版本检查")
    print(f"{'='*60}")
    print(f"镜像: {image_input}")
    print(f"标准化: {normalized_name}:{tag}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 检查渡渡鸟 API
    print("【1. 渡渡鸟容器同步站 (docker.aityp.com)】")
    print("-" * 40)
    results = check_dobird_api(image_name)
    if not results:
        print("  未找到镜像信息")
    for r in results:
        if 'error' in r:
            print(f"  ❌ 错误: {r['error']}")
        else:
            source = r.get('source', 'N/A')
            mirror = r.get('mirror', 'N/A')
            platform = r.get('platform', 'N/A')
            size = r.get('size', 'N/A')
            created = r.get('createdAt', 'N/A')
            
            # 提取 tag
            source_tag = source.split(':')[-1] if ':' in source else 'latest'
            
            print(f"  📦 Tag: {source_tag}")
            print(f"     来源: {source}")
            print(f"     镜像: {mirror}")
            print(f"     平台: {platform}")
            print(f"     大小: {size}")
            print(f"     创建: {created}")
            print()
    
    # 2. 检查 docker.1panel.live
    print("【2. Docker.1panel.live 标签列表】")
    print("-" * 40)
    tags = check_1panel_tags(image_name)
    if tags:
        print(f"  📋 共 {len(tags)} 个标签")
        
        # 分类标签
        version_tags = sorted([t for t in tags if t.startswith('v') or (t[0].isdigit() and '.' in t)])
        sha_tags = sorted([t for t in tags if t.startswith('sha-')])
        other_tags = [t for t in tags if not t.startswith('v') and not t.startswith('sha-') and not (t[0].isdigit() and '.' in t)]
        
        if version_tags:
            print(f"  🏷️  版本标签: {', '.join(version_tags[-5:])}")
        if sha_tags:
            print(f"  🔑 SHA 标签: {len(sha_tags)} 个")
        if other_tags:
            print(f"  📌 其他标签: {', '.join(other_tags[:5])}")
    else:
        print("  ❌ 无法获取标签列表（可能需要认证或镜像不存在）")
    
    # 3. 检查本地镜像
    print()
    print("【3. 本地镜像信息】")
    print("-" * 40)
    local_info = get_local_image_info(image_name, tag)
    if local_info:
        print(f"  🏠 ID: {local_info['id'][:19]}")
        print(f"  🕐 创建: {local_info['created']}")
        if local_info['digest'] and local_info['digest'] != 'N/A':
            print(f"  🔗 Digest: {local_info['digest'][:50]}...")
    else:
        print(f"  ⚠️  本地未找到 {image_name}:{tag}")
    
    # 4. 总结
    print()
    print("【总结】")
    print("-" * 40)
    if results:
        # 找到最新的镜像
        latest = None
        for r in results:
            if 'createdAt' in r:
                if latest is None or r['createdAt'] > latest['createdAt']:
                    latest = r
        
        if latest:
            print(f"  📌 最新同步: {latest.get('source', 'N/A')}")
            print(f"  🕐 同步时间: {latest.get('createdAt', 'N/A')}")
    
    if tags:
        version_tags = sorted([t for t in tags if t.startswith('v') or (t[0].isdigit() and '.' in t)])
        if version_tags:
            print(f"  🏷️  最新版本: {version_tags[-1]}")
    
    # 5. 建议
    print()
    print("【拉取建议】")
    print("-" * 40)
    if results:
        print("  可以尝试以下方式拉取：")
        print(f"    docker pull {image_name}:{tag}")
        print(f"    docker pull docker.1panel.live/{image_name}:{tag}")
        print(f"    docker pull ghcr.nju.edu.cn/{image_name}:{tag}")
    else:
        print("  ⚠️  未找到镜像信息，请检查镜像名是否正确")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
