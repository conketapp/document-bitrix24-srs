# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-5.5
### Hiển thị các Chỉ số Tài chính & Tiến độ Tổng hợp của Dự án

#### Thông tin User Story
- **Story ID:** CP-5.5
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 5
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-1.3, CP-2.1, CP-5.2, CP-5.3

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án hoặc Quản lý cấp cao,  
**Tôi muốn** hệ thống tự động tính toán và hiển thị các chỉ số tài chính và tiến độ tổng hợp cho từng dự án trên giao diện chi tiết dự án, bao gồm các chỉ số tài chính và tiến độ quan trọng  
**Để** tôi có thể có cái nhìn toàn diện, nhanh chóng về tình hình tài chính và tiến độ thực hiện của từng dự án so với kế hoạch và tổng mức đầu tư, phục vụ công tác ra quyết định và báo cáo.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Các chỉ số này được hiển thị rõ ràng và dễ hiểu trên trang chi tiết của mỗi dự án
- [ ] Hệ thống tự động tính toán các chỉ số dựa trên dữ liệu từ Module Chi phí (các khoản chi phí đã được liên kết với dự án) và thông tin ngân sách được quản lý trong Module Dự án
- [ ] Các chỉ số được cập nhật tự động khi có thay đổi về chi phí hoặc kế hoạch trong các module liên quan
- [ ] Hiển thị đầy đủ các chỉ số: Dự kiến giải ngân, Giải ngân thực tế, Thực hiện thực tế, Nghiệm thu thực tế, Tỷ lệ hoàn thành
- [ ] Có thể xem chỉ số cho một dự án hoặc nhiều dự án cùng lúc
- [ ] Có thể lọc chỉ số theo khoảng thời gian (năm hiện tại, quý, tháng)
- [ ] Hiển thị biểu đồ và đồ thị trực quan cho các chỉ số
- [ ] Có thể so sánh chỉ số giữa các dự án
- [ ] Có thể xuất báo cáo chỉ số ra Excel/PDF
- [ ] Có thể thiết lập cảnh báo khi chỉ số vượt ngưỡng
- [ ] Hiển thị trend và dự báo cho các chỉ số
- [ ] Có thể drill-down để xem chi tiết từng chỉ số

---

### Functional Requirements

#### Core Features
1. **Financial Indicators**
   - Expected disbursement in year
   - Actual disbursement to date
   - Actual implementation to date
   - Actual acceptance to date
   - Completion ratio

2. **Progress Indicators**
   - Cumulative disbursement
   - Cumulative implementation
   - Cumulative acceptance
   - Expected completion ratio

3. **Real-time Calculation**
   - Automatic calculation
   - Real-time updates
   - Data synchronization
   - Performance optimization

4. **Multi-project Support**
   - Single project view
   - Multi-project comparison
   - Aggregated indicators
   - Project grouping

#### Business Rules
- Chỉ số được tính toán tự động dựa trên dữ liệu từ Module Chi phí
- Cập nhật real-time khi có thay đổi về chi phí hoặc kế hoạch
- Chỉ hiển thị dữ liệu mà người dùng có quyền xem
- Tính toán chính xác theo định nghĩa từng chỉ số
- Hỗ trợ xem nhiều dự án cùng lúc

