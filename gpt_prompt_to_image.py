from openai import OpenAI
import base64
import time

client = OpenAI()

# ========= 1️⃣ 中文想法 =========
idea_cn = "一只很可爱的Q版小猫，卡通风格，明亮配色，适合做表情包"

# ========= 2️⃣ 用 GPT 生成英文绘画 Prompt =========
prompt_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a professional AI art prompt engineer."
        },
        {
            "role": "user",
            "content": f"""
请把下面的中文描述，改写成一个高质量的英文绘画 prompt，
适合用在 AI 图像生成模型中。

要求：
- 英文
- 描述清晰、具体
- 偏向卡通 / Q版风格
- 不要出现任何文字或水印相关描述

中文描述：
{idea_cn}
"""
        }
    ]
)

image_prompt = prompt_response.choices[0].message.content.strip()

print("🎨 生成的绘画 Prompt：")
print(image_prompt)
print("-" * 50)

# ========= 3️⃣ 用 prompt 生成图片 =========
image_result = client.images.generate(
    model="gpt-image-1",
    prompt=image_prompt,
    size="1024x1024"
)

image_base64 = image_result.data[0].b64_json
filename = f"cat_{int(time.time())}.png"

with open(filename, "wb") as f:
    f.write(base64.b64decode(image_base64))

print(f"✅ 图片生成成功：{filename}")
