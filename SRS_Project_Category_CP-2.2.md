# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-2.2
### Xóa khoản mục chi phí

#### Thông tin User Story
- **Story ID:** CP-2.2
- **Priority:** Medium
- **Story Points:** 3
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** có thể xóa một khoản mục chi phí khỏi danh mục  
**Để** tôi có thể loại bỏ các chi phí bị trùng lặp, sai sót hoặc không còn cần thiết.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xóa" trên trang chi tiết khoản mục chi phí hoặc trong danh sách
- [ ] Có hộp thoại xác nhận trước khi xóa để tránh thao tác nhầm lẫn
- [ ] Hệ thống kiểm tra quyền xóa trước khi cho phép thao tác
- [ ] Hiển thị thông tin chi tiết về khoản mục chi phí sẽ bị xóa trong hộp thoại xác nhận
- [ ] Có thể xóa một hoặc nhiều khoản mục chi phí cùng lúc
- [ ] Hệ thống ghi log lịch sử xóa với thông tin người thực hiện và lý do
- [ ] Có thể khôi phục khoản mục chi phí đã xóa trong thời gian nhất định (soft delete)
- [ ] Hiển thị thông báo thành công sau khi xóa
- [ ] Cập nhật danh sách chi phí sau khi xóa
- [ ] Có thể xóa vĩnh viễn (hard delete) với quyền đặc biệt
- [ ] Hệ thống kiểm tra ràng buộc trước khi xóa (nếu có liên kết với dự án, hợp đồng, v.v.)

---

### Functional Requirements

#### Core Features
1. **Delete Confirmation**
   - Confirmation dialog with cost item details
   - Reason for deletion input
   - Warning about consequences
   - Cancel option

2. **Permission Management**
   - Role-based delete permissions
   - Owner-only deletion option
   - Approval requirement for sensitive items
   - Audit trail maintenance

3. **Soft Delete Implementation**
   - Mark as deleted instead of physical removal
   - Recovery period (30 days default)
   - Permanent deletion option
   - Archive functionality

4. **Bulk Delete Operations**
   - Multiple item selection
   - Batch deletion confirmation
   - Progress tracking
   - Error handling

#### Business Rules
- Chỉ người tạo hoặc người có quyền mới được xóa khoản mục chi phí
- Khoản mục chi phí đã được phê duyệt cần có quyền đặc biệt để xóa
- Khoản mục chi phí có liên kết với dự án hoặc hợp đồng cần kiểm tra ràng buộc
- Soft delete mặc định với thời gian khôi phục 30 ngày
- Hard delete chỉ dành cho quản trị viên hệ thống
- Lịch sử xóa phải được ghi lại đầy đủ với lý do

#### Delete Scenarios
1. **Single Item Delete**
   - Delete from detail view
   - Delete from list view
   - Confirmation dialog
   - Success notification

2. **Bulk Delete**
   - Multiple selection
   - Batch confirmation
   - Progress indicator
   - Error reporting

3. **Soft Delete**
   - Mark as deleted
   - Hide from normal views
   - Recovery option
   - Auto-cleanup after period

4. **Hard Delete**
   - Permanent removal
   - Admin permission required
   - Final confirmation
   - Irreversible action

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Cập nhật bảng cost_items để hỗ trợ soft delete
ALTER TABLE cost_items ADD COLUMN (
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    deleted_by INT NULL,
    delete_reason VARCHAR(500) NULL,
    can_restore BOOLEAN DEFAULT TRUE,
    restore_deadline DATE NULL,
    
    FOREIGN KEY (deleted_by) REFERENCES users(id),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_deleted_at (deleted_at),
    INDEX idx_restore_deadline (restore_deadline)
);

-- Bảng lịch sử xóa khoản mục chi phí
CREATE TABLE cost_item_deletions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    deletion_type ENUM('soft', 'hard', 'bulk') NOT NULL,
    deleted_by INT NOT NULL,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delete_reason VARCHAR(500) NULL,
    affected_items JSON NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id),
    FOREIGN KEY (deleted_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_deletion_type (deletion_type),
    INDEX idx_deleted_at (deleted_at)
);

-- Bảng khôi phục khoản mục chi phí
CREATE TABLE cost_item_restorations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    restored_by INT NOT NULL,
    restored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    restoration_reason VARCHAR(500) NULL,
    original_deletion_id INT NULL,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id),
    FOREIGN KEY (restored_by) REFERENCES users(id),
    FOREIGN KEY (original_deletion_id) REFERENCES cost_item_deletions(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_restored_at (restored_at)
);

