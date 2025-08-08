# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-2.1
### Chỉnh sửa thông tin Hợp đồng

#### Thông tin User Story
- **Story ID:** HD-2.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 2
- **Status:** To Do
- **Phụ thuộc:** HD-1.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách hợp đồng,  
**Tôi muốn** có thể chỉnh sửa tất cả các thông tin của một hợp đồng đã tạo,  
**Để** tôi có thể cập nhật hoặc sửa chữa các thông tin sai sót hoặc thay đổi trong quá trình thực hiện hợp đồng.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Chỉnh sửa" trên trang chi tiết hợp đồng hoặc trong danh sách
- [ ] Form chỉnh sửa hiển thị tất cả thông tin hiện tại của hợp đồng
- [ ] Người dùng có thể chỉnh sửa tất cả các trường thông tin (trừ một số trường đặc biệt)
- [ ] Có validation cho các trường bắt buộc và format dữ liệu
- [ ] Có thể lưu nháp hoặc lưu hoàn thành
- [ ] Hiển thị lịch sử thay đổi thông tin hợp đồng
- [ ] Có thể hoàn tác thay đổi trong một khoảng thời gian nhất định
- [ ] Thông báo cho các bên liên quan khi có thay đổi quan trọng
- [ ] Có thể chỉnh sửa phụ lục hợp đồng
- [ ] Có thể cập nhật lịch thanh toán

#### 2.4 Activity Diagram
![HD-2.1 Activity Diagram](diagrams/HD-2.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý chỉnh sửa thông tin hợp đồng*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Giao diện Chỉnh sửa**
   - Form chỉnh sửa với tất cả thông tin hiện tại
   - Chỉnh sửa trực tiếp cho một số trường
   - Chỉnh sửa hàng loạt cho nhiều hợp đồng
   - Xem trước thay đổi trước khi lưu

2. **Xác thực Dữ liệu**
   - Xác thực thời gian thực
   - Xác thực chéo trường
   - Xác thực quy tắc kinh doanh
   - Xác thực định dạng

3. **Quản lý Thay đổi**
   - Theo dõi tất cả thay đổi
   - Lịch sử phiên bản
   - Chức năng hoàn tác
   - Quy trình phê duyệt thay đổi

4. **Kiểm soát Phân quyền**
   - Phân quyền chỉnh sửa dựa trên vai trò
   - Phân quyền cấp trường
   - Yêu cầu phê duyệt cho thay đổi quan trọng
   - Ghi log kiểm toán

#### Quy tắc Kinh doanh
- Một số trường không thể chỉnh sửa sau khi hợp đồng đã được ký
- Thay đổi giá trị hợp đồng yêu cầu phê duyệt
- Thay đổi thời gian hợp đồng cần xác thực
- Lưu lịch sử tất cả thay đổi
- Hoàn tác được phép trong 24h sau khi thay đổi

#### Các Trường Có thể Chỉnh sửa
1. **Thông tin Cơ bản**
   - Tên hợp đồng
   - Mô tả hợp đồng
   - Loại hợp đồng
   - Trạng thái hợp đồng

2. **Thông tin Tài chính**
   - Giá trị hợp đồng - cần phê duyệt
   - Điều khoản thanh toán
   - Lịch thanh toán
   - Phân bổ ngân sách

3. **Thông tin Thời gian**
   - Ngày bắt đầu hợp đồng - cần xác thực
   - Ngày kết thúc hợp đồng - cần xác thực
   - Ngày có hiệu lực
   - Ngày hoàn thành

4. **Thông tin Các bên**
   - Người quản lý hợp đồng
   - Người giám sát hợp đồng
   - Các bên liên quan khác

5. **Thông tin Phụ lục**
   - Chi tiết phụ lục
   - Ngày phụ lục
   - Phê duyệt phụ lục

6. **Thông tin Tài liệu**
   - Tài liệu hợp đồng
   - Tài liệu hỗ trợ
   - Tài liệu đính kèm bổ sung

---

#### 5.5 Sequence Diagram
![HD-2.1 Sequence Diagram](diagrams/HD-2.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi chỉnh sửa thông tin hợp đồng*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử thay đổi hợp đồng
CREATE TABLE contract_changes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type ENUM('update', 'delete', 'restore') NOT NULL,
    change_reason TEXT,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approved_by INT,
    approved_at TIMESTAMP NULL,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Bảng cấu hình quyền chỉnh sửa hợp đồng
CREATE TABLE contract_field_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    can_edit BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_role_id INT,
    edit_restrictions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (approval_role_id) REFERENCES roles(id),
    UNIQUE KEY unique_role_field (role_id, field_name)
);

-- Bảng thông báo thay đổi hợp đồng
CREATE TABLE contract_change_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    change_id INT NOT NULL,
    notification_type ENUM('email', 'sms', 'in_app') NOT NULL,
    recipient_id INT NOT NULL,
    message TEXT NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (change_id) REFERENCES contract_changes(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);

-- Bảng phiên bản hợp đồng
CREATE TABLE contract_versions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    version_number INT NOT NULL,
    contract_data JSON NOT NULL,
    change_summary TEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE KEY unique_contract_version (contract_id, version_number)
);

