# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-1.3
### Xóa Tài sản/Dịch vụ

#### Thông tin User Story
- **Story ID:** TSDV-1.3
- **Priority:** Medium
- **Story Points:** 3
- **Sprint:** Sprint 1
- **Status:** To Do
- **Dependencies:** TSDV-1.1, TSDV-1.2

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý tài sản/dịch vụ,  
**Tôi muốn** có thể xóa một khoản mục tài sản hoặc dịch vụ khỏi hệ thống  
**Để** tôi có thể loại bỏ các mục không còn sử dụng hoặc bị nhập sai.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xóa" trên trang chi tiết hoặc trong danh sách
- [ ] Hệ thống yêu cầu xác nhận trước khi xóa để tránh thao tác nhầm lẫn
- [ ] Có thể xóa một mục hoặc nhiều mục cùng lúc
- [ ] Có thể xem danh sách các mục sẽ bị ảnh hưởng trước khi xóa
- [ ] Có thể xóa mềm (soft delete) hoặc xóa cứng (hard delete)
- [ ] Có thể khôi phục mục đã xóa trong thời gian nhất định
- [ ] Có thể xem lịch sử xóa và khôi phục
- [ ] Có thể xuất báo cáo về các mục đã xóa
- [ ] Có thể thiết lập quyền xóa cho từng vai trò người dùng
- [ ] Có thể gửi thông báo khi có mục bị xóa
- [ ] Có thể xóa có điều kiện (chỉ xóa khi không có ràng buộc)
- [ ] Có thể xóa hàng loạt với bộ lọc

#### 2.4 Activity Diagram
![TSDV-1.3 Activity Diagram](diagrams/TSDV-1.3%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý xóa Tài sản/Dịch vụ*

#### 2.5 Sequence Diagram
![TSDV-1.3 Sequence Diagram](diagrams/TSDV-1.3%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi xóa Tài sản/Dịch vụ*

---

### Functional Requirements

#### Core Features
1. **Delete Operations**
   - Single item deletion
   - Bulk deletion
   - Conditional deletion
   - Soft delete/Hard delete

2. **Confirmation System**
   - Delete confirmation dialog
   - Impact analysis
   - Dependency checking
   - Risk assessment

3. **Recovery System**
   - Soft delete with recovery period
   - Restore functionality
   - Permanent deletion
   - Recovery history

4. **Permission Management**
   - Delete permissions
   - Role-based access
   - Approval workflows
   - Audit logging

#### Business Rules
- Chỉ người có quyền xóa mới có thể thực hiện thao tác xóa
- Xóa mềm được thực hiện trước, xóa cứng chỉ dành cho admin
- Thời gian khôi phục mặc định là 30 ngày
- Các mục có ràng buộc không thể xóa trực tiếp
- Thông báo phải được gửi khi có mục bị xóa
- Lịch sử xóa phải được lưu trữ đầy đủ

#### Delete Types
1. **Soft Delete**
   - Mark as deleted
   - Hide from normal view
   - Maintain data integrity
   - Allow recovery

2. **Hard Delete**
   - Permanent removal
   - Admin only
   - Irreversible action
   - Complete cleanup

3. **Conditional Delete**
   - Check dependencies
   - Validate constraints
   - Warn about impacts
   - Require approval

#### Recovery Options
1. **Automatic Recovery**
   - Recovery period
   - Auto-restore options
   - Notification system
   - Cleanup scheduling

2. **Manual Recovery**
   - User-initiated restore
   - Selective restoration
   - Data validation
   - Conflict resolution

3. **Bulk Recovery**
   - Multiple item restore
   - Batch operations
   - Progress tracking
   - Error handling

#### Permission Levels
1. **User Level**
   - Delete own items
   - Soft delete only
   - Limited permissions
   - Basic confirmation

2. **Manager Level**
   - Delete team items
   - Conditional deletion
   - Approval required
   - Impact analysis

3. **Admin Level**
   - Delete any item
   - Hard delete capability
   - No approval needed
   - Full permissions

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử xóa tài sản/dịch vụ
CREATE TABLE asset_service_deletions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    asset_service_code VARCHAR(50) NOT NULL,
    asset_service_name VARCHAR(200) NOT NULL,
    asset_service_type ENUM('asset', 'service') NOT NULL,
    deletion_type ENUM('soft', 'hard', 'conditional') NOT NULL,
    deletion_reason VARCHAR(500),
    deleted_by INT NOT NULL,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recovery_deadline DATE,
    is_recovered BOOLEAN DEFAULT FALSE,
    recovered_by INT NULL,
    recovered_at TIMESTAMP NULL,
    recovery_notes TEXT,
    
    FOREIGN KEY (deleted_by) REFERENCES users(id),
    FOREIGN KEY (recovered_by) REFERENCES users(id),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_deletion_type (deletion_type),
    INDEX idx_deleted_at (deleted_at),
    INDEX idx_is_recovered (is_recovered),
    INDEX idx_recovery_deadline (recovery_deadline)
);

-- Bảng khôi phục tài sản/dịch vụ
CREATE TABLE asset_service_recoveries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    deletion_id INT NOT NULL,
    asset_service_id INT NOT NULL,
    recovery_type ENUM('manual', 'automatic', 'bulk') NOT NULL,
    recovery_reason VARCHAR(500),
    recovered_by INT NOT NULL,
    recovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recovery_data JSON,
    validation_status ENUM('pending', 'validated', 'failed') DEFAULT 'pending',
    validation_notes TEXT,
    
    FOREIGN KEY (deletion_id) REFERENCES asset_service_deletions(id),
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id),
    FOREIGN KEY (recovered_by) REFERENCES users(id),
    INDEX idx_deletion_id (deletion_id),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_recovery_type (recovery_type),
    INDEX idx_validation_status (validation_status)
);

