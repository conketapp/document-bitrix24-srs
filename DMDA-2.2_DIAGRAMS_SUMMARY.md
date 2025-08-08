# DMDA-2.2: Chỉnh sửa Dự án - Diagrams Summary

## 📋 Tổng quan
DMDA-2.2 tập trung vào chức năng chỉnh sửa dự án với workflow phức tạp dựa trên trạng thái dự án.

## 🎯 User Story
**Với vai trò là** Cán bộ khởi tạo dự án,  
**Tôi muốn** có thể chỉnh sửa tất cả các thông tin của một dự án,  
**Tùy theo trạng thái phê duyệt**,  
**Để** đảm bảo mọi thông tin được cập nhật chính xác trước khi đi vào thực hiện hoặc khi cần điều chỉnh sau phê duyệt.

## 📊 Diagrams Created

### 1. Activity Diagram
**File:** `diagrams/dmda-2.2-activity-diagram.puml`  
**Image:** `diagrams/DMDA-2.2 Activity Diagram.png`

**Mô tả luồng xử lý:**
- Kiểm tra quyền chỉnh sửa
- Phân loại theo trạng thái dự án:
  - **draft/pending_approval**: Chỉnh sửa trực tiếp
  - **approved/in_progress**: Yêu cầu chỉnh sửa
  - **edit_requested**: Chờ phê duyệt yêu cầu
  - **completed/cancelled**: Không thể chỉnh sửa

**Các bước chính:**
1. Người dùng chọn dự án cần chỉnh sửa
2. Kiểm tra quyền và trạng thái dự án
3. Hiển thị form phù hợp (chỉnh sửa trực tiếp hoặc yêu cầu)
4. Xử lý thay đổi hoặc gửi yêu cầu
5. Cập nhật database và log thay đổi

### 2. Sequence Diagram
**File:** `diagrams/dmda-2.2-sequence-diagram.puml`  
**Image:** `diagrams/DMDA-2.2 Sequence Diagram.png`

**Mô tả tương tác giữa các thành phần:**
- **User**: Người dùng thực hiện các thao tác
- **Frontend**: Giao diện người dùng
- **Backend API**: Xử lý logic nghiệp vụ
- **Database**: Lưu trữ dữ liệu
- **Approval System**: Hệ thống phê duyệt
- **Notification Service**: Gửi thông báo

**Các workflow chính:**
1. **Chỉnh sửa Dự án Trực tiếp** (draft/pending_approval)
2. **Yêu cầu Chỉnh sửa** (approved/in_progress)
3. **Phê duyệt Yêu cầu Chỉnh sửa**
4. **Từ chối Yêu cầu Chỉnh sửa**

## 🔧 Technical Implementation

### Database Schema
```sql
-- Trạng thái dự án mới
ALTER TABLE projects MODIFY COLUMN status ENUM(
    'draft', 'pending_approval', 'approved', 'edit_requested', 
    'in_progress', 'completed', 'cancelled'
) DEFAULT 'draft';

-- Bảng lưu lịch sử thay đổi
CREATE TABLE project_change_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    action_type ENUM('create', 'edit', 'edit_request', 'approve_edit', 'reject_edit'),
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints
```
GET /api/projects/{id}/edit
PUT /api/projects/{id}
POST /api/projects/{id}/edit-request
GET /api/projects/{id}/edit-requests
PUT /api/projects/{id}/edit-requests/{request_id}/approve
PUT /api/projects/{id}/edit-requests/{request_id}/reject
GET /api/projects/{id}/change-history
```

### Business Rules
- Chỉ người tạo dự án hoặc người được phân quyền mới có thể chỉnh sửa
- Mọi thay đổi phải được log lại với timestamp và user
- Dự án đã phê duyệt cần workflow phê duyệt yêu cầu chỉnh sửa
- Người phê duyệt yêu cầu chỉnh sửa phải có quyền "APPROVE_EDIT_REQUEST"

## 📱 UI Components
- **EditProjectButton**: Nút chỉnh sửa dự án
- **RequestEditButton**: Nút yêu cầu chỉnh sửa
- **ProjectEditForm**: Form chỉnh sửa dự án
- **EditRequestForm**: Form gửi yêu cầu chỉnh sửa
- **ChangeHistoryModal**: Modal xem lịch sử thay đổi
- **ApprovalWorkflow**: Workflow phê duyệt yêu cầu

## 🔄 Integration
- **Bitrix24 Integration**: Sync thay đổi dự án với Bitrix24
- **Notification System**: Email và in-app notifications
- **Audit Trail**: Log mọi thay đổi cho compliance

## ✅ Acceptance Criteria
- [x] Khi dự án chưa được phê duyệt: Người dùng có thể trực tiếp chỉnh sửa
- [x] Nút "Chỉnh sửa" hiển thị rõ ràng trên giao diện
- [x] Khi dự án đã được phê duyệt: Hệ thống hiển thị nút "Yêu cầu chỉnh sửa"
- [x] Khi người dùng gửi yêu cầu, dự án chuyển sang trạng thái "Đã gửi yêu cầu chỉnh sửa"
- [x] Sau khi được người có thẩm quyền phê duyệt yêu cầu: Người gửi mới được chỉnh sửa thông tin
- [x] Mọi thay đổi phải được ghi lại trong log lịch sử dự án
- [x] Nếu từ chối, hệ thống thông báo lý do và không cho chỉnh sửa

## 📈 Performance Requirements
- Thời gian mở form chỉnh sửa < 2 giây
- Thời gian lưu thay đổi < 3 giây
- Real-time validation không lag
- Log history load < 1 giây

---

**Status:** ✅ Completed  
**Diagrams:** Activity Diagram, Sequence Diagram  
**Integration:** SRS_Project_Category_DMDA-2.2.md
