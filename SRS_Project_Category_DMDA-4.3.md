# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### User Story: DMDA-4.3
### Xuất Dữ liệu Danh mục Dự án ra Excel

#### Thông tin User Story
- **Story ID:** DMDA-4.3
- **Priority:** Medium
- **Story Points:** 6
- **Sprint:** Sprint 4
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-3.5

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** có thể xuất toàn bộ hoặc một phần danh mục dự án (dựa trên bộ lọc hiện tại) ra file Excel,  
**Để** tôi có thể dễ dàng phân tích, báo cáo hoặc chia sẻ dữ liệu dự án ngoại tuyến.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Xuất Excel" trong danh mục dự án
- [ ] File Excel bao gồm tất cả các trường thông tin hiển thị của dự án
- [ ] Dữ liệu được xuất ra giữ nguyên định dạng và có thể đọc được
- [ ] Có thể xuất theo bộ lọc hiện tại
- [ ] Có thể chọn các trường cần xuất
- [ ] File Excel có định dạng đẹp và dễ đọc
- [ ] Có thể xuất với nhiều sheet khác nhau
- [ ] Progress indicator cho quá trình xuất

---

### Functional Requirements

#### Core Features
1. **Export Functionality**
   - Export toàn bộ danh sách dự án
   - Export theo bộ lọc hiện tại
   - Export với custom fields selection
   - Multiple export formats (Excel, CSV, PDF)

2. **Excel Formatting**
   - Proper column headers
   - Data formatting (dates, numbers, currency)
   - Conditional formatting cho status
   - Auto-fit column widths
   - Multiple sheets cho different data

3. **Export Options**
   - Select specific fields to export
   - Choose export format
   - Set file naming convention
   - Include/exclude metadata

#### Business Rules
- Chỉ users có quyền mới có thể export
- Large exports phải có progress indicator
- File size limit cho performance
- Export history tracking
- Data validation trước khi export

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lưu lịch sử export
CREATE TABLE export_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    export_type ENUM('excel', 'csv', 'pdf') NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size BIGINT,
    record_count INT NOT NULL,
    filters_applied JSON,
    fields_exported JSON,
    export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('processing', 'completed', 'failed') DEFAULT 'processing',
    error_message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bảng cấu hình export templates
CREATE TABLE export_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    fields_config JSON NOT NULL,
    format_config JSON NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Bảng cấu hình export fields
CREATE TABLE export_field_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    field_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    field_type ENUM('text', 'number', 'date', 'currency', 'status', 'boolean') NOT NULL,
    is_required BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    format_config JSON
);

-- Insert default export fields
INSERT INTO export_field_config (field_name, display_name, field_type, is_required, sort_order) VALUES
('project_code', 'Mã dự án', 'text', TRUE, 1),
('name', 'Tên dự án', 'text', TRUE, 2),
('category_name', 'Loại dự án', 'text', TRUE, 3),
('year', 'Năm', 'number', TRUE, 4),
('start_date', 'Ngày bắt đầu', 'date', TRUE, 5),
('end_date', 'Ngày kết thúc', 'date', FALSE, 6),
('budget', 'Ngân sách (VND)', 'currency', TRUE, 7),
('status', 'Trạng thái', 'status', TRUE, 8),
('project_type', 'Loại dự án', 'text', TRUE, 9),
('is_official', 'Dự án chính thức', 'boolean', TRUE, 10),
('created_by_name', 'Người tạo', 'text', TRUE, 11),
('created_at', 'Ngày tạo', 'date', TRUE, 12);
```

#### API Endpoints
```
POST /api/projects/export
- Request: { 
    format: 'excel' | 'csv' | 'pdf',
    filters: ProjectFilter,
    fields: string[],
    template_id?: number,
    include_metadata?: boolean
}
- Response: { 
    export_id: string, 
    download_url: string, 
    estimated_time: number 
}

GET /api/projects/export/{export_id}/status
- Response: { 
    status: 'processing' | 'completed' | 'failed',
    progress: number,
    download_url?: string,
    error_message?: string 
}

GET /api/export/templates
- Response: List of available export templates

