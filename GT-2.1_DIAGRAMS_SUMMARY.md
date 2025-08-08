# GT-2.1: Chỉnh sửa thông tin Gói thầu - Diagrams Summary

## 📋 Tổng quan
GT-2.1 tập trung vào chức năng chỉnh sửa thông tin gói thầu với quản lý thay đổi và audit trail.

## 🎯 User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể chỉnh sửa tất cả các thông tin của một gói thầu đã tạo,  
**Để** tôi có thể cập nhật hoặc sửa chữa các thông tin sai sót hoặc thay đổi trong quá trình quản lý gói thầu.

## 📊 Diagrams Created

### 1. Activity Diagram
**File:** `diagrams/gt-2.1-activity-diagram.puml`  
**Image:** `diagrams/GT-2.1 Activity Diagram.png`

**Mô tả luồng xử lý:**
- Kiểm tra quyền chỉnh sửa gói thầu
- Mở form chỉnh sửa với thông tin hiện tại
- Chỉnh sửa các trường thông tin
- Validation real-time
- Kiểm tra thay đổi quan trọng
- Lưu thay đổi và tạo log
- Thông báo cho stakeholders

**Các bước chính:**
1. Người dùng truy cập trang chi tiết gói thầu
2. Kiểm tra quyền chỉnh sửa gói thầu
3. Hiển thị nút "Chỉnh sửa" (nếu có quyền)
4. Mở form chỉnh sửa với thông tin hiện tại
5. Người dùng chỉnh sửa thông tin
6. Validation real-time
7. Kiểm tra thay đổi quan trọng
8. Lưu thay đổi và tạo log
9. Gửi thông báo cho stakeholders

### 2. Sequence Diagram
**File:** `diagrams/gt-2.1-sequence-diagram.puml`  
**Image:** `diagrams/GT-2.1 Sequence Diagram.png`

**Mô tả tương tác giữa các thành phần:**
- **User**: Người dùng thực hiện các thao tác
- **Frontend**: Giao diện người dùng
- **Backend API**: Xử lý logic nghiệp vụ
- **Database**: Lưu trữ dữ liệu
- **Notification Service**: Gửi thông báo
- **Audit Service**: Ghi log audit trail

**Các workflow chính:**
1. **Khởi tạo Form Chỉnh sửa** với thông tin hiện tại
2. **Chỉnh sửa Thông tin** với validation real-time
3. **Lưu Thay đổi** với kiểm tra thay đổi quan trọng
4. **Lịch sử Thay đổi** để xem lịch sử chỉnh sửa
5. **Hoàn tác Thay đổi** trong 24h
6. **Xử lý Lỗi** cho các trường hợp không hợp lệ

## 🔧 Technical Implementation

### Database Schema
```sql
-- Bảng lịch sử thay đổi gói thầu
CREATE TABLE tender_package_changes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type ENUM('update', 'delete', 'restore') NOT NULL,
    change_reason TEXT,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approved_by INT,
    approved_at TIMESTAMP NULL,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng cấu hình quyền chỉnh sửa
CREATE TABLE edit_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    can_edit BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_role_id INT
);
```

### API Endpoints
```
# Tender Package Edit
GET /api/tender-packages/{id}/edit
PUT /api/tender-packages/{id}
PUT /api/tender-packages/{id}/confirm-important-changes
GET /api/tender-packages/{id}/changes
POST /api/tender-packages/{id}/rollback
```

### Business Rules
- Mã gói thầu không thể chỉnh sửa sau khi tạo
- Một số trường yêu cầu approval khi thay đổi
- Thay đổi quan trọng cần thông báo cho stakeholders
- Lưu lịch sử tất cả thay đổi
- Rollback được phép trong 24h sau khi thay đổi

## 📱 UI Components
- **EditButton**: Nút chỉnh sửa gói thầu
- **TenderPackageEditForm**: Form chỉnh sửa thông tin
- **ChangeHistoryModal**: Modal xem lịch sử thay đổi
- **RollbackButton**: Nút hoàn tác thay đổi
- **ImportantChangeWarning**: Cảnh báo thay đổi quan trọng
- **ConfirmationDialog**: Dialog xác nhận thay đổi

## 🔄 Integration
- **Permission Control**: Kiểm tra quyền chỉnh sửa theo role
- **Change Management**: Track tất cả thay đổi với version history
- **Notification System**: Thông báo cho stakeholders khi có thay đổi quan trọng
- **Audit Trail**: Log mọi thay đổi cho compliance
- **Rollback System**: Hoàn tác thay đổi trong 24h

## ✅ Acceptance Criteria
- [x] Có nút/chức năng "Chỉnh sửa" trên trang chi tiết gói thầu hoặc trong danh sách
- [x] Form chỉnh sửa hiển thị tất cả thông tin hiện tại của gói thầu
- [x] Người dùng có thể chỉnh sửa tất cả các trường thông tin (trừ mã gói thầu)
- [x] Có validation cho các trường bắt buộc và format dữ liệu
- [x] Có thể lưu nháp hoặc lưu hoàn thành
- [x] Hiển thị lịch sử thay đổi thông tin gói thầu
- [x] Có thể hoàn tác thay đổi trong một khoảng thời gian nhất định
- [x] Thông báo cho các bên liên quan khi có thay đổi quan trọng

## 📈 Performance Requirements
- Thời gian tải form chỉnh sửa < 2 giây
- Thời gian lưu thay đổi < 3 giây
- Real-time validation không lag
- Thời gian hiển thị lịch sử thay đổi < 1 giây

---

**Status:** ✅ Completed  
**Diagrams:** Activity Diagram, Sequence Diagram  
**Integration:** SRS_Project_Category_GT-2.1.md
