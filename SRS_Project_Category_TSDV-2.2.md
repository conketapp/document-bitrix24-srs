# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-2.2
### Xuất danh sách Tài sản/Dịch vụ ra file

#### Thông tin User Story
- **Story ID:** TSDV-2.2
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** TSDV-1.1, TSDV-2.1

#### Mô tả User Story
**Với vai trò là** Người dùng hệ thống,  
**Tôi muốn** có thể xuất danh sách các tài sản và dịch vụ (dựa trên các bộ lọc hiện tại) ra file Excel hoặc các định dạng phổ biến khác,  
**Để** tôi có thể dễ dàng phân tích, báo cáo hoặc chia sẻ dữ liệu ngoại tuyến khi cần.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xuất file" (ví dụ: Xuất Excel)
- [ ] File xuất ra bao gồm đầy đủ các trường thông tin hiển thị của tài sản/dịch vụ
- [ ] Có thể xuất toàn bộ danh sách hoặc chỉ các mục đã chọn
- [ ] Có thể xuất dựa trên bộ lọc hiện tại
- [ ] Hỗ trợ nhiều định dạng file (Excel, PDF, CSV)
- [ ] Có thể tùy chỉnh các cột xuất ra
- [ ] Có thể đặt tên file xuất
- [ ] Có thể lên lịch xuất file định kỳ
- [ ] Có thể chia sẻ file xuất qua email hoặc link
- [ ] Có thể xem lịch sử xuất file và tải lại

---

### Functional Requirements

#### Core Features
1. **Export Functionality**
   - Single export
   - Bulk export
   - Scheduled export
   - Custom export

2. **File Formats**
   - Excel (.xlsx, .xls)
   - PDF (.pdf)
   - CSV (.csv)
   - JSON (.json)

3. **Export Options**
   - All records
   - Selected records
   - Filtered records
   - Custom range

4. **Customization**
   - Column selection
   - Formatting options
   - Template selection
   - Layout customization

#### Business Rules
- Chỉ xuất dữ liệu mà người dùng có quyền xem
- File xuất phải bao gồm thông tin đầy đủ và chính xác
- Có thể lưu và tái sử dụng cấu hình xuất
- File xuất phải có định dạng chuẩn và dễ đọc
- Có thể chia sẻ file xuất với người khác

#### Export Types
1. **Basic Export**
   - All assets/services
   - Selected items
   - Current filtered results

2. **Advanced Export**
   - Custom date range
   - Specific categories
   - Status-based export
   - Project-based export

3. **Report Export**
   - Summary report
   - Detailed report
   - Statistical report
   - Comparative report

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử xuất file
CREATE TABLE asset_service_export_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    export_name VARCHAR(200) NOT NULL,
    export_type ENUM('all', 'selected', 'filtered', 'custom') NOT NULL,
    export_format ENUM('xlsx', 'xls', 'pdf', 'csv', 'json') NOT NULL,
    export_config JSON NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    row_count INT DEFAULT 0,
    column_count INT DEFAULT 0,
    export_criteria JSON,
    exported_by INT NOT NULL,
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_scheduled BOOLEAN DEFAULT FALSE,
    schedule_id INT NULL,
    download_count INT DEFAULT 0,
    last_downloaded_at TIMESTAMP NULL,
    
    FOREIGN KEY (exported_by) REFERENCES users(id),
    INDEX idx_export_type (export_type),
    INDEX idx_export_format (export_format),
    INDEX idx_exported_by (exported_by),
    INDEX idx_exported_at (exported_at)
);

-- Bảng cấu hình xuất file
CREATE TABLE asset_service_export_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_name VARCHAR(200) NOT NULL,
    config_description TEXT,
    export_format ENUM('xlsx', 'xls', 'pdf', 'csv', 'json') NOT NULL,
    column_config JSON NOT NULL,
    format_config JSON NOT NULL,
    template_config JSON,
    is_default BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_export_format (export_format),
    INDEX idx_is_default (is_default)
);

