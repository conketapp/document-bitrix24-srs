# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-2.3
### Nhập Tài sản/Dịch vụ hàng loạt từ file

#### Thông tin User Story
- **Story ID:** TSDV-2.3
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** TSDV-1.1, TSDV-2.1, TSDV-2.2

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý tài sản/dịch vụ,  
**Tôi muốn** có thể nhập dữ liệu tài sản hoặc dịch vụ hàng loạt từ một file (ví dụ: Excel) vào hệ thống,  
**Để** tôi có thể tiết kiệm thời gian và công sức khi cần thêm số lượng lớn tài sản/dịch vụ.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Cung cấp một mẫu file nhập liệu chuẩn để người dùng điền thông tin
- [ ] Hệ thống kiểm tra tính hợp lệ của dữ liệu trước khi nhập (ví dụ: định dạng ngày, kiểu dữ liệu)
- [ ] Báo cáo các lỗi hoặc dữ liệu không hợp lệ sau khi quá trình nhập hoàn tất
- [ ] Có thể xem trước dữ liệu trước khi nhập chính thức
- [ ] Có thể chọn các bản ghi cụ thể để nhập hoặc bỏ qua
- [ ] Có thể xử lý các trường hợp trùng lặp (bỏ qua, cập nhật, hoặc tạo mới)
- [ ] Có thể nhập file với nhiều định dạng (Excel, CSV)
- [ ] Có thể tùy chỉnh mapping giữa cột file và trường dữ liệu
- [ ] Có thể lưu và tái sử dụng cấu hình nhập liệu
- [ ] Có thể theo dõi tiến trình nhập liệu
- [ ] Có thể xem lịch sử nhập liệu và kết quả
- [ ] Có thể rollback nhập liệu nếu cần thiết

#### 2.4 Activity Diagram
![TSDV-2.3 Activity Diagram](diagrams/TSDV-2.3%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý nhập Tài sản/Dịch vụ hàng loạt*

#### 2.5 Sequence Diagram
![TSDV-2.3 Sequence Diagram](diagrams/TSDV-2.3%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi nhập Tài sản/Dịch vụ hàng loạt*

---

### Functional Requirements

#### Core Features
1. **Import Functionality**
   - File upload
   - Data validation
   - Preview data
   - Bulk import
   - Error handling

2. **File Formats**
   - Excel (.xlsx, .xls)
   - CSV (.csv)
   - JSON (.json)

3. **Import Options**
   - Create new records
   - Update existing records
   - Skip duplicates
   - Merge data

4. **Validation**
   - Data type validation
   - Format validation
   - Business rule validation
   - Duplicate detection

#### Business Rules
- Chỉ cho phép nhập dữ liệu mà người dùng có quyền tạo
- Dữ liệu nhập phải tuân thủ các quy tắc nghiệp vụ
- Phải có cơ chế xử lý trùng lặp rõ ràng
- Phải có khả năng rollback khi có lỗi
- Phải ghi log đầy đủ quá trình nhập liệu

#### Import Types
1. **Asset Import**
   - Hardware assets
   - Software assets
   - Infrastructure assets
   - Custom assets

2. **Service Import**
   - IT services
   - Business services
   - Support services
   - Custom services

3. **Mixed Import**
   - Assets and services
   - Different categories
   - Multiple types

#### Validation Rules
1. **Required Fields**
   - Asset/Service code
   - Name
   - Type
   - Category
   - Status

2. **Data Format Validation**
   - Date format (dd/MM/yyyy)
   - Number format
   - Currency format
   - Email format
   - Phone format

3. **Business Rule Validation**
   - Code uniqueness
   - Category existence
   - Status validity
   - Project existence
   - User existence

4. **Data Type Validation**
   - String length
   - Numeric range
   - Date range
   - Enum values

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử nhập liệu
CREATE TABLE asset_service_import_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    import_name VARCHAR(200) NOT NULL,
    import_type ENUM('asset', 'service', 'mixed') NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT,
    file_path VARCHAR(500) NOT NULL,
    import_config JSON NOT NULL,
    total_records INT DEFAULT 0,
    valid_records INT DEFAULT 0,
    invalid_records INT DEFAULT 0,
    created_records INT DEFAULT 0,
    updated_records INT DEFAULT 0,
    skipped_records INT DEFAULT 0,
    error_records INT DEFAULT 0,
    import_status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    error_message TEXT,
    imported_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (imported_by) REFERENCES users(id),
    INDEX idx_import_type (import_type),
    INDEX idx_import_status (import_status),
    INDEX idx_imported_by (imported_by),
    INDEX idx_created_at (created_at)
);

-- Bảng chi tiết nhập liệu
CREATE TABLE asset_service_import_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    import_history_id INT NOT NULL,
    row_number INT NOT NULL,
    original_data JSON NOT NULL,
    processed_data JSON,
    validation_status ENUM('valid', 'invalid', 'warning') NOT NULL,
    import_status ENUM('pending', 'created', 'updated', 'skipped', 'error') DEFAULT 'pending',
    error_messages JSON,
    warning_messages JSON,
    created_asset_service_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (import_history_id) REFERENCES asset_service_import_history(id) ON DELETE CASCADE,
    FOREIGN KEY (created_asset_service_id) REFERENCES assets_services(id),
    INDEX idx_import_history_id (import_history_id),
    INDEX idx_validation_status (validation_status),
    INDEX idx_import_status (import_status),
    INDEX idx_row_number (row_number)
);

