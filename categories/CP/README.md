# CP - Chi phí & Dự án
## Quản lý Chi phí và Dự án

### 📋 Tổng quan
Category CP tập trung vào việc quản lý chi phí dự án, theo dõi ngân sách và phân tích ROI cho các dự án của Agribank.

### 📊 Thống kê User Stories

| Story ID | Tên User Story | Priority | Story Points | Status |
|----------|----------------|----------|--------------|--------|
| CP-1.1 | Quản lý thông tin dự án cơ bản | High | 8 | ✅ Done |
| CP-1.2 | Quản lý ngân sách dự án | High | 13 | ✅ Done |
| CP-1.3 | Theo dõi chi phí thực tế | High | 13 | ✅ Done |
| CP-2.1 | Quản lý gói thầu | Medium | 8 | ✅ Done |
| CP-2.2 | Quản lý hợp đồng | Medium | 8 | ✅ Done |
| CP-3.1 | Phân tích ROI dự án | Medium | 5 | ✅ Done |
| CP-4.1 | Quản lý rủi ro dự án | Medium | 8 | ✅ Done |
| CP-4.2 | Báo cáo tiến độ dự án | Medium | 5 | ✅ Done |
| CP-5.1 | Quản lý nhân sự dự án | Low | 8 | ✅ Done |
| CP-5.2 | Quản lý tài nguyên dự án | Low | 5 | ✅ Done |
| CP-5.3 | Quản lý thời gian dự án | Low | 8 | ✅ Done |
| CP-5.4 | Quản lý chất lượng dự án | Low | 5 | ✅ Done |
| CP-5.5 | Quản lý thay đổi dự án | Low | 8 | ✅ Done |
| CP-5.6 | Đóng dự án và bàn giao | Low | 5 | ✅ Done |

### 🎯 Mục tiêu chính

#### 1. Quản lý Dự án
- Tạo và quản lý thông tin dự án
- Theo dõi tiến độ và trạng thái
- Quản lý nhân sự và tài nguyên
- Đóng dự án và bàn giao

#### 2. Quản lý Chi phí
- Lập kế hoạch ngân sách
- Theo dõi chi phí thực tế
- Phân tích chênh lệch
- Báo cáo tài chính

#### 3. Quản lý Hợp đồng
- Quản lý gói thầu
- Theo dõi hợp đồng
- Quản lý thanh toán
- Đánh giá nhà thầu

#### 4. Phân tích và Báo cáo
- Phân tích ROI
- Quản lý rủi ro
- Báo cáo tiến độ
- Dashboard tổng quan

### 🔗 Liên kết User Stories

#### Epic 1: Quản lý Dự án Cơ bản
- [CP-1.1: Quản lý thông tin dự án cơ bản](CP-1.1.md)
- [CP-1.2: Quản lý ngân sách dự án](CP-1.2.md)
- [CP-1.3: Theo dõi chi phí thực tế](CP-1.3.md)

#### Epic 2: Quản lý Hợp đồng và Thầu
- [CP-2.1: Quản lý gói thầu](CP-2.1.md)
- [CP-2.2: Quản lý hợp đồng](CP-2.2.md)

#### Epic 3: Phân tích và Báo cáo
- [CP-3.1: Phân tích ROI dự án](CP-3.1.md)

#### Epic 4: Quản lý Rủi ro và Tiến độ
- [CP-4.1: Quản lý rủi ro dự án](CP-4.1.md)
- [CP-4.2: Báo cáo tiến độ dự án](CP-4.2.md)

#### Epic 5: Quản lý Dự án Nâng cao
- [CP-5.1: Quản lý nhân sự dự án](CP-5.1.md)
- [CP-5.2: Quản lý tài nguyên dự án](CP-5.2.md)
- [CP-5.3: Quản lý thời gian dự án](CP-5.3.md)
- [CP-5.4: Quản lý chất lượng dự án](CP-5.4.md)
- [CP-5.5: Quản lý thay đổi dự án](CP-5.5.md)
- [CP-5.6: Đóng dự án và bàn giao](CP-5.6.md)

### 🏗️ Kiến trúc Hệ thống

#### Core Modules
1. **Project Management Module**
   - Project creation and configuration
   - Project lifecycle management
   - Project status tracking
   - Project documentation

2. **Budget Management Module**
   - Budget planning and allocation
   - Cost tracking and monitoring
   - Variance analysis
   - Financial reporting

3. **Contract Management Module**
   - Tender package management
   - Contract creation and tracking
   - Payment management
   - Vendor evaluation

4. **Risk Management Module**
   - Risk identification and assessment
   - Risk mitigation planning
   - Risk monitoring and reporting
   - Issue tracking

#### Database Schema
```sql
-- Projects
CREATE TABLE projects (
    id INT PRIMARY KEY,
    project_name VARCHAR(100),
    project_code VARCHAR(50),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    budget_amount DECIMAL(15,2),
    actual_amount DECIMAL(15,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Budgets
CREATE TABLE project_budgets (
    id INT PRIMARY KEY,
    project_id INT,
    budget_type VARCHAR(50),
    planned_amount DECIMAL(15,2),
    actual_amount DECIMAL(15,2),
    variance_amount DECIMAL(15,2),
    budget_date DATE,
    created_at TIMESTAMP
);

-- Contracts
CREATE TABLE contracts (
    id INT PRIMARY KEY,
    project_id INT,
    contract_number VARCHAR(50),
    vendor_name VARCHAR(100),
    contract_amount DECIMAL(15,2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    created_at TIMESTAMP
);
```

### 📊 Metrics và KPI

#### Project Metrics
- **Project Completion Rate**: Tỷ lệ hoàn thành dự án
- **Budget Variance**: Chênh lệch ngân sách
- **Schedule Variance**: Chênh lệch tiến độ
- **Resource Utilization**: Sử dụng tài nguyên

#### Financial Metrics
- **ROI**: Return on Investment
- **Cost Performance Index**: CPI
- **Schedule Performance Index**: SPI
- **Budget at Completion**: BAC

### 🔄 Quy trình Workflow

#### 1. Project Initiation
1. Tạo dự án mới
2. Thiết lập ngân sách
3. Phân bổ nhân sự
4. Xác định rủi ro

#### 2. Project Execution
1. Theo dõi tiến độ
2. Cập nhật chi phí
3. Quản lý thay đổi
4. Báo cáo định kỳ

#### 3. Project Closure
1. Đánh giá kết quả
2. Bàn giao sản phẩm
3. Đóng dự án
4. Lessons learned

### 📚 Tài liệu Tham khảo

#### Standards
- [PMBOK Guide](link)
- [PRINCE2 Methodology](link)
- [Agile Project Management](link)
- [Agribank Project Standards](link)

#### Templates
- [Project Charter Template](link)
- [Budget Template](link)
- [Risk Register Template](link)
- [Status Report Template](link)

---

**📌 Lưu ý**: Category CP là core module của hệ thống, cần được ưu tiên phát triển trước.

**🔄 Cập nhật cuối**: 2024-01-25
**👥 Maintained by**: Project Management Team 