# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-4.1
### Hiển thị Tổng giá trị Hợp đồng, Lũy kế Chi phí Thực hiện và Giá trị Chưa Hoàn thành

#### Thông tin User Story
- **Story ID:** HD-4.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 4
- **Status:** To Do
- **Phụ thuộc:** HD-1.1, Chi phí Module

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách hợp đồng hoặc Quản lý,  
**Tôi muốn** hệ thống tự động hiển thị:
- Tổng giá trị hợp đồng: Giá trị đã được ghi nhận khi tạo hợp đồng
- Giá trị thực hiện lũy kế: Tổng số tiền của tất cả các khoản mục chi phí đã được liên kết với hợp đồng này trong Module Chi phí và có trạng thái là "Giá trị đã thực hiện"
- Giá trị nghiệm thu lũy kế: Tổng số tiền của tất cả các khoản mục chi phí đã được liên kết với hợp đồng này trong Module Chi phí và có trạng thái là "Giá trị đã nghiệm thu"
- Giá trị giải ngân lũy kế: Tổng số tiền của tất cả các khoản mục chi phí đã được liên kết với hợp đồng này trong Module Chi phí và có trạng thái là "Đã thanh toán đầy đủ"
- Giá trị chưa hoàn thành giải ngân: Giá trị được tính bằng Tổng giá trị hợp đồng trừ đi Lũy kế thực hiện hợp đồng (Giá trị giải ngân)  
**Để** tôi có thể nhanh chóng so sánh ngân sách hợp đồng với chi phí thực tế đã phát sinh và nắm bắt phần giá trị còn lại cần được thực hiện/thanh toán, giúp theo dõi tình hình tài chính của từng hợp đồng một cách hiệu quả.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Các chỉ số này được hiển thị rõ ràng trên trang chi tiết của mỗi hợp đồng
- [ ] Giá trị thực hiện lũy kế, giá trị nghiệm thu lũy kế, giá trị giải ngân lũy kế và Giá trị chưa hoàn thành giải ngân được tính toán tự động và cập nhật khi có thêm chi phí được liên kết hoặc chi phí liên kết bị chỉnh sửa/xóa/thay đổi trạng thái thanh toán trong Module Chi phí
- [ ] Có thể có thêm tỷ lệ hoàn thành (Lũy kế thực hiện giải ngân / Tổng giá trị hợp đồng) nếu cần thiết
- [ ] Hiển thị biểu đồ trực quan cho các chỉ số tài chính
- [ ] Có thể xem chi tiết từng khoản mục chi phí liên kết
- [ ] Có thể xuất báo cáo tài chính hợp đồng
- [ ] Hiển thị cảnh báo khi vượt ngân sách hoặc sắp hết ngân sách
- [ ] Có thể so sánh với kế hoạch ngân sách ban đầu
- [ ] Hiển thị lịch sử thay đổi các chỉ số tài chính
- [ ] Có thể thiết lập ngưỡng cảnh báo cho từng hợp đồng

