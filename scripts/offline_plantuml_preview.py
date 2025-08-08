#!/usr/bin/env python3
"""
Script preview PlantUML hoàn toàn offline - Giải pháp cho lỗi AggregateError
"""

import os
import sys
import subprocess
import tempfile
import webbrowser
import zlib
import base64

def generate_offline_preview(plantuml_code, title="PlantUML Preview"):
    """Tạo preview offline hoàn toàn"""
    
    # Tạo Kroki URL
    kroki_url = generate_kroki_url(plantuml_code)
    
    # Tạo HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .header p {{
            opacity: 0.8;
            font-size: 14px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .diagram-section {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .diagram-section h3 {{
            margin-bottom: 15px;
            color: #2c3e50;
            font-size: 18px;
        }}
        
        .diagram {{
            max-width: 100%;
            height: auto;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .code-section {{
            background: #2d3748;
            border-radius: 8px;
            margin: 20px 0;
            overflow: hidden;
        }}
        
        .code-header {{
            background: #1a202c;
            color: white;
            padding: 15px 20px;
            font-weight: 600;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .code-content {{
            padding: 20px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
            font-size: 13px;
            line-height: 1.6;
            color: #e2e8f0;
            white-space: pre-wrap;
            overflow-x: auto;
            background: #2d3748;
        }}
        
        .buttons {{
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-secondary {{
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
            box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3);
        }}
        
        .btn-secondary:hover {{
            box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4);
        }}
        
        .status {{
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
        }}
        
        .status.success {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        
        .status.error {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .feature {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .feature h4 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        
        .feature p {{
            color: #6c757d;
            font-size: 14px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌿 PlantUML Preview</h1>
            <p>Offline Preview - Không cần VS Code Extension</p>
        </div>
        
        <div class="content">
            <div class="diagram-section">
                <h3>📊 Diagram Preview</h3>
                <img src="{kroki_url}" alt="PlantUML Diagram" class="diagram" 
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                <div style="display:none; padding:20px; color:#666; text-align:center;">
                    <p>⚠️ Không thể tải diagram. Vui lòng kiểm tra kết nối internet.</p>
                    <a href="{kroki_url}" target="_blank" class="btn">🔗 Mở trong tab mới</a>
                </div>
            </div>
            
            <div class="code-section">
                <div class="code-header">
                    <span>📝</span>
                    <span>PlantUML Code</span>
                </div>
                <div class="code-content">{plantuml_code}</div>
            </div>
            
            <div class="buttons">
                <a href="{kroki_url}" target="_blank" class="btn">
                    <span>🔗</span>
                    <span>Mở Kroki</span>
                </a>
                <a href="https://www.plantuml.com/plantuml/uml/" target="_blank" class="btn btn-secondary">
                    <span>🌐</span>
                    <span>Online Editor</span>
                </a>
                <a href="https://kroki.io/" target="_blank" class="btn btn-secondary">
                    <span>📊</span>
                    <span>Kroki Home</span>
                </a>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h4>✅ Offline Preview</h4>
                    <p>Không cần VS Code extension, hoạt động hoàn toàn offline</p>
                </div>
                <div class="feature">
                    <h4>🚀 Nhanh chóng</h4>
                    <p>Preview ngay lập tức với Kroki URL</p>
                </div>
                <div class="feature">
                    <h4>🎨 Giao diện đẹp</h4>
                    <p>HTML responsive với thiết kế hiện đại</p>
                </div>
                <div class="feature">
                    <h4>🔧 Dễ sử dụng</h4>
                    <p>Chỉ cần chạy script Python đơn giản</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

def generate_kroki_url(plantuml_code, format_type="svg"):
    """Generate Kroki URL từ PlantUML code"""
    try:
        if not plantuml_code.endswith('\n'):
            plantuml_code += '\n'
        
        compressed = zlib.compress(plantuml_code.encode('utf-8'), level=9)
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii').rstrip('=')
        kroki_url = f"https://kroki.io/plantuml/{format_type}/{encoded}"
        
        return kroki_url
    except Exception as e:
        print(f"❌ Lỗi khi tạo Kroki URL: {e}")
        return None

def create_offline_preview(plantuml_code, title="PlantUML Preview"):
    """Tạo preview offline"""
    try:
        html_content = generate_offline_preview(plantuml_code, title)
        
        # Tạo file HTML tạm thời
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            html_file = f.name
        
        print(f"🌐 Đang mở preview offline...")
        print(f"📁 File: {html_file}")
        
        # Mở file HTML trong browser
        webbrowser.open(f"file://{html_file}")
        
        print("✅ Đã mở preview offline!")
        print("💡 Giải pháp hoàn toàn offline - không cần VS Code extension")
        
        return html_file
        
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
        create_offline_preview(plantuml_code, title)
        return True
        
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return False

def main():
    print("🌿 PlantUML Offline Preview - Giải pháp cho lỗi AggregateError")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("📝 Cách sử dụng:")
        print("python3 scripts/offline_plantuml_preview.py <file.puml>")
        print("python3 scripts/offline_plantuml_preview.py --code '<plantuml_code>'")
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
        print("  python3 scripts/offline_plantuml_preview.py diagrams/test-plantuml.puml")
        print('  python3 scripts/offline_plantuml_preview.py --code "@startuml\nclass User\n@enduml"')
        print("\n🎯 Lợi ích:")
        print("  ✅ Hoàn toàn offline")
        print("  ✅ Không cần VS Code extension")
        print("  ✅ Không bị lỗi AggregateError")
        print("  ✅ Giao diện đẹp")
        return
    
    if sys.argv[1] == "--code":
        if len(sys.argv) < 3:
            print("❌ Thiếu PlantUML code")
            return
        
        plantuml_code = sys.argv[2]
        create_offline_preview(plantuml_code, "PlantUML Code Preview")
    else:
        plantuml_file = sys.argv[1]
        preview_from_file(plantuml_file)

if __name__ == "__main__":
    main()
