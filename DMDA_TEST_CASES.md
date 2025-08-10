# Test Cases - Epic DMDA: Danh mục dự án

## Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Last Updated:** 08-2024  

---

## 1. Test Cases DMDA-1.1: Xem Danh mục Dự án

### TC-DMDA-1.1-001: Hiển thị danh sách mặc định
**Steps:** Truy cập trang danh mục dự án
**Expected:** Hiển thị danh sách với bộ lọc mặc định, thời gian < 1s

### TC-DMDA-1.1-002: Lọc theo năm
**Steps:** Chọn năm "2024" → Áp dụng bộ lọc
**Expected:** Chỉ hiển thị dự án năm 2024

### TC-DMDA-1.1-003: Lọc theo loại dự án
**Steps:** Chọn "Dự án Đầu tư" → Áp dụng bộ lọc
**Expected:** Chỉ hiển thị dự án đầu tư

### TC-DMDA-1.1-004: Lọc theo trạng thái phê duyệt
**Steps:** Chọn "Đã phê duyệt" → Áp dụng bộ lọc
**Expected:** Chỉ hiển thị dự án đã phê duyệt

---

## 2. Test Cases DMDA-1.2: Phân loại Dự án

### TC-DMDA-1.2-001: Phân loại dự án mới
**Steps:** Tạo dự án năm hiện tại
**Expected:** Phân loại "Dự án Mới", có màu sắc phân biệt

### TC-DMDA-1.2-002: Phân loại dự án chuyển tiếp
**Steps:** Tạo dự án năm trước
**Expected:** Phân loại "Dự án Chuyển tiếp", có màu sắc phân biệt

---

## 3. Test Cases DMDA-1.3: Tạo Mã Dự án

### TC-DMDA-1.3-001: Tạo mã dự án đầu tiên
**Steps:** Tạo dự án mới
**Expected:** Mã format PRJ-YYYY-0001

### TC-DMDA-1.3-002: Tạo mã dự án thứ 2
**Steps:** Tạo dự án thứ 2
**Expected:** Mã format PRJ-YYYY-0002

---

## 4. Test Cases DMDA-2.1: Tạo Dự án Mới

### TC-DMDA-2.1-001: Tạo dự án thành công
**Steps:** Nhập đầy đủ thông tin → Tạo dự án
**Expected:** Dự án được tạo, trạng thái initialized

### TC-DMDA-2.1-002: Validation thông tin bắt buộc
**Steps:** Để trống trường bắt buộc → Tạo dự án
**Expected:** Hiển thị lỗi validation

---

## 5. Test Cases DMDA-2.2: Chỉnh sửa Dự án

### TC-DMDA-2.2-001: Chỉnh sửa dự án khởi tạo
**Steps:** Chỉnh sửa dự án initialized
**Expected:** Có thể chỉnh sửa trực tiếp

### TC-DMDA-2.2-002: Yêu cầu chỉnh sửa dự án đã phê duyệt
**Steps:** Click "Yêu cầu chỉnh sửa" trên dự án approved
**Expected:** Trạng thái edit_requested

---

## 6. Test Cases DMDA-2.3: Xóa Dự án

### TC-DMDA-2.3-001: Xóa dự án khởi tạo
**Steps:** Xóa dự án initialized
**Expected:** Dự án được xóa (soft delete)

### TC-DMDA-2.3-002: Không thể xóa dự án đã phê duyệt
**Steps:** Thử xóa dự án approved
**Expected:** Hiển thị thông báo lỗi

---

## 7. Test Cases DMDA-2.4: Dừng Thực hiện

### TC-DMDA-2.4-001: Dừng dự án đã phê duyệt
**Steps:** Dừng dự án approved + not_started
**Expected:** Trạng thái thực hiện = suspended

### TC-DMDA-2.4-002: Khôi phục dự án đã dừng
**Steps:** Khôi phục dự án suspended
**Expected:** Trạng thái thực hiện = in_progress

---

## 8. Test Cases DMDA-3.1: Gửi Phê duyệt

### TC-DMDA-3.1-001: Gửi phê duyệt dự án khởi tạo
**Steps:** Gửi phê duyệt dự án initialized
**Expected:** Trạng thái phê duyệt = pending_approval

### TC-DMDA-3.1-002: Không thể gửi phê duyệt dự án đã phê duyệt
**Steps:** Thử gửi phê duyệt dự án approved
**Expected:** Hiển thị thông báo lỗi

---

## 9. Test Cases DMDA-3.2: Gửi Phê duyệt Hàng loạt

### TC-DMDA-3.2-001: Chọn nhiều dự án
**Steps:** Chọn 3 dự án initialized
**Expected:** Hiển thị nút "Gửi Phê duyệt (3 dự án)"

