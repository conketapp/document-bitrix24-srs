# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-2.1
### Chỉnh sửa thông tin khoản mục chi phí

#### Thông tin User Story
- **Story ID:** CP-2.1
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** có thể chỉnh sửa thông tin của một khoản mục chi phí đã tạo  
**Để** tôi có thể cập nhật các thông tin sai sót hoặc thay đổi liên quan đến chi phí.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Chỉnh sửa" trên trang chi tiết khoản mục chi phí hoặc trong danh sách
- [ ] Khi nhấn nút "Chỉnh sửa", hệ thống chuyển sang chế độ chỉnh sửa với form đầy đủ thông tin
- [ ] Tất cả các trường thông tin có thể chỉnh sửa (trừ mã chi phí)
- [ ] Hệ thống hiển thị thông tin hiện tại trong form chỉnh sửa
- [ ] Có validation cho các trường bắt buộc và định dạng dữ liệu
- [ ] Có nút "Lưu" và "Hủy" trong chế độ chỉnh sửa
- [ ] Hệ thống hiển thị thông báo xác nhận khi lưu thành công
- [ ] Hệ thống ghi log lịch sử thay đổi thông tin
- [ ] Có thể chỉnh sửa từ cả trang chi tiết và danh sách chi phí
- [ ] Hỗ trợ chỉnh sửa inline cho một số trường đơn giản
- [ ] Có thể xem lịch sử thay đổi của khoản mục chi phí

---

### Functional Requirements

#### Core Features
1. **Edit Mode Activation**
   - Edit button in cost item detail view
   - Edit button in cost item list view
   - Inline editing for simple fields
   - Bulk edit capabilities

2. **Form Pre-population**
   - Load existing cost item data
   - Maintain data integrity
   - Handle complex field relationships
   - Preserve calculated fields

3. **Validation & Error Handling**
   - Real-time validation
   - Business rule enforcement
   - Cross-field validation
   - Error message display

4. **Change Tracking**
   - Change history logging
   - User attribution
   - Timestamp tracking
   - Change reason documentation

#### Business Rules
- Mã chi phí không thể chỉnh sửa sau khi đã tạo
- Chỉ người tạo hoặc người có quyền mới được chỉnh sửa
- Một số trường có thể bị khóa chỉnh sửa tùy theo trạng thái phê duyệt
- Thay đổi thông tin quan trọng có thể yêu cầu phê duyệt lại
- Lịch sử thay đổi phải được ghi lại đầy đủ

#### Editable Fields
1. **Basic Information**
   - Tên chi phí (Cost name)
   - Mô tả chi phí (Cost description)
   - Danh mục chi phí (Cost category)
   - Danh mục con (Cost subcategory)

2. **Amount & Financial**
   - Tổng chi phí (Total amount)
   - Số tiền VAT (VAT amount)
   - Tỷ lệ VAT (VAT rate)
   - Đơn vị tiền tệ (Currency)

3. **Timeline Information**
   - Ngày bắt đầu dự kiến (Planned start date)
   - Ngày kết thúc dự kiến (Planned end date)
   - Ngày bắt đầu thực tế (Actual start date)
   - Ngày kết thúc thực tế (Actual end date)

4. **Related Information**
   - Dự án liên quan (Project ID)
   - Gói thầu (Tender package ID)
   - Hợp đồng (Contract ID)
   - Nhà cung cấp (Supplier/Vendor)

5. **Additional Information**
   - Ưu tiên (Priority)
   - Mức độ rủi ro (Risk level)
   - Ghi chú (Notes)
   - Thẻ (Tags)

6. **Recurring Cost Fields** (nếu là chi phí định kỳ)
   - Tần suất (Frequency)
   - Số kỳ (Number of periods)
   - Chi phí mỗi kỳ (Cost per period)
   - Ngày bắt đầu định kỳ (Recurring start date)

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử thay đổi thông tin chi phí
CREATE TABLE cost_item_changes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type ENUM('created', 'updated', 'deleted') NOT NULL,
    changed_by INT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    change_reason VARCHAR(500) NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_changed_at (changed_at),
    INDEX idx_field_name (field_name)
);

-- Bảng cấu hình quyền chỉnh sửa
CREATE TABLE cost_edit_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_role VARCHAR(50) NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    can_edit BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_level ENUM('manager', 'director', 'board') NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_role_field (user_role, field_name),
    INDEX idx_user_role (user_role),
    INDEX idx_field_name (field_name)
);

-- Bảng trạng thái chỉnh sửa
CREATE TABLE cost_edit_status (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    is_editing BOOLEAN DEFAULT FALSE,
    edited_by INT NULL,
    edit_started_at TIMESTAMP NULL,
    edit_session_id VARCHAR(100) NULL,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (edited_by) REFERENCES users(id),
    UNIQUE KEY unique_cost_item (cost_item_id),
    INDEX idx_edit_session (edit_session_id)
);

