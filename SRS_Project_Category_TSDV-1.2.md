# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-1.2
### Chỉnh sửa thông tin Tài sản/Dịch vụ

#### Thông tin User Story
- **Story ID:** TSDV-1.2
- **Priority:** High
- **Story Points:** 4
- **Sprint:** Sprint 1
- **Status:** To Do
- **Dependencies:** TSDV-1.1

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý tài sản/dịch vụ,  
**Tôi muốn** có thể chỉnh sửa các thông tin của một khoản mục tài sản hoặc dịch vụ đã tạo  
**Để** tôi có thể cập nhật khi có thay đổi về đặc tính, trạng thái hoặc thông số.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Chỉnh sửa" trên trang chi tiết hoặc trong danh sách
- [ ] Các thông tin được cập nhật phải được lưu lại chính xác
- [ ] Có thể chỉnh sửa tất cả các trường thông tin của tài sản/dịch vụ
- [ ] Có thể chỉnh sửa thông tin chi tiết tùy theo loại (tài sản/dịch vụ)
- [ ] Có thể thay đổi người phụ trách tài sản/dịch vụ
- [ ] Có thể cập nhật trạng thái tài sản/dịch vụ
- [ ] Có thể thêm/xóa/sửa tài liệu đính kèm
- [ ] Có thể xem lịch sử thay đổi của tài sản/dịch vụ
- [ ] Có thể hoàn tác thay đổi nếu cần
- [ ] Có thể lưu bản nháp khi chỉnh sửa
- [ ] Có thể xuất thông tin đã chỉnh sửa
- [ ] Có thể gửi thông báo khi có thay đổi quan trọng

---

### Functional Requirements

#### Core Features
1. **Edit Functionality**
   - Edit basic information
   - Edit detailed information
   - Edit attachments
   - Edit assignments

2. **Change Management**
   - Change history tracking
   - Change approval workflow
   - Change notifications
   - Change rollback

3. **Validation System**
   - Data validation
   - Permission validation
   - Business rule validation
   - Conflict detection

4. **Documentation**
   - Change documentation
   - Version control
   - Audit trail
   - Export capabilities

#### Business Rules
- Chỉ người có quyền mới có thể chỉnh sửa tài sản/dịch vụ
- Một số thay đổi quan trọng cần được phê duyệt
- Lịch sử thay đổi phải được lưu trữ đầy đủ
- Thông báo phải được gửi khi có thay đổi quan trọng
- Có thể hoàn tác thay đổi trong một khoảng thời gian nhất định

#### Editable Fields
1. **Basic Information**
   - Name
   - Description
   - Category
   - Subcategory
   - Status
   - Priority

2. **Asset-specific Fields**
   - Model
   - Specifications
   - Serial number
   - Manufacturer
   - Supplier
   - Purchase date
   - Purchase cost
   - Current value
   - Location
   - Warranty information

3. **Service-specific Fields**
   - Service level agreement
   - Service provider
   - Service contact
   - Start date
   - End date
   - Service cost
   - Billing frequency
   - Performance metrics

4. **Assignment Information**
   - Responsible person
   - Assigned by
   - Assignment date
   - Assignment notes

5. **Documentation**
   - Attachments
   - Notes
   - Tags
   - Related documents

#### Change Types
1. **Minor Changes**
   - Description updates
   - Note additions
   - Tag modifications
   - Attachment updates

2. **Major Changes**
   - Status changes
   - Assignment changes
   - Cost modifications
   - Location changes

3. **Critical Changes**
   - Category changes
   - Project reassignment
   - Disposal/retirement
   - Significant cost changes

#### Approval Workflow
1. **Automatic Approval**
   - Minor changes
   - Non-critical updates
   - User's own assets/services

2. **Manager Approval**
   - Major changes
   - Status changes
   - Assignment changes

3. **Admin Approval**
   - Critical changes
   - Category changes
   - Disposal decisions

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử thay đổi tài sản/dịch vụ
CREATE TABLE asset_service_changes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    change_type ENUM('basic_info', 'detailed_info', 'assignment', 'status', 'attachment', 'documentation') NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_reason VARCHAR(500),
    change_priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    is_approved BOOLEAN DEFAULT FALSE,
    approved_by INT NULL,
    approved_at TIMESTAMP NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_change_type (change_type),
    INDEX idx_is_approved (is_approved),
    INDEX idx_created_at (created_at)
);

-- Bảng phiên bản tài sản/dịch vụ
CREATE TABLE asset_service_versions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    version_number INT NOT NULL,
    version_data JSON NOT NULL,
    version_notes TEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE KEY unique_version (asset_service_id, version_number),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_version_number (version_number)
);

