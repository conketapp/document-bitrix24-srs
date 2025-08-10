# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### 1. Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Date:** 07-2025  
**Author:** Công ty Thiên Phú Digital  

### 2. Mô tả Epic
Epic này tập trung vào việc phát triển hệ thống quản lý danh mục dự án, cho phép cán bộ quản lý dự án tổ chức và quản lý các dự án theo năm và phân loại một cách hiệu quả.

---

## User Story: DMDA-1.1
### Tạo Danh mục Dự án theo Năm và Phân loại

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-1.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 1
- **Status:** To Do

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn có** một danh mục cho phép tôi tổ chức các dự án theo năm (ví dụ: 2024, 2025) và theo loại dự án (ví dụ: Dự án đầu tư, Mua sắm tài sản, Thuê dịch vụ, Bảo trì, Tất cả),  
**Để** tôi có thể dễ dàng tìm kiếm, quản lý và có cái nhìn tổng quan về tất cả các dự án đang triển khai hoặc đã hoàn thành.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Người dùng có thể xem danh sách dự án được lọc theo năm, loại dự án và nguồn gốc dự án
- [ ] Hệ thống hiển thị danh sách dự án với đầy đủ thông tin: Mã dự án, Tên dự án, Nguồn gốc dự án, TMĐT dự kiến, TMĐT phê duyệt, Lũy kế vốn đã ứng, Vốn đã ứng năm hiện tại, Dự kiến vốn sẽ ứng, Đề xuất kế hoạch vốn năm sau, Trạng thái phê duyệt
- [ ] Người dùng có thể chọn năm từ dropdown (2024, 2025, v.v.) - mặc định là năm hiện tại
- [ ] Người dùng có thể chọn loại dự án từ dropdown: Dự án Đầu tư, Dự án Mua sắm, Dự án Thuê dịch vụ, Dự án Bảo trì, Tất cả - mặc định là "Tất cả"
- [ ] Người dùng có thể chọn nguồn gốc dự án từ dropdown: Dự án Mới, Dự án Chuyển tiếp, Tất cả - mặc định là "Tất cả"
- [ ] Người dùng có thể lọc theo trạng thái phê duyệt: Khởi tạo, Chờ phê duyệt, Đã phê duyệt, Từ chối phê duyệt, Dừng thực hiện, Yêu cầu chỉnh sửa
- [ ] Hệ thống tự động phân loại dự án mới/chuyển tiếp dựa trên năm tạo và trạng thái
- [ ] Mã dự án được tạo tự động theo format PRJ-YYYY-XXXX
- [ ] Kết quả lọc được hiển thị ngay lập tức với thời gian phản hồi < 1 giây
- [ ] Giao diện responsive và dễ sử dụng trên cả desktop và mobile
- [ ] Hỗ trợ phân trang khi có nhiều dự án (>20 dự án)
- [ ] Hiển thị thông báo khi không có dự án nào thỏa mãn điều kiện lọc