-- Bảng quyền xóa
CREATE TABLE asset_service_delete_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_role VARCHAR(100) NOT NULL,
    asset_service_type ENUM('asset', 'service', 'all') NOT NULL,
    can_soft_delete BOOLEAN DEFAULT FALSE,
    can_hard_delete BOOLEAN DEFAULT FALSE,
    can_bulk_delete BOOLEAN DEFAULT FALSE,
    requires_approval BOOLEAN DEFAULT TRUE,
    approval_level ENUM('none', 'manager', 'admin') DEFAULT 'manager',
    recovery_period_days INT DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_role_type (user_role, asset_service_type),
    INDEX idx_user_role (user_role),
    INDEX idx_is_active (is_active)
);

-- Bảng xác nhận xóa
CREATE TABLE asset_service_delete_confirmations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    confirmation_type ENUM('single', 'bulk', 'conditional') NOT NULL,
    confirmation_data JSON NOT NULL,
    impact_analysis JSON,
    risk_assessment ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    confirmed_by INT NOT NULL,
    confirmed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmation_notes TEXT,
    
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id),
    FOREIGN KEY (confirmed_by) REFERENCES users(id),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_confirmation_type (confirmation_type),
    INDEX idx_risk_assessment (risk_assessment)
);

-- Bảng thông báo xóa
CREATE TABLE asset_service_delete_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    deletion_id INT NOT NULL,
    notification_type ENUM('deletion_made', 'recovery_available', 'recovery_expired', 'permanent_deletion') NOT NULL,
    recipient_id INT NOT NULL,
    notification_message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (deletion_id) REFERENCES asset_service_deletions(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id),
    INDEX idx_deletion_id (deletion_id),
    INDEX idx_recipient_id (recipient_id),
    INDEX idx_is_read (is_read)
);

