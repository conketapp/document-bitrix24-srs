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

## User Story: DMDA-2.2
### Chỉnh sửa Dự án

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-2.2
- **Priority:** High
- **Story Points:** 13
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-1.2, DMDA-1.3, DMDA-2.1 (Cần có danh sách dự án và tạo dự án)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ khởi tạo dự án,  
**Tôi muốn** có thể chỉnh sửa tất cả các thông tin của một dự án,  
**Tùy theo trạng thái phê duyệt**,  
**Để** đảm bảo mọi thông tin được cập nhật chính xác trước khi đi vào thực hiện hoặc khi cần điều chỉnh sau phê duyệt.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Khi dự án chưa được phê duyệt (trạng thái là "Khởi tạo" hoặc "Chờ phê duyệt"): Người dùng có thể trực tiếp chỉnh sửa toàn bộ thông tin dự án
- [ ] Nút "Chỉnh sửa" hiển thị rõ ràng trên giao diện
- [ ] Khi dự án đã được phê duyệt: Hệ thống hiển thị nút "Yêu cầu chỉnh sửa"
- [ ] Khi người dùng gửi yêu cầu, dự án chuyển sang trạng thái "Yêu cầu chỉnh sửa"
- [ ] Sau khi được người có thẩm quyền phê duyệt yêu cầu: Người gửi mới được chỉnh sửa thông tin
- [ ] Mọi thay đổi phải được ghi lại trong log lịch sử dự án
- [ ] Nếu từ chối, hệ thống thông báo lý do và không cho chỉnh sửa

