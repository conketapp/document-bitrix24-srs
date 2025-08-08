# 📋 SRS Documentation System

## 🎯 Mục đích
Hệ thống tài liệu Software Requirements Specification (SRS) cho dự án quản lý dự án và tài sản Agribank, bao gồm 58 user stories được tổ chức theo module và chức năng.

## 📊 Tổng quan

### 📈 Thống kê
- **Tổng số SRS**: 58 files
- **Ngôn ngữ**: Tiếng Việt
- **Định dạng**: Markdown (.md)
- **Diagrams**: PlantUML (.puml)
- **Web Preview**: HTML + Bootstrap

### 🏗️ Cấu trúc Modules

| Module | Số lượng | Mô tả |
|--------|----------|-------|
| **CP** (Chi phí) | 14 SRS | Quản lý chi phí dự án |
| **TSDV** (Tài sản & Dịch vụ) | 8 SRS | Quản lý tài sản và dịch vụ |
| **BC** (Báo cáo) | 3 SRS | Báo cáo và thống kê |
| **HD** (Hợp đồng) | 8 SRS | Quản lý hợp đồng |
| **DMDA** (Danh mục dự án) | 17 SRS | Quản lý danh mục dự án |
| **GT** (Gói thầu) | 8 SRS | Quản lý gói thầu |

## 📁 Cấu trúc Dự án

```
document-bitrix24/
├── 📋 SRS_INDEX.md                    # Index tổng hợp tất cả SRS
├── 📊 diagrams/                       # PlantUML diagrams
│   ├── 📋 README.md                   # Hướng dẫn diagrams
│   ├── 🚀 QUICK_ACCESS.md            # Truy cập nhanh diagrams
│   ├── 📈 DIAGRAMS_INDEX.md          # Index diagrams
│   ├── 🎨 cp-*.puml                  # CP series diagrams
│   ├── 🏗️ tsdv-*.puml                # TSDV series diagrams
│   └── 📊 *.png                      # Generated images
├── 📄 SRS_Project_Category_*.md      # 52 SRS files
├── 🌐 docs/                          # Web preview
│   └── 📄 index.html                 # Main web page
├── ⚙️ .github/workflows/             # GitHub Actions
│   └── 📄 deploy.yml                 # Auto-deploy
├── 🚀 netlify.toml                   # Netlify config
└── 📖 README.md                      # File này
```

## 🚀 Cách sử dụng

### 📖 Đọc tài liệu

#### 1. **Xem Index tổng hợp:**
```bash
# Mở file index chính
open SRS_INDEX.md
```

#### 2. **Tìm kiếm SRS cụ thể:**
```bash
# Tìm theo module
grep -r "CP-1.1" .

# Tìm theo chức năng
grep -r "chi phí" SRS_Project_Category_CP-*.md
```

#### 3. **Xem Diagrams:**
```bash
# Mở diagrams index
open diagrams/DIAGRAMS_INDEX.md

# Xem quick access
open diagrams/QUICK_ACCESS.md
```

### 🌐 Preview Online

#### **Cách 1: GitHub Pages**
1. Push code lên GitHub
2. Vào Settings > Pages
3. Source: Deploy from branch
4. URL: `https://your-username.github.io/your-repo`

#### **Cách 2: Netlify**
1. Đăng ký tại https://netlify.com
2. Drag & drop folder `docs`
3. URL tự động được tạo

#### **Cách 3: Vercel**
1. Import GitHub repo vào Vercel
2. Deploy tự động

### 🎨 Xem Diagrams

#### **Online Preview:**
- **PlantUML Online:** https://www.plantuml.com/plantuml/
- **Kroki:** https://kroki.io/
- **Mermaid Live:** https://mermaid.live/

#### **Local Preview:**
```bash
# Cài đặt PlantUML
brew install plantuml

# Generate PNG từ PUML
plantuml diagrams/cp-1.1-activity-diagram.puml
```

## 📋 Danh sách SRS

### 🏢 CP Series - Chi phí (14 SRS)

#### CP-1.x: Quản lý Chi phí Cơ bản
- **CP-1.1**: [Tạo khoản mục chi phí mới và nhập thông tin chi tiết](SRS_Project_Category_CP-1.1.md)
- **CP-1.2**: [Liên kết khoản mục chi phí với Dự án, Gói thầu và Hợp đồng](SRS_Project_Category_CP-1.2.md)
- **CP-1.3**: [Cập nhật Trạng thái Thanh toán](SRS_Project_Category_CP-1.3.md)

#### CP-2.x: Chỉnh sửa và Xóa Chi phí
- **CP-2.1**: [Chỉnh sửa thông tin khoản mục chi phí](SRS_Project_Category_CP-2.1.md)
- **CP-2.2**: [Xóa khoản mục chi phí](SRS_Project_Category_CP-2.2.md)

