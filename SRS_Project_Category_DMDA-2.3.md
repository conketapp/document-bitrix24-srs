# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### 1. Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Date:** 2024  
**Author:** Development Team  

### 2. Mô tả Epic
Epic này tập trung vào việc phát triển hệ thống quản lý danh mục dự án, cho phép cán bộ quản lý dự án tổ chức và quản lý các dự án theo năm và phân loại một cách hiệu quả.

---

## User Story: DMDA-2.3
### Xóa Dự án

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-2.3
- **Priority:** Medium
- **Story Points:** 5
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-2.1, DMDA-2.2 (Cần có danh sách dự án và quản lý trạng thái)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ khởi tạo dự án,  
**Tôi muốn** có thể xóa một dự án khỏi danh mục,  
**Chỉ khi dự án đó chưa được phê duyệt**,  
**Để** tôi có thể loại bỏ các dự án bị trùng lặp, sai sót hoặc không còn cần thiết.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Nút/chức năng "Xóa" chỉ hiển thị hoặc cho phép xóa khi trạng thái dự án là "Chờ phê duyệt" hoặc "Khởi tạo"
- [ ] Có hộp thoại xác nhận trước khi xóa để tránh thao tác nhầm lẫn
- [ ] Hiển thị thông tin dự án trong hộp thoại xác nhận để user xác nhận đúng dự án
- [ ] Sau khi xóa, dự án không còn hiển thị trong danh sách
- [ ] Thông báo thành công sau khi xóa
- [ ] Ghi log xóa dự án vào lịch sử hệ thống
- [ ] Đồng bộ xóa dự án với Bitrix24

#### 2.4 Activity Diagram
![DMDA-2.3 Activity Diagram](diagrams/DMDA-2.3%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý xóa dự án theo trạng thái*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Xóa Dự án có Điều kiện**
   - Chỉ cho phép xóa dự án có trạng thái: "draft", "pending_approval"
   - Ẩn nút xóa cho dự án đã phê duyệt
   - Validation trước khi xóa

2. **Confirmation Dialog**
   - Hiển thị thông tin dự án cần xóa
   - Yêu cầu user nhập lý do xóa
   - Cảnh báo về tính không thể hoàn tác

3. **Soft Delete Implementation**
   - Không xóa thực sự dữ liệu khỏi database
   - Chỉ đánh dấu deleted_at và status = 'deleted'
   - Giữ lại lịch sử cho audit trail

#### 3.2 Business Rules
- Chỉ người tạo dự án hoặc người có quyền "DELETE_PROJECT" mới có thể xóa
- Dự án đã phê duyệt không thể xóa (chỉ có thể hủy)
- Mọi thao tác xóa phải được log với lý do
- Xóa dự án sẽ xóa tất cả related data (edit requests, change logs)

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian hiển thị confirmation dialog < 1 giây
- Thời gian xóa dự án < 3 giây
- Không ảnh hưởng đến performance của danh sách dự án

#### 4.2 Usability
- Confirmation dialog rõ ràng và dễ hiểu
- Thông báo lỗi cụ thể khi không thể xóa
- Undo functionality (tùy chọn, trong 30 giây)

#### 4.3 Security
- Xác thực người dùng trước khi xóa
- Phân quyền theo vai trò và trạng thái dự án
- Audit trail cho mọi thao tác xóa
- CSRF protection

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Thêm trường deleted_at vào bảng projects
ALTER TABLE projects ADD COLUMN deleted_at TIMESTAMP NULL;
ALTER TABLE projects ADD COLUMN deleted_by INT NULL;
ALTER TABLE projects ADD COLUMN delete_reason TEXT;

-- Thêm index cho soft delete
CREATE INDEX idx_projects_deleted ON projects(deleted_at);
CREATE INDEX idx_projects_status_deleted ON projects(status, deleted_at);

-- Bảng log xóa dự án
CREATE TABLE project_deletion_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    deleted_by INT NOT NULL,
    delete_reason TEXT NOT NULL,
    project_data JSON, -- Lưu snapshot dữ liệu dự án trước khi xóa
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (deleted_by) REFERENCES users(id)
);

-- Trigger để tự động cập nhật deleted_at
DELIMITER //
CREATE TRIGGER update_deleted_at
BEFORE UPDATE ON projects
FOR EACH ROW
BEGIN
    IF NEW.status = 'deleted' AND OLD.status != 'deleted' THEN
        SET NEW.deleted_at = CURRENT_TIMESTAMP;
    END IF;
END//
DELIMITER ;
```

#### 5.2 API Endpoints
```
DELETE /api/projects/{id}
- Request: { reason: string }
- Response: { success: boolean, message: string }

GET /api/projects/{id}/can-delete
- Response: { canDelete: boolean, reason?: string }

POST /api/projects/{id}/restore
- Request: { reason: string }
- Response: Project restored successfully