-- Bảng cấu hình nhập liệu
CREATE TABLE asset_service_import_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_name VARCHAR(200) NOT NULL,
    config_description TEXT,
    import_type ENUM('asset', 'service', 'mixed') NOT NULL,
    column_mapping JSON NOT NULL,
    validation_rules JSON NOT NULL,
    import_options JSON NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_import_type (import_type),
    INDEX idx_is_default (is_default),
    INDEX idx_is_public (is_public)
);

-- Insert default import configurations
INSERT INTO asset_service_import_config (config_name, config_description, import_type, column_mapping, validation_rules, import_options, is_default) VALUES
('Cấu hình nhập tài sản chuẩn', 'Cấu hình nhập tài sản với đầy đủ thông tin', 'asset',
'{"code": "A", "name": "B", "type": "C", "category": "D", "subcategory": "E", "status": "F", "responsible_person": "G", "location": "H", "purchase_cost": "I", "current_value": "J", "purchase_date": "K", "warranty_expiry": "L", "description": "M"}',
'{"required_fields": ["code", "name", "type", "category"], "format_rules": {"purchase_date": "dd/MM/yyyy", "purchase_cost": "number", "current_value": "number"}}',
'{"duplicate_handling": "skip", "create_missing_references": false, "auto_generate_codes": false}', true),
('Cấu hình nhập dịch vụ chuẩn', 'Cấu hình nhập dịch vụ với đầy đủ thông tin', 'service',
'{"code": "A", "name": "B", "type": "C", "category": "D", "subcategory": "E", "status": "F", "responsible_person": "G", "service_provider": "H", "service_cost": "I", "start_date": "J", "end_date": "K", "description": "L"}',
'{"required_fields": ["code", "name", "type", "category"], "format_rules": {"start_date": "dd/MM/yyyy", "end_date": "dd/MM/yyyy", "service_cost": "number"}}',
'{"duplicate_handling": "skip", "create_missing_references": false, "auto_generate_codes": false}', false);
```

#### API Endpoints
```typescript
# Upload Import File
POST /api/assets-services/import/upload
Content-Type: multipart/form-data
{
  "file": File,
  "import_type": "asset",
  "config_id": 1
}
Response: {
  "success": true,
  "import_id": 123,
  "file_name": "import_assets.xlsx",
  "file_size": 2048576,
  "total_rows": 150,
  "message": "File đã được tải lên thành công"
}