-- Bảng phê duyệt thay đổi
CREATE TABLE asset_service_approvals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    change_id INT NOT NULL,
    approver_id INT NOT NULL,
    approval_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approval_notes TEXT,
    approved_at TIMESTAMP NULL,
    
    FOREIGN KEY (change_id) REFERENCES asset_service_changes(id) ON DELETE CASCADE,
    FOREIGN KEY (approver_id) REFERENCES users(id),
    INDEX idx_change_id (change_id),
    INDEX idx_approval_status (approval_status)
);

-- Bảng thông báo thay đổi
CREATE TABLE asset_service_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    change_id INT NOT NULL,
    notification_type ENUM('change_made', 'change_approved', 'change_rejected', 'approval_required') NOT NULL,
    recipient_id INT NOT NULL,
    notification_message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    FOREIGN KEY (change_id) REFERENCES asset_service_changes(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_recipient_id (recipient_id),
    INDEX idx_is_read (is_read)
);

-- Bảng cấu hình quyền chỉnh sửa
CREATE TABLE asset_service_edit_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_role VARCHAR(100) NOT NULL,
    asset_service_type ENUM('asset', 'service', 'all') NOT NULL,
    editable_fields JSON NOT NULL,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_level ENUM('none', 'manager', 'admin') DEFAULT 'none',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_role_type (user_role, asset_service_type),
    INDEX idx_user_role (user_role),
    INDEX idx_is_active (is_active)
);

-- Insert default edit permissions
INSERT INTO asset_service_edit_permissions (user_role, asset_service_type, editable_fields, requires_approval, approval_level) VALUES
('asset_manager', 'asset', '["name", "description", "category", "status", "location", "responsible_person"]', false, 'none'),
('service_manager', 'service', '["name", "description", "category", "status", "service_provider", "responsible_person"]', false, 'none'),
('admin', 'all', '["*"]', false, 'none'),
('user', 'all', '["description", "notes"]', true, 'manager');
```

#### API Endpoints
```typescript
# Get Asset/Service for Editing
GET /api/assets-services/{id}/edit
{
  "include_history": true,
  "include_versions": true
}
Response: {
  "asset_service": {
    "id": 123,
    "asset_service_code": "TS2024000001",
    "name": "Máy chủ Dell PowerEdge R740",
    "description": "Máy chủ vật lý cho hệ thống ERP",
    "type": "asset",
    "category": "Hardware",
    "subcategory": "Server",
    "status": "active",
    "priority": "high",
    "responsible_person_id": 456,
    "source_project_id": 123,
    "asset_details": {
      "model": "PowerEdge R740",
      "specifications": "Intel Xeon, 32GB RAM, 2TB SSD",
      "serial_number": "DELL123456789",
      "manufacturer": "Dell Technologies",
      "supplier": "Dell Vietnam",
      "purchase_date": "2024-01-15",
      "purchase_cost": 45000000,
      "current_value": 40000000,
      "location": "Data Center A"
    },
    "attachments": [
      {
        "id": 1,
        "file_name": "technical_specs.pdf",
        "file_size": 1024000,
        "uploaded_at": "2024-01-25T10:30:00Z"
      }
    ]
  },
  "edit_permissions": {
    "can_edit_basic": true,
    "can_edit_details": true,
    "can_change_assignment": true,
    "can_change_status": true,
    "requires_approval": false
  },
  "change_history": [
    {
      "id": 1,
      "change_type": "basic_info",
      "field_name": "status",
      "old_value": "draft",
      "new_value": "active",
      "created_at": "2024-01-25T09:00:00Z",
      "created_by": "Nguyễn Văn A"
    }
  ]
}

# Update Asset/Service
PUT /api/assets-services/{id}
{
  "name": "Máy chủ Dell PowerEdge R740 (Updated)",
  "description": "Máy chủ vật lý cho hệ thống ERP - Đã nâng cấp RAM",
  "status": "maintenance",
  "priority": "critical",
  "responsible_person_id": 789,
  "asset_details": {
    "specifications": "Intel Xeon, 64GB RAM, 2TB SSD",
    "current_value": 42000000,
    "location": "Data Center B"
  },
  "change_reason": "Nâng cấp RAM và chuyển vị trí",
  "notify_approvers": true
}
Response: {
  "success": true,
  "asset_service_id": 123,
  "change_id": 456,
  "requires_approval": false,
  "message": "Tài sản đã được cập nhật thành công"
}