-- Insert default edit permissions
INSERT INTO cost_edit_permissions (user_role, field_name, can_edit, requires_approval) VALUES
('cost_manager', 'cost_name', TRUE, FALSE),
('cost_manager', 'total_amount', TRUE, TRUE),
('cost_manager', 'vat_amount', TRUE, TRUE),
('cost_manager', 'planned_start_date', TRUE, FALSE),
('cost_manager', 'planned_end_date', TRUE, FALSE),
('cost_manager', 'project_id', TRUE, TRUE),
('cost_manager', 'contract_id', TRUE, TRUE),
('cost_manager', 'supplier_name', TRUE, FALSE),
('cost_manager', 'priority', TRUE, FALSE),
('cost_manager', 'risk_level', TRUE, FALSE),
('cost_manager', 'notes', TRUE, FALSE),
('cost_manager', 'tags', TRUE, FALSE);
```

#### API Endpoints
```typescript
# Cost Item Edit Management
GET /api/cost-items/{id}/edit
Response: {
  "cost_item": {
    "id": 123,
    "cost_code": "CP-2024-0001",
    "cost_name": "Chi phí thiết bị văn phòng",
    "cost_description": "Mua sắm thiết bị văn phòng cho dự án",
    "cost_category": "Thiết bị",
    "cost_subcategory": "Văn phòng",
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
    "notes": "Chi phí mua sắm thiết bị văn phòng",
    "tags": ["thiết bị", "văn phòng"]
  },
  "edit_permissions": {
    "cost_name": true,
    "total_amount": true,
    "vat_amount": true,
    "planned_start_date": true,
    "planned_end_date": true,
    "project_id": true,
    "contract_id": true,
    "supplier_name": true,
    "priority": true,
    "risk_level": true,
    "notes": true,
    "tags": true
  },
  "approval_required": {
    "total_amount": true,
    "vat_amount": true,
    "project_id": true,
    "contract_id": true
  }
}

PUT /api/cost-items/{id}/edit
{
  "cost_name": "Chi phí thiết bị văn phòng - Cập nhật",
  "cost_description": "Mua sắm thiết bị văn phòng cho dự án - Phiên bản mới",
  "total_amount": 55000000,
  "vat_amount": 5500000,
  "planned_start_date": "2024-01-20",
  "planned_end_date": "2024-02-20",
  "supplier_name": "Công ty ABC - Chi nhánh mới",
  "priority": "high",
  "notes": "Cập nhật thông tin chi phí theo yêu cầu mới",
  "change_reason": "Cập nhật theo yêu cầu của ban quản lý"
}

# Inline Edit
PATCH /api/cost-items/{id}/inline-edit
{
  "field_name": "cost_name",
  "new_value": "Chi phí thiết bị văn phòng - Cập nhật",
  "change_reason": "Sửa lỗi chính tả"
}

# Bulk Edit
PUT /api/cost-items/bulk-edit
{
  "cost_item_ids": [123, 124, 125],
  "updates": {
    "supplier_name": "Công ty ABC - Chi nhánh mới",
    "priority": "high",
    "notes": "Cập nhật thông tin nhà cung cấp"
  },
  "change_reason": "Cập nhật thông tin nhà cung cấp cho tất cả chi phí"
}

# Edit History
GET /api/cost-items/{id}/edit-history
Response: [
  {
    "id": 1,
    "field_name": "cost_name",
    "old_value": "Chi phí thiết bị văn phòng",
    "new_value": "Chi phí thiết bị văn phòng - Cập nhật",
    "change_type": "updated",
    "changed_by": 456,
    "changed_at": "2024-01-25T10:30:00Z",
    "change_reason": "Cập nhật theo yêu cầu của ban quản lý"
  },
  {
    "id": 2,
    "field_name": "total_amount",
    "old_value": "50000000",
    "new_value": "55000000",
    "change_type": "updated",
    "changed_by": 456,
    "changed_at": "2024-01-25T10:30:00Z",
    "change_reason": "Điều chỉnh chi phí theo thực tế"
  }
]

# Edit Permissions
GET /api/cost-items/{id}/edit-permissions
Response: {
  "user_role": "cost_manager",
  "permissions": {
    "cost_name": {
      "can_edit": true,
      "requires_approval": false
    },
    "total_amount": {
      "can_edit": true,
      "requires_approval": true,
      "approval_level": "manager"
    }
  }
}

# Edit Status
GET /api/cost-items/{id}/edit-status
Response: {
  "is_editing": false,
  "edited_by": null,
  "edit_started_at": null,
  "edit_session_id": null
}

POST /api/cost-items/{id}/start-edit
{
  "session_id": "edit_session_123"
}

POST /api/cost-items/{id}/end-edit
{
  "session_id": "edit_session_123"
}

# Edit Validation
POST /api/cost-items/{id}/validate-edit
{
  "cost_name": "Chi phí thiết bị văn phòng - Cập nhật",
  "total_amount": 55000000,
  "planned_start_date": "2024-01-20"
}
Response: {
  "is_valid": true,
  "errors": [],
  "warnings": [
    "Tổng chi phí tăng 10% so với ban đầu"
  ]
}
```

#### Frontend Components
```typescript
// Cost Item Edit Component
interface CostItemEditComponent {
  costItemId: number
  costItem: CostItem
  isEditing: boolean
  editPermissions: EditPermissions
  
