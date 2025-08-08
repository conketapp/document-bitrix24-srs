# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-1.1
### Tạo Hợp đồng mới và nhập thông tin cần thiết

#### Thông tin User Story
- **Story ID:** HD-1.1
- **Priority:** High
- **Story Points:** 10
- **Sprint:** Sprint 1
- **Status:** To Do
- **Phụ thuộc:** GT-1.1, GT-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách hợp đồng,  
**Tôi muốn** có thể tạo một hồ sơ hợp đồng mới và nhập các thông tin cần thiết về hợp đồng,  
**Để** tôi có thể khởi tạo và quản lý các hợp đồng một cách có hệ thống.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có một form để tạo hợp đồng mới với các trường thông tin quan trọng
- [ ] Mã hợp đồng sẽ trùng với số hợp đồng (do cán bộ phụ trách hợp đồng nhập) và có thể chỉnh sửa (phân quyền chỉnh sửa)
- [ ] Các trường nhập liệu đảm bảo tính chính xác và định dạng phù hợp (ví dụ: ngày tháng, số tiền)
- [ ] Form có validation cho các trường bắt buộc và format dữ liệu
- [ ] Có thể liên kết hợp đồng với gói thầu đã có
- [ ] Hỗ trợ lưu nháp và hoàn thành sau
- [ ] Có thể upload tài liệu hợp đồng
- [ ] Hiển thị preview thông tin hợp đồng trước khi lưu
- [ ] Có thể tạo nhiều phụ lục hợp đồng

