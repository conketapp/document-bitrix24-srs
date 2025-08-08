# 🧹 Kế hoạch dọn dẹp và cấu trúc lại file

## 📁 Cấu trúc hiện tại (cần dọn dẹp):

### 🔴 Files cần xóa (trùng lặp/không cần thiết):
- `TROUBLESHOOTING_NETWORK_ERROR.md` - Trùng với `SOLUTION_AGGREGATE_ERROR.md`
- `SOLUTION_AGGREGATE_ERROR.md` - Trùng với `FINAL_SOLUTION_AGGREGATE_ERROR.md`
- `CURSOR_PREVIEW_GUIDE.md` - Trùng với `PLANTUML_VSCODE_GUIDE.md`
- `PLANTUML_SUCCESS.md` - Thông tin đã cũ
- `PREVIEW_GUIDE.md` - Trùng với `PLANTUML_VSCODE_GUIDE.md`
- `test_mermaid_preview.md` - File test không cần thiết
- `java_installation_guide.md` - Thông tin đã cũ
- `direct_preview_example.md` - Trùng với `PLANTUML_VSCODE_GUIDE.md`
- `mermaid_example.md` - Không cần thiết
- `vscode_plantuml_guide.md` - Trùng với `PLANTUML_VSCODE_GUIDE.md`
- `TROUBLESHOOTING_400_ERROR.md` - Thông tin đã cũ
- `kroki_working_example.md` - Trùng với `kroki_plantuml_example.md`
- `SRS_with_kroki_example.md` - Trùng với `kroki_plantuml_example.md`
- `kroki_plantuml_example.md` - Thông tin đã cũ
- `plantuml_example.md` - Trùng với `PLANTUML_GUIDE.md`
- `test_output.md` - File test không cần thiết
- `test_user_class.md` - File test không cần thiết
- `advanced_test.md` - File test không cần thiết
- `graphviz.tar.gz` - File tải về không cần thiết

### 🔴 Scripts cần xóa (trùng lặp/không cần thiết):
- `plantuml_to_kroki.py` - Phiên bản cũ
- `plantuml_to_kroki_improved.py` - Phiên bản cũ
- `plantuml_to_kroki_correct.py` - Phiên bản cũ
- `plantuml_to_kroki.sh` - Không cần thiết
- `test_preview.py` - Không cần thiết
- `open_kroki_preview.py` - Trùng với `cursor_plantuml_preview.py`
- `plantuml_quick_preview.py` - Trùng với `quick_preview.py`

## 📁 Cấu trúc mới (sau khi dọn dẹp):

```
document bitrix24/
├── README.md                           # Hướng dẫn chính
├── PLANTUML_GUIDE.md                  # Hướng dẫn PlantUML chính
├── PLANTUML_VSCODE_GUIDE.md           # Hướng dẫn VS Code
├── FINAL_SOLUTION_AGGREGATE_ERROR.md  # Giải pháp lỗi AggregateError
├── PLANTUML_TO_MARKDOWN_GUIDE.md     # Hướng dẫn export to MD
├── scripts/
│   ├── setup_plantuml_vscode.py      # Setup PlantUML
│   ├── quick_preview.py              # Preview nhanh
│   ├── cursor_plantuml_preview.py    # Preview với HTML đẹp
│   ├── offline_plantuml_preview.py   # Preview offline
│   ├── plantuml_to_md.py            # Export to MD cơ bản
│   ├── advanced_plantuml_to_md.py   # Export to MD nâng cao
│   └── plantuml_to_kroki_final.py   # Generate Kroki URL
├── diagrams/
│   ├── *.puml                        # Files PlantUML
│   └── images/                       # Ảnh đã generate
├── .vscode/
│   └── settings.json                 # VS Code settings
├── plantuml.jar                      # PlantUML JAR
└── categories/                       # Thư mục SRS gốc
    └── ...
```

## 🎯 Lợi ích sau khi dọn dẹp:

### ✅ **Gọn gàng hơn:**
- Giảm từ 20+ files xuống 6 files chính
- Giảm từ 14 scripts xuống 7 scripts cần thiết
- Cấu trúc rõ ràng, dễ tìm

### ✅ **Dễ sử dụng hơn:**
- Chỉ giữ lại những gì cần thiết
- Không bị nhầm lẫn giữa các phiên bản
- Hướng dẫn rõ ràng

### ✅ **Dễ bảo trì hơn:**
- Ít file cần quản lý
- Không có file trùng lặp
- Cấu trúc logic
