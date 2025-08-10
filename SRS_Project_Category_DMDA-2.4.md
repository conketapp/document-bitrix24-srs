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

## User Story: DMDA-2.4
### Dừng Thực hiện Dự án

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-2.4
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-2.1, DMDA-2.2 (Cần có danh sách dự án và quản lý trạng thái)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** có thể dừng thực hiện một dự án đã được phê duyệt,  
**Để** dự án chuyển sang trạng thái "DỪNG THỰC HIỆN" khi không còn cần thiết hoặc không thể tiếp tục thực hiện.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Nút "Dừng thực hiện" chỉ hiển thị cho dự án có trạng thái "Đã phê duyệt" hoặc "Đang thực hiện"
- [ ] Có hộp thoại xác nhận trước khi dừng thực hiện
- [ ] User phải nhập lý do dừng thực hiện (bắt buộc)
- [ ] Dự án chuyển sang trạng thái "DỪNG THỰC HIỆN" sau khi xác nhận
- [ ] Ghi log thay đổi trạng thái vào lịch sử dự án
- [ ] Thông báo cho stakeholders về việc dừng dự án
- [ ] Đồng bộ trạng thái với Bitrix24

#### 2.4 Activity Diagram
![DMDA-2.4 Activity Diagram](diagrams/DMDA-2.4%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý dừng thực hiện dự án theo trạng thái*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Dừng Thực hiện Dự án**
   - Chỉ cho phép dừng dự án có trạng thái: "approved", "in_progress"
   - Form xác nhận với lý do dừng thực hiện
   - Validation lý do dừng thực hiện

2. **Quản lý Trạng thái Dự án**
   - Thêm trạng thái mới: "suspended" (DỪNG THỰC HIỆN)
   - Cập nhật workflow trạng thái dự án
   - Hiển thị trạng thái rõ ràng trong UI

3. **Confirmation Dialog**
   - Hiển thị thông tin dự án cần dừng
   - Yêu cầu nhập lý do dừng thực hiện
   - Cảnh báo về tác động của việc dừng dự án

#### 3.2 Business Rules
- Chỉ người quản lý dự án hoặc người có quyền "SUSPEND_PROJECT" mới có thể dừng dự án
- Dự án đã hoàn thành không thể dừng thực hiện
- Mọi thao tác dừng dự án phải được log với lý do
- Dự án dừng thực hiện có thể được khôi phục lại (tùy chọn)

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian hiển thị confirmation dialog < 1 giây
- Thời gian cập nhật trạng thái < 3 giây
- Không ảnh hưởng đến performance của danh sách dự án

#### 4.2 Usability
- Confirmation dialog rõ ràng và dễ hiểu
- Thông báo lỗi cụ thể khi không thể dừng dự án
- Hiển thị trạng thái dừng thực hiện rõ ràng

#### 4.3 Security
- Xác thực người dùng trước khi dừng dự án
- Phân quyền theo vai trò và trạng thái dự án
- Audit trail cho mọi thao tác dừng dự án
- CSRF protection

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Cập nhật bảng projects với trạng thái mới
ALTER TABLE projects MODIFY COLUMN status ENUM(
    'draft',           -- Khởi tạo
    'pending_approval', -- Chờ phê duyệt
    'approved',        -- Đã phê duyệt
    'edit_requested',  -- Yêu cầu chỉnh sửa
    'in_progress',     -- Đang thực hiện
    'suspended',       -- DỪNG THỰC HIỆN
    'completed',       -- Hoàn thành
    'cancelled',       -- Đã hủy
    'deleted'          -- Đã xóa
) DEFAULT 'draft';

-- Bảng lưu lịch sử dừng dự án
CREATE TABLE project_suspension_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    suspended_by INT NOT NULL,
    suspension_reason TEXT NOT NULL,
    suspension_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resumed_date TIMESTAMP NULL,
    resumed_by INT NULL,
    resume_reason TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (suspended_by) REFERENCES users(id),
    FOREIGN KEY (resumed_by) REFERENCES users(id)
);

-- Thêm index cho trạng thái suspended
CREATE INDEX idx_projects_suspended ON projects(status, suspended_at);
```

#### 5.2 API Endpoints
```
POST /api/projects/{id}/suspend
- Request: { reason: string }
- Response: { success: boolean, message: string }

