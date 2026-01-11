import os
import json
import shutil
import subprocess
import time
import glob
from PIL import Image  # 可选，用于图片压缩

# ===================== 配置项（新增分类配置） =====================
AI_COMIC_DIR = "D:/AI_Comic_Output"
AI_COMIC_PATTERN = "raw_comic*.png"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(PROJECT_ROOT, "img")
COMIC_HTML_DIR = os.path.join(PROJECT_ROOT, "comics")
COMIC_INDEX_JSON = os.path.join(PROJECT_ROOT, "comic-index.json")
GIT_BRANCH = "main"
IMAGE_QUALITY = 85

# 新增：五大分类配置（固定值，方便选择）
CATEGORIES = [
    "生活日常",
    "职场打工",
    "校园",
    "趣味脑洞",
    "节日季节"
]
# 默认配置（含分类）
DEFAULT_TITLE_PREFIX = "趣味四格漫画-"
DEFAULT_THEME = "日常·搞笑·轻松一刻"
DEFAULT_CATEGORY = "生活日常"  # 默认分类


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


def read_meta_from_json(meta_file_path, comic_id_num):
    """从JSON读取标题/主题/分类，默认用通用配置"""
    # 若没有元数据文件，直接返回默认值
    if not os.path.exists(meta_file_path):
        return (
            f"{DEFAULT_TITLE_PREFIX}{comic_id_num}",
            DEFAULT_THEME,
            DEFAULT_CATEGORY
        )

    try:
        with open(meta_file_path, "r", encoding="utf-8") as f:
            meta_data = json.load(f)
        comic_title = meta_data.get("title", f"{DEFAULT_TITLE_PREFIX}{comic_id_num}")
        comic_topic = meta_data.get("topic", DEFAULT_THEME)
        # 读取分类，若不在配置列表则用默认
        comic_category = meta_data.get("category", DEFAULT_CATEGORY)
        if comic_category not in CATEGORIES:
            comic_category = DEFAULT_CATEGORY
        return comic_title, comic_topic, comic_category
    except Exception as e:
        print(f"读取JSON失败，使用默认值：{e}")
        return (
            f"{DEFAULT_TITLE_PREFIX}{comic_id_num}",
            DEFAULT_THEME,
            DEFAULT_CATEGORY
        )


def generate_comic_html(comic_id, comic_title, comic_topic, img_relative_paths):
    """生成多图片漫画详情页（适配笑点制造机风格）"""
    html_path = os.path.join(COMIC_HTML_DIR, f"{comic_id}.html")
    # 循环生成所有图片的HTML代码
    img_html = ""
    for img_path in img_relative_paths:
        img_html += f'<img src="../{img_path}" alt="{comic_title}" class="comic-img">'

    # 详情页模板（多图片适配）
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{comic_title} - 笑点制造机</title>
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
        .topic {{ 
            color: #666; 
            font-size: 16px; 
            margin-bottom: 30px;
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
        <h1>{comic_title}</h1>
        <div class="topic">主题：{comic_topic}</div>
        {img_html}
        <div class="footer">© 笑点制造机 · AI辅助创作 · 仅供娱乐</div>
    </div>
</body>
</html>
    """
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template.strip())
    print(f"多图片漫画详情页生成完成：{html_path}")
    return html_path


def update_comic_index(comic_id, comic_title, comic_topic, comic_category, main_img_path, html_path):
    """更新漫画索引JSON（新增category字段）"""
    with open(COMIC_INDEX_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_comic = {
        "id": comic_id,
        "title": comic_title,
        "topic": comic_topic,
        "category": comic_category,  # 新增：分类字段
        "img": main_img_path,  # 列表页展示第一张图
        "html": html_path,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    data["comics"].append(new_comic)

    with open(COMIC_INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"漫画索引JSON更新完成（含分类）：{COMIC_INDEX_JSON}")


def git_push():
    """Git提交推送"""
    try:
        os.chdir(PROJECT_ROOT)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto add multi-img comic: {time.strftime('%Y%m%d_%H%M%S')}"],
                       check=True)
        subprocess.run(["git", "push", "origin", GIT_BRANCH], check=True)
        print("Git推送成功，Cloudflare将自动部署！")
    except subprocess.CalledProcessError as e:
        print(f"Git推送失败：{e}")


def main():
    """主流程（适配多图片+分类）"""
    # 1. 创建必要目录
    for dir_path in [IMG_DIR, COMIC_HTML_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"创建目录：{dir_path}")

    # 2. 获取漫画ID
    comic_id_num = get_next_comic_id()
    comic_id = f"comic-{comic_id_num}"

    # 3. 读取标题、主题、分类（修复：传入comic_id_num参数）
    AI_META_JSON_PATH = os.path.join(AI_COMIC_DIR, "comic_meta.json")
    comic_title, comic_topic, comic_category = read_meta_from_json(AI_META_JSON_PATH, comic_id_num)
    print(f"漫画标题：{comic_title}")
    print(f"漫画主题：{comic_topic}")
    print(f"漫画分类：{comic_category}")

    # 4. 扫描AI生成的所有图片（raw_comic1.png、raw_comic2.png...）
    ai_comic_files = glob.glob(os.path.join(AI_COMIC_DIR, AI_COMIC_PATTERN))
    # 按文件名排序（确保1、2、3的顺序）
    ai_comic_files.sort()
    if not ai_comic_files:
        print("⚠️ 未找到AI生成的漫画图片！")
        return

    # 5. 批量处理图片（复制/压缩）
    img_relative_paths = []  # 存储所有图片的相对路径
    for idx, img_file in enumerate(ai_comic_files, 1):
        # 命名规则：comic-001-1.png、comic-001-2.png...
        img_filename = f"{comic_id}-{idx}.png"
        img_output_path = os.path.join(IMG_DIR, img_filename)
        # 压缩图片（注释此行则禁用压缩）
        compress_image(img_file, img_output_path)
        # 若禁用压缩，替换为：shutil.copy(img_file, img_output_path)
        # 保存相对路径（用于详情页）
        img_relative_paths.append(f"img/{img_filename}")

    # 6. 生成多图片详情页
    html_relative_path = f"comics/{comic_id}.html"
    generate_comic_html(comic_id, comic_title, comic_topic, img_relative_paths)

    # 7. 更新JSON索引（新增分类字段）
    update_comic_index(comic_id, comic_title, comic_topic, comic_category, img_relative_paths[0], html_relative_path)

    # 8. 推送到GitHub
    git_push()

    # 可选：清空AI输出目录（避免重复处理）
    # for img_file in ai_comic_files:
    #     os.remove(img_file)
    # print("已清空AI输出目录，避免重复处理")


if __name__ == "__main__":
    main()
    print("===== 多图片+分类漫画生成&同步流程完成 =====")