#### 2.4 Activity Diagram
![DMDA-1.1 Activity Diagram](diagrams/DMDA-1.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý của User Story DMDA-1.1*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Lọc theo Năm**
   - Dropdown chọn năm (2024, 2025, v.v.)
   - Không có option "Tất cả"
   - Mặc định hiển thị năm hiện tại

2. **Lọc theo Loại Dự án**
   - Dropdown chọn loại dự án:
     - Dự án Đầu tư
     - Dự án Mua sắm
     - Dự án Thuê dịch vụ
     - Dự án Bảo trì
     - Tất cả
   - Mặc định hiển thị "Tất cả"

3. **Lọc theo Nguồn gốc Dự án**
   - Dropdown chọn nguồn gốc dự án:
     - Dự án Mới
     - Dự án Chuyển tiếp
     - Tất cả
   - Mặc định hiển thị "Tất cả"

3. **Hiển thị Danh sách Dự án**
   - Mã dự án
   - Tên dự án
   - Nguồn gốc dự án
   - TMĐT dự kiến theo KHV
   - TMĐT đã được phê duyệt
   - Lũy kế vốn đã ứng
   - Tổng vốn đã ứng từ trong năm đến hiện tại
   - Dự kiến vốn sẽ ứng
   - Đề xuất kế hoạch vốn năm sau
   - Trạng thái phê duyệt

#### 3.2 Business Rules
- Chỉ hiển thị dự án mà người dùng có quyền xem
- Dự án được sắp xếp theo thứ tự ưu tiên (dự án đang triển khai trước)
- Hỗ trợ phân trang nếu có nhiều dự án

#### 3.3 Validation Rules
**Validation cho Filter:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| Năm | year | Number | 4 chữ số (2024, 2025, v.v.) | ✅ |
| Loại dự án | projectSource | String | 'INV', 'PUR', 'SER', 'MAI' | ❌ |
| Nguồn gốc dự án | projectType | ENUM | 'new', 'carryover' | ❌ |
| Trạng thái | status | ENUM | 'initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested' | ❌ |

**Validation cho Hiển thị Dự án:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| Mã dự án | project_code | Text | Format: PRJ-YYYY-XXXX | ✅ |
| Tên dự án | name | Text | 3-255 ký tự | ✅ |
| Nguồn gốc dự án | project_source | Text | 1-100 ký tự | ✅ |
| TMĐT dự kiến theo KHV | planned_budget | Decimal | Số dương, định dạng tiền tệ | ❌ |
| TMĐT đã được phê duyệt | approved_budget | Decimal | Số dương, định dạng tiền tệ | ❌ |
| Lũy kế vốn đã ứng | total_disbursed | Decimal | Số dương, định dạng tiền tệ | ❌ |
| Tổng vốn đã ứng từ trong năm đến hiện tại | current_year_disbursed | Decimal | Số dương, định dạng tiền tệ | ❌ |
| Dự kiến vốn sẽ ứng | expected_disbursement | Decimal | Số dương, định dạng tiền tệ | ❌ |
| Đề xuất kế hoạch vốn năm sau | next_year_plan | Decimal | Số dương, định dạng tiền tệ | ❌ |
| Trạng thái phê duyệt | status | ENUM | 'initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested' | ✅ |

**Validation cho Database:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| project_code | VARCHAR(20) | Text | NOT NULL, UNIQUE | ✅ |
| name | VARCHAR(255) | Text | NOT NULL | ✅ |
| project_source | VARCHAR(100) | Text | NOT NULL | ✅ |
| planned_budget | DECIMAL(15,2) | Decimal | NULL | ❌ |
| approved_budget | DECIMAL(15,2) | Decimal | NULL | ❌ |
| total_disbursed | DECIMAL(15,2) | Decimal | NULL | ❌ |
| current_year_disbursed | DECIMAL(15,2) | Decimal | NULL | ❌ |
| expected_disbursement | DECIMAL(15,2) | Decimal | NULL | ❌ |
| next_year_plan | DECIMAL(15,2) | Decimal | NULL | ❌ |
| status | ENUM | Text | 'initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested' | ✅ |

**Mapping Trạng thái Dự án:**
| Key (Database) | Label (Hiển thị) | Mô tả |
|----------------|-------------------|-------|
| initialized | Khởi tạo | Dự án mới được tạo |
| pending_approval | Chờ phê duyệt | Dự án đã gửi chờ phê duyệt |
| approved | Đã phê duyệt | Dự án đã được phê duyệt |
| rejected | Từ chối phê duyệt | Dự án bị từ chối phê duyệt |
| suspended | Dừng thực hiện | Dự án tạm dừng thực hiện |
| edit_requested | Yêu cầu chỉnh sửa | Dự án yêu cầu chỉnh sửa |

**Mapping Loại Dự án:**
| Key (Database) | Label (Hiển thị) | Mô tả |
|----------------|-------------------|-------|
| INV | Dự án Đầu tư | Dự án đầu tư mới |
| PUR | Dự án Mua sắm | Dự án mua sắm tài sản |
| SER | Dự án Thuê dịch vụ | Dự án thuê dịch vụ |
| MAI | Dự án Bảo trì | Dự án bảo trì, sửa chữa |

**Mapping Nguồn gốc Dự án:**
| Key (Database) | Label (Hiển thị) | Mô tả |
|----------------|-------------------|-------|
| new | Dự án Mới | Dự án bắt đầu trong năm hiện tại |
| carryover | Dự án Chuyển tiếp | Dự án từ năm trước chưa hoàn thành |

**Quy tắc chung:**
- Mã dự án phải theo format PRJ-YYYY-XXXX và không được trùng lặp
- Nguồn gốc dự án không được để trống
- Tất cả các khoản vốn phải là số dương (nếu có)
- Lũy kế vốn đã ứng không được vượt quá TMĐT đã được phê duyệt
- Tổng vốn đã ứng từ trong năm đến hiện tại không được vượt quá lũy kế vốn đã ứng
- Chỉ hiển thị dự án mà user có quyền xem

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian tải trang < 3 giây
- Thời gian lọc < 1 giây
- Hỗ trợ tối đa 1000 dự án trên một trang

#### 4.2 Usability
- Giao diện thân thiện với người dùng
- Responsive design cho mobile và desktop
- Hỗ trợ keyboard navigation
- Tooltip hướng dẫn cho các chức năng

#### 4.3 Security
- Xác thực người dùng trước khi truy cập
- Phân quyền theo vai trò
- Logging các hoạt động truy cập

---

### 5. Technical Specifications

#### 5.1 Database Schema
```sql
-- Bảng dự án
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    project_source VARCHAR(100) NOT NULL,
    project_type ENUM('new', 'carryover') NOT NULL,
    planned_budget DECIMAL(15,2),
    approved_budget DECIMAL(15,2),
    total_disbursed DECIMAL(15,2) DEFAULT 0,
    current_year_disbursed DECIMAL(15,2) DEFAULT 0,
    expected_disbursement DECIMAL(15,2),
    next_year_plan DECIMAL(15,2),
    status ENUM('initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested') DEFAULT 'initialized',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng loại dự án
CREATE TABLE project_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### 5.2 API Endpoints
```
GET /api/projects
- Parameters: year (optional), category_id (optional)
- Response: List of projects with pagination

GET /api/project-categories
- Response: List of all project categories
```

#### 5.3 Sequence Diagram
![DMDA-1.1 Sequence Diagram](diagrams/DMDA-1.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các component trong hệ thống*

#### 5.4 UI Components
- FilterComponent: Dropdown cho năm và loại dự án
- ProjectListComponent: Hiển thị danh sách dự án
- PaginationComponent: Phân trang
- LoadingState: Trạng thái loading
- EmptyState: Trạng thái không có dữ liệu

---

### 6. Data Flow

#### 6.1 System Flow
1. User chọn năm và loại dự án
2. System gọi API để lấy dữ liệu
3. Hiển thị danh sách dự án đã lọc
4. User có thể tương tác với danh sách

#### 6.2 API Integration
- Sử dụng REST API để lấy dữ liệu dự án
- API endpoints: `/api/projects`, `/api/project-categories`
- Hỗ trợ filtering và pagination

---

### 7. User Interface Requirements

#### 7.1 Layout
- Header với tiêu đề "Danh mục dự án"
- Filter section với 2 dropdown
- Main content area hiển thị danh sách
- Footer với thông tin phân trang

#### 7.2 Design Guidelines
- Sử dụng Tailwind CSS cho styling
- Color scheme theo brand guidelines
- Typography: Font size 14px cho text thường
- Spacing: 16px padding/margin

---

### 8. Testing Requirements

#### 8.1 Unit Tests
- Test filter logic
- Test API endpoints
- Test database queries

#### 8.2 Integration Tests
- Test API endpoints
- Test data filtering and pagination

#### 8.3 User Acceptance Tests
- Test filter functionality
- Test responsive design
- Test accessibility

---

### 9. Deployment Requirements

#### 9.1 Environment
- Development: Local environment
- Staging: Test environment
- Production: Live environment

#### 9.2 Dependencies
- Next.js framework
- React components
- Tailwind CSS
- REST API client

---

### 10. Success Criteria
- [ ] User có thể lọc dự án theo năm và loại
- [ ] Performance đáp ứng yêu cầu
- [ ] UI/UX thân thiện và dễ sử dụng
- [ ] API integration hoạt động ổn định
- [ ] Tất cả test cases pass

---

### 11. Risks and Mitigation

#### 11.1 Technical Risks
- **Risk:** API rate limiting
- **Mitigation:** Implement caching và request throttling

- **Risk:** Performance issues với large datasets
- **Mitigation:** Implement pagination và lazy loading

#### 11.2 Business Risks
- **Risk:** User adoption
- **Mitigation:** Provide training và user documentation

---

### 12. Future Enhancements
- Advanced search functionality
- Export to Excel/PDF
- Dashboard với charts và analytics
- Mobile app support
- Real-time notifications

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 2 