GET /api/projects/{id}/can-suspend
- Response: { canSuspend: boolean, reason?: string }

POST /api/projects/{id}/resume
- Request: { reason: string }
- Response: Project resumed successfully

GET /api/projects/suspended
- Response: List of suspended projects

GET /api/projects/{id}/suspension-history
- Response: List of suspension logs for project
```

#### 5.3 Data Models
```typescript
interface Project {
    id: number;
    project_code: string;
    name: string;
    status: 'initialized' | 'pending_approval' | 'approved' | 'rejected' | 'suspended' | 'edit_requested';
    suspended_at?: string;
    suspended_by?: number;
    suspension_reason?: string;
    // ... other fields
}

interface SuspendProjectRequest {
    reason: string;
}

interface SuspendProjectResponse {
    success: boolean;
    message: string;
    project_id: number;
    new_status: string;
}

interface ProjectSuspensionLog {
    id: number;
    project_id: number;
    suspended_by: number;
    suspension_reason: string;
    suspension_date: string;
    resumed_date?: string;
    resumed_by?: number;
    resume_reason?: string;
}

interface CanSuspendResponse {
    canSuspend: boolean;
    reason?: string;
    projectStatus: string;
    userPermissions: string[];
}
```

#### 5.4 Sequence Diagram
![DMDA-2.4 Sequence Diagram](diagrams/DMDA-2.4%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi dừng thực hiện dự án*

#### 5.5 UI Components
- SuspendProjectButton: Nút dừng thực hiện dự án (conditional)
- SuspendConfirmationModal: Modal xác nhận dừng dự án
- SuspensionReasonInput: Input nhập lý do dừng thực hiện
- ProjectResumeButton: Nút khôi phục dự án (tùy chọn)
- SuspendedProjectsList: Danh sách dự án đã dừng
- SuspensionHistoryModal: Modal xem lịch sử dừng dự án

---

### 6. Yêu cầu Tích hợp

#### 6.1 Tích hợp Bitrix24
- Cập nhật deal status thành "SUSPENDED" trong Bitrix24
- Đồng bộ suspension reason với custom field trong Bitrix24
- Ghi log suspension action trong Bitrix24 activity feed
- Thông báo stakeholders trong Bitrix24

#### 6.2 Hệ thống Thông báo
- Thông báo email cho stakeholders khi dự án bị dừng
- Thông báo trong ứng dụng cho project manager
- Cảnh báo cho admin về dự án bị dừng
- Thông báo SMS cho urgent suspensions (tùy chọn)

#### 6.3 Luồng Dữ liệu
1. Người dùng nhấn nút "Dừng thực hiện"
2. Hệ thống kiểm tra quyền và trạng thái dự án
3. Hiển thị confirmation dialog với thông tin dự án
4. Người dùng nhập lý do dừng thực hiện và xác nhận
5. Hệ thống xác thực và cập nhật trạng thái dự án
6. Ghi log suspension action
7. Đồng bộ với Bitrix24
8. Gửi thông báo
9. Cập nhật related data

---

### 7. Yêu cầu Giao diện Người dùng

#### 7.1 Hiển thị Nút Dừng Thực hiện
- **Draft/Pending**: Ẩn nút "Dừng thực hiện"
- **Approved/In Progress**: Hiển thị nút "Dừng thực hiện"
- **Suspended**: Hiển thị nút "Khôi phục"
- **Completed/Cancelled**: Ẩn nút "Dừng thực hiện"

#### 7.2 Confirmation Dialog Layout
```
┌─────────────────────────────────────┐
│ Xác nhận Dừng Thực hiện Dự án      │
├─────────────────────────────────────┤
│ Bạn có chắc chắn muốn dừng dự án:  │
│                                     │
│ Mã dự án: INV-2024-001             │
│ Tên dự án: Dự án ABC               │
│ Loại dự án: Đầu tư                 │
│ Trạng thái hiện tại: Đang thực hiện │
│                                     │
│ Lý do dừng thực hiện *             │
│ [Textarea - required]              │
│                                     │
│ ⚠️ Lưu ý: Dự án sẽ chuyển sang     │
│    trạng thái "DỪNG THỰC HIỆN"    │
│                                     │
│ [Hủy] [Xác nhận Dừng]             │
└─────────────────────────────────────┘
```

#### 7.3 Status Display
- **Suspended Status**: Hiển thị badge màu cam với icon "pause"
- **Suspension Date**: Hiển thị ngày dừng thực hiện
- **Suspension Reason**: Tooltip hiển thị lý do dừng

#### 7.4 Success/Error Messages
- **Success**: "Đã dừng thực hiện dự án thành công"
- **Error - No Permission**: "Bạn không có quyền dừng dự án này"
- **Error - Invalid Status**: "Không thể dừng dự án ở trạng thái này"
- **Error - System Error**: "Có lỗi xảy ra, vui lòng thử lại"

---

### 8. Yêu cầu Kiểm thử

#### 8.1 Kiểm thử Đơn vị
```typescript
describe('Dừng Thực hiện Dự án', () => {
    test('nên cho phép dừng dự án đã phê duyệt', () => {
        const project = { status: 'approved' };
        const user = { permissions: ['SUSPEND_PROJECT'] };
        expect(canSuspendProject(project, user)).toBe(true);
    });

    test('không nên cho phép dừng dự án đã hoàn thành', () => {
        const project = { status: 'completed' };
        const user = { permissions: ['SUSPEND_PROJECT'] };
        expect(canSuspendProject(project, user)).toBe(false);
    });

    test('nên dừng dự án với lý do', async () => {
        const projectId = 1;
        const reason = 'Hạn chế ngân sách';
        await suspendProject(projectId, reason);
        
        const project = await getProject(projectId);
        expect(project.status).toBe('suspended');
        expect(project.suspension_reason).toBe(reason);
        expect(project.suspended_at).toBeDefined();
    });

    test('nên ghi log hành động dừng dự án', async () => {
        const projectId = 1;
        const reason = 'Dừng thử nghiệm';
        await suspendProject(projectId, reason);
        
        const logs = await getSuspensionLogs(projectId);
        expect(logs).toContainEqual({
            project_id: projectId,
            suspension_reason: reason
        });
    });
});
```

#### 8.2 Kiểm thử Tích hợp
- Kiểm thử đồng bộ Bitrix24 khi dừng dự án
- Kiểm thử hệ thống thông báo
- Kiểm thử hệ thống phân quyền
- Kiểm thử quy trình dừng dự án

#### 8.3 Kiểm thử Chấp nhận Người dùng
- Kiểm thử hiển thị nút dừng dự án
- Kiểm thử hộp thoại xác nhận
- Kiểm thử quy trình dừng dự án
- Kiểm thử xử lý lỗi
- Kiểm thử chức năng khôi phục (tùy chọn)

---

### 9. Deployment Requirements

#### 9.1 Di chuyển Cơ sở Dữ liệu
```sql
-- Script di chuyển
BEGIN;
-- Cập nhật bảng projects với trạng thái mới
ALTER TABLE projects MODIFY COLUMN status ENUM(
    'initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested', 
    'in_progress', 'suspended', 'completed', 'cancelled', 'deleted'
) DEFAULT 'draft';

