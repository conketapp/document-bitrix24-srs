# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-2.2
### Xóa Hợp đồng

#### Thông tin User Story
- **Story ID:** HD-2.2
- **Priority:** Medium
- **Story Points:** 5
- **Sprint:** Sprint 2
- **Status:** To Do
- **Phụ thuộc:** HD-1.1, HD-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách hợp đồng,  
**Tôi muốn** có thể xóa một hợp đồng khỏi danh mục,  
**Để** tôi có thể loại bỏ các hợp đồng bị trùng lặp, sai sót hoặc không còn cần thiết.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xóa" trên trang chi tiết hợp đồng hoặc trong danh sách
- [ ] Có hộp thoại xác nhận trước khi xóa để tránh thao tác nhầm lẫn
- [ ] Hệ thống không xóa vĩnh viễn mà chỉ chuyển trạng thái hợp đồng sang "Đã ẩn" hoặc "Đã xóa" (ẩn khỏi danh sách thông thường)
- [ ] Kiểm tra dependencies trước khi xóa (hợp đồng có liên kết với gói thầu, thanh toán, v.v.)
- [ ] Hiển thị cảnh báo nếu hợp đồng có dependencies quan trọng
- [ ] Cho phép khôi phục hợp đồng đã xóa trong khoảng thời gian nhất định
- [ ] Ghi log tất cả hoạt động xóa hợp đồng
- [ ] Thông báo cho các bên liên quan khi hợp đồng bị xóa
- [ ] Có thể xóa nhiều hợp đồng cùng lúc (bulk delete)
- [ ] Hiển thị danh sách hợp đồng đã xóa cho admin

#### 2.4 Activity Diagram
![HD-2.2 Activity Diagram](diagrams/HD-2.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý xóa hợp đồng*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Giao diện Xóa**
   - Nút xóa trên trang chi tiết và danh sách
   - Hộp thoại xác nhận với thông tin chi tiết
   - Xóa hàng loạt với chọn nhiều
   - Triển khai xóa mềm

2. **Kiểm tra Dependencies**
   - Kiểm tra gói thầu liên kết
   - Kiểm tra lịch thanh toán
   - Kiểm tra phụ lục
   - Kiểm tra tài liệu và đính kèm

3. **Hệ thống Khôi phục**
   - Thùng rác cho hợp đồng đã xóa
   - Chức năng khôi phục
   - Xóa vĩnh viễn sau thời gian nhất định
   - Cấu hình cửa sổ khôi phục

4. **Ghi log Kiểm toán**
   - Ghi log tất cả hành động xóa
   - Theo dõi lý do xóa
   - Ghi lại người thực hiện xóa
   - Duy trì lịch sử xóa

#### Quy tắc Kinh doanh
- Chỉ quản trị viên và người quản lý hợp đồng mới có quyền xóa hợp đồng
- Hợp đồng đã ký không thể xóa (chỉ có thể lưu trữ)
- Hợp đồng có lịch thanh toán đang hoạt động không thể xóa
- Cửa sổ khôi phục: 30 ngày cho xóa mềm
- Xóa vĩnh viễn sau 90 ngày
- Thông báo cho các bên liên quan khi hợp đồng bị xóa

#### Các Kịch bản Xóa
1. **Xóa Hợp đồng Đơn lẻ**
   - Nhấn nút xóa
   - Hiển thị hộp thoại xác nhận
   - Kiểm tra dependencies
   - Thực hiện xóa mềm
   - Gửi thông báo

2. **Xóa Hàng loạt**
   - Chọn nhiều hợp đồng
   - Hiển thị hộp thoại xóa hàng loạt
   - Kiểm tra dependencies cho tất cả
   - Xác nhận xóa
   - Xử lý trong nền

3. **Xử lý Dependencies**
   - Hiển thị danh sách dependencies
   - Cho phép xóa cưỡng chế
   - Cập nhật records liên quan
   - Duy trì tính toàn vẹn tham chiếu

4. **Quy trình Khôi phục**
   - Truy cập thùng rác
   - Chọn hợp đồng để khôi phục
   - Xác nhận khôi phục
   - Cập nhật trạng thái và hiển thị

---

#### 5.5 Sequence Diagram
![HD-2.2 Sequence Diagram](diagrams/HD-2.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi xóa hợp đồng*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lưu trữ hợp đồng đã xóa (soft delete)
CREATE TABLE deleted_contracts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    original_id INT NOT NULL,
    contract_code VARCHAR(20) NOT NULL,
    contract_name VARCHAR(500) NOT NULL,
    contract_description TEXT,
    contract_type ENUM('service', 'goods', 'construction', 'consulting', 'other') NOT NULL,
    contract_value DECIMAL(15,2),
    currency VARCHAR(10) DEFAULT 'VND',
    contract_start_date DATE,
    contract_end_date DATE,
    contract_status ENUM('draft', 'active', 'completed', 'terminated', 'hidden', 'deleted') NOT NULL,
    tender_package_id INT,
    contract_manager_id INT,
    contract_supervisor_id INT,
    payment_terms TEXT,
    effective_date DATE,
    completion_date DATE,
    bitrix_task_id INT,
    bitrix_workflow_id INT,
    bitrix_status VARCHAR(100),
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_by INT NOT NULL,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delete_reason TEXT,
    can_restore BOOLEAN DEFAULT TRUE,
    restore_deadline TIMESTAMP,
    permanent_delete_date TIMESTAMP,
    
    FOREIGN KEY (deleted_by) REFERENCES users(id),
    INDEX idx_original_id (original_id),
    INDEX idx_deleted_at (deleted_at),
    INDEX idx_restore_deadline (restore_deadline)
);

-- Bảng lịch sử xóa hợp đồng
CREATE TABLE contract_delete_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    action_type ENUM('soft_delete', 'permanent_delete', 'restore') NOT NULL,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delete_reason TEXT,
    dependencies_checked JSON,
    force_delete BOOLEAN DEFAULT FALSE,
    notification_sent BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id)
);