-- Insert default contract field permissions
INSERT INTO contract_field_permissions (role_id, field_name, can_edit, requires_approval, edit_restrictions) VALUES
-- Contract Manager - full access
(1, 'contract_name', TRUE, FALSE, NULL),
(1, 'contract_description', TRUE, FALSE, NULL),
(1, 'contract_type', TRUE, FALSE, NULL),
(1, 'contract_value', TRUE, TRUE, '{"min_value": 0, "max_percentage_change": 10}'),
(1, 'contract_start_date', TRUE, TRUE, '{"cannot_change_after_signing": true}'),
(1, 'contract_end_date', TRUE, TRUE, '{"cannot_change_after_signing": true}'),
(1, 'contract_status', TRUE, TRUE, NULL),
(1, 'payment_terms', TRUE, FALSE, NULL),
(1, 'contract_manager_id', TRUE, FALSE, NULL),
(1, 'contract_supervisor_id', TRUE, FALSE, NULL),

-- Contract Supervisor - limited access
(2, 'contract_name', TRUE, FALSE, NULL),
(2, 'contract_description', TRUE, FALSE, NULL),
(2, 'contract_type', TRUE, FALSE, NULL),
(2, 'contract_value', TRUE, TRUE, '{"min_value": 0, "max_percentage_change": 5}'),
(2, 'contract_start_date', FALSE, FALSE, NULL),
(2, 'contract_end_date', FALSE, FALSE, NULL),
(2, 'contract_status', TRUE, TRUE, NULL),
(2, 'payment_terms', TRUE, FALSE, NULL),
(2, 'contract_manager_id', FALSE, FALSE, NULL),
(2, 'contract_supervisor_id', TRUE, FALSE, NULL),

-- Contract Officer - basic access
(3, 'contract_name', TRUE, FALSE, NULL),
(3, 'contract_description', TRUE, FALSE, NULL),
(3, 'contract_type', TRUE, FALSE, NULL),
(3, 'contract_value', FALSE, FALSE, NULL),
(3, 'contract_start_date', FALSE, FALSE, NULL),
(3, 'contract_end_date', FALSE, FALSE, NULL),
(3, 'contract_status', FALSE, FALSE, NULL),
(3, 'payment_terms', TRUE, FALSE, NULL),
(3, 'contract_manager_id', FALSE, FALSE, NULL),
(3, 'contract_supervisor_id', FALSE, FALSE, NULL);
```

#### API Endpoints
```
# Contract Edit
GET /api/contracts/{id}/edit
PUT /api/contracts/{id}
PATCH /api/contracts/{id}/partial-update

# Change Management
GET /api/contracts/{id}/changes
POST /api/contracts/{id}/changes/approve
POST /api/contracts/{id}/changes/reject
POST /api/contracts/{id}/changes/rollback

# Bulk Edit
POST /api/contracts/bulk-update
{
  "contract_ids": [1, 2, 3],
  "updates": {
    "contract_status": "active",
    "payment_terms": "Updated payment terms"
  }
}

# Change History
GET /api/contracts/{id}/history
GET /api/contracts/{id}/history/{change_id}

# Contract Versions
GET /api/contracts/{id}/versions
GET /api/contracts/{id}/versions/{version_number}
POST /api/contracts/{id}/versions/restore

# Notifications
GET /api/contracts/{id}/notifications
POST /api/contracts/{id}/notifications/send
```

#### Frontend Components
```typescript
// Contract Edit Form
interface ContractEditForm {
  // Form State
  isEditing: boolean
  isSaving: boolean
  hasChanges: boolean
  validationErrors: ValidationError[]
  
  // Contract Data
  originalData: Contract
  currentData: Contract
  changes: ContractChange[]
  
  // Actions
  onFieldChange: (field: string, value: any) => void
  onSave: () => Promise<void>
  onSaveDraft: () => Promise<void>
  onCancel: () => void
  onRollback: (changeId: number) => Promise<void>
}