#### CP-3.x: Đính kèm và Quản lý Tài liệu
- **CP-3.1**: [Đính kèm chứng từ/hóa đơn cho khoản mục chi phí](SRS_Project_Category_CP-3.1.md)

#### CP-4.x: Phê duyệt và Quy trình
- **CP-4.1**: [Đính kèm Tác vụ đến Khoản mục Chi phí](SRS_Project_Category_CP-4.1.md)
- **CP-4.2**: [Xem và Truy cập Chi phí liên quan từ Tác vụ](SRS_Project_Category_CP-4.2.md)

#### CP-5.x: Báo cáo và Phân tích
- **CP-5.1**: [Ghi nhận Lịch sử Thao tác Chi phí (Log)](SRS_Project_Category_CP-5.1.md)
- **CP-5.2**: [Tìm kiếm & Lọc Chi phí Đa tiêu chí](SRS_Project_Category_CP-5.2.md)
- **CP-5.3**: [Tổng hợp & Báo cáo Chi phí theo Dự án/Gói thầu/Hợp đồng](SRS_Project_Category_CP-5.3.md)
- **CP-5.4**: [Xuất Dữ liệu Chi phí ra Excel](SRS_Project_Category_CP-5.4.md)
- **CP-5.5**: [Hiển thị các Chỉ số Tài chính & Tiến độ Tổng hợp của Dự án](SRS_Project_Category_CP-5.5.md)
- **CP-5.6**: [Cảnh báo khi Tổng Chi phí Vượt quá Ngân sách Dự án](SRS_Project_Category_CP-5.6.md)

### 🏗️ TSDV Series - Tài sản & Dịch vụ (8 SRS)

#### TSDV-1.x: Tạo và Quản lý Tài sản/Dịch vụ
- **TSDV-1.1**: [Tạo mới một Tài sản/Dịch vụ đầu ra từ dự án](SRS_Project_Category_TSDV-1.1.md)
- **TSDV-1.2**: [Chỉnh sửa thông tin Tài sản/Dịch vụ](SRS_Project_Category_TSDV-1.2.md)
- **TSDV-1.3**: [Xóa Tài sản/Dịch vụ](SRS_Project_Category_TSDV-1.3.md)

#### TSDV-2.x: Quản lý Danh mục và Phân loại
- **TSDV-2.1**: [Quản lý danh mục Tài sản/Dịch vụ](SRS_Project_Category_TSDV-2.1.md)
- **TSDV-2.2**: [Phân loại và Gán nhãn Tài sản/Dịch vụ](SRS_Project_Category_TSDV-2.2.md)
- **TSDV-2.3**: [Tìm kiếm và Lọc Tài sản/Dịch vụ](SRS_Project_Category_TSDV-2.3.md)

#### TSDV-3.x: Theo dõi và Bảo trì
- **TSDV-3.1**: [Theo dõi lịch sử sử dụng, bảo hành, bảo dưỡng của Tài sản](SRS_Project_Category_TSDV-3.1.md)
- **TSDV-3.2**: [Nhắc nhở khi Tài sản/Dịch vụ sắp hết hạn bảo hành/bảo trì/sử dụng](SRS_Project_Category_TSDV-3.2.md)

### 📊 BC Series - Báo cáo (3 SRS)
- **BC-1.1**: [Báo cáo tiến độ dự án](SRS_Project_Category_BC-1.1.md)
- **BC-1.2**: [Báo cáo tài chính dự án](SRS_Project_Category_BC-1.2.md)
- **BC-1.3**: [Báo cáo tổng hợp dự án](SRS_Project_Category_BC-1.3.md)

### 🎯 HD Series - Hợp đồng (8 SRS)
- **HD-1.1**: [Tạo mới hợp đồng](SRS_Project_Category_HD-1.1.md)
- **HD-2.1**: [Quản lý điều khoản hợp đồng](SRS_Project_Category_HD-2.1.md)
- **HD-2.2**: [Quản lý điều kiện thanh toán](SRS_Project_Category_HD-2.2.md)
- **HD-3.1**: [Theo dõi tiến độ thực hiện hợp đồng](SRS_Project_Category_HD-3.1.md)
- **HD-4.1**: [Quản lý thanh toán hợp đồng](SRS_Project_Category_HD-4.1.md)
- **HD-5.1**: [Báo cáo tình hình hợp đồng](SRS_Project_Category_HD-5.1.md)
- **HD-5.2**: [Phân tích hiệu quả hợp đồng](SRS_Project_Category_HD-5.2.md)
- **HD-5.3**: [Cảnh báo hợp đồng sắp hết hạn](SRS_Project_Category_HD-5.3.md)

### 🔧 DMDA Series - Danh mục dự án (17 SRS)
- **DMDA-1.x**: Quản lý danh mục dự án (3 SRS)
- **DMDA-2.x**: Phân tích và báo cáo dự án (4 SRS)
- **DMDA-3.x**: Dashboard và thống kê (5 SRS)
- **DMDA-4.x**: Thông báo và cảnh báo (5 SRS)

