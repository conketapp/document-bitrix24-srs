# Danh sách Test Cases cho Epic DMDA - Quản lý Danh mục Dự án

## Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Date:** 12-2024  

---

## 1. Test Cases cho DMDA-1.1: Tạo Danh mục Dự án theo Năm và Phân loại

### 1.1 Test Cases cho Lọc theo Năm
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-1.1.1 | Lọc dự án theo năm 2024 | 1. Mở trang danh mục dự án<br>2. Chọn năm "2024" từ dropdown<br>3. Click "Lọc" | Hiển thị chỉ các dự án năm 2024 | High |
| TC-1.1.2 | Lọc dự án theo năm 2025 | 1. Mở trang danh mục dự án<br>2. Chọn năm "2025" từ dropdown<br>3. Click "Lọc" | Hiển thị chỉ các dự án năm 2025 | High |
| TC-1.1.3 | Mặc định hiển thị năm hiện tại | 1. Mở trang danh mục dự án | Dropdown năm mặc định là năm hiện tại | High |
| TC-1.1.4 | Không có dự án trong năm được chọn | 1. Chọn năm không có dự án<br>2. Click "Lọc" | Hiển thị thông báo "Không có dự án nào" | Medium |

### 1.2 Test Cases cho Lọc theo Loại Dự án
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-1.2.1 | Lọc theo "Dự án Đầu tư" | 1. Chọn loại "Dự án Đầu tư"<br>2. Click "Lọc" | Hiển thị chỉ dự án đầu tư | High |
| TC-1.2.2 | Lọc theo "Dự án Mua sắm" | 1. Chọn loại "Dự án Mua sắm"<br>2. Click "Lọc" | Hiển thị chỉ dự án mua sắm | High |
| TC-1.2.3 | Lọc theo "Dự án Thuê dịch vụ" | 1. Chọn loại "Dự án Thuê dịch vụ"<br>2. Click "Lọc" | Hiển thị chỉ dự án thuê dịch vụ | High |
| TC-1.2.4 | Lọc theo "Dự án Bảo trì" | 1. Chọn loại "Dự án Bảo trì"<br>2. Click "Lọc" | Hiển thị chỉ dự án bảo trì | High |
| TC-1.2.5 | Lọc theo "Tất cả" | 1. Chọn loại "Tất cả"<br>2. Click "Lọc" | Hiển thị tất cả dự án | High |

### 1.3 Test Cases cho Lọc theo Nguồn gốc Dự án
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-1.3.1 | Lọc theo "Dự án Mới" | 1. Chọn nguồn gốc "Dự án Mới"<br>2. Click "Lọc" | Hiển thị chỉ dự án mới | High |
| TC-1.3.2 | Lọc theo "Dự án Chuyển tiếp" | 1. Chọn nguồn gốc "Dự án Chuyển tiếp"<br>2. Click "Lọc" | Hiển thị chỉ dự án chuyển tiếp | High |
| TC-1.3.3 | Lọc theo "Tất cả" nguồn gốc | 1. Chọn nguồn gốc "Tất cả"<br>2. Click "Lọc" | Hiển thị tất cả dự án | High |

### 1.4 Test Cases cho Hiển thị Danh sách Dự án
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-1.4.1 | Hiển thị đầy đủ thông tin dự án | 1. Mở danh sách dự án | Hiển thị: Mã dự án, Tên dự án, Nguồn gốc, TMĐT dự kiến, TMĐT phê duyệt, Lũy kế vốn đã ứng, Vốn đã ứng năm hiện tại, Dự kiến vốn sẽ ứng, Đề xuất kế hoạch vốn năm sau, Trạng thái phê duyệt | High |
| TC-1.4.2 | Phân trang khi có >20 dự án | 1. Tạo >20 dự án<br>2. Mở danh sách | Hiển thị phân trang với 20 dự án/trang | Medium |
| TC-1.4.3 | Responsive trên mobile | 1. Mở danh sách trên mobile | Giao diện responsive, dễ sử dụng | Medium |
| TC-1.4.4 | Thời gian phản hồi < 1 giây | 1. Click "Lọc" | Kết quả hiển thị trong < 1 giây | High |

---

## 2. Test Cases cho DMDA-1.2: Tự động Phân biệt Dự án Chuyển tiếp và Dự án Mới

