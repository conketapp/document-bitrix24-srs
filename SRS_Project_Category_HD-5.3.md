# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-5.3
### Xuất Dữ liệu Hợp đồng ra Excel

#### Thông tin User Story
- **Story ID:** HD-5.3
- **Priority:** Medium
- **Story Points:** 4
- **Sprint:** Sprint 5
- **Status:** To Do
- **Phụ thuộc:** HD-1.1, HD-5.2

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý hoặc phụ trách hợp đồng,  
**Tôi muốn** có thể xuất toàn bộ hoặc một phần danh sách hợp đồng (dựa trên các bộ lọc hiện tại) ra file Excel,  
**Để** tôi có thể dễ dàng phân tích, báo cáo hoặc chia sẻ dữ liệu hợp đồng ngoại tuyến khi cần.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xuất Excel" trong danh mục hợp đồng
- [ ] File Excel bao gồm tất cả các trường thông tin hiển thị của hợp đồng
- [ ] Có thể xuất toàn bộ danh sách hoặc chỉ các bản ghi đã chọn
- [ ] Có thể xuất dữ liệu dựa trên bộ lọc hiện tại
- [ ] File Excel có định dạng đẹp với header, styling và formatting phù hợp
- [ ] Có thể chọn các cột cần xuất
- [ ] Hỗ trợ xuất với nhiều sheet (ví dụ: Summary, Details, Financial)
- [ ] Có thể lên lịch xuất tự động
- [ ] Hiển thị tiến trình xuất file
- [ ] Thông báo khi xuất hoàn thành
- [ ] Có thể tải xuống file ngay lập tức hoặc gửi qua email
- [ ] Hỗ trợ xuất với các template có sẵn

#### 2.4 Activity Diagram
![HD-5.3 Activity Diagram](diagrams/HD-5.3%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý xuất dữ liệu hợp đồng ra Excel*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Giao diện Xuất**
   - Vị trí nút xuất
   - Dialog tùy chọn xuất
   - Chọn cột
   - Chọn định dạng

2. **Xử lý Dữ liệu**
   - Tổng hợp dữ liệu
   - Chuyển đổi định dạng
   - Áp dụng template
   - Tối ưu hóa hiệu suất

3. **Tạo File**
   - Tạo file Excel
   - Nhiều sheet
   - Styling và formatting
   - Nén file

4. **Quản lý Xuất**
   - Lịch sử xuất
   - Xuất theo lịch
   - Quản lý template
   - Kiểm soát truy cập

#### Quy tắc Kinh doanh
- Xuất phải bao gồm tất cả thông tin hiển thị trong danh sách
- File Excel phải có định dạng chuẩn và dễ đọc
- Xuất phải tuân thủ quyền truy cập của user
- Kích thước file không được vượt quá 50MB
- Lịch sử xuất phải được lưu trữ trong 30 ngày

#### Tùy chọn Xuất
1. **Phạm vi Xuất**
   - Tất cả hợp đồng
   - Hợp đồng đã chọn
   - Hợp đồng theo bộ lọc
   - Kết quả tìm kiếm

2. **Định dạng Xuất**
   - Excel chuẩn (.xlsx)
   - Excel cũ (.xls)
   - Định dạng CSV (.csv)
   - Định dạng PDF (.pdf)

3. **Template Xuất**
   - Template cơ bản
   - Template tài chính
   - Template quản lý
   - Template tùy chỉnh

4. **Nội dung Xuất**
   - Thông tin hợp đồng
   - Dữ liệu tài chính
   - Tài liệu liên quan
   - Lịch sử hoạt động

---

#### 5.5 Sequence Diagram
![HD-5.3 Sequence Diagram](diagrams/HD-5.3%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi xuất dữ liệu hợp đồng ra Excel*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử xuất file
CREATE TABLE contract_export_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    export_name VARCHAR(200) NOT NULL,
    export_type ENUM('excel', 'csv', 'pdf') NOT NULL,
    export_scope ENUM('all', 'selected', 'filtered', 'search') NOT NULL,
    export_criteria JSON,
    selected_columns JSON,
    template_id INT,
    file_path VARCHAR(500),
    file_size BIGINT,
    record_count INT DEFAULT 0,
    export_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    error_message TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES export_templates(id),
    INDEX idx_user_id (user_id),
    INDEX idx_export_status (export_status),
    INDEX idx_started_at (started_at)
);

-- Bảng template xuất file
CREATE TABLE export_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(200) NOT NULL,
    template_description TEXT,
    template_type ENUM('basic', 'financial', 'management', 'custom') NOT NULL,
    template_config JSON NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_template_type (template_type),
    INDEX idx_is_default (is_default)
);

