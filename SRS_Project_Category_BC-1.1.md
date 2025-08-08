# Software Requirements Specification (SRS)
## Epic: Báo cáo - Tạo và Quản lý Báo cáo Tổng hợp

### User Story: BC-1.1
### Tạo báo cáo tổng hợp theo các tiêu chí khác nhau

#### Thông tin User Story
- **Story ID:** BC-1.1
- **Priority:** High
- **Story Points:** 21
- **Sprint:** Sprint 1
- **Status:** To Do
- **Phụ thuộc:** CP-1.1, CP-1.2, TSDV-1.1, TSDV-1.2

#### Mô tả User Story
**Với vai trò là** Quản lý dự án/chương trình hoặc Cán bộ quản lý cấp cao,  
**Tôi muốn** có thể tạo các báo cáo tổng hợp dựa trên nhiều tiêu chí lọc và nhóm khác nhau (ví dụ: theo dự án, theo gói thầu, theo hợp đồng, theo thời gian, theo phòng ban/đơn vị, theo loại chi phí/tài sản),  
**Để** tôi có thể có cái nhìn đa chiều về tình hình hoạt động, chi tiêu và hiệu quả.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có giao diện thân thiện cho phép người dùng chọn các trường dữ liệu cần hiển thị, các tiêu chí lọc, và cách nhóm dữ liệu (ví dụ: nhóm theo dự án, sau đó nhóm theo loại chi phí)
- [ ] Hệ thống có thể lưu lại các mẫu báo cáo đã tùy chỉnh để tái sử dụng
- [ ] Có thể tạo báo cáo theo nhiều định dạng (Excel, PDF, CSV, HTML)
- [ ] Có thể thiết lập lịch trình gửi báo cáo tự động
- [ ] Có thể chia sẻ báo cáo với người dùng khác
- [ ] Có thể xuất báo cáo với các biểu đồ và đồ thị trực quan
- [ ] Có thể lọc dữ liệu theo khoảng thời gian tùy chỉnh
- [ ] Có thể so sánh dữ liệu giữa các kỳ báo cáo
- [ ] Có thể thiết lập quyền truy cập báo cáo theo vai trò người dùng
- [ ] Có thể xem preview báo cáo trước khi xuất
- [ ] Có thể thiết lập các tham số mặc định cho báo cáo
- [ ] Hệ thống ghi log đầy đủ các hoạt động tạo và xuất báo cáo