-- Bảng cấu hình quyền xóa
CREATE TABLE cost_delete_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_role VARCHAR(50) NOT NULL,
    can_delete_own BOOLEAN DEFAULT TRUE,
    can_delete_others BOOLEAN DEFAULT FALSE,
    can_hard_delete BOOLEAN DEFAULT FALSE,
    can_bulk_delete BOOLEAN DEFAULT FALSE,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_level ENUM('manager', 'director', 'admin') NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_role (user_role),
    INDEX idx_user_role (user_role)
);

-- Bảng kiểm tra ràng buộc trước khi xóa
CREATE TABLE cost_delete_constraints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    constraint_name VARCHAR(100) NOT NULL,
    constraint_type ENUM('project_link', 'contract_link', 'payment_link', 'approval_status') NOT NULL,
    error_message VARCHAR(500) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_constraint_type (constraint_type),
    INDEX idx_is_active (is_active)
);

-- Insert default delete permissions
INSERT INTO cost_delete_permissions (user_role, can_delete_own, can_delete_others, can_hard_delete, can_bulk_delete, requires_approval) VALUES
('cost_manager', TRUE, TRUE, FALSE, TRUE, FALSE),
('cost_staff', TRUE, FALSE, FALSE, FALSE, TRUE),
('admin', TRUE, TRUE, TRUE, TRUE, FALSE);

-- Insert default delete constraints
INSERT INTO cost_delete_constraints (constraint_name, constraint_type, error_message) VALUES
('Project Link Constraint', 'project_link', 'Không thể xóa khoản mục chi phí đã liên kết với dự án'),
('Contract Link Constraint', 'contract_link', 'Không thể xóa khoản mục chi phí đã liên kết với hợp đồng'),
('Payment Link Constraint', 'payment_link', 'Không thể xóa khoản mục chi phí đã có thanh toán'),
('Approval Status Constraint', 'approval_status', 'Không thể xóa khoản mục chi phí đã được phê duyệt');
```

#### API Endpoints
```typescript
# Single Cost Item Delete
DELETE /api/cost-items/{id}
{
  "delete_reason": "Khoản mục chi phí bị trùng lặp",
  "deletion_type": "soft"
}
Response: {
  "success": true,
  "message": "Khoản mục chi phí đã được xóa thành công",
  "deleted_at": "2024-01-25T10:30:00Z",
  "restore_deadline": "2024-02-24T10:30:00Z"
}

# Bulk Cost Items Delete
DELETE /api/cost-items/bulk-delete
{
  "cost_item_ids": [123, 124, 125],
  "delete_reason": "Xóa các khoản mục chi phí không cần thiết",
  "deletion_type": "soft"
}
Response: {
  "success": true,
  "deleted_count": 3,
  "failed_count": 0,
  "failed_items": [],
  "message": "Đã xóa thành công 3 khoản mục chi phí"
}

# Hard Delete (Admin only)
DELETE /api/cost-items/{id}/permanent
{
  "delete_reason": "Xóa vĩnh viễn theo yêu cầu",
  "admin_confirmation": true
}
Response: {
  "success": true,
  "message": "Khoản mục chi phí đã được xóa vĩnh viễn"
}

# Restore Deleted Cost Item
POST /api/cost-items/{id}/restore
{
  "restoration_reason": "Khôi phục theo yêu cầu của ban quản lý"
}
Response: {
  "success": true,
  "message": "Khoản mục chi phí đã được khôi phục thành công",
  "restored_at": "2024-01-25T11:00:00Z"
}

# Get Deleted Cost Items
GET /api/cost-items/deleted
{
  "page": 1,
  "limit": 20,
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
Response: {
  "deleted_items": [
    {
      "id": 123,
      "cost_code": "CP-2024-0001",
      "cost_name": "Chi phí thiết bị văn phòng",
      "deleted_at": "2024-01-25T10:30:00Z",
      "deleted_by": 456,
      "delete_reason": "Khoản mục chi phí bị trùng lặp",
      "restore_deadline": "2024-02-24T10:30:00Z",
      "can_restore": true
    }
  ],
  "pagination": {
    "total": 15,
    "page": 1,
    "limit": 20,
    "total_pages": 1
  }
}

# Check Delete Constraints
GET /api/cost-items/{id}/delete-constraints
Response: {
  "can_delete": true,
  "constraints": [],
  "warnings": [
    "Khoản mục chi phí này đã được phê duyệt"
  ],
  "required_approval": false
}

# Delete History
GET /api/cost-items/{id}/delete-history
Response: [
  {
    "id": 1,
    "deletion_type": "soft",
    "deleted_by": 456,
    "deleted_at": "2024-01-25T10:30:00Z",
    "delete_reason": "Khoản mục chi phí bị trùng lặp",
    "ip_address": "192.168.1.100"
  }
]

# Delete Statistics
GET /api/cost-items/delete-statistics
Response: {
  "total_deleted": 25,
  "soft_deleted": 20,
  "hard_deleted": 5,
  "restored_count": 3,
  "pending_restore": 2,
  "deletion_by_reason": {
    "Trùng lặp": 10,
    "Sai sót": 8,
    "Không cần thiết": 7
  },
  "deletion_by_user": {
    "user_456": 15,
    "user_789": 10
  }
}
```

#### Frontend Components
```typescript
// Delete Confirmation Component
interface DeleteConfirmationComponent {
  costItem: CostItem
  isVisible: boolean
  deleteType: 'soft' | 'hard'
  
  onConfirm: (reason: string) => Promise<void>
  onCancel: () => void
  onClose: () => void
}

// Bulk Delete Component
interface BulkDeleteComponent {
  selectedCostItems: CostItem[]
  isVisible: boolean
  
  onConfirm: (reason: string) => Promise<void>
  onCancel: () => void
  onClearSelection: () => void
}

// Delete Progress Component
interface DeleteProgressComponent {
  totalItems: number
  processedItems: number
  failedItems: number
  isVisible: boolean
  
  onCancel: () => void
  onRetry: () => Promise<void>
}

// Restore Deleted Items Component
interface RestoreDeletedItemsComponent {
  deletedItems: DeletedCostItem[]
  filters: RestoreFilters
  
  onRestore: (itemId: number, reason: string) => Promise<void>
  onBulkRestore: (itemIds: number[], reason: string) => Promise<void>
  onFilterChange: (filters: RestoreFilters) => void
}

// Delete History Component
interface DeleteHistoryComponent {
  costItemId: number
  deleteHistory: DeleteHistory[]
  
  onViewHistory: () => void
  onExportHistory: () => void
}

// Delete Constraints Component
interface DeleteConstraintsComponent {
  costItemId: number
  constraints: DeleteConstraint[]
  
  onCheckConstraints: () => Promise<void>
  onResolveConstraint: (constraintId: number) => Promise<void>
}

// Delete Statistics Component
interface DeleteStatisticsComponent {
  statistics: DeleteStatistics
  
  onRefreshStatistics: () => Promise<void>
  onViewDetails: (category: string) => void
}

// Delete Permission Component
interface DeletePermissionComponent {
  userRole: string
  permissions: DeletePermission
  
  onPermissionChange: (permission: string, value: boolean) => void
  onSavePermissions: () => Promise<void>
}

// Delete Settings Component
interface DeleteSettingsComponent {
  settings: DeleteSettings
  
  onSettingChange: (setting: string, value: any) => void
  onSaveSettings: () => Promise<void>
}
```

---

### UI/UX Design

#### Delete Confirmation Dialog
- **Confirmation Layout:**
  - Warning icon and message
  - Cost item details display
  - Reason input field
  - Action buttons (Delete/Cancel)
  - Consequences warning

#### Bulk Delete Interface
- **Bulk Operations:**
  - Selected items list
  - Batch confirmation
  - Progress indicator
  - Error reporting

#### Restore Interface
- **Restore Management:**
  - Deleted items list
  - Filter and search
  - Restore options
  - Deadline display

#### Delete History View
- **History Display:**
  - Timeline view
  - User attribution
  - Reason display
  - Action details

---

### Integration Requirements

#### Cost Item Integration
1. **Data Consistency**
   - Constraint checking
   - Relationship validation
   - Cascade updates
   - Data integrity

2. **Permission Management**
   - Role-based access
   - Approval workflows
   - Audit logging
   - Security controls

#### Recovery Integration
1. **Restore Process**
   - Data recovery
   - Relationship restoration
   - Status updates
   - Notification system

2. **Cleanup Process**
   - Automatic cleanup
   - Data archiving
   - Storage optimization
   - Performance monitoring

---

### Security Considerations

#### Data Protection
- Delete permission validation
- Constraint enforcement
- Audit trail maintenance
- Data recovery procedures

#### Access Control
- Role-based deletion
- Approval requirements
- Session management
- Security logging

---

### Testing Strategy

#### Unit Tests
- Delete permission logic
- Constraint validation
- Soft delete functionality
- Restore process

#### Integration Tests
- Database operations
- API endpoint testing
- Bulk operations
- Recovery procedures

#### User Acceptance Tests
- Delete workflow completion
- Permission validation
- Constraint handling
- Restore functionality

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Permission configuration
- Constraint setup
- Recovery procedures

#### Monitoring & Logging
- Delete activity tracking
- Performance monitoring
- Error logging
- Security auditing

---

### Documentation

#### User Manual
- Delete procedures
- Permission guidelines
- Recovery process
- Constraint handling

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Integration guides 