# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-1.2
### Kết nối API lấy thông tin gói thầu từ Cổng thông tin đấu thầu Quốc gia

#### Thông tin User Story
- **Story ID:** GT-1.2
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 1
- **Status:** To Do
- **Dependencies:** GT-1.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** hệ thống có khả năng kết nối API để tự động lấy các thông tin của gói thầu từ Cổng thông tin đấu thầu Quốc gia (muasamcong.mpi.gov.vn) vào các trường tương ứng trong form tạo/chỉnh sửa gói thầu,  
**Để** tôi có thể tiết kiệm thời gian nhập liệu thủ công, đảm bảo tính chính xác và đồng bộ của dữ liệu gói thầu với thông tin công khai.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có trường để nhập hoặc dán đường dẫn/mã ID gói thầu trên Cổng thông tin đấu thầu Quốc gia
- [ ] Có nút/chức năng "Lấy thông tin từ Cổng" để kích hoạt việc tự động điền dữ liệu
- [ ] Các trường thông tin liên quan (ví dụ: mã TBMT, tên gói thầu, giá gói thầu, hình thức lựa chọn, v.v.) được tự động điền và người dùng có thể xem lại/chỉnh sửa
- [ ] Hệ thống hiển thị trạng thái kết nối và xử lý dữ liệu
- [ ] Có thể lưu và đồng bộ thông tin đã lấy từ Cổng
- [ ] Hỗ trợ xử lý lỗi khi không thể kết nối hoặc dữ liệu không hợp lệ
- [ ] Có thể cập nhật thông tin từ Cổng sau khi đã tạo gói thầu

