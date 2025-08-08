# GT-1.1: Tạo Gói thầu mới - Diagrams Summary

## 📋 Tổng quan
GT-1.1 tập trung vào chức năng tạo gói thầu mới với tích hợp dự án và Bitrix24.

## 🎯 User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể tạo một hồ sơ gói thầu mới và nhập các thông tin cần thiết về gói thầu (ví dụ: tên, mã TBMT, giá, dự án liên quan, hình thức lựa chọn nhà thầu, v.v.),  
**Để** tôi có thể khởi tạo một gói thầu với đầy đủ thông tin và phục vụ công tác quản lý, theo dõi sau này.

## 📊 Diagrams Created

### 1. Activity Diagram
**File:** `diagrams/gt-1.1-activity-diagram.puml`  
**Image:** `diagrams/GT-1.1 Activity Diagram.png`

**Mô tả luồng xử lý:**
- Khởi tạo form tạo gói thầu
- Nhập thông tin cơ bản (bắt buộc)
- Validation thông tin
- Tự động sinh mã gói thầu
- Nhập thông tin chi tiết (tùy chọn)
- Lưu nháp hoặc hoàn thành
- Preview và xác nhận thông tin
- Tích hợp với dự án và Bitrix24

**Các bước chính:**
1. Người dùng truy cập trang tạo gói thầu
2. Nhập thông tin cơ bản (tên, dự án, hình thức, giá trị, thời gian)
3. Validation thông tin cơ bản
4. Tự động sinh mã gói thầu (GT-YYYY-XXXX)
5. Nhập thông tin chi tiết (tùy chọn)
6. Lưu nháp hoặc hoàn thành
7. Preview và xác nhận thông tin
8. Tích hợp với dự án và Bitrix24

### 2. Sequence Diagram
**File:** `diagrams/gt-1.1-sequence-diagram.puml`  
**Image:** `diagrams/GT-1.1 Sequence Diagram.png`

**Mô tả tương tác giữa các thành phần:**
- **User**: Người dùng thực hiện các thao tác
- **Frontend**: Giao diện người dùng
- **Backend API**: Xử lý logic nghiệp vụ
- **Database**: Lưu trữ dữ liệu
- **Project Module**: Tích hợp với module dự án
- **Bitrix24**: Đồng bộ dữ liệu
- **Notification Service**: Gửi thông báo

**Các workflow chính:**
1. **Khởi tạo Form** với danh sách dự án
2. **Nhập Thông tin Cơ bản** với validation real-time
3. **Tạo Gói thầu** với tích hợp dự án và Bitrix24
4. **Lưu Nháp** cho thông tin chưa hoàn chỉnh
5. **Preview và Xác nhận** thông tin trước khi lưu
6. **Xử lý Lỗi** cho các trường hợp không hợp lệ

## 🔧 Technical Implementation

### Database Schema
```sql
-- Bảng gói thầu
CREATE TABLE tender_packages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_code VARCHAR(20) NOT NULL UNIQUE, -- GT-YYYY-XXXX
    name VARCHAR(500) NOT NULL,
    description TEXT,
    project_id INT NOT NULL,
    tender_method ENUM('open_tender', 'limited_tender', 'direct_appointment', 'competitive_consultation', 'other') NOT NULL,
    estimated_value DECIMAL(15,2),
    currency VARCHAR(10) DEFAULT 'VND',
    start_date DATE,
    end_date DATE,
    status ENUM('draft', 'created', 'in_progress', 'completed', 'cancelled') DEFAULT 'draft',
    
    -- Thông tin chi tiết (tùy chọn)
    tbmt_code VARCHAR(100),
    participant_count INT,
    hsmt_approval_decision VARCHAR(200),
    kqlcnt_approval_decision VARCHAR(200),
    winning_bid_value DECIMAL(15,2),
    winning_contractor VARCHAR(500),
    
    -- Thông tin từ Bitrix
    bitrix_task_id INT,
    bitrix_workflow_id INT,
    bitrix_status VARCHAR(100),
    
    -- Metadata
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### API Endpoints
```
# Tender Package Management
GET /api/tender-packages
POST /api/tender-packages
GET /api/tender-packages/{id}
PUT /api/tender-packages/{id}
DELETE /api/tender-packages/{id}

# Tender Package Creation
POST /api/tender-packages/create
POST /api/tender-packages/draft
GET /api/tender-packages/preview
PUT /api/tender-packages/{id}/confirm
```

### Business Rules
- Mã gói thầu tự động sinh theo format: GT-YYYY-XXXX
- Dự án liên quan phải tồn tại trong hệ thống
- Hình thức lựa chọn nhà thầu phải được phê duyệt trước khi triển khai
- Thông tin từ Bitrix được cập nhật real-time
- Workflow tự động dựa trên hình thức lựa chọn nhà thầu

## 📱 UI Components
- **TenderPackageForm**: Form tạo gói thầu
- **ProjectSelector**: Dropdown chọn dự án liên quan
- **TenderMethodSelector**: Dropdown chọn hình thức lựa chọn
- **DraftSaveButton**: Nút lưu nháp
- **PreviewModal**: Modal xem trước thông tin
- **ConfirmationDialog**: Dialog xác nhận thông tin

## 🔄 Integration
- **Project Module Integration**: Chọn dự án từ danh sách có sẵn
- **Bitrix24 Integration**: Tự động triển khai workflow theo hình thức
- **Notification System**: Thông báo khi tạo gói thầu thành công
- **Audit Trail**: Log mọi thay đổi cho compliance

## ✅ Acceptance Criteria
- [x] Có một form để tạo gói thầu mới với các trường thông tin quan trọng
- [x] Mã gói thầu tự động sinh và không thể chỉnh sửa
- [x] Trường Dự án liên quan cho phép chọn từ danh sách các dự án đã có trong Module Dự án
- [x] Một số thông tin được link, lấy thông tin từ Bitrix
- [x] Khi triển khai gói thầu trên Bitrix, Bitrix sẽ tự động triển khai theo luồng công việc phù hợp với Hình thức đã được phê duyệt
- [x] Form có validation cho các trường bắt buộc
- [x] Hỗ trợ lưu nháp và hoàn thành sau
- [x] Hiển thị preview thông tin gói thầu trước khi lưu

## 📈 Performance Requirements
- Thời gian tải form < 2 giây
- Thời gian tạo gói thầu < 5 giây
- Thời gian lưu nháp < 2 giây
- Real-time validation không lag

---

**Status:** ✅ Completed  
**Diagrams:** Activity Diagram, Sequence Diagram  
**Integration:** SRS_Project_Category_GT-1.1.md
