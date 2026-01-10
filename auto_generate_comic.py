import os
import json
import shutil
import subprocess
import time
from PIL import Image  # 可选，用于图片压缩

# ===================== 配置项（根据你的需求修改） =====================
AI_COMIC_RAW_PATH = "D:/AI_Comic_Output/raw_comic.png"  # AI生成的四格漫画原图路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(PROJECT_ROOT, "img")
COMIC_HTML_DIR = os.path.join(PROJECT_ROOT, "comics")
COMIC_INDEX_JSON = os.path.join(PROJECT_ROOT, "comic-index.json")
GIT_BRANCH = "main"
IMAGE_QUALITY = 85

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
    """压缩图片（适配四格漫画）"""
    try:
        img = Image.open(input_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_path, "JPEG", optimize=True, quality=IMAGE_QUALITY)
        print(f"四格漫画图片压缩完成：{output_path}")
    except Exception as e:
        shutil.copy(input_path, output_path)
        print(f"图片压缩失败，直接复制：{e}")

def generate_comic_html(comic_id, comic_title, comic_topic, img_path):
    """生成四格漫画详情页（适配笑点制造机风格）"""
    html_path = os.path.join(COMIC_HTML_DIR, f"{comic_id}.html")
    # 详情页模板（与首页视觉统一）
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
        <img src="../{img_path}" alt="{comic_title}" class="comic-img">
        <div class="footer">© 笑点制造机 · AI辅助创作 · 仅供娱乐</div>
    </div>
</body>
</html>
    """
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template.strip())
    print(f"漫画详情页生成完成：{html_path}")
    return html_path

def update_comic_index(comic_id, comic_title, comic_topic, img_path, html_path):
    """更新漫画索引JSON（新增主题字段）"""
    with open(COMIC_INDEX_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    new_comic = {
        "id": comic_id,
        "title": comic_title,
        "topic": comic_topic,  # 新增主题字段
        "img": img_path,
        "html": html_path,
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    data["comics"].append(new_comic)
    
    with open(COMIC_INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"漫画索引JSON更新完成：{COMIC_INDEX_JSON}")

def git_push():
    """Git提交推送"""
    try:
        os.chdir(PROJECT_ROOT)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto add comic: {time.strftime('%Y%m%d_%H%M%S')}"], check=True)
        subprocess.run(["git", "push", "origin", GIT_BRANCH], check=True)
        print("Git推送成功，Cloudflare将自动部署！")
    except subprocess.CalledProcessError as e:
        print(f"Git推送失败：{e}")

def main():
    """主流程（适配笑点制造机）"""
    # 创建必要目录
    for dir_path in [IMG_DIR, COMIC_HTML_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"创建目录：{dir_path}")
    
    # 获取漫画ID
    comic_id_num = get_next_comic_id()
    comic_id = f"comic-{comic_id_num}"
    
    # 自定义标题和主题（可手动输入，也可从AI生成结果读取）
    comic_title = input(f"请输入漫画标题（如：程序员的测试）：") or f"笑点漫画-{comic_id_num}"
    comic_topic = input(f"请输入漫画主题（如：程序员·反转型笑话）：") or f"AI创作·四格漫画"
    
    # 处理四格漫画图片
    img_filename = f"{comic_id}-4grid.png"  # 四格漫画专属命名
    img_output_path = os.path.join(IMG_DIR, img_filename)
    compress_image(AI_COMIC_RAW_PATH, img_output_path)  # 压缩图片
    # 若禁用压缩，替换为：shutil.copy(AI_COMIC_RAW_PATH, img_output_path)
    
    # 生成详情页
    img_relative_path = f"img/{img_filename}"
    html_relative_path = f"comics/{comic_id}.html"
    generate_comic_html(comic_id, comic_title, comic_topic, img_relative_path)
    
    # 更新索引JSON
    update_comic_index(comic_id, comic_title, comic_topic, img_relative_path, html_relative_path)
    
    # 推送GitHub
    git_push()

if __name__ == "__main__":
    main()
    print("===== 笑点制造机漫画生成&同步流程完成 =====")