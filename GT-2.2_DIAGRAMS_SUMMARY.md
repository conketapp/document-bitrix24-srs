# GT-2.2: Xóa Gói thầu - Diagrams Summary

## 📋 Tổng quan
GT-2.2 tập trung vào chức năng xóa gói thầu với kiểm tra dependencies và soft delete.

## 🎯 User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể xóa một gói thầu khỏi danh mục,  
**Để** tôi có thể loại bỏ các gói thầu bị trùng lặp, sai sót hoặc không còn cần thiết.

## 📊 Diagrams Created

### 1. Activity Diagram
**File:** `diagrams/gt-2.2-activity-diagram.puml`  
**Image:** `diagrams/GT-2.2 Activity Diagram.png`

**Mô tả luồng xử lý:**
- Kiểm tra quyền xóa gói thầu
- Kiểm tra trạng thái gói thầu
- Kiểm tra dependencies (hợp đồng, tài liệu, workflow)
- Hiển thị confirmation dialog
- Thực hiện soft delete
- Ghi log và gửi thông báo

**Các bước chính:**
1. Người dùng chọn gói thầu cần xóa
2. Kiểm tra quyền xóa gói thầu
3. Kiểm tra trạng thái gói thầu (chỉ cho phép draft/cancelled)
4. Kiểm tra dependencies (hợp đồng, tài liệu, workflow)
5. Hiển thị confirmation dialog với thông tin chi tiết
6. Yêu cầu nhập lý do xóa
7. Thực hiện soft delete
8. Ghi log và gửi thông báo

### 2. Sequence Diagram
**File:** `diagrams/gt-2.2-sequence-diagram.puml`  
**Image:** `diagrams/GT-2.2 Sequence Diagram.png`

**Mô tả tương tác giữa các thành phần:**
- **User**: Người dùng thực hiện các thao tác
- **Frontend**: Giao diện người dùng
- **Backend API**: Xử lý logic nghiệp vụ
- **Database**: Lưu trữ dữ liệu
- **Audit Service**: Ghi log audit trail
- **Notification Service**: Gửi thông báo

**Các workflow chính:**
1. **Kiểm tra Quyền và Trạng thái** trước khi xóa
2. **Kiểm tra Dependencies** (hợp đồng, tài liệu, workflow)
3. **Xác nhận Xóa** với lý do và confirmation
4. **Khôi phục Gói thầu** trong 30 ngày
5. **Bulk Delete** cho nhiều gói thầu cùng lúc
6. **Xử lý Lỗi** cho các trường hợp không thể xóa

## 🔧 Technical Implementation

### Database Schema
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
    original_data JSON
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
    warnings_shown JSON
);
```

### API Endpoints
```
# Tender Package Delete
DELETE /api/tender-packages/{id}
POST /api/tender-packages/{id}/delete
GET /api/tender-packages/{id}/delete-check
POST /api/tender-packages/{id}/restore

# Bulk Delete
POST /api/tender-packages/bulk-delete-check
DELETE /api/tender-packages/bulk
```

### Business Rules
- Chỉ users có quyền DELETE_TENDER_PACKAGE mới có thể xóa
- Không thể xóa gói thầu đã có hợp đồng liên kết
- Không thể xóa gói thầu đang trong quá trình triển khai
- Soft delete trong 30 ngày trước khi permanent delete
- Log tất cả delete operations cho audit trail

### Delete Restrictions
1. **Status-based Restrictions**
   - Không thể xóa gói thầu có status "in_progress"
   - Không thể xóa gói thầu có status "completed"
   - Chỉ có thể xóa gói thầu có status "draft" hoặc "cancelled"

2. **Dependency-based Restrictions**
   - Gói thầu có hợp đồng liên kết
   - Gói thầu có documents attached
   - Gói thầu có active workflows
   - Gói thầu có audit records

## 📱 UI Components
- **DeleteButton**: Nút xóa gói thầu
- **ConfirmationDialog**: Dialog xác nhận xóa
- **BulkDeleteButton**: Nút xóa nhiều gói thầu
- **RestoreButton**: Nút khôi phục gói thầu
- **DependencyWarning**: Cảnh báo dependencies
- **DeleteReasonInput**: Input nhập lý do xóa

## 🔄 Integration
- **Permission Control**: Kiểm tra quyền xóa theo role
- **Dependency Management**: Kiểm tra dependencies trước khi xóa
- **Soft Delete System**: Xóa mềm với khả năng khôi phục
- **Audit Trail**: Log mọi thao tác xóa cho compliance
- **Bulk Operations**: Xóa nhiều gói thầu cùng lúc

## ✅ Acceptance Criteria
- [x] Có nút/chức năng "Xóa" trên trang chi tiết gói thầu hoặc trong danh sách
- [x] Có hộp thoại xác nhận trước khi xóa để tránh thao tác nhầm lẫn
- [x] Hệ thống có thể yêu cầu quyền đặc biệt để xóa gói thầu, hoặc không cho phép xóa nếu gói thầu đã liên kết với Hợp đồng
- [x] Hiển thị thông tin chi tiết về gói thầu sẽ bị xóa trong hộp thoại xác nhận
- [x] Có thể xóa một hoặc nhiều gói thầu cùng lúc (bulk delete)
- [x] Hiển thị cảnh báo nếu gói thầu có dữ liệu liên quan
- [x] Có thể khôi phục gói thầu đã xóa trong một khoảng thời gian nhất định
- [x] Ghi log lịch sử xóa gói thầu để audit trail

## 📈 Performance Requirements
- Thời gian kiểm tra dependencies < 2 giây
- Thời gian thực hiện soft delete < 3 giây
- Thời gian bulk delete < 10 giây cho 100 gói thầu
- Thời gian khôi phục gói thầu < 2 giây

---

**Status:** ✅ Completed  
**Diagrams:** Activity Diagram, Sequence Diagram  
**Integration:** SRS_Project_Category_GT-2.2.md