-- Bảng lịch xuất file
CREATE TABLE asset_service_export_schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_name VARCHAR(200) NOT NULL,
    schedule_description TEXT,
    export_config_id INT NOT NULL,
    schedule_type ENUM('daily', 'weekly', 'monthly', 'custom') NOT NULL,
    schedule_config JSON NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMP NULL,
    next_run_at TIMESTAMP NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (export_config_id) REFERENCES asset_service_export_config(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_schedule_type (schedule_type),
    INDEX idx_is_active (is_active)
);

-- Insert default export configurations
INSERT INTO asset_service_export_config (config_name, config_description, export_format, column_config, format_config, is_default) VALUES
('Cấu hình xuất Excel chuẩn', 'Cấu hình xuất Excel với đầy đủ thông tin', 'xlsx', 
'{"columns": ["code", "name", "type", "category", "status", "responsible_person", "location", "purchase_cost", "current_value", "created_at"]}', 
'{"date_format": "dd/MM/yyyy", "number_format": "#,##0", "currency_format": "#,##0 VND"}', true),
('Cấu hình xuất PDF báo cáo', 'Cấu hình xuất PDF cho báo cáo', 'pdf',
'{"columns": ["code", "name", "type", "category", "status", "responsible_person", "purchase_cost", "current_value"]}',
'{"page_size": "A4", "orientation": "portrait", "header": true, "footer": true}', false),
('Cấu hình xuất CSV đơn giản', 'Cấu hình xuất CSV cho dữ liệu thô', 'csv',
'{"columns": ["code", "name", "type", "category", "status", "responsible_person", "purchase_cost"]}',
'{"encoding": "UTF-8", "delimiter": ","}', false);
```

#### API Endpoints
```typescript
# Export Assets/Services
POST /api/assets-services/export
{
  "export_type": "filtered",
  "export_format": "xlsx",
  "export_config": {
    "columns": ["code", "name", "type", "category", "status", "responsible_person", "purchase_cost", "current_value"],
    "filters": {
      "type": ["asset"],
      "status": ["active", "maintenance"]
    },
    "template_id": 1,
    "include_summary": true,
    "include_statistics": true
  },
  "file_name": "Danh sách tài sản đang hoạt động",
  "schedule_export": false
}
Response: {
  "success": true,
  "export_id": 123,
  "file_name": "Danh sách tài sản đang hoạt động_20240125_143022.xlsx",
  "file_size": 2048576,
  "download_url": "/api/assets-services/export/download/123",
  "message": "File xuất đã được tạo thành công"
}

