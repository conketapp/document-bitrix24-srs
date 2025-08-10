# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### 1. Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Date:** 07-2025  
**Author:** Công ty Thiên Phú Digital  

### 2. Mô tả Epic
Epic này tập trung vào việc phát triển hệ thống quản lý danh mục dự án, cho phép cán bộ quản lý dự án tổ chức và quản lý các dự án theo năm và phân loại một cách hiệu quả.

---

## User Story: DMDA-3.2
### Gửi Phê duyệt Nhiều Dự án Cùng lúc (Multiselect)

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-3.2
- **Priority:** Medium
- **Story Points:** 10
- **Sprint:** Sprint 3
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-3.1 (Cần có danh sách dự án và gửi phê duyệt đơn lẻ)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** có thể chọn nhiều dự án trong danh mục (sử dụng tính năng multiselect) và gửi chúng đi phê duyệt cùng một lúc,  
**Để** tôi có thể tiết kiệm thời gian và tối ưu hóa quy trình khi cần phê duyệt hàng loạt dự án.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Chức năng multiselect (checkbox) hiển thị bên cạnh mỗi dự án trong danh sách
- [ ] Có nút "Gửi Phê duyệt (đã chọn)" hoặc tương tự sau khi chọn nhiều dự án
- [ ] Hệ thống xử lý việc gửi phê duyệt cho từng dự án đã chọn
- [ ] Chỉ hiển thị checkbox cho dự án có thể gửi phê duyệt (initialized, edit_requested)
- [ ] Có hộp thoại xác nhận trước khi gửi phê duyệt hàng loạt
- [ ] Hiển thị danh sách dự án đã chọn trong hộp thoại xác nhận
- [ ] Ghi log hành động gửi phê duyệt hàng loạt
- [ ] Thông báo kết quả sau khi hoàn thành (thành công/thất bại)