-- Bảng cấu hình xuất file
CREATE TABLE export_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng lịch xuất tự động
CREATE TABLE export_schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    schedule_name VARCHAR(200) NOT NULL,
    schedule_description TEXT,
    export_criteria JSON NOT NULL,
    schedule_frequency ENUM('daily', 'weekly', 'monthly') NOT NULL,
    schedule_time TIME NOT NULL,
    schedule_day VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMP NULL,
    next_run_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_active (is_active),
    INDEX idx_next_run_at (next_run_at)
);

-- Bảng cột xuất mặc định
CREATE TABLE export_columns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    column_key VARCHAR(100) NOT NULL,
    column_name VARCHAR(200) NOT NULL,
    column_description TEXT,
    data_type ENUM('text', 'number', 'date', 'currency', 'percentage') NOT NULL,
    is_default BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    is_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_column_key (column_key),
    INDEX idx_sort_order (sort_order),
    INDEX idx_is_default (is_default)
);

-- Insert default export configuration
INSERT INTO export_config (config_key, config_value, description) VALUES
('max_file_size_mb', '50', 'Maximum file size in MB'),
('max_records_per_export', '10000', 'Maximum records per export'),
('export_timeout_seconds', '300', 'Export timeout in seconds'),
('enable_background_export', 'true', 'Enable background export processing'),
('enable_email_notification', 'true', 'Enable email notification for completed exports'),
('default_template_id', '1', 'Default export template ID'),
('enable_compression', 'true', 'Enable file compression'),
('retention_days', '30', 'Export history retention in days');

-- Insert default export columns
INSERT INTO export_columns (column_key, column_name, column_description, data_type, is_default, sort_order) VALUES
('contract_code', 'Mã hợp đồng', 'Contract code', 'text', TRUE, 1),
('contract_name', 'Tên hợp đồng', 'Contract name', 'text', TRUE, 2),
('contract_type', 'Loại hợp đồng', 'Contract type', 'text', TRUE, 3),
('contract_status', 'Trạng thái', 'Contract status', 'text', TRUE, 4),
('contract_value', 'Giá trị hợp đồng', 'Contract value', 'currency', TRUE, 5),
('currency', 'Đơn vị tiền tệ', 'Currency', 'text', TRUE, 6),
('contract_start_date', 'Ngày bắt đầu', 'Contract start date', 'date', TRUE, 7),
('contract_end_date', 'Ngày kết thúc', 'Contract end date', 'date', TRUE, 8),
('effective_date', 'Ngày hiệu lực', 'Effective date', 'date', FALSE, 9),
('completion_date', 'Ngày hoàn thành', 'Completion date', 'date', FALSE, 10),
('contract_manager', 'Người quản lý', 'Contract manager', 'text', TRUE, 11),
('contract_supervisor', 'Người giám sát', 'Contract supervisor', 'text', FALSE, 12),
('tender_package', 'Gói thầu', 'Tender package', 'text', TRUE, 13),
('project', 'Dự án', 'Project', 'text', TRUE, 14),
('category', 'Danh mục', 'Category', 'text', TRUE, 15),
('payment_terms', 'Điều khoản thanh toán', 'Payment terms', 'text', FALSE, 16),
('cumulative_payment', 'Thanh toán lũy kế', 'Cumulative payment', 'currency', FALSE, 17),
('remaining_value', 'Giá trị còn lại', 'Remaining value', 'currency', FALSE, 18),
('progress_ratio', 'Tỷ lệ hoàn thành', 'Progress ratio', 'percentage', FALSE, 19),
('created_at', 'Ngày tạo', 'Created date', 'date', FALSE, 20),
('updated_at', 'Ngày cập nhật', 'Updated date', 'date', FALSE, 21);