# Get Change History
GET /api/assets-services/{id}/changes
{
  "change_type": "basic_info",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "changes": [
    {
      "id": 1,
      "change_type": "basic_info",
      "field_name": "status",
      "old_value": "draft",
      "new_value": "active",
      "change_reason": "Kích hoạt tài sản",
      "change_priority": "medium",
      "is_approved": true,
      "approved_by": "Nguyễn Văn B",
      "approved_at": "2024-01-25T10:00:00Z",
      "created_by": "Nguyễn Văn A",
      "created_at": "2024-01-25T09:00:00Z"
    },
    {
      "id": 2,
      "change_type": "detailed_info",
      "field_name": "specifications",
      "old_value": "Intel Xeon, 32GB RAM, 2TB SSD",
      "new_value": "Intel Xeon, 64GB RAM, 2TB SSD",
      "change_reason": "Nâng cấp RAM",
      "change_priority": "high",
      "is_approved": false,
      "created_by": "Nguyễn Văn A",
      "created_at": "2024-01-25T11:00:00Z"
    }
  ],
  "summary": {
    "total_changes": 5,
    "approved_changes": 3,
    "pending_changes": 2,
    "rejected_changes": 0
  }
}

# Approve/Reject Change
POST /api/assets-services/changes/{change_id}/approve
{
  "approval_status": "approved",
  "approval_notes": "Thay đổi hợp lý và cần thiết",
  "notify_creator": true
}
Response: {
  "success": true,
  "change_id": 456,
  "approval_status": "approved",
  "approved_by": "Nguyễn Văn B",
  "approved_at": "2024-01-25T12:00:00Z"
}

# Rollback Change
POST /api/assets-services/{id}/rollback
{
  "change_id": 456,
  "rollback_reason": "Thay đổi không phù hợp",
  "notify_affected_users": true
}
Response: {
  "success": true,
  "asset_service_id": 123,
  "rolled_back_change": 456,
  "message": "Thay đổi đã được hoàn tác thành công"
}

# Save Draft Changes
POST /api/assets-services/{id}/save-draft
{
  "draft_data": {
    "name": "Máy chủ Dell PowerEdge R740 (Draft)",
    "description": "Máy chủ vật lý cho hệ thống ERP - Bản nháp",
    "status": "maintenance",
    "asset_details": {
      "specifications": "Intel Xeon, 64GB RAM, 2TB SSD",
      "location": "Data Center B"
    }
  },
  "draft_notes": "Chỉnh sửa tạm thời, chưa hoàn thiện"
}
Response: {
  "success": true,
  "draft_id": "DRAFT-2024-001",
  "message": "Bản nháp đã được lưu thành công"
}

# Get Edit Permissions
GET /api/assets-services/{id}/edit-permissions
{
  "user_id": 456
}
Response: {
  "user_id": 456,
  "user_role": "asset_manager",
  "permissions": {
    "can_edit_basic": true,
    "can_edit_details": true,
    "can_change_assignment": true,
    "can_change_status": true,
    "can_change_category": false,
    "can_change_project": false,
    "requires_approval": false,
    "approval_level": "none"
  },
  "editable_fields": [
    "name", "description", "category", "status", "location", 
    "responsible_person", "model", "specifications", "current_value"
  ],
  "restricted_fields": [
    "asset_service_code", "type", "source_project_id", "created_by"
  ]
}

# Export Change History
GET /api/assets-services/{id}/changes/export
{
  "format": "excel",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "include_details": true
}
Response: File download with change history

# Get Pending Approvals
GET /api/assets-services/approvals/pending
{
  "approver_id": 789,
  "change_type": "basic_info"
}
Response: {
  "pending_approvals": [
    {
      "id": 456,
      "asset_service_id": 123,
      "asset_service_name": "Máy chủ Dell PowerEdge R740",
      "change_type": "detailed_info",
      "field_name": "specifications",
      "old_value": "Intel Xeon, 32GB RAM, 2TB SSD",
      "new_value": "Intel Xeon, 64GB RAM, 2TB SSD",
      "change_reason": "Nâng cấp RAM",
      "change_priority": "high",
      "created_by": "Nguyễn Văn A",
      "created_at": "2024-01-25T11:00:00Z"
    }
  ],
  "summary": {
    "total_pending": 5,
    "high_priority": 2,
    "critical_priority": 1
  }
}
```

#### Frontend Components
```typescript
// Asset/Service Edit Form Component
interface AssetServiceEditFormComponent {
  assetService: AssetService
  editPermissions: EditPermissions
  originalData: AssetService
  