# Preview Import Data
GET /api/assets-services/import/{import_id}/preview
{
  "page": 1,
  "page_size": 20
}
Response: {
  "preview_data": [
    {
      "row_number": 1,
      "original_data": {
        "code": "TS2024000001",
        "name": "Máy chủ Dell PowerEdge R740",
        "type": "asset",
        "category": "Hardware",
        "subcategory": "Server",
        "status": "active",
        "responsible_person": "Nguyễn Văn A",
        "location": "Data Center A",
        "purchase_cost": 45000000,
        "current_value": 40000000,
        "purchase_date": "15/01/2024",
        "warranty_expiry": "15/01/2027",
        "description": "Máy chủ Dell PowerEdge R740"
      },
      "validation_status": "valid",
      "error_messages": [],
      "warning_messages": []
    }
  ],
  "validation_summary": {
    "total_rows": 150,
    "valid_rows": 145,
    "invalid_rows": 3,
    "warning_rows": 2
  },
  "pagination": {
    "current_page": 1,
    "total_pages": 8,
    "total_items": 150,
    "page_size": 20
  }
}

# Execute Import
POST /api/assets-services/import/{import_id}/execute
{
  "import_options": {
    "duplicate_handling": "skip",
    "create_missing_references": false,
    "auto_generate_codes": false,
    "validate_before_import": true
  },
  "selected_rows": [1, 2, 3, 4, 6, 7, 9, 10],
  "skip_invalid_rows": true
}
Response: {
  "success": true,
  "import_results": {
    "total_processed": 8,
    "created_records": 6,
    "updated_records": 1,
    "skipped_records": 1,
    "error_records": 0,
    "import_status": "completed",
    "execution_time_ms": 2500
  },
  "message": "Nhập liệu đã hoàn thành thành công"
}