-- Insert default export templates
INSERT INTO export_templates (template_name, template_description, template_type, template_config, is_default, created_by) VALUES
('Template Cơ bản', 'Template xuất thông tin cơ bản hợp đồng', 'basic', '{"sheets": ["Contracts"], "columns": ["contract_code", "contract_name", "contract_type", "contract_status", "contract_value", "contract_manager"]}', TRUE, 1),
('Template Tài chính', 'Template xuất thông tin tài chính hợp đồng', 'financial', '{"sheets": ["Summary", "Financial Details"], "columns": ["contract_code", "contract_name", "contract_value", "cumulative_payment", "remaining_value", "progress_ratio"]}', FALSE, 1),
('Template Quản lý', 'Template xuất thông tin quản lý hợp đồng', 'management', '{"sheets": ["Overview", "Timeline", "People"], "columns": ["contract_code", "contract_name", "contract_manager", "contract_supervisor", "contract_start_date", "contract_end_date", "progress_ratio"]}', FALSE, 1);
```

#### API Endpoints
```
# Contract Export
POST /api/contracts/export
{
  "export_type": "excel",
  "export_scope": "filtered",
  "export_criteria": {
    "contract_status": "active",
    "contract_value_min": 1000000
  },
  "selected_columns": ["contract_code", "contract_name", "contract_value", "status"],
  "template_id": 1,
  "include_formatting": true
}

# Export History
GET /api/contracts/export/history
GET /api/contracts/export/history/{export_id}
DELETE /api/contracts/export/history/{export_id}

# Export Templates
GET /api/contracts/export/templates
POST /api/contracts/export/templates
{
  "template_name": "Custom Template",
  "template_description": "Custom export template",
  "template_type": "custom",
  "template_config": {
    "sheets": ["Contracts", "Summary"],
    "columns": ["contract_code", "contract_name", "contract_value"]
  }
}

PUT /api/contracts/export/templates/{template_id}
DELETE /api/contracts/export/templates/{template_id}

# Export Configuration
GET /api/contracts/export/config
PUT /api/contracts/export/config
{
  "max_file_size_mb": 50,
  "max_records_per_export": 10000,
  "export_timeout_seconds": 300
}

# Export Columns
GET /api/contracts/export/columns
PUT /api/contracts/export/columns/{column_id}
{
  "is_default": true,
  "sort_order": 5
}

# Export Schedules
GET /api/contracts/export/schedules
POST /api/contracts/export/schedules
{
  "schedule_name": "Weekly Export",
  "schedule_description": "Weekly contract export",
  "export_criteria": {
    "contract_status": "active"
  },
  "schedule_frequency": "weekly",
  "schedule_time": "09:00:00",
  "schedule_day": "monday"
}

PUT /api/contracts/export/schedules/{schedule_id}
DELETE /api/contracts/export/schedules/{schedule_id}

# Export Progress
GET /api/contracts/export/progress/{export_id}
Response: {
  "export_id": 123,
  "status": "processing",
  "progress": 75,
  "current_record": 7500,
  "total_records": 10000,
  "estimated_time_remaining": 30
}

# Download Export
GET /api/contracts/export/download/{export_id}
GET /api/contracts/export/download/{export_id}/email
{
  "email": "user@example.com",
  "subject": "Contract Export",
  "message": "Please find attached the contract export"
}
```

#### Frontend Components
```typescript
// Export Dialog Component
interface ExportDialogComponent {
  isOpen: boolean
  isLoading: boolean
  exportOptions: ExportOptions
  
  onExport: (options: ExportOptions) => Promise<void>
  onCancel: () => void
  onTemplateSelect: (templateId: number) => void
}

// Export Options Component
interface ExportOptionsComponent {
  exportScope: ExportScope
  exportFormat: ExportFormat
  selectedColumns: string[]
  availableColumns: ExportColumn[]
  
  onScopeChange: (scope: ExportScope) => void
  onFormatChange: (format: ExportFormat) => void
  onColumnToggle: (columnKey: string) => void
  onSelectAllColumns: () => void
  onDeselectAllColumns: () => void
}

// Export Template Component
interface ExportTemplateComponent {
  templates: ExportTemplate[]
  selectedTemplate: ExportTemplate | null
  
