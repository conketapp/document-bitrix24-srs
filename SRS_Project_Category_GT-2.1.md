# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-2.1
### Chỉnh sửa thông tin Gói thầu

#### Thông tin User Story
- **Story ID:** GT-2.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** GT-1.1, GT-1.2

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể chỉnh sửa tất cả các thông tin của một gói thầu đã tạo,  
**Để** tôi có thể cập nhật hoặc sửa chữa các thông tin sai sót hoặc thay đổi trong quá trình quản lý gói thầu.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Chỉnh sửa" trên trang chi tiết gói thầu hoặc trong danh sách
- [ ] Form chỉnh sửa hiển thị tất cả thông tin hiện tại của gói thầu
- [ ] Người dùng có thể chỉnh sửa tất cả các trường thông tin (trừ mã gói thầu)
- [ ] Có validation cho các trường bắt buộc và format dữ liệu
- [ ] Có thể lưu nháp hoặc lưu hoàn thành
- [ ] Hiển thị lịch sử thay đổi thông tin gói thầu
- [ ] Có thể hoàn tác thay đổi trong một khoảng thời gian nhất định
- [ ] Thông báo cho các bên liên quan khi có thay đổi quan trọng

#### 2.4 Activity Diagram
![GT-2.1 Activity Diagram](diagrams/GT-2.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý chỉnh sửa thông tin gói thầu*

---

### Functional Requirements

#### Core Features
1. **Edit Interface**
   - Form chỉnh sửa với tất cả thông tin hiện tại
   - Inline editing cho một số trường
   - Bulk edit cho nhiều gói thầu
   - Preview changes trước khi lưu

2. **Data Validation**
   - Real-time validation
   - Cross-field validation
   - Business rule validation
   - Format validation

3. **Change Management**
   - Track tất cả thay đổi
   - Version history
   - Rollback functionality
   - Change approval workflow

4. **Permission Control**
   - Role-based edit permissions
   - Field-level permissions
   - Approval requirements cho thay đổi quan trọng
   - Audit trail

#### Business Rules
- Mã gói thầu không thể chỉnh sửa sau khi tạo
- Một số trường yêu cầu approval khi thay đổi
- Thay đổi quan trọng cần thông báo cho stakeholders
- Lưu lịch sử tất cả thay đổi
- Rollback được phép trong 24h sau khi thay đổi

#### Editable Fields
1. **Basic Information**
   - Tên gói thầu
   - Mô tả
   - Dự án liên quan
   - Hình thức lựa chọn nhà thầu
   - Giá trị dự kiến
   - Thời gian bắt đầu/kết thúc

2. **Detailed Information**
   - Mã TBMT
   - Số lượng nhà thầu tham gia
   - Quyết định phê duyệt HSMT
   - Quyết định phê duyệt KQLCNT
   - Giá trúng thầu
   - Nhà thầu trúng thầu

3. **Status Information**
   - Trạng thái gói thầu
   - Ghi chú
   - Tags/Labels

---

### Technical Specifications

#### Sequence Diagram
![GT-2.1 Sequence Diagram](diagrams/GT-2.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi chỉnh sửa thông tin gói thầu*

#### Database Schema Updates
```sql
-- Bảng lịch sử thay đổi gói thầu
CREATE TABLE tender_package_changes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT NOT NULL,
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
    
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Bảng cấu hình quyền chỉnh sửa
CREATE TABLE edit_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    can_edit BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_role_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (approval_role_id) REFERENCES roles(id),
    UNIQUE KEY unique_role_field (role_id, field_name)
);

-- Bảng thông báo thay đổi
CREATE TABLE change_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT NOT NULL,
    change_id INT NOT NULL,
    notification_type ENUM('email', 'sms', 'in_app') NOT NULL,
    recipient_id INT NOT NULL,
    message TEXT NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id) ON DELETE CASCADE,
    FOREIGN KEY (change_id) REFERENCES tender_package_changes(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);

-- Insert default edit permissions
INSERT INTO edit_permissions (role_id, field_name, can_edit, requires_approval) VALUES
-- System Administrator - full access
(1, 'name', TRUE, FALSE),
(1, 'description', TRUE, FALSE),
(1, 'project_id', TRUE, TRUE),
(1, 'tender_method', TRUE, TRUE),
(1, 'estimated_value', TRUE, TRUE),
(1, 'start_date', TRUE, FALSE),
(1, 'end_date', TRUE, FALSE),
(1, 'status', TRUE, TRUE),

-- Category Manager - limited access
(2, 'name', TRUE, FALSE),
(2, 'description', TRUE, FALSE),
(2, 'project_id', TRUE, TRUE),
(2, 'tender_method', TRUE, TRUE),
(2, 'estimated_value', TRUE, TRUE),
(2, 'start_date', TRUE, FALSE),
(2, 'end_date', TRUE, FALSE),
(2, 'status', FALSE, FALSE),

-- Project Manager - project-level access
(3, 'name', TRUE, FALSE),
(3, 'description', TRUE, FALSE),
(3, 'project_id', FALSE, FALSE),
(3, 'tender_method', TRUE, TRUE),
(3, 'estimated_value', TRUE, TRUE),
(3, 'start_date', TRUE, FALSE),
(3, 'end_date', TRUE, FALSE),
(3, 'status', TRUE, TRUE);
```

#### API Endpoints
```
# Tender Package Edit
GET /api/tender-packages/{id}/edit
PUT /api/tender-packages/{id}
PATCH /api/tender-packages/{id}/partial-update

# Change Management
GET /api/tender-packages/{id}/changes
POST /api/tender-packages/{id}/changes/approve
POST /api/tender-packages/{id}/changes/reject
POST /api/tender-packages/{id}/changes/rollback

# Bulk Edit
POST /api/tender-packages/bulk-update
{
  "tender_package_ids": [1, 2, 3],
  "updates": {
    "status": "in_progress",
    "description": "Updated description"
  }
}

# Change History
GET /api/tender-packages/{id}/history
GET /api/tender-packages/{id}/history/{change_id}

# Notifications
GET /api/tender-packages/{id}/notifications
POST /api/tender-packages/{id}/notifications/send
```

#### Frontend Components
```typescript
// Tender Package Edit Form
interface TenderPackageEditForm {
  // Form State
  isEditing: boolean
  isSaving: boolean
  hasChanges: boolean
  validationErrors: ValidationError[]
  
  // Data
  originalData: TenderPackage
  currentData: TenderPackage
  changes: TenderPackageChange[]
  
  // Actions
  onFieldChange: (field: string, value: any) => void
  onSave: () => Promise<void>
  onSaveDraft: () => Promise<void>
  onCancel: () => void
  onRollback: (changeId: number) => Promise<void>
}

// Change History Component
interface ChangeHistoryComponent {
  changes: TenderPackageChange[]
  canRollback: boolean
  onRollback: (changeId: number) => void
  onViewDetails: (changeId: number) => void
}

// Approval Workflow Component
interface ApprovalWorkflowComponent {
  pendingChanges: TenderPackageChange[]
  userRole: UserRole
  onApprove: (changeId: number) => Promise<void>
  onReject: (changeId: number, reason: string) => Promise<void>
}

// Bulk Edit Component
interface BulkEditComponent {
  selectedTenderPackages: TenderPackage[]
  availableFields: string[]
  onBulkUpdate: (updates: Partial<TenderPackage>) => Promise<void>
  onSelectAll: () => void
  onDeselectAll: () => void
}

// Notification Component
interface ChangeNotificationComponent {
  notifications: ChangeNotification[]
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
- Encrypt sensitive data
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