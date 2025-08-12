# Bảng Validation cho Epic GT - Quản lý Gói thầu

## Tổng quan
Tài liệu này chứa các bảng validation chi tiết cho tất cả các User Stories trong Epic GT (General Tasks) - Quản lý Gói thầu.

---

## GT-1.1: Tạo Gói thầu mới

### **Bảng Validation Form Tạo Gói thầu**

#### **Thông tin Cơ bản**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Mã gói thầu | tender_code | VARCHAR(20) | Tự động sinh GT-YYYY-XXXX | ✅ | Không cho phép chỉnh sửa |
| Tên gói thầu | tender_name | VARCHAR(500) | 3-500 ký tự, không trùng lặp | ✅ | Tên mô tả gói thầu |
| Mô tả gói thầu | tender_description | TEXT | Tối đa 2000 ký tự | ❌ | Mô tả chi tiết gói thầu |
| Dự án liên quan | project_id | INT | ID hợp lệ từ bảng projects | ✅ | Chọn từ danh sách dự án |
| Hình thức lựa chọn nhà thầu | tender_method | ENUM | 'open_bidding', 'limited_bidding', 'direct_contract', 'competitive_consultation' | ✅ | Hình thức đấu thầu |

#### **Thông tin Giá trị và Ngân sách**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Giá trị dự kiến | estimated_value | DECIMAL(15,2) | > 0, định dạng tiền tệ | ✅ | Giá trị dự kiến gói thầu |
| Đơn vị tiền tệ | currency | VARCHAR(10) | VND, USD, EUR | ✅ | Mặc định VND |
| Mã TBMT | tbmt_code | VARCHAR(50) | Format: TBMT-XXXX-YYYY | ❌ | Mã thông báo mời thầu |
| Số lượng nhà thầu tham gia | participant_count | INT | >= 0 | ❌ | Số lượng nhà thầu |

#### **Thông tin Timeline**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Ngày bắt đầu dự kiến | planned_start_date | DATE | Định dạng YYYY-MM-DD | ✅ | Ngày bắt đầu dự kiến |
| Ngày kết thúc dự kiến | planned_end_date | DATE | >= planned_start_date | ✅ | Ngày kết thúc dự kiến |
| Ngày mở thầu | tender_open_date | DATE | >= planned_start_date | ❌ | Ngày mở thầu |
| Ngày đóng thầu | tender_close_date | DATE | >= tender_open_date | ❌ | Ngày đóng thầu |

#### **Thông tin Quyết định**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Quyết định phê duyệt HSMT | hsmt_approval_decision | VARCHAR(100) | Link từ Bitrix | ❌ | Quyết định phê duyệt HSMT |
| Quyết định phê duyệt KQLCNT | kqlcnt_approval_decision | VARCHAR(100) | Link từ Bitrix | ❌ | Quyết định phê duyệt KQLCNT |
| Giá trúng thầu | winning_bid_amount | DECIMAL(15,2) | > 0, <= estimated_value | ❌ | Giá trúng thầu |
| Nhà thầu trúng thầu | winning_contractor | VARCHAR(200) | Link từ Bitrix | ❌ | Nhà thầu trúng thầu |

#### **Thông tin Bổ sung**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Trạng thái gói thầu | tender_status | ENUM | 'draft', 'created', 'in_progress', 'completed', 'cancelled' | ✅ | Trạng thái hiện tại |
| Mức độ ưu tiên | priority | ENUM | 'low', 'medium', 'high', 'critical' | ✅ | Mức độ ưu tiên |
| Ghi chú | notes | TEXT | Tối đa 1000 ký tự | ❌ | Ghi chú bổ sung |
| Thẻ | tags | JSON | Mảng thẻ tối đa 10 thẻ | ❌ | Thẻ phân loại |

### **Quy tắc Validation Nghiệp vụ**

#### **Validation Cross-field**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Timeline validation | planned_start_date có giá trị | planned_end_date >= planned_start_date | "Ngày kết thúc phải sau ngày bắt đầu" |
| Tender dates | tender_open_date có giá trị | tender_close_date >= tender_open_date | "Ngày đóng thầu phải sau ngày mở thầu" |
| Project validation | project_id có giá trị | Project phải tồn tại và active | "Dự án không tồn tại hoặc không hoạt động" |
| Winning bid | winning_bid_amount có giá trị | winning_bid_amount <= estimated_value | "Giá trúng thầu không được vượt quá giá dự kiến" |

