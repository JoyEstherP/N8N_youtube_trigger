# import sys
# from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# video_path = sys.argv[1]
# quote = sys.argv[2]

# output_folder = "C:/Users/joy/Output"
# font_path = "C:/Users/joy/Fonts/BebasNeue.ttf"  # Or use "Arial"

# video = VideoFileClip(video_path)
# words = quote.split()
# clips = []

# for i, word in enumerate(words):
#     txt = TextClip(word, fontsize=48, font=font_path, color='white')
#     txt = txt.set_position('center').set_start(i * 0.5).set_duration(video.duration - i * 0.5)
#     clips.append(txt)

# final = CompositeVideoClip([video] + clips)
# safe_name = "".join(c if c.isalnum() else "_" for c in quote[:20])
# final.write_videofile(f"{output_folder}/{safe_name}_captioned.mp4", fps=24)




# caption_typewriter.py

# import sys
# from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# video_path = sys.argv[1]
# quote = sys.argv[2]

# clip = VideoFileClip(video_path)

# # Typewriter: Show one more word every 0.4 seconds
# words = quote.split()
# duration_per_step = 0.4
# text_clips = []

# for i in range(1, len(words) + 1):
#     partial_text = ' '.join(words[:i])
#     txt_clip = TextClip(
#         partial_text,
#         fontsize=48,
#         color='white',
#         font='Arial-Bold',
#         method='caption',
#         size=(clip.w * 0.8, None)
#     ).set_position('center').set_duration(duration_per_step)
    
#     text_clips.append(txt_clip)

# # Concatenate all steps
# typing_text = concatenate_videoclips(text_clips, method="compose")

# # Extend to match the video length (after the animation ends)
# if typing_text.duration < clip.duration:
#     last_text = text_clips[-1].set_duration(clip.duration - typing_text.duration)
#     typing_text = concatenate_videoclips([typing_text, last_text])

# final = CompositeVideoClip([clip, typing_text])
# final.write_videofile("output_with_typewriter.mp4", codec="libx264")


# import sys
# import os
# from PIL import Image, ImageDraw, ImageFont
# from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips

# # --- INPUT ARGS ---
# video_path = sys.argv[1]
# quote = sys.argv[2]

# # --- LOAD VIDEO ---
# clip = VideoFileClip(video_path)

# # --- FONT CONFIG ---
# font_path = r"C:\Users\joshu\OneDrive\Dokumen\YoutubeProjects\Bebas_Neue\bebasNeue.ttf"  # You can change this to another TTF font
# font_size = 48
# font_color = "white"
# bg_color = (0, 0, 0, 0)  # Transparent

# # --- SETTINGS ---
# duration_per_word = 0.4
# video_size = (clip.w, clip.h)
# max_width = int(clip.w * 0.8)

# # --- TYPEWRITER TEXT AS IMAGECLIPS ---
# words = quote.split()
# image_clips = []

# for i in range(1, len(words) + 1):
#     partial_text = ' '.join(words[:i])

#     # Create transparent image
#     img = Image.new("RGBA", video_size, bg_color)
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype(font_path, font_size)

#     # Calculate position (center)
#     text_size = draw.textbbox((0, 0), partial_text, font=font)
#     text_width = text_size[2] - text_size[0]
#     text_height = text_size[3] - text_size[1]
#     x = (video_size[0] - text_width) // 2
#     y = (video_size[1] - text_height) // 2

#     # Draw text
#     draw.text((x, y), partial_text, font=font, fill=font_color)

#     # Convert to MoviePy ImageClip
#     frame = ImageClip(img).set_duration(duration_per_word)
#     image_clips.append(frame)

# # --- CONCATENATE TEXT IMAGE CLIPS ---
# typing_clip = concatenate_videoclips(image_clips, method="compose")

# # --- EXTEND FINAL FRAME TO MATCH VIDEO LENGTH ---
# if typing_clip.duration < clip.duration:
#     last_frame = image_clips[-1].set_duration(clip.duration - typing_clip.duration)
#     typing_clip = concatenate_videoclips([typing_clip, last_frame])

# # --- OVERLAY ON VIDEO ---
# final = CompositeVideoClip([clip, typing_clip])
# output_path = os.path.join(os.path.dirname(video_path), "output_no_magick.mp4")
# final.write_videofile(output_path, codec="libx264")

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import numpy as np
import sys
import os
import textwrap
# --- Input arguments ---
video_path = sys.argv[1]
quote = sys.argv[2]
output_filename = sys.argv[3]  # Example: "quote_clip_01" (no .mp4)

# --- Load video ---
clip = VideoFileClip(video_path)

# --- Styling config ---
font_path = r"C:\Users\joshu\OneDrive\Dokumen\YoutubeProjects\Bebas_Neue\bebasNeue.ttf"
font_size = 64  # Bigger size
font_color = "white"
bg_color = (0, 0, 0, 0)
video_size = (clip.w, clip.h)
duration_per_word = 0.4

words = quote.split()
image_clips = []

for i in range(1, len(words) + 1):
    partial_text = ' '.join(words[:i])
    img = Image.new("RGBA", video_size, bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)

    # --- Wrap the text so it doesn't overflow ---
    max_width = int(video_size[0] * 0.8)  # 80% of video width
    lines = []
    current_line = ''
    for word in partial_text.split():
        test_line = f"{current_line} {word}".strip()
        test_width = draw.textbbox((0, 0), test_line, font=font)[2]
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    # --- Measure text block height ---
    line_height = font.getbbox("Ay")[3] + 10
    total_height = line_height * len(lines)

    # --- Draw background box ---
    text_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
    x = (video_size[0] - text_width) // 2
    y = (video_size[1] - total_height) // 2

    padding = 30
    rect_x0 = x - padding
    rect_y0 = y - padding
    rect_x1 = x + text_width + padding
    rect_y1 = y + total_height + padding
    draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=(0, 0, 0, 150))  # Semi-transparent box

    # --- Draw each line of text ---
    for j, line in enumerate(lines):
        line_width = draw.textbbox((0, 0), line, font=font)[2]
        line_x = (video_size[0] - line_width) // 2
        line_y = y + j * line_height
        draw.text((line_x, line_y), line, font=font, fill=font_color)
        draw.text((line_x + 1, line_y), line, font=font, fill=font_color)  # Simulated bold

    frame = ImageClip(np.array(img)).set_duration(duration_per_word)
    image_clips.append(frame)


# --- Assemble typewriter effect ---
typing_clip = concatenate_videoclips(image_clips, method="compose")

# --- Pad to full video duration ---
if typing_clip.duration < clip.duration:
    last_frame = image_clips[-1].set_duration(clip.duration - typing_clip.duration)
    typing_clip = concatenate_videoclips([typing_clip, last_frame])

final = CompositeVideoClip([clip, typing_clip])

# --- Output ---
output_dir = os.path.dirname(video_path)
safe_filename = output_filename.strip().replace(" ", "_") + ".mp4"
output_path = os.path.join(output_dir, safe_filename)

final.write_videofile(output_path, codec="libx264", preset="ultrafast", fps=24)

