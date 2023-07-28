import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
 
 
def create_image(cmd, ip, filename, key_file=None):
    # 셸 명령 실행
    if key_file:
        result = subprocess.run(f"ssh -oStrictHostKeyChecking=no -i {key_file} ec2-user@{ip} {cmd}", shell=True, capture_output=True, text=True)
    else:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
 
    # 텍스트 줄의 길이 계산
    lines = result.stdout.strip().split("\n")
    max_line_length = max([len(line) for line in lines])
 
    # 이미지 크기 설정
    padding = 10
    font_size = 14
    line_spacing = 5
    text_height = (font_size + line_spacing) * len(lines)
    image_width = max_line_length * font_size + 2 * padding
    image_height = text_height + 2 * padding
 
    # 이미지 생성
    background_color = (0, 0, 0)
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)
 
    # 폰트 설정
    font_path = "/usr/share/fonts/NanumGothicCoding.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255, 255, 255)
 
    # 텍스트 그리기
    y = padding
    for line in lines:
        draw.text((padding, y), line, font=font, fill=text_color)
        y += font_size + line_spacing
 
    # 이미지 저장
    save_dir = f"tmp/{ip}"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{filename}.png")
    image.save(save_path)