  onTemplateSelect: (template: ExportTemplate) => void
  onTemplateCreate: (template: Partial<ExportTemplate>) => Promise<void>
  onTemplateEdit: (templateId: number) => void
  onTemplateDelete: (templateId: number) => Promise<void>
}

// Export Progress Component
interface ExportProgressComponent {
  exportId: number
  progress: ExportProgress
  
  onCancel: () => void
  onDownload: () => void
  onEmail: (email: string) => Promise<void>
}

// Export History Component
interface ExportHistoryComponent {
  exportHistory: ExportHistoryEntry[]
  isLoading: boolean
  
  onViewDetails: (exportId: number) => void
  onDownload: (exportId: number) => void
  onDelete: (exportId: number) => Promise<void>
  onReschedule: (exportId: number) => Promise<void>
}

// Export Schedule Component
interface ExportScheduleComponent {
  schedules: ExportSchedule[]
  isLoading: boolean
  
  onScheduleCreate: (schedule: Partial<ExportSchedule>) => Promise<void>
  onScheduleEdit: (scheduleId: number) => void
  onScheduleDelete: (scheduleId: number) => Promise<void>
  onScheduleToggle: (scheduleId: number, isActive: boolean) => Promise<void>
}

// Export Configuration Component
interface ExportConfigurationComponent {
  config: ExportConfig
  
  onUpdateConfig: (config: Partial<ExportConfig>) => Promise<void>
  onResetConfig: () => Promise<void>
  onTestExport: () => Promise<void>
}

// Column Selection Component
interface ColumnSelectionComponent {
  availableColumns: ExportColumn[]
  selectedColumns: string[]
  
  onColumnToggle: (columnKey: string) => void
  onColumnReorder: (fromIndex: number, toIndex: number) => void
  onSelectAll: () => void
  onDeselectAll: () => void
  onSaveSelection: (name: string) => Promise<void>
}

// Export Preview Component
interface ExportPreviewComponent {
  previewData: any[]
  selectedColumns: string[]
  
  onColumnChange: (columns: string[]) => void
  onFormatChange: (format: ExportFormat) => void
  onExport: () => Promise<void>
}
```

---

### UI/UX Design

#### Export Interface
- **Export Button:**
  - Prominent export button
  - Dropdown with export options
  - Quick export vs. advanced export

#### Export Dialog
- **Dialog Layout:**
  - Export scope selection
  - Format selection
  - Column selection
  - Template selection
  - Progress indicator

#### Export Options
- **Options Panel:**
  - Scope selection (all, selected, filtered)
  - Format selection (Excel, CSV, PDF)
  - Column selection with checkboxes
  - Template selection dropdown

#### Export Progress
- **Progress Display:**
  - Progress bar
  - Status messages
  - Estimated time remaining
  - Cancel button

---

### Integration Requirements

#### File Generation Integration
1. **Excel Generation**
   - Excel library integration
   - Multiple sheets support
   - Styling and formatting
   - Formula support

2. **Data Processing**
   - Data aggregation
   - Format conversion
   - Performance optimization
   - Memory management

#### Background Processing
1. **Export Queue**
   - Background job processing
   - Progress tracking
   - Error handling
   - Notification system

2. **File Storage**
   - Secure file storage
   - File compression
   - Access control
   - Cleanup automation

---

### Security Considerations

#### Export Security
- Role-based export permissions
- Data filtering by access rights
- Sensitive data protection
- Export audit logging

#### File Security
- Secure file generation
- Encrypted file storage
- Access control
- Download restrictions

---

### Testing Strategy

#### Unit Tests
- Export functionality testing
- Template processing
- File generation
- Performance testing

#### Integration Tests
- Background processing
- File storage integration
- Email notification
- Template management

#### User Acceptance Tests
- Export interface usability
- File download testing
- Template functionality
- Performance under load

---

### Deployment & Configuration

#### Environment Setup
- Excel library installation
- Background job configuration
- File storage setup
- Email service configuration

#### Monitoring & Logging
- Export performance monitoring
- File generation tracking
- User export behavior
- Error tracking

---

### Documentation

#### User Manual
- Export interface guide
- Template usage instructions
- Schedule management
- File download procedures

#### Technical Documentation
- API documentation
- Export architecture
- Performance optimization
- Security implementation 