### TC-DMDA-3.2-002: Gửi phê duyệt hàng loạt
**Steps:** Gửi phê duyệt 3 dự án
**Expected:** Tất cả 3 dự án chuyển pending_approval

---

## 10. Test Cases DMDA-3.3: Phê duyệt Dự án

### TC-DMDA-3.3-001: Phê duyệt dự án chờ phê duyệt
**Steps:** Phê duyệt dự án pending_approval
**Expected:** Trạng thái phê duyệt = approved

### TC-DMDA-3.3-002: Không thể phê duyệt dự án đã phê duyệt
**Steps:** Thử phê duyệt dự án approved
**Expected:** Hiển thị thông báo lỗi

---

## 11. Test Cases DMDA-3.5: Dự án Chính thức

### TC-DMDA-3.5-001: Hiển thị dự án chính thức
**Steps:** Lọc "Chỉ dự án chính thức"
**Expected:** Chỉ hiển thị dự án approved

### TC-DMDA-3.5-002: Thống kê dự án chính thức
**Steps:** Xem thống kê dự án chính thức
**Expected:** Số liệu chính xác

---

## 12. Test Cases DMDA-4.1: Lịch sử Thao tác

### TC-DMDA-4.1-001: Ghi log tạo dự án
**Steps:** Tạo dự án mới
**Expected:** Ghi log action_type = "project_created"

### TC-DMDA-4.1-002: Xem lịch sử hoạt động
**Steps:** Truy cập trang lịch sử
**Expected:** Hiển thị log theo thời gian

---

## 13. Test Cases DMDA-4.2: Chế độ Xem Kanban

### TC-DMDA-4.2-001: Chuyển đổi chế độ xem
**Steps:** Chuyển sang chế độ Kanban
**Expected:** Hiển thị dự án theo cột trạng thái

### TC-DMDA-4.2-002: Kéo thả dự án
**Steps:** Kéo dự án giữa các cột
**Expected:** Dự án được chuyển cột thành công

---

## 14. Test Cases DMDA-4.3: Xuất Excel

### TC-DMDA-4.3-001: Xuất toàn bộ danh sách
**Steps:** Xuất Excel toàn bộ danh sách
**Expected:** File Excel được tạo với đầy đủ thông tin

### TC-DMDA-4.3-002: Xuất theo bộ lọc
**Steps:** Xuất Excel theo bộ lọc hiện tại
**Expected:** File Excel chỉ chứa dự án thỏa mãn bộ lọc

---

## 15. Test Cases DMDA-4.5: Phân quyền

### TC-DMDA-4.5-001: Kiểm tra quyền xem
**Steps:** Truy cập dự án với quyền VIEW_PROJECT
**Expected:** Có thể xem, không thể chỉnh sửa

### TC-DMDA-4.5-002: Kiểm tra quyền chỉnh sửa
**Steps:** Truy cập dự án với quyền EDIT_INITIALIZED_PROJECT
**Expected:** Có thể chỉnh sửa dự án initialized

---

## Test Cases Tích hợp

### TC-DMDA-INT-001: Đồng bộ Bitrix24
**Steps:** Tạo dự án → Kiểm tra Bitrix24
**Expected:** Dự án được tạo trong Bitrix24

### TC-DMDA-INT-002: Đồng bộ phê duyệt
**Steps:** Phê duyệt dự án → Kiểm tra Bitrix24
**Expected:** Trạng thái được cập nhật trong Bitrix24

---

## Test Cases Hiệu suất

### TC-DMDA-PERF-001: Load danh sách lớn
**Steps:** Load 1000+ dự án
**Expected:** Thời gian < 2s

### TC-DMDA-PERF-002: Tìm kiếm
**Steps:** Tìm kiếm trong 1000+ dự án
**Expected:** Thời gian < 1s

---

## Test Cases Bảo mật

### TC-DMDA-SEC-001: Kiểm tra quyền truy cập
**Steps:** Truy cập không có quyền
**Expected:** Hiển thị lỗi 403

### TC-DMDA-SEC-002: CSRF Protection
**Steps:** Gửi request không có CSRF token
**Expected:** Request bị từ chối

---

## Tổng kết

### Thống kê
- **Tổng Test Cases:** 40+
- **High Priority:** 20+
- **Medium Priority:** 15+
- **Low Priority:** 5+

### Độ ưu tiên
1. **Critical:** DMDA-1.1, DMDA-2.1, DMDA-3.1
2. **Important:** DMDA-2.2, DMDA-3.2, DMDA-3.3
3. **Nice to have:** DMDA-4.1, DMDA-4.2, DMDA-4.3

### Môi trường Test
- **Dev:** Tất cả test cases
- **Staging:** High + Medium priority
- **Production:** High priority + Smoke test

---

**Document Version:** 1.0  
**Last Updated:** 08-2024
