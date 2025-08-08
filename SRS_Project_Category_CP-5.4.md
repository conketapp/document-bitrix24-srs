# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-5.4
### Xuất Dữ liệu Chi phí ra Excel

#### Thông tin User Story
- **Story ID:** CP-5.4
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 5
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-2.1, CP-5.2, CP-5.3

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý hoặc phụ trách chi phí,  
**Tôi muốn** có thể xuất toàn bộ hoặc một phần danh sách chi phí (dựa trên các bộ lọc và báo cáo hiện tại) ra file Excel  
**Để** tôi có thể dễ dàng phân tích, báo cáo hoặc chia sẻ dữ liệu chi phí ngoại tuyến khi cần.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xuất Excel" trong danh sách chi phí và báo cáo
- [ ] File Excel bao gồm tất cả các trường thông tin hiển thị của chi phí
- [ ] Có thể xuất toàn bộ danh sách hoặc chỉ các mục đã chọn
- [ ] Có thể xuất dữ liệu đã được lọc theo các tiêu chí hiện tại
- [ ] File Excel có định dạng đẹp với header, bảng tính và tổng hợp
- [ ] Có thể chọn các cột cụ thể để xuất
- [ ] Có thể xuất nhiều sheet trong cùng một file Excel
- [ ] File Excel có tên tự động với timestamp
- [ ] Có thể xuất cả dữ liệu chi tiết và báo cáo tổng hợp
- [ ] Hỗ trợ xuất với các định dạng Excel khác nhau (.xlsx, .xls)
- [ ] Có thể xuất với hoặc không có định dạng (formatting)
- [ ] Có thể xuất dữ liệu từ các báo cáo đã tạo
- [ ] Có thể lên lịch xuất tự động
- [ ] Có thể gửi file Excel qua email

---

### Functional Requirements

#### Core Features
1. **Export Options**
   - Export all cost items
   - Export selected items only
   - Export filtered data
   - Export report data
   - Export with custom columns

2. **Excel Formatting**
   - Professional formatting
   - Multiple worksheets
   - Headers and footers
   - Auto-sizing columns
   - Color coding

3. **Export Configuration**
   - Column selection
   - Data range selection
   - Format options
   - File naming
   - Email delivery

4. **Scheduled Export**
   - Automated export
   - Email delivery
   - File storage
   - Export history

#### Business Rules
- Chỉ xuất dữ liệu mà người dùng có quyền xem
- File Excel phải có định dạng chuẩn và dễ đọc
- Tên file phải có timestamp để tránh trùng lặp
- Dữ liệu xuất phải chính xác và đầy đủ
- Có thể xuất với hoặc không có định dạng

#### Export Types
1. **Cost List Export**
   - All cost items
   - Filtered cost items
   - Selected cost items
   - Custom column selection

2. **Report Export**
   - Summary reports
   - Detailed reports
   - Comparative reports
   - Chart data export

3. **Analysis Export**
   - Cost analysis
   - Trend analysis
   - Budget comparison
   - Performance metrics

4. **Custom Export**
   - User-defined columns
   - Custom formatting
   - Multiple sheets
   - Calculated fields

#### Export Formats
1. **Excel Formats**
   - .xlsx (Excel 2007+)
   - .xls (Excel 97-2003)
   - .csv (Comma separated)

2. **Formatting Options**
   - With formatting
   - Without formatting
   - Custom formatting
   - Template-based

3. **Content Options**
   - All data
   - Summary only
   - Selected columns
   - Calculated fields

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử xuất Excel
CREATE TABLE cost_export_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    export_name VARCHAR(200) NOT NULL,
    export_type ENUM('cost_list', 'report', 'analysis', 'custom') NOT NULL,
    export_config JSON NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    row_count INT DEFAULT 0,
    column_count INT DEFAULT 0,
    export_format ENUM('xlsx', 'xls', 'csv') DEFAULT 'xlsx',
    exported_by INT NOT NULL,
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_scheduled BOOLEAN DEFAULT FALSE,
    schedule_id INT NULL,
    
    FOREIGN KEY (exported_by) REFERENCES users(id),
    INDEX idx_export_type (export_type),
    INDEX idx_exported_by (exported_by),
    INDEX idx_exported_at (exported_at),
    INDEX idx_is_scheduled (is_scheduled)
);