-- Bảng ràng buộc xóa
CREATE TABLE asset_service_delete_constraints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    constraint_type ENUM('dependency', 'reference', 'assignment', 'documentation') NOT NULL,
    constraint_description TEXT NOT NULL,
    constraint_severity ENUM('warning', 'blocking', 'critical') DEFAULT 'blocking',
    related_entity_type VARCHAR(100),
    related_entity_id INT,
    constraint_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_constraint_type (constraint_type),
    INDEX idx_constraint_severity (constraint_severity)
);

-- Insert default delete permissions
INSERT INTO asset_service_delete_permissions (user_role, asset_service_type, can_soft_delete, can_hard_delete, can_bulk_delete, requires_approval, approval_level, recovery_period_days) VALUES
('asset_manager', 'asset', true, false, true, false, 'none', 30),
('service_manager', 'service', true, false, true, false, 'none', 30),
('admin', 'all', true, true, true, false, 'none', 30),
('user', 'all', true, false, false, true, 'manager', 30);
```

#### API Endpoints
```typescript
# Delete Single Asset/Service
DELETE /api/assets-services/{id}
{
  "deletion_type": "soft",
  "deletion_reason": "Tài sản không còn sử dụng",
  "notify_users": true,
  "schedule_cleanup": true
}
Response: {
  "success": true,
  "asset_service_id": 123,
  "deletion_id": 456,
  "deletion_type": "soft",
  "recovery_deadline": "2024-02-24",
  "message": "Tài sản đã được xóa thành công"
}

# Bulk Delete Assets/Services
POST /api/assets-services/bulk-delete
{
  "asset_service_ids": [123, 124, 125],
  "deletion_type": "soft",
  "deletion_reason": "Các tài sản không còn sử dụng",
  "notify_users": true,
  "schedule_cleanup": true
}
Response: {
  "success": true,
  "deleted_count": 3,
  "failed_count": 0,
  "deletion_ids": [456, 457, 458],
  "recovery_deadline": "2024-02-24",
  "message": "3 tài sản đã được xóa thành công"
}

# Get Delete Confirmation
GET /api/assets-services/{id}/delete-confirmation
{
  "deletion_type": "soft"
}
Response: {
  "asset_service": {
    "id": 123,
    "asset_service_code": "TS2024000001",
    "name": "Máy chủ Dell PowerEdge R740",
    "type": "asset",
    "status": "active"
  },
  "impact_analysis": {
    "dependencies": [
      {
        "type": "assignment",
        "description": "Đang được gán cho Nguyễn Văn A",
        "severity": "warning"
      },
      {
        "type": "documentation",
        "description": "Có 3 tài liệu đính kèm",
        "severity": "warning"
      }
    ],
    "risk_level": "medium",
    "can_delete": true,
    "warnings": [
      "Tài sản đang được sử dụng",
      "Có tài liệu đính kèm sẽ bị xóa"
    ]
  },
  "recovery_info": {
    "recovery_period_days": 30,
    "recovery_deadline": "2024-02-24",
    "can_recover": true
  }
}

# Restore Deleted Asset/Service
POST /api/assets-services/{id}/restore
{
  "restoration_reason": "Tài sản vẫn còn cần thiết",
  "validate_data": true,
  "notify_users": true
}
Response: {
  "success": true,
  "asset_service_id": 123,
  "recovery_id": 789,
  "restored_at": "2024-01-25T15:30:00Z",
  "message": "Tài sản đã được khôi phục thành công"
}

# Get Deleted Items
GET /api/assets-services/deleted
{
  "deletion_type": "soft",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "include_recovered": false
}
Response: {
  "deleted_items": [
    {
      "id": 123,
      "asset_service_code": "TS2024000001",
      "name": "Máy chủ Dell PowerEdge R740",
      "type": "asset",
      "deletion_type": "soft",
      "deletion_reason": "Tài sản không còn sử dụng",
      "deleted_by": "Nguyễn Văn A",
      "deleted_at": "2024-01-25T10:30:00Z",
      "recovery_deadline": "2024-02-24",
      "can_recover": true,
      "days_remaining": 15
    }
  ],
  "summary": {
    "total_deleted": 5,
    "can_recover": 3,
    "expired": 2,
    "permanently_deleted": 0
  }
}

