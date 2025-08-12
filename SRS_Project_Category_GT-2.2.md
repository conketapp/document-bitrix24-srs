# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-2.2
### Xóa Gói thầu

#### Thông tin User Story
- **Story ID:** GT-2.2
- **Priority:** Medium
- **Story Points:** 5
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** GT-1.1, GT-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể xóa một gói thầu khỏi danh mục,  
**Để** tôi có thể loại bỏ các gói thầu bị trùng lặp, sai sót hoặc không còn cần thiết.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xóa" trên trang chi tiết gói thầu hoặc trong danh sách
- [ ] Có hộp thoại xác nhận trước khi xóa để tránh thao tác nhầm lẫn
- [ ] Hệ thống có thể yêu cầu quyền đặc biệt để xóa gói thầu, hoặc không cho phép xóa nếu gói thầu đã liên kết với Hợp đồng
- [ ] Hiển thị thông tin chi tiết về gói thầu sẽ bị xóa trong hộp thoại xác nhận
- [ ] Có thể xóa một hoặc nhiều gói thầu cùng lúc (bulk delete)
- [ ] Hiển thị cảnh báo nếu gói thầu có dữ liệu liên quan
- [ ] Có thể khôi phục gói thầu đã xóa trong một khoảng thời gian nhất định
- [ ] Ghi log lịch sử xóa gói thầu để audit trail