GET /api/export/history
- Response: List of export history records
```

#### Data Models
```typescript
interface ExportRequest {
    format: 'excel' | 'csv' | 'pdf';
    filters: ProjectFilter;
    fields: string[];
    template_id?: number;
    include_metadata?: boolean;
    file_name?: string;
}

interface ExportResponse {
    export_id: string;
    download_url: string;
    estimated_time: number;
    file_size?: number;
}

interface ExportStatus {
    export_id: string;
    status: 'processing' | 'completed' | 'failed';
    progress: number;
    download_url?: string;
    error_message?: string;
    record_count?: number;
}

interface ExportTemplate {
    id: number;
    name: string;
    description: string;
    fields_config: ExportFieldConfig[];
    format_config: ExportFormatConfig;
    is_default: boolean;
    created_by: number;
    created_at: string;
}

interface ExportFieldConfig {
    field_name: string;
    display_name: string;
    field_type: 'text' | 'number' | 'date' | 'currency' | 'status' | 'boolean';
    is_required: boolean;
    sort_order: number;
    format_config?: object;
}
```

---

### User Interface Requirements

#### Export Options Modal
```
┌─────────────────────────────────────────────────────────┐
│ Xuất Dữ liệu Dự án                                    │
├─────────────────────────────────────────────────────────┤
│ Định dạng xuất:                                       │
│ ○ Excel (.xlsx)                                       │
│ ○ CSV (.csv)                                          │
│ ○ PDF (.pdf)                                          │
│                                                         │
│ Phạm vi xuất:                                         │
│ ☑️ Tất cả dự án                                        │
│ ☐ Theo bộ lọc hiện tại                                 │
│ ☐ Dự án đã chọn                                       │
│                                                         │
│ Trường dữ liệu:                                        │
│ ☑️ Mã dự án                                            │
│ ☑️ Tên dự án                                           │
│ ☑️ Loại dự án                                          │
│ ☑️ Năm                                                  │
│ ☑️ Ngày bắt đầu                                         │
│ ☑️ Ngày kết thúc                                       │
│ ☑️ Ngân sách                                            │
│ ☑️ Trạng thái                                           │
│ ☑️ Loại dự án (Mới/Carryover)                          │
│ ☑️ Dự án chính thức                                     │
│ ☑️ Người tạo                                            │
│ ☑️ Ngày tạo                                             │
│ ☐ Người phê duyệt                                      │
│ ☐ Ngày phê duyệt                                       │
│                                                         │
│ Template: [Mặc định ▼]                                 │
│                                                         │
│ Tên file: [Danh_muc_du_an_2024.xlsx]                  │
│                                                         │
│ [Hủy] [Xuất Excel]                                     │
└─────────────────────────────────────────────────────────┘
```

#### Export Progress
```
┌─────────────────────────────────────────────────────────┐
│ Đang xuất dữ liệu...                                   │
├─────────────────────────────────────────────────────────┤
│ ████████████████████░░ 80%                             │
│                                                         │
│ Đã xử lý: 800/1000 dự án                              │
│ Thời gian còn lại: ~2 phút                             │
│                                                         │
│ [Hủy xuất]                                             │
└─────────────────────────────────────────────────────────┘
```

#### Excel File Structure
```
Sheet 1: Danh mục Dự án
┌─────────┬─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Mã dự án│ Tên dự án   │ Loại dự án  │ Năm     │ Ngày    │ Ngày    │ Ngân    │ Trạng   │
│         │             │             │         │ bắt đầu │ kết thúc│ sách    │ thái    │
├─────────┼─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ INV-001 │ Dự án A     │ Đầu tư      │ 2024    │ 01/03   │ 31/12   │ 500M    │ Đã phê  │
│ INV-002 │ Dự án B     │ Mua sắm     │ 2024    │ 15/03   │ 30/11   │ 300M    │ Chờ phê │
│ INV-003 │ Dự án C     │ Thuê dịch vụ│ 2024    │ 01/04   │ 31/12   │ 200M    │ Hoàn    │
└─────────┴─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