# Permanent Delete (Admin Only)
DELETE /api/assets-services/{id}/permanent
{
  "confirmation_code": "PERMANENT_DELETE_2024",
  "deletion_reason": "Xóa vĩnh viễn theo yêu cầu",
  "notify_admin": true
}
Response: {
  "success": true,
  "asset_service_id": 123,
  "permanently_deleted": true,
  "deleted_at": "2024-01-25T16:00:00Z",
  "message": "Tài sản đã được xóa vĩnh viễn"
}

# Get Delete Permissions
GET /api/assets-services/{id}/delete-permissions
{
  "user_id": 456
}
Response: {
  "user_id": 456,
  "user_role": "asset_manager",
  "permissions": {
    "can_soft_delete": true,
    "can_hard_delete": false,
    "can_bulk_delete": true,
    "requires_approval": false,
    "approval_level": "none",
    "recovery_period_days": 30
  },
  "constraints": [
    {
      "type": "assignment",
      "description": "Tài sản đang được gán",
      "severity": "warning"
    }
  ]
}

# Export Deletion Report
GET /api/assets-services/deletions/export
{
  "format": "excel",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "include_recovered": true
}
Response: File download with deletion report

# Schedule Cleanup
POST /api/assets-services/schedule-cleanup
{
  "cleanup_type": "expired_recoveries",
  "cleanup_date": "2024-02-24",
  "notify_admin": true
}
Response: {
  "success": true,
  "cleanup_scheduled": true,
  "cleanup_date": "2024-02-24",
  "estimated_items": 15,
  "message": "Lịch trình dọn dẹp đã được thiết lập"
}

# Get Bulk Delete Preview
POST /api/assets-services/bulk-delete/preview
{
  "asset_service_ids": [123, 124, 125],
  "deletion_type": "soft"
}
Response: {
  "preview": {
    "total_items": 3,
    "can_delete": 2,
    "cannot_delete": 1,
    "items": [
      {
        "id": 123,
        "name": "Máy chủ Dell PowerEdge R740",
        "can_delete": true,
        "warnings": ["Đang được gán"]
      },
      {
        "id": 124,
        "name": "Dịch vụ bảo trì ERP",
        "can_delete": false,
        "reason": "Có ràng buộc với dự án đang hoạt động"
      }
    ]
  },
  "impact_summary": {
    "total_dependencies": 5,
    "high_risk_items": 1,
    "medium_risk_items": 2,
    "low_risk_items": 0
  }
}
```

#### Frontend Components
```typescript
// Delete Confirmation Component
interface DeleteConfirmationComponent {
  assetService: AssetService
  impactAnalysis: ImpactAnalysis
  recoveryInfo: RecoveryInfo
  
  onConfirmDelete: (reason: string) => Promise<void>
  onCancelDelete: () => void
  onShowImpact: () => void
  onShowRecovery: () => void
}

// Bulk Delete Component
interface BulkDeleteComponent {
  selectedItems: AssetService[]
  deletePreview: DeletePreview
  impactSummary: ImpactSummary
  
  onPreviewDelete: () => void
  onConfirmBulkDelete: (reason: string) => Promise<void>
  onCancelBulkDelete: () => void
  onItemSelect: (items: AssetService[]) => void
}

// Deleted Items List Component
interface DeletedItemsListComponent {
  deletedItems: DeletedItem[]
  summary: DeletionSummary
  
  onItemSelect: (item: DeletedItem) => void
  onRestoreItem: (itemId: number) => Promise<void>
  onPermanentDelete: (itemId: number) => Promise<void>
  onFilterChange: (filters: DeletionFilters) => void
  onExportReport: () => void
}