-- Bảng cấu hình xuất Excel
CREATE TABLE cost_export_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_name VARCHAR(100) NOT NULL,
    config_description TEXT,
    export_type ENUM('cost_list', 'report', 'analysis', 'custom') NOT NULL,
    column_config JSON NOT NULL,
    format_config JSON NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE KEY unique_config_name (config_name),
    INDEX idx_export_type (export_type),
    INDEX idx_is_default (is_default)
);

-- Bảng lịch trình xuất Excel
CREATE TABLE cost_export_schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_name VARCHAR(200) NOT NULL,
    export_config_id INT NOT NULL,
    schedule_type ENUM('daily', 'weekly', 'monthly', 'quarterly', 'yearly') NOT NULL,
    schedule_config JSON NOT NULL,
    recipients JSON,
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMP NULL,
    next_run_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (export_config_id) REFERENCES cost_export_config(id),
    INDEX idx_export_config_id (export_config_id),
    INDEX idx_is_active (is_active),
    INDEX idx_next_run_at (next_run_at)
);

-- Bảng template xuất Excel
CREATE TABLE cost_export_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(100) NOT NULL,
    template_description TEXT,
    template_type ENUM('cost_list', 'report', 'analysis', 'custom') NOT NULL,
    template_config JSON NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_template_name (template_name),
    INDEX idx_template_type (template_type),
    INDEX idx_sort_order (sort_order)
);

-- Insert default export templates
INSERT INTO cost_export_templates (template_name, template_description, template_type, template_config, sort_order) VALUES
('cost_list_basic', 'Xuất danh sách chi phí cơ bản', 'cost_list', '{"columns": ["cost_code", "cost_name", "total_amount", "paid_amount", "payment_status", "approval_status"], "formatting": true}', 1),
('cost_list_detailed', 'Xuất danh sách chi phí chi tiết', 'cost_list', '{"columns": ["cost_code", "cost_name", "cost_category", "supplier", "total_amount", "paid_amount", "payment_status", "approval_status", "created_at", "updated_at"], "formatting": true}', 2),
('cost_report_summary', 'Xuất báo cáo tổng hợp chi phí', 'report', '{"sheets": ["summary", "by_category", "by_supplier"], "formatting": true, "charts": true}', 3),
('cost_analysis_comparison', 'Xuất phân tích so sánh chi phí', 'analysis', '{"sheets": ["comparison", "trend", "variance"], "formatting": true, "charts": true}', 4);
```

#### API Endpoints
```typescript
# Export Cost List to Excel
POST /api/cost-export/export-list
{
  "export_type": "cost_list",
  "export_config": {
    "columns": ["cost_code", "cost_name", "cost_category", "supplier", "total_amount", "paid_amount", "payment_status", "approval_status"],
    "filters": {
      "cost_status": ["active", "approved"],
      "payment_status": ["pending", "partial", "paid"],
      "date_from": "2024-01-01",
      "date_to": "2024-12-31"
    },
    "formatting": true,
    "include_summary": true
  },
  "file_name": "cost_list_2024_01_25",
  "export_format": "xlsx"
}
Response: {
  "success": true,
  "export_id": "EXP-2024-001",
  "file_name": "cost_list_2024_01_25_20240125_143022.xlsx",
  "file_size": 245760,
  "row_count": 150,
  "column_count": 8,
  "download_url": "/api/cost-export/download/EXP-2024-001"
}

# Export Report to Excel
POST /api/cost-export/export-report
{
  "report_id": 123,
  "export_config": {
    "sheets": ["summary", "by_category", "by_supplier", "details"],
    "formatting": true,
    "charts": true,
    "include_charts": true
  },
  "file_name": "cost_report_project_A",
  "export_format": "xlsx"
}
Response: {
  "success": true,
  "export_id": "EXP-2024-002",
  "file_name": "cost_report_project_A_20240125_143022.xlsx",
  "file_size": 512000,
  "sheets": ["summary", "by_category", "by_supplier", "details"],
  "download_url": "/api/cost-export/download/EXP-2024-002"
}