#### 2.4 Activity Diagram
![GT-2.2 Activity Diagram](diagrams/GT-2.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý xóa gói thầu*

---

### Functional Requirements

#### Core Features
1. **Delete Interface**
   - Delete button trên detail page và list view
   - Bulk delete cho multiple selection
   - Confirmation dialog với thông tin chi tiết
   - Warning messages cho dependencies

2. **Permission Control**
   - Role-based delete permissions
   - Special permission requirements
   - Dependency validation
   - Approval workflow cho delete operations

3. **Dependency Management**
   - Check for related contracts
   - Check for related documents
   - Check for active workflows
   - Prevent deletion if dependencies exist

4. **Recovery System**
   - Soft delete implementation
   - Recovery window (30 days)
   - Restore functionality
   - Permanent deletion after recovery period

#### Business Rules
- Chỉ users có quyền DELETE_TENDER_PACKAGE mới có thể xóa
- Không thể xóa gói thầu đã có hợp đồng liên kết
- Không thể xóa gói thầu đang trong quá trình triển khai
- Soft delete trong 30 ngày trước khi permanent delete
- Log tất cả delete operations cho audit trail

#### Delete Restrictions
1. **Status-based Restrictions**
   - Không thể xóa gói thầu có status "in_progress"
   - Không thể xóa gói thầu có status "completed"
   - Chỉ có thể xóa gói thầu có status "draft" hoặc "cancelled"

2. **Dependency-based Restrictions**
   - Gói thầu có hợp đồng liên kết
   - Gói thầu có documents attached
   - Gói thầu có active workflows
   - Gói thầu có audit records

3. **Permission-based Restrictions**
   - User role không có delete permission
   - Gói thầu thuộc project mà user không có quyền
   - Gói thầu được tạo bởi user khác (trừ admin)

---

### Technical Specifications

#### Sequence Diagram
![GT-2.2 Sequence Diagram](diagrams/GT-2.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi xóa gói thầu*

#### Database Schema Updates
```sql
-- Bảng lưu trữ gói thầu đã xóa (soft delete)
CREATE TABLE deleted_tender_packages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    original_id INT NOT NULL,
    tender_code VARCHAR(20) NOT NULL,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    project_id INT,
    tender_method ENUM('open_tender', 'limited_tender', 'direct_appointment', 'competitive_consultation', 'other'),
    estimated_value DECIMAL(15,2),
    currency VARCHAR(10),
    start_date DATE,
    end_date DATE,
    status ENUM('draft', 'created', 'in_progress', 'completed', 'cancelled'),
    
    -- Thông tin xóa
    deleted_by INT NOT NULL,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delete_reason TEXT,
    can_restore BOOLEAN DEFAULT TRUE,
    permanent_delete_at TIMESTAMP,
    
    -- Backup data
    original_data JSON,
    
    FOREIGN KEY (deleted_by) REFERENCES users(id)
);

-- Bảng lịch sử xóa gói thầu
CREATE TABLE tender_package_deletion_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT NOT NULL,
    action_type ENUM('delete', 'restore', 'permanent_delete') NOT NULL,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    dependencies_checked JSON,
    warnings_shown JSON,
    
    FOREIGN KEY (performed_by) REFERENCES users(id)
);

-- Bảng cấu hình quyền xóa
CREATE TABLE delete_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    resource_type ENUM('tender_package', 'project', 'contract') NOT NULL,
    can_delete BOOLEAN DEFAULT FALSE,
    requires_approval BOOLEAN DEFAULT TRUE,
    approval_role_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (approval_role_id) REFERENCES roles(id)
);

-- Insert default delete permissions
INSERT INTO delete_permissions (role_id, resource_type, can_delete, requires_approval) VALUES
-- System Administrator - full delete access
(1, 'tender_package', TRUE, FALSE),
(1, 'project', TRUE, FALSE),
(1, 'contract', TRUE, FALSE),

-- Category Manager - limited delete access
(2, 'tender_package', TRUE, TRUE),
(2, 'project', FALSE, FALSE),
(2, 'contract', FALSE, FALSE),

-- Project Manager - project-level delete access
(3, 'tender_package', TRUE, TRUE),
(3, 'project', FALSE, FALSE),
(3, 'contract', FALSE, FALSE);
```

#### API Endpoints
```
# Tender Package Delete
DELETE /api/tender-packages/{id}
POST /api/tender-packages/{id}/delete
{
  "reason": "Duplicate tender package",
  "force_delete": false
}

# Bulk Delete
POST /api/tender-packages/bulk-delete
{
  "tender_package_ids": [1, 2, 3],
  "reason": "Bulk cleanup",
  "force_delete": false
}

# Delete Validation
GET /api/tender-packages/{id}/delete-validation
{
  "can_delete": true,
  "dependencies": [
    {
      "type": "contract",
      "count": 2,
      "details": "Active contracts found"
    }
  ],
  "warnings": [
    "This tender package has active workflows"
  ]
}

# Recovery
POST /api/tender-packages/{id}/restore
GET /api/tender-packages/deleted
DELETE /api/tender-packages/{id}/permanent-delete

# Delete Logs
GET /api/tender-packages/{id}/delete-logs
GET /api/tender-packages/delete-logs/summary
```

#### Frontend Components
```typescript
// Delete Confirmation Dialog
interface DeleteConfirmationDialog {
  tenderPackage: TenderPackage
  isVisible: boolean
  isDeleting: boolean
  validationResult: DeleteValidationResult
  onConfirm: (reason: string, forceDelete: boolean) => Promise<void>
  onCancel: () => void
  onClose: () => void
}

// Delete Validation Result
interface DeleteValidationResult {
  canDelete: boolean
  dependencies: Dependency[]
  warnings: string[]
  errors: string[]
  requiresApproval: boolean
}

// Dependency Information
interface Dependency {
  type: 'contract' | 'document' | 'workflow' | 'audit'
  count: number
  details: string
  severity: 'warning' | 'error' | 'info'
}

// Bulk Delete Component
interface BulkDeleteComponent {
  selectedTenderPackages: TenderPackage[]
  validationResults: DeleteValidationResult[]
  onBulkDelete: (reason: string, forceDelete: boolean) => Promise<void>
  onSelectAll: () => void
  onDeselectAll: () => void
}

// Recovery Component
interface RecoveryComponent {
  deletedTenderPackages: DeletedTenderPackage[]
  onRestore: (tenderPackageId: number) => Promise<void>
  onPermanentDelete: (tenderPackageId: number) => Promise<void>
  onViewDetails: (tenderPackageId: number) => void
}

// Delete Log Component
interface DeleteLogComponent {
  logs: TenderPackageDeletionLog[]
  onViewLog: (logId: number) => void
  onExportLogs: () => void
}
```

---

### UI/UX Design

#### Delete Confirmation Dialog
- **Layout:** Modal dialog với warning styling
- **Components:**
  - Warning icon và message
  - Tender package details
  - Dependencies list
  - Reason input field
  - Force delete checkbox
  - Confirm/Cancel buttons

#### Bulk Delete Interface
- **Layout:** Modal với table view
- **Components:**
  - Selected items count
  - Validation summary
  - Individual item warnings
  - Bulk action buttons
  - Progress indicator

#### Recovery Interface
- **Layout:** Dedicated page với table
- **Components:**
  - Deleted items table
  - Restore buttons
  - Permanent delete buttons
  - Filter và search
  - Export functionality

#### Warning Messages
- **Dependency Warnings:**
  - Contract dependencies
  - Document dependencies
  - Workflow dependencies
  - Audit trail warnings

---

### Integration Requirements

#### Permission System Integration
1. **Role-based Access Control**
   - Check user permissions
   - Validate delete rights
   - Handle approval workflows
   - Log permission checks

2. **Dependency Validation**
   - Check related contracts
   - Check attached documents
   - Check active workflows
   - Check audit requirements

#### Notification System
1. **Delete Notifications**
   - Notify stakeholders
   - Notify project managers
   - Notify contract owners
   - Escalation notifications

2. **Recovery Notifications**
   - Notify when items are restored
   - Notify before permanent deletion
   - Notify about recovery window expiry

---

### Security Considerations

#### Access Control
- Role-based delete permissions
- Special permission requirements
- Approval workflow integration
- Audit trail maintenance

#### Data Protection
- Soft delete implementation
- Secure data recovery
- Permanent deletion safeguards
- Backup before deletion

#### Validation Security
- Validate all dependencies
- Prevent unauthorized deletions
- Check business rules
- Maintain data integrity

---

### Testing Strategy

#### Unit Tests
- Delete permission validation
- Dependency checking logic
- Recovery functionality
- Logging mechanisms

#### Integration Tests
- End-to-end delete workflow
- Bulk delete functionality
- Recovery process testing
- Notification system

#### User Acceptance Tests
- Delete confirmation workflow
- Bulk delete experience
- Recovery interface testing
- Warning message clarity

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Permission configuration
- Recovery window settings
- Notification setup

#### Monitoring & Logging
- Delete activity monitoring
- Recovery tracking
- Performance monitoring
- Error tracking

---

### Documentation

#### User Manual
- Delete operation guide
- Recovery procedures
- Warning message explanations
- Best practices

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Performance optimization

---

### Validation Table

#### **Bảng Validation Form Xóa**

##### **Thông tin Xác nhận Xóa**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Mã gói thầu | tender_code | VARCHAR(20) | GT-YYYY-XXXX | ✅ | Mã gói thầu cần xóa |
| Lý do xóa | delete_reason | TEXT | 10-500 ký tự | ✅ | Lý do xóa gói thầu |
| Xác nhận xóa | confirm_delete | BOOLEAN | true/false | ✅ | Checkbox xác nhận |
| Người xóa | deleted_by | INT | User ID | ✅ | Người thực hiện xóa |

##### **Thông tin Kiểm tra Dependencies**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Số hợp đồng liên quan | related_contracts | INT | >= 0 | ✅ | Số hợp đồng đã tạo |
| Số chi phí liên quan | related_costs | INT | >= 0 | ✅ | Số chi phí đã tạo |
| Số tài liệu đính kèm | related_documents | INT | >= 0 | ✅ | Số tài liệu đính kèm |
| Trạng thái gói thầu | tender_status | ENUM | 'draft', 'created', 'in_progress', 'completed', 'cancelled' | ✅ | Trạng thái hiện tại |

#### **Quy tắc Validation Xóa**

##### **Validation Permission và Status**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Delete permission | User có quyền | Role-based access | "Bạn không có quyền xóa gói thầu" |
| Status validation | Trạng thái cho phép | Chỉ 'draft' hoặc 'created' | "Chỉ có thể xóa gói thầu ở trạng thái nháp hoặc đã tạo" |
| Dependencies check | Không có dependencies | related_contracts = 0 | "Không thể xóa gói thầu đã có hợp đồng liên quan" |

##### **Validation Business Rules**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Reason required | Lý do xóa | Ít nhất 10 ký tự | "Vui lòng nhập lý do xóa (ít nhất 10 ký tự)" |
| Confirmation | Xác nhận xóa | confirm_delete = true | "Vui lòng xác nhận việc xóa gói thầu" |
| Soft delete | Xóa mềm | Chỉ đánh dấu deleted | "Gói thầu sẽ được đánh dấu xóa thay vì xóa hoàn toàn" | 