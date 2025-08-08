#!/usr/bin/env python3
"""
Script export PlantUML sang ảnh và chèn vào Markdown
"""

import os
import sys
import subprocess
import re
import tempfile
import shutil
from datetime import datetime

def generate_plantuml_image(plantuml_code, output_dir="diagrams/images", filename=None):
    """Generate ảnh từ PlantUML code"""
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
        
        # Generate PNG
        png_file = os.path.join(output_dir, f"{filename}.png")
        result = subprocess.run(['java', '-jar', 'plantuml.jar', temp_puml, '-o', output_dir], 
                              capture_output=True, text=True)
        
        # Cleanup temp file
        os.remove(temp_puml)
        
        if result.returncode == 0 or os.path.exists(png_file):
            print(f"✅ Đã tạo ảnh: {png_file}")
            return png_file
        else:
            print(f"⚠️ Có lỗi khi generate, nhưng có thể vẫn tạo được file")
            return png_file if os.path.exists(png_file) else None
            
    except Exception as e:
        print(f"❌ Lỗi khi generate ảnh: {e}")
        return None

def insert_image_to_md(md_file, image_path, caption=None, position="end"):
    """Chèn ảnh vào file Markdown"""
    try:
        # Đọc file Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tạo đường dẫn tương đối
        relative_path = os.path.relpath(image_path, os.path.dirname(md_file))
        
        # Tạo markdown image syntax
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

def create_md_with_plantuml(plantuml_code, md_file, caption=None, position="end"):
    """Tạo file Markdown với PlantUML"""
    try:
        # Generate ảnh
        image_path = generate_plantuml_image(plantuml_code)
        
        if not image_path:
            print("❌ Không thể tạo ảnh")
            return False
        
        # Tạo file Markdown nếu chưa có
        if not os.path.exists(md_file):
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# PlantUML Diagram\n\n")
        
        # Chèn ảnh vào Markdown
        return insert_image_to_md(md_file, image_path, caption, position)
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def process_plantuml_file(puml_file, md_file, caption=None, position="end"):
    """Xử lý file PlantUML và chèn vào Markdown"""
    try:
        # Đọc file PlantUML
        with open(puml_file, 'r', encoding='utf-8') as f:
            plantuml_code = f.read()
        
        # Tạo caption từ tên file nếu chưa có
        if not caption:
            caption = os.path.splitext(os.path.basename(puml_file))[0].replace('-', ' ').title()
        
        return create_md_with_plantuml(plantuml_code, md_file, caption, position)
        
    except Exception as e:
        print(f"❌ Lỗi đọc file PlantUML: {e}")
        return False

def main():
    print("🌿 PlantUML to Markdown - Export ảnh và chèn vào MD")
    print("=" * 60)
    
    if len(sys.argv) < 3:
        print("📝 Cách sử dụng:")
        print("python3 scripts/plantuml_to_md.py <plantuml_code> <md_file> [caption] [position]")
        print("python3 scripts/plantuml_to_md.py --file <puml_file> <md_file> [caption] [position]")
        print("\n📁 Files có sẵn:")
        
        # Liệt kê các file .puml có sẵn
        puml_files = []
        for root, dirs, files in os.walk('diagrams'):
            for file in files:
                if file.endswith('.puml'):
                    puml_files.append(os.path.join(root, file))
        
        if puml_files:
            for i, file in enumerate(puml_files, 1):
                print(f"  {i}. {file}")
        else:
            print("  Không có file .puml nào")
        
        print("\n💡 Ví dụ:")
        print("  python3 scripts/plantuml_to_md.py '@startuml\nclass User\n@enduml' output.md 'User Class'")
        print("  python3 scripts/plantuml_to_md.py --file diagrams/test-plantuml.puml output.md 'Test Diagram'")
        print("\n🎯 Vị trí chèn:")
        print("  end    - Chèn vào cuối file (mặc định)")
        print("  start  - Chèn vào đầu file")
        print("  <số>   - Chèn vào dòng số cụ thể")
        return
    
    if sys.argv[1] == "--file":
        if len(sys.argv) < 4:
            print("❌ Thiếu tham số")
            return
        
        puml_file = sys.argv[2]
        md_file = sys.argv[3]
        caption = sys.argv[4] if len(sys.argv) > 4 else None
        position = sys.argv[5] if len(sys.argv) > 5 else "end"
        
        success = process_plantuml_file(puml_file, md_file, caption, position)
    else:
        plantuml_code = sys.argv[1]
        md_file = sys.argv[2]
        caption = sys.argv[3] if len(sys.argv) > 3 else None
        position = sys.argv[4] if len(sys.argv) > 4 else "end"
        
        success = create_md_with_plantuml(plantuml_code, md_file, caption, position)
    
    if success:
        print(f"\n✅ Hoàn thành! Đã tạo ảnh và chèn vào: {md_file}")
        print(f"📁 Ảnh được lưu trong: diagrams/images/")
    else:
        print("\n❌ Có lỗi xảy ra!")

if __name__ == "__main__":
    main()