#### 2.4 Activity Diagram
![HD-1.1 Activity Diagram](diagrams/HD-1.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tạo hợp đồng mới và nhập thông tin cần thiết*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Form Tạo Hợp đồng**
   - Thông tin cơ bản hợp đồng
   - Thông tin tài chính
   - Thông tin thời gian
   - Thông tin các bên
   - Tài liệu đính kèm

2. **Xác thực Dữ liệu**
   - Xác thực thời gian thực
   - Xác thực định dạng
   - Xác thực quy tắc kinh doanh
   - Xác thực chéo trường

3. **Liên kết Hợp đồng**
   - Liên kết với gói thầu
   - Liên kết với dự án
   - Liên kết với nhà thầu
   - Liên kết với tài liệu

4. **Quản lý Hợp đồng**
   - Theo dõi trạng thái hợp đồng
   - Kiểm soát phiên bản
   - Quy trình phê duyệt
   - Mẫu hợp đồng

#### Quy tắc Kinh doanh
- Số hợp đồng phải duy nhất trong hệ thống
- Giá trị hợp đồng phải khớp với giá trị gói thầu
- Ngày hợp đồng phải hợp lý (ngày bắt đầu < ngày kết thúc)
- Trạng thái hợp đồng phải tuân theo quy trình
- Tài liệu hợp đồng phải được đính kèm

#### Các Trường Thông tin Hợp đồng
1. **Thông tin Cơ bản Hợp đồng**
   - Số hợp đồng
   - Tên hợp đồng
   - Loại hợp đồng
   - Mô tả hợp đồng
   - Trạng thái hợp đồng

2. **Thông tin Tài chính**
   - Giá trị hợp đồng
   - Đơn vị tiền tệ
   - Điều khoản thanh toán
   - Lịch thanh toán
   - Phân bổ ngân sách

3. **Thông tin Thời gian**
   - Ngày bắt đầu hợp đồng
   - Ngày kết thúc hợp đồng
   - Ngày ký hợp đồng
   - Ngày có hiệu lực
   - Ngày hoàn thành

4. **Thông tin Các bên**
   - Chủ đầu tư
   - Nhà thầu
   - Người quản lý hợp đồng
   - Người giám sát hợp đồng

5. **Thông tin Gói thầu**
   - Gói thầu liên kết
   - Hình thức lựa chọn
   - Giá trúng thầu
   - Đánh giá thầu

6. **Document Information**
   - Contract documents (tài liệu hợp đồng)
   - Supporting documents (tài liệu hỗ trợ)
   - Amendments (phụ lục hợp đồng)
   - Attachments (tài liệu đính kèm)

---

#### 5.5 Sequence Diagram
![HD-1.1 Sequence Diagram](diagrams/HD-1.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tạo hợp đồng mới*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng hợp đồng chính
CREATE TABLE contracts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_number VARCHAR(100) NOT NULL UNIQUE,
    contract_name VARCHAR(500) NOT NULL,
    contract_type ENUM('construction', 'service', 'supply', 'consulting', 'other') NOT NULL,
    contract_description TEXT,
    contract_status ENUM('draft', 'pending_approval', 'approved', 'active', 'completed', 'terminated', 'cancelled') DEFAULT 'draft',
    
    -- Financial Information
    contract_value DECIMAL(15,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'VND',
    payment_terms TEXT,
    payment_schedule JSON,
    budget_allocation JSON,
    
    -- Timeline Information
    contract_start_date DATE NOT NULL,
    contract_end_date DATE NOT NULL,
    signing_date DATE,
    effective_date DATE,
    completion_date DATE,
    
    -- Party Information
    client_id INT NOT NULL,
    contractor_id INT NOT NULL,
    contract_manager_id INT NOT NULL,
    contract_supervisor_id INT,
    
    -- Tender Package Information
    tender_package_id INT,
    tender_method VARCHAR(100),
    winning_bid_value DECIMAL(15,2),
    tender_evaluation TEXT,
    
    -- Metadata
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (client_id) REFERENCES organizations(id),
    FOREIGN KEY (contractor_id) REFERENCES organizations(id),
    FOREIGN KEY (contract_manager_id) REFERENCES users(id),
    FOREIGN KEY (contract_supervisor_id) REFERENCES users(id),
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Bảng phụ lục hợp đồng
CREATE TABLE contract_amendments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    amendment_number VARCHAR(50) NOT NULL,
    amendment_type ENUM('value_change', 'timeline_change', 'scope_change', 'other') NOT NULL,
    amendment_description TEXT NOT NULL,
    old_value JSON,
    new_value JSON,
    amendment_date DATE NOT NULL,
    effective_date DATE NOT NULL,
    approved_by INT,
    approved_at TIMESTAMP NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Bảng tài liệu hợp đồng
CREATE TABLE contract_documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    document_type ENUM('contract_main', 'amendment', 'supporting', 'attachment') NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- Bảng lịch thanh toán
CREATE TABLE payment_schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    payment_number VARCHAR(50) NOT NULL,
    payment_description TEXT NOT NULL,
    payment_amount DECIMAL(15,2) NOT NULL,
    payment_percentage DECIMAL(5,2),
    due_date DATE NOT NULL,
    payment_status ENUM('pending', 'paid', 'overdue', 'cancelled') DEFAULT 'pending',
    paid_amount DECIMAL(15,2) DEFAULT 0,
    paid_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
);

-- Bảng quyền chỉnh sửa hợp đồng
CREATE TABLE contract_edit_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    can_edit BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_field (role_id, field_name)
);

-- Insert default contract edit permissions
INSERT INTO contract_edit_permissions (role_id, field_name, can_edit, requires_approval) VALUES
-- Contract Manager - full access
(1, 'contract_number', TRUE, FALSE),
(1, 'contract_name', TRUE, FALSE),
(1, 'contract_type', TRUE, FALSE),
(1, 'contract_value', TRUE, TRUE),
(1, 'contract_start_date', TRUE, FALSE),
(1, 'contract_end_date', TRUE, FALSE),
(1, 'contract_status', TRUE, TRUE),

-- Contract Supervisor - limited access
(2, 'contract_number', FALSE, FALSE),
(2, 'contract_name', TRUE, FALSE),
(2, 'contract_type', TRUE, FALSE),
(2, 'contract_value', TRUE, TRUE),
(2, 'contract_start_date', TRUE, FALSE),
(2, 'contract_end_date', TRUE, FALSE),
(2, 'contract_status', TRUE, TRUE),

-- Contract Officer - basic access
(3, 'contract_number', TRUE, FALSE),
(3, 'contract_name', TRUE, FALSE),
(3, 'contract_type', TRUE, FALSE),
(3, 'contract_value', TRUE, TRUE),
(3, 'contract_start_date', TRUE, FALSE),
(3, 'contract_end_date', TRUE, FALSE),
(3, 'contract_status', FALSE, FALSE);
```

#### API Endpoints
```
# Contract Management
GET /api/contracts
POST /api/contracts
GET /api/contracts/{id}
PUT /api/contracts/{id}
DELETE /api/contracts/{id}

# Contract Creation
POST /api/contracts/create
{
  "contract_number": "HD-2024-001",
  "contract_name": "Hợp đồng xây dựng trụ sở",
  "contract_type": "construction",
  "contract_description": "Xây dựng trụ sở chính ngân hàng",
  "contract_value": 50000000000,
  "currency": "VND",
  "contract_start_date": "2024-01-15",
  "contract_end_date": "2024-12-31",
  "client_id": 1,
  "contractor_id": 2,
  "contract_manager_id": 3,
  "tender_package_id": 123
}

# Contract Amendments
GET /api/contracts/{id}/amendments
POST /api/contracts/{id}/amendments
PUT /api/contracts/{id}/amendments/{amendment_id}

# Contract Documents
GET /api/contracts/{id}/documents
POST /api/contracts/{id}/documents/upload
DELETE /api/contracts/{id}/documents/{document_id}

# Payment Schedules
GET /api/contracts/{id}/payment-schedules
POST /api/contracts/{id}/payment-schedules
PUT /api/contracts/{id}/payment-schedules/{schedule_id}

# Contract Validation
POST /api/contracts/validate
{
  "contract_number": "HD-2024-001",
  "contract_value": 50000000000,
  "tender_package_id": 123
}
```

#### Frontend Components
```typescript
// Contract Creation Form
interface ContractCreationForm {
  // Form State
  isCreating: boolean
  hasErrors: boolean
  validationErrors: ValidationError[]
  
  // Contract Data
  contractData: ContractFormData
  linkedTenderPackage?: TenderPackage
  selectedContractor?: Organization
  
  // Actions
  onFieldChange: (field: string, value: any) => void
  onSave: () => Promise<void>
  onSaveDraft: () => Promise<void>
  onCancel: () => void
  onValidate: () => Promise<ValidationResult>
}

// Contract Form Data Interface
interface ContractFormData {
  // Basic Information
  contract_number: string
  contract_name: string
  contract_type: ContractType
  contract_description?: string
  contract_status: ContractStatus
  
  // Financial Information
  contract_value: number
  currency: string
  payment_terms?: string
  payment_schedule?: PaymentSchedule[]
  budget_allocation?: BudgetAllocation[]
  
  // Timeline Information
  contract_start_date: Date
  contract_end_date: Date
  signing_date?: Date
  effective_date?: Date
  completion_date?: Date
  
  // Party Information
  client_id: number
  contractor_id: number
  contract_manager_id: number
  contract_supervisor_id?: number
  
  // Tender Package Information
  tender_package_id?: number
  tender_method?: string
  winning_bid_value?: number
  tender_evaluation?: string
}

// Contract Amendment Component
interface ContractAmendmentComponent {
  contract: Contract
  amendments: ContractAmendment[]
  onAddAmendment: (amendment: ContractAmendment) => Promise<void>
  onEditAmendment: (amendmentId: number, updates: Partial<ContractAmendment>) => Promise<void>
  onDeleteAmendment: (amendmentId: number) => Promise<void>
}

// Payment Schedule Component
interface PaymentScheduleComponent {
  contract: Contract
  paymentSchedules: PaymentSchedule[]
  onAddPayment: (payment: PaymentSchedule) => Promise<void>
  onEditPayment: (paymentId: number, updates: Partial<PaymentSchedule>) => Promise<void>
  onDeletePayment: (paymentId: number) => Promise<void>
}

// Contract Document Component
interface ContractDocumentComponent {
  contract: Contract
  documents: ContractDocument[]
  onUploadDocument: (file: File, documentType: DocumentType) => Promise<void>
  onDeleteDocument: (documentId: number) => Promise<void>
  onDownloadDocument: (documentId: number) => void
}

// Contract Validation Component
interface ContractValidationComponent {
  contractData: ContractFormData
  validationResult: ValidationResult
  onValidate: () => Promise<ValidationResult>
  onFixErrors: (errors: ValidationError[]) => void
}

// Contract Preview Component
interface ContractPreviewComponent {
  contract: Contract
  isVisible: boolean
  onClose: () => void
  onEdit: () => void
  onApprove: () => Promise<void>
  onReject: (reason: string) => Promise<void>
}
```

---

### UI/UX Design

#### Contract Creation Form
- **Layout:** Multi-step form với progress indicator
- **Steps:**
  1. Basic Information
  2. Financial Information
  3. Timeline Information
  4. Party Information
  5. Tender Package Linking
  6. Document Upload
  7. Preview và Confirmation

#### Form Components
- **Contract Number Input:** Text input với validation
- **Contract Type Selector:** Dropdown với descriptions
- **Currency Input:** Number input với currency selector
- **Date Range Picker:** Start date và end date
- **Party Selector:** Searchable dropdown cho organizations
- **Tender Package Linker:** Search và select tender package
- **Document Upload:** Drag & drop file upload

#### Validation Interface
- **Real-time Validation:** Inline error messages
- **Cross-field Validation:** Business rule checking
- **Format Validation:** Date, currency, number formats
- **Required Field Indicators:** Visual cues cho required fields

---

### Integration Requirements

#### Tender Package Integration
1. **Tender Package Linking**
   - Search và select tender packages
   - Auto-fill contract information
   - Validate contract value against tender value
   - Link contractor information

2. **Data Synchronization**
   - Sync contract status với tender status
   - Update tender package khi contract created
   - Maintain data consistency

#### Document Management Integration
1. **Document Upload**
   - Multiple file upload
   - File type validation
   - File size limits
   - Document categorization

2. **Document Preview**
   - PDF preview
   - Document versioning
   - Document approval workflow

---

### Security Considerations

#### Data Protection
- Encrypt sensitive contract data
- Secure document storage
- Access control cho contract information
- Audit trail cho contract changes

#### Validation Security
- Input validation cho contract data
- Business rule enforcement
- Cross-field validation
- Format validation

#### Access Control
- Role-based contract access
- Field-level permissions
- Document access control
- Approval workflow security

---

### Testing Strategy

#### Unit Tests
- Contract form validation
- Business rule validation
- Document upload testing
- Payment schedule testing

#### Integration Tests
- End-to-end contract creation
- Tender package integration
- Document management
- Payment processing

#### User Acceptance Tests
- Contract creation workflow
- Form validation experience
- Document upload testing
- Payment schedule management

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Document storage configuration
- Email notification setup
- Approval workflow configuration

#### Monitoring & Logging
- Contract creation tracking
- Document upload monitoring
- Payment schedule tracking
- Error tracking

---

### Documentation

#### User Manual
- Contract creation guide
- Document upload procedures
- Payment schedule management
- Approval workflow

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Integration details 