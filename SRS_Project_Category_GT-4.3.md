# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-4.3
### Xuất Dữ liệu Gói thầu ra Excel

#### Thông tin User Story
- **Story ID:** GT-4.3
- **Priority:** Medium
- **Story Points:** 5
- **Sprint:** Sprint 4
- **Status:** To Do
- **Dependencies:** GT-1.1, GT-4.2

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý hoặc phụ trách gói thầu,  
**Tôi muốn** có thể xuất toàn bộ hoặc một phần danh sách gói thầu (dựa trên các bộ lọc hiện tại) ra file Excel,  
**Để** tôi có thể dễ dàng phân tích, báo cáo hoặc chia sẻ dữ liệu gói thầu ngoại tuyến khi cần.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xuất Excel" trong danh mục gói thầu
- [ ] File Excel bao gồm tất cả các trường thông tin hiển thị của gói thầu
- [ ] Có thể xuất toàn bộ danh sách hoặc chỉ các gói thầu đã được lọc
- [ ] Có thể chọn các cột cụ thể để xuất
- [ ] File Excel có định dạng đẹp với header, styling và formatting phù hợp
- [ ] Có thể xuất nhiều sheet trong cùng một file Excel
- [ ] Hỗ trợ xuất với các bộ lọc hiện tại (tìm kiếm, lọc theo trạng thái, v.v.)
- [ ] Có thể lên lịch xuất tự động và gửi qua email
- [ ] Hiển thị tiến trình xuất và thông báo khi hoàn thành
- [ ] Có thể tải xuống file ngay lập tức hoặc nhận thông báo khi sẵn sàng

