#!/usr/bin/env python3
"""
Script setup PlantUML cho VS Code
"""

import os
import json
import subprocess
import sys

def check_java():
    """Kiểm tra Java đã cài đặt chưa"""
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java đã được cài đặt")
            return True
        else:
            print("❌ Java chưa được cài đặt")
            return False
    except FileNotFoundError:
        print("❌ Java chưa được cài đặt")
        return False

def check_plantuml_jar():
    """Kiểm tra PlantUML JAR file"""
    if os.path.exists('plantuml.jar'):
        print("✅ PlantUML JAR file đã tồn tại")
        return True
    else:
        print("❌ PlantUML JAR file chưa tồn tại")
        return False

def download_plantuml():
    """Tải PlantUML JAR file"""
    print("Đang tải PlantUML...")
    try:
        subprocess.run([
            'curl', '-L', '-o', 'plantuml.jar',
            'https://github.com/plantuml/plantuml/releases/download/v1.2025.4/plantuml-1.2025.4.jar'
        ], check=True)
        print("✅ Đã tải PlantUML thành công")
        return True
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi tải PlantUML")
        return False

def create_vscode_settings():
    """Tạo VS Code settings cho PlantUML"""
    settings = {
        "plantuml.server": "PlantUMLServer",
        "plantuml.render": "PlantUMLServer",
        "plantuml.exportFormat": "png",
        "plantuml.plantumlServer": "https://www.plantuml.com/plantuml",
        "plantuml.diagramsRoot": "diagrams",
        "plantuml.exportOutDir": "diagrams/images"
    }
    
    # Tạo thư mục .vscode nếu chưa có
    os.makedirs('.vscode', exist_ok=True)
    
    # Ghi settings
    with open('.vscode/settings.json', 'w') as f:
        json.dump(settings, f, indent=2)
    
    print("✅ Đã tạo VS Code settings")

def create_plantuml_test():
    """Tạo file test PlantUML"""
    test_content = """@startuml
!theme plain
skinparam classAttributeIconSize 0

class User {
  -id: int
  -username: string
  -email: string
  +login()
  +logout()
}

class Product {
  -id: int
  -name: string
  -price: decimal
  +create()
  +update()
}

User ||--o{ Order : places
Product ||--o{ OrderItem : contains
@enduml"""
    
    with open('diagrams/test-plantuml.puml', 'w') as f:
        f.write(test_content)
    
    print("✅ Đã tạo file test PlantUML: diagrams/test-plantuml.puml")

def test_plantuml():
    """Test PlantUML"""
    print("Đang test PlantUML...")
    try:
        result = subprocess.run(['java', '-jar', 'plantuml.jar', 'diagrams/test-plantuml.puml'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PlantUML hoạt động!")
            print("📁 File đã được tạo: diagrams/test-plantuml.png")
        else:
            print("⚠️ PlantUML có thể hoạt động với một số hạn chế")
            print("Lỗi:", result.stderr)
    except Exception as e:
        print(f"❌ Lỗi khi test PlantUML: {e}")

def print_instructions():
    """In hướng dẫn sử dụng"""
    print("\n" + "="*50)
    print("HƯỚNG DẪN SỬ DỤNG PLANTUML TRONG VS CODE")
    print("="*50)
    
    print("\n1. Cài đặt Extension:")
    print("   - Mở VS Code")
    print("   - Nhấn Ctrl+Shift+X")
    print("   - Tìm 'PlantUML'")
    print("   - Cài đặt extension 'PlantUML' của jebbs")
    
    print("\n2. Xem Preview:")
    print("   - Mở file .puml trong VS Code")
    print("   - Nhấn Alt+Shift+P")
    print("   - Chọn 'PlantUML: Preview Current Diagram'")
    
    print("\n3. Export Diagram:")
    print("   - Nhấn Alt+Shift+P")
    print("   - Chọn 'PlantUML: Export Current Diagram'")
    print("   - Chọn format: PNG, SVG, PDF")
    
    print("\n4. Test ngay:")
    print("   - Mở file: diagrams/test-plantuml.puml")
    print("   - Xem preview hoặc export")
    
    print("\n5. Sử dụng với Java:")
    print("   - java -jar plantuml.jar diagrams/your-file.puml")
    print("   - java -jar plantuml.jar -tsvg diagrams/your-file.puml")

def main():
    print("🔧 Setup PlantUML cho VS Code")
    print("="*40)
    
    # Kiểm tra Java
    if not check_java():
        print("\n❌ Vui lòng cài đặt Java trước:")
        print("   curl -s 'https://get.sdkman.io' | bash")
        print("   source '$HOME/.sdkman/bin/sdkman-init.sh'")
        print("   sdk install java 17.0.2-open")
        return
    
    # Kiểm tra PlantUML
    if not check_plantuml_jar():
        if not download_plantuml():
            return
    
    # Tạo settings
    create_vscode_settings()
    
    # Tạo file test
    create_plantuml_test()
    
    # Test PlantUML
    test_plantuml()
    
    # In hướng dẫn
    print_instructions()

if __name__ == "__main__":
    main()