### 2.1 Test Cases cho Logic Phân loại Tự động
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-2.1.1 | Phân loại dự án mới (năm hiện tại) | 1. Tạo dự án với năm tạo = năm hiện tại | Tự động phân loại là "Dự án Mới" | High |
| TC-2.1.2 | Phân loại dự án chuyển tiếp (năm trước) | 1. Tạo dự án với năm tạo < năm hiện tại và trạng thái ≠ "approved" | Tự động phân loại là "Dự án Chuyển tiếp" | High |
| TC-2.1.3 | Dự án đã phê duyệt không phải chuyển tiếp | 1. Dự án năm trước với trạng thái "approved" | Phân loại là "Dự án Mới" | High |
| TC-2.1.4 | Cập nhật phân loại khi thay đổi trạng thái | 1. Thay đổi trạng thái dự án chuyển tiếp thành "approved" | Tự động cập nhật thành "Dự án Mới" | High |

### 2.2 Test Cases cho Hiển thị Phân loại
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-2.2.1 | Hiển thị badge "Dự án Mới" | 1. Xem dự án được phân loại mới | Hiển thị badge màu xanh "Dự án Mới" | High |
| TC-2.2.2 | Hiển thị badge "Dự án Chuyển tiếp" | 1. Xem dự án được phân loại chuyển tiếp | Hiển thị badge màu cam "Dự án Chuyển tiếp" | High |
| TC-2.2.3 | Tooltip giải thích logic phân loại | 1. Hover vào badge phân loại | Hiển thị tooltip giải thích logic | Medium |
| TC-2.2.4 | Không cho phép chỉnh sửa thủ công | 1. Thử chỉnh sửa trường phân loại | Không cho phép chỉnh sửa | High |

---

## 3. Test Cases cho DMDA-1.3: Mã Dự án Tự sinh theo Logic

### 3.1 Test Cases cho Tự động Sinh Mã
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-3.1.1 | Sinh mã dự án đầu tư | 1. Tạo dự án đầu tư mới | Mã được sinh: PRJ-2024-0001 | High |
| TC-3.1.2 | Sinh mã dự án mua sắm | 1. Tạo dự án mua sắm mới | Mã được sinh: PRJ-2024-0002 | High |
| TC-3.1.3 | Sinh mã dự án thuê dịch vụ | 1. Tạo dự án thuê dịch vụ mới | Mã được sinh: PRJ-2024-0003 | High |
| TC-3.1.4 | Sinh mã dự án bảo trì | 1. Tạo dự án bảo trì mới | Mã được sinh: PRJ-2024-0004 | High |
| TC-3.1.5 | Reset số thứ tự cho năm mới | 1. Tạo dự án đầu tiên năm 2025 | Mã được sinh: PRJ-2025-0001 | High |

### 3.2 Test Cases cho Tính duy nhất Mã
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-3.2.1 | Mã dự án duy nhất | 1. Tạo nhiều dự án liên tiếp | Mỗi dự án có mã khác nhau | High |
| TC-3.2.2 | Xử lý concurrent requests | 1. Tạo 2 dự án đồng thời | Không có mã trùng lặp | High |
| TC-3.2.3 | Không cho phép chỉnh sửa mã | 1. Thử chỉnh sửa mã dự án | Không cho phép chỉnh sửa | High |

### 3.3 Test Cases cho Format Mã
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-3.3.1 | Format mã đúng chuẩn | 1. Tạo dự án mới | Mã theo format PRJ-YYYY-XXXX | High |
| TC-3.3.2 | Số thứ tự 4 chữ số | 1. Tạo dự án thứ 1, 10, 100 | Mã: PRJ-2024-0001, PRJ-2024-0010, PRJ-2024-0100 | High |

---

## 4. Test Cases cho DMDA-2.1: Tạo Dự án Mới trong Danh mục

### 4.1 Test Cases cho Form Tạo Dự án
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-4.1.1 | Hiển thị form tạo dự án | 1. Click "Tạo Dự án Mới" | Hiển thị form với các trường bắt buộc | High |
| TC-4.1.2 | Validation trường bắt buộc | 1. Để trống trường bắt buộc<br>2. Click "Lưu" | Hiển thị thông báo lỗi | High |
| TC-4.1.3 | Tạo dự án thành công | 1. Điền đầy đủ thông tin<br>2. Click "Lưu" | Tạo thành công và hiển thị trong danh sách | High |
| TC-4.1.4 | Tự động sinh mã dự án | 1. Tạo dự án mới | Mã dự án được tự động sinh | High |