#### **Validation Business Rules**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Mã gói thầu | Tự động sinh | Format: GT-YYYY-XXXX | "Mã gói thầu được tự động sinh" |
| Tên gói thầu | Không trùng lặp | Kiểm tra trong database | "Tên gói thầu đã tồn tại" |
| TBMT code | Format validation | TBMT-XXXX-YYYY | "Mã TBMT không đúng định dạng" |
| Participant count | Số lượng hợp lệ | >= 0 | "Số lượng nhà thầu phải >= 0" |

---

## GT-1.2: Kết nối API lấy thông tin gói thầu từ Cổng thông tin đấu thầu Quốc gia

### **Bảng Validation Form Kết nối API**

#### **Thông tin Kết nối**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| URL gói thầu | tender_url | VARCHAR(500) | URL hợp lệ muasamcong.mpi.gov.vn | ✅ | URL gói thầu trên Cổng |
| Mã ID gói thầu | tender_id | VARCHAR(50) | Format: số hoặc chuỗi hợp lệ | ❌ | Mã ID gói thầu |
| API Key | api_key | VARCHAR(100) | Key hợp lệ cho API | ✅ | API key xác thực |
| Timeout | timeout | INT | 10-300 giây | ❌ | Thời gian timeout |

#### **Thông tin Xử lý**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Trạng thái kết nối | connection_status | ENUM | 'connecting', 'success', 'failed', 'timeout' | ✅ | Trạng thái kết nối |
| Thời gian kết nối | connection_time | TIMESTAMP | Tự động ghi | ✅ | Thời gian thực hiện |
| Số lần thử | retry_count | INT | 0-5 lần | ❌ | Số lần thử lại |
| Lỗi kết nối | error_message | TEXT | Tối đa 500 ký tự | ❌ | Thông báo lỗi |

### **Quy tắc Validation API**

#### **Validation URL và ID**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| URL format | URL hợp lệ | muasamcong.mpi.gov.vn domain | "URL không hợp lệ hoặc không phải Cổng thông tin đấu thầu" |
| Tender ID | ID hợp lệ | Format: số hoặc chuỗi | "Mã ID gói thầu không hợp lệ" |
| API Key | Key hợp lệ | Định dạng và độ dài | "API Key không hợp lệ" |

#### **Validation Response Data**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Response format | JSON hợp lệ | Parse được JSON | "Dữ liệu phản hồi không hợp lệ" |
| Required fields | Các trường bắt buộc | Tồn tại trong response | "Thiếu thông tin bắt buộc từ API" |
| Data mapping | Map được dữ liệu | Tương thích với form | "Không thể map dữ liệu từ API" |

---

## GT-2.1: Chỉnh sửa thông tin Gói thầu

### **Bảng Validation Form Chỉnh sửa**

#### **Thông tin Cơ bản (Có thể chỉnh sửa)**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Chỉnh sửa được |
|--------|-----------|---------------|------------|----------|----------------|
| Tên gói thầu | tender_name | VARCHAR(500) | 3-500 ký tự, không trùng lặp | ✅ | ✅ |
| Mô tả gói thầu | tender_description | TEXT | Tối đa 2000 ký tự | ❌ | ✅ |
| Dự án liên quan | project_id | INT | ID hợp lệ từ bảng projects | ✅ | ✅ |
| Hình thức lựa chọn nhà thầu | tender_method | ENUM | 'open_bidding', 'limited_bidding', 'direct_contract', 'competitive_consultation' | ✅ | ✅ |

#### **Thông tin Giá trị (Có thể chỉnh sửa)**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Chỉnh sửa được |
|--------|-----------|---------------|------------|----------|----------------|
| Giá trị dự kiến | estimated_value | DECIMAL(15,2) | > 0, định dạng tiền tệ | ✅ | ✅ |
| Mã TBMT | tbmt_code | VARCHAR(50) | Format: TBMT-XXXX-YYYY | ❌ | ✅ |
| Số lượng nhà thầu tham gia | participant_count | INT | >= 0 | ❌ | ✅ |

