from PIL import Image, ImageDraw, ImageFont
import os

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_image(filename, width, height, text, bg_color=(255, 255, 255), text_color=(44, 82, 130)):
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw placeholder text
    font_size = 40
    try:
        font = ImageFont.truetype("Arial", font_size)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=text_color)
    return img

def main():
    # Create images directory if it doesn't exist
    create_directory_if_not_exists('static/images')
    
    # Image configurations
    images = [
        ('logo.png', 'Resume Coach RAG'),
        ('problem.png', 'Problem Statement'),
        ('research.png', 'Research & Solution'),
        ('architecture.png', 'Technical Architecture'),
        ('pipeline.png', 'Processing Pipeline'),
        ('results.png', 'Results & Metrics'),
        ('features.png', 'Features Demo'),
        ('future.png', 'Future Work'),
        ('contact.png', 'Contact Info')
    ]
    
    # Generate images
    for filename, text in images:
        img = create_image(filename, 800, 600, text)
        img.save(f'static/images/{filename}')

if __name__ == '__main__':
    main() 