#### 2.4 Activity Diagram
![HD-4.1 Activity Diagram](diagrams/HD-4.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý hiển thị thông tin tài chính hợp đồng*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Dashboard Tài chính**
   - Chỉ số tài chính thời gian thực
   - Biểu đồ và đồ thị trực quan
   - Theo dõi tiến độ
   - So sánh ngân sách

2. **Tính toán Tự động**
   - Tính toán chi phí lũy kế
   - Theo dõi trạng thái thanh toán
   - Tính toán giá trị còn lại
   - Tính toán tỷ lệ hoàn thành

3. **Tích hợp Chi phí**
   - Liên kết với Module Chi phí
   - Đồng bộ dữ liệu thời gian thực
   - Lọc theo trạng thái
   - Chi tiết khoản mục chi phí

4. **Hệ thống Cảnh báo**
   - Cảnh báo ngưỡng ngân sách
   - Thông báo đến hạn thanh toán
   - Cảnh báo vượt ngân sách
   - Cột mốc hoàn thành

#### Quy tắc Kinh doanh
- Tất cả tính toán phải thời gian thực và chính xác
- Giá trị chưa hoàn thành = Tổng giá trị hợp đồng - Giá trị giải ngân lũy kế
- Tỷ lệ hoàn thành = (Giá trị giải ngân lũy kế / Tổng giá trị hợp đồng) × 100%
- Cảnh báo khi vượt 90% ngân sách
- Cảnh báo khi vượt 100% ngân sách
- Lưu lịch sử thay đổi các chỉ số

#### Chỉ số Tài chính
1. **Chỉ số Giá trị Hợp đồng**
   - Tổng giá trị hợp đồng
   - Ngân sách ban đầu
   - Ngân sách điều chỉnh
   - Thay đổi hợp đồng

2. **Chỉ số Chi phí Lũy kế**
   - Giá trị thực hiện lũy kế
   - Giá trị nghiệm thu lũy kế
   - Giá trị giải ngân lũy kế
   - Giá trị thanh toán lũy kế

3. **Chỉ số Giá trị Còn lại**
   - Giá trị thực hiện còn lại
   - Giá trị nghiệm thu còn lại
   - Giá trị giải ngân còn lại
   - Giá trị thanh toán còn lại

4. **Chỉ số Tiến độ**
   - Tỷ lệ hoàn thành thực hiện
   - Tỷ lệ hoàn thành nghiệm thu
   - Tỷ lệ hoàn thành giải ngân
   - Tỷ lệ hoàn thành thanh toán

---

#### 5.5 Sequence Diagram
![HD-4.1 Sequence Diagram](diagrams/HD-4.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi hiển thị thông tin tài chính hợp đồng*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng chỉ số tài chính hợp đồng
CREATE TABLE contract_financial_indicators (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    indicator_date DATE NOT NULL,
    
    -- Contract Values
    total_contract_value DECIMAL(15,2) NOT NULL,
    original_budget DECIMAL(15,2) NOT NULL,
    revised_budget DECIMAL(15,2),
    contract_variations DECIMAL(15,2) DEFAULT 0,
    
    -- Cumulative Values
    cumulative_implementation_value DECIMAL(15,2) DEFAULT 0,
    cumulative_acceptance_value DECIMAL(15,2) DEFAULT 0,
    cumulative_disbursement_value DECIMAL(15,2) DEFAULT 0,
    cumulative_payment_value DECIMAL(15,2) DEFAULT 0,
    
    -- Remaining Values
    remaining_implementation_value DECIMAL(15,2) DEFAULT 0,
    remaining_acceptance_value DECIMAL(15,2) DEFAULT 0,
    remaining_disbursement_value DECIMAL(15,2) DEFAULT 0,
    remaining_payment_value DECIMAL(15,2) DEFAULT 0,
    
    -- Progress Ratios
    implementation_progress_ratio DECIMAL(5,2) DEFAULT 0,
    acceptance_progress_ratio DECIMAL(5,2) DEFAULT 0,
    disbursement_progress_ratio DECIMAL(5,2) DEFAULT 0,
    payment_progress_ratio DECIMAL(5,2) DEFAULT 0,
    
    -- Alert Status
    budget_alert_status ENUM('normal', 'warning', 'critical') DEFAULT 'normal',
    payment_alert_status ENUM('normal', 'warning', 'critical') DEFAULT 'normal',
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    UNIQUE KEY unique_contract_date (contract_id, indicator_date),
    INDEX idx_contract_id (contract_id),
    INDEX idx_indicator_date (indicator_date)
);

-- Bảng liên kết chi phí với hợp đồng
CREATE TABLE contract_cost_links (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    cost_item_id INT NOT NULL,
    cost_amount DECIMAL(15,2) NOT NULL,
    cost_status ENUM('pending', 'implemented', 'accepted', 'disbursed', 'paid', 'cancelled') NOT NULL,
    cost_category VARCHAR(100),
    cost_description TEXT,
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id),
    UNIQUE KEY unique_contract_cost (contract_id, cost_item_id),
    INDEX idx_contract_status (contract_id, cost_status)
);

-- Bảng lịch sử chỉ số tài chính
CREATE TABLE contract_financial_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    indicator_date DATE NOT NULL,
    change_type ENUM('cost_added', 'cost_updated', 'cost_removed', 'status_changed', 'budget_updated') NOT NULL,
    old_value DECIMAL(15,2),
    new_value DECIMAL(15,2),
    change_description TEXT,
    cost_item_id INT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id),
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_contract_date (contract_id, indicator_date)
);