GET /api/projects/deleted
- Response: List of deleted projects (admin only)
```

#### 5.3 Data Models
```typescript
interface Project {
    id: number;
    project_code: string;
    name: string;
    status: 'draft' | 'pending_approval' | 'approved' | 'edit_requested' | 'in_progress' | 'completed' | 'cancelled' | 'deleted';
    deleted_at?: string;
    deleted_by?: number;
    delete_reason?: string;
    // ... other fields
}

interface DeleteProjectRequest {
    reason: string;
}

interface DeleteProjectResponse {
    success: boolean;
    message: string;
    project_id: number;
}

interface ProjectDeletionLog {
    id: number;
    project_id: number;
    deleted_by: number;
    delete_reason: string;
    project_data: any; // JSON snapshot
    created_at: string;
}

interface CanDeleteResponse {
    canDelete: boolean;
    reason?: string;
    projectStatus: string;
    userPermissions: string[];
}
```

#### 5.4 Sequence Diagram
![DMDA-2.3 Sequence Diagram](diagrams/DMDA-2.3%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi xóa dự án*

#### 5.5 UI Components
- DeleteProjectButton: Nút xóa dự án (conditional)
- DeleteConfirmationModal: Modal xác nhận xóa
- DeleteReasonInput: Input nhập lý do xóa
- ProjectRestoreButton: Nút khôi phục dự án (admin)
- DeletedProjectsList: Danh sách dự án đã xóa (admin)

---

### 6. Yêu cầu Tích hợp

#### 6.1 Tích hợp Bitrix24
- Soft delete deal/lead trong Bitrix24
- Cập nhật deal status thành "CLOSED" với reason "Deleted"
- Đồng bộ deletion log với Bitrix24 activity feed
- Lưu trữ related contacts/companies nếu cần

#### 6.2 Hệ thống Thông báo
- Thông báo email cho admin khi có dự án bị xóa
- Thông báo trong ứng dụng cho user thực hiện xóa
- Cảnh báo cho stakeholders nếu dự án quan trọng bị xóa

#### 6.3 Luồng Dữ liệu
1. Người dùng nhấn nút "Xóa"
2. Hệ thống kiểm tra quyền và trạng thái dự án
3. Hiển thị confirmation dialog với thông tin dự án
4. Người dùng nhập lý do xóa và xác nhận
5. Hệ thống xác thực và soft delete dự án
6. Cập nhật related data (edit requests, logs)
7. Đồng bộ với Bitrix24
8. Gửi thông báo
9. Ghi log deletion action

---

### 7. Yêu cầu Giao diện Người dùng

#### 7.1 Hiển thị Nút Xóa
- **Draft/Pending**: Hiển thị nút "Xóa"
- **Approved/In Progress**: Ẩn nút "Xóa", hiển thị nút "Hủy"
- **Completed**: Ẩn nút "Xóa"
- **Deleted**: Hiển thị nút "Khôi phục" (chỉ admin)

#### 7.2 Confirmation Dialog Layout
```
┌─────────────────────────────────────┐
│ Xác nhận Xóa Dự án                 │
├─────────────────────────────────────┤
│ Bạn có chắc chắn muốn xóa dự án:   │
│                                     │
│ Mã dự án: INV-2024-001             │
│ Tên dự án: Dự án ABC               │
│ Loại dự án: Đầu tư                 │
│ Trạng thái: Chờ phê duyệt          │
│                                     │
│ Lý do xóa *                        │
│ [Textarea - required]              │
│                                     │
│ ⚠️ Lưu ý: Thao tác này không thể   │
│    hoàn tác!                       │
│                                     │
│ [Hủy] [Xác nhận Xóa]              │
└─────────────────────────────────────┘
```

#### 7.3 Success/Error Messages
- **Success**: "Đã xóa dự án thành công"
- **Error - No Permission**: "Bạn không có quyền xóa dự án này"
- **Error - Approved Project**: "Không thể xóa dự án đã được phê duyệt"
- **Error - System Error**: "Có lỗi xảy ra, vui lòng thử lại"

---

### 8. Yêu cầu Kiểm thử

#### 8.1 Kiểm thử Đơn vị
```typescript
describe('Xóa Dự án', () => {
    test('nên cho phép xóa dự án draft', () => {
        const project = { status: 'draft' };
        const user = { permissions: ['DELETE_PROJECT'] };
        expect(canDeleteProject(project, user)).toBe(true);
    });

    test('không nên cho phép xóa dự án đã phê duyệt', () => {
        const project = { status: 'approved' };
        const user = { permissions: ['DELETE_PROJECT'] };
        expect(canDeleteProject(project, user)).toBe(false);
    });

    test('nên soft delete dự án', async () => {
        const projectId = 1;
        const reason = 'Dự án trùng lặp';
        await deleteProject(projectId, reason);
        
        const project = await getProject(projectId);
        expect(project.status).toBe('deleted');
        expect(project.deleted_at).toBeDefined();
        expect(project.delete_reason).toBe(reason);
    });

    test('nên ghi log hành động xóa', async () => {
        const projectId = 1;
        const reason = 'Kiểm thử xóa';
        await deleteProject(projectId, reason);
        
        const logs = await getDeletionLogs(projectId);
        expect(logs).toContainEqual({
            project_id: projectId,
            delete_reason: reason
        });
    });
});
```

#### 8.2 Integration Tests
- Test Bitrix24 sync khi xóa
- Test notification system
- Test permission system
- Test soft delete functionality

#### 8.3 User Acceptance Tests
- Test delete button visibility
- Test confirmation dialog
- Test deletion workflow
- Test error handling
- Test restore functionality (admin)

---

### 9. Deployment Requirements

#### 9.1 Database Migration
```sql
-- Migration script
BEGIN;
-- Add deletion fields to projects table
ALTER TABLE projects ADD COLUMN deleted_at TIMESTAMP NULL;
ALTER TABLE projects ADD COLUMN deleted_by INT NULL;
ALTER TABLE projects ADD COLUMN delete_reason TEXT;