  onFieldChange: (field: string, value: any) => void
  onSave: (data: any) => Promise<void>
  onSaveDraft: (data: any) => Promise<void>
  onCancel: () => void
  onReset: () => void
}

// Change History Component
interface ChangeHistoryComponent {
  changes: AssetServiceChange[]
  changeSummary: ChangeSummary
  
  onChangeSelect: (change: AssetServiceChange) => void
  onChangeFilter: (filters: ChangeFilters) => void
  onChangeExport: () => void
  onChangeRollback: (changeId: number) => void
}

// Approval Component
interface ApprovalComponent {
  pendingApprovals: PendingApproval[]
  
  onApprovalSelect: (approval: PendingApproval) => void
  onApprove: (approvalId: number, notes: string) => Promise<void>
  onReject: (approvalId: number, reason: string) => Promise<void>
  onApprovalFilter: (filters: ApprovalFilters) => void
}

// Edit Permissions Component
interface EditPermissionsComponent {
  permissions: EditPermissions
  editableFields: string[]
  restrictedFields: string[]
  
  onPermissionChange: (permissions: EditPermissions) => void
  onFieldToggle: (field: string, editable: boolean) => void
  onPermissionSave: () => void
}

// Version Control Component
interface VersionControlComponent {
  versions: AssetServiceVersion[]
  currentVersion: number
  
  onVersionSelect: (version: AssetServiceVersion) => void
  onVersionCompare: (version1: number, version2: number) => void
  onVersionRestore: (version: number) => void
  onVersionExport: (version: number) => void
}

// Change Notification Component
interface ChangeNotificationComponent {
  notifications: ChangeNotification[]
  
  onNotificationRead: (notificationId: number) => void
  onNotificationAction: (notification: ChangeNotification) => void
  onNotificationSettings: () => void
}

// Edit Validation Component
interface EditValidationComponent {
  validationRules: ValidationRule[]
  validationErrors: ValidationError[]
  
  onValidate: (data: any) => ValidationResult
  onClearErrors: () => void
  onShowErrors: (errors: ValidationError[]) => void
}

// Change Comparison Component
interface ChangeComparisonComponent {
  oldData: AssetService
  newData: AssetService
  
  onHighlightChanges: () => void
  onShowDifferences: () => void
  onAcceptChanges: () => void
  onRejectChanges: () => void
}

// Edit Workflow Component
interface EditWorkflowComponent {
  workflowSteps: WorkflowStep[]
  currentStep: number
  
  onStepComplete: (step: number) => void
  onStepBack: (step: number) => void
  onWorkflowComplete: () => void
  onWorkflowCancel: () => void
}
```

---

### UI/UX Design

#### Edit Form Interface
- **Form Layout:**
  - Edit mode indicators
  - Field validation
  - Change highlighting
  - Action buttons

#### Change History Interface
- **History Layout:**
  - Change timeline
  - Change details
  - Approval status
  - Rollback options

#### Approval Interface
- **Approval Design:**
  - Pending approvals list
  - Change comparison
  - Approval actions
  - Notification settings

#### Version Control Interface
- **Version Layout:**
  - Version timeline
  - Version comparison
  - Restore options
  - Export options

---

### Integration Requirements

#### Change Management Integration
1. **Workflow Engine**
   - Approval workflows
   - Change notifications
   - Status tracking
   - Audit logging

2. **Notification System**
   - Email notifications
   - In-app notifications
   - SMS alerts
   - System messages

#### Version Control Integration
1. **Version Management**
   - Version creation
   - Version comparison
   - Version restoration
   - Version export

2. **Document Management**
   - Document versioning
   - Change tracking
   - Document comparison
   - Document export

---

### Security Considerations

#### Data Protection
- Change authorization
- Data validation
- Permission checks
- Audit logging

#### Change Security
- Approval workflows
- Change tracking
- Rollback protection
- Access control

---

### Testing Strategy

#### Unit Tests
- Edit form validation
- Change tracking logic
- Approval workflows
- Permission validation

#### Integration Tests
- Change management
- Notification delivery
- Version control
- Workflow integration

#### User Acceptance Tests
- Edit workflow
- Approval process
- Change history
- Rollback functionality

---

### Deployment & Configuration

#### Environment Setup
- Change management setup
- Approval workflow configuration
- Notification system setup
- Version control setup

#### Monitoring & Logging
- Change monitoring
- Approval tracking
- Performance monitoring
- Error logging

---

### Documentation

#### User Manual
- Edit procedures
- Approval workflows
- Change history
- Rollback procedures

#### Technical Documentation
- API documentation
- Change management
- Integration guides
- Configuration guides 