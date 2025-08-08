# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-1.1
### Tạo khoản mục chi phí mới và nhập thông tin chi tiết

#### Thông tin User Story
- **Story ID:** CP-1.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 1
- **Status:** To Do
- **Phụ thuộc:** Không có

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách Chi phí/Dự án/Gói thầu/Hợp đồng,  
**Tôi muốn** có thể tạo một khoản mục chi phí mới và nhập các thông tin cần thiết  
**Để** tôi có thể ghi nhận và theo dõi các khoản chi tiêu một cách có hệ thống, bao gồm cả chi phí một lần và chi phí định kỳ, đồng thời quản lý kế hoạch và thực tế thanh toán.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có một form để tạo khoản mục chi phí với đầy đủ các trường thông tin quan trọng
- [ ] Mã chi phí tự động sinh và không thể chỉnh sửa
- [ ] Các trường nhập liệu đảm bảo tính chính xác và định dạng phù hợp (ví dụ: ngày tháng, số tiền)
- [ ] Có trường "Loại Chi phí" với hai lựa chọn: "Một lần" (One-time) và "Định kỳ" (Recurring)
- [ ] Giao diện sẽ hiển thị thêm các trường thông tin đặc thù cho chi phí định kỳ:
  - "Tần suất" với 3 lựa chọn: "Tháng" (Monthly), "Quý" (Quarterly), "Năm" (Annually)
  - "Số kỳ": Nhập số lượng kỳ theo tần suất đã chọn (VD: 12 tháng, 3 quý, 2 năm,...)
  - "Hình thức nhập chi phí": Cho phép lựa chọn giữa "Cùng chi phí mỗi kỳ" hoặc "Mỗi kỳ nhập chi phí riêng"
  - Trường "Chi phí mỗi kỳ" (nếu chọn "Cùng chi phí mỗi kỳ")
  - "Ngày bắt đầu định kỳ"
- [ ] Form có validation cho tất cả các trường bắt buộc
- [ ] Có thể lưu nháp và hoàn thành sau
- [ ] Hiển thị preview thông tin chi phí trước khi lưu
- [ ] Có thể liên kết chi phí với dự án, gói thầu hoặc hợp đồng
- [ ] Hỗ trợ upload tài liệu đính kèm cho chi phí
- [ ] Có thể thiết lập người phê duyệt cho chi phí