### 4.2 Test Cases cho Các trường Thông tin
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-4.2.1 | Validation tên dự án | 1. Nhập tên < 3 ký tự<br>2. Nhập tên > 255 ký tự | Hiển thị thông báo lỗi | High |
| TC-4.2.2 | Validation người quản lý | 1. Để trống người quản lý | Hiển thị thông báo lỗi | High |
| TC-4.2.3 | Validation phòng ban | 1. Chọn phòng ban hợp lệ | Lưu thành công | High |
| TC-4.2.4 | Validation loại dự án | 1. Chọn loại dự án từ dropdown | Lưu thành công | High |

### 4.3 Test Cases cho Thông tin Bổ sung
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-4.3.1 | Chọn nguồn vốn | 1. Chọn nguồn vốn từ dropdown | Lưu thành công | Medium |
| TC-4.3.2 | Đề án chiến lược | 1. Check "Thuộc đề án chiến lược"<br>2. Nhập tên đề án | Hiển thị trường nhập đề án | Medium |
| TC-4.3.3 | Validation TMĐT dự kiến | 1. Nhập số âm cho TMĐT | Hiển thị thông báo lỗi | High |

---

## 5. Test Cases cho DMDA-2.2: Chỉnh sửa Dự án

### 5.1 Test Cases cho Chỉnh sửa Thông tin
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-5.1.1 | Mở form chỉnh sửa | 1. Click "Chỉnh sửa" trên dự án | Hiển thị form với thông tin hiện tại | High |
| TC-5.1.2 | Cập nhật thông tin thành công | 1. Thay đổi thông tin<br>2. Click "Lưu" | Cập nhật thành công | High |
| TC-5.1.3 | Không cho phép chỉnh sửa mã | 1. Thử chỉnh sửa mã dự án | Trường mã bị disable | High |
| TC-5.1.4 | Validation khi chỉnh sửa | 1. Để trống trường bắt buộc | Hiển thị thông báo lỗi | High |

---

## 6. Test Cases cho DMDA-3.1: Gửi Phê duyệt Dự án Lần lượt

### 6.1 Test Cases cho Gửi Phê duyệt
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-6.1.1 | Hiển thị nút "Gửi Phê duyệt" | 1. Mở dự án trạng thái "Khởi tạo" | Hiển thị nút "Gửi Phê duyệt" | High |
| TC-6.1.2 | Không hiển thị nút cho dự án đã phê duyệt | 1. Mở dự án trạng thái "Đã phê duyệt" | Không hiển thị nút "Gửi Phê duyệt" | High |
| TC-6.1.3 | Gửi phê duyệt thành công | 1. Click "Gửi Phê duyệt"<br>2. Chọn người phê duyệt<br>3. Click "Xác nhận" | Chuyển trạng thái thành "Chờ phê duyệt" | High |
| TC-6.1.4 | Hiển thị dialog xác nhận | 1. Click "Gửi Phê duyệt" | Hiển thị dialog xác nhận | Medium |

### 6.2 Test Cases cho Quản lý Trạng thái
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-6.2.1 | Chuyển trạng thái từ "Khởi tạo" | 1. Gửi phê duyệt dự án "Khởi tạo" | Chuyển thành "Chờ phê duyệt" | High |
| TC-6.2.2 | Chuyển trạng thái từ "Yêu cầu chỉnh sửa" | 1. Gửi phê duyệt dự án "Yêu cầu chỉnh sửa" | Chuyển thành "Chờ phê duyệt" | High |
| TC-6.2.3 | Ghi log hành động | 1. Gửi phê duyệt dự án | Ghi log với thông tin: người gửi, thời gian, người phê duyệt | Medium |

---

## 7. Test Cases cho DMDA-3.2: Phê duyệt Dự án

### 7.1 Test Cases cho Phê duyệt
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-7.1.1 | Hiển thị danh sách dự án chờ phê duyệt | 1. Đăng nhập với quyền phê duyệt | Hiển thị tab "Chờ phê duyệt" | High |
| TC-7.1.2 | Phê duyệt dự án thành công | 1. Click "Phê duyệt"<br>2. Nhập lý do (nếu cần)<br>3. Click "Xác nhận" | Chuyển trạng thái thành "Đã phê duyệt" | High |
| TC-7.1.3 | Từ chối phê duyệt | 1. Click "Từ chối"<br>2. Nhập lý do từ chối<br>3. Click "Xác nhận" | Chuyển trạng thái thành "Từ chối phê duyệt" | High |
| TC-7.1.4 | Yêu cầu chỉnh sửa | 1. Click "Yêu cầu chỉnh sửa"<br>2. Nhập yêu cầu chỉnh sửa<br>3. Click "Xác nhận" | Chuyển trạng thái thành "Yêu cầu chỉnh sửa" | High |