-- Create deletion logs table
CREATE TABLE project_deletion_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    deleted_by INT NOT NULL,
    delete_reason TEXT NOT NULL,
    project_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (deleted_by) REFERENCES users(id)
);

-- Add indexes
CREATE INDEX idx_projects_deleted ON projects(deleted_at);
CREATE INDEX idx_projects_status_deleted ON projects(status, deleted_at);

-- Create trigger
DELIMITER //
CREATE TRIGGER update_deleted_at
BEFORE UPDATE ON projects
FOR EACH ROW
BEGIN
    IF NEW.status = 'deleted' AND OLD.status != 'deleted' THEN
        SET NEW.deleted_at = CURRENT_TIMESTAMP;
    END IF;
END//
DELIMITER ;

COMMIT;
```

#### 9.2 Environment Configuration
- Soft delete settings
- Notification settings
- Permission settings
- Bitrix24 integration settings

---

### 10. Success Criteria
- [ ] User chỉ có thể xóa dự án draft/pending
- [ ] Confirmation dialog hiển thị đầy đủ thông tin
- [ ] Soft delete hoạt động chính xác
- [ ] Deletion logs được ghi đầy đủ
- [ ] Tích hợp thành công với Bitrix24
- [ ] Notification system hoạt động
- [ ] Tất cả test cases pass

---

### 11. Risks and Mitigation

#### 11.1 Technical Risks
- **Risk:** Accidental deletion of important projects
- **Mitigation:** Confirmation dialog và soft delete

- **Risk:** Data inconsistency after deletion
- **Mitigation:** Transaction-based deletion và proper cleanup

- **Risk:** Performance impact of soft delete queries
- **Mitigation:** Proper indexing và query optimization

#### 11.2 Business Risks
- **Risk:** User confusion about deletion rules
- **Mitigation:** Clear UI indicators và help documentation

- **Risk:** Loss of important project data
- **Mitigation:** Soft delete với restore functionality

---

### 12. Future Enhancements
- Bulk delete functionality
- Advanced restore options
- Deletion templates
- Automated cleanup rules
- Deletion analytics
- Advanced audit trail

---

### 13. Dependencies
- **DMDA-1.1**: Cần có danh sách dự án
- **DMDA-2.1**: Cần có tạo dự án
- **DMDA-2.2**: Cần có quản lý trạng thái dự án
- **User Management**: Cần hệ thống phân quyền
- **Notification System**: Cần hệ thống thông báo
- **Bitrix24 API**: Cần integration endpoints

---

### 14. Deletion Rules Matrix

#### 14.1 Project Status vs Deletion Permission
| Project Status | Can Delete | Button Text | Confirmation Required |
|----------------|------------|-------------|----------------------|
| Draft | Yes | "Xóa" | Yes |
| Pending Approval | Yes | "Xóa" | Yes |
| Approved | No | Hidden | N/A |
| Edit Requested | No | Hidden | N/A |
| In Progress | No | Hidden | N/A |
| Completed | No | Hidden | N/A |
| Cancelled | Yes | "Xóa" | Yes |
| Deleted | No | "Khôi phục" | Yes |

#### 14.2 User Role vs Deletion Permission
| User Role | Draft | Pending | Approved | In Progress | Completed |
|-----------|-------|---------|----------|-------------|-----------|
| Creator | Delete | Delete | No | No | No |
| Manager | Delete | Delete | No | No | No |
| Admin | Delete | Delete | No | No | No |
| Viewer | No | No | No | No | No |

#### 14.3 Deletion Workflow
```
User clicks Delete → Check Permissions → Show Confirmation → 
User confirms → Soft Delete → Update Related Data → 
Sync with Bitrix24 → Send Notifications → Log Action
```

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 2 