# Get Import History
GET /api/assets-services/import/history
{
  "page": 1,
  "page_size": 20,
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "imports": [
    {
      "id": 123,
      "import_name": "Nhập tài sản từ Excel",
      "import_type": "asset",
      "file_name": "import_assets.xlsx",
      "file_size": 2048576,
      "total_records": 150,
      "valid_records": 145,
      "invalid_records": 3,
      "created_records": 140,
      "updated_records": 5,
      "skipped_records": 0,
      "error_records": 0,
      "import_status": "completed",
      "started_at": "2024-01-25T14:30:00Z",
      "completed_at": "2024-01-25T14:32:30Z",
      "imported_by": "Nguyễn Văn A"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "page_size": 20
  }
}

# Get Import Templates
GET /api/assets-services/import/templates
{
  "template_type": "asset"
}
Response: {
  "templates": [
    {
      "id": 1,
      "template_name": "Template nhập tài sản chuẩn",
      "template_description": "Template Excel cho nhập tài sản với đầy đủ thông tin",
      "template_type": "asset",
      "template_file_path": "/templates/asset_import_template.xlsx",
      "template_config": {
        "columns": ["code", "name", "type", "category", "subcategory", "status", "responsible_person", "location", "purchase_cost", "current_value", "purchase_date", "warranty_expiry", "description"],
        "sample_data": [
          {
            "code": "TS2024000001",
            "name": "Máy chủ Dell PowerEdge R740",
            "type": "asset",
            "category": "Hardware",
            "subcategory": "Server",
            "status": "active",
            "responsible_person": "Nguyễn Văn A",
            "location": "Data Center A",
            "purchase_cost": 45000000,
            "current_value": 40000000,
            "purchase_date": "15/01/2024",
            "warranty_expiry": "15/01/2027",
            "description": "Máy chủ Dell PowerEdge R740"
          }
        ]
      },
      "is_default": true
    }
  ]
}

# Download Import Template
GET /api/assets-services/import/templates/{template_id}/download
Response: File download

# Rollback Import
POST /api/assets-services/import/{import_id}/rollback
{
  "rollback_reason": "Dữ liệu nhập sai, cần rollback",
  "rollback_options": {
    "delete_created_records": true,
    "revert_updated_records": true,
    "keep_import_history": true
  }
}
Response: {
  "success": true,
  "rollback_id": 456,
  "rollback_results": {
    "deleted_records": 140,
    "reverted_records": 5,
    "rollback_status": "completed"
  },
  "message": "Rollback đã hoàn thành thành công"
}
```

#### Frontend Components
```typescript
// Import Interface Component
interface ImportInterfaceComponent {
  importType: string
  importConfig: ImportConfig
  importHistory: ImportHistory[]
  
  onFileUpload: (file: File) => Promise<void>
  onImportTypeChange: (type: string) => void
  onImportConfigChange: (config: ImportConfig) => void
  onImportExecute: () => Promise<void>
  onImportHistorySelect: (history: ImportHistory) => void
}

// File Upload Component
interface FileUploadComponent {
  acceptedFormats: string[]
  maxFileSize: number
  uploadProgress: number
  
  onFileSelect: (file: File) => void
  onFileUpload: (file: File) => Promise<void>
  onUploadProgress: (progress: number) => void
  onUploadComplete: (result: UploadResult) => void
  onUploadError: (error: string) => void
}

// Import Preview Component
interface ImportPreviewComponent {
  previewData: PreviewData[]
  validationSummary: ValidationSummary
  pagination: PaginationInfo
  
  onRowSelect: (rowNumber: number) => void
  onRowDeselect: (rowNumber: number) => void
  onSelectAll: () => void
  onDeselectAll: () => void
  onPageChange: (page: number) => void
  onValidationRefresh: () => void
}

// Import Progress Component
interface ImportProgressComponent {
  importProgress: ImportProgress
  
  onProgressUpdate: (progress: ImportProgress) => void
  onImportComplete: (result: ImportResult) => void
  onImportCancel: () => void
  onImportRetry: () => void
}

// Import History Component
interface ImportHistoryComponent {
  importHistory: ImportHistory[]
  pagination: PaginationInfo
  
  onHistorySelect: (history: ImportHistory) => void
  onHistoryDetails: (history: ImportHistory) => void
  onHistoryRollback: (history: ImportHistory) => void
  onHistoryDelete: (historyId: number) => void
  onPageChange: (page: number) => void
}
```

---

### UI/UX Design

#### Import Interface Layout
- **Import Layout:**
  - File upload area
  - Import type selection
  - Configuration panel
  - Preview area

#### File Upload Design
- **Upload Design:**
  - Drag and drop area
  - File selection button
  - Progress indicator
  - Format validation

#### Import Preview Interface
- **Preview Layout:**
  - Data table
  - Validation indicators
  - Row selection
  - Error highlighting

#### Import Progress Interface
- **Progress Design:**
  - Progress bar
  - Status messages
  - Cancel button
  - Completion summary

---

### Integration Requirements

#### File Processing Integration
1. **Excel Processing**
   - Excel library integration
   - Multiple sheet support
   - Cell formatting
   - Data extraction

2. **CSV Processing**
   - CSV library integration
   - Encoding detection
   - Delimiter detection
   - Data parsing

3. **JSON Processing**
   - JSON library integration
   - Schema validation
   - Data transformation
   - Error handling

#### Data Validation Integration
1. **Validation Engine**
   - Rule-based validation
   - Custom validators
   - Business rule validation
   - Reference validation

2. **Error Handling**
   - Error collection
   - Error reporting
   - Error recovery
   - Rollback mechanisms

---

### Security Considerations

#### Data Protection
- Import permission validation
- Data sanitization
- File type validation
- Size limit enforcement

#### Import Security
- File scanning
- Malware detection
- Access control
- Audit logging

---

### Testing Strategy

#### Unit Tests
- Import logic validation
- Data validation
- File processing
- Error handling

#### Integration Tests
- File upload integration
- Database integration
- Validation engine integration
- Rollback system testing

#### User Acceptance Tests
- Import workflow
- File format validation
- Error handling
- Rollback functionality

---

### Deployment & Configuration

#### Environment Setup
- File processing libraries
- Validation engine setup
- Storage configuration
- Import scheduling

#### Monitoring & Logging
- Import performance monitoring
- File processing analytics
- Error tracking
- Usage logging

---

### Documentation

#### User Manual
- Import procedures
- Template usage
- Validation rules
- Error handling

#### Technical Documentation
- API documentation
- Import configuration
- Integration guides
- Performance optimization 