# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-5.3
### Tổng hợp & Báo cáo Chi phí theo Dự án/Gói thầu/Hợp đồng

#### Thông tin User Story
- **Story ID:** CP-5.3
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 5
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-2.1, CP-5.2

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý hoặc phụ trách tài chính/chi phí,  
**Tôi muốn** hệ thống có khả năng tổng hợp và hiển thị báo cáo chi phí theo từng nhiều Dự án, Gói thầu hoặc Hợp đồng  
**Để** tôi có thể có cái nhìn tổng quan về tổng chi phí phát sinh cho từng hạng mục và đánh giá hiệu quả tài chính.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có một phần "Báo cáo Chi phí" trong module
- [ ] Báo cáo có thể được xem theo từng nhiều Dự án, Gói thầu hoặc Hợp đồng đã chọn
- [ ] Hiển thị tổng số tiền chi phí và danh sách các khoản mục chi phí con
- [ ] Có thể lọc báo cáo theo khoảng thời gian
- [ ] Có thể lọc theo trạng thái chi phí (đã phê duyệt, chưa phê duyệt, đã thanh toán, chưa thanh toán)
- [ ] Hiển thị tổng hợp theo danh mục chi phí
- [ ] Có thể so sánh chi phí giữa các dự án/gói thầu/hợp đồng
- [ ] Có thể xuất báo cáo ra file Excel/PDF
- [ ] Hiển thị biểu đồ và đồ thị trực quan
- [ ] Có thể drill-down để xem chi tiết từng khoản mục chi phí
- [ ] Hiển thị tỷ lệ phần trăm chi phí so với ngân sách (nếu có)
- [ ] Có thể lưu và tái sử dụng các báo cáo thường dùng

---

### Functional Requirements

#### Core Features
1. **Cost Aggregation**
   - Aggregate costs by project
   - Aggregate costs by tender package
   - Aggregate costs by contract
   - Multi-level aggregation

2. **Report Generation**
   - Standard cost reports
   - Custom report builder
   - Scheduled reports
   - Export capabilities

3. **Visual Analytics**
   - Charts and graphs
   - Trend analysis
   - Comparison views
   - Drill-down capabilities

4. **Report Management**
   - Saved reports
   - Report templates
   - Report scheduling
   - Report sharing

#### Business Rules
- Chỉ hiển thị dữ liệu mà người dùng có quyền xem
- Tổng hợp chi phí phải chính xác và real-time
- Báo cáo phải hỗ trợ nhiều định dạng xuất
- Dữ liệu phải được cập nhật theo thời gian thực
- Có thể so sánh chi phí giữa các thời kỳ

#### Report Types
1. **Project Cost Reports**: Tổng chi phí theo dự án, chi phí theo danh mục, so sánh với ngân sách
2. **Tender Package Reports**: Tổng chi phí theo gói thầu, chi phí theo nhà cung cấp, hiệu quả đấu thầu
3. **Contract Cost Reports**: Tổng chi phí theo hợp đồng, chi phí theo điều khoản, tuân thủ hợp đồng
4. **Comparative Reports**: So sánh giữa các dự án, gói thầu, hợp đồng, trend analysis

#### Report Metrics
1. **Financial Metrics**: Tổng chi phí, chi phí đã thanh toán, chi phí còn lại, tỷ lệ thanh toán
2. **Status Metrics**: Chi phí đã phê duyệt, chờ phê duyệt, bị từ chối, tỷ lệ phê duyệt
3. **Category Metrics**: Chi phí theo danh mục, loại, nhà cung cấp, thời gian
4. **Performance Metrics**: So sánh với ngân sách, hiệu quả chi phí, trend analysis, variance analysis

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng báo cáo chi phí
CREATE TABLE cost_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(200) NOT NULL,
    report_type ENUM('project', 'tender_package', 'contract', 'comparative', 'custom') NOT NULL,
    report_description TEXT,
    report_criteria JSON NOT NULL,
    report_config JSON NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_public BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_report_type (report_type),
    INDEX idx_created_by (created_by),
    INDEX idx_is_active (is_active)
);

-- Bảng thống kê báo cáo
CREATE TABLE cost_report_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    entity_type ENUM('project', 'tender_package', 'contract') NOT NULL,
    entity_id INT NOT NULL,
    report_date DATE NOT NULL,
    total_cost DECIMAL(15,2) DEFAULT 0,
    paid_cost DECIMAL(15,2) DEFAULT 0,
    remaining_cost DECIMAL(15,2) DEFAULT 0,
    approved_cost DECIMAL(15,2) DEFAULT 0,
    pending_cost DECIMAL(15,2) DEFAULT 0,
    cost_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_entity_date (entity_type, entity_id, report_date),
    INDEX idx_entity_type (entity_type),
    INDEX idx_entity_id (entity_id),
    INDEX idx_report_date (report_date)
);