-- Bảng cấu hình cảnh báo tài chính
CREATE TABLE contract_financial_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    alert_type ENUM('budget_warning', 'budget_critical', 'payment_due', 'completion_milestone') NOT NULL,
    threshold_value DECIMAL(15,2),
    threshold_percentage DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    notification_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    INDEX idx_contract_alert (contract_id, alert_type)
);

-- Bảng báo cáo tài chính hợp đồng
CREATE TABLE contract_financial_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    report_date DATE NOT NULL,
    report_type ENUM('daily', 'weekly', 'monthly', 'quarterly', 'annual') NOT NULL,
    report_data JSON NOT NULL,
    generated_by INT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (generated_by) REFERENCES users(id),
    UNIQUE KEY unique_contract_report (contract_id, report_date, report_type)
);

-- Insert default financial alerts
INSERT INTO contract_financial_alerts (contract_id, alert_type, threshold_percentage, notification_enabled) VALUES
(1, 'budget_warning', 80.00, TRUE),
(1, 'budget_critical', 100.00, TRUE),
(1, 'payment_due', NULL, TRUE),
(1, 'completion_milestone', 50.00, TRUE);
```

#### API Endpoints
```
# Financial Indicators
GET /api/contracts/{id}/financial-indicators
GET /api/contracts/{id}/financial-indicators/{date}
POST /api/contracts/{id}/financial-indicators/calculate

# Cost Links
GET /api/contracts/{id}/cost-links
POST /api/contracts/{id}/cost-links
{
  "cost_item_id": 123,
  "cost_amount": 1000000,
  "cost_status": "implemented",
  "cost_category": "materials",
  "cost_description": "Construction materials"
}

PUT /api/contracts/{id}/cost-links/{link_id}
DELETE /api/contracts/{id}/cost-links/{link_id}

# Financial History
GET /api/contracts/{id}/financial-history
GET /api/contracts/{id}/financial-history/{date}

# Financial Alerts
GET /api/contracts/{id}/financial-alerts
POST /api/contracts/{id}/financial-alerts
{
  "alert_type": "budget_warning",
  "threshold_percentage": 80.00,
  "notification_enabled": true
}

# Financial Reports
GET /api/contracts/{id}/financial-reports
POST /api/contracts/{id}/financial-reports/generate
{
  "report_type": "monthly",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}

# Dashboard Data
GET /api/contracts/{id}/financial-dashboard
Response: {
  "total_contract_value": 1000000000,
  "cumulative_implementation": 750000000,
  "cumulative_acceptance": 600000000,
  "cumulative_disbursement": 500000000,
  "remaining_disbursement": 500000000,
  "implementation_progress": 75.00,
  "acceptance_progress": 60.00,
  "disbursement_progress": 50.00,
  "alerts": [
    {
      "type": "budget_warning",
      "message": "Contract has reached 80% of budget",
      "severity": "warning"
    }
  ]
}