#### **Thông tin Timeline (Có thể chỉnh sửa)**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Chỉnh sửa được |
|--------|-----------|---------------|------------|----------|----------------|
| Ngày bắt đầu dự kiến | planned_start_date | DATE | Định dạng YYYY-MM-DD | ✅ | ✅ |
| Ngày kết thúc dự kiến | planned_end_date | DATE | >= planned_start_date | ✅ | ✅ |
| Ngày mở thầu | tender_open_date | DATE | >= planned_start_date | ❌ | ✅ |
| Ngày đóng thầu | tender_close_date | DATE | >= tender_open_date | ❌ | ✅ |

#### **Thông tin Không thể chỉnh sửa**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Chỉnh sửa được |
|--------|-----------|---------------|------------|----------|----------------|
| Mã gói thầu | tender_code | VARCHAR(20) | GT-YYYY-XXXX | ✅ | ❌ |
| Ngày tạo | created_date | TIMESTAMP | Tự động | ✅ | ❌ |
| Người tạo | created_by | INT | User ID | ✅ | ❌ |

### **Quy tắc Validation Chỉnh sửa**

#### **Validation Permission**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Edit permission | User có quyền | Role-based access | "Bạn không có quyền chỉnh sửa gói thầu này" |
| Status validation | Trạng thái cho phép | Không phải 'completed' | "Không thể chỉnh sửa gói thầu đã hoàn thành" |
| Time limit | Trong thời gian cho phép | 24h sau khi tạo | "Đã quá thời gian cho phép chỉnh sửa" |

#### **Validation Business Rules**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Timeline consistency | Ngày hợp lệ | planned_end_date >= planned_start_date | "Ngày kết thúc phải sau ngày bắt đầu" |
| Project validation | Dự án tồn tại | Project active và accessible | "Dự án không tồn tại hoặc không truy cập được" |
| Tender method | Hình thức hợp lệ | Theo quy định đấu thầu | "Hình thức lựa chọn nhà thầu không hợp lệ" |

---

## GT-2.2: Xóa Gói thầu

### **Bảng Validation Form Xóa**

#### **Thông tin Xác nhận Xóa**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Mã gói thầu | tender_code | VARCHAR(20) | GT-YYYY-XXXX | ✅ | Mã gói thầu cần xóa |
| Lý do xóa | delete_reason | TEXT | 10-500 ký tự | ✅ | Lý do xóa gói thầu |
| Xác nhận xóa | confirm_delete | BOOLEAN | true/false | ✅ | Checkbox xác nhận |
| Người xóa | deleted_by | INT | User ID | ✅ | Người thực hiện xóa |

#### **Thông tin Kiểm tra Dependencies**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Số hợp đồng liên quan | related_contracts | INT | >= 0 | ✅ | Số hợp đồng đã tạo |
| Số chi phí liên quan | related_costs | INT | >= 0 | ✅ | Số chi phí đã tạo |
| Số tài liệu đính kèm | related_documents | INT | >= 0 | ✅ | Số tài liệu đính kèm |
| Trạng thái gói thầu | tender_status | ENUM | 'draft', 'created', 'in_progress', 'completed', 'cancelled' | ✅ | Trạng thái hiện tại |

### **Quy tắc Validation Xóa**

#### **Validation Permission và Status**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Delete permission | User có quyền | Role-based access | "Bạn không có quyền xóa gói thầu" |
| Status validation | Trạng thái cho phép | Chỉ 'draft' hoặc 'created' | "Chỉ có thể xóa gói thầu ở trạng thái nháp hoặc đã tạo" |
| Dependencies check | Không có dependencies | related_contracts = 0 | "Không thể xóa gói thầu đã có hợp đồng liên quan" |

#### **Validation Business Rules**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Reason required | Lý do xóa | Ít nhất 10 ký tự | "Vui lòng nhập lý do xóa (ít nhất 10 ký tự)" |
| Confirmation | Xác nhận xóa | confirm_delete = true | "Vui lòng xác nhận việc xóa gói thầu" |
| Soft delete | Xóa mềm | Chỉ đánh dấu deleted | "Gói thầu sẽ được đánh dấu xóa thay vì xóa hoàn toàn" |

