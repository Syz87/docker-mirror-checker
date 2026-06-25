#!/bin/bash
#
# Docker Mirror Checker 使用示例
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_SCRIPT="$SCRIPT_DIR/../scripts/check_mirrors.py"

echo "=========================================="
echo "Docker Mirror Checker 使用示例"
echo "=========================================="
echo ""

# 示例 1：检查 Docker Hub 官方镜像
echo "【示例 1】检查 Docker Hub 官方镜像"
echo "------------------------------------------"
python3 "$CHECK_SCRIPT" nginx
echo ""

# 示例 2：检查带标签的镜像
echo "【示例 2】检查带标签的镜像"
echo "------------------------------------------"
python3 "$CHECK_SCRIPT" redis:alpine
echo ""

# 示例 3：检查用户镜像
echo "【示例 3】检查用户镜像"
echo "------------------------------------------"
python3 "$CHECK_SCRIPT" linuxserver/nginx
echo ""

# 示例 4：检查 GHCR 镜像
echo "【示例 4】检查 GHCR 镜像"
echo "------------------------------------------"
python3 "$CHECK_SCRIPT" ghcr.io/zhulinsen/daily_stock_analysis
echo ""

# 示例 5：批量检查
echo "【示例 5】批量检查多个镜像"
echo "------------------------------------------"
for image in nginx redis postgres mysql; do
    echo "--- 检查: $image ---"
    python3 "$CHECK_SCRIPT" "$image" 2>&1 | head -10
    echo ""
done

echo "=========================================="
echo "示例完成"
echo "=========================================="