# Bulk Financial Data
GET /api/contracts/financial-summary
{
  "contract_ids": [1, 2, 3],
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
```

#### Frontend Components
```typescript
// Financial Dashboard Component
interface FinancialDashboardComponent {
  contractId: number
  financialData: ContractFinancialData
  isLoading: boolean
  
  onRefresh: () => Promise<void>
  onExportReport: () => void
  onViewDetails: (indicatorType: string) => void
}

// Financial Indicators Component
interface FinancialIndicatorsComponent {
  indicators: FinancialIndicator[]
  isLoading: boolean
  
  onIndicatorClick: (indicator: FinancialIndicator) => void
  onDateRangeChange: (startDate: Date, endDate: Date) => void
  onExportData: () => void
}

// Cost Links Component
interface CostLinksComponent {
  contractId: number
  costLinks: ContractCostLink[]
  isLoading: boolean
  
  onAddCostLink: (costLink: Partial<ContractCostLink>) => Promise<void>
  onUpdateCostLink: (linkId: number, updates: Partial<ContractCostLink>) => Promise<void>
  onRemoveCostLink: (linkId: number) => Promise<void>
  onViewCostDetails: (costItemId: number) => void
}

// Financial Charts Component
interface FinancialChartsComponent {
  financialData: ContractFinancialData
  chartType: 'pie' | 'bar' | 'line' | 'progress'
  
  onChartTypeChange: (type: string) => void
  onDataPointClick: (dataPoint: any) => void
  onExportChart: () => void
}

// Financial Alerts Component
interface FinancialAlertsComponent {
  contractId: number
  alerts: FinancialAlert[]
  
  onAcknowledgeAlert: (alertId: number) => Promise<void>
  onConfigureAlert: (alertType: string) => void
  onViewAlertHistory: () => void
}

// Financial History Component
interface FinancialHistoryComponent {
  contractId: number
  history: FinancialHistoryEntry[]
  isLoading: boolean
  
  onViewEntry: (entryId: number) => void
  onFilterHistory: (filters: HistoryFilters) => void
  onExportHistory: () => void
}

// Progress Indicators Component
interface ProgressIndicatorsComponent {
  progressData: ProgressData
  showPercentages: boolean
  
  onTogglePercentages: () => void
  onViewProgressDetails: (progressType: string) => void
}

// Budget Comparison Component
interface BudgetComparisonComponent {
  contractId: number
  comparisonData: BudgetComparisonData
  
  onViewVarianceDetails: (varianceType: string) => void
  onExportComparison: () => void
}

// Financial Reports Component
interface FinancialReportsComponent {
  contractId: number
  reports: FinancialReport[]
  
  onGenerateReport: (reportType: string, dateRange: DateRange) => Promise<void>
  onDownloadReport: (reportId: number) => void
  onScheduleReport: (schedule: ReportSchedule) => Promise<void>
}
```

---

### UI/UX Design

#### Financial Dashboard
- **Dashboard Layout:**
  - Key indicators cards
  - Progress bars
  - Charts and graphs
  - Alert notifications

#### Financial Indicators Display
- **Indicator Cards:**
  - Large numbers with currency formatting
  - Color-coded status indicators
  - Progress bars for ratios
  - Trend arrows

#### Cost Links Management
- **Cost Links Table:**
  - Cost item details
  - Status indicators
  - Amount formatting
  - Action buttons

#### Charts and Visualizations
- **Chart Types:**
  - Pie charts for budget allocation
  - Bar charts for progress comparison
  - Line charts for trends
  - Progress circles for completion

---

### Integration Requirements

#### Cost Module Integration
1. **Real-time Data Sync**
   - Cost item status changes
   - Amount updates
   - Link/unlink operations
   - Status synchronization

2. **Calculation Engine**
   - Automatic recalculation
   - Historical data tracking
   - Performance optimization
   - Data consistency

#### Notification System
1. **Financial Alerts**
   - Budget threshold notifications
   - Payment due alerts
   - Completion milestone notifications
   - Over-budget warnings

2. **Report Generation**
   - Scheduled reports
   - Export functionality
   - Email notifications
   - Dashboard updates

---

### Security Considerations

#### Data Protection
- Encrypted financial data
- Access control for sensitive information
- Audit logging for all calculations
- Secure API endpoints

#### Calculation Integrity
- Validation of all calculations
- Double-entry verification
- Historical data preservation
- Error handling and recovery

#### Access Control
- Role-based financial access
- Contract-level permissions
- Sensitive data masking
- Export restrictions

---

### Testing Strategy

#### Unit Tests
- Financial calculation accuracy
- Data integration logic
- Alert system functionality
- Report generation

#### Integration Tests
- Cost module integration
- Real-time data synchronization
- Calculation performance
- Alert delivery system

#### User Acceptance Tests
- Dashboard usability
- Financial data accuracy
- Alert system effectiveness
- Report functionality

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Calculation engine setup
- Alert system configuration
- Report generation setup

#### Monitoring & Logging
- Financial calculation monitoring
- Performance tracking
- Alert system monitoring
- Data integrity checks

---

### Documentation

#### User Manual
- Financial dashboard guide
- Cost linking procedures
- Alert configuration
- Report generation instructions

#### Technical Documentation
- API documentation
- Calculation algorithms
- Integration architecture
- Performance optimization 