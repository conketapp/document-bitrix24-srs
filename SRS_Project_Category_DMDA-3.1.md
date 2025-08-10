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

## User Story: DMDA-3.1
### Gửi Phê duyệt Dự án Lần lượt

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-3.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 3
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-2.1, DMDA-2.2 (Cần có danh sách dự án và tạo/chỉnh sửa dự án)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** có thể gửi từng dự án riêng lẻ để phê duyệt,  
**Để** tôi có thể kiểm soát và theo dõi chi tiết từng quy trình phê duyệt của từng dự án.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Gửi Phê duyệt" trên trang chi tiết của mỗi dự án
- [ ] Nút chỉ hiển thị cho dự án có trạng thái "Khởi tạo" hoặc "Chỉnh sửa"
- [ ] Khi gửi, dự án sẽ chuyển trạng thái và thông báo được gửi đến người phê duyệt
- [ ] Có hộp thoại xác nhận trước khi gửi phê duyệt
- [ ] Hiển thị danh sách người phê duyệt có thể chọn
- [ ] Ghi log hành động gửi phê duyệt
- [ ] Thông báo thành công sau khi gửi phê duyệt

#### 2.4 Activity Diagram
![DMDA-3.1 Activity Diagram](diagrams/DMDA-3.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý gửi phê duyệt dự án lần lượt*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Gửi Phê duyệt Dự án**
   - Chỉ cho phép gửi dự án có trạng thái: "initialized", "edit_requested"
   - Form chọn người phê duyệt
   - Validation trước khi gửi
   - Confirmation dialog

2. **Quản lý Trạng thái Dự án**
   - Chuyển trạng thái từ "initialized" → "pending_approval"
   - Chuyển trạng thái từ "edit_requested" → "pending_approval"
   - Hiển thị trạng thái "Chờ phê duyệt" rõ ràng

3. **Workflow Phê duyệt**
   - Chọn người phê duyệt từ danh sách
   - Gửi notification cho người phê duyệt
   - Theo dõi trạng thái phê duyệt
   - Log toàn bộ quá trình

#### 3.2 Business Rules
- Chỉ người tạo dự án hoặc người có quyền "SUBMIT_FOR_APPROVAL" mới có thể gửi phê duyệt
- Dự án đã phê duyệt không thể gửi phê duyệt lại
- Mỗi lần gửi phê duyệt phải chọn ít nhất một người phê duyệt
- Người phê duyệt phải có quyền "APPROVE_PROJECT"

#### 3.3 Mapping Trạng thái Dự án
| Key (Database) | Label (Hiển thị) | Mô tả |
|----------------|-------------------|-------|
| initialized | Khởi tạo | Dự án mới được tạo |
| pending_approval | Chờ phê duyệt | Dự án đã gửi chờ phê duyệt |
| approved | Đã phê duyệt | Dự án đã được phê duyệt |
| rejected | Từ chối phê duyệt | Dự án bị từ chối phê duyệt |
| suspended | Dừng thực hiện | Dự án tạm dừng thực hiện |
| edit_requested | Yêu cầu chỉnh sửa | Dự án yêu cầu chỉnh sửa |

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian hiển thị form gửi phê duyệt < 1 giây
- Thời gian gửi phê duyệt < 3 giây
- Load danh sách người phê duyệt < 2 giây

#### 4.2 Usability
- Form gửi phê duyệt dễ sử dụng
- Confirmation dialog rõ ràng
- Thông báo lỗi cụ thể
- Hiển thị trạng thái phê duyệt rõ ràng

#### 4.3 Security
- Xác thực người dùng trước khi gửi phê duyệt
- Phân quyền theo vai trò
- Audit trail cho mọi thao tác gửi phê duyệt
- CSRF protection

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Bảng quản lý phê duyệt dự án
CREATE TABLE project_approvals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    submitted_by INT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approver_id INT,
    approval_date TIMESTAMP NULL,
    approval_comment TEXT,
    rejection_reason TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

-- Bảng lưu lịch sử gửi phê duyệt
CREATE TABLE project_submission_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    submitted_by INT NOT NULL,
    approver_id INT NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submission_comment TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

-- Bảng quyền người phê duyệt
CREATE TABLE project_approvers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    approval_level ENUM('level_1', 'level_2', 'level_3') DEFAULT 'level_1',
    max_approval_amount DECIMAL(15,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Thêm index cho performance
CREATE INDEX idx_project_approvals_project ON project_approvals(project_id);
CREATE INDEX idx_project_approvals_status ON project_approvals(status);
CREATE INDEX idx_project_submission_logs_project ON project_submission_logs(project_id);
```

#### 5.2 API Endpoints
```
POST /api/projects/{id}/submit-for-approval
- Request: { approver_id: number, comment?: string }
- Response: { success: boolean, message: string }

GET /api/projects/{id}/can-submit-approval
- Response: { canSubmit: boolean, reason?: string }

GET /api/projects/approvers
- Response: List of available approvers

GET /api/projects/{id}/approval-status
- Response: Current approval status and history

POST /api/projects/{id}/approve
- Request: { approver_id: number, comment?: string }
- Response: Project approved successfully

POST /api/projects/{id}/reject
- Request: { approver_id: number, reason: string }
- Response: Project rejected successfully
```

#### 5.3 Data Models
```typescript
interface Project {
    id: number;
    project_code: string;
    name: string;
    status: 'initialized' | 'pending_approval' | 'approved' | 'rejected' | 'suspended' | 'edit_requested';
    submitted_for_approval_at?: string;
    submitted_by?: number;
    // ... other fields
}

interface SubmitApprovalRequest {
    approver_id: number;
    comment?: string;
}

interface SubmitApprovalResponse {
    success: boolean;
    message: string;
    project_id: number;
    new_status: string;
}

interface ProjectApproval {
    id: number;
    project_id: number;
    submitted_by: number;
    submitted_at: string;
    status: 'pending' | 'approved' | 'rejected';
    approver_id?: number;
    approval_date?: string;
    approval_comment?: string;
    rejection_reason?: string;
}

interface ProjectApprover {
    id: number;
    user_id: number;
    user_name: string;
    approval_level: 'level_1' | 'level_2' | 'level_3';
    max_approval_amount?: number;
    is_active: boolean;
}

interface CanSubmitApprovalResponse {
    canSubmit: boolean;
    reason?: string;
    projectStatus: string;
    userPermissions: string[];
    availableApprovers: ProjectApprover[];
}
```

#### 5.4 UI Components
- SubmitApprovalButton: Nút gửi phê duyệt (conditional)
- SubmitApprovalModal: Modal gửi phê duyệt
- ApproverSelectionDropdown: Dropdown chọn người phê duyệt
- ApprovalCommentInput: Input nhập comment
- ApprovalStatusBadge: Badge hiển thị trạng thái phê duyệt
- ApprovalHistoryModal: Modal xem lịch sử phê duyệt

#### 5.5 Sequence Diagram
![DMDA-3.1 Sequence Diagram](diagrams/DMDA-3.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi gửi phê duyệt dự án*

---

### 6. Integration Requirements

#### 6.1 Bitrix24 Integration
- Update deal status thành "PENDING_APPROVAL" trong Bitrix24
- Create task cho người phê duyệt trong Bitrix24
- Sync approval workflow với Bitrix24
- Log approval action trong Bitrix24 activity feed

#### 6.2 Notification System
- Email notification cho người phê duyệt
- In-app notification cho project manager
- SMS notification cho urgent approvals (tùy chọn)
- Reminder notifications cho pending approvals

#### 6.3 Data Flow
1. User click "Gửi Phê duyệt" button
2. System check permissions và project status
3. Show submission form với danh sách approvers
4. User chọn approver và nhập comment
5. System validate và submit for approval
6. Update project status
7. Create approval record
8. Sync với Bitrix24
9. Send notifications
10. Log submission action

---

### 7. User Interface Requirements

#### 7.1 Submit Button Visibility
- **Draft**: Show "Gửi Phê duyệt" button
- **Edit Requested**: Show "Gửi Phê duyệt" button
- **Pending Approval**: Show "Đang chờ phê duyệt" status
- **Approved/In Progress**: Hide submit button
- **Completed/Cancelled**: Hide submit button

#### 7.2 Submission Form Layout
```
┌─────────────────────────────────────┐
│ Gửi Dự án để Phê duyệt             │
├─────────────────────────────────────┤
│ Dự án: INV-2024-001 - Dự án ABC   │
│                                     │
│ Người phê duyệt *                  │
│ [Dropdown với danh sách approvers] │
│                                     │
│ Ghi chú (tùy chọn)                 │
│ [Textarea]                         │
│                                     │
│ ⚠️ Lưu ý: Dự án sẽ chuyển sang     │
│    trạng thái "Chờ phê duyệt"      │
│                                     │
│ [Hủy] [Gửi Phê duyệt]             │
└─────────────────────────────────────┘
```

#### 7.3 Approval Status Display
- **Pending Approval**: Badge màu vàng với icon "clock"
- **Approved**: Badge màu xanh với icon "check"
- **Rejected**: Badge màu đỏ với icon "x"
- **Approval Date**: Hiển thị ngày phê duyệt
- **Approver Name**: Hiển thị tên người phê duyệt

#### 7.4 Success/Error Messages
- **Success**: "Đã gửi dự án để phê duyệt thành công"
- **Error - No Permission**: "Bạn không có quyền gửi phê duyệt"
- **Error - Invalid Status**: "Không thể gửi phê duyệt dự án ở trạng thái này"
- **Error - No Approver**: "Vui lòng chọn người phê duyệt"
- **Error - System Error**: "Có lỗi xảy ra, vui lòng thử lại"

---

### 8. Testing Requirements

#### 8.1 Unit Tests
```typescript
describe('Project Approval Submission', () => {
    test('should allow submission of draft project', () => {
        const project = { status: 'draft' };
        const user = { permissions: ['SUBMIT_FOR_APPROVAL'] };
        expect(canSubmitForApproval(project, user)).toBe(true);
    });

    test('should not allow submission of approved project', () => {
        const project = { status: 'approved' };
        const user = { permissions: ['SUBMIT_FOR_APPROVAL'] };
        expect(canSubmitForApproval(project, user)).toBe(false);
    });

    test('nên gửi dự án để phê duyệt', async () => {
        const projectId = 1;
        const approverId = 2;
        const comment = 'Sẵn sàng để xem xét';
        await submitForApproval(projectId, approverId, comment);
        
        const project = await getProject(projectId);
        expect(project.status).toBe('pending_approval');
        expect(project.submitted_for_approval_at).toBeDefined();
    });

    test('nên tạo bản ghi phê duyệt', async () => {
        const projectId = 1;
        const approverId = 2;
        await submitForApproval(projectId, approverId);
        
        const approval = await getProjectApproval(projectId);
        expect(approval.status).toBe('pending');
        expect(approval.approver_id).toBe(approverId);
    });
});
```

#### 8.2 Kiểm thử Tích hợp
- Kiểm thử đồng bộ Bitrix24 khi gửi phê duyệt
- Kiểm thử hệ thống thông báo
- Kiểm thử hệ thống phân quyền
- Kiểm thử quy trình phê duyệt

#### 8.3 Kiểm thử Chấp nhận Người dùng
- Kiểm thử hiển thị nút gửi phê duyệt
- Kiểm thử form gửi phê duyệt
- Kiểm thử chọn người phê duyệt
- Kiểm thử quy trình phê duyệt
- Kiểm thử xử lý lỗi

---

### 9. Deployment Requirements

#### 9.1 Di chuyển Cơ sở Dữ liệu
```sql
-- Script di chuyển
BEGIN;
-- Tạo bảng phê duyệt
CREATE TABLE project_approvals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    submitted_by INT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approver_id INT,
    approval_date TIMESTAMP NULL,
    approval_comment TEXT,
    rejection_reason TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

CREATE TABLE project_submission_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    submitted_by INT NOT NULL,
    approver_id INT NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submission_comment TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

CREATE TABLE project_approvers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    approval_level ENUM('level_1', 'level_2', 'level_3') DEFAULT 'level_1',
    max_approval_amount DECIMAL(15,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Thêm các index
CREATE INDEX idx_project_approvals_project ON project_approvals(project_id);
CREATE INDEX idx_project_approvals_status ON project_approvals(status);
CREATE INDEX idx_project_submission_logs_project ON project_submission_logs(project_id);

-- Thêm người phê duyệt mặc định
INSERT INTO project_approvers (user_id, approval_level, max_approval_amount) VALUES
(1, 'level_1', 100000000),
(2, 'level_2', 500000000),
(3, 'level_3', 1000000000);

COMMIT;
```

#### 9.2 Cấu hình Môi trường
- Cài đặt phê duyệt
- Cài đặt thông báo
- Cài đặt phân quyền
- Cài đặt tích hợp Bitrix24

---

### 10. Tiêu chí Thành công
- [ ] Người dùng chỉ có thể gửi phê duyệt dự án khởi tạo/yêu cầu chỉnh sửa
- [ ] Form gửi phê duyệt hiển thị đầy đủ thông tin
- [ ] Bản ghi phê duyệt được tạo chính xác
- [ ] Tích hợp thành công với Bitrix24
- [ ] Hệ thống thông báo hoạt động
- [ ] Tất cả các trường hợp kiểm thử đều thành công

---

### 11. Rủi ro và Giải pháp

#### 11.1 Rủi ro Kỹ thuật
- **Rủi ro:** Quy trình phê duyệt phức tạp
- **Giải pháp:** Sử dụng workflow engine và kiểm thử toàn diện

- **Rủi ro:** Thất bại gửi thông báo
- **Giải pháp:** Triển khai logic thử lại và thông báo dự phòng

- **Rủi ro:** Vấn đề hiệu suất với danh sách phê duyệt lớn
- **Giải pháp:** Triển khai phân trang và cache

#### 11.2 Rủi ro Kinh doanh
- **Rủi ro:** Người dùng nhầm lẫn về quy trình phê duyệt
- **Giải pháp:** Chỉ báo UI rõ ràng và tài liệu hướng dẫn

- **Rủi ro:** Chậm trễ phê duyệt ảnh hưởng tiến độ dự án
- **Giải pháp:** Triển khai quy tắc leo thang và nhắc nhở

---

### 12. Cải tiến Tương lai
- Quy trình phê duyệt nhiều cấp
- Gửi phê duyệt hàng loạt
- Mẫu phê duyệt
- Quy tắc phê duyệt tự động
- Phân tích phê duyệt
- Theo dõi phê duyệt nâng cao

---

### 13. Phụ thuộc
- **DMDA-1.1**: Cần có danh sách dự án
- **DMDA-2.1**: Cần có tạo dự án
- **DMDA-2.2**: Cần có chỉnh sửa dự án
- **Quản lý Người dùng**: Cần hệ thống phân quyền
- **Hệ thống Thông báo**: Cần hệ thống thông báo
- **Bitrix24 API**: Cần các endpoint tích hợp

---

### 14. Ma trận Quy tắc Phê duyệt

#### 14.1 Trạng thái Dự án vs Quyền Gửi Phê duyệt
| Trạng thái Dự án | Có thể Gửi | Văn bản Nút | Yêu cầu Xác nhận |
|------------------|------------|-------------|------------------|
| Khởi tạo | Có | "Gửi Phê duyệt" | Có |
| Yêu cầu chỉnh sửa | Có | "Gửi Phê duyệt" | Có |
| Chờ phê duyệt | Không | "Đang chờ phê duyệt" | Không áp dụng |
| Đã phê duyệt | Không | Ẩn | Không áp dụng |
| Đang thực hiện | Không | Ẩn | Không áp dụng |
| Dừng thực hiện | Không | Ẩn | Không áp dụng |
| Hoàn thành | Không | Ẩn | Không áp dụng |
| Đã hủy | Không | Ẩn | Không áp dụng |

#### 14.2 Vai trò Người dùng vs Quyền Gửi Phê duyệt
| Vai trò Người dùng | Khởi tạo | Chờ phê duyệt | Đã phê duyệt | Từ chối phê duyệt | Dừng thực hiện | Yêu cầu chỉnh sửa |
|-------------------|----------|---------------------------|----------------|-------------|
| Người tạo | Gửi | Gửi | Xem | Không |
| Quản lý | Gửi | Gửi | Xem | Không |
| Quản trị viên | Gửi | Gửi | Xem | Không |
| Người xem | Không | Không | Xem | Không |

#### 14.3 Quy trình Gửi Phê duyệt
```
Người dùng nhấn Gửi → Kiểm tra Quyền → Hiển thị Form → 
Người dùng chọn Người phê duyệt → Người dùng xác nhận → Cập nhật Trạng thái → 
Tạo Bản ghi Phê duyệt → Đồng bộ với Bitrix24 → 
Gửi Thông báo → Ghi Log
```

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 3 