# GT-1.2: Kết nối API lấy thông tin gói thầu từ Cổng thông tin đấu thầu Quốc gia - Diagrams Summary

## 📋 Tổng quan
GT-1.2 tập trung vào chức năng kết nối API để tự động lấy thông tin gói thầu từ Cổng thông tin đấu thầu Quốc gia.

## 🎯 User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** hệ thống có khả năng kết nối API để tự động lấy các thông tin của gói thầu từ Cổng thông tin đấu thầu Quốc gia (muasamcong.mpi.gov.vn) vào các trường tương ứng trong form tạo/chỉnh sửa gói thầu,  
**Để** tôi có thể tiết kiệm thời gian nhập liệu thủ công, đảm bảo tính chính xác và đồng bộ của dữ liệu gói thầu với thông tin công khai.

## 📊 Diagrams Created

### 1. Activity Diagram
**File:** `diagrams/gt-1.2-activity-diagram.puml`  
**Image:** `diagrams/GT-1.2 Activity Diagram.png`

**Mô tả luồng xử lý:**
- Khởi tạo form với trường nhập URL/mã ID
- Nhập URL hoặc mã ID gói thầu
- Kết nối API với Cổng thông tin đấu thầu Quốc gia
- Parse và validate dữ liệu từ API
- Map dữ liệu sang form fields
- Auto-fill và cho phép chỉnh sửa
- Lưu và đồng bộ thông tin

**Các bước chính:**
1. Người dùng truy cập form tạo/chỉnh sửa gói thầu
2. Nhập URL hoặc mã ID gói thầu
3. Nhấn "Lấy thông tin từ Cổng"
4. Kiểm tra kết nối API
5. Gửi request đến Cổng thông tin đấu thầu Quốc gia
6. Parse và validate dữ liệu từ API
7. Map dữ liệu từ API sang form fields
8. Auto-fill thông tin vào form
9. Cho phép người dùng chỉnh sửa
10. Lưu dữ liệu vào database

### 2. Sequence Diagram
**File:** `diagrams/gt-1.2-sequence-diagram.puml`  
**Image:** `diagrams/GT-1.2 Sequence Diagram.png`

**Mô tả tương tác giữa các thành phần:**
- **User**: Người dùng thực hiện các thao tác
- **Frontend**: Giao diện người dùng
- **Backend API**: Xử lý logic nghiệp vụ
- **Database**: Lưu trữ dữ liệu
- **National Tender Portal API**: API của Cổng thông tin đấu thầu Quốc gia
- **Rate Limiter**: Kiểm soát tốc độ truy cập API
- **Data Validator**: Xác thực dữ liệu từ API

**Các workflow chính:**
1. **Khởi tạo Form** với trường nhập URL/mã ID
2. **Nhập Thông tin Gói thầu** với validation URL format
3. **Kết nối API** với rate limiting và error handling
4. **Cập nhật Gói thầu Hiện có** từ Cổng
5. **Xử lý Lỗi** cho các trường hợp không thể kết nối

## 🔧 Technical Implementation

### API Integration Configuration
```typescript
// API Configuration
interface NationalTenderPortalConfig {
  baseUrl: string // 'https://muasamcong.mpi.gov.vn'
  apiKey: string
  timeout: number // 30000ms
  retryAttempts: number // 3
  rateLimit: {
    requestsPerMinute: number // 60
    requestsPerHour: number // 1000
  }
}

// API Response Structure
interface TenderPortalResponse {
  success: boolean
  data: {
    ma_goi_thau: string
    ten_goi_thau: string
    gia_goi_thau: number
    hinh_thuc_lua_chon: string
    ma_tbmt: string
    so_luong_nha_thau: number
    ngay_mo_thau: string
    ngay_dong_thau: string
    mo_ta_chi_tiet: string
    dia_diem_thuc_hien: string
    chu_dau_tu: string
    trang_thai: string
  }
  error?: {
    code: string
    message: string
  }
}
```