#### 2.4 Activity Diagram
![DMDA-2.2 Activity Diagram](diagrams/DMDA-2.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý chỉnh sửa dự án theo trạng thái*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Chỉnh sửa Dự án Trực tiếp**
   - Chỉnh sửa khi trạng thái: "Khởi tạo", "Chờ phê duyệt"
   - Form chỉnh sửa với tất cả thông tin dự án
   - Validation real-time
   - Auto-save draft (tùy chọn)

2. **Quy trình Yêu cầu Chỉnh sửa**
   - Nút "Yêu cầu chỉnh sửa" cho dự án đã phê duyệt
   - Form gửi yêu cầu với lý do chỉnh sửa
   - Workflow phê duyệt yêu cầu
   - Thông báo kết quả phê duyệt

3. **Quản lý Trạng thái Dự án**
   - **Khởi tạo**: Có thể chỉnh sửa trực tiếp
   - **Chờ phê duyệt**: Có thể chỉnh sửa trực tiếp
   - **Đã phê duyệt**: Chỉ có thể yêu cầu chỉnh sửa
   - **Yêu cầu chỉnh sửa**: Chờ phê duyệt yêu cầu
   - **Đang thực hiện**: Chỉ có thể yêu cầu chỉnh sửa
   - **Hoàn thành**: Không thể chỉnh sửa

#### 3.2 Business Rules
- Chỉ người tạo dự án hoặc người được phân quyền mới có thể chỉnh sửa
- Mọi thay đổi phải được log lại với timestamp và user
- Dự án đã phê duyệt cần workflow phê duyệt yêu cầu chỉnh sửa
- Người phê duyệt yêu cầu chỉnh sửa phải có quyền "APPROVE_EDIT_REQUEST"

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
- Thời gian mở form chỉnh sửa < 2 giây
- Thời gian lưu thay đổi < 3 giây
- Real-time validation không lag
- Log history load < 1 giây

#### 4.2 Usability
- Form chỉnh sửa dễ sử dụng
- Validation messages rõ ràng
- Confirmation dialogs cho thay đổi quan trọng
- Undo/Redo functionality (tùy chọn)

#### 4.3 Security
- Xác thực người dùng trước khi chỉnh sửa
- Phân quyền theo vai trò và trạng thái dự án
- Audit trail cho mọi thay đổi
- CSRF protection

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Cập nhật bảng projects với trạng thái mới
ALTER TABLE projects MODIFY COLUMN status ENUM(
    'initialized',     -- Khởi tạo
    'pending_approval', -- Chờ phê duyệt
    'approved',        -- Đã phê duyệt
    'rejected',        -- Từ chối phê duyệt
    'suspended',       -- Dừng thực hiện
    'edit_requested'   -- Yêu cầu chỉnh sửa
) DEFAULT 'initialized';

-- Bảng lưu lịch sử thay đổi dự án
CREATE TABLE project_change_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    action_type ENUM('create', 'edit', 'edit_request', 'approve_edit', 'reject_edit') NOT NULL,
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bảng yêu cầu chỉnh sửa
CREATE TABLE project_edit_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    requester_id INT NOT NULL,
    request_reason TEXT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approver_id INT,
    approval_date TIMESTAMP NULL,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (requester_id) REFERENCES users(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

-- Bảng quyền người dùng
CREATE TABLE user_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    permission_type ENUM('EDIT_PROJECT', 'APPROVE_EDIT_REQUEST', 'VIEW_PROJECT_HISTORY') NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (granted_by) REFERENCES users(id)
);
```

#### 5.2 API Endpoints
```
GET /api/projects/{id}/edit
- Response: Project data for editing

PUT /api/projects/{id}
- Request: Updated project data
- Response: Updated project with change log

POST /api/projects/{id}/edit-request
- Request: { reason: string }
- Response: Edit request created

GET /api/projects/{id}/edit-requests
- Response: List of edit requests for project

PUT /api/projects/{id}/edit-requests/{request_id}/approve
- Request: { approver_id: number }
- Response: Request approved

PUT /api/projects/{id}/edit-requests/{request_id}/reject
- Request: { rejection_reason: string }
- Response: Request rejected

GET /api/projects/{id}/change-history
- Response: List of project changes
```

#### 5.3 Data Models
```typescript
interface Project {
    id: number;
    project_code: string;
    name: string;
    description?: string;
    category_id: number;
    year: number;
    start_date: string;
    end_date?: string;
    budget?: number;
    status: 'initialized' | 'pending_approval' | 'approved' | 'rejected' | 'suspended' | 'edit_requested';
    created_by: number;
    created_at: string;
    updated_at: string;
}

interface ProjectEditRequest {
    id: number;
    project_id: number;
    requester_id: number;
    request_reason: string;
    status: 'pending' | 'approved' | 'rejected';
    approver_id?: number;
    approval_date?: string;
    rejection_reason?: string;
    created_at: string;
}

interface ProjectChangeLog {
    id: number;
    project_id: number;
    user_id: number;
    action_type: 'create' | 'edit' | 'edit_request' | 'approve_edit' | 'reject_edit';
    field_name?: string;
    old_value?: string;
    new_value?: string;
    change_reason?: string;
    created_at: string;
}

interface EditProjectRequest {
    name?: string;
    description?: string;
    category_id?: number;
    year?: number;
    start_date?: string;
    end_date?: string;
    budget?: number;
}
```

#### 5.4 Sequence Diagram
![DMDA-2.2 Sequence Diagram](diagrams/DMDA-2.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi chỉnh sửa dự án*

#### 5.5 UI Components
- EditProjectButton: Nút chỉnh sửa dự án
- RequestEditButton: Nút yêu cầu chỉnh sửa
- ProjectEditForm: Form chỉnh sửa dự án
- EditRequestForm: Form gửi yêu cầu chỉnh sửa
- ChangeHistoryModal: Modal xem lịch sử thay đổi
- ApprovalWorkflow: Workflow phê duyệt yêu cầu

---

### 6. Yêu cầu Tích hợp

#### 6.1 Tích hợp Bitrix24
- Đồng bộ thay đổi dự án với Bitrix24
- Cập nhật thông tin deal/lead khi chỉnh sửa
- Đồng bộ quy trình phê duyệt với Bitrix24
- Ghi log thay đổi trong Bitrix24 activity feed

#### 6.2 Hệ thống Thông báo
- Thông báo email cho người phê duyệt
- Thông báo trong ứng dụng cho người gửi yêu cầu
- Thông báo SMS cho thay đổi khẩn cấp (tùy chọn)

#### 6.3 Luồng Dữ liệu
1. Người dùng nhấn "Chỉnh sửa" hoặc "Yêu cầu chỉnh sửa"
2. Hệ thống kiểm tra quyền và trạng thái dự án
3. Hiển thị form phù hợp (chỉnh sửa trực tiếp hoặc form yêu cầu)
4. Người dùng gửi thay đổi
5. Hệ thống xác thực và xử lý
6. Cập nhật cơ sở dữ liệu và đồng bộ với Bitrix24
7. Gửi thông báo
8. Ghi log thay đổi

---

### 7. Yêu cầu Giao diện Người dùng

#### 7.1 Bố cục Form Chỉnh sửa
```
┌─────────────────────────────────────┐
│ Chỉnh sửa Dự án: [Project Name]    │
├─────────────────────────────────────┤
│ Tên dự án *                        │
│ [Input field]                      │
│                                     │
│ Loại dự án *                       │
│ [Dropdown]                         │
│                                     │
│ Năm thực hiện *                    │
│ [Dropdown]                         │
│                                     │
│ Ngày bắt đầu *                     │
│ [Date picker]                      │
│                                     │
│ Ngày kết thúc dự kiến              │
│ [Date picker]                      │
│                                     │
│ Ngân sách                          │
│ [Number input]                     │
│                                     │
│ Mô tả dự án                        │
│ [Textarea]                         │
│                                     │
│ [Cancel] [Lưu thay đổi]           │
└─────────────────────────────────────┘
```

#### 7.2 Form Yêu cầu Chỉnh sửa
```
┌─────────────────────────────────────┐
│ Yêu cầu Chỉnh sửa Dự án            │
├─────────────────────────────────────┤
│ Lý do chỉnh sửa *                  │
│ [Textarea - required]              │
│                                     │
│ Chi tiết thay đổi dự kiến:         │
│ [Textarea - optional]              │
│                                     │
│ [Cancel] [Gửi yêu cầu]            │
└─────────────────────────────────────┘
```

#### 7.3 Giao diện theo Trạng thái
- **Draft/Pending**: Hiển thị nút "Chỉnh sửa"
- **Approved/In Progress**: Hiển thị nút "Yêu cầu chỉnh sửa"
- **Completed**: Chỉ hiển thị nút "Xem lịch sử"
- **Edit Requested**: Hiển thị trạng thái "Đang chờ phê duyệt"

---

### 8. Yêu cầu Kiểm thử

#### 8.1 Kiểm thử Đơn vị
```typescript
describe('Quyền Chỉnh sửa Dự án', () => {
    test('nên cho phép chỉnh sửa trực tiếp cho dự án draft', () => {
        const project = { status: 'draft' };
        const user = { permissions: ['EDIT_PROJECT'] };
        expect(canEditDirectly(project, user)).toBe(true);
    });

    test('nên yêu cầu gửi yêu cầu chỉnh sửa cho dự án đã phê duyệt', () => {
        const project = { status: 'approved' };
        const user = { permissions: ['EDIT_PROJECT'] };
        expect(canEditDirectly(project, user)).toBe(false);
        expect(canRequestEdit(project, user)).toBe(true);
    });

    test('should log all changes', async () => {
        const changes = { name: 'Old Name', newName: 'New Name' };
        await updateProject(projectId, changes);
        const logs = await getChangeLogs(projectId);
        expect(logs).toContainEqual({
            action_type: 'edit',
            field_name: 'name',
            old_value: 'Old Name',
            new_value: 'New Name'
        });
    });
});
```

#### 8.2 Integration Tests
- Test approval workflow
- Test Bitrix24 sync
- Test notification system
- Test permission system

#### 8.3 User Acceptance Tests
- Test direct editing for draft projects
- Test edit request workflow
- Test approval/rejection process
- Test change history viewing

---

### 9. Deployment Requirements

#### 9.1 Database Migration
```sql
-- Migration script
BEGIN;
-- Update projects table
ALTER TABLE projects MODIFY COLUMN status ENUM(...);

-- Create new tables
CREATE TABLE project_change_logs (...);
CREATE TABLE project_edit_requests (...);
CREATE TABLE user_permissions (...);

-- Add indexes
CREATE INDEX idx_change_logs_project ON project_change_logs(project_id);
CREATE INDEX idx_edit_requests_project ON project_edit_requests(project_id);
CREATE INDEX idx_user_permissions_user ON user_permissions(user_id);

COMMIT;
```

#### 9.2 Environment Configuration
- Permission settings
- Notification settings
- Workflow configuration
- Bitrix24 integration settings

---

### 10. Success Criteria
- [ ] User có thể chỉnh sửa dự án draft/pending trực tiếp
- [ ] User có thể gửi yêu cầu chỉnh sửa cho dự án approved
- [ ] Workflow phê duyệt hoạt động chính xác
- [ ] Mọi thay đổi được log đầy đủ
- [ ] Tích hợp thành công với Bitrix24
- [ ] Notification system hoạt động
- [ ] Tất cả test cases pass

---

### 11. Risks and Mitigation

#### 11.1 Technical Risks
- **Risk:** Complex approval workflow
- **Mitigation:** Use workflow engine và comprehensive testing

- **Risk:** Data inconsistency during concurrent edits
- **Mitigation:** Implement optimistic locking

- **Risk:** Performance issues với large change logs
- **Mitigation:** Implement pagination và archiving

#### 11.2 Business Risks
- **Risk:** User confusion about edit permissions
- **Mitigation:** Clear UI indicators và help documentation

- **Risk:** Approval delays affecting project timeline
- **Mitigation:** Implement escalation rules và notifications

---

### 12. Future Enhancements
- Bulk edit functionality
- Advanced approval workflows
- Change impact analysis
- Automated approval rules
- Change templates
- Advanced reporting

---

### 13. Dependencies
- **DMDA-1.1**: Cần có danh sách dự án
- **DMDA-2.1**: Cần có tạo dự án
- **User Management**: Cần hệ thống phân quyền
- **Notification System**: Cần hệ thống thông báo
- **Bitrix24 API**: Cần integration endpoints

---

### 14. Workflow States

#### 14.1 Project Status Flow
```
Khởi tạo → Chờ phê duyệt → Đã phê duyệt → Từ chối phê duyệt → Dừng thực hiện → Yêu cầu chỉnh sửa
  ↓         ↓                ↓           ↓
Direct    Direct          Request     Request
Edit      Edit            Edit        Edit
```

#### 14.2 Edit Request Flow
```
Request Created → Pending Approval → Approved/Rejected
      ↓                ↓                ↓
   Email           Email to         Email to
Notification    Approver         Requester
```

#### 14.3 Permission Matrix
| User Role | Khởi tạo | Chờ phê duyệt | Đã phê duyệt | Từ chối phê duyệt | Dừng thực hiện | Yêu cầu chỉnh sửa |
|-----------|-------|---------|----------|-------------|-----------|
| Creator | Edit | Edit | Request | Request | View Only |
| Manager | Edit | Edit | Approve | Request | View Only |
| Viewer | View | View | View | View | View |

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 2 