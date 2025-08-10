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

## User Story: DMDA-3.3
### Phê duyệt Dự án

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-3.3
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 3
- **Status:** To Do
- **Phụ thuộc:** DMDA-1.1, DMDA-3.1, DMDA-3.2 (Cần có danh sách dự án và gửi phê duyệt)

#### 2.2 Mô tả User Story
**Với vai trò là** Người Phê duyệt dự án,  
**Tôi muốn** có thể xem thông tin chi tiết của dự án và chấp thuận phê duyệt dự án đó,  
**Để** dự án có thể chuyển sang trạng thái đã được duyệt và tiến hành các bước tiếp theo.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Phê duyệt" rõ ràng trên trang chi tiết dự án
- [ ] Sau khi phê duyệt, trạng thái dự án tự động cập nhật (ví dụ: "Đã phê duyệt")
- [ ] Hệ thống ghi lại thông tin người phê duyệt và thời gian phê duyệt
- [ ] Chỉ người có quyền phê duyệt mới thấy nút "Phê duyệt"
- [ ] Có hộp thoại xác nhận trước khi phê duyệt
- [ ] Có thể nhập comment khi phê duyệt (tùy chọn)
- [ ] Thông báo thành công sau khi phê duyệt
- [ ] Ghi log hành động phê duyệt
- [ ] Đồng bộ trạng thái với Bitrix24