#### 2.4 Activity Diagram
![CP-1.1 Activity Diagram](diagrams/CP-1.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tạo khoản mục chi phí mới và nhập thông tin chi tiết*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Tạo Khoản mục Chi phí**
   - Mã chi phí tự động sinh
   - Form trường thông tin đầy đủ
   - Validation thời gian thực
   - Chức năng lưu nháp

2. **Quản lý Loại Chi phí**
   - Xử lý chi phí một lần
   - Cấu hình chi phí định kỳ
   - Thiết lập tần suất
   - Quản lý kỳ hạn

3. **Validation Dữ liệu**
   - Validation định dạng trường
   - Validation quy tắc kinh doanh
   - Cross-field validation
   - Kiểm tra trường bắt buộc

4. **Hỗ trợ Tích hợp**
   - Liên kết dự án
   - Liên kết gói thầu
   - Liên kết hợp đồng
   - Đính kèm tài liệu

#### Quy tắc Kinh doanh
- Mã chi phí phải tự động sinh theo format: CP-YYYY-XXXX
- Chi phí định kỳ phải có tần suất và số kỳ
- Chi phí mỗi kỳ phải > 0
- Ngày bắt đầu định kỳ phải hợp lệ
- Tổng chi phí = Chi phí mỗi kỳ × Số kỳ (cho chi phí định kỳ)

#### Trường Thông tin Chi phí
1. **Thông tin Cơ bản**
   - Cost code (mã chi phí) - tự động sinh
   - Cost name (tên chi phí)
   - Cost description (mô tả chi phí)
   - Cost category (danh mục chi phí)
   - Cost subcategory (danh mục con)

2. **Loại Chi phí & Số tiền**
   - Cost type (loại chi phí): One-time/Recurring
   - Total amount (tổng chi phí)
   - Currency (đơn vị tiền tệ)
   - VAT amount (số tiền VAT)
   - VAT rate (tỷ lệ VAT)

3. **Trường Chi phí Định kỳ** (nếu chọn định kỳ)
   - Frequency (tần suất): Monthly/Quarterly/Annually
   - Number of periods (số kỳ)
   - Cost per period (chi phí mỗi kỳ)
   - Input method (hình thức nhập): Same cost/Different cost
   - Start date (ngày bắt đầu định kỳ)

4. **Thông tin Timeline**
   - Planned start date (ngày bắt đầu dự kiến)
   - Planned end date (ngày kết thúc dự kiến)
   - Actual start date (ngày bắt đầu thực tế)
   - Actual end date (ngày kết thúc thực tế)

5. **Related Information**
   - Project ID (mã dự án)
   - Tender package ID (mã gói thầu)
   - Contract ID (mã hợp đồng)
   - Supplier/Vendor (nhà cung cấp)
   - Approval status (trạng thái phê duyệt)

6. **Additional Information**
   - Priority (ưu tiên)
   - Risk level (mức độ rủi ro)
   - Notes (ghi chú)
   - Attachments (tài liệu đính kèm)
   - Tags (thẻ)

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng khoản mục chi phí chính
CREATE TABLE cost_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_code VARCHAR(20) NOT NULL UNIQUE, -- CP-YYYY-XXXX
    cost_name VARCHAR(500) NOT NULL,
    cost_description TEXT,
    cost_category VARCHAR(100) NOT NULL,
    cost_subcategory VARCHAR(100),
    cost_type ENUM('one_time', 'recurring') NOT NULL,
    total_amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'VND',
    vat_amount DECIMAL(15,2) DEFAULT 0,
    vat_rate DECIMAL(5,2) DEFAULT 0,
    
    -- Recurring cost fields
    frequency ENUM('monthly', 'quarterly', 'annually') NULL,
    number_of_periods INT NULL,
    cost_per_period DECIMAL(15,2) NULL,
    input_method ENUM('same_cost', 'different_cost') NULL,
    recurring_start_date DATE NULL,
    
    -- Timeline
    planned_start_date DATE,
    planned_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    
    -- Related entities
    project_id INT,
    tender_package_id INT,
    contract_id INT,
    supplier_name VARCHAR(200),
    supplier_code VARCHAR(50),
    
    -- Status and approval
    approval_status ENUM('draft', 'pending', 'approved', 'rejected', 'cancelled') DEFAULT 'draft',
    approval_notes TEXT,
    approved_by INT,
    approved_at TIMESTAMP NULL,
    
    -- Additional info
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    risk_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    notes TEXT,
    tags JSON,
    
    -- Audit fields
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id),
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    
    INDEX idx_cost_code (cost_code),
    INDEX idx_cost_type (cost_type),
    INDEX idx_approval_status (approval_status),
    INDEX idx_project_id (project_id),
    INDEX idx_contract_id (contract_id)
);

-- Bảng chi tiết kỳ thanh toán cho chi phí định kỳ
CREATE TABLE cost_periods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    period_number INT NOT NULL,
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    planned_amount DECIMAL(15,2) NOT NULL,
    actual_amount DECIMAL(15,2) DEFAULT 0,
    payment_status ENUM('pending', 'partial', 'completed', 'cancelled') DEFAULT 'pending',
    payment_date DATE NULL,
    payment_reference VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    UNIQUE KEY unique_cost_period (cost_item_id, period_number),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_payment_status (payment_status)
);

-- Bảng tài liệu đính kèm chi phí
CREATE TABLE cost_attachments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    description TEXT,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id)
);

-- Bảng lịch sử thay đổi chi phí
CREATE TABLE cost_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    action_type ENUM('created', 'updated', 'status_changed', 'approved', 'rejected') NOT NULL,
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_action_type (action_type)
);

-- Bảng cấu hình danh mục chi phí
CREATE TABLE cost_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    category_description TEXT,
    parent_category_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_category_id) REFERENCES cost_categories(id),
    UNIQUE KEY unique_category_name (category_name),
    INDEX idx_parent_category (parent_category_id),
    INDEX idx_sort_order (sort_order)
);

-- Bảng cấu hình phê duyệt chi phí
CREATE TABLE cost_approval_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_category_id INT,
    cost_amount_min DECIMAL(15,2),
    cost_amount_max DECIMAL(15,2),
    approval_level ENUM('manager', 'director', 'board') NOT NULL,
    required_approvers JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cost_category_id) REFERENCES cost_categories(id),
    INDEX idx_cost_category (cost_category_id),
    INDEX idx_amount_range (cost_amount_min, cost_amount_max)
);

-- Insert default cost categories
INSERT INTO cost_categories (category_name, category_description, sort_order) VALUES
('Nhân sự', 'Chi phí nhân sự và lao động', 1),
('Vật tư', 'Chi phí vật tư, nguyên liệu', 2),
('Thiết bị', 'Chi phí thiết bị, máy móc', 3),
('Dịch vụ', 'Chi phí dịch vụ thuê ngoài', 4),
('Vận chuyển', 'Chi phí vận chuyển, logistics', 5),
('Quản lý', 'Chi phí quản lý dự án', 6),
('Khác', 'Chi phí khác', 7);

