#!/usr/bin/env python3
"""
Script cuối cùng để convert PlantUML thành URL Kroki
Sử dụng phương pháp khác để tránh lỗi 400
"""

import sys
import base64
import zlib
import argparse
import urllib.parse
from pathlib import Path

def encode_plantuml_to_kroki(plantuml_code, format='svg'):
    """
    Encode PlantUML code thành URL Kroki với phương pháp mới
    
    Args:
        plantuml_code (str): PlantUML code
        format (str): Output format (svg, png, pdf)
    
    Returns:
        str: Kroki URL
    """
    try:
        # Loại bỏ whitespace thừa và normalize
        plantuml_code = plantuml_code.strip()
        
        # Thêm newline nếu cần
        if not plantuml_code.endswith('\n'):
            plantuml_code += '\n'
        
        # Compress với deflate (level 9)
        compressed = zlib.compress(plantuml_code.encode('utf-8'), level=9)
        
        # Encode thành base64 với urlsafe
        encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
        
        # Loại bỏ padding '='
        encoded = encoded.rstrip('=')
        
        # Tạo URL Kroki
        kroki_url = f"https://kroki.io/plantuml/{format}/{encoded}"
        
        return kroki_url
    except Exception as e:
        print(f"Lỗi khi encode: {e}")
        return None

def read_plantuml_file(file_path):
    """
    Đọc file PlantUML
    
    Args:
        file_path (str): Đường dẫn file .puml
    
    Returns:
        str: Nội dung file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        sys.exit(1)

def validate_plantuml_code(plantuml_code):
    """
    Validate PlantUML code
    
    Args:
        plantuml_code (str): PlantUML code
    
    Returns:
        bool: True nếu valid
    """
    # Kiểm tra có @startuml và @enduml
    if '@startuml' not in plantuml_code or '@enduml' not in plantuml_code:
        print("Cảnh báo: PlantUML code thiếu @startuml hoặc @enduml")
        return False
    
    # Kiểm tra độ dài
    if len(plantuml_code) > 50000:
        print("Cảnh báo: PlantUML code quá dài, có thể gây lỗi")
        return False
    
    return True

def generate_markdown_image(plantuml_code, format='svg', alt_text="Diagram"):
    """
    Tạo Markdown image tag với URL Kroki
    
    Args:
        plantuml_code (str): PlantUML code
        format (str): Output format
        alt_text (str): Alt text cho image
    
    Returns:
        str: Markdown image tag
    """
    kroki_url = encode_plantuml_to_kroki(plantuml_code, format)
    if kroki_url:
        return f"![{alt_text}]({kroki_url})"
    else:
        return f"![{alt_text}](ERROR: Không thể tạo URL Kroki)"

def test_kroki_url(url):
    """
    Test URL Kroki có hoạt động không
    
    Args:
        url (str): Kroki URL
    
    Returns:
        bool: True nếu URL hợp lệ
    """
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.status == 200
    except Exception as e:
        print(f"Lỗi khi test URL: {e}")
        return False

def create_simple_test():
    """
    Tạo file test đơn giản
    """
    test_content = """@startuml
class User {
  -id: int
  -username: string
  +login()
}
@enduml"""
    
    with open('diagrams/test-simple.puml', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("Đã tạo file test: diagrams/test-simple.puml")

def main():
    parser = argparse.ArgumentParser(description='Convert PlantUML to Kroki URL (Final)')
    parser.add_argument('input_file', help='Input PlantUML file (.puml)')
    parser.add_argument('--format', choices=['svg', 'png', 'pdf'], default='svg',
                       help='Output format (default: svg)')
    parser.add_argument('--markdown', action='store_true',
                       help='Generate Markdown image tag')
    parser.add_argument('--alt-text', default='Diagram',
                       help='Alt text for Markdown image')
    parser.add_argument('--test', action='store_true',
                       help='Test if URL works')
    parser.add_argument('--create-test', action='store_true',
                       help='Create simple test file')
    
    args = parser.parse_args()
    
    if args.create_test:
        create_simple_test()
        return
    
    # Đọc file PlantUML
    plantuml_code = read_plantuml_file(args.input_file)
    
    # Validate PlantUML code
    if not validate_plantuml_code(plantuml_code):
        print("PlantUML code không hợp lệ!")
        sys.exit(1)
    
    # Tạo URL Kroki
    kroki_url = encode_plantuml_to_kroki(plantuml_code, args.format)
    
    if not kroki_url:
        print("Không thể tạo URL Kroki!")
        sys.exit(1)
    
    # Test URL nếu được yêu cầu
    if args.test:
        print("Đang test URL...")
        if test_kroki_url(kroki_url):
            print("✅ URL hoạt động!")
        else:
            print("❌ URL không hoạt động!")
            print("Thử tạo file test đơn giản...")
            create_simple_test()
            print("Chạy: python3 scripts/plantuml_to_kroki_final.py diagrams/test-simple.puml --test")
    
    if args.markdown:
        # Tạo Markdown image tag
        markdown_tag = generate_markdown_image(plantuml_code, args.format, args.alt_text)
        print("Markdown image tag:")
        print(markdown_tag)
    else:
        # In URL Kroki
        print("URL Kroki:")
        print(kroki_url)
    
    # In thông tin debug
    print(f"\nThông tin debug:")
    print(f"- Độ dài PlantUML code: {len(plantuml_code)} ký tự")
    print(f"- Format: {args.format}")
    print(f"- File: {args.input_file}")
    print(f"- URL length: {len(kroki_url)} ký tự")

if __name__ == "__main__":
    main()