#### 2.4 Activity Diagram
![GT-4.3 Activity Diagram](diagrams/GT-4.3%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý xuất dữ liệu gói thầu ra Excel*

---

### Functional Requirements

#### Core Features
1. **Export Interface**
   - Export button trong list view
   - Export options modal
   - Column selection interface
   - Filter-based export
   - Scheduled export

2. **Excel Generation**
   - Multiple worksheet support
   - Professional formatting
   - Data validation
   - Formulas và calculations
   - Charts và graphs

3. **Export Options**
   - Full data export
   - Filtered data export
   - Selected items export
   - Custom column selection
   - Multiple format support

4. **Export Management**
   - Export history
   - Download management
   - Email notifications
   - Scheduled exports
   - Export templates

#### Business Rules
- Export limit: 50,000 records per export
- File size limit: 100MB per file
- Export timeout: 10 minutes
- Auto-cleanup: 30 days for temporary files
- Email notification cho large exports
- Background processing cho exports lớn

#### Export Data Fields
1. **Basic Information**
   - Tender code (mã gói thầu)
   - Tender name (tên gói thầu)
   - Description (mô tả)
   - Project name (tên dự án)
   - Status (trạng thái)
   - Tender method (hình thức lựa chọn)

2. **Financial Information**
   - Estimated value (giá trị dự kiến)
   - Winning bid value (giá trúng thầu)
   - Currency (đơn vị tiền tệ)
   - Budget allocation (phân bổ ngân sách)

3. **Timeline Information**
   - Start date (ngày bắt đầu)
   - End date (ngày kết thúc)
   - Created date (ngày tạo)
   - Updated date (ngày cập nhật)

4. **Document Information**
   - Document count (số lượng tài liệu)
   - Document types (loại tài liệu)
   - Last document upload (tài liệu cuối cùng)

5. **User Information**
   - Created by (người tạo)
   - Assigned to (người phụ trách)
   - Last modified by (người sửa cuối)

6. **API Integration Information**
   - Portal sync status (trạng thái đồng bộ cổng)
   - Bitrix workflow status (trạng thái workflow)
   - API call count (số lần gọi API)

---

### Technical Specifications

#### Sequence Diagram
![GT-4.3 Sequence Diagram](diagrams/GT-4.3%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi xuất dữ liệu gói thầu ra Excel*

#### Database Schema Updates
```sql
-- Bảng quản lý xuất dữ liệu
CREATE TABLE export_jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    export_name VARCHAR(255) NOT NULL,
    export_type ENUM('excel', 'csv', 'pdf') NOT NULL,
    export_scope ENUM('all', 'filtered', 'selected') NOT NULL,
    filters JSON,
    selected_columns JSON,
    selected_items JSON,
    file_path VARCHAR(500),
    file_size BIGINT,
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    progress_percentage INT DEFAULT 0,
    total_records INT,
    processed_records INT DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bảng lịch xuất tự động
CREATE TABLE scheduled_exports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    export_name VARCHAR(255) NOT NULL,
    schedule_type ENUM('daily', 'weekly', 'monthly', 'custom') NOT NULL,
    schedule_config JSON NOT NULL,
    export_config JSON NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMP NULL,
    next_run_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bảng template xuất dữ liệu
CREATE TABLE export_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(255) NOT NULL,
    template_description TEXT,
    export_type ENUM('excel', 'csv', 'pdf') NOT NULL,
    column_config JSON NOT NULL,
    formatting_config JSON,
    is_default BOOLEAN DEFAULT FALSE,
    is_shared BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Bảng cấu hình cột xuất
CREATE TABLE export_columns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    column_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    data_type ENUM('text', 'number', 'date', 'currency', 'boolean') NOT NULL,
    is_exportable BOOLEAN DEFAULT TRUE,
    is_default_exported BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    formatting_rules JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_column_name (column_name)
);

-- Insert default export columns
INSERT INTO export_columns (column_name, display_name, data_type, is_exportable, is_default_exported, sort_order) VALUES
-- Basic Information
('tender_code', 'Mã gói thầu', 'text', TRUE, TRUE, 1),
('tender_name', 'Tên gói thầu', 'text', TRUE, TRUE, 2),
('description', 'Mô tả', 'text', TRUE, FALSE, 3),
('project_name', 'Tên dự án', 'text', TRUE, TRUE, 4),
('status', 'Trạng thái', 'text', TRUE, TRUE, 5),
('tender_method', 'Hình thức lựa chọn', 'text', TRUE, TRUE, 6),

-- Financial Information
('estimated_value', 'Giá trị dự kiến', 'currency', TRUE, TRUE, 7),
('winning_bid_value', 'Giá trúng thầu', 'currency', TRUE, FALSE, 8),
('currency', 'Đơn vị tiền tệ', 'text', TRUE, TRUE, 9),

-- Timeline Information
('start_date', 'Ngày bắt đầu', 'date', TRUE, TRUE, 10),
('end_date', 'Ngày kết thúc', 'date', TRUE, TRUE, 11),
('created_at', 'Ngày tạo', 'date', TRUE, FALSE, 12),
('updated_at', 'Ngày cập nhật', 'date', TRUE, FALSE, 13),

-- Document Information
('document_count', 'Số lượng tài liệu', 'number', TRUE, FALSE, 14),
('document_types', 'Loại tài liệu', 'text', TRUE, FALSE, 15),
('last_document_upload', 'Tài liệu cuối cùng', 'date', TRUE, FALSE, 16),

-- User Information
('created_by_name', 'Người tạo', 'text', TRUE, FALSE, 17),
('assigned_to_name', 'Người phụ trách', 'text', TRUE, FALSE, 18),
('last_modified_by_name', 'Người sửa cuối', 'text', TRUE, FALSE, 19),

-- API Integration Information
('portal_sync_status', 'Trạng thái đồng bộ cổng', 'text', TRUE, FALSE, 20),
('bitrix_workflow_status', 'Trạng thái workflow', 'text', TRUE, FALSE, 21),
('api_call_count', 'Số lần gọi API', 'number', TRUE, FALSE, 22);

-- Insert default export templates
INSERT INTO export_templates (template_name, template_description, export_type, column_config, formatting_config, is_default) VALUES
('Tổng quan gói thầu', 'Template xuất thông tin cơ bản gói thầu', 'excel', 
 '["tender_code", "tender_name", "project_name", "status", "tender_method", "estimated_value", "start_date", "end_date"]',
 '{"header_style": {"bold": true, "background_color": "#4472C4", "font_color": "white"}, "currency_format": "VND"}',
 TRUE),
('Chi tiết gói thầu', 'Template xuất thông tin chi tiết đầy đủ', 'excel',
 '["tender_code", "tender_name", "description", "project_name", "status", "tender_method", "estimated_value", "winning_bid_value", "start_date", "end_date", "created_by_name", "assigned_to_name"]',
 '{"header_style": {"bold": true, "background_color": "#4472C4", "font_color": "white"}, "currency_format": "VND", "date_format": "dd/mm/yyyy"}',
 FALSE);
```

#### API Endpoints
```
# Export Management
POST /api/tender-packages/export
{
  "export_type": "excel",
  "export_scope": "filtered",
  "filters": {
    "status": ["in_progress", "completed"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  },
  "selected_columns": [
    "tender_code",
    "tender_name",
    "project_name",
    "status",
    "estimated_value"
  ],
  "template_id": 1
}

# Export Templates
GET /api/export/templates
POST /api/export/templates
PUT /api/export/templates/{id}
DELETE /api/export/templates/{id}

# Export Jobs
GET /api/export/jobs
GET /api/export/jobs/{id}
DELETE /api/export/jobs/{id}

# Download Export
GET /api/export/jobs/{id}/download
GET /api/export/jobs/{id}/status

# Scheduled Exports
GET /api/export/scheduled
POST /api/export/scheduled
PUT /api/export/scheduled/{id}
DELETE /api/export/scheduled/{id}

# Export Columns Configuration
GET /api/export/columns
PUT /api/export/columns/{id}
```

#### Frontend Components
```typescript
// Export Interface Component
interface ExportInterface {
  exportScope: 'all' | 'filtered' | 'selected'
  selectedColumns: string[]
  exportFormat: 'excel' | 'csv' | 'pdf'
  templateId?: number
  onExport: (config: ExportConfig) => Promise<void>
  onCancel: () => void
}

// Export Options Modal
interface ExportOptionsModal {
  isVisible: boolean
  exportConfig: ExportConfig
  availableColumns: ExportColumn[]
  availableTemplates: ExportTemplate[]
  onConfigChange: (config: ExportConfig) => void
  onExport: () => Promise<void>
  onCancel: () => void
}

// Column Selection Component
interface ColumnSelectionComponent {
  selectedColumns: string[]
  availableColumns: ExportColumn[]
  onColumnToggle: (columnName: string) => void
  onSelectAll: () => void
  onDeselectAll: () => void
  onMoveUp: (columnName: string) => void
  onMoveDown: (columnName: string) => void
}

// Export Progress Component
interface ExportProgressComponent {
  jobId: number
  progress: number
  status: 'pending' | 'processing' | 'completed' | 'failed'
  totalRecords: number
  processedRecords: number
  estimatedTimeRemaining: number
  onDownload: () => void
  onCancel: () => void
}

// Export History Component
interface ExportHistoryComponent {
  exportJobs: ExportJob[]
  onDownloadJob: (jobId: number) => void
  onDeleteJob: (jobId: number) => void
  onRerunJob: (jobId: number) => void
}

// Scheduled Export Component
interface ScheduledExportComponent {
  scheduledExports: ScheduledExport[]
  onCreateSchedule: (schedule: ScheduledExportConfig) => void
  onEditSchedule: (scheduleId: number) => void
  onDeleteSchedule: (scheduleId: number) => void
  onToggleSchedule: (scheduleId: number, isActive: boolean) => void
}

// Export Template Component
interface ExportTemplateComponent {
  templates: ExportTemplate[]
  onSaveTemplate: (template: ExportTemplate) => void
  onLoadTemplate: (templateId: number) => void
  onDeleteTemplate: (templateId: number) => void
  onShareTemplate: (templateId: number) => void
}

// Export Configuration Interface
interface ExportConfig {
  exportType: 'excel' | 'csv' | 'pdf'
  exportScope: 'all' | 'filtered' | 'selected'
  selectedColumns: string[]
  filters?: SearchFilters
  selectedItems?: number[]
  templateId?: number
  formattingOptions?: {
    headerStyle?: any
    currencyFormat?: string
    dateFormat?: string
    numberFormat?: string
  }
}
```

---

### UI/UX Design

#### Export Button
- **Layout:** Button trong toolbar hoặc dropdown menu
- **Components:**
  - Export icon
  - Dropdown với export options
  - Quick export cho default template
  - Advanced export modal trigger

#### Export Options Modal
- **Layout:** Modal với tabs
- **Components:**
  - Scope selection (All, Filtered, Selected)
  - Column selection với drag & drop
  - Template selection
  - Formatting options
  - Preview button

#### Export Progress
- **Layout:** Progress bar với details
- **Components:**
  - Progress percentage
  - Records processed/total
  - Estimated time remaining
  - Cancel button
  - Download button khi completed

#### Export History
- **Layout:** Table với action buttons
- **Components:**
  - Export job list
  - Status indicators
  - Download buttons
  - Delete buttons
  - Rerun buttons

---

### Integration Requirements

#### Excel Generation Integration
1. **Excel Library**
   - ExcelJS hoặc XLSX library
   - Multiple worksheet support
   - Professional formatting
   - Charts và graphs

2. **Data Processing**
   - Large dataset handling
   - Memory optimization
   - Background processing
   - Error handling

#### File Storage Integration
1. **Temporary Storage**
   - Secure file storage
   - Auto-cleanup
   - Access control
   - Download tracking

2. **Email Integration**
   - Email notifications
   - File attachments
   - Scheduled delivery
   - Delivery confirmation

---

### Security Considerations

#### Export Security
- Data access validation
- Export permission checking
- Sensitive data filtering
- File access control

#### Data Protection
- Secure file generation
- Temporary file cleanup
- Download link expiration
- Audit logging

#### Access Control
- Export permission validation
- Template sharing controls
- Scheduled export permissions
- Download tracking

---

### Testing Strategy

#### Unit Tests
- Export configuration validation
- Excel generation logic
- Column selection testing
- Template management

#### Integration Tests
- End-to-end export workflow
- Large dataset handling
- Email notification testing
- File download testing

#### User Acceptance Tests
- Export interface usability
- Progress tracking experience
- Download functionality
- Template management

---

### Deployment & Configuration

#### Environment Setup
- Excel library installation
- File storage configuration
- Email service setup
- Background job configuration

#### Monitoring & Logging
- Export performance tracking
- File storage monitoring
- Error tracking
- Usage analytics

---

### Documentation

#### User Manual
- Export interface guide
- Template management
- Scheduled export setup
- Download procedures

#### Technical Documentation
- API documentation
- Excel generation details
- Performance optimization
- Security implementation

---

### Validation Table

#### **Bảng Validation Form Quản lý Quyền**

##### **Thông tin Người dùng**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| User ID | user_id | INT | ID hợp lệ từ bảng users | ✅ | ID người dùng |
| Tên người dùng | user_name | VARCHAR(100) | Tên hiển thị | ✅ | Tên người dùng |
| Email | user_email | VARCHAR(100) | Email hợp lệ | ✅ | Email người dùng |
| Vai trò | user_role | ENUM | 'admin', 'manager', 'user', 'viewer' | ✅ | Vai trò người dùng |

##### **Thông tin Quyền**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Quyền xem | view_permission | BOOLEAN | true/false | ✅ | Quyền xem gói thầu |
| Quyền tạo | create_permission | BOOLEAN | true/false | ✅ | Quyền tạo gói thầu |
| Quyền chỉnh sửa | edit_permission | BOOLEAN | true/false | ✅ | Quyền chỉnh sửa |
| Quyền xóa | delete_permission | BOOLEAN | true/false | ✅ | Quyền xóa gói thầu |
| Quyền xuất báo cáo | export_permission | BOOLEAN | true/false | ✅ | Quyền xuất báo cáo |

#### **Quy tắc Validation Quyền**

##### **Validation Permission**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| User exists | Người dùng tồn tại | ID hợp lệ trong database | "Người dùng không tồn tại" |
| Role validation | Vai trò hợp lệ | Theo quy định hệ thống | "Vai trò không hợp lệ" |
| Permission logic | Logic quyền | view_permission >= edit_permission | "Quyền chỉnh sửa yêu cầu quyền xem" | 