-- Insert default approval configuration
INSERT INTO cost_approval_config (cost_category_id, cost_amount_min, cost_amount_max, approval_level, required_approvers) VALUES
(NULL, 0, 10000000, 'manager', '["manager"]'),
(NULL, 10000000, 100000000, 'director', '["manager", "director"]'),
(NULL, 100000000, NULL, 'board', '["manager", "director", "board"]');
```

#### API Endpoints
```
# Cost Item Creation
POST /api/cost-items
{
  "cost_name": "Chi phí thiết bị văn phòng",
  "cost_description": "Mua sắm thiết bị văn phòng cho dự án",
  "cost_category": "Thiết bị",
  "cost_subcategory": "Văn phòng",
  "cost_type": "one_time",
  "total_amount": 50000000,
  "currency": "VND",
  "vat_amount": 5000000,
  "vat_rate": 10.00,
  "planned_start_date": "2024-01-15",
  "planned_end_date": "2024-02-15",
  "project_id": 123,
  "contract_id": 456,
  "supplier_name": "Công ty ABC",
  "priority": "medium",
  "risk_level": "low",
  "notes": "Chi phí mua sắm thiết bị văn phòng"
}

# Recurring Cost Creation
POST /api/cost-items
{
  "cost_name": "Chi phí thuê văn phòng",
  "cost_description": "Thuê văn phòng làm việc",
  "cost_category": "Dịch vụ",
  "cost_subcategory": "Thuê văn phòng",
  "cost_type": "recurring",
  "total_amount": 120000000,
  "currency": "VND",
  "frequency": "monthly",
  "number_of_periods": 12,
  "cost_per_period": 10000000,
  "input_method": "same_cost",
  "recurring_start_date": "2024-01-01",
  "planned_start_date": "2024-01-01",
  "planned_end_date": "2024-12-31",
  "project_id": 123,
  "supplier_name": "Công ty XYZ",
  "priority": "high",
  "risk_level": "medium"
}

# Cost Item Management
GET /api/cost-items
GET /api/cost-items/{id}
PUT /api/cost-items/{id}
DELETE /api/cost-items/{id}

# Cost Periods
GET /api/cost-items/{id}/periods
POST /api/cost-items/{id}/periods
{
  "period_number": 1,
  "period_start_date": "2024-01-01",
  "period_end_date": "2024-01-31",
  "planned_amount": 10000000,
  "actual_amount": 10000000,
  "payment_status": "completed",
  "payment_date": "2024-01-15"
}

# Cost Attachments
GET /api/cost-items/{id}/attachments
POST /api/cost-items/{id}/attachments
Content-Type: multipart/form-data
{
  "file": File,
  "description": "Hóa đơn thanh toán"
}

# Cost History
GET /api/cost-items/{id}/history

# Cost Categories
GET /api/cost-categories
POST /api/cost-categories
{
  "category_name": "Marketing",
  "category_description": "Chi phí marketing và quảng cáo",
  "parent_category_id": null,
  "sort_order": 8
}

# Cost Approval
POST /api/cost-items/{id}/approve
{
  "approval_status": "approved",
  "approval_notes": "Chi phí hợp lệ, được phê duyệt"
}

POST /api/cost-items/{id}/reject
{
  "approval_status": "rejected",
  "approval_notes": "Chi phí không hợp lệ, cần bổ sung thông tin"
}

# Cost Statistics
GET /api/cost-items/statistics
Response: {
  "total_cost_items": 150,
  "total_amount": 5000000000,
  "by_type": {
    "one_time": 100,
    "recurring": 50
  },
  "by_status": {
    "draft": 20,
    "pending": 30,
    "approved": 80,
    "rejected": 20
  },
  "by_category": {
    "Nhân sự": 30,
    "Vật tư": 25,
    "Thiết bị": 20,
    "Dịch vụ": 35,
    "Khác": 40
  }
}
```

#### Frontend Components
```typescript
// Cost Item Form Component
interface CostItemFormComponent {
  costItem: Partial<CostItem>
  isEditing: boolean
  isLoading: boolean
  validationErrors: ValidationError[]
  
  onSubmit: (costItem: CostItem) => Promise<void>
  onSaveDraft: () => Promise<void>
  onCancel: () => void
  onFieldChange: (field: string, value: any) => void
}

// Cost Type Selection Component
interface CostTypeSelectionComponent {
  costType: 'one_time' | 'recurring'
  
  onCostTypeChange: (type: string) => void
  onShowRecurringFields: () => void
  onHideRecurringFields: () => void
}

// Recurring Cost Configuration Component
interface RecurringCostConfigComponent {
  frequency: 'monthly' | 'quarterly' | 'annually'
  numberOfPeriods: number
  costPerPeriod: number
  inputMethod: 'same_cost' | 'different_cost'
  recurringStartDate: Date
  
