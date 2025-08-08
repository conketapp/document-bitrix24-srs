# DMDA-2.4: Dừng Thực hiện Dự án - Diagrams Summary

## 📋 Tổng quan
DMDA-2.4 tập trung vào chức năng dừng thực hiện dự án với điều kiện nghiêm ngặt và khả năng khôi phục.

## 🎯 User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** có thể dừng thực hiện một dự án đã được phê duyệt,  
**Để** dự án chuyển sang trạng thái "DỪNG THỰC HIỆN" khi không còn cần thiết hoặc không thể tiếp tục thực hiện.

## 📊 Diagrams Created

### 1. Activity Diagram
**File:** `diagrams/dmda-2.4-activity-diagram.puml`  
**Image:** `diagrams/DMDA-2.4 Activity Diagram.png`

**Mô tả luồng xử lý:**
- Kiểm tra quyền dừng dự án
- Phân loại theo trạng thái dự án:
  - **approved/in_progress**: Cho phép dừng thực hiện với confirmation dialog
  - **draft/pending_approval**: Không thể dừng (chưa được phê duyệt)
  - **completed**: Không thể dừng (đã hoàn thành)
  - **suspended**: Đã dừng thực hiện
  - **cancelled/deleted**: Đã bị hủy/xóa

**Các bước chính:**
1. Người dùng chọn dự án cần dừng thực hiện
2. Kiểm tra quyền và trạng thái dự án
3. Hiển thị confirmation dialog với thông tin dự án
4. Yêu cầu nhập lý do dừng thực hiện
5. Cập nhật trạng thái dự án thành "suspended"
6. Ghi log thay đổi và thông báo cho stakeholders
7. Đồng bộ trạng thái với Bitrix24

### 2. Sequence Diagram
**File:** `diagrams/dmda-2.4-sequence-diagram.puml`  
**Image:** `diagrams/DMDA-2.4 Sequence Diagram.png`

**Mô tả tương tác giữa các thành phần:**
- **User**: Người dùng thực hiện các thao tác
- **Frontend**: Giao diện người dùng
- **Backend API**: Xử lý logic nghiệp vụ
- **Database**: Lưu trữ dữ liệu
- **Bitrix24**: Đồng bộ dữ liệu
- **Notification Service**: Gửi thông báo

**Các workflow chính:**
1. **Kiểm tra Quyền và Trạng thái**
2. **Quy trình Dừng Thực hiện Dự án**
3. **Xử lý Lỗi** cho các trường hợp không thể dừng
4. **Khôi phục Dự án** (tùy chọn)

## 🔧 Technical Implementation

### Database Schema
```sql
-- Cập nhật bảng projects với trạng thái mới
ALTER TABLE projects MODIFY COLUMN status ENUM(
    'draft', 'pending_approval', 'approved', 'edit_requested', 
    'in_progress', 'suspended', 'completed', 'cancelled'
) DEFAULT 'draft';

-- Thêm trường cho suspension
ALTER TABLE projects ADD COLUMN suspended_at TIMESTAMP NULL;
ALTER TABLE projects ADD COLUMN suspended_by INT NULL;
ALTER TABLE projects ADD COLUMN suspend_reason TEXT;
```

### API Endpoints
```
PUT /api/projects/{id}/suspend
- Request: { suspend_reason: string }
- Response: Project suspended successfully

PUT /api/projects/{id}/resume
- Response: Project resumed successfully

GET /api/projects/{id}/can-suspend
- Response: { canSuspend: boolean, reason?: string }
```

### Business Rules
- Chỉ người quản lý dự án hoặc người có quyền "SUSPEND_PROJECT" mới có thể dừng dự án
- Dự án đã hoàn thành không thể dừng thực hiện
- Mọi thao tác dừng dự án phải được log với lý do
- Dự án dừng thực hiện có thể được khôi phục lại (tùy chọn)

## 📱 UI Components
- **SuspendProjectButton**: Nút dừng thực hiện dự án (conditional)
- **SuspendConfirmationModal**: Modal xác nhận dừng dự án
- **SuspensionReasonInput**: Input nhập lý do dừng thực hiện
- **ProjectResumeButton**: Nút khôi phục dự án (tùy chọn)
- **SuspendedProjectsList**: Danh sách dự án đã dừng
- **SuspensionHistoryModal**: Modal xem lịch sử dừng dự án

## 🔄 Integration
- **Bitrix24 Integration**: Update deal status thành "SUSPENDED" trong Bitrix24
- **Notification System**: Email và in-app notifications cho stakeholders
- **Audit Trail**: Log mọi thao tác dừng dự án cho compliance

## ✅ Acceptance Criteria
- [x] Nút "Dừng thực hiện" chỉ hiển thị cho dự án đã phê duyệt hoặc đang thực hiện
- [x] Có hộp thoại xác nhận trước khi dừng thực hiện
- [x] User phải nhập lý do dừng thực hiện (bắt buộc)
- [x] Dự án chuyển sang trạng thái "DỪNG THỰC HIỆN" sau khi xác nhận
- [x] Ghi log thay đổi trạng thái vào lịch sử dự án
- [x] Thông báo cho stakeholders về việc dừng dự án
- [x] Đồng bộ trạng thái với Bitrix24

## 📈 Performance Requirements
- Thời gian hiển thị confirmation dialog < 1 giây
- Thời gian cập nhật trạng thái < 3 giây
- Không ảnh hưởng đến performance của danh sách dự án

---

**Status:** ✅ Completed  
**Diagrams:** Activity Diagram, Sequence Diagram  
**Integration:** SRS_Project_Category_DMDA-2.4.md
