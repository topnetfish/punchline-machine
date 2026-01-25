import json
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SOURCE_INDEX = os.path.join(PROJECT_ROOT, "comic-index.json")
TARGET_INDEX = os.path.join(OUTPUT_DIR, "comic-index.json")

def build_index():
    if not os.path.exists(SOURCE_INDEX):
        raise RuntimeError("comic-index.json 不存在，请先生成漫画")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(SOURCE_INDEX, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 只给前端需要的字段（非常重要）
    frontend_data = {
        "comics": [
            {
                "id": c["id"],
                "title": c["title"],
                "category": c["category"],
                "topic": c["topic"],
                "img": c["img"],
                "html": c["html"],
                "create_time": c["create_time"]
            }
            for c in data.get("comics", [])
        ]
    }

    with open(TARGET_INDEX, "w", encoding="utf-8") as f:
        json.dump(frontend_data, f, ensure_ascii=False, indent=2)

    print("✅ 前端 comic-index.json 已生成")

if __name__ == "__main__":
    build_index()