### Database Schema
```sql
-- Bảng lưu trữ thông tin kết nối API
CREATE TABLE api_connections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    connection_name VARCHAR(100) NOT NULL,
    base_url VARCHAR(500) NOT NULL,
    api_key VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    rate_limit_per_minute INT DEFAULT 60,
    rate_limit_per_hour INT DEFAULT 1000,
    timeout_ms INT DEFAULT 30000,
    retry_attempts INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng lưu trữ lịch sử API calls
CREATE TABLE api_call_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    connection_id INT NOT NULL,
    endpoint VARCHAR(200) NOT NULL,
    request_data JSON,
    response_data JSON,
    status_code INT,
    response_time_ms INT,
    success BOOLEAN,
    error_message TEXT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints
```
# API Integration
POST /api/tender-packages/fetch-from-portal
PUT /api/tender-packages/{id}/update-from-portal
POST /api/tender-packages/{id}/sync-from-portal

# Data Mapping
GET /api/tender-packages/mapping-rules
PUT /api/tender-packages/mapping-rules
```

### Business Rules
- API calls được rate limited để tránh overload
- Dữ liệu từ Cổng được validate trước khi sử dụng
- User có thể edit dữ liệu sau khi auto-fill
- Backup dữ liệu gốc từ Cổng
- Log tất cả API calls và responses

### Data Mapping Rules
1. **Basic Information Mapping**
   - `tender_code` ↔ `ma_goi_thau`
   - `name` ↔ `ten_goi_thau`
   - `estimated_value` ↔ `gia_goi_thau`
   - `tender_method` ↔ `hinh_thuc_lua_chon`

2. **Detailed Information Mapping**
   - `tbmt_code` ↔ `ma_tbmt`
   - `participant_count` ↔ `so_luong_nha_thau`
   - `start_date` ↔ `ngay_mo_thau`
   - `end_date` ↔ `ngay_dong_thau`

## 📱 UI Components
- **PortalURLInput**: Input field cho URL/mã ID gói thầu
- **FetchFromPortalButton**: Nút "Lấy thông tin từ Cổng"
- **LoadingIndicator**: Hiển thị trạng thái kết nối
- **DataPreviewModal**: Modal xem trước dữ liệu từ Cổng
- **SyncFromPortalButton**: Nút "Cập nhật từ Cổng"
- **ErrorDisplay**: Hiển thị lỗi kết nối/dữ liệu

## 🔄 Integration
- **National Tender Portal API**: Kết nối với muasamcong.mpi.gov.vn
- **Rate Limiting**: Kiểm soát tốc độ truy cập API
- **Data Validation**: Xác thực dữ liệu từ API
- **Error Handling**: Xử lý lỗi kết nối và dữ liệu
- **Audit Trail**: Log mọi API calls cho compliance

## ✅ Acceptance Criteria
- [x] Có trường để nhập hoặc dán đường dẫn/mã ID gói thầu trên Cổng thông tin đấu thầu Quốc gia
- [x] Có nút/chức năng "Lấy thông tin từ Cổng" để kích hoạt việc tự động điền dữ liệu
- [x] Các trường thông tin liên quan được tự động điền và người dùng có thể xem lại/chỉnh sửa
- [x] Hệ thống hiển thị trạng thái kết nối và xử lý dữ liệu
- [x] Có thể lưu và đồng bộ thông tin đã lấy từ Cổng
- [x] Hỗ trợ xử lý lỗi khi không thể kết nối hoặc dữ liệu không hợp lệ
- [x] Có thể cập nhật thông tin từ Cổng sau khi đã tạo gói thầu

## 📈 Performance Requirements
- Thời gian kết nối API < 30 giây
- Thời gian parse và map dữ liệu < 5 giây
- Rate limiting: 60 requests/phút, 1000 requests/giờ
- Retry mechanism: 3 lần thử lại khi lỗi

---

**Status:** ✅ Completed  
**Diagrams:** Activity Diagram, Sequence Diagram  
**Integration:** SRS_Project_Category_GT-1.2.md