#### Financial Indicators Definition
1. **Dự kiến giải ngân trong năm**: Tổng chi phí đã được lên kế hoạch hoặc dự kiến phát sinh cho dự án trong năm hiện tại
2. **Giải ngân trong năm đến hiện tại**: Tổng chi phí thực tế đã giải ngân cho dự án từ đầu năm đến ngày hiện tại
3. **Thực hiện trong năm đến hiện tại**: Tổng chi phí thực tế đã thực hiện cho dự án từ đầu năm đến ngày hiện tại
4. **Nghiệm thu trong năm đến hiện tại**: Tổng chi phí thực tế đã nghiệm thu cho dự án từ đầu năm đến ngày hiện tại
5. **Tỷ lệ hoàn thành trong năm đến hiện tại**: Tỷ lệ giữa "Giải ngân trong năm đến hiện tại" so với "Kế hoạch vốn được duyệt trong năm"
6. **Lũy kế giải ngân**: Tổng chi phí thực tế đã giải ngân cho dự án từ ngày bắt đầu dự án đến ngày hiện tại
7. **Lũy kế thực hiện**: Tổng chi phí thực tế đã thực hiện cho dự án từ ngày bắt đầu dự án đến ngày hiện tại
8. **Lũy kế nghiệm thu**: Tổng chi phí thực tế đã nghiệm thu cho dự án từ ngày bắt đầu dự án đến ngày hiện tại
9. **Tỷ lệ hoàn thành dự kiến đến hết năm**: Tỷ lệ giữa tổng chi phí đã/sẽ dự kiến giải ngân đến hết năm so với Kế hoạch vốn được duyệt trong năm

#### Display Modes
1. **Single Project View**
   - Detailed indicators for one project
   - Historical trends
   - Progress charts
   - Drill-down capabilities

2. **Multi-project Comparison**
   - Side-by-side comparison
   - Aggregated indicators
   - Ranking and sorting
   - Performance analysis

3. **Dashboard View**
   - Summary indicators
   - Key metrics
   - Alert notifications
   - Quick actions

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng chỉ số tài chính dự án
CREATE TABLE project_financial_indicators (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    indicator_date DATE NOT NULL,
    year INT NOT NULL,
    
    -- Chỉ số trong năm
    expected_disbursement_year DECIMAL(15,2) DEFAULT 0,
    actual_disbursement_ytd DECIMAL(15,2) DEFAULT 0,
    actual_implementation_ytd DECIMAL(15,2) DEFAULT 0,
    actual_acceptance_ytd DECIMAL(15,2) DEFAULT 0,
    completion_ratio_ytd DECIMAL(5,2) DEFAULT 0,
    
    -- Chỉ số lũy kế
    cumulative_disbursement DECIMAL(15,2) DEFAULT 0,
    cumulative_implementation DECIMAL(15,2) DEFAULT 0,
    cumulative_acceptance DECIMAL(15,2) DEFAULT 0,
    expected_completion_ratio DECIMAL(5,2) DEFAULT 0,
    
    -- Thông tin bổ sung
    approved_budget_year DECIMAL(15,2) DEFAULT 0,
    remaining_budget DECIMAL(15,2) DEFAULT 0,
    project_start_date DATE,
    project_end_date DATE,
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id),
    UNIQUE KEY unique_project_date (project_id, indicator_date),
    INDEX idx_project_id (project_id),
    INDEX idx_indicator_date (indicator_date),
    INDEX idx_year (year)
);

-- Bảng lịch sử chỉ số
CREATE TABLE project_indicator_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    indicator_date DATE NOT NULL,
    indicator_type ENUM('disbursement', 'implementation', 'acceptance', 'completion_ratio') NOT NULL,
    old_value DECIMAL(15,2),
    new_value DECIMAL(15,2),
    change_reason VARCHAR(500),
    changed_by INT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (changed_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_indicator_date (indicator_date),
    INDEX idx_indicator_type (indicator_type)
);

-- Bảng cấu hình chỉ số
CREATE TABLE project_indicator_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_name VARCHAR(100) NOT NULL,
    config_description TEXT,
    indicator_types JSON NOT NULL,
    display_options JSON NOT NULL,
    alert_thresholds JSON,
    is_default BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE KEY unique_config_name (config_name),
    INDEX idx_is_default (is_default)
);

-- Bảng cảnh báo chỉ số
CREATE TABLE project_indicator_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    alert_type ENUM('disbursement_exceeded', 'implementation_delayed', 'acceptance_delayed', 'completion_low') NOT NULL,
    alert_message TEXT NOT NULL,
    threshold_value DECIMAL(15,2),
    current_value DECIMAL(15,2),
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    resolved_by INT NULL,
    
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_is_active (is_active)
);