# Get Export History
GET /api/assets-services/export/history
{
  "page": 1,
  "page_size": 20,
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "exports": [
    {
      "id": 123,
      "export_name": "Danh sách tài sản đang hoạt động",
      "export_type": "filtered",
      "export_format": "xlsx",
      "file_name": "Danh sách tài sản đang hoạt động_20240125_143022.xlsx",
      "file_size": 2048576,
      "row_count": 150,
      "column_count": 8,
      "exported_by": "Nguyễn Văn A",
      "exported_at": "2024-01-25T14:30:22Z",
      "download_count": 3
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "page_size": 20
  }
}

# Download Export File
GET /api/assets-services/export/download/{export_id}
Response: File download

# Get Export Configurations
GET /api/assets-services/export/configurations
Response: {
  "configurations": [
    {
      "id": 1,
      "config_name": "Cấu hình xuất Excel chuẩn",
      "config_description": "Cấu hình xuất Excel với đầy đủ thông tin",
      "export_format": "xlsx",
      "column_config": {
        "columns": ["code", "name", "type", "category", "status", "responsible_person", "location", "purchase_cost", "current_value", "created_at"]
      },
      "format_config": {
        "date_format": "dd/MM/yyyy",
        "number_format": "#,##0",
        "currency_format": "#,##0 VND"
      },
      "is_default": true
    }
  ]
}

# Save Export Configuration
POST /api/assets-services/export/configurations
{
  "config_name": "Cấu hình xuất tùy chỉnh",
  "config_description": "Cấu hình xuất file tùy chỉnh cho bộ phận IT",
  "export_format": "xlsx",
  "column_config": {
    "columns": ["code", "name", "type", "category", "status", "responsible_person", "purchase_cost"]
  },
  "format_config": {
    "date_format": "dd/MM/yyyy",
    "number_format": "#,##0",
    "currency_format": "#,##0 VND"
  },
  "is_public": false
}
Response: {
  "success": true,
  "config_id": 123,
  "message": "Cấu hình xuất đã được lưu thành công"
}

# Schedule Export
POST /api/assets-services/export/schedule
{
  "schedule_name": "Xuất báo cáo hàng tuần",
  "schedule_description": "Xuất báo cáo tài sản và dịch vụ hàng tuần",
  "export_config_id": 1,
  "schedule_type": "weekly",
  "schedule_config": {
    "day_of_week": 1,
    "time": "09:00",
    "timezone": "Asia/Ho_Chi_Minh"
  },
  "is_active": true
}
Response: {
  "success": true,
  "schedule_id": 123,
  "next_run_at": "2024-01-29T09:00:00Z",
  "message": "Lịch xuất file đã được tạo thành công"
}

# Share Export File
POST /api/assets-services/export/{export_id}/share
{
  "share_type": "email",
  "share_config": {
    "recipients": ["user1@company.com", "user2@company.com"],
    "subject": "Báo cáo Tài sản và Dịch vụ",
    "message": "Đính kèm báo cáo tài sản và dịch vụ theo yêu cầu",
    "expires_in_days": 7
  }
}
Response: {
  "success": true,
  "share_id": 123,
  "access_token": "abc123def456",
  "expires_at": "2024-02-01T14:30:22Z",
  "message": "File đã được chia sẻ thành công"
}

# Bulk Export
POST /api/assets-services/export/bulk
{
  "export_items": [
    {
      "export_type": "filtered",
      "export_format": "xlsx",
      "filters": {"type": ["asset"], "status": ["active"]},
      "file_name": "Tài sản đang hoạt động"
    },
    {
      "export_type": "filtered",
      "export_format": "pdf",
      "filters": {"type": ["service"], "status": ["active"]},
      "file_name": "Dịch vụ đang hoạt động"
    }
  ],
  "zip_files": true
}
Response: {
  "success": true,
  "bulk_export_id": 456,
  "total_files": 2,
  "zip_file_url": "/api/assets-services/export/bulk/download/456",
  "message": "Xuất hàng loạt đã hoàn thành"
}
```

#### Frontend Components
```typescript
// Export Interface Component
interface ExportInterfaceComponent {
  exportType: string
  exportFormat: string
  exportConfig: ExportConfig
  exportHistory: ExportHistory[]
  
  onExport: (config: ExportConfig) => Promise<void>
  onExportTypeChange: (type: string) => void
  onExportFormatChange: (format: string) => void
  onExportConfigChange: (config: ExportConfig) => void
  onExportHistorySelect: (history: ExportHistory) => void
}

// Export Configuration Component
interface ExportConfigurationComponent {
  configurations: ExportConfiguration[]
  selectedConfig: ExportConfiguration
  
  onConfigSelect: (config: ExportConfiguration) => void
  onConfigSave: (config: ExportConfiguration) => void
  onConfigEdit: (config: ExportConfiguration) => void
  onConfigDelete: (configId: number) => void
}

// Column Selection Component
interface ColumnSelectionComponent {
  availableColumns: ColumnOption[]
  selectedColumns: string[]
  
  onColumnSelect: (column: string) => void
  onColumnDeselect: (column: string) => void
  onColumnReorder: (columns: string[]) => void
  onColumnSelectAll: () => void
  onColumnDeselectAll: () => void
}

// Export Format Component
interface ExportFormatComponent {
  availableFormats: ExportFormat[]
  selectedFormat: ExportFormat
  
  onFormatSelect: (format: ExportFormat) => void
  onFormatPreview: (format: ExportFormat) => void
  onFormatConfigChange: (config: FormatConfig) => void
}

// Export Schedule Component
interface ExportScheduleComponent {
  schedules: ExportSchedule[]
  newSchedule: ExportSchedule
  
  onScheduleCreate: (schedule: ExportSchedule) => void
  onScheduleEdit: (schedule: ExportSchedule) => void
  onScheduleDelete: (scheduleId: number) => void
  onScheduleToggle: (scheduleId: number, isActive: boolean) => void
}

// Export History Component
interface ExportHistoryComponent {
  exportHistory: ExportHistory[]
  pagination: PaginationInfo
  
  onHistorySelect: (history: ExportHistory) => void
  onHistoryDownload: (history: ExportHistory) => void
  onHistoryShare: (history: ExportHistory) => void
  onHistoryDelete: (historyId: number) => void
  onPageChange: (page: number) => void
}

// Export Share Component
interface ExportShareComponent {
  exportHistory: ExportHistory
  shareConfig: ShareConfig
  
  onShareViaEmail: (config: ShareConfig) => void
  onShareViaLink: (config: ShareConfig) => void
  onShareViaInternal: (config: ShareConfig) => void
  onShareConfigChange: (config: ShareConfig) => void
}

// Bulk Export Component
interface BulkExportComponent {
  exportItems: BulkExportItem[]
  
  onItemAdd: (item: BulkExportItem) => void
  onItemRemove: (itemId: string) => void
  onItemEdit: (item: BulkExportItem) => void
  onBulkExport: () => Promise<void>
  onZipFilesToggle: (zipFiles: boolean) => void
}

// Export Progress Component
interface ExportProgressComponent {
  exportProgress: ExportProgress
  
  onProgressUpdate: (progress: ExportProgress) => void
  onExportComplete: (result: ExportResult) => void
  onExportCancel: () => void
  onExportRetry: () => void
}
```

---

### UI/UX Design

#### Export Interface Layout
- **Export Layout:**
  - Export type selection
  - Format selection
  - Configuration panel
  - Preview area

#### Export Configuration Panel
- **Configuration Design:**
  - Column selection
  - Format options
  - Template selection
  - Custom settings

#### Export History Interface
- **History Layout:**
  - Export list
  - Download buttons
  - Share options
  - Delete actions

#### Export Progress Interface
- **Progress Design:**
  - Progress bar
  - Status messages
  - Cancel button
  - Completion notification

---

### Integration Requirements

#### File Generation Integration
1. **Excel Generation**
   - Excel library integration
   - Multiple sheets
   - Formatting options
   - Charts and graphs

2. **PDF Generation**
   - PDF library integration
   - Professional layout
   - Table formatting
   - Header and footer

3. **CSV Generation**
   - CSV library integration
   - UTF-8 encoding
   - Custom delimiters
   - Data validation

#### Storage Integration
1. **File Storage**
   - Local file system
   - Cloud storage
   - Temporary storage
   - Cleanup processes

2. **File Management**
   - File organization
   - Access control
   - Download tracking
   - Expiration handling

---

### Security Considerations

#### Data Protection
- Export permission validation
- Data filtering by user rights
- File access control
- Audit logging

#### File Security
- File encryption
- Secure download links
- Access token management
- File expiration

---

### Testing Strategy

#### Unit Tests
- Export logic validation
- File format generation
- Configuration handling
- Template processing

#### Integration Tests
- File generation integration
- Storage system integration
- Email sharing integration
- Download system testing

#### User Acceptance Tests
- Export workflow
- File format validation
- Download functionality
- Share functionality

---

### Deployment & Configuration

#### Environment Setup
- File generation libraries
- Storage configuration
- Email service setup
- Export scheduling

#### Monitoring & Logging
- Export performance monitoring
- File generation analytics
- Download tracking
- Error logging

---

### Documentation

#### User Manual
- Export procedures
- Format selection
- Configuration options
- Download procedures

#### Technical Documentation
- API documentation
- File generation configuration
- Integration guides
- Performance optimization 