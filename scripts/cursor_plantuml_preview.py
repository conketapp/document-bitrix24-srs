#!/usr/bin/env python3
"""
Script preview PlantUML trực tiếp trong Cursor
"""

import os
import sys
import subprocess
import webbrowser
import zlib
import base64
import tempfile
import json

def generate_kroki_url(plantuml_code, format_type="svg"):
    """Generate Kroki URL từ PlantUML code"""
    try:
        # Thêm newline nếu chưa có
        if not plantuml_code.endswith('\n'):
            plantuml_code += '\n'
        
        # Compress với zlib (deflate)
        compressed = zlib.compress(plantuml_code.encode('utf-8'), level=9)
        
        # Encode base64 và loại bỏ padding
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii').rstrip('=')
        
        # Tạo Kroki URL
        kroki_url = f"https://kroki.io/plantuml/{format_type}/{encoded}"
        
        return kroki_url
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo Kroki URL: {e}")
        return None

def create_html_preview(plantuml_code, title="PlantUML Preview"):
    """Tạo file HTML để preview PlantUML"""
    kroki_url = generate_kroki_url(plantuml_code)
    
    if not kroki_url:
        return None
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 15px 20px;
            font-size: 18px;
            font-weight: 600;
        }}
        .content {{
            padding: 20px;
        }}
        .diagram {{
            text-align: center;
            margin: 20px 0;
        }}
        .diagram img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .code-section {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            margin: 20px 0;
        }}
        .code-header {{
            background: #e9ecef;
            padding: 10px 15px;
            font-weight: 600;
            border-bottom: 1px solid #e9ecef;
        }}
        .code-content {{
            padding: 15px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            line-height: 1.4;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .buttons {{
            margin: 20px 0;
            text-align: center;
        }}
        .btn {{
            display: inline-block;
            padding: 10px 20px;
            margin: 0 5px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 500;
        }}
        .btn:hover {{
            background: #0056b3;
        }}
        .btn-secondary {{
            background: #6c757d;
        }}
        .btn-secondary:hover {{
            background: #545b62;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            🌿 PlantUML Preview
        </div>
        <div class="content">
            <div class="diagram">
                <img src="{kroki_url}" alt="PlantUML Diagram" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                <div style="display:none; padding:20px; color:#666; text-align:center;">
                    <p>⚠️ Không thể tải diagram. Vui lòng kiểm tra kết nối internet.</p>
                    <a href="{kroki_url}" target="_blank" class="btn">Mở trong tab mới</a>
                </div>
            </div>
            
            <div class="code-section">
                <div class="code-header">📝 PlantUML Code</div>
                <div class="code-content">{plantuml_code}</div>
            </div>
            
            <div class="buttons">
                <a href="{kroki_url}" target="_blank" class="btn">🔗 Mở Kroki</a>
                <a href="https://www.plantuml.com/plantuml/uml/" target="_blank" class="btn btn-secondary">🌐 Online Editor</a>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    # Tạo file HTML tạm thời
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        return f.name

def preview_in_cursor(plantuml_code, title="PlantUML Preview"):
    """Preview PlantUML trong Cursor"""
    try:
        # Tạo file HTML
        html_file = create_html_preview(plantuml_code, title)
        
        if html_file:
            print(f"🌐 Đang mở preview trong browser...")
            print(f"📁 File: {html_file}")
            
            # Mở file HTML trong browser
            webbrowser.open(f"file://{html_file}")
            
            print("✅ Đã mở preview trong browser!")
            print("💡 File HTML sẽ tự động xóa khi browser đóng")
            
            return html_file
        else:
            print("❌ Không thể tạo preview")
            return None
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None

def preview_from_file(plantuml_file):
    """Preview từ file PlantUML"""
    if not os.path.exists(plantuml_file):
        print(f"❌ File không tồn tại: {plantuml_file}")
        return False
    
    try:
        with open(plantuml_file, 'r', encoding='utf-8') as f:
            plantuml_code = f.read()
        
        title = f"PlantUML Preview - {os.path.basename(plantuml_file)}"
        preview_in_cursor(plantuml_code, title)
        return True
        
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return False

def main():
    print("🌿 PlantUML Preview trong Cursor")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        print("📝 Cách sử dụng:")
        print("python3 scripts/cursor_plantuml_preview.py <file.puml>")
        print("python3 scripts/cursor_plantuml_preview.py --code '<plantuml_code>'")
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
        print("  python3 scripts/cursor_plantuml_preview.py diagrams/test-plantuml.puml")
        print('  python3 scripts/cursor_plantuml_preview.py --code "@startuml\nclass User\n@enduml"')
        return
    
    if sys.argv[1] == "--code":
        if len(sys.argv) < 3:
            print("❌ Thiếu PlantUML code")
            return
        
        plantuml_code = sys.argv[2]
        preview_in_cursor(plantuml_code, "PlantUML Code Preview")
    else:
        plantuml_file = sys.argv[1]
        preview_from_file(plantuml_file)

if __name__ == "__main__":
    main()