Sheet 2: Thống kê
┌─────────────┬─────────┬─────────────┬─────────┐
│ Loại dự án  │ Số lượng│ Tổng ngân   │ Tỷ lệ   │
│             │         │ sách (VND)  │ (%)     │
├─────────────┼─────────┼─────────────┼─────────┤
│ Đầu tư      │ 5       │ 2,500,000   │ 50%     │
│ Mua sắm     │ 3       │ 1,500,000   │ 30%     │
│ Thuê dịch vụ│ 2       │ 1,000,000   │ 20%     │
└─────────────┴─────────┴─────────────┴─────────┘
```

---

### Integration Requirements

#### Excel Generation
- Use ExcelJS hoặc similar library
- Proper formatting cho dates, numbers, currency
- Conditional formatting cho status columns
- Auto-fit column widths
- Multiple sheets với different data
- Header styling và data styling

#### File Management
- Temporary file storage
- Cleanup old export files
- File size monitoring
- Download tracking
- Export history management

---

### Testing Requirements

#### Unit Tests
```typescript
describe('Project Export', () => {
    test('should generate Excel file with correct data', async () => {
        const projects = [
            {
                id: 1,
                project_code: 'INV-001',
                name: 'Dự án A',
                category_name: 'Đầu tư',
                year: 2024,
                budget: 500000000,
                status: 'approved'
            }
        ];
        
        const exportRequest = {
            format: 'excel',
            filters: {},
            fields: ['project_code', 'name', 'category_name', 'year', 'budget', 'status']
        };
        
        const result = await exportProjects(exportRequest);
        expect(result.export_id).toBeDefined();
        expect(result.download_url).toBeDefined();
    });

    test('should apply filters correctly', async () => {
        const filters = {
            year: 2024,
            status: 'approved',
            official_only: true
        };
        
        const projects = await getFilteredProjects(filters);
        expect(projects.every(p => p.year === 2024)).toBe(true);
        expect(projects.every(p => p.status === 'approved')).toBe(true);
    });

    test('should track export history', async () => {
        const exportId = 'exp_123';
        const userId = 1;
        
        await trackExportHistory(exportId, userId, {
            format: 'excel',
            record_count: 100,
            file_size: 2048000
        });
        
        const history = await getExportHistory(userId);
        expect(history).toHaveLength(1);
        expect(history[0].export_type).toBe('excel');
    });
});
```

---

### Success Criteria
- [ ] Export Excel hoạt động với đầy đủ dữ liệu
- [ ] File Excel có định dạng đẹp và dễ đọc
- [ ] Export theo bộ lọc hoạt động chính xác
- [ ] Progress indicator hiển thị đúng
- [ ] Export history được ghi lại
- [ ] File download hoạt động
- [ ] Performance tốt với large datasets
- [ ] Error handling hoạt động

---

### Export Configuration Rules

#### Default Export Fields
| Field Name | Display Name | Type | Required | Sort Order |
|------------|--------------|------|----------|------------|
| project_code | Mã dự án | text | Yes | 1 |
| name | Tên dự án | text | Yes | 2 |
| category_name | Loại dự án | text | Yes | 3 |
| year | Năm | number | Yes | 4 |
| start_date | Ngày bắt đầu | date | Yes | 5 |
| end_date | Ngày kết thúc | date | No | 6 |
| budget | Ngân sách (VND) | currency | Yes | 7 |
| status | Trạng thái | status | Yes | 8 |
| project_type | Loại dự án | text | Yes | 9 |
| is_official | Dự án chính thức | boolean | Yes | 10 |
| created_by_name | Người tạo | text | Yes | 11 |
| created_at | Ngày tạo | date | Yes | 12 |

#### Export Formats
| Format | Extension | Description | Use Case |
|--------|-----------|-------------|----------|
| Excel | .xlsx | Full formatting, multiple sheets | Reports, analysis |
| CSV | .csv | Simple text format | Data import |
| PDF | .pdf | Fixed layout | Sharing, printing |

#### File Size Limits
| Export Type | Max Records | Max File Size | Timeout |
|-------------|-------------|---------------|---------|
| Excel | 10,000 | 50 MB | 10 minutes |
| CSV | 50,000 | 100 MB | 15 minutes |
| PDF | 1,000 | 20 MB | 5 minutes |

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 4 