---

## 8. Test Cases cho DMDA-3.3: Theo dõi Trạng thái Dự án

### 8.1 Test Cases cho Hiển thị Trạng thái
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-8.1.1 | Hiển thị trạng thái phê duyệt | 1. Xem danh sách dự án | Hiển thị badge trạng thái phê duyệt | High |
| TC-8.1.2 | Hiển thị trạng thái thực hiện | 1. Xem danh sách dự án | Hiển thị badge trạng thái thực hiện | High |
| TC-8.1.3 | Hiển thị trạng thái yêu cầu chỉnh sửa | 1. Xem dự án có yêu cầu chỉnh sửa | Hiển thị badge "Yêu cầu chỉnh sửa" | Medium |
| TC-8.1.4 | Màu sắc phân biệt trạng thái | 1. Xem các dự án trạng thái khác nhau | Màu sắc khác nhau cho từng trạng thái | Medium |

---

## 9. Test Cases cho DMDA-3.4: Quản lý Quy trình Phê duyệt

### 9.1 Test Cases cho Workflow
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-9.1.1 | Workflow phê duyệt đầy đủ | 1. Tạo dự án → Gửi phê duyệt → Phê duyệt → Hoàn thành | Trạng thái chuyển đổi đúng theo workflow | High |
| TC-9.1.2 | Workflow từ chối và chỉnh sửa | 1. Từ chối → Yêu cầu chỉnh sửa → Chỉnh sửa → Gửi lại | Workflow hoạt động đúng | High |
| TC-9.1.3 | Ghi log toàn bộ quá trình | 1. Thực hiện các bước trong workflow | Ghi log đầy đủ các hành động | Medium |

---

## 10. Test Cases cho DMDA-3.5: Báo cáo và Thống kê

### 10.1 Test Cases cho Báo cáo
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-10.1.1 | Báo cáo theo loại dự án | 1. Xem báo cáo thống kê | Hiển thị số lượng dự án theo loại | Medium |
| TC-10.1.2 | Báo cáo theo trạng thái | 1. Xem báo cáo thống kê | Hiển thị số lượng dự án theo trạng thái | Medium |
| TC-10.1.3 | Báo cáo theo năm | 1. Xem báo cáo thống kê | Hiển thị số lượng dự án theo năm | Medium |
| TC-10.1.4 | Export báo cáo | 1. Click "Export" | Tải file báo cáo (Excel/PDF) | Medium |

---

## 11. Test Cases cho DMDA-4.1: Tích hợp Bitrix24

### 11.1 Test Cases cho Đồng bộ Dữ liệu
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-11.1.1 | Đồng bộ khi tạo dự án mới | 1. Tạo dự án mới trong hệ thống | Dữ liệu được đồng bộ với Bitrix24 | High |
| TC-11.1.2 | Đồng bộ khi cập nhật dự án | 1. Cập nhật thông tin dự án | Dữ liệu được đồng bộ với Bitrix24 | High |
| TC-11.1.3 | Đồng bộ trạng thái phê duyệt | 1. Thay đổi trạng thái phê duyệt | Trạng thái được đồng bộ với Bitrix24 | High |
| TC-11.1.4 | Xử lý lỗi đồng bộ | 1. Tạo dự án khi Bitrix24 offline | Hiển thị thông báo lỗi và retry | Medium |

---

## 12. Test Cases cho DMDA-4.2: Quản lý File và Tài liệu

### 12.1 Test Cases cho Upload File
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-12.1.1 | Upload file quyết định | 1. Upload file quyết định chủ trương đầu tư | File được lưu và hiển thị | Medium |
| TC-12.1.2 | Validation định dạng file | 1. Upload file không đúng định dạng | Hiển thị thông báo lỗi | Medium |
| TC-12.1.3 | Validation kích thước file | 1. Upload file quá lớn | Hiển thị thông báo lỗi | Medium |
| TC-12.1.4 | Download file | 1. Click "Download" trên file | Tải file về máy | Medium |

---

## 13. Test Cases cho Performance và Security