# Get Export Templates
GET /api/cost-export/templates
{
  "export_type": "cost_list"
}
Response: {
  "templates": [
    {
      "id": 1,
      "template_name": "cost_list_basic",
      "template_description": "Xuất danh sách chi phí cơ bản",
      "template_type": "cost_list",
      "template_config": {
        "columns": ["cost_code", "cost_name", "total_amount", "paid_amount", "payment_status", "approval_status"],
        "formatting": true
      }
    },
    {
      "id": 2,
      "template_name": "cost_list_detailed",
      "template_description": "Xuất danh sách chi phí chi tiết",
      "template_type": "cost_list",
      "template_config": {
        "columns": ["cost_code", "cost_name", "cost_category", "supplier", "total_amount", "paid_amount", "payment_status", "approval_status", "created_at", "updated_at"],
        "formatting": true
      }
    }
  ]
}

# Save Export Configuration
POST /api/cost-export/save-config
{
  "config_name": "Xuất chi phí dự án A",
  "config_description": "Cấu hình xuất Excel cho dự án A",
  "export_type": "cost_list",
  "column_config": {
    "columns": ["cost_code", "cost_name", "cost_category", "supplier", "total_amount", "paid_amount", "payment_status", "approval_status"],
    "column_order": ["cost_code", "cost_name", "cost_category", "supplier", "total_amount", "paid_amount", "payment_status", "approval_status"]
  },
  "format_config": {
    "formatting": true,
    "auto_size": true,
    "header_style": "bold",
    "alternate_rows": true
  },
  "is_public": false
}
Response: {
  "success": true,
  "config_id": 123,
  "message": "Cấu hình xuất đã được lưu thành công"
}

# Get Export History
GET /api/cost-export/history
{
  "export_type": "cost_list",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "export_history": [
    {
      "id": 1,
      "export_name": "cost_list_2024_01_25",
      "export_type": "cost_list",
      "file_name": "cost_list_2024_01_25_20240125_143022.xlsx",
      "file_size": 245760,
      "row_count": 150,
      "column_count": 8,
      "exported_by": "Nguyễn Văn A",
      "exported_at": "2024-01-25T14:30:22Z"
    }
  ]
}

# Download Export File
GET /api/cost-export/download/{export_id}
Response: File download

# Schedule Export
POST /api/cost-export/schedule
{
  "schedule_name": "Xuất báo cáo hàng tháng",
  "export_config_id": 123,
  "schedule_type": "monthly",
  "schedule_config": {
    "day_of_month": 1,
    "time": "09:00",
    "timezone": "Asia/Ho_Chi_Minh"
  },
  "recipients": ["user1@example.com", "user2@example.com"]
}
Response: {
  "success": true,
  "schedule_id": 456,
  "next_run_at": "2024-02-01T09:00:00+07:00"
}

# Get Export Statistics
GET /api/cost-export/statistics
{
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "total_exports": 150,
  "total_file_size": 36700160,
  "by_type": {
    "cost_list": 100,
    "report": 30,
    "analysis": 20
  },
  "by_format": {
    "xlsx": 120,
    "xls": 20,
    "csv": 10
  },
  "by_user": [
    {
      "user": "Nguyễn Văn A",
      "export_count": 50,
      "total_size": 12288000
    }
  ]
}
```

#### Frontend Components
```typescript
// Export Configuration Component
interface ExportConfigComponent {
  exportType: string
  columnConfig: ColumnConfig
  formatConfig: FormatConfig
  
  onColumnChange: (columns: string[]) => void
  onFormatChange: (config: FormatConfig) => void
  onSaveConfig: (name: string) => void
  onLoadConfig: (configId: number) => void
}

// Export Template Component
interface ExportTemplateComponent {
  templates: ExportTemplate[]
  selectedTemplate: ExportTemplate | null
  
  onTemplateSelect: (template: ExportTemplate) => void
  onTemplateCustomize: (template: ExportTemplate) => void
  onTemplateSave: (template: ExportTemplate) => void
}