-- Bảng lịch trình báo cáo
CREATE TABLE cost_report_schedules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_id INT NOT NULL,
    schedule_name VARCHAR(200) NOT NULL,
    schedule_type ENUM('daily', 'weekly', 'monthly', 'quarterly', 'yearly') NOT NULL,
    schedule_config JSON NOT NULL,
    recipients JSON,
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMP NULL,
    next_run_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (report_id) REFERENCES cost_reports(id),
    INDEX idx_report_id (report_id),
    INDEX idx_is_active (is_active),
    INDEX idx_next_run_at (next_run_at)
);
```

#### API Endpoints
```typescript
# Generate Cost Report
POST /api/cost-reports/generate
{
  "report_type": "project",
  "entity_ids": [123, 124, 125],
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "filters": {
    "cost_status": ["active", "approved"],
    "payment_status": ["pending", "partial", "paid"],
    "cost_category": ["Thiết bị", "Dịch vụ"]
  },
  "metrics": ["total_cost", "paid_cost", "remaining_cost", "approved_cost"],
  "group_by": ["cost_category", "supplier"],
  "include_details": true
}
Response: {
  "report_id": "REP-2024-001",
  "report_data": {
    "summary": {
      "total_cost": 1500000000,
      "paid_cost": 900000000,
      "remaining_cost": 600000000,
      "approved_cost": 1200000000,
      "cost_count": 150
    },
    "by_category": [
      {
        "category": "Thiết bị",
        "total_cost": 800000000,
        "paid_cost": 500000000,
        "remaining_cost": 300000000,
        "cost_count": 80
      }
    ],
    "by_supplier": [
      {
        "supplier": "Công ty ABC",
        "total_cost": 500000000,
        "paid_cost": 300000000,
        "remaining_cost": 200000000,
        "cost_count": 50
      }
    ],
    "details": [
      {
        "id": 123,
        "cost_code": "CP-2024-0001",
        "cost_name": "Chi phí thiết bị văn phòng",
        "total_amount": 50000000,
        "paid_amount": 30000000,
        "payment_status": "partial",
        "approval_status": "approved"
      }
    ]
  },
  "charts": {
    "cost_by_category": {
      "type": "pie",
      "data": [
        {"label": "Thiết bị", "value": 800000000, "percentage": 53.3},
        {"label": "Dịch vụ", "value": 700000000, "percentage": 46.7}
      ]
    },
    "cost_trend": {
      "type": "line",
      "data": [
        {"date": "2024-01", "value": 100000000},
        {"date": "2024-02", "value": 150000000}
      ]
    }
  }
}

# Get Report Statistics
GET /api/cost-reports/statistics
{
  "entity_type": "project",
  "entity_id": 123,
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "total_cost": 1500000000,
  "paid_cost": 900000000,
  "remaining_cost": 600000000,
  "approved_cost": 1200000000,
  "cost_count": 150,
  "by_category": {
    "Thiết bị": 800000000,
    "Dịch vụ": 700000000
  },
  "by_status": {
    "approved": 1200000000,
    "pending": 300000000
  },
  "by_payment": {
    "paid": 900000000,
    "partial": 400000000,
    "pending": 200000000
  },
  "trend": [
    {
      "month": "2024-01",
      "total_cost": 100000000,
      "paid_cost": 60000000
    },
    {
      "month": "2024-02",
      "total_cost": 150000000,
      "paid_cost": 90000000
    }
  ]
}

# Export Report
POST /api/cost-reports/{report_id}/export
{
  "export_format": "excel",
  "include_charts": true,
  "include_details": true
}
Response: File download with report data

# Save Custom Report
POST /api/cost-reports/save
{
  "report_name": "Báo cáo chi phí dự án A",
  "report_type": "project",
  "report_description": "Báo cáo chi phí chi tiết cho dự án A",
  "report_criteria": {
    "entity_ids": [123],
    "date_from": "2024-01-01",
    "date_to": "2024-12-31",
    "filters": {
      "cost_status": ["active", "approved"]
    }
  },
  "report_config": {
    "metrics": ["total_cost", "paid_cost", "remaining_cost"],
    "group_by": ["cost_category"],
    "charts": ["cost_by_category"]
  },
  "is_public": false
}
Response: {
  "success": true,
  "report_id": 123,
  "message": "Báo cáo đã được lưu thành công"
}
```

#### Frontend Components
```typescript
// Cost Report Component
interface CostReportComponent {
  reportType: string
  entityIds: number[]
  dateRange: DateRange
  filters: ReportFilters
  
