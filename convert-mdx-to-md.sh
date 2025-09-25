#!/bin/bash

# 创建目标目录
mkdir -p mdocs

# 查找所有 .mdx 文件并转换为 .md
find mdx -name "*.mdx" -type f | while read mdx_file; do
    # 获取相对路径（去掉 mdx/ 前缀）
    relative_path=${mdx_file#mdx/}
    # 替换扩展名为 .md
    md_file="mdocs/${relative_path%.mdx}.md"
    # 创建必要的子目录
    mkdir -p "$(dirname "$md_file")"
    # 复制文件并重命名
    cp "$mdx_file" "$md_file"
    echo "转换: $mdx_file -> $md_file"
done

echo "转换完成！所有 .mdx 文件已转换为 .md 文件并保存到 mdocs 目录"