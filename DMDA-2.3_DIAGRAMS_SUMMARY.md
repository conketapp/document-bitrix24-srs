# DMDA-2.3: Xóa Dự án - Diagrams Summary

## 📋 Tổng quan
DMDA-2.3 tập trung vào chức năng xóa dự án với điều kiện nghiêm ngặt và soft delete implementation.

## 🎯 User Story
**Với vai trò là** Cán bộ khởi tạo dự án,  
**Tôi muốn** có thể xóa một dự án khỏi danh mục,  
**Chỉ khi dự án đó chưa được phê duyệt**,  
**Để** tôi có thể loại bỏ các dự án bị trùng lặp, sai sót hoặc không còn cần thiết.

## 📊 Diagrams Created

### 1. Activity Diagram
**File:** `diagrams/dmda-2.3-activity-diagram.puml`  
**Image:** `diagrams/DMDA-2.3 Activity Diagram.png`

**Mô tả luồng xử lý:**
- Kiểm tra quyền xóa dự án
- Phân loại theo trạng thái dự án:
  - **draft/pending_approval**: Cho phép xóa với confirmation dialog
  - **approved/in_progress/completed**: Không thể xóa
  - **suspended/cancelled/deleted**: Đã bị dừng/hủy/xóa

**Các bước chính:**
1. Người dùng chọn dự án cần xóa
2. Kiểm tra quyền và trạng thái dự án
3. Hiển thị confirmation dialog với thông tin dự án
4. Yêu cầu nhập lý do xóa
5. Thực hiện soft delete
6. Cập nhật database và đồng bộ với Bitrix24
7. Gửi thông báo và log thay đổi

### 2. Sequence Diagram
**File:** `diagrams/dmda-2.3-sequence-diagram.puml`  
**Image:** `diagrams/DMDA-2.3 Sequence Diagram.png`

**Mô tả tương tác giữa các thành phần:**
- **User**: Người dùng thực hiện các thao tác
- **Frontend**: Giao diện người dùng
- **Backend API**: Xử lý logic nghiệp vụ
- **Database**: Lưu trữ dữ liệu
- **Bitrix24**: Đồng bộ dữ liệu
- **Notification Service**: Gửi thông báo

**Các workflow chính:**
1. **Kiểm tra Quyền và Trạng thái**
2. **Quy trình Xóa Dự án** với soft delete
3. **Xử lý Lỗi** cho các trường hợp không thể xóa
4. **Undo Functionality** (tùy chọn, trong 30 giây)

## 🔧 Technical Implementation

### Database Schema
```sql
-- Thêm trường cho soft delete
ALTER TABLE projects ADD COLUMN deleted_at TIMESTAMP NULL;
ALTER TABLE projects ADD COLUMN deleted_by INT NULL;
ALTER TABLE projects ADD COLUMN delete_reason TEXT;

-- Thêm index cho soft delete
CREATE INDEX idx_projects_deleted ON projects(deleted_at);
```

### API Endpoints
```
DELETE /api/projects/{id}
- Request: { delete_reason: string }
- Response: Project deleted successfully

POST /api/projects/{id}/restore
- Response: Project restored successfully

GET /api/projects/{id}/can-delete
- Response: { canDelete: boolean, reason?: string }
```

### Business Rules
- Chỉ người tạo dự án hoặc người có quyền "DELETE_PROJECT" mới có thể xóa
- Dự án đã phê duyệt không thể xóa (chỉ có thể hủy)
- Mọi thao tác xóa phải được log với lý do
- Xóa dự án sẽ xóa tất cả related data (edit requests, change logs)

## 📱 UI Components
- **DeleteProjectButton**: Nút xóa dự án (conditional)
- **DeleteConfirmationModal**: Modal xác nhận xóa
- **DeleteReasonInput**: Input nhập lý do xóa
- **ProjectRestoreButton**: Nút khôi phục dự án (admin)
- **DeletedProjectsList**: Danh sách dự án đã xóa (admin)

## 🔄 Integration
- **Bitrix24 Integration**: Soft delete deal/lead trong Bitrix24
- **Notification System**: Email và in-app notifications
- **Audit Trail**: Log mọi thao tác xóa cho compliance

## ✅ Acceptance Criteria
- [x] Nút "Xóa" chỉ hiển thị cho dự án chưa được phê duyệt
- [x] Có hộp thoại xác nhận trước khi xóa
- [x] Hiển thị thông tin dự án trong hộp thoại xác nhận
- [x] Sau khi xóa, dự án không còn hiển thị trong danh sách
- [x] Thông báo thành công sau khi xóa
- [x] Ghi log xóa dự án vào lịch sử hệ thống
- [x] Đồng bộ xóa dự án với Bitrix24

## 📈 Performance Requirements
- Thời gian hiển thị confirmation dialog < 1 giây
- Thời gian xóa dự án < 3 giây
- Không ảnh hưởng đến performance của danh sách dự án

---

**Status:** ✅ Completed  
**Diagrams:** Activity Diagram, Sequence Diagram  
**Integration:** SRS_Project_Category_DMDA-2.3.md