-- Bảng báo cáo chỉ số
CREATE TABLE project_indicator_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(200) NOT NULL,
    report_type ENUM('single_project', 'multi_project', 'comparison', 'summary') NOT NULL,
    project_ids JSON NOT NULL,
    report_period ENUM('daily', 'weekly', 'monthly', 'quarterly', 'yearly') NOT NULL,
    report_data JSON,
    generated_by INT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (generated_by) REFERENCES users(id),
    INDEX idx_report_type (report_type),
    INDEX idx_generated_by (generated_by),
    INDEX idx_generated_at (generated_at)
);

-- Insert default indicator configurations
INSERT INTO project_indicator_config (config_name, config_description, indicator_types, display_options, alert_thresholds, is_default) VALUES
('default_indicators', 'Cấu hình chỉ số mặc định', 
 '["expected_disbursement_year", "actual_disbursement_ytd", "actual_implementation_ytd", "actual_acceptance_ytd", "completion_ratio_ytd", "cumulative_disbursement", "cumulative_implementation", "cumulative_acceptance", "expected_completion_ratio"]',
 '{"display_mode": "cards", "show_charts": true, "show_trends": true, "show_comparison": true}',
 '{"completion_ratio_ytd": {"min": 0.8, "max": 1.2}, "expected_completion_ratio": {"min": 0.9, "max": 1.1}}',
 true);
```

#### API Endpoints
```typescript
# Get Project Financial Indicators
GET /api/project-indicators/{project_id}
{
  "date": "2024-01-25",
  "year": 2024,
  "include_history": true,
  "include_trends": true
}
Response: {
  "project_id": 123,
  "project_name": "Dự án A",
  "indicator_date": "2024-01-25",
  "year": 2024,
  "indicators": {
    "expected_disbursement_year": 1500000000,
    "actual_disbursement_ytd": 900000000,
    "actual_implementation_ytd": 800000000,
    "actual_acceptance_ytd": 750000000,
    "completion_ratio_ytd": 0.6,
    "cumulative_disbursement": 2500000000,
    "cumulative_implementation": 2200000000,
    "cumulative_acceptance": 2000000000,
    "expected_completion_ratio": 0.95
  },
  "budget_info": {
    "approved_budget_year": 1500000000,
    "remaining_budget": 600000000,
    "project_start_date": "2023-01-01",
    "project_end_date": "2024-12-31"
  },
  "trends": {
    "disbursement_trend": [
      {"month": "2024-01", "value": 100000000},
      {"month": "2024-02", "value": 150000000}
    ],
    "implementation_trend": [
      {"month": "2024-01", "value": 90000000},
      {"month": "2024-02", "value": 120000000}
    ]
  },
  "alerts": [
    {
      "alert_type": "completion_low",
      "alert_message": "Tỷ lệ hoàn thành thấp hơn kế hoạch",
      "severity": "medium",
      "threshold_value": 0.8,
      "current_value": 0.6
    }
  ]
}

# Get Multi-project Indicators
POST /api/project-indicators/multi
{
  "project_ids": [123, 124, 125],
  "date": "2024-01-25",
  "year": 2024,
  "include_comparison": true
}
Response: {
  "projects": [
    {
      "project_id": 123,
      "project_name": "Dự án A",
      "indicators": {
        "expected_disbursement_year": 1500000000,
        "actual_disbursement_ytd": 900000000,
        "completion_ratio_ytd": 0.6
      }
    },
    {
      "project_id": 124,
      "project_name": "Dự án B",
      "indicators": {
        "expected_disbursement_year": 2000000000,
        "actual_disbursement_ytd": 1200000000,
        "completion_ratio_ytd": 0.6
      }
    }
  ],
  "aggregated": {
    "total_expected_disbursement": 3500000000,
    "total_actual_disbursement": 2100000000,
    "average_completion_ratio": 0.6
  },
  "comparison": {
    "best_performing": 124,
    "worst_performing": 123,
    "performance_ranking": [124, 125, 123]
  }
}

