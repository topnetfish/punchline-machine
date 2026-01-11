from openai import OpenAI
import base64
import time

client = OpenAI()

result = client.images.generate(
    model="gpt-image-1",
    prompt="Chibi cartoon style, cute cat, bright colors, no text",
    size="1024x1024"
)

image_base64 = result.data[0].b64_json
filename = f"cat_{int(time.time())}.png"

with open(filename, "wb") as f:
    f.write(base64.b64decode(image_base64))

print(f"✅ 图片生成成功：{filename}")