// Recovery Component
interface RecoveryComponent {
  deletedItem: DeletedItem
  recoveryOptions: RecoveryOptions
  
  onRestore: (reason: string) => Promise<void>
  onValidateData: () => Promise<ValidationResult>
  onShowRecoveryHistory: () => void
  onCancelRecovery: () => void
}

// Delete Permissions Component
interface DeletePermissionsComponent {
  permissions: DeletePermissions
  constraints: DeleteConstraint[]
  
  onPermissionChange: (permissions: DeletePermissions) => void
  onConstraintView: (constraint: DeleteConstraint) => void
  onPermissionSave: () => void
}

// Delete History Component
interface DeleteHistoryComponent {
  deleteHistory: DeleteHistory[]
  
  onHistoryFilter: (filters: HistoryFilters) => void
  onHistoryExport: () => void
  onHistoryDetail: (history: DeleteHistory) => void
}

// Cleanup Scheduler Component
interface CleanupSchedulerComponent {
  scheduledCleanups: ScheduledCleanup[]
  
  onScheduleCleanup: (cleanup: CleanupConfig) => Promise<void>
  onCancelCleanup: (cleanupId: number) => Promise<void>
  onCleanupPreview: (cleanupId: number) => void
}

// Delete Notification Component
interface DeleteNotificationComponent {
  notifications: DeleteNotification[]
  
  onNotificationRead: (notificationId: number) => void
  onNotificationAction: (notification: DeleteNotification) => void
  onNotificationSettings: () => void
}

// Impact Analysis Component
interface ImpactAnalysisComponent {
  impactAnalysis: ImpactAnalysis
  
  onShowDependencies: () => void
  onShowRisks: () => void
  onShowAlternatives: () => void
  onExportAnalysis: () => void
}
```

---

### UI/UX Design

#### Delete Confirmation Interface
- **Confirmation Layout:**
  - Warning messages
  - Impact analysis
  - Recovery options
  - Action buttons

#### Bulk Delete Interface
- **Bulk Layout:**
  - Item selection
  - Preview list
  - Impact summary
  - Confirmation dialog

#### Deleted Items Interface
- **Items Layout:**
  - Deleted items list
  - Recovery options
  - Filter controls
  - Export options

#### Recovery Interface
- **Recovery Design:**
  - Recovery form
  - Data validation
  - Progress tracking
  - Success feedback

---

### Integration Requirements

#### Delete Management Integration
1. **Permission System**
   - Role-based permissions
   - Approval workflows
   - Access control
   - Audit logging

2. **Notification System**
   - Delete notifications
   - Recovery alerts
   - Cleanup reminders
   - Admin alerts

#### Recovery System Integration
1. **Data Management**
   - Data validation
   - Conflict resolution
   - Integrity checks
   - Backup restoration

2. **Cleanup Management**
   - Scheduled cleanup
   - Automatic removal
   - Storage optimization
   - Performance monitoring

---

### Security Considerations

#### Data Protection
- Delete authorization
- Permission validation
- Data backup
- Audit logging

#### Recovery Security
- Recovery validation
- Data integrity
- Access control
- Rollback protection

---

### Testing Strategy

#### Unit Tests
- Delete permission logic
- Recovery validation
- Cleanup scheduling
- Notification delivery

#### Integration Tests
- Delete workflow
- Recovery process
- Cleanup operations
- Permission validation

#### User Acceptance Tests
- Delete confirmation
- Recovery workflow
- Bulk operations
- Permission management

---

### Deployment & Configuration

#### Environment Setup
- Delete permission setup
- Recovery system configuration
- Cleanup scheduling
- Notification setup

#### Monitoring & Logging
- Delete monitoring
- Recovery tracking
- Cleanup operations
- Error logging

---

### Documentation

#### User Manual
- Delete procedures
- Recovery workflows
- Permission management
- Cleanup processes

#### Technical Documentation
- API documentation
- Delete management
- Integration guides
- Configuration guides 