#### 2.4 Activity Diagram
![GT-1.2 Activity Diagram](diagrams/GT-1.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý kết nối API lấy thông tin gói thầu*

---

### Functional Requirements

#### Core Features
1. **API Integration với Cổng thông tin đấu thầu Quốc gia**
   - Kết nối API muasamcong.mpi.gov.vn
   - Xác thực và bảo mật kết nối
   - Xử lý rate limiting và timeout
   - Error handling và retry mechanism

2. **Data Mapping và Transformation**
   - Map dữ liệu từ API response sang form fields
   - Transform format dữ liệu phù hợp
   - Validate dữ liệu nhận được
   - Handle missing hoặc invalid data

3. **User Interface Integration**
   - Input field cho URL/mã ID gói thầu
   - Button "Lấy thông tin từ Cổng"
   - Loading indicator và status messages
   - Preview dữ liệu trước khi lưu

4. **Data Synchronization**
   - Auto-fill form fields
   - Allow manual editing sau khi auto-fill
   - Save và sync với database
   - Update existing tender packages

#### Business Rules
- API calls được rate limited để tránh overload
- Dữ liệu từ Cổng được validate trước khi sử dụng
- User có thể edit dữ liệu sau khi auto-fill
- Backup dữ liệu gốc từ Cổng
- Log tất cả API calls và responses

#### Data Mapping Rules
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

3. **Additional Information Mapping**
   - `description` ↔ `mo_ta_chi_tiet`
   - `location` ↔ `dia_diem_thuc_hien`
   - `procurement_agency` ↔ `chu_dau_tu`

---

### Technical Specifications

#### Sequence Diagram
![GT-1.2 Sequence Diagram](diagrams/GT-1.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi kết nối API lấy thông tin gói thầu*

#### API Integration Configuration
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

// Data Mapping Service
interface TenderPortalDataMapper {
  mapApiResponseToForm(response: TenderPortalResponse): TenderPackageForm
  validateApiData(data: any): ValidationResult
  transformDataFormat(data: any): any
}
```

#### Database Schema Updates
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
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (connection_id) REFERENCES api_connections(id),
    FOREIGN KEY (performed_by) REFERENCES users(id)
);

-- Bảng mapping dữ liệu từ Cổng thông tin
CREATE TABLE tender_portal_mappings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT NOT NULL,
    portal_tender_id VARCHAR(100) NOT NULL,
    portal_url VARCHAR(500),
    last_sync_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_status ENUM('success', 'failed', 'partial') DEFAULT 'success',
    original_data JSON,
    mapped_data JSON,
    
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id) ON DELETE CASCADE,
    UNIQUE KEY unique_tender_mapping (tender_package_id, portal_tender_id)
);

-- Insert default API connection for National Tender Portal
INSERT INTO api_connections (connection_name, base_url, api_key, rate_limit_per_minute, rate_limit_per_hour) VALUES
('National Tender Portal', 'https://muasamcong.mpi.gov.vn/api', 'your_api_key_here', 60, 1000);
```

#### API Endpoints
```
# Tender Portal Integration
POST /api/tender-portal/fetch-data
{
  "portal_url": "https://muasamcong.mpi.gov.vn/tender/12345",
  "tender_id": "GT-2024-001"
}

GET /api/tender-portal/validate-url
{
  "url": "https://muasamcong.mpi.gov.vn/tender/12345"
}

POST /api/tender-portal/sync-existing
{
  "tender_package_id": 123,
  "portal_url": "https://muasamcong.mpi.gov.vn/tender/12345"
}

# API Connection Management
GET /api/connections
PUT /api/connections/{id}
POST /api/connections/test

# API Call Logs
GET /api/connections/{id}/logs
GET /api/connections/logs/summary
```

#### Frontend Components
```typescript
// Tender Portal Integration Component
interface TenderPortalIntegration {
  // URL Input and Validation
  validatePortalUrl(url: string): Promise<ValidationResult>
  extractTenderId(url: string): string
  
  // Data Fetching
  fetchTenderData(portalUrl: string): Promise<TenderPortalResponse>
  fetchTenderDataById(tenderId: string): Promise<TenderPortalResponse>
  
  // Data Processing
  mapPortalDataToForm(portalData: TenderPortalResponse): TenderPackageForm
  validatePortalData(data: TenderPortalResponse): ValidationResult
  
  // UI State Management
  setLoadingState(isLoading: boolean): void
  setErrorState(error: string): void
  setSuccessState(data: TenderPackageForm): void
}

// Portal URL Input Component
interface PortalUrlInput {
  url: string
  isValid: boolean
  isLoading: boolean
  errorMessage?: string
  onUrlChange: (url: string) => void
  onFetchData: () => void
  onClear: () => void
}

// Data Preview Component
interface DataPreviewComponent {
  originalData: TenderPortalResponse
  mappedData: TenderPackageForm
  onConfirm: (data: TenderPackageForm) => void
  onEdit: (field: string, value: any) => void
  onCancel: () => void
}

// API Connection Status Component
interface ApiConnectionStatus {
  isConnected: boolean
  lastSyncTime?: Date
  syncStatus: 'success' | 'failed' | 'partial'
  errorMessage?: string
  onRetry: () => void
}
```

---

### UI/UX Design

#### Portal URL Input Section
- **Layout:** Input field với validation và action buttons
- **Components:**
  - URL input field với placeholder
  - "Validate URL" button
  - "Fetch Data" button
  - Clear button
  - Status indicator

#### Data Fetching Process
- **Loading State:**
  - Spinner animation
  - Progress indicator
  - Status messages
  - Cancel button

#### Data Preview Interface
- **Layout:** Side-by-side comparison
- **Sections:**
  - Original data from portal
  - Mapped form data
  - Edit controls
  - Confirm/Cancel buttons

#### Error Handling
- **Error States:**
  - Invalid URL format
  - Connection timeout
  - API rate limit exceeded
  - Data validation errors
  - Network errors

---

### Integration Requirements

#### National Tender Portal API
1. **Authentication**
   - API key authentication
   - Rate limiting compliance
   - Request signing

2. **Data Format**
   - JSON response format
   - UTF-8 encoding
   - Standard date formats
   - Currency formatting

3. **Error Handling**
   - HTTP status codes
   - Error message format
   - Retry logic
   - Fallback mechanisms

#### Form Integration
1. **Auto-fill Functionality**
   - Map portal data to form fields
   - Preserve user-entered data
   - Allow manual overrides
   - Validate mapped data

2. **Data Validation**
   - Cross-field validation
   - Business rule validation
   - Format validation
   - Required field validation

---

### Security Considerations

#### API Security
- Secure API key storage
- HTTPS communication
- Request signing
- Rate limiting protection

#### Data Protection
- Encrypt sensitive data
- Secure data transmission
- Access control
- Audit logging

#### Error Handling
- Don't expose sensitive information in errors
- Log errors securely
- Implement proper error recovery
- User-friendly error messages

---

### Testing Strategy

#### Unit Tests
- API connection logic
- Data mapping functions
- URL validation
- Error handling

#### Integration Tests
- End-to-end API integration
- Form auto-fill functionality
- Data synchronization
- Error scenarios

#### User Acceptance Tests
- Portal URL input workflow
- Data fetching process
- Form auto-fill experience
- Error handling scenarios

---

### Deployment & Configuration

#### Environment Setup
- API key configuration
- Rate limiting setup
- Error monitoring
- Performance monitoring

#### Monitoring & Logging
- API call monitoring
- Response time tracking
- Error rate monitoring
- Usage analytics

---

### Documentation

#### User Manual
- Portal URL input guide
- Data fetching procedures
- Error troubleshooting
- Best practices

#### Technical Documentation
- API integration details
- Data mapping specifications
- Security implementation
- Performance optimization 