#### 2.4 Activity Diagram
![DMDA-3.3 Activity Diagram](diagrams/DMDA-3.3%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý phê duyệt dự án*

---
### 3. Functional Requirements

#### 3.1 Core Features
1. **Phê duyệt Dự án**
   - Chỉ cho phép phê duyệt dự án có trạng thái: "pending_approval"
   - Form xác nhận phê duyệt với comment tùy chọn
   - Validation trước khi phê duyệt
   - Confirmation dialog

2. **Quản lý Trạng thái Dự án**
   - Chuyển trạng thái từ "pending_approval" → "approved"
   - Hiển thị trạng thái "Đã phê duyệt" rõ ràng
   - Cập nhật thông tin phê duyệt

3. **Workflow Phê duyệt**
   - Xem thông tin chi tiết dự án
   - Xác nhận phê duyệt
   - Gửi notification cho project manager
   - Theo dõi lịch sử phê duyệt
   - Log toàn bộ quá trình

#### 3.2 Business Rules
- Chỉ người có quyền "APPROVE_PROJECT" mới có thể phê duyệt dự án
- Dự án đã phê duyệt không thể phê duyệt lại
- Dự án chưa được gửi phê duyệt không thể phê duyệt
- Mỗi lần phê duyệt phải ghi lại thông tin người phê duyệt và thời gian

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian hiển thị form phê duyệt < 1 giây
- Thời gian xử lý phê duyệt < 3 giây
- Load thông tin dự án < 2 giây

#### 4.2 Usability
- Form phê duyệt dễ sử dụng
- Confirmation dialog rõ ràng
- Thông báo lỗi cụ thể
- Hiển thị trạng thái phê duyệt rõ ràng

#### 4.3 Security
- Xác thực người dùng trước khi phê duyệt
- Phân quyền theo vai trò
- Audit trail cho mọi thao tác phê duyệt
- CSRF protection

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Cập nhật bảng project_approvals
ALTER TABLE project_approvals ADD COLUMN approval_notes TEXT;
ALTER TABLE project_approvals ADD COLUMN approval_date TIMESTAMP NULL;

-- Bảng lưu lịch sử phê duyệt
CREATE TABLE project_approval_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    approver_id INT NOT NULL,
    approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approval_notes TEXT,
    previous_status VARCHAR(50),
    new_status VARCHAR(50),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

-- Thêm index cho performance
CREATE INDEX idx_project_approval_history_project ON project_approval_history(project_id);
CREATE INDEX idx_project_approval_history_approver ON project_approval_history(approver_id);
```

#### 5.2 API Endpoints
```
POST /api/projects/{id}/approve
- Request: { approver_id: number, approval_notes?: string }
- Response: { success: boolean, message: string }

GET /api/projects/{id}/can-approve
- Response: { canApprove: boolean, reason?: string }

GET /api/projects/{id}/approval-details
- Response: Current approval details and history

POST /api/projects/{id}/reject
- Request: { approver_id: number, rejection_reason: string }
- Response: Project rejected successfully

GET /api/projects/pending-approval
- Response: List of projects pending approval
```

#### 5.3 Data Models
```typescript
interface Project {
    id: number;
    project_code: string;
    name: string;
    status: 'initialized' | 'pending_approval' | 'approved' | 'rejected' | 'suspended' | 'edit_requested';
    approved_at?: string;
    approved_by?: number;
    approval_notes?: string;
    // ... other fields
}

interface ApproveProjectRequest {
    approver_id: number;
    approval_notes?: string;
}

interface ApproveProjectResponse {
    success: boolean;
    message: string;
    project_id: number;
    new_status: string;
    approval_date: string;
}

interface ProjectApprovalHistory {
    id: number;
    project_id: number;
    approver_id: number;
    approval_date: string;
    approval_notes?: string;
    previous_status: string;
    new_status: string;
}

interface CanApproveResponse {
    canApprove: boolean;
    reason?: string;
    projectStatus: string;
    userPermissions: string[];
    approvalDetails?: ProjectApproval;
}
```

#### 5.4 UI Components
- ApproveProjectButton: Nút phê duyệt dự án (conditional)
- ApproveProjectModal: Modal phê duyệt dự án
- ApprovalNotesInput: Input nhập ghi chú phê duyệt
- ApprovalStatusBadge: Badge hiển thị trạng thái phê duyệt
- ApprovalHistoryModal: Modal xem lịch sử phê duyệt

#### 5.5 Sequence Diagram
![DMDA-3.3 Sequence Diagram](diagrams/DMDA-3.3%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi phê duyệt dự án*

---

### 6. Yêu cầu Tích hợp

#### 6.1 Tích hợp Bitrix24
- Cập nhật deal status thành "APPROVED" trong Bitrix24
- Đồng bộ approval notes với custom field trong Bitrix24
- Ghi log approval action trong Bitrix24 activity feed
- Thông báo stakeholders trong Bitrix24

#### 6.2 Hệ thống Thông báo
- Thông báo email cho project manager khi dự án được phê duyệt
- Thông báo trong ứng dụng cho người tạo dự án
- Thông báo cho admin về dự án đã được phê duyệt
- Thông báo SMS cho urgent approvals (tùy chọn)

#### 6.3 Luồng Dữ liệu
1. Người phê duyệt truy cập trang chi tiết dự án
2. Hệ thống kiểm tra quyền phê duyệt và trạng thái dự án
3. Hiển thị nút "Phê duyệt" nếu có quyền
4. Người phê duyệt nhấn "Phê duyệt" và nhập comment (tùy chọn)
5. Hệ thống xác thực và cập nhật trạng thái dự án
6. Ghi log approval action
7. Đồng bộ với Bitrix24
8. Gửi thông báo
9. Cập nhật related data

---

### 7. Yêu cầu Giao diện Người dùng

#### 7.1 Hiển thị Nút Phê duyệt
- **Pending Approval**: Hiển thị nút "Phê duyệt"
- **Approved**: Hiển thị badge "Đã phê duyệt"
- **Draft/Edit Requested**: Ẩn nút "Phê duyệt"
- **In Progress/Completed**: Ẩn nút "Phê duyệt"

#### 7.2 Confirmation Dialog Layout
```
┌─────────────────────────────────────┐
│ Xác nhận Phê duyệt Dự án           │
├─────────────────────────────────────┤
│ Bạn có chắc chắn muốn phê duyệt:   │
│                                     │
│ Mã dự án: INV-2024-001             │
│ Tên dự án: Dự án ABC               │
│ Loại dự án: Đầu tư                 │
│ Trạng thái hiện tại: Chờ phê duyệt │
│                                     │
│ Ghi chú phê duyệt (tùy chọn)       │
│ [Textarea]                         │
│                                     │
│ ⚠️ Lưu ý: Dự án sẽ chuyển sang     │
│    trạng thái "Đã phê duyệt"       │
│                                     │
│ [Hủy] [Phê duyệt]                  │
└─────────────────────────────────────┘
```

#### 7.3 Status Display
- **Approved Status**: Hiển thị badge màu xanh với icon "check"
- **Approval Date**: Hiển thị ngày phê duyệt
- **Approver Name**: Hiển thị tên người phê duyệt
- **Approval Notes**: Tooltip hiển thị ghi chú phê duyệt

#### 7.4 Success/Error Messages
- **Success**: "Đã phê duyệt dự án thành công"
- **Error - No Permission**: "Bạn không có quyền phê duyệt dự án này"
- **Error - Invalid Status**: "Không thể phê duyệt dự án ở trạng thái này"
- **Error - System Error**: "Có lỗi xảy ra, vui lòng thử lại"

---

### 8. Yêu cầu Kiểm thử

#### 8.1 Kiểm thử Đơn vị
```typescript
describe('Phê duyệt Dự án', () => {
    test('nên cho phép phê duyệt dự án đang chờ phê duyệt', () => {
        const project = { status: 'pending_approval' };
        const user = { permissions: ['APPROVE_PROJECT'] };
        expect(canApproveProject(project, user)).toBe(true);
    });

    test('không nên cho phép phê duyệt dự án đã phê duyệt', () => {
        const project = { status: 'approved' };
        const user = { permissions: ['APPROVE_PROJECT'] };
        expect(canApproveProject(project, user)).toBe(false);
    });

    test('nên phê duyệt dự án với ghi chú', async () => {
        const projectId = 1;
        const approverId = 2;
        const notes = 'Dự án đáp ứng đầy đủ yêu cầu';
        await approveProject(projectId, approverId, notes);
        
        const project = await getProject(projectId);
        expect(project.status).toBe('approved');
        expect(project.approval_notes).toBe(notes);
        expect(project.approved_at).toBeDefined();
    });

    test('nên ghi log hành động phê duyệt', async () => {
        const projectId = 1;
        const approverId = 2;
        await approveProject(projectId, approverId);
        
        const logs = await getApprovalLogs(projectId);
        expect(logs).toContainEqual({
            project_id: projectId,
            approver_id: approverId,
            new_status: 'approved'
        });
    });
});
```

#### 8.2 Kiểm thử Tích hợp
- Kiểm thử đồng bộ Bitrix24 khi phê duyệt dự án
- Kiểm thử hệ thống thông báo
- Kiểm thử hệ thống phân quyền
- Kiểm thử quy trình phê duyệt

#### 8.3 Kiểm thử Chấp nhận Người dùng
- Kiểm thử hiển thị nút phê duyệt
- Kiểm thử hộp thoại xác nhận
- Kiểm thử quy trình phê duyệt
- Kiểm thử xử lý lỗi
- Kiểm thử hiển thị trạng thái phê duyệt

---

### 9. Yêu cầu Triển khai

#### 9.1 Di chuyển Cơ sở Dữ liệu
```sql
-- Script di chuyển
BEGIN;
-- Cập nhật bảng project_approvals
ALTER TABLE project_approvals ADD COLUMN approval_notes TEXT;
ALTER TABLE project_approvals ADD COLUMN approval_date TIMESTAMP NULL;

-- Tạo bảng lịch sử phê duyệt
CREATE TABLE project_approval_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    approver_id INT NOT NULL,
    approval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approval_notes TEXT,
    previous_status VARCHAR(50),
    new_status VARCHAR(50),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (approver_id) REFERENCES users(id)
);