// Export Options Component
interface ExportOptionsComponent {
  exportOptions: ExportOptions
  
  onFormatChange: (format: string) => void
  onRangeChange: (range: ExportRange) => void
  onColumnSelect: (columns: string[]) => void
  onFormattingToggle: (enabled: boolean) => void
}

// Export Progress Component
interface ExportProgressComponent {
  exportId: string
  progress: number
  status: string
  
  onCancel: () => void
  onDownload: () => void
}

// Export History Component
interface ExportHistoryComponent {
  exportHistory: ExportHistory[]
  
  onHistorySelect: (history: ExportHistory) => void
  onHistoryDownload: (exportId: string) => void
  onHistoryDelete: (exportId: string) => void
  onHistoryResend: (exportId: string) => void
}

// Export Scheduler Component
interface ExportSchedulerComponent {
  schedules: ExportSchedule[]
  
  onCreateSchedule: (schedule: ExportSchedule) => Promise<void>
  onUpdateSchedule: (scheduleId: number, updates: Partial<ExportSchedule>) => Promise<void>
  onDeleteSchedule: (scheduleId: number) => Promise<void>
  onToggleSchedule: (scheduleId: number, active: boolean) => Promise<void>
}

// Export Statistics Component
interface ExportStatisticsComponent {
  statistics: ExportStatistics
  
  onDateRangeChange: (range: DateRange) => void
  onFilterChange: (filters: ExportFilters) => void
  onExportStatistics: () => void
}

// Export Preview Component
interface ExportPreviewComponent {
  previewData: PreviewData
  columnConfig: ColumnConfig
  
  onColumnReorder: (columns: string[]) => void
  onColumnResize: (column: string, width: number) => void
  onPreviewRefresh: () => void
}

// Export Email Component
interface ExportEmailComponent {
  exportId: string
  emailConfig: EmailConfig
  
  onRecipientAdd: (email: string) => void
  onRecipientRemove: (email: string) => void
  onSubjectChange: (subject: string) => void
  onMessageChange: (message: string) => void
  onSendEmail: () => Promise<void>
}
```

---

### UI/UX Design

#### Export Configuration Interface
- **Configuration Layout:**
  - Column selection panel
  - Format options panel
  - Preview area
  - Template library

#### Export Options Dialog
- **Options Design:**
  - Format selection
  - Range selection
  - Column selection
  - Formatting options

#### Export Progress Interface
- **Progress Design:**
  - Progress bar
  - Status messages
  - Cancel option
  - Download link

#### Export History Interface
- **History Layout:**
  - Export list
  - Filter options
  - Download actions
  - Delete options

---

### Integration Requirements

#### Excel Generation Integration
1. **Excel Library**
   - ExcelJS or similar
   - Multiple format support
   - Formatting capabilities
   - Chart generation

2. **File Management**
   - File storage
   - File cleanup
   - Download handling
   - Email attachment

#### Data Processing Integration
1. **Data Aggregation**
   - Real-time data
   - Filtered data
   - Calculated fields
   - Summary data

2. **Format Processing**
   - Column formatting
   - Cell styling
   - Header formatting
   - Summary sheets

---

### Security Considerations

#### Data Protection
- Export permission validation
- Data filtering by user rights
- File access control
- Email security

#### Export Security
- File size limits
- Export frequency limits
- Sensitive data protection
- Audit logging

---

### Testing Strategy

#### Unit Tests
- Excel generation logic
- Data formatting
- File creation
- Email delivery

#### Integration Tests
- Database export
- File system integration
- Email service testing
- Download functionality

#### User Acceptance Tests
- Export workflow
- File format validation
- Email delivery
- Performance testing

---

### Deployment & Configuration

#### Environment Setup
- Excel library installation
- File storage configuration
- Email service setup
- Schedule configuration

#### Monitoring & Logging
- Export monitoring
- File size tracking
- Error logging
- Usage analytics

---

### Documentation

#### User Manual
- Export procedures
- Template usage
- Schedule management
- File management

#### Technical Documentation
- API documentation
- Excel generation
- File handling
- Integration guides 