-- Bảng dependencies của hợp đồng
CREATE TABLE contract_dependencies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    dependency_type ENUM('tender_package', 'payment_schedule', 'amendment', 'document', 'notification', 'approval') NOT NULL,
    dependency_id INT NOT NULL,
    dependency_name VARCHAR(200) NOT NULL,
    is_critical BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    UNIQUE KEY unique_contract_dependency (contract_id, dependency_type, dependency_id)
);

-- Bảng cấu hình xóa hợp đồng
CREATE TABLE contract_delete_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    can_delete BOOLEAN DEFAULT FALSE,
    can_bulk_delete BOOLEAN DEFAULT FALSE,
    can_force_delete BOOLEAN DEFAULT FALSE,
    can_permanent_delete BOOLEAN DEFAULT FALSE,
    can_restore BOOLEAN DEFAULT FALSE,
    recovery_window_days INT DEFAULT 30,
    permanent_delete_days INT DEFAULT 90,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_role_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (approval_role_id) REFERENCES roles(id)
);

-- Bảng thông báo xóa hợp đồng
CREATE TABLE contract_delete_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    delete_history_id INT NOT NULL,
    notification_type ENUM('email', 'sms', 'in_app') NOT NULL,
    recipient_id INT NOT NULL,
    message TEXT NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (delete_history_id) REFERENCES contract_delete_history(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id)
);

-- Insert default delete permissions
INSERT INTO contract_delete_config (role_id, can_delete, can_bulk_delete, can_force_delete, can_permanent_delete, can_restore, requires_approval) VALUES
-- Contract Manager - full delete permissions
(1, TRUE, TRUE, TRUE, FALSE, TRUE, FALSE),
-- Contract Supervisor - limited delete permissions
(2, TRUE, TRUE, FALSE, FALSE, TRUE, TRUE),
-- Contract Officer - no delete permissions
(3, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE),
-- Admin - full permissions including permanent delete
(4, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE);
```

#### API Endpoints
```
# Contract Delete
DELETE /api/contracts/{id}
POST /api/contracts/{id}/delete
{
  "reason": "Duplicate contract",
  "force_delete": false,
  "notify_stakeholders": true
}

# Bulk Delete
POST /api/contracts/bulk-delete
{
  "contract_ids": [1, 2, 3],
  "reason": "Bulk cleanup",
  "force_delete": false,
  "notify_stakeholders": true
}

# Check Dependencies
GET /api/contracts/{id}/dependencies
Response: {
  "dependencies": [
    {
      "type": "tender_package",
      "id": 123,
      "name": "GT-2024-001",
      "is_critical": true
    }
  ],
  "can_delete": false,
  "force_delete_required": true
}

# Restore Contract
POST /api/contracts/{id}/restore
{
  "restore_reason": "Contract was deleted by mistake"
}

# Recycle Bin
GET /api/contracts/deleted
GET /api/contracts/deleted/{id}
POST /api/contracts/deleted/{id}/restore
DELETE /api/contracts/deleted/{id}/permanent

# Delete History
GET /api/contracts/{id}/delete-history
GET /api/contracts/delete-history