---

## GT-3.1: Upload và Quản lý Tài liệu Gói thầu

### **Bảng Validation Form Upload Tài liệu**

#### **Thông tin File Upload**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| File tài liệu | document_file | FILE | PDF, DOC, DOCX, XLS, XLSX, JPG, PNG | ✅ | File tài liệu |
| Tên tài liệu | document_name | VARCHAR(200) | 3-200 ký tự | ✅ | Tên hiển thị tài liệu |
| Loại tài liệu | document_type | ENUM | 'hsmt', 'tbmt', 'contract', 'report', 'other' | ✅ | Phân loại tài liệu |
| Mô tả | document_description | TEXT | Tối đa 500 ký tự | ❌ | Mô tả tài liệu |
| Phiên bản | document_version | VARCHAR(20) | Format: v1.0, v2.1 | ❌ | Phiên bản tài liệu |

#### **Thông tin Metadata**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Kích thước file | file_size | BIGINT | <= 50MB | ✅ | Kích thước file |
| Định dạng file | file_extension | VARCHAR(10) | Các định dạng cho phép | ✅ | Định dạng file |
| Checksum | file_checksum | VARCHAR(64) | SHA-256 hash | ✅ | Checksum file |
| Ngày upload | upload_date | TIMESTAMP | Tự động | ✅ | Thời gian upload |

### **Quy tắc Validation Upload**

#### **Validation File**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| File size | Kích thước hợp lệ | <= 50MB | "File quá lớn, tối đa 50MB" |
| File type | Định dạng cho phép | PDF, DOC, DOCX, XLS, XLSX, JPG, PNG | "Định dạng file không được hỗ trợ" |
| File content | Nội dung hợp lệ | Không chứa virus | "File có thể chứa nội dung độc hại" |
| File name | Tên hợp lệ | Không chứa ký tự đặc biệt | "Tên file chứa ký tự không hợp lệ" |

#### **Validation Business Rules**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Document type | Loại tài liệu | Theo quy định | "Loại tài liệu không hợp lệ" |
| Version format | Định dạng phiên bản | vX.Y format | "Định dạng phiên bản không hợp lệ" |
| Duplicate check | Trùng lặp tên | Kiểm tra trong database | "Tên tài liệu đã tồn tại" |

---

## GT-4.1: Tìm kiếm và Lọc Gói thầu

### **Bảng Validation Form Tìm kiếm**

#### **Thông tin Tìm kiếm Cơ bản**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Từ khóa tìm kiếm | search_keyword | VARCHAR(100) | 1-100 ký tự | ❌ | Từ khóa tìm kiếm |
| Mã gói thầu | tender_code | VARCHAR(20) | GT-YYYY-XXXX | ❌ | Mã gói thầu |
| Tên gói thầu | tender_name | VARCHAR(200) | 1-200 ký tự | ❌ | Tên gói thầu |
| Dự án liên quan | project_id | INT | ID hợp lệ | ❌ | Dự án liên quan |

#### **Thông tin Lọc Nâng cao**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Trạng thái gói thầu | tender_status | ENUM | 'draft', 'created', 'in_progress', 'completed', 'cancelled' | ❌ | Trạng thái |
| Hình thức lựa chọn | tender_method | ENUM | 'open_bidding', 'limited_bidding', 'direct_contract', 'competitive_consultation' | ❌ | Hình thức |
| Khoảng giá trị | value_range | JSON | {min: number, max: number} | ❌ | Khoảng giá trị |
| Khoảng thời gian | date_range | JSON | {start: date, end: date} | ❌ | Khoảng thời gian |

### **Quy tắc Validation Tìm kiếm**

#### **Validation Input**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Search keyword | Từ khóa hợp lệ | Không chứa SQL injection | "Từ khóa tìm kiếm không hợp lệ" |
| Date range | Khoảng thời gian | start_date <= end_date | "Ngày bắt đầu phải trước ngày kết thúc" |
| Value range | Khoảng giá trị | min_value <= max_value | "Giá trị tối thiểu phải <= giá trị tối đa" |

---

## GT-4.2: Xuất báo cáo Gói thầu

### **Bảng Validation Form Xuất báo cáo**

