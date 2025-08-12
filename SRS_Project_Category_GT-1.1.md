# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-1.1
### Tạo Gói thầu mới

#### Thông tin User Story
- **Story ID:** GT-1.1
- **Priority:** High
- **Story Points:** 13
- **Sprint:** Sprint 1
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể tạo một hồ sơ gói thầu mới và nhập các thông tin cần thiết về gói thầu (ví dụ: tên, mã TBMT, giá, dự án liên quan, hình thức lựa chọn nhà thầu, v.v.),  
**Để** tôi có thể khởi tạo một gói thầu với đầy đủ thông tin và phục vụ công tác quản lý, theo dõi sau này.

**Lưu ý:** Một số thông tin gói thầu khác của gói thầu như mã TBMT, số lượng nhà thầu tham gia, quyết định phê duyệt HSMT, quyết định phê duyệt KQLCNT, giá trúng thầu,...không bắt buộc người dùng nhập ngay từ đầu và sẽ cho phép người dùng chỉnh sửa, cập nhật sau khi có thông tin và một số thông tin như quyết định phê duyệt KQLCNT, nhà thầu trúng thầu, giá trúng thầu,...sẽ được link, lấy thông tin từ Bitrix.

Sau khi có thông tin phê duyệt của gói thầu, dựa trên Hình thức lựa chọn nhà thầu (đấu thầu rộng rãi, chỉ định thầu,...) đã được phê duyệt, khi triển khai gói thầu trên Bitrix sẽ tự động triển khai theo luồng công việc phù hợp với Hình thức đã được phê duyệt.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có một form để tạo gói thầu mới với các trường thông tin quan trọng
- [ ] Mã gói thầu tự động sinh và không thể chỉnh sửa
- [ ] Trường Dự án liên quan cho phép chọn từ danh sách các dự án đã có trong Module Dự án
- [ ] Một số thông tin được link, lấy thông tin từ Bitrix
- [ ] Khi triển khai gói thầu trên Bitrix, Bitrix sẽ tự động triển khai theo luồng công việc phù hợp với Hình thức đã được phê duyệt
- [ ] Form có validation cho các trường bắt buộc
- [ ] Hỗ trợ lưu nháp và hoàn thành sau
- [ ] Hiển thị preview thông tin gói thầu trước khi lưu

