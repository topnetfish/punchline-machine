import os
import json
import shutil
import subprocess
import time
import glob
from PIL import Image  # 可选，用于图片压缩
# 导入模板库
from comic_templates import get_template, get_all_categories, get_sub_categories

# ===================== 配置项 =====================
AI_COMIC_DIR = "D:/AI_Comic_Output"
AI_COMIC_PATTERN = "raw_comic*.png"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(PROJECT_ROOT, "img")
COMIC_HTML_DIR = os.path.join(PROJECT_ROOT, "comics")
COMIC_INDEX_JSON = os.path.join(PROJECT_ROOT, "comic-index.json")
GIT_BRANCH = "main"
IMAGE_QUALITY = 85

# 默认配置（从模板库兜底）
DEFAULT_CATEGORY = "生活日常"
DEFAULT_SUB_CATEGORY = "居家日常"


# ===================== 核心函数 =====================
def get_next_comic_id():
    """获取下一个漫画的序号（comic-001→002→003...）"""
    if not os.path.exists(COMIC_INDEX_JSON):
        with open(COMIC_INDEX_JSON, "w", encoding="utf-8") as f:
            json.dump({"comics": []}, f, ensure_ascii=False, indent=2)
        return "001"

    with open(COMIC_INDEX_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    comic_list = data.get("comics", [])
    if not comic_list:
        return "001"

    last_id_str = comic_list[-1]["id"].split("-")[-1]
    last_id = int(last_id_str)
    next_id = str(last_id + 1).zfill(3)
    return next_id


def compress_image(input_path, output_path):
    """压缩图片（适配多图片）"""
    try:
        img = Image.open(input_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_path, "JPEG", optimize=True, quality=IMAGE_QUALITY)
        print(f"图片压缩完成：{output_path}")
    except Exception as e:
        shutil.copy(input_path, output_path)
        print(f"图片压缩失败，直接复制：{e}")


def get_comic_meta(comic_id_num, meta_file_path=None):
    """
    获取漫画元数据（优先读JSON，其次用模板，最后兜底）
    :param comic_id_num: 漫画ID（如"001"）
    :param meta_file_path: 元数据JSON路径
    :return: (title, topic, category, sub_topic, funny_example)
    """
    # 1. 优先读取自定义JSON
    if meta_file_path and os.path.exists(meta_file_path):
        try:
            with open(meta_file_path, "r", encoding="utf-8") as f:
                meta_data = json.load(f)

            category = meta_data.get("category", DEFAULT_CATEGORY)
            sub_category = meta_data.get("sub_category", DEFAULT_SUB_CATEGORY)

            # 尝试从模板补全缺失字段
            template = get_template(category, sub_category)
            if template:
                title = meta_data.get("title", template["default_title"])
                topic = meta_data.get("topic", template["default_topic"])
                sub_topic = meta_data.get("sub_topic", template["sub_topic"])
                funny_example = meta_data.get("funny_example", template["funny_example"])
            else:
                # 无模板时用自定义值/默认值
                title = meta_data.get("title", f"趣味四格漫画-{comic_id_num}")
                topic = meta_data.get("topic", "日常·搞笑·轻松一刻")
                sub_topic = meta_data.get("sub_topic", "居家日常")
                funny_example = meta_data.get("funny_example", "简单有趣的日常小笑点")

            # 校验主分类合法性
            if category not in get_all_categories():
                category = DEFAULT_CATEGORY

            return title, topic, category, sub_topic, funny_example
        except Exception as e:
            print(f"读取自定义JSON失败，使用模板：{e}")

    # 2. 使用默认模板
    template = get_template(DEFAULT_CATEGORY, DEFAULT_SUB_CATEGORY)
    if template:
        return (
            template["default_title"],
            template["default_topic"],
            DEFAULT_CATEGORY,
            template["sub_topic"],
            template["funny_example"]
        )

    # 3. 最终兜底
    return (
        f"趣味四格漫画-{comic_id_num}",
        "日常·搞笑·轻松一刻",
        DEFAULT_CATEGORY,
        "居家日常",
        "简单有趣的日常小笑点"
    )


def generate_comic_html(comic_id, title, topic, category, sub_topic, funny_example, img_paths):
    """生成详情页（完整展示模板信息）"""
    html_path = os.path.join(COMIC_HTML_DIR, f"{comic_id}.html")
    img_html = "".join([f'<img src="../{p}" alt="{title}" class="comic-img">' for p in img_paths])

    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title} - 笑点制造机</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: #f5f5f5; 
            color: #333;
        }}
        .container {{ 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 40px 20px; 
        }}
        .back-btn {{ 
            display: inline-block; 
            padding: 8px 16px; 
            background: #333; 
            color: white; 
            text-decoration: none; 
            border-radius: 4px; 
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .back-btn:hover {{ background: #555; }}
        h1 {{ 
            font-size: 28px; 
            margin-bottom: 10px; 
            font-weight: 600;
        }}
        .meta-info {{
            color: #666;
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.8;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        .meta-info .label {{
            color: #333;
            font-weight: 500;
            display: inline-block;
            width: 80px;
        }}
        .comic-img {{ 
            width: 100%; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #999;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-btn">← 返回笑点制造机</a>
        <h1>{title}</h1>
        <div class="meta-info">
            <div><span class="label">主分类：</span>{category}</div>
            <div><span class="label">子主题：</span>{sub_topic}</div>
            <div><span class="label">核心笑点：</span>{funny_example}</div>
            <div><span class="label">主题标签：</span>{topic}</div>
        </div>
        {img_html}
        <div class="footer">© 笑点制造机 · AI辅助创作 · 仅供娱乐</div>
    </div>
</body>
</html>
    """
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template.strip())
    print(f"详情页生成完成：{html_path}")
    return html_path


def update_comic_index(comic_id, title, topic, category, sub_topic, funny_example, main_img, html_path):
    """更新索引（含完整模板字段）"""
    with open(COMIC_INDEX_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_comic = {
        "id": comic_id,
        "title": title,
        "topic": topic,
        "category": category,
        "sub_topic": sub_topic,
        "funny_example": funny_example,
        "img": main_img,
        "html": html_path,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    data["comics"].append(new_comic)

    with open(COMIC_INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"索引更新完成：{COMIC_INDEX_JSON}")


def git_push():
    """Git推送"""
    try:
        os.chdir(PROJECT_ROOT)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"新增漫画 {time.strftime('%Y%m%d_%H%M%S')}"], check=True,
                       capture_output=True)
        subprocess.run(["git", "push", "origin", GIT_BRANCH], check=True, capture_output=True)
        print("Git推送成功！")
    except subprocess.CalledProcessError as e:
        print(f"Git推送失败：{e.stderr.decode('utf-8')}")


def main():
    """主流程（支持模板调用）"""
    # 1. 初始化目录
    for dir in [IMG_DIR, COMIC_HTML_DIR]:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"创建目录：{dir}")

    # 2. 获取漫画ID
    comic_id_num = get_next_comic_id()
    comic_id = f"comic-{comic_id_num}"
    print(f"开始生成漫画：{comic_id}")

    # 3. 获取元数据（优先自定义JSON，其次模板）
    meta_file = os.path.join(AI_COMIC_DIR, "comic_meta.json")
    title, topic, category, sub_topic, funny_example = get_comic_meta(comic_id_num, meta_file)
    print(f"元数据：\n- 标题：{title}\n- 主分类：{category}\n- 子主题：{sub_topic}\n- 笑点：{funny_example}")

    # 4. 处理图片
    img_files = glob.glob(os.path.join(AI_COMIC_DIR, AI_COMIC_PATTERN))
    img_files.sort()
    if not img_files:
        print("⚠️ 未找到AI生成的图片！")
        return

    img_paths = []
    for idx, img in enumerate(img_files, 1):
        img_name = f"{comic_id}-{idx}.png"
        img_dst = os.path.join(IMG_DIR, img_name)
        compress_image(img, img_dst)  # 注释此行禁用压缩
        img_paths.append(f"img/{img_name}")

    # 5. 生成详情页
    html_path = f"comics/{comic_id}.html"
    generate_comic_html(comic_id, title, topic, category, sub_topic, funny_example, img_paths)

    # 6. 更新索引
    update_comic_index(comic_id, title, topic, category, sub_topic, funny_example, img_paths[0], html_path)

    # 7. 推送Git
    git_push()

    print(f"\n✅ 漫画 {comic_id} 生成完成！")
    print(f"- 预览地址：index.html（首页）")
    print(f"- 详情地址：{html_path}")


if __name__ == "__main__":
    main()