-- Thêm các index
CREATE INDEX idx_project_approval_history_project ON project_approval_history(project_id);
CREATE INDEX idx_project_approval_history_approver ON project_approval_history(approver_id);

COMMIT;
```

#### 9.2 Cấu hình Môi trường
- Cài đặt phê duyệt
- Cài đặt thông báo
- Cài đặt phân quyền
- Cài đặt tích hợp Bitrix24

---

### 10. Tiêu chí Thành công
- [ ] Người dùng chỉ có thể phê duyệt dự án đang chờ phê duyệt
- [ ] Hộp thoại xác nhận hiển thị đầy đủ thông tin
- [ ] Log phê duyệt được ghi đầy đủ
- [ ] Tích hợp thành công với Bitrix24
- [ ] Hệ thống thông báo hoạt động
- [ ] Tất cả các trường hợp kiểm thử đều thành công

---

### 11. Rủi ro và Giải pháp

#### 11.1 Rủi ro Kỹ thuật
- **Rủi ro:** Phê duyệt nhầm các dự án quan trọng
- **Giải pháp:** Hộp thoại xác nhận và kiểm tra phân quyền

- **Rủi ro:** Dữ liệu không nhất quán sau khi phê duyệt
- **Giải pháp:** Phê duyệt dựa trên transaction và ghi log đúng cách

- **Rủi ro:** Ảnh hưởng hiệu suất của các truy vấn phê duyệt
- **Giải pháp:** Tạo index phù hợp và tối ưu hóa truy vấn

#### 11.2 Rủi ro Kinh doanh
- **Rủi ro:** Người dùng nhầm lẫn về quy tắc phê duyệt
- **Giải pháp:** Chỉ báo UI rõ ràng và tài liệu hướng dẫn

- **Rủi ro:** Thông báo chậm cho các bên liên quan
- **Giải pháp:** Thông báo ngay lập tức và quy tắc leo thang

---

### 12. Cải tiến Tương lai
- Phê duyệt nhiều cấp
- Phê duyệt có điều kiện
- Mẫu phê duyệt
- Quy tắc phê duyệt tự động
- Phân tích phê duyệt
- Theo dõi phê duyệt nâng cao

---

### 13. Phụ thuộc
- **DMDA-1.1**: Cần có danh sách dự án
- **DMDA-3.1**: Cần có gửi phê duyệt đơn lẻ
- **DMDA-3.2**: Cần có gửi phê duyệt hàng loạt
- **Quản lý Người dùng**: Cần hệ thống phân quyền
- **Hệ thống Thông báo**: Cần hệ thống thông báo
- **Bitrix24 API**: Cần các endpoint tích hợp

---

### 14. Ma trận Quy tắc Phê duyệt

#### 14.1 Trạng thái Dự án vs Quyền Phê duyệt
| Trạng thái Dự án | Có thể Phê duyệt | Văn bản Nút | Yêu cầu Xác nhận |
|------------------|------------------|-------------|------------------|
| Khởi tạo | Không | Ẩn | Không áp dụng |
| Chờ phê duyệt | Có | "Phê duyệt" | Có |
| Đã phê duyệt | Không | "Đã phê duyệt" | Không áp dụng |
| Yêu cầu chỉnh sửa | Không | Ẩn | Không áp dụng |
| Đang thực hiện | Không | Ẩn | Không áp dụng |
| Dừng thực hiện | Không | Ẩn | Không áp dụng |
| Hoàn thành | Không | Ẩn | Không áp dụng |
| Đã hủy | Không | Ẩn | Không áp dụng |

#### 14.2 Vai trò Người dùng vs Quyền Phê duyệt
| Vai trò Người dùng | Chờ phê duyệt | Đã phê duyệt | Đang thực hiện |
|-------------------|----------------|--------------|----------------|
| Người phê duyệt | Phê duyệt | Xem | Xem |
| Quản lý | Xem | Xem | Xem |
| Quản trị viên | Phê duyệt | Xem | Xem |
| Người xem | Xem | Xem | Xem |

#### 14.3 Quy trình Phê duyệt
```
Người phê duyệt truy cập → Kiểm tra Quyền → Hiển thị Nút Phê duyệt → 
Người phê duyệt xác nhận → Cập nhật Trạng thái → Ghi Log → 
Đồng bộ với Bitrix24 → Gửi Thông báo → Cập nhật Giao diện
```

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 3
