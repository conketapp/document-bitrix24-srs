#!/usr/bin/env python3
"""
Script nâng cao: Export PlantUML sang ảnh và chèn vào Markdown
"""

import os
import sys
import subprocess
import re
import tempfile
import shutil
from datetime import datetime
import argparse

def generate_plantuml_image(plantuml_code, output_dir="diagrams/images", filename=None, format_type="png"):
    """Generate ảnh từ PlantUML code với nhiều format"""
    try:
        # Tạo thư mục output nếu chưa có
        os.makedirs(output_dir, exist_ok=True)
        
        # Tạo filename nếu chưa có
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"plantuml_{timestamp}"
        
        # Tạo file PlantUML tạm thời
        temp_puml = os.path.join(tempfile.gettempdir(), f"{filename}.puml")
        with open(temp_puml, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
        
        # Generate ảnh với format cụ thể
        output_file = os.path.join(output_dir, f"{filename}.{format_type}")
        
        if format_type == "png":
            result = subprocess.run(['java', '-jar', 'plantuml.jar', temp_puml, '-o', output_dir], 
                                  capture_output=True, text=True)
        elif format_type == "svg":
            result = subprocess.run(['java', '-jar', 'plantuml.jar', '-tsvg', temp_puml, '-o', output_dir], 
                                  capture_output=True, text=True)
        elif format_type == "pdf":
            result = subprocess.run(['java', '-jar', 'plantuml.jar', '-tpdf', temp_puml, '-o', output_dir], 
                                  capture_output=True, text=True)
        else:
            print(f"❌ Format không hỗ trợ: {format_type}")
            return None
        
        # Cleanup temp file
        os.remove(temp_puml)
        
        if result.returncode == 0 or os.path.exists(output_file):
            print(f"✅ Đã tạo ảnh: {output_file}")
            return output_file
        else:
            print(f"⚠️ Có lỗi khi generate, nhưng có thể vẫn tạo được file")
            return output_file if os.path.exists(output_file) else None
            
    except Exception as e:
        print(f"❌ Lỗi khi generate ảnh: {e}")
        return None

def insert_image_to_md(md_file, image_path, caption=None, position="end", image_size=None):
    """Chèn ảnh vào file Markdown với tùy chọn size"""
    try:
        # Đọc file Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tạo đường dẫn tương đối
        relative_path = os.path.relpath(image_path, os.path.dirname(md_file))
        
        # Tạo markdown image syntax với size nếu có
        if image_size:
            image_md = f"\n<img src=\"{relative_path}\" alt=\"{caption or 'PlantUML Diagram'}\" width=\"{image_size}\">\n\n"
        else:
            if caption:
                image_md = f"\n![{caption}]({relative_path})\n\n*{caption}*\n"
            else:
                image_md = f"\n![PlantUML Diagram]({relative_path})\n"
        
        if position == "end":
            # Thêm vào cuối file
            new_content = content + image_md
        elif position == "start":
            # Thêm vào đầu file
            new_content = image_md + content
        else:
            # Thêm vào vị trí cụ thể
            lines = content.split('\n')
            try:
                pos = int(position)
                lines.insert(pos, image_md.strip())
                new_content = '\n'.join(lines)
            except ValueError:
                print(f"❌ Vị trí không hợp lệ: {position}")
                return False
        
        # Ghi lại file
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Đã chèn ảnh vào: {md_file}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi chèn ảnh: {e}")
        return False

def create_md_with_plantuml(plantuml_code, md_file, caption=None, position="end", format_type="png", image_size=None):
    """Tạo file Markdown với PlantUML"""
    try:
        # Generate ảnh
        image_path = generate_plantuml_image(plantuml_code, format_type=format_type)
        
        if not image_path:
            print("❌ Không thể tạo ảnh")
            return False
        
        # Tạo file Markdown nếu chưa có
        if not os.path.exists(md_file):
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# PlantUML Diagram\n\n")
        
        # Chèn ảnh vào Markdown
        return insert_image_to_md(md_file, image_path, caption, position, image_size)
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def process_plantuml_file(puml_file, md_file, caption=None, position="end", format_type="png", image_size=None):
    """Xử lý file PlantUML và chèn vào Markdown"""
    try:
        # Đọc file PlantUML
        with open(puml_file, 'r', encoding='utf-8') as f:
            plantuml_code = f.read()
        
        # Tạo caption từ tên file nếu chưa có
        if not caption:
            caption = os.path.splitext(os.path.basename(puml_file))[0].replace('-', ' ').title()
        
        return create_md_with_plantuml(plantuml_code, md_file, caption, position, format_type, image_size)
        
    except Exception as e:
        print(f"❌ Lỗi đọc file PlantUML: {e}")
        return False

def batch_process_plantuml_files(input_dir, output_dir, format_type="png"):
    """Xử lý hàng loạt các file PlantUML"""
    try:
        # Tạo thư mục output nếu chưa có
        os.makedirs(output_dir, exist_ok=True)
        
        # Tìm tất cả file .puml
        puml_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.puml'):
                    puml_files.append(os.path.join(root, file))
        
        if not puml_files:
            print(f"❌ Không tìm thấy file .puml trong: {input_dir}")
            return False
        
        print(f"🔍 Tìm thấy {len(puml_files)} file PlantUML")
        
        success_count = 0
        for puml_file in puml_files:
            # Tạo tên file output
            base_name = os.path.splitext(os.path.basename(puml_file))[0]
            md_file = os.path.join(output_dir, f"{base_name}.md")
            
            print(f"\n📝 Đang xử lý: {puml_file}")
            
            if process_plantuml_file(puml_file, md_file, format_type=format_type):
                success_count += 1
                print(f"✅ Đã tạo: {md_file}")
            else:
                print(f"❌ Lỗi khi xử lý: {puml_file}")
        
        print(f"\n🎉 Hoàn thành! Đã xử lý thành công {success_count}/{len(puml_files)} file")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi batch process: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Export PlantUML sang ảnh và chèn vào Markdown')
    parser.add_argument('--file', help='File PlantUML (.puml)')
    parser.add_argument('--code', help='PlantUML code trực tiếp')
    parser.add_argument('--output', required=True, help='File Markdown output')
    parser.add_argument('--caption', help='Caption cho ảnh')
    parser.add_argument('--position', default='end', help='Vị trí chèn (end/start/số)')
    parser.add_argument('--format', default='png', choices=['png', 'svg', 'pdf'], help='Format ảnh')
    parser.add_argument('--size', help='Kích thước ảnh (px)')
    parser.add_argument('--batch', help='Thư mục chứa file PlantUML để xử lý hàng loạt')
    parser.add_argument('--batch-output', help='Thư mục output cho batch process')
    
    args = parser.parse_args()
    
    print("🌿 Advanced PlantUML to Markdown")
    print("=" * 50)
    
    if args.batch:
        # Batch process
        if not args.batch_output:
            print("❌ Cần --batch-output cho batch process")
            return
        
        success = batch_process_plantuml_files(args.batch, args.batch_output, args.format)
    elif args.file:
        # Process từ file
        success = process_plantuml_file(args.file, args.output, args.caption, args.position, args.format, args.size)
    elif args.code:
        # Process từ code
        success = create_md_with_plantuml(args.code, args.output, args.caption, args.position, args.format, args.size)
    else:
        print("❌ Cần --file, --code hoặc --batch")
        print("\n💡 Ví dụ:")
        print("  python3 scripts/advanced_plantuml_to_md.py --file diagrams/test.puml --output output.md")
        print("  python3 scripts/advanced_plantuml_to_md.py --code '@startuml\nclass User\n@enduml' --output output.md")
        print("  python3 scripts/advanced_plantuml_to_md.py --batch diagrams --batch-output docs")
        return
    
    if success:
        print(f"\n✅ Hoàn thành!")
        if not args.batch:
            print(f"📁 File: {args.output}")
        print(f"📁 Ảnh được lưu trong: diagrams/images/")
    else:
        print("\n❌ Có lỗi xảy ra!")

if __name__ == "__main__":
    main()