#### 2.4 Activity Diagram
![DMDA-3.2 Activity Diagram](diagrams/DMDA-3.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý gửi phê duyệt nhiều dự án cùng lúc*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Multiselect Functionality**
   - Checkbox hiển thị cho mỗi dự án trong danh sách
   - Chỉ hiển thị checkbox cho dự án có thể gửi phê duyệt
   - Select all/none functionality
   - Counter hiển thị số dự án đã chọn

2. **Bulk Approval Submission**
   - Nút "Gửi Phê duyệt (X dự án)" sau khi chọn
   - Form chọn người phê duyệt cho tất cả dự án
   - Validation trước khi gửi hàng loạt
   - Confirmation dialog với danh sách dự án

3. **Batch Processing**
   - Xử lý từng dự án đã chọn
   - Progress indicator cho quá trình xử lý
   - Error handling cho từng dự án
   - Summary report sau khi hoàn thành

#### 3.2 Business Rules
- Chỉ dự án có trạng thái "initialized" hoặc "edit_requested" mới có thể được chọn
- Tối đa 50 dự án có thể được gửi phê duyệt cùng lúc
- Người phê duyệt được chọn sẽ áp dụng cho tất cả dự án
- Mỗi dự án sẽ được xử lý riêng lẻ, không ảnh hưởng đến nhau

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian load checkbox < 500ms
- Thời gian xử lý mỗi dự án < 2 giây
- Progress indicator update mỗi 1 giây
- Không ảnh hưởng đến performance của danh sách

#### 4.2 Usability
- UI responsive và dễ sử dụng
- Clear visual feedback cho selection state
- Intuitive bulk action workflow
- Comprehensive error reporting

#### 4.3 Security
- Xác thực người dùng trước khi bulk action
- Phân quyền theo vai trò
- Audit trail cho mọi bulk action
- CSRF protection

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Bảng lưu lịch sử bulk approval
CREATE TABLE bulk_approval_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_id VARCHAR(36) NOT NULL, -- UUID cho batch
    submitted_by INT NOT NULL,
    approver_id INT NOT NULL,
    total_projects INT NOT NULL,
    successful_count INT DEFAULT 0,
    failed_count INT DEFAULT 0,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date TIMESTAMP NULL,
    status ENUM('processing', 'completed', 'failed') DEFAULT 'processing',
    FOREIGN KEY (submitted_by) REFERENCES users(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

-- Bảng chi tiết bulk approval
CREATE TABLE bulk_approval_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_id VARCHAR(36) NOT NULL,
    project_id INT NOT NULL,
    status ENUM('pending', 'success', 'failed') DEFAULT 'pending',
    error_message TEXT,
    processed_at TIMESTAMP NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    INDEX idx_batch_id (batch_id),
    INDEX idx_project_id (project_id)
);

-- Thêm index cho performance
CREATE INDEX idx_bulk_approval_batch ON bulk_approval_logs(batch_id);
CREATE INDEX idx_bulk_approval_user ON bulk_approval_logs(submitted_by);
CREATE INDEX idx_bulk_details_batch ON bulk_approval_details(batch_id);
```

#### 5.2 API Endpoints
```
POST /api/projects/bulk-submit-approval
- Request: { 
    project_ids: number[], 
    approver_id: number, 
    comment?: string 
}
- Response: { 
    batch_id: string, 
    total_projects: number, 
    message: string 
}

GET /api/projects/bulk-approval-status/{batch_id}
- Response: { 
    status: string, 
    progress: number, 
    successful_count: number, 
    failed_count: number, 
    details: array 
}

GET /api/projects/can-bulk-submit
- Response: { 
    canSubmit: boolean, 
    available_projects: number, 
    reason?: string 
}

GET /api/projects/bulk-approval-history
- Response: List of bulk approval batches
```

#### 5.3 Data Models
```typescript
interface BulkApprovalRequest {
    project_ids: number[];
    approver_id: number;
    comment?: string;
}

interface BulkApprovalResponse {
    batch_id: string;
    total_projects: number;
    message: string;
    status: 'processing' | 'completed' | 'failed';
}

interface BulkApprovalLog {
    id: number;
    batch_id: string;
    submitted_by: number;
    approver_id: number;
    total_projects: number;
    successful_count: number;
    failed_count: number;
    submission_date: string;
    completion_date?: string;
    status: 'processing' | 'completed' | 'failed';
}

interface BulkApprovalDetail {
    id: number;
    batch_id: string;
    project_id: number;
    status: 'pending' | 'success' | 'failed';
    error_message?: string;
    processed_at?: string;
}

interface BulkApprovalStatus {
    status: string;
    progress: number;
    successful_count: number;
    failed_count: number;
    details: BulkApprovalDetail[];
}

interface ProjectSelection {
    id: number;
    project_code: string;
    name: string;
    status: string;
    can_submit: boolean;
    selected: boolean;
}
```

#### 5.4 UI Components
- ProjectCheckbox: Checkbox cho mỗi dự án
- SelectAllCheckbox: Checkbox chọn tất cả
- BulkActionButton: Nút hành động hàng loạt
- BulkApprovalModal: Modal gửi phê duyệt hàng loạt
- ProgressIndicator: Hiển thị tiến độ xử lý
- BulkApprovalSummary: Tóm tắt kết quả xử lý
- BulkApprovalHistory: Lịch sử gửi phê duyệt hàng loạt

#### 5.5 Sequence Diagram
![DMDA-3.2 Sequence Diagram](diagrams/DMDA-3.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi gửi phê duyệt nhiều dự án cùng lúc*

---

### 6. Integration Requirements

#### 6.1 Bitrix24 Integration
- Batch update deal status thành "PENDING_APPROVAL"
- Create tasks cho người phê duyệt cho từng dự án
- Sync bulk approval workflow với Bitrix24
- Log bulk action trong Bitrix24 activity feed

#### 6.2 Notification System
- Email notification cho người phê duyệt về batch
- In-app notification cho project manager
- Progress notifications cho bulk processing
- Summary notification sau khi hoàn thành

#### 6.3 Data Flow
1. User select multiple projects via checkboxes
2. User click "Gửi Phê duyệt (X dự án)" button
3. System validate selected projects
4. Show bulk approval form với approver selection
5. User confirm và submit
6. System create batch record và process each project
7. Update progress indicator
8. Sync với Bitrix24 cho từng dự án
9. Send notifications
10. Log bulk action và show summary

---

### 7. User Interface Requirements

#### 7.1 Project List with Checkboxes
```
┌─────────────────────────────────────────────────────────┐
│ [✓] Chọn tất cả    [Gửi Phê duyệt (3 dự án)]        │
├─────────────────────────────────────────────────────────┤
│ [✓] INV-2024-001 | Dự án A | Draft                   │
│ [ ] INV-2024-002 | Dự án B | Approved (disabled)     │
│ [✓] INV-2024-003 | Dự án C | Draft                   │
│ [✓] INV-2024-004 | Dự án D | Edit Requested          │
│ [ ] INV-2024-005 | Dự án E | Completed (disabled)    │
└─────────────────────────────────────────────────────────┘
```

#### 7.2 Bulk Approval Modal
```
┌─────────────────────────────────────┐
│ Gửi Phê duyệt Hàng loạt            │
├─────────────────────────────────────┤
│ Đã chọn 3 dự án:                   │
│ • INV-2024-001 - Dự án A           │
│ • INV-2024-003 - Dự án C           │
│ • INV-2024-004 - Dự án D           │
│                                     │
│ Người phê duyệt *                  │
│ [Dropdown với danh sách approvers] │
│                                     │
│ Ghi chú (tùy chọn)                 │
│ [Textarea]                         │
│                                     │
│ ⚠️ Lưu ý: Tất cả dự án sẽ chuyển   │
│    sang trạng thái "Chờ phê duyệt" │
│                                     │
│ [Hủy] [Gửi Phê duyệt (3 dự án)]   │
└─────────────────────────────────────┘
```

#### 7.3 Progress Indicator
```
┌─────────────────────────────────────┐
│ Đang xử lý...                      │
├─────────────────────────────────────┤
│ ████████████████████░░ 80%         │
│                                     │
│ Đã xử lý: 2/3 dự án               │
│ Thành công: 2 | Thất bại: 0        │
│                                     │
│ Đang xử lý: INV-2024-004           │
└─────────────────────────────────────┘
```

#### 7.4 Success/Error Messages
- **Success**: "Đã gửi phê duyệt thành công 3/3 dự án"
- **Partial Success**: "Đã gửi phê duyệt thành công 2/3 dự án. 1 dự án thất bại"
- **Error - No Selection**: "Vui lòng chọn ít nhất một dự án"
- **Error - Invalid Projects**: "Một số dự án không thể gửi phê duyệt"
- **Error - System Error**: "Có lỗi xảy ra, vui lòng thử lại"

---

### 8. Testing Requirements

#### 8.1 Unit Tests
```typescript
describe('Bulk Project Approval', () => {
    test('should allow selection of draft projects', () => {
        const projects = [
            { id: 1, status: 'draft', can_submit: true },
            { id: 2, status: 'approved', can_submit: false }
        ];
        const selectedIds = getSelectableProjectIds(projects);
        expect(selectedIds).toEqual([1]);
    });

    test('should validate bulk submission', async () => {
        const request = {
            project_ids: [1, 2, 3],
            approver_id: 1
        };
        const result = await validateBulkSubmission(request);
        expect(result.isValid).toBe(true);
    });

    test('should process bulk approval', async () => {
        const batchId = 'batch-123';
        const projectIds = [1, 2, 3];
        const approverId = 1;
        
        await processBulkApproval(batchId, projectIds, approverId);
        
        const batch = await getBulkApprovalLog(batchId);
        expect(batch.status).toBe('completed');
        expect(batch.successful_count).toBe(3);
    });

    test('should handle partial failures', async () => {
        const batchId = 'batch-123';
        const projectIds = [1, 2, 3]; // Project 2 will fail
        
        await processBulkApproval(batchId, projectIds, 1);
        
        const batch = await getBulkApprovalLog(batchId);
        expect(batch.successful_count).toBe(2);
        expect(batch.failed_count).toBe(1);
    });
});
```

#### 8.2 Integration Tests
- Test Bitrix24 sync cho bulk operations
- Test notification system cho batch processing
- Test permission system cho bulk actions
- Test error handling cho partial failures

#### 8.3 User Acceptance Tests
- Test multiselect functionality
- Test bulk approval workflow
- Test progress indicator
- Test error handling
- Test summary reporting

---

### 9. Deployment Requirements

#### 9.1 Database Migration
```sql
-- Migration script
BEGIN;
-- Create bulk approval tables
CREATE TABLE bulk_approval_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_id VARCHAR(36) NOT NULL,
    submitted_by INT NOT NULL,
    approver_id INT NOT NULL,
    total_projects INT NOT NULL,
    successful_count INT DEFAULT 0,
    failed_count INT DEFAULT 0,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date TIMESTAMP NULL,
    status ENUM('processing', 'completed', 'failed') DEFAULT 'processing',
    FOREIGN KEY (submitted_by) REFERENCES users(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

CREATE TABLE bulk_approval_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_id VARCHAR(36) NOT NULL,
    project_id INT NOT NULL,
    status ENUM('pending', 'success', 'failed') DEFAULT 'pending',
    error_message TEXT,
    processed_at TIMESTAMP NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Add indexes
CREATE INDEX idx_bulk_approval_batch ON bulk_approval_logs(batch_id);
CREATE INDEX idx_bulk_approval_user ON bulk_approval_logs(submitted_by);
CREATE INDEX idx_bulk_details_batch ON bulk_approval_details(batch_id);

COMMIT;
```

#### 9.2 Environment Configuration
- Bulk processing settings
- Notification settings
- Permission settings
- Bitrix24 integration settings

---

### 10. Success Criteria
- [ ] User có thể chọn nhiều dự án bằng checkbox
- [ ] Bulk approval form hiển thị đầy đủ thông tin
- [ ] Progress indicator hoạt động chính xác
- [ ] Batch processing xử lý từng dự án riêng lẻ
- [ ] Tích hợp thành công với Bitrix24
- [ ] Notification system hoạt động
- [ ] Tất cả test cases pass

---

### 11. Risks and Mitigation

#### 11.1 Technical Risks
- **Risk:** Performance issues với large batch processing
- **Mitigation:** Implement batch size limits và progress tracking

- **Risk:** Partial failures affecting user experience
- **Mitigation:** Comprehensive error handling và detailed reporting

- **Risk:** Memory issues với large selections
- **Mitigation:** Implement pagination và lazy loading

#### 11.2 Business Risks
- **Risk:** User confusion about bulk operations
- **Mitigation:** Clear UI indicators và help documentation

- **Risk:** Accidental bulk submissions
- **Mitigation:** Confirmation dialogs và undo functionality

---

### 12. Future Enhancements
- Advanced filtering cho bulk selection
- Bulk approval templates
- Scheduled bulk approvals
- Bulk approval analytics
- Advanced batch processing
- Bulk approval workflows

---

### 13. Dependencies
- **DMDA-1.1**: Cần có danh sách dự án
- **DMDA-3.1**: Cần có gửi phê duyệt đơn lẻ
- **User Management**: Cần hệ thống phân quyền
- **Notification System**: Cần hệ thống thông báo
- **Bitrix24 API**: Cần integration endpoints

---

### 14. Bulk Processing Rules

#### 14.1 Selection Rules
| Project Status | Can Select | Checkbox State | Reason |
|----------------|------------|----------------|---------|
| Draft | Yes | Enabled | Có thể gửi phê duyệt |
| Edit Requested | Yes | Enabled | Có thể gửi phê duyệt |
| Pending Approval | No | Disabled | Đã gửi phê duyệt |
| Approved | No | Disabled | Đã được phê duyệt |
| In Progress | No | Disabled | Đang thực hiện |
| Completed | No | Disabled | Đã hoàn thành |
| Cancelled | No | Disabled | Đã hủy |

#### 14.2 Processing Rules
- **Batch Size Limit**: Tối đa 50 dự án mỗi lần
- **Processing Order**: Theo thứ tự trong danh sách
- **Error Handling**: Continue processing nếu một dự án thất bại
- **Timeout**: 30 giây cho mỗi dự án

#### 14.3 User Role vs Bulk Permission
| User Role | Can Bulk Submit | Max Batch Size | Can View History |
|-----------|----------------|----------------|------------------|
| Creator | Yes | 50 | Yes |
| Manager | Yes | 50 | Yes |
| Admin | Yes | 100 | Yes |
| Viewer | No | 0 | No |

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 3 