  onFrequencyChange: (frequency: string) => void
  onPeriodsChange: (periods: number) => void
  onCostPerPeriodChange: (amount: number) => void
  onInputMethodChange: (method: string) => void
  onStartDateChange: (date: Date) => void
}

// Cost Category Selection Component
interface CostCategorySelectionComponent {
  categories: CostCategory[]
  selectedCategory: string
  selectedSubcategory: string
  
  onCategoryChange: (category: string) => void
  onSubcategoryChange: (subcategory: string) => void
  onCategorySearch: (query: string) => void
}

// Cost Amount Calculation Component
interface CostAmountCalculationComponent {
  totalAmount: number
  vatAmount: number
  vatRate: number
  currency: string
  
  onTotalAmountChange: (amount: number) => void
  onVatRateChange: (rate: number) => void
  onCurrencyChange: (currency: string) => void
  onCalculateVat: () => void
}

// Cost Attachment Component
interface CostAttachmentComponent {
  costItemId: number
  attachments: CostAttachment[]
  
  onUploadFile: (file: File) => Promise<void>
  onDeleteAttachment: (attachmentId: number) => Promise<void>
  onDownloadAttachment: (attachmentId: number) => void
}

// Cost Preview Component
interface CostPreviewComponent {
  costItem: CostItem
  isOpen: boolean
  
  onClose: () => void
  onEdit: () => void
  onApprove: () => Promise<void>
  onReject: () => Promise<void>
}

// Cost Approval Component
interface CostApprovalComponent {
  costItem: CostItem
  approvalConfig: CostApprovalConfig
  
  onApprove: (notes: string) => Promise<void>
  onReject: (notes: string) => Promise<void>
  onRequestMoreInfo: (notes: string) => Promise<void>
}

// Cost Period Management Component
interface CostPeriodManagementComponent {
  costItemId: number
  periods: CostPeriod[]
  
  onAddPeriod: (period: Partial<CostPeriod>) => Promise<void>
  onUpdatePeriod: (periodId: number, updates: Partial<CostPeriod>) => Promise<void>
  onDeletePeriod: (periodId: number) => Promise<void>
  onBulkUpdatePeriods: (updates: Partial<CostPeriod>) => Promise<void>
}

// Cost Validation Component
interface CostValidationComponent {
  costItem: Partial<CostItem>
  validationErrors: ValidationError[]
  
  onValidate: () => ValidationError[]
  onShowErrors: () => void
  onClearErrors: () => void
}
```

---

### UI/UX Design

#### Cost Creation Form
- **Form Layout:**
  - Multi-step form
  - Progress indicator
  - Field grouping
  - Real-time validation

#### Cost Type Interface
- **Type Selection:**
  - Radio button selection
  - Dynamic field display
  - Conditional validation
  - Visual feedback

#### Recurring Cost Interface
- **Recurring Configuration:**
  - Frequency dropdown
  - Period input
  - Cost per period
  - Date picker

#### Form Validation
- **Validation Display:**
  - Inline error messages
  - Field highlighting
  - Summary validation
  - Real-time feedback

---

### Integration Requirements

#### Project Integration
1. **Project Linking**
   - Project selection dropdown
   - Project validation
   - Budget checking
   - Cost allocation

2. **Contract Integration**
   - Contract selection
   - Contract validation
   - Payment terms
   - Cost tracking

#### Document Integration
1. **File Upload**
   - Multiple file support
   - File type validation
   - File size limits
   - Preview functionality

2. **Document Management**
   - File storage
   - Version control
   - Access control
   - Download tracking

---

### Security Considerations

#### Data Protection
- Input validation
- SQL injection prevention
- XSS protection
- CSRF protection

#### Access Control
- Role-based permissions
- Cost item ownership
- Approval workflows
- Audit logging

---

### Testing Strategy

#### Unit Tests
- Form validation logic
- Cost calculation
- Business rules
- Data transformation

#### Integration Tests
- Database operations
- File upload
- API endpoints
- Workflow testing

#### User Acceptance Tests
- Form usability
- Validation feedback
- Error handling
- Workflow completion

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- File storage configuration
- Email service setup
- Approval workflow configuration

#### Monitoring & Logging
- Form submission tracking
- Error monitoring
- Performance tracking
- User behavior analytics

---

### Documentation

#### User Manual
- Form usage guide
- Validation rules
- Workflow procedures
- Error resolution

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Performance optimization

#### 5.5 Sequence Diagram
![CP-1.1 Sequence Diagram](diagrams/CP-1.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tạo khoản mục chi phí mới và nhập thông tin chi tiết* 