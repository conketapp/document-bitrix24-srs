# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### 1. Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Date:** 2024  
**Author:** Development Team  

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
- [ ] Người dùng có thể xem danh sách dự án được lọc theo năm và loại
- [ ] Hệ thống hiển thị danh sách dự án với thông tin cơ bản
- [ ] Người dùng có thể chọn năm từ dropdown (2024, 2025, v.v.)
- [ ] Người dùng có thể chọn loại dự án từ dropdown
- [ ] Hệ thống hỗ trợ lọc theo "Tất cả" cho cả năm và loại
- [ ] Kết quả lọc được hiển thị ngay lập tức
- [ ] Giao diện responsive và dễ sử dụng

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
     - Dự án đầu tư
     - Mua sắm tài sản
     - Thuê dịch vụ
     - Bảo trì
     - Tất cả
   - Mặc định hiển thị "Tất cả"

3. **Hiển thị Danh sách Dự án**
   - Tên dự án
   - Năm thực hiện
   - Loại dự án
   - Trạng thái dự án
   - Ngày bắt đầu
   - Ngày kết thúc dự kiến
   - Ngân sách

#### 3.2 Business Rules
- Chỉ hiển thị dự án mà người dùng có quyền xem
- Dự án được sắp xếp theo thứ tự ưu tiên (dự án đang triển khai trước)
- Hỗ trợ phân trang nếu có nhiều dự án

#### 3.3 Validation Rules
**Validation cho Filter:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| Năm | year | Number | 4 chữ số (2024, 2025, v.v.) | ✅ |
| Loại dự án | categoryId | Number | ID hợp lệ từ bảng project_categories | ❌ |
| Trạng thái | status | ENUM | 'active', 'completed', 'cancelled' | ❌ |

**Validation cho Hiển thị Dự án:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| Tên dự án | name | Text | 3-255 ký tự | ✅ |
| Năm thực hiện | year | Number | 4 chữ số | ✅ |
| Loại dự án | category_name | Text | Tên loại dự án hợp lệ | ✅ |
| Trạng thái dự án | status | ENUM | 'active', 'completed', 'cancelled' | ✅ |
| Ngày bắt đầu | start_date | Date | Định dạng YYYY-MM-DD | ❌ |
| Ngày kết thúc | end_date | Date | Định dạng YYYY-MM-DD | ❌ |
| Ngân sách | budget | Decimal | Số dương, định dạng tiền tệ | ❌ |

**Validation cho Database:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| name | VARCHAR(255) | Text | NOT NULL | ✅ |
| year | INT | Number | NOT NULL | ✅ |
| category_id | INT | Number | FOREIGN KEY, NOT NULL | ✅ |
| status | ENUM | Text | 'active', 'completed', 'cancelled' | ✅ |
| start_date | DATE | Date | NULL | ❌ |
| end_date | DATE | Date | NULL | ❌ |
| budget | DECIMAL(15,2) | Decimal | NULL | ❌ |

**Quy tắc chung:**
- Năm phải là năm hợp lệ (không được trong quá khứ xa)
- Loại dự án phải tồn tại trong bảng project_categories
- Ngày kết thúc phải sau ngày bắt đầu (nếu có)
- Ngân sách phải là số dương (nếu có)
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
    name VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    category_id INT NOT NULL,
    status ENUM('active', 'completed', 'cancelled') DEFAULT 'active',
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES project_categories(id)
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
**Last Updated:** 2024  
**Next Review:** Sprint 2 