# Calculate Indicators
POST /api/project-indicators/calculate
{
  "project_ids": [123, 124, 125],
  "date": "2024-01-25",
  "force_recalculate": false
}
Response: {
  "success": true,
  "calculated_projects": 3,
  "calculation_time": "2.5s",
  "alerts_generated": 2
}

# Get Indicator Trends
GET /api/project-indicators/{project_id}/trends
{
  "indicator_type": "disbursement",
  "period": "monthly",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "project_id": 123,
  "indicator_type": "disbursement",
  "trends": [
    {
      "period": "2024-01",
      "expected": 100000000,
      "actual": 90000000,
      "variance": -10000000,
      "variance_percentage": -10
    },
    {
      "period": "2024-02",
      "expected": 120000000,
      "actual": 150000000,
      "variance": 30000000,
      "variance_percentage": 25
    }
  ],
  "summary": {
    "total_expected": 1500000000,
    "total_actual": 1400000000,
    "total_variance": -100000000,
    "average_variance_percentage": -6.67
  }
}

# Get Indicator Alerts
GET /api/project-indicators/alerts
{
  "project_ids": [123, 124, 125],
  "severity": ["high", "critical"],
  "is_active": true
}
Response: {
  "alerts": [
    {
      "id": 1,
      "project_id": 123,
      "project_name": "Dự án A",
      "alert_type": "completion_low",
      "alert_message": "Tỷ lệ hoàn thành thấp hơn kế hoạch",
      "severity": "high",
      "threshold_value": 0.8,
      "current_value": 0.6,
      "created_at": "2024-01-25T10:30:00Z"
    }
  ],
  "summary": {
    "total_alerts": 5,
    "high_severity": 2,
    "critical_severity": 1
  }
}

# Generate Indicator Report
POST /api/project-indicators/report
{
  "report_name": "Báo cáo chỉ số tài chính tháng 1/2024",
  "report_type": "multi_project",
  "project_ids": [123, 124, 125],
  "report_period": "monthly",
  "include_charts": true,
  "include_comparison": true
}
Response: {
  "success": true,
  "report_id": "REP-2024-001",
  "report_data": {
    "summary": {
      "total_projects": 3,
      "total_expected_disbursement": 3500000000,
      "total_actual_disbursement": 2100000000,
      "average_completion_ratio": 0.6
    },
    "projects": [
      {
        "project_id": 123,
        "project_name": "Dự án A",
        "indicators": {
          "expected_disbursement_year": 1500000000,
          "actual_disbursement_ytd": 900000000,
          "completion_ratio_ytd": 0.6
        }
      }
    ],
    "charts": {
      "completion_ratio_chart": {
        "type": "bar",
        "data": [
          {"project": "Dự án A", "value": 0.6},
          {"project": "Dự án B", "value": 0.6}
        ]
      }
    }
  }
}
```

#### Frontend Components
```typescript
// Project Indicators Component
interface ProjectIndicatorsComponent {
  projectId: number
  indicators: FinancialIndicators
  trends: IndicatorTrends
  alerts: IndicatorAlert[]
  
  onIndicatorClick: (indicator: string) => void
  onTrendView: (period: string) => void
  onAlertAction: (alert: IndicatorAlert) => void
  onExportReport: () => void
}

// Multi-project Indicators Component
interface MultiProjectIndicatorsComponent {
  projectIds: number[]
  indicators: MultiProjectIndicators
  comparison: ProjectComparison
  
  onProjectSelect: (projectIds: number[]) => void
  onComparisonView: () => void
  onRankingView: () => void
  onExportComparison: () => void
}

// Indicator Dashboard Component
interface IndicatorDashboardComponent {
  dashboardData: DashboardData
  selectedPeriod: string
  
  onPeriodChange: (period: string) => void
  onFilterChange: (filters: DashboardFilters) => void
  onDrillDown: (metric: string) => void
  onRefresh: () => void
}