-- Thêm các trường dừng dự án
ALTER TABLE projects ADD COLUMN suspended_at TIMESTAMP NULL;
ALTER TABLE projects ADD COLUMN suspended_by INT NULL;
ALTER TABLE projects ADD COLUMN suspension_reason TEXT;

-- Tạo bảng log dừng dự án
CREATE TABLE project_suspension_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    suspended_by INT NOT NULL,
    suspension_reason TEXT NOT NULL,
    suspension_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resumed_date TIMESTAMP NULL,
    resumed_by INT NULL,
    resume_reason TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (suspended_by) REFERENCES users(id),
    FOREIGN KEY (resumed_by) REFERENCES users(id)
);

-- Thêm các index
CREATE INDEX idx_projects_suspended ON projects(status, suspended_at);
CREATE INDEX idx_suspension_logs_project ON project_suspension_logs(project_id);

COMMIT;
```

#### 9.2 Cấu hình Môi trường
- Cài đặt dừng dự án
- Cài đặt thông báo
- Cài đặt phân quyền
- Cài đặt tích hợp Bitrix24

---

### 10. Tiêu chí Thành công
- [ ] Người dùng chỉ có thể dừng dự án đã phê duyệt/đang thực hiện
- [ ] Hộp thoại xác nhận hiển thị đầy đủ thông tin
- [ ] Log dừng dự án được ghi đầy đủ
- [ ] Tích hợp thành công với Bitrix24
- [ ] Hệ thống thông báo hoạt động
- [ ] Tất cả các trường hợp kiểm thử đều thành công

---

### 11. Rủi ro và Giải pháp

#### 11.1 Rủi ro Kỹ thuật
- **Rủi ro:** Dừng nhầm các dự án quan trọng
- **Giải pháp:** Hộp thoại xác nhận và kiểm tra phân quyền

- **Rủi ro:** Dữ liệu không nhất quán sau khi dừng
- **Giải pháp:** Dừng dự án dựa trên transaction và ghi log đúng cách

- **Rủi ro:** Ảnh hưởng hiệu suất của các truy vấn dừng dự án
- **Giải pháp:** Tạo index phù hợp và tối ưu hóa truy vấn

#### 11.2 Rủi ro Kinh doanh
- **Rủi ro:** Người dùng nhầm lẫn về quy tắc dừng dự án
- **Giải pháp:** Chỉ báo UI rõ ràng và tài liệu hướng dẫn

- **Rủi ro:** Thông báo chậm cho các bên liên quan
- **Giải pháp:** Thông báo ngay lập tức và quy tắc leo thang

---

### 12. Cải tiến Tương lai
- Chức năng dừng hàng loạt
- Tùy chọn khôi phục nâng cao
- Mẫu dừng dự án
- Quy tắc dừng tự động
- Phân tích dừng dự án
- Theo dõi kiểm toán nâng cao

---

### 13. Phụ thuộc
- **DMDA-1.1**: Cần có danh sách dự án
- **DMDA-2.1**: Cần có tạo dự án
- **DMDA-2.2**: Cần có quản lý trạng thái dự án
- **Quản lý Người dùng**: Cần hệ thống phân quyền
- **Hệ thống Thông báo**: Cần hệ thống thông báo
- **Bitrix24 API**: Cần các endpoint tích hợp

---

### 14. Ma trận Quy tắc Dừng Dự án

#### 14.1 Trạng thái Dự án vs Quyền Dừng
| Trạng thái Dự án | Có thể Dừng | Văn bản Nút | Yêu cầu Xác nhận |
|------------------|-------------|-------------|------------------|
| Khởi tạo | Không | Ẩn | Không áp dụng |
| Chờ phê duyệt | Không | Ẩn | Không áp dụng |
| Đã phê duyệt | Có | "Dừng thực hiện" | Có |
| Yêu cầu chỉnh sửa | Không | Ẩn | Không áp dụng |
| Đang thực hiện | Có | "Dừng thực hiện" | Có |
| Dừng thực hiện | Không | "Khôi phục" | Có |
| Hoàn thành | Không | Ẩn | Không áp dụng |
| Đã hủy | Không | Ẩn | Không áp dụng |
| Đã xóa | Không | Ẩn | Không áp dụng |

#### 14.2 Vai trò Người dùng vs Quyền Dừng
| Vai trò Người dùng | Đã phê duyệt | Đang thực hiện | Dừng thực hiện | Hoàn thành |
|-------------------|---------------|----------------|----------------|------------|
| Người tạo | Dừng | Dừng | Khôi phục | Không |
| Quản lý | Dừng | Dừng | Khôi phục | Không |
| Quản trị viên | Dừng | Dừng | Khôi phục | Không |
| Người xem | Không | Không | Không | Không |

#### 14.3 Quy trình Dừng Dự án
```
Người dùng nhấn Dừng → Kiểm tra Quyền → Hiển thị Xác nhận → 
Người dùng xác nhận → Cập nhật Trạng thái → Ghi Log → 
Đồng bộ với Bitrix24 → Gửi Thông báo → Cập nhật Giao diện
```

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 2 