#!/usr/bin/env python3
"""
Script preview nhanh PlantUML code trực tiếp
"""

import sys
import webbrowser
import zlib
import base64

def quick_preview(plantuml_code):
    """Preview nhanh PlantUML code"""
    try:
        # Thêm newline nếu chưa có
        if not plantuml_code.endswith('\n'):
            plantuml_code += '\n'
        
        # Compress với zlib (deflate)
        compressed = zlib.compress(plantuml_code.encode('utf-8'), level=9)
        
        # Encode base64 và loại bỏ padding
        encoded = base64.urlsafe_b64encode(compressed).decode('ascii').rstrip('=')
        
        # Tạo Kroki URL
        kroki_url = f"https://kroki.io/plantuml/svg/{encoded}"
        
        print(f"🌐 Kroki URL: {kroki_url}")
        
        # Mở trong browser
        webbrowser.open(kroki_url)
        
        print("✅ Đã mở preview trong browser!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("📝 Cách sử dụng:")
        print("python3 scripts/quick_preview.py '<plantuml_code>'")
        print("\n💡 Ví dụ:")
        print('python3 scripts/quick_preview.py "@startuml\nclass User\n@enduml"')
        return
    
    plantuml_code = sys.argv[1]
    quick_preview(plantuml_code)

if __name__ == "__main__":
    main()