// Change History Component
interface ChangeHistoryComponent {
  changes: ContractChange[]
  canRollback: boolean
  onRollback: (changeId: number) => void
  onViewDetails: (changeId: number) => void
}

// Approval Workflow Component
interface ApprovalWorkflowComponent {
  pendingChanges: ContractChange[]
  userRole: UserRole
  onApprove: (changeId: number) => Promise<void>
  onReject: (changeId: number, reason: string) => Promise<void>
}

// Bulk Edit Component
interface BulkEditComponent {
  selectedContracts: Contract[]
  availableFields: string[]
  onBulkUpdate: (updates: Partial<Contract>) => Promise<void>
  onSelectAll: () => void
  onDeselectAll: () => void
}

// Contract Version Component
interface ContractVersionComponent {
  versions: ContractVersion[]
  currentVersion: number
  onViewVersion: (versionNumber: number) => void
  onRestoreVersion: (versionNumber: number) => Promise<void>
  onCompareVersions: (version1: number, version2: number) => void
}

// Amendment Edit Component
interface AmendmentEditComponent {
  contract: Contract
  amendments: ContractAmendment[]
  onAddAmendment: (amendment: ContractAmendment) => Promise<void>
  onEditAmendment: (amendmentId: number, updates: Partial<ContractAmendment>) => Promise<void>
  onDeleteAmendment: (amendmentId: number) => Promise<void>
}

// Payment Schedule Edit Component
interface PaymentScheduleEditComponent {
  contract: Contract
  paymentSchedules: PaymentSchedule[]
  onAddPayment: (payment: PaymentSchedule) => Promise<void>
  onEditPayment: (paymentId: number, updates: Partial<PaymentSchedule>) => Promise<void>
  onDeletePayment: (paymentId: number) => Promise<void>
  onBulkUpdatePayments: (updates: Partial<PaymentSchedule>) => Promise<void>
}

// Notification Component
interface ContractChangeNotificationComponent {
  notifications: ContractChangeNotification[]
  onMarkAsRead: (notificationId: number) => void
  onSendNotification: (recipients: number[], message: string) => Promise<void>
}
```

---

### UI/UX Design

#### Edit Interface
- **Layout:** Inline editing với form overlay
- **Components:**
  - Edit button trên detail page
  - Inline edit cho simple fields
  - Modal form cho complex fields
  - Bulk edit interface

#### Change Management Interface
- **Change History Panel:**
  - Timeline view của changes
  - Diff view cho field changes
  - Rollback buttons
  - Approval status indicators

#### Approval Workflow
- **Approval Interface:**
  - Pending changes list
  - Approval/reject buttons
  - Reason input for rejections
  - Notification settings

#### Bulk Edit Interface
- **Bulk Edit Modal:**
  - Selected items count
  - Field selection
  - Preview changes
  - Confirm/cancel actions

---

### Integration Requirements

#### Form Integration
1. **Edit Form**
   - Pre-populate với current data
   - Real-time validation
   - Auto-save functionality
   - Conflict resolution

2. **Change Tracking**
   - Track tất cả field changes
   - Store change metadata
   - Link changes to users
   - Maintain change history

#### Notification System
1. **Change Notifications**
   - Email notifications
   - In-app notifications
   - SMS notifications (optional)
   - Notification preferences

2. **Approval Notifications**
   - Notify approvers
   - Notify change requesters
   - Notify stakeholders
   - Escalation notifications

---

### Security Considerations

#### Access Control
- Role-based edit permissions
- Field-level permissions
- Approval requirements
- Audit logging

#### Data Protection
- Encrypt sensitive contract data
- Secure change history
- Access control
- Data backup

#### Change Validation
- Validate changes before save
- Prevent unauthorized changes
- Track change sources
- Maintain data integrity

---

### Testing Strategy

#### Unit Tests
- Edit form validation
- Change tracking logic
- Permission checking
- Notification system

#### Integration Tests
- End-to-end edit workflow
- Approval process testing
- Bulk edit functionality
- Change history tracking

#### User Acceptance Tests
- Edit interface usability
- Change approval workflow
- Bulk edit experience
- Notification system testing

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Permission configuration
- Notification settings
- Approval workflow setup

#### Monitoring & Logging
- Edit activity monitoring
- Change tracking
- Performance monitoring
- Error tracking

---

### Documentation

#### User Manual
- Edit interface guide
- Change approval procedures
- Bulk edit instructions
- Notification management

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Performance optimization 