  onStartEdit: () => void
  onSaveEdit: (updates: Partial<CostItem>) => Promise<void>
  onCancelEdit: () => void
  onFieldChange: (field: string, value: any) => void
}

// Edit Form Component
interface CostItemEditFormComponent {
  costItem: CostItem
  originalCostItem: CostItem
  validationErrors: ValidationError[]
  
  onFieldUpdate: (field: string, value: any) => void
  onValidate: () => ValidationError[]
  onReset: () => void
  onSave: () => Promise<void>
}

// Inline Edit Component
interface InlineEditComponent {
  fieldName: string
  currentValue: any
  fieldType: 'text' | 'number' | 'date' | 'select' | 'textarea'
  options?: any[]
  
  onValueChange: (value: any) => void
  onSave: (value: any) => Promise<void>
  onCancel: () => void
}

// Bulk Edit Component
interface BulkEditComponent {
  selectedCostItems: number[]
  availableFields: string[]
  
  onSelectItems: (itemIds: number[]) => void
  onFieldUpdate: (field: string, value: any) => void
  onApplyBulkEdit: () => Promise<void>
  onClearSelection: () => void
}

// Edit History Component
interface EditHistoryComponent {
  costItemId: number
  editHistory: CostItemChange[]
  
  onViewHistory: () => void
  onExportHistory: () => void
  onFilterHistory: (filters: EditHistoryFilters) => void
}

// Edit Permissions Component
interface EditPermissionsComponent {
  userRole: string
  permissions: EditPermission[]
  
  onPermissionChange: (field: string, canEdit: boolean) => void
  onApprovalChange: (field: string, requiresApproval: boolean) => void
}

// Edit Status Component
interface EditStatusComponent {
  costItemId: number
  editStatus: EditStatus
  
  onStartEdit: () => Promise<void>
  onEndEdit: () => Promise<void>
  onLockEdit: () => Promise<void>
  onUnlockEdit: () => Promise<void>
}

// Edit Validation Component
interface EditValidationComponent {
  costItem: Partial<CostItem>
  validationRules: ValidationRule[]
  
  onValidate: () => ValidationResult
  onShowErrors: () => void
  onClearErrors: () => void
}

// Edit Confirmation Component
interface EditConfirmationComponent {
  changes: CostItemChange[]
  isVisible: boolean
  
  onConfirm: () => Promise<void>
  onCancel: () => void
  onReviewChanges: () => void
}

// Edit Approval Component
interface EditApprovalComponent {
  costItemId: number
  changes: CostItemChange[]
  approvalLevel: string
  
  onRequestApproval: () => Promise<void>
  onApprove: (notes: string) => Promise<void>
  onReject: (notes: string) => Promise<void>
}
```

---

### UI/UX Design

#### Edit Mode Interface
- **Edit Activation:**
  - Prominent edit button
  - Inline edit indicators
  - Edit mode toggle
  - Visual feedback

#### Edit Form Design
- **Form Layout:**
  - Pre-populated fields
  - Field grouping
  - Validation indicators
  - Save/cancel actions

#### Inline Editing
- **Inline Interface:**
  - Click-to-edit functionality
  - Auto-save options
  - Validation feedback
  - Undo functionality

#### Change Tracking
- **History Display:**
  - Timeline view
  - Change details
  - User attribution
  - Diff highlighting

---

### Integration Requirements

#### Cost Item Integration
1. **Data Synchronization**
   - Real-time updates
   - Conflict resolution
   - Data consistency
   - Change propagation

2. **Permission Management**
   - Role-based access
   - Field-level permissions
   - Approval workflows
   - Audit logging

#### Approval Integration
1. **Approval Workflow**
   - Automatic approval routing
   - Approval notifications
   - Status tracking
   - Decision logging

2. **Change Management**
   - Change impact analysis
   - Dependency tracking
   - Rollback capabilities
   - Version control

---

### Security Considerations

#### Data Protection
- Edit permission validation
- Change authorization
- Data integrity checks
- Audit trail maintenance

#### Access Control
- Role-based editing
- Field-level permissions
- Session management
- Concurrent edit prevention

---

### Testing Strategy

#### Unit Tests
- Edit permission logic
- Validation rules
- Change tracking
- Business rule enforcement

#### Integration Tests
- Database operations
- API endpoint testing
- Approval workflow
- Concurrent editing

#### User Acceptance Tests
- Edit workflow completion
- Permission validation
- Change history accuracy
- Approval process

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Permission configuration
- Approval workflow setup
- Audit logging configuration

#### Monitoring & Logging
- Edit activity tracking
- Performance monitoring
- Error logging
- User behavior analytics

---

### Documentation

#### User Manual
- Edit procedures
- Permission guidelines
- Approval process
- Change tracking

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Integration guides 