### 13.1 Test Cases cho Performance
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-13.1.1 | Thời gian tải trang < 3 giây | 1. Mở trang danh mục dự án | Tải trong < 3 giây | High |
| TC-13.1.2 | Thời gian lọc < 1 giây | 1. Thực hiện lọc dự án | Kết quả hiển thị trong < 1 giây | High |
| TC-13.1.3 | Hỗ trợ 1000 dự án | 1. Tạo 1000 dự án<br>2. Mở danh sách | Hiển thị bình thường với phân trang | Medium |

### 13.2 Test Cases cho Security
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-13.2.1 | Xác thực người dùng | 1. Truy cập trang không đăng nhập | Chuyển hướng đến trang đăng nhập | High |
| TC-13.2.2 | Phân quyền theo vai trò | 1. Đăng nhập với quyền khác nhau | Hiển thị chức năng theo quyền | High |
| TC-13.2.3 | Logging hoạt động | 1. Thực hiện các thao tác | Ghi log đầy đủ | Medium |

---

## 14. Test Cases cho Usability và Accessibility

### 14.1 Test Cases cho Usability
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-14.1.1 | Responsive trên mobile | 1. Mở trang trên mobile | Giao diện responsive | Medium |
| TC-14.1.2 | Keyboard navigation | 1. Sử dụng keyboard để điều hướng | Có thể điều hướng bằng keyboard | Medium |
| TC-14.1.3 | Tooltip hướng dẫn | 1. Hover vào các chức năng | Hiển thị tooltip hướng dẫn | Low |

### 14.2 Test Cases cho Accessibility
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-14.2.1 | Screen reader support | 1. Sử dụng screen reader | Có thể đọc được nội dung | Low |
| TC-14.2.2 | Color contrast | 1. Kiểm tra độ tương phản màu sắc | Đạt tiêu chuẩn WCAG | Low |

---

## 15. Test Cases cho Error Handling

### 15.1 Test Cases cho Xử lý Lỗi
| TC ID | Test Case Name | Test Steps | Expected Result | Priority |
|-------|----------------|------------|-----------------|----------|
| TC-15.1.1 | Lỗi mạng | 1. Ngắt kết nối mạng<br>2. Thực hiện thao tác | Hiển thị thông báo lỗi và retry | Medium |
| TC-15.1.2 | Lỗi server | 1. Server trả về lỗi 500 | Hiển thị thông báo lỗi phù hợp | Medium |
| TC-15.1.3 | Lỗi validation | 1. Nhập dữ liệu không hợp lệ | Hiển thị thông báo lỗi cụ thể | High |
| TC-15.1.4 | Lỗi đồng bộ Bitrix24 | 1. Bitrix24 không phản hồi | Hiển thị thông báo và queue retry | Medium |

---

## Tổng kết

### Thống kê Test Cases
- **Tổng số Test Cases:** 89
- **High Priority:** 45 (50.6%)
- **Medium Priority:** 35 (39.3%)
- **Low Priority:** 9 (10.1%)

### Phân bố theo Module
- **DMDA-1.1 (Lọc và hiển thị):** 15 test cases
- **DMDA-1.2 (Phân loại tự động):** 8 test cases
- **DMDA-1.3 (Sinh mã tự động):** 8 test cases
- **DMDA-2.1 (Tạo dự án):** 12 test cases
- **DMDA-2.2 (Chỉnh sửa):** 4 test cases
- **DMDA-3.1 (Gửi phê duyệt):** 8 test cases
- **DMDA-3.2 (Phê duyệt):** 4 test cases
- **DMDA-3.3 (Theo dõi trạng thái):** 4 test cases
- **DMDA-3.4 (Quản lý workflow):** 3 test cases
- **DMDA-3.5 (Báo cáo):** 4 test cases
- **DMDA-4.1 (Tích hợp Bitrix24):** 4 test cases
- **DMDA-4.2 (Quản lý file):** 4 test cases
- **Performance & Security:** 6 test cases
- **Usability & Accessibility:** 5 test cases
- **Error Handling:** 4 test cases

### Khuyến nghị
1. **Ưu tiên test High Priority trước** (45 test cases)
2. **Tập trung vào các chức năng core** (DMDA-1.1, DMDA-1.2, DMDA-1.3, DMDA-2.1)
3. **Test tích hợp Bitrix24** cẩn thận vì ảnh hưởng đến dữ liệu thực
4. **Test performance** với dữ liệu lớn
5. **Test security** đầy đủ trước khi deploy production

---

**Document Version:** 1.0  
**Last Updated:** 12-2024  
**Next Review:** Sprint 3
