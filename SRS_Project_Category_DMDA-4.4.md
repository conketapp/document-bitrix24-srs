# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### User Story: DMDA-4.4
### Báo cáo Thống kê Dự án Tổng quan

#### Thông tin User Story
- **Story ID:** DMDA-4.4
- **Priority:** High
- **Story Points:** 10
- **Sprint:** Sprint 4
- **Status:** To Do
- **Phụ thuộc:** DMDA-1.1, DMDA-3.5, DMDA-4.3

#### Mô tả User Story
**Với vai trò là** Quản lý cấp cao hoặc Cán bộ quản lý dự án,  
**Tôi muốn** có các báo cáo và thống kê về tình hình dự án (ví dụ: số lượng dự án theo từng trạng thái, số lượng dự án mới/chuyển tiếp theo năm,...),  
**Để** tôi có thể đánh giá hiệu quả làm việc, đưa ra các quyết định chiến lược và lập kế hoạch cho tương lai.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có một khu vực "Báo cáo" hoặc "Thống kê" trong module Dự án
- [ ] Báo cáo hiển thị dưới dạng biểu đồ (tròn, cột) và bảng biểu dễ hiểu
- [ ] Có thể lọc báo cáo theo năm, loại dự án, trạng thái, người phụ trách, v.v.
- [ ] Có thể export báo cáo ra Excel/PDF
- [ ] Báo cáo real-time với dữ liệu mới nhất
- [ ] Có thể drill-down vào chi tiết từ biểu đồ