#### 2.4 Activity Diagram
![GT-1.1 Activity Diagram](diagrams/GT-1.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tạo gói thầu mới*

---

### Functional Requirements

#### Core Features
1. **Form Tạo Gói thầu**
   - Thông tin cơ bản gói thầu
   - Thông tin dự án liên quan
   - Hình thức lựa chọn nhà thầu
   - Thông tin ngân sách và giá trị
   - Thông tin thời gian

2. **Tích hợp với Module Dự án**
   - Chọn dự án từ danh sách có sẵn
   - Hiển thị thông tin dự án được chọn
   - Validation dự án tồn tại và hợp lệ

3. **Tích hợp với Bitrix**
   - Link thông tin từ Bitrix
   - Tự động triển khai workflow
   - Đồng bộ trạng thái gói thầu

4. **Quản lý Trạng thái**
   - Trạng thái nháp
   - Trạng thái đã tạo
   - Trạng thái đang triển khai
   - Trạng thái hoàn thành

#### Business Rules
- Mã gói thầu tự động sinh theo format: GT-YYYY-XXXX
- Dự án liên quan phải tồn tại trong hệ thống
- Hình thức lựa chọn nhà thầu phải được phê duyệt trước khi triển khai
- Thông tin từ Bitrix được cập nhật real-time
- Workflow tự động dựa trên hình thức lựa chọn nhà thầu

#### Thông tin Gói thầu
1. **Thông tin Cơ bản (Bắt buộc)**
   - Tên gói thầu
   - Mã gói thầu (tự động)
   - Dự án liên quan
   - Hình thức lựa chọn nhà thầu
   - Giá trị dự kiến
   - Thời gian bắt đầu
   - Thời gian kết thúc dự kiến

2. **Thông tin Chi tiết (Tùy chọn)**
   - Mã TBMT
   - Số lượng nhà thầu tham gia
   - Quyết định phê duyệt HSMT
   - Quyết định phê duyệt KQLCNT
   - Giá trúng thầu
   - Nhà thầu trúng thầu

3. **Thông tin từ Bitrix (Link)**
   - Quyết định phê duyệt KQLCNT
   - Nhà thầu trúng thầu
   - Giá trúng thầu
   - Trạng thái triển khai

---

### Technical Specifications

#### Sequence Diagram
![GT-1.1 Sequence Diagram](diagrams/GT-1.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tạo gói thầu mới*

#### Database Schema Updates
```sql
-- Bảng gói thầu
CREATE TABLE tender_packages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_code VARCHAR(20) NOT NULL UNIQUE, -- GT-YYYY-XXXX
    name VARCHAR(500) NOT NULL,
    description TEXT,
    project_id INT NOT NULL,
    tender_method ENUM('open_tender', 'limited_tender', 'direct_appointment', 'competitive_consultation', 'other') NOT NULL,
    estimated_value DECIMAL(15,2),
    currency VARCHAR(10) DEFAULT 'VND',
    start_date DATE,
    end_date DATE,
    status ENUM('draft', 'created', 'in_progress', 'completed', 'cancelled') DEFAULT 'draft',
    
    -- Thông tin chi tiết (tùy chọn)
    tbmt_code VARCHAR(100),
    participant_count INT,
    hsmt_approval_decision VARCHAR(200),
    kqlcnt_approval_decision VARCHAR(200),
    winning_bid_value DECIMAL(15,2),
    winning_contractor VARCHAR(500),
    
    -- Thông tin từ Bitrix
    bitrix_task_id INT,
    bitrix_workflow_id INT,
    bitrix_status VARCHAR(100),
    
    -- Metadata
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Bảng lịch sử gói thầu
CREATE TABLE tender_package_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT NOT NULL,
    action_type ENUM('created', 'updated', 'status_changed', 'bitrix_synced') NOT NULL,
    old_value JSON,
    new_value JSON,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id)
);

-- Bảng cấu hình workflow Bitrix
CREATE TABLE bitrix_workflow_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_method ENUM('open_tender', 'limited_tender', 'direct_appointment', 'competitive_consultation', 'other') NOT NULL,
    workflow_template_id INT NOT NULL,
    workflow_name VARCHAR(200) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_method_workflow (tender_method, workflow_template_id)
);

-- Insert default workflow configurations
INSERT INTO bitrix_workflow_config (tender_method, workflow_template_id, workflow_name) VALUES
('open_tender', 1, 'Đấu thầu rộng rãi - Workflow chuẩn'),
('limited_tender', 2, 'Đấu thầu hạn chế - Workflow chuẩn'),
('direct_appointment', 3, 'Chỉ định thầu - Workflow chuẩn'),
('competitive_consultation', 4, 'Tư vấn cạnh tranh - Workflow chuẩn');
```

#### API Endpoints
```
# Tender Package Management
GET /api/tender-packages
POST /api/tender-packages
GET /api/tender-packages/{id}
PUT /api/tender-packages/{id}
DELETE /api/tender-packages/{id}

# Tender Package Creation
POST /api/tender-packages/create
{
  "name": "Gói thầu mua sắm thiết bị IT",
  "project_id": 123,
  "tender_method": "open_tender",
  "estimated_value": 1000000000,
  "start_date": "2024-01-15",
  "end_date": "2024-06-30",
  "description": "Mô tả chi tiết gói thầu"
}

# Bitrix Integration
POST /api/tender-packages/{id}/deploy-to-bitrix
GET /api/tender-packages/{id}/bitrix-status
POST /api/tender-packages/{id}/sync-from-bitrix

# Project Integration
GET /api/projects/{project_id}/tender-packages
GET /api/tender-packages/available-projects

# Tender Package History
GET /api/tender-packages/{id}/history
```

#### Frontend Components
```typescript
// Tender Package Creation Form
interface TenderPackageForm {
  // Basic Information
  name: string
  project_id: number
  tender_method: TenderMethod
  estimated_value: number
  currency: string
  start_date: Date
  end_date: Date
  description?: string
  
  // Optional Information
  tbmt_code?: string
  participant_count?: number
  hsmt_approval_decision?: string
  kqlcnt_approval_decision?: string
  winning_bid_value?: number
  winning_contractor?: string
}

// Tender Package Interface
interface TenderPackage {
  id: number
  tender_code: string
  name: string
  description?: string
  project: Project
  tender_method: TenderMethod
  estimated_value: number
  currency: string
  start_date: Date
  end_date: Date
  status: TenderStatus
  
  // Optional fields
  tbmt_code?: string
  participant_count?: number
  hsmt_approval_decision?: string
  kqlcnt_approval_decision?: string
  winning_bid_value?: number
  winning_contractor?: string
  
  // Bitrix integration
  bitrix_task_id?: number
  bitrix_workflow_id?: number
  bitrix_status?: string
  
  // Metadata
  created_by: User
  created_at: Date
  updated_by?: User
  updated_at: Date
}

// Bitrix Integration Service
interface BitrixIntegrationService {
  deployTenderPackage(tenderPackageId: number): Promise<BitrixDeploymentResult>
  getTenderPackageStatus(tenderPackageId: number): Promise<BitrixStatus>
  syncTenderPackageData(tenderPackageId: number): Promise<void>
  getWorkflowTemplate(tenderMethod: TenderMethod): Promise<WorkflowTemplate>
}
```

---

### UI/UX Design

#### Tender Package Creation Form
- **Layout:** Multi-step form với progress indicator
- **Steps:**
  1. Thông tin cơ bản
  2. Chọn dự án liên quan
  3. Cấu hình hình thức lựa chọn nhà thầu
  4. Thông tin ngân sách và thời gian
  5. Preview và xác nhận

#### Form Components
- **Project Selector:** Dropdown với search và filter
- **Tender Method Selector:** Radio buttons với description
- **Date Range Picker:** Start date và end date
- **Currency Input:** Number input với currency selector
- **Rich Text Editor:** Cho description
- **Validation Messages:** Real-time validation feedback

#### Responsive Design
- **Desktop:** Full-width form với sidebar navigation
- **Tablet:** Stacked layout với collapsible sections
- **Mobile:** Single column layout với step-by-step navigation

---

### Integration Requirements

#### Bitrix Integration
1. **Workflow Deployment**
   - Tự động tạo task trong Bitrix
   - Áp dụng workflow template theo tender method
   - Cập nhật trạng thái real-time

2. **Data Synchronization**
   - Sync thông tin từ Bitrix về hệ thống
   - Cập nhật trạng thái gói thầu
   - Log tất cả thay đổi

3. **API Integration**
   - RESTful API calls
   - Authentication với Bitrix
   - Error handling và retry mechanism

#### Project Module Integration
1. **Project Selection**
   - Load danh sách dự án từ module DMDA
   - Filter theo quyền người dùng
   - Display project information

2. **Data Validation**
   - Validate project exists
   - Check project status
   - Ensure user has access to project

---

### Security Considerations

#### Data Protection
- Encrypt sensitive tender information
- Role-based access control
- Audit trail for all changes
- Data backup và recovery

#### Access Control
- Only authorized users can create tender packages
- Project access validation
- Bitrix integration security
- API authentication và authorization

---

### Testing Strategy

#### Unit Tests
- Form validation logic
- Tender code generation
- Project integration
- Bitrix API integration

#### Integration Tests
- End-to-end tender creation flow
- Bitrix workflow deployment
- Project module integration
- Data synchronization

#### User Acceptance Tests
- Tender package creation workflow
- Project selection process
- Bitrix integration testing
- Form validation và error handling

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Bitrix API configuration
- Default workflow templates
- Environment-specific settings

#### Monitoring & Logging
- Tender creation logs
- Bitrix integration logs
- Performance monitoring
- Error tracking và alerting

---

### Documentation

#### User Manual
- Tender package creation guide
- Project selection procedures
- Bitrix integration overview
- Troubleshooting common issues

#### Technical Documentation
- API documentation
- Database schema documentation
- Bitrix integration details
- Security implementation guidelines

---

### Validation Table

#### **Bảng Validation Form Tạo Gói thầu**

##### **Thông tin Cơ bản**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Mã gói thầu | tender_code | VARCHAR(20) | Tự động sinh GT-YYYY-XXXX | ✅ | Không cho phép chỉnh sửa |
| Tên gói thầu | tender_name | VARCHAR(500) | 3-500 ký tự, không trùng lặp | ✅ | Tên mô tả gói thầu |
| Mô tả gói thầu | tender_description | TEXT | Tối đa 2000 ký tự | ❌ | Mô tả chi tiết gói thầu |
| Dự án liên quan | project_id | INT | ID hợp lệ từ bảng projects | ✅ | Chọn từ danh sách dự án |
| Hình thức lựa chọn nhà thầu | tender_method | ENUM | 'open_bidding', 'limited_bidding', 'direct_contract', 'competitive_consultation' | ✅ | Hình thức đấu thầu |

##### **Thông tin Giá trị và Ngân sách**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Giá trị dự kiến | estimated_value | DECIMAL(15,2) | > 0, định dạng tiền tệ | ✅ | Giá trị dự kiến gói thầu |
| Đơn vị tiền tệ | currency | VARCHAR(10) | VND, USD, EUR | ✅ | Mặc định VND |
| Mã TBMT | tbmt_code | VARCHAR(50) | Format: TBMT-XXXX-YYYY | ❌ | Mã thông báo mời thầu |
| Số lượng nhà thầu tham gia | participant_count | INT | >= 0 | ❌ | Số lượng nhà thầu |

##### **Thông tin Timeline**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Ngày bắt đầu dự kiến | planned_start_date | DATE | Định dạng YYYY-MM-DD | ✅ | Ngày bắt đầu dự kiến |
| Ngày kết thúc dự kiến | planned_end_date | DATE | >= planned_start_date | ✅ | Ngày kết thúc dự kiến |
| Ngày mở thầu | tender_open_date | DATE | >= planned_start_date | ❌ | Ngày mở thầu |
| Ngày đóng thầu | tender_close_date | DATE | >= tender_open_date | ❌ | Ngày đóng thầu |

##### **Thông tin Quyết định**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Quyết định phê duyệt HSMT | hsmt_approval_decision | VARCHAR(100) | Link từ Bitrix | ❌ | Quyết định phê duyệt HSMT |
| Quyết định phê duyệt KQLCNT | kqlcnt_approval_decision | VARCHAR(100) | Link từ Bitrix | ❌ | Quyết định phê duyệt KQLCNT |
| Giá trúng thầu | winning_bid_amount | DECIMAL(15,2) | > 0, <= estimated_value | ❌ | Giá trúng thầu |
| Nhà thầu trúng thầu | winning_contractor | VARCHAR(200) | Link từ Bitrix | ❌ | Nhà thầu trúng thầu |

##### **Thông tin Bổ sung**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Trạng thái gói thầu | tender_status | ENUM | 'draft', 'created', 'in_progress', 'completed', 'cancelled' | ✅ | Trạng thái hiện tại |
| Mức độ ưu tiên | priority | ENUM | 'low', 'medium', 'high', 'critical' | ✅ | Mức độ ưu tiên |
| Ghi chú | notes | TEXT | Tối đa 1000 ký tự | ❌ | Ghi chú bổ sung |
| Thẻ | tags | JSON | Mảng thẻ tối đa 10 thẻ | ❌ | Thẻ phân loại |

#### **Quy tắc Validation Nghiệp vụ**

##### **Validation Cross-field**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Timeline validation | planned_start_date có giá trị | planned_end_date >= planned_start_date | "Ngày kết thúc phải sau ngày bắt đầu" |
| Tender dates | tender_open_date có giá trị | tender_close_date >= tender_open_date | "Ngày đóng thầu phải sau ngày mở thầu" |
| Project validation | project_id có giá trị | Project phải tồn tại và active | "Dự án không tồn tại hoặc không hoạt động" |
| Winning bid | winning_bid_amount có giá trị | winning_bid_amount <= estimated_value | "Giá trúng thầu không được vượt quá giá dự kiến" |

##### **Validation Business Rules**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Mã gói thầu | Tự động sinh | Format: GT-YYYY-XXXX | "Mã gói thầu được tự động sinh" |
| Tên gói thầu | Không trùng lặp | Kiểm tra trong database | "Tên gói thầu đã tồn tại" |
| TBMT code | Format validation | TBMT-XXXX-YYYY | "Mã TBMT không đúng định dạng" |
| Participant count | Số lượng hợp lệ | >= 0 | "Số lượng nhà thầu phải >= 0" | 