  onGenerateReport: () => Promise<void>
  onFilterChange: (filters: ReportFilters) => void
  onExportReport: () => void
  onSaveReport: () => void
}

// Report Summary Component
interface ReportSummaryComponent {
  summary: CostSummary
  
  onViewDetails: (metric: string) => void
  onExportSummary: () => void
}

// Report Chart Component
interface ReportChartComponent {
  chartData: ChartData
  chartType: string
  chartConfig: ChartConfig
  
  onChartClick: (dataPoint: any) => void
  onChartExport: () => void
}

// Report Table Component
interface ReportTableComponent {
  tableData: TableData[]
  columns: TableColumn[]
  sortConfig: SortConfig
  
  onSortChange: (column: string, order: string) => void
  onRowClick: (row: any) => void
  onExportTable: () => void
}

// Report Builder Component
interface ReportBuilderComponent {
  reportConfig: ReportConfig
  availableMetrics: string[]
  availableCharts: string[]
  
  onConfigChange: (config: ReportConfig) => void
  onSaveTemplate: (name: string) => void
  onLoadTemplate: (templateId: number) => void
}

// Saved Reports Component
interface SavedReportsComponent {
  savedReports: SavedReport[]
  
  onReportSelect: (report: SavedReport) => void
  onReportDelete: (reportId: number) => void
  onReportEdit: (report: SavedReport) => void
  onReportShare: (report: SavedReport) => void
}

// Report Comparison Component
interface ReportComparisonComponent {
  comparisonData: ComparisonData
  
  onEntitySelect: (entities: number[]) => void
  onMetricSelect: (metrics: string[]) => void
  onComparisonTypeChange: (type: string) => void
}

// Report Drill-down Component
interface ReportDrillDownComponent {
  drillDownData: DrillDownData
  drillLevel: number
  
  onDrillDown: (dimension: string, value: any) => void
  onDrillUp: () => void
  onDrillToDetail: (item: any) => void
}
```

---

### UI/UX Design

#### Report Dashboard Layout
- **Dashboard Design:**
  - Summary cards
  - Chart widgets
  - Data tables
  - Filter panels

#### Report Builder Interface
- **Builder Layout:**
  - Drag-and-drop widgets
  - Configuration panels
  - Preview area
  - Template library

#### Report Viewer Interface
- **Viewer Design:**
  - Interactive charts
  - Sortable tables
  - Drill-down capabilities
  - Export options

#### Report Comparison Interface
- **Comparison Layout:**
  - Side-by-side views
  - Comparative charts
  - Difference highlighting
  - Trend analysis

---

### Integration Requirements

#### Cost Data Integration
1. **Data Aggregation**
   - Real-time aggregation
   - Multi-level grouping
   - Performance optimization
   - Data validation

2. **Report Generation**
   - Template-based generation
   - Custom report builder
   - Scheduled reports
   - Export functionality

#### Visualization Integration
1. **Chart Libraries**
   - Interactive charts
   - Multiple chart types
   - Responsive design
   - Export capabilities

2. **Data Presentation**
   - Tabular data
   - Summary views
   - Drill-down navigation
   - Comparison tools

---

### Security Considerations

#### Data Protection
- Report access control
- Data export security
- Schedule permission
- Template sharing

#### Report Security
- Permission validation
- Data filtering
- Export restrictions
- Audit logging

---

### Testing Strategy

#### Unit Tests
- Report generation logic
- Data aggregation
- Chart rendering
- Export functionality

#### Integration Tests
- Database aggregation
- API endpoint testing
- Chart integration
- Export testing

#### User Acceptance Tests
- Report generation workflow
- Chart interaction
- Export functionality
- Performance validation

---

### Deployment & Configuration

#### Environment Setup
- Database aggregation setup
- Chart library configuration
- Export service setup
- Schedule configuration

#### Monitoring & Logging
- Report generation monitoring
- Performance tracking
- Error logging
- Usage analytics

---

### Documentation

#### User Manual
- Report generation procedures
- Chart interaction
- Export functionality
- Schedule management

#### Technical Documentation
- API documentation
- Database schema
- Chart implementation
- Integration guides 