#### 2.4 Activity Diagram
![DMDA-4.4 Activity Diagram](diagrams/DMDA-4.4%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý báo cáo thống kê dự án tổng quan*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Tổng quan Dashboard**
   - Tổng quan dự án theo trạng thái
   - Phân bố dự án theo loại và năm
   - Thống kê ngân sách và tiến độ
   - Chỉ số KPI cho quản lý

2. **Hiển thị Biểu đồ**
   - Biểu đồ tròn cho phân bố trạng thái
   - Biểu đồ cột cho so sánh loại dự án
   - Biểu đồ đường cho phân tích xu hướng
   - Biểu đồ donut cho phân bố ngân sách

3. **Lọc Báo cáo**
   - Lọc theo năm, loại dự án, trạng thái
   - Lọc theo người phụ trách
   - Chọn khoảng thời gian
   - So sánh khoảng thời gian tùy chỉnh

#### Quy tắc Kinh doanh
- Cập nhật dữ liệu thời gian thực
- Truy cập dựa trên phân quyền cho báo cáo
- Khả năng drill-down cho phân tích chi tiết
- Chức năng xuất cho báo cáo
- So sánh dữ liệu lịch sử

---

#### 5.5 Sequence Diagram
![DMDA-4.4 Sequence Diagram](diagrams/DMDA-4.4%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi xem báo cáo thống kê dự án*

---

### Đặc tả Kỹ thuật

#### Cập nhật Cấu trúc Cơ sở Dữ liệu
```sql
-- Bảng lưu cấu hình báo cáo
CREATE TABLE report_configurations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(100) NOT NULL,
    report_type ENUM('dashboard', 'chart', 'table', 'summary') NOT NULL,
    chart_type ENUM('pie', 'bar', 'line', 'donut', 'area') NOT NULL,
    data_source VARCHAR(100) NOT NULL,
    filters_config JSON,
    display_config JSON,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng lưu cache thống kê
CREATE TABLE statistics_cache (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cache_key VARCHAR(255) NOT NULL UNIQUE,
    cache_data JSON NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- Insert default report configurations
INSERT INTO report_configurations (report_name, report_type, chart_type, data_source, filters_config, display_config) VALUES
('Status Distribution', 'chart', 'pie', 'project_status_stats', '{"group_by": "status"}', '{"title": "Phân bố theo trạng thái", "colors": ["#10B981", "#F59E0B", "#EF4444", "#6B7280"]}'),
('Category Comparison', 'chart', 'bar', 'project_category_stats', '{"group_by": "category"}', '{"title": "So sánh theo loại dự án", "orientation": "vertical"}'),
('Budget Allocation', 'chart', 'donut', 'project_budget_stats', '{"group_by": "category"}', '{"title": "Phân bố ngân sách", "show_percentage": true}'),
('Yearly Trend', 'chart', 'line', 'project_yearly_stats', '{"group_by": "year"}', '{"title": "Xu hướng theo năm", "show_trend": true}');
```

#### API Endpoints
```
GET /api/reports/dashboard
- Request: { 
    year?: number, 
    category_id?: number, 
    status?: string, 
    user_id?: number 
}
- Response: { 
    overview: DashboardOverview, 
    charts: ChartData[], 
    tables: TableData[] 
}

GET /api/reports/chart/{chart_type}
- Request: { 
    filters: ReportFilter, 
    chart_config: ChartConfig 
}
- Response: { 
    data: ChartData, 
    metadata: ChartMetadata 
}

GET /api/reports/export
- Request: { 
    report_name: string, 
    format: 'excel' | 'pdf', 
    filters: ReportFilter 
}
- Response: { 
    download_url: string, 
    file_name: string 
}
```

#### Data Models
```typescript
interface DashboardOverview {
    total_projects: number;
    total_budget: number;
    completed_projects: number;
    pending_projects: number;
    average_completion_time: number;
    success_rate: number;
    kpi_metrics: KPIMetrics;
}

interface KPIMetrics {
    projects_this_month: number;
    budget_utilization: number;
    approval_rate: number;
    average_approval_time: number;
}

interface ChartData {
    chart_id: string;
    chart_type: 'pie' | 'bar' | 'line' | 'donut' | 'area';
    title: string;
    data: ChartDataPoint[];
    config: ChartConfig;
}

interface ChartDataPoint {
    label: string;
    value: number;
    percentage?: number;
    color?: string;
    metadata?: object;
}

interface ReportFilter {
    year?: number;
    category_id?: number;
    status?: string;
    user_id?: number;
    date_from?: string;
    date_to?: string;
    official_only?: boolean;
}
```

---

### User Interface Requirements

#### Dashboard Overview
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Báo cáo Thống kê Dự án - Dashboard                                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Bộ lọc: [Năm: 2024 ▼] [Loại: Tất cả ▼] [Nguồn gốc: Tất cả ▼] [Trạng thái: Tất cả ▼] [Người phụ   │
│ trách: Tất cả ▼] [Thời gian: Tháng này ▼] [Áp dụng] [Làm mới] [Export]      │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 📊 Tổng quan                                                                   │
│ ┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐       │
│ │ Tổng dự án  │ Tổng TMĐT   │ Tổng vốn    │ Đã phê      │ Tỷ lệ phê   │       │
│ │ 150         │ dự kiến     │ đã ứng      │ duyệt       │ duyệt 85%   │       │
│ │             │ 25.5 tỷ VND │ 15.2 tỷ VND │ 127 dự án   │             │       │
│ └─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘       │
│                                                                                 │
│ 📈 Biểu đồ                                                                     │
│ ┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐ │
│ │ Phân bố theo trạng thái             │ │ So sánh theo loại dự án             │ │
│ │ ┌─────────────────────────────────┐ │ │ ┌─────────────────────────────────┐ │ │
│ │ │ 🟢 Đã phê duyệt: 60%           │ │ │ │ ████████████████████ Đầu tư: 8  │ │ │
│ │ │ 🟡 Chờ phê duyệt: 25%          │ │ │ │ ████████████ Mua sắm: 5         │ │ │
│ │ │ 🔴 Đã từ chối: 10%             │ │ │ │ ████████ Thuê dịch vụ: 3        │ │ │
│ │ │ ⚫ Khác: 5%                     │ │ │ │ ████ Bảo trì: 2                 │ │ │
│ │ └─────────────────────────────────┘ │ │ └─────────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ └─────────────────────────────────────┘ │
│                                                                                 │
│ 📋 Bảng chi tiết                                                               │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ Dự án theo tháng                                                           │ │
│ ├─────────────────────────────────────────────────────────────────────────────┤ │
│ │ Tháng │ Tổng │ Mới │ TMĐT dự kiến │ TMĐT phê duyệt │ Vốn đã ứng │ Tỷ lệ    │ │
│ ├─────────────────────────────────────────────────────────────────────────────┤ │
│ │ 01    │ 15   │ 12  │ 2.5 tỷ VND   │ 2.2 tỷ VND     │ 1.8 tỷ VND │ 82%      │ │
│ │ 02    │ 18   │ 14  │ 3.2 tỷ VND   │ 2.9 tỷ VND     │ 2.1 tỷ VND │ 72%      │ │
│ │ 03    │ 22   │ 16  │ 4.1 tỷ VND   │ 3.7 tỷ VND     │ 2.8 tỷ VND │ 76%      │ │
│ │ 04    │ 20   │ 15  │ 3.8 tỷ VND   │ 3.4 tỷ VND     │ 2.5 tỷ VND │ 74%      │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ [Export Excel] [Export PDF] [Chia sẻ] [Lưu báo cáo]                          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Chart Detail View
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Chi tiết Biểu đồ - Phân bố theo trạng thái                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🟢 Đã phê duyệt (90 dự án - 60%)                                          │ │
│ │ • Dự án đầu tư: 45 dự án                                                  │ │
│ │ • Dự án mua sắm: 30 dự án                                                 │ │
│ │ • Dự án thuê dịch vụ: 15 dự án                                            │ │
│ │                                                                             │ │
│ │ 🟡 Chờ phê duyệt (37 dự án - 25%)                                         │ │
│ │ • Dự án đầu tư: 20 dự án                                                  │ │
│ │ • Dự án mua sắm: 12 dự án                                                 │ │
│ │ • Dự án thuê dịch vụ: 5 dự án                                             │ │
│ │                                                                             │ │
│ │ 🔴 Đã từ chối (15 dự án - 10%)                                             │ │
│ │ • Dự án đầu tư: 8 dự án                                                   │ │
│ │ • Dự án mua sắm: 5 dự án                                                  │ │
│ │ • Dự án thuê dịch vụ: 2 dự án                                             │ │
│ │                                                                             │ │
│ │ ⚫ Khác (8 dự án - 5%)                                                     │ │
│ │ • Dự án đang thực hiện: 5 dự án                                           │ │
│ │ • Dự án hoàn thành: 3 dự án                                               │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ [Quay lại] [Export] [Chia sẻ] [Drill-down]                                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Report Filter Panel
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Bộ lọc Báo cáo                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Thời gian:                                                                     │
│ ☑️ Tháng này                                                                   │
│ ☐ Quý này                                                                      │
│ ☐ Năm này                                                                      │
│ ☐ Tùy chọn: [Từ ngày] [Đến ngày]                                             │
│                                                                                 │
│ Năm: [2024 ▼]                                                                  │
│                                                                                 │
│ Loại dự án:                                                                    │
│ ☑️ Tất cả                                                                      │
│ ☐ Dự án Đầu tư                                                                │
│ ☐ Dự án Mua sắm                                                               │
│ ☐ Dự án Thuê dịch vụ                                                          │
│ ☐ Dự án Bảo trì                                                               │
│                                                                                 │
│ Nguồn gốc dự án:                                                              │
│ ☑️ Tất cả                                                                      │
│ ☐ Dự án Mới                                                                   │
│ ☐ Dự án Chuyển tiếp                                                           │
│                                                                                 │
│ Trạng thái:                                                                    │
│ ☑️ Tất cả                                                                      │
│ ☐ Đã phê duyệt                                                                │
│ ☐ Chờ phê duyệt                                                               │
│ ☐ Đã từ chối                                                                   │
│ ☐ Đang thực hiện                                                               │
│ ☐ Hoàn thành                                                                   │
│                                                                                 │
│ Người phụ trách:                                                              │
│ ☑️ Tất cả                                                                      │
│ ☐ Nguyễn Văn A                                                                │
│ ☐ Trần Thị B                                                                   │
│ ☐ Lê Văn C                                                                     │
│                                                                                 │
│ Dự án chính thức:                                                             │
│ ☑️ Tất cả                                                                      │
│ ☐ Chỉ dự án chính thức                                                        │
│ ☐ Chỉ dự án không chính thức                                                  │
│                                                                                 │
│ [Áp dụng] [Xóa bộ lọc] [Lưu bộ lọc]                                          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### Integration Requirements

#### Chart Library Integration
- Use Chart.js hoặc D3.js cho visualizations
- Responsive charts cho mobile/tablet
- Interactive charts với drill-down
- Export charts as images

#### Data Processing
- Real-time data aggregation
- Caching cho performance
- Batch processing cho large datasets
- Data validation và error handling

---

### Testing Requirements

#### Unit Tests
```typescript
describe('Project Reports', () => {
    test('should generate dashboard overview', async () => {
        const filters = {
            year: 2024,
            category_id: 1,
            status: 'approved'
        };
        
        const dashboard = await generateDashboardOverview(filters);
        expect(dashboard.total_projects).toBeGreaterThan(0);
        expect(dashboard.total_budget).toBeGreaterThan(0);
        expect(dashboard.kpi_metrics).toBeDefined();
    });

    test('should generate chart data correctly', async () => {
        const chartConfig = {
            chart_type: 'pie',
            data_source: 'project_status_stats',
            filters: { year: 2024 }
        };
        
        const chartData = await generateChartData(chartConfig);
        expect(chartData.data).toHaveLength(4); // 4 status types
        expect(chartData.data[0].label).toBe('Đã phê duyệt');
        expect(chartData.data[0].value).toBeGreaterThan(0);
    });

    test('should apply filters correctly', async () => {
        const filters = {
            year: 2024,
            category_id: 1,
            official_only: true
        };
        
        const projects = await getFilteredProjects(filters);
        expect(projects.every(p => p.year === 2024)).toBe(true);
        expect(projects.every(p => p.category_id === 1)).toBe(true);
        expect(projects.every(p => p.is_official === true)).toBe(true);
    });
});
```

---

### Success Criteria
- [ ] Dashboard hiển thị đầy đủ thống kê
- [ ] Biểu đồ hoạt động chính xác và responsive
- [ ] Filter báo cáo hoạt động đúng
- [ ] Export reports thành công
- [ ] Real-time updates hoạt động
- [ ] Drill-down functionality hoạt động
- [ ] Performance tốt với large datasets
- [ ] Mobile responsive design

---

### Report Configuration Rules

#### Default Charts
| Chart Name | Chart Type | Data Source | Description |
|-------------|------------|-------------|-------------|
| Status Distribution | Pie | project_status_stats | Phân bố theo trạng thái |
| Category Comparison | Bar | project_category_stats | So sánh theo loại dự án |
| Budget Allocation | Donut | project_budget_stats | Phân bố ngân sách |
| Yearly Trend | Line | project_yearly_stats | Xu hướng theo năm |

#### KPI Metrics
| Metric | Description | Calculation |
|--------|-------------|-------------|
| Total Projects | Tổng số dự án | COUNT(projects) |
| Total Budget | Tổng ngân sách | SUM(budget) |
| Completion Rate | Tỷ lệ hoàn thành | completed/total * 100 |
| Approval Rate | Tỷ lệ phê duyệt | approved/total * 100 |
| Average Approval Time | Thời gian phê duyệt TB | AVG(approval_time) |

#### Cache Configuration
| Cache Type | TTL | Description |
|------------|-----|-------------|
| Dashboard Data | 5 minutes | Real-time dashboard data |
| Chart Data | 10 minutes | Chart statistics |
| Report Data | 30 minutes | Full report data |
| Historical Data | 1 hour | Historical statistics |

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 4 