#### **Thông tin Báo cáo**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Loại báo cáo | report_type | ENUM | 'summary', 'detailed', 'custom' | ✅ | Loại báo cáo |
| Định dạng xuất | export_format | ENUM | 'pdf', 'excel', 'csv' | ✅ | Định dạng file |
| Phạm vi dữ liệu | data_scope | ENUM | 'all', 'filtered', 'selected' | ✅ | Phạm vi dữ liệu |
| Tên file | file_name | VARCHAR(100) | 3-100 ký tự | ✅ | Tên file xuất |

#### **Thông tin Tùy chọn**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Cột hiển thị | columns | JSON | Mảng tên cột | ❌ | Cột cần xuất |
| Sắp xếp | sort_order | JSON | {field: string, direction: string} | ❌ | Thứ tự sắp xếp |
| Lọc dữ liệu | filters | JSON | Mảng điều kiện lọc | ❌ | Điều kiện lọc |

### **Quy tắc Validation Xuất báo cáo**

#### **Validation Export**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| File name | Tên file hợp lệ | Không chứa ký tự đặc biệt | "Tên file chứa ký tự không hợp lệ" |
| Data scope | Phạm vi hợp lệ | Có dữ liệu để xuất | "Không có dữ liệu để xuất báo cáo" |
| Export permission | Quyền xuất báo cáo | User có quyền | "Bạn không có quyền xuất báo cáo" |

---

## GT-4.3: Quản lý Quyền truy cập Gói thầu

### **Bảng Validation Form Quản lý Quyền**

#### **Thông tin Người dùng**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| User ID | user_id | INT | ID hợp lệ từ bảng users | ✅ | ID người dùng |
| Tên người dùng | user_name | VARCHAR(100) | Tên hiển thị | ✅ | Tên người dùng |
| Email | user_email | VARCHAR(100) | Email hợp lệ | ✅ | Email người dùng |
| Vai trò | user_role | ENUM | 'admin', 'manager', 'user', 'viewer' | ✅ | Vai trò người dùng |

#### **Thông tin Quyền**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Quyền xem | view_permission | BOOLEAN | true/false | ✅ | Quyền xem gói thầu |
| Quyền tạo | create_permission | BOOLEAN | true/false | ✅ | Quyền tạo gói thầu |
| Quyền chỉnh sửa | edit_permission | BOOLEAN | true/false | ✅ | Quyền chỉnh sửa |
| Quyền xóa | delete_permission | BOOLEAN | true/false | ✅ | Quyền xóa gói thầu |
| Quyền xuất báo cáo | export_permission | BOOLEAN | true/false | ✅ | Quyền xuất báo cáo |

### **Quy tắc Validation Quyền**

#### **Validation Permission**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| User exists | Người dùng tồn tại | ID hợp lệ trong database | "Người dùng không tồn tại" |
| Role validation | Vai trò hợp lệ | Theo quy định hệ thống | "Vai trò không hợp lệ" |
| Permission logic | Logic quyền | view_permission >= edit_permission | "Quyền chỉnh sửa yêu cầu quyền xem" |

---

## Tổng kết Validation Rules

### **Thống kê Validation Rules**
- **GT-1.1 (Tạo gói thầu):** 15 validation rules
- **GT-1.2 (Kết nối API):** 8 validation rules  
- **GT-2.1 (Chỉnh sửa):** 12 validation rules
- **GT-2.2 (Xóa):** 6 validation rules
- **GT-3.1 (Upload tài liệu):** 8 validation rules
- **GT-4.1 (Tìm kiếm):** 6 validation rules
- **GT-4.2 (Xuất báo cáo):** 4 validation rules
- **GT-4.3 (Quản lý quyền):** 4 validation rules

**Tổng cộng:** 63 validation rules

### **Ưu tiên Validation**
1. **High Priority:** Validation bảo mật và dữ liệu (45 rules)
2. **Medium Priority:** Validation UI/UX (12 rules)  
3. **Low Priority:** Validation tối ưu hóa (6 rules)

### **Lưu ý Implementation**
- Tất cả validation rules phải được implement ở cả Frontend và Backend
- Validation messages phải rõ ràng và hướng dẫn người dùng
- Cần có unit tests cho tất cả validation rules
- Validation phải real-time và user-friendly