### 🎯 GT Series - Gói thầu (8 SRS)
- **GT-1.x**: Quản lý gói thầu cơ bản (2 SRS)
- **GT-2.x**: Quản lý gói thầu nâng cao (2 SRS)
- **GT-3.x**: Theo dõi gói thầu (1 SRS)
- **GT-4.x**: Báo cáo và phân tích gói thầu (3 SRS)

## 🎨 Diagrams

### 📊 Activity Diagrams
- **CP Series**: 14 diagrams
- **TSDV Series**: 8 diagrams
- **Tổng cộng**: 22 Activity diagrams

### 📈 Sequence Diagrams
- **CP Series**: 14 diagrams
- **TSDV Series**: 8 diagrams
- **Tổng cộng**: 22 Sequence diagrams

### 🎯 Cách xem Diagrams
1. **Online**: Sử dụng PlantUML Online Editor
2. **Local**: Cài đặt PlantUML và generate PNG
3. **Web**: Xem trong docs/diagrams.html

## 🛠️ Công cụ và Technologies

### 📝 Documentation
- **Markdown**: Định dạng tài liệu
- **PlantUML**: Tạo diagrams
- **Bootstrap 5**: Web interface
- **Font Awesome**: Icons

### 🌐 Deployment
- **GitHub Pages**: Hosting chính
- **Netlify**: Alternative hosting
- **Vercel**: Fast deployment

### 🔧 Development
- **Git**: Version control
- **GitHub Actions**: CI/CD
- **Node.js**: Build tools

## 📋 Template SRS

### Cấu trúc chuẩn:
```markdown
# Software Requirements Specification (SRS)
## Epic: [Tên Epic]

### User Story: [Story ID]
### [Tên User Story]

#### Thông tin User Story
- **Story ID:** [ID]
- **Priority:** [High/Medium/Low]
- **Story Points:** [Số điểm]
- **Sprint:** [Sprint số]
- **Status:** [To Do/In Progress/Done]
- **Dependencies:** [Các dependencies]

#### Mô tả User Story
**Với vai trò là** [Actor],  
**Tôi muốn** [Goal],  
**Để** [Benefit].

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] [Criteria 1]
- [ ] [Criteria 2]
- [ ] [Criteria 3]

---

### Functional Requirements
#### Core Features
1. **[Feature 1]**
   - [Description]
   - [Requirements]

#### Business Rules
- [Rule 1]
- [Rule 2]

#### Technical Specifications
#### Database Schema Updates
#### API Endpoints
#### Frontend Components
#### UI/UX Design
#### Integration
#### Security
#### Testing
#### Deployment
#### Documentation
```

## 🚀 Quick Start

### 1. **Clone repository:**
```bash
git clone https://github.com/your-username/document-bitrix24.git
cd document-bitrix24
```

### 2. **Xem index chính:**
```bash
open SRS_INDEX.md
```

### 3. **Preview web:**
```bash
open docs/index.html
```

### 4. **Xem diagrams:**
```bash
open diagrams/DIAGRAMS_INDEX.md
```

## 📞 Hỗ trợ

### 🔍 Tìm kiếm nhanh
- **Theo chức năng**: CP, TSDV, BC, HD, DMDA, GT
- **Theo trạng thái**: To Do, In Progress, Done
- **Theo độ ưu tiên**: High, Medium, Low

### 📚 Tài liệu liên quan
- [SRS Index](SRS_INDEX.md) - Index tổng hợp
- [Diagrams Index](diagrams/DIAGRAMS_INDEX.md) - Index diagrams
- [Quick Access](diagrams/QUICK_ACCESS.md) - Truy cập nhanh
- [Web Preview](docs/index.html) - Giao diện web

### 🛠️ Công cụ hỗ trợ
- **PlantUML**: https://www.plantuml.com/plantuml/
- **Markdown Preview**: VS Code extension
- **GitHub Pages**: Tự động deploy
- **Netlify**: Alternative hosting

## 📝 Changelog

### v1.0.0 (2024-01-25)
- ✅ Tạo 58 SRS files
- ✅ Tạo 44 PlantUML diagrams
- ✅ Tạo web interface
- ✅ Setup GitHub Pages
- ✅ Setup Netlify deployment

## 📄 License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 👥 Contributors

- **Development Team**: Tạo và maintain SRS
- **Business Analysts**: Review và validate requirements
- **Stakeholders**: Provide feedback và approval

---

**📧 Liên hệ**: [your-email@example.com]  
**🌐 Website**: [https://your-repo.github.io]  
**📱 Support**: [https://github.com/your-repo/issues]

---

*Cập nhật lần cuối: 2024-01-25*  
*Phiên bản: 1.0.0* 