#### 2.4 Activity Diagram
![BC-1.1 Activity Diagram](diagrams/BC-1.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tạo báo cáo tổng hợp theo các tiêu chí khác nhau*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Report Builder**
   - Giao diện kéo thả
   - Chọn trường dữ liệu
   - Cấu hình bộ lọc
   - Tùy chọn nhóm
   - Tùy chọn sắp xếp

2. **Nguồn Dữ liệu**
   - Dữ liệu dự án
   - Dữ liệu hợp đồng
   - Dữ liệu tài sản
   - Dữ liệu chi phí
   - Dữ liệu phòng ban
   - Dữ liệu theo thời gian

3. **Template Báo cáo**
   - Template có sẵn
   - Template tùy chỉnh
   - Chia sẻ template
   - Phiên bản template
   - Danh mục template

4. **Tùy chọn Xuất**
   - Xuất Excel
   - Xuất PDF
   - Xuất CSV
   - Xuất HTML
   - Gửi qua email

#### Quy tắc Kinh doanh
- Chỉ người dùng có quyền mới có thể tạo báo cáo
- Dữ liệu phải được cập nhật thời gian thực hoặc theo lịch trình
- Báo cáo phải bao gồm thông tin về người tạo và thời gian tạo
- Các báo cáo nhạy cảm phải được mã hóa
- Hệ thống phải ghi log đầy đủ các hoạt động báo cáo
- Dữ liệu phải được validate trước khi xuất báo cáo

#### Danh mục Báo cáo
1. **Báo cáo Dự án**
   - Tổng quan dự án
   - Tiến độ dự án
   - Chi phí dự án
   - Timeline dự án
   - Tài nguyên dự án

2. **Báo cáo Hợp đồng**
   - Tổng quan hợp đồng
   - Hiệu suất hợp đồng
   - Chi phí hợp đồng
   - Timeline hợp đồng
   - Tuân thủ hợp đồng

3. **Báo cáo Tài sản**
   - Danh mục tài sản
   - Sử dụng tài sản
   - Chi phí tài sản
   - Bảo trì tài sản
   - Khấu hao tài sản

4. **Báo cáo Tài chính**
   - Phân tích chi phí
   - Ngân sách vs thực tế
   - Expense tracking
   - Revenue analysis
   - Profitability analysis

5. **Department Reports**
   - Department performance
   - Department costs
   - Department resources
   - Department timeline
   - Department comparison

---

### Non-Functional Requirements

#### Performance Requirements
- Báo cáo phải được tạo trong vòng 30 giây
- Hệ thống phải hỗ trợ tối đa 100 người dùng đồng thời
- Export file phải được tạo trong vòng 60 giây
- Giao diện báo cáo phải load trong vòng 3 giây
- Hệ thống phải xử lý được dữ liệu lớn (1GB+)

#### Security Requirements
- Chỉ người dùng có quyền mới có thể truy cập báo cáo
- Dữ liệu nhạy cảm phải được mã hóa
- Log đầy đủ các hoạt động truy cập báo cáo
- Backup định kỳ các template và cấu hình báo cáo
- Kiểm soát quyền truy cập theo vai trò

#### Usability Requirements
- Giao diện thân thiện, dễ sử dụng
- Hướng dẫn step-by-step cho người dùng mới
- Preview báo cáo trước khi xuất
- Tùy chỉnh giao diện theo sở thích người dùng
- Hỗ trợ đa ngôn ngữ

#### Reliability Requirements
- Hệ thống phải hoạt động 24/7
- Có cơ chế backup cho template và cấu hình
- Tự động khôi phục khi có lỗi
- Monitoring và alerting cho hệ thống báo cáo
- Version control cho template báo cáo

---

### Technical Requirements

#### System Architecture
1. **Report Engine**
   - Query builder
   - Data aggregation
   - Template rendering
   - Export processing

2. **Data Warehouse**
   - Data integration
   - Data transformation
   - Data quality
   - Data governance

3. **Template Engine**
   - Template management
   - Variable substitution
   - Formatting engine
   - Preview generation

4. **Export Service**
   - Multi-format export
   - File compression
   - Email delivery
   - File storage

#### Database Schema
```sql
-- Report Templates
CREATE TABLE report_templates (
    id INT PRIMARY KEY,
    template_name VARCHAR(100),
    template_type VARCHAR(50),
    template_config JSON,
    created_by INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN
);

-- Report Schedules
CREATE TABLE report_schedules (
    id INT PRIMARY KEY,
    template_id INT,
    schedule_name VARCHAR(100),
    cron_expression VARCHAR(100),
    recipients TEXT,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    is_active BOOLEAN
);

-- Report History
CREATE TABLE report_history (
    id INT PRIMARY KEY,
    template_id INT,
    generated_by INT,
    generated_at TIMESTAMP,
    file_path VARCHAR(255),
    file_size INT,
    status VARCHAR(20)
);

-- Report Permissions
CREATE TABLE report_permissions (
    id INT PRIMARY KEY,
    user_id INT,
    template_id INT,
    permission_type VARCHAR(50),
    granted_at TIMESTAMP
);
```

#### API Endpoints
```typescript
// Report Templates
GET /api/reports/templates
POST /api/reports/templates
PUT /api/reports/templates/{id}
DELETE /api/reports/templates/{id}

// Report Generation
POST /api/reports/generate
GET /api/reports/generate/{id}/status
GET /api/reports/generate/{id}/download

// Report Schedules
GET /api/reports/schedules
POST /api/reports/schedules
PUT /api/reports/schedules/{id}
DELETE /api/reports/schedules/{id}

// Report History
GET /api/reports/history
GET /api/reports/history/{id}

// Report Permissions
GET /api/reports/permissions
POST /api/reports/permissions
DELETE /api/reports/permissions/{id}
```

---

### User Interface Requirements

#### Report Builder Interface
1. **Data Source Selection**
   - Available data sources
   - Data source preview
   - Data source validation
   - Connection status

2. **Field Selection**
   - Available fields list
   - Field search/filter
   - Field description
   - Field data type

3. **Filter Configuration**
   - Filter builder
   - Filter conditions
   - Filter operators
   - Filter validation

4. **Grouping Configuration**
   - Group by fields
   - Group levels
   - Group sorting
   - Group subtotals

5. **Sorting Configuration**
   - Sort fields
   - Sort direction
   - Sort priority
   - Sort validation

#### Template Management
1. **Template Library**
   - Template categories
   - Template search
   - Template preview
   - Template sharing

2. **Template Editor**
   - Visual editor
   - Code editor
   - Template variables
   - Template validation

3. **Template Versioning**
   - Version history
   - Version comparison
   - Version rollback
   - Version comments

#### Report Viewer
1. **Report Display**
   - Data table view
   - Chart view
   - Dashboard view
   - Print view

2. **Interactive Features**
   - Drill-down capability
   - Filter on-the-fly
   - Sort on-the-fly
   - Export options

3. **Export Options**
   - Format selection
   - Page settings
   - Quality settings
   - File naming

---

### Integration Requirements

#### Data Source Integration
- Database connections
- API integrations
- File imports
- Real-time data feeds
- Data synchronization

#### Export Service Integration
- Email service
- File storage service
- Cloud storage
- FTP/SFTP
- WebDAV

#### Third-party Services
- Chart libraries
- PDF generators
- Excel generators
- Email services
- Cloud services

#### Authentication Integration
- LDAP/Active Directory
- SSO integration
- Role-based access
- Permission management
- Audit logging

---

### Testing Requirements

#### Unit Testing
- Report engine logic
- Template rendering
- Data aggregation
- Export functionality

#### Integration Testing
- Data source connections
- Export service integration
- Authentication integration
- Third-party service integration

#### User Acceptance Testing
- Report builder interface
- Template management
- Export functionality
- End-to-end workflow

#### Performance Testing
- Large dataset handling
- Concurrent user testing
- Export performance
- Memory usage optimization

---

### Deployment Requirements

#### Environment Setup
- Production report server
- Staging environment
- Development environment
- Backup systems

#### Monitoring & Alerting
- System health monitoring
- Report generation monitoring
- Error rate tracking
- Performance metrics

#### Security Considerations
- Data encryption
- Access control
- Audit logging
- Backup security

#### Backup & Recovery
- Template backup
- Configuration backup
- Data backup
- Disaster recovery plan

---

### Documentation Requirements

#### User Documentation
- Report builder guide
- Template creation guide
- Export options guide
- Troubleshooting guide

#### Technical Documentation
- API documentation
- Database schema
- System architecture
- Deployment guide

#### Admin Documentation
- System configuration
- Monitoring setup
- Security guidelines
- Maintenance procedures

---

### Data Requirements

#### Data Sources
1. **Project Data**
   - Project information
   - Project status
   - Project timeline
   - Project costs
   - Project resources

2. **Contract Data**
   - Contract details
   - Contract status
   - Contract timeline
   - Contract costs
   - Contract performance

3. **Asset Data**
   - Asset inventory
   - Asset status
   - Asset costs
   - Asset maintenance
   - Asset utilization

4. **Financial Data**
   - Cost data
   - Budget data
   - Revenue data
   - Expense data
   - Profit data

5. **Organizational Data**
   - Department data
   - Employee data
   - Role data
   - Permission data
   - Audit data

#### Data Quality
- Data validation rules
- Data cleansing procedures
- Data consistency checks
- Data accuracy verification
- Data completeness validation

#### Data Governance
- Data ownership
- Data classification
- Data retention policies
- Data access controls
- Data audit trails

#### 5.5 Sequence Diagram
![BC-1.1 Sequence Diagram](diagrams/BC-1.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tạo báo cáo tổng hợp theo các tiêu chí khác nhau* 