# Delete Configuration
GET /api/contracts/delete-config
PUT /api/contracts/delete-config
{
  "recovery_window_days": 30,
  "permanent_delete_days": 90
}
```

#### Frontend Components
```typescript
// Contract Delete Dialog
interface ContractDeleteDialog {
  contract: Contract
  isOpen: boolean
  isLoading: boolean
  dependencies: ContractDependency[]
  canDelete: boolean
  forceDeleteRequired: boolean
  
  onConfirm: (reason: string, forceDelete: boolean) => Promise<void>
  onCancel: () => void
  onCheckDependencies: () => Promise<void>
}

// Bulk Delete Dialog
interface BulkDeleteDialog {
  selectedContracts: Contract[]
  isOpen: boolean
  isLoading: boolean
  dependencies: ContractDependency[]
  canDeleteAll: boolean
  
  onConfirm: (reason: string, forceDelete: boolean) => Promise<void>
  onCancel: () => void
  onSelectAll: () => void
  onDeselectAll: () => void
}

// Recycle Bin Component
interface RecycleBinComponent {
  deletedContracts: DeletedContract[]
  isLoading: boolean
  filters: RecycleBinFilters
  
  onRestore: (contractId: number) => Promise<void>
  onPermanentDelete: (contractId: number) => Promise<void>
  onBulkRestore: (contractIds: number[]) => Promise<void>
  onBulkPermanentDelete: (contractIds: number[]) => Promise<void>
  onFilterChange: (filters: RecycleBinFilters) => void
}

// Delete History Component
interface DeleteHistoryComponent {
  deleteHistory: ContractDeleteHistory[]
  isLoading: boolean
  
  onViewDetails: (historyId: number) => void
  onExportHistory: () => void
}

// Dependency Check Component
interface DependencyCheckComponent {
  dependencies: ContractDependency[]
  isChecking: boolean
  
  onForceDelete: () => void
  onCancel: () => void
}

// Delete Notification Component
interface DeleteNotificationComponent {
  notifications: ContractDeleteNotification[]
  onMarkAsRead: (notificationId: number) => void
  onSendNotification: (recipients: number[], message: string) => Promise<void>
}

// Contract Status Badge
interface ContractStatusBadge {
  status: ContractStatus
  isDeleted: boolean
  deletedAt?: Date
  canRestore: boolean
  onRestore?: () => void
}
```

---

### UI/UX Design

#### Delete Interface
- **Delete Button:**
  - Red delete button với icon
  - Disabled state cho contracts không thể xóa
  - Tooltip với lý do không thể xóa

#### Confirmation Dialog
- **Dialog Layout:**
  - Contract information summary
  - Dependencies warning
  - Reason input field
  - Force delete checkbox
  - Confirm/Cancel buttons

#### Recycle Bin Interface
- **Recycle Bin View:**
  - List of deleted contracts
  - Filter options (date, type, deleted by)
  - Bulk actions
  - Restore/Permanent delete buttons

#### Delete History
- **History Timeline:**
  - Chronological list of delete actions
  - User who performed action
  - Reason for deletion
  - Dependencies checked

---

### Integration Requirements

#### Contract Management Integration
1. **Status Updates**
   - Update contract status to "deleted"
   - Hide from normal list views
   - Maintain in database for recovery

2. **Dependency Management**
   - Check all related records
   - Update or remove references
   - Maintain data integrity

#### Notification System
1. **Delete Notifications**
   - Notify contract manager
   - Notify stakeholders
   - Notify linked tender packages
   - Email and in-app notifications

2. **Recovery Notifications**
   - Notify when contract is restored
   - Update all related systems
   - Re-establish connections

---

### Security Considerations

#### Access Control
- Role-based delete permissions
- Approval requirements for critical contracts
- Audit logging for all delete actions
- Recovery window limitations

#### Data Protection
- Soft delete implementation
- Encrypted storage for deleted data
- Secure recovery process
- Permanent delete after time limit

#### Validation
- Dependency validation before delete
- Force delete confirmation
- Recovery deadline enforcement
- Data integrity checks

---

### Testing Strategy

#### Unit Tests
- Delete permission validation
- Dependency checking logic
- Recovery process testing
- Notification system

#### Integration Tests
- End-to-end delete workflow
- Bulk delete functionality
- Recovery process testing
- Dependency management

#### User Acceptance Tests
- Delete interface usability
- Confirmation dialog testing
- Recycle bin functionality
- Recovery process testing

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Delete permission configuration
- Recovery window settings
- Notification setup

#### Monitoring & Logging
- Delete activity monitoring
- Recovery process tracking
- Performance monitoring
- Error tracking

---

### Documentation

#### User Manual
- Delete interface guide
- Recovery process instructions
- Bulk delete procedures
- Recycle bin management

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Recovery procedures 