// Indicator Trend Component
interface IndicatorTrendComponent {
  trendData: TrendData
  indicatorType: string
  period: string
  
  onPeriodChange: (period: string) => void
  onIndicatorChange: (type: string) => void
  onTrendExport: () => void
}

// Indicator Alert Component
interface IndicatorAlertComponent {
  alerts: IndicatorAlert[]
  
  onAlertSelect: (alert: IndicatorAlert) => void
  onAlertResolve: (alertId: number) => void
  onAlertFilter: (filters: AlertFilters) => void
  onAlertExport: () => void
}

// Indicator Chart Component
interface IndicatorChartComponent {
  chartData: ChartData
  chartType: string
  chartConfig: ChartConfig
  
  onChartClick: (dataPoint: any) => void
  onChartExport: () => void
  onChartTypeChange: (type: string) => void
}

// Indicator Comparison Component
interface IndicatorComparisonComponent {
  comparisonData: ComparisonData
  
  onProjectSelect: (projects: number[]) => void
  onMetricSelect: (metrics: string[]) => void
  onComparisonTypeChange: (type: string) => void
  onExportComparison: () => void
}

// Indicator Report Component
interface IndicatorReportComponent {
  reportData: ReportData
  
  onReportGenerate: (config: ReportConfig) => void
  onReportExport: (format: string) => void
  onReportSchedule: (schedule: ReportSchedule) => void
}

// Indicator Settings Component
interface IndicatorSettingsComponent {
  settings: IndicatorSettings
  
  onThresholdChange: (thresholds: AlertThresholds) => void
  onDisplayChange: (display: DisplayOptions) => void
  onCalculationChange: (calculation: CalculationConfig) => void
  onSettingsSave: () => void
}
```

---

### UI/UX Design

#### Project Indicators Dashboard
- **Dashboard Layout:**
  - Indicator cards
  - Trend charts
  - Alert notifications
  - Quick actions

#### Multi-project Comparison Interface
- **Comparison Layout:**
  - Side-by-side comparison
  - Ranking tables
  - Performance charts
  - Filter options

#### Indicator Detail View
- **Detail Design:**
  - Detailed indicators
  - Historical trends
  - Drill-down capabilities
  - Export options

#### Alert Management Interface
- **Alert Layout:**
  - Alert list
  - Severity filters
  - Action buttons
  - Resolution tracking

---

### Integration Requirements

#### Data Integration
1. **Cost Module Integration**
   - Real-time cost data
   - Payment status updates
   - Implementation status
   - Acceptance status

2. **Project Module Integration**
   - Project budget information
   - Project timeline data
   - Project status updates
   - Budget approvals

#### Calculation Engine
1. **Real-time Calculation**
   - Automatic recalculation
   - Performance optimization
   - Data validation
   - Error handling

2. **Indicator Formulas**
   - Disbursement calculations
   - Implementation tracking
   - Acceptance monitoring
   - Completion ratios

---

### Security Considerations

#### Data Protection
- Indicator access control
- Project permission validation
- Sensitive data protection
- Audit logging

#### Calculation Security
- Formula validation
- Data integrity checks
- Access control
- Change tracking

---

### Testing Strategy

#### Unit Tests
- Indicator calculation logic
- Formula validation
- Data aggregation
- Performance testing

#### Integration Tests
- Module integration testing
- Real-time updates
- Data synchronization
- Alert generation

#### User Acceptance Tests
- Indicator display accuracy
- Real-time updates
- Multi-project comparison
- Alert functionality

---

### Deployment & Configuration

#### Environment Setup
- Calculation engine setup
- Real-time processing
- Alert system configuration
- Performance monitoring

#### Monitoring & Logging
- Calculation monitoring
- Performance tracking
- Error logging
- Usage analytics

---

### Documentation

#### User Manual
- Indicator interpretation
- Dashboard navigation
- Alert management
- Report generation

#### Technical Documentation
- API documentation
- Calculation formulas
- Integration guides
- Performance optimization 