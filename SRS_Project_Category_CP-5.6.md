# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-5.6
### Cảnh báo khi Tổng Chi phí Vượt quá Ngân sách Dự án

#### Thông tin User Story
- **Story ID:** CP-5.6
- **Priority:** High
- **Story Points:** 6
- **Sprint:** Sprint 5
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-1.3, CP-2.1, CP-5.2, CP-5.5

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án hoặc Quản lý cấp cao,  
**Tôi muốn** hệ thống tự động cảnh báo khi tổng chi phí thực tế đã phát sinh cho một dự án (hoặc tổng với các chi phí dự kiến cho phần còn lại của năm) vượt quá (hoặc sắp vượt quá) Kế hoạch vốn trong năm hoặc Tổng mức đầu tư đã được phê duyệt của dự án  
**Để** tôi có thể kịp thời nắm bắt rủi ro vượt ngân sách và đưa ra các biện pháp điều chỉnh.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Hệ thống so sánh tổng chi phí thực tế/dự kiến của dự án với ngân sách được giao
- [ ] Cảnh báo có thể hiển thị dưới dạng thông báo trên giao diện (ví dụ: biểu tượng cảnh báo màu đỏ), email, hoặc tin nhắn
- [ ] Cho phép người dùng cấu hình ngưỡng cảnh báo (ví dụ: cảnh báo khi chi phí đạt 90% ngân sách)
- [ ] Cảnh báo được kích hoạt tự động khi có thay đổi về chi phí hoặc ngân sách
- [ ] Có thể xem danh sách tất cả cảnh báo vượt ngân sách
- [ ] Có thể phân loại cảnh báo theo mức độ nghiêm trọng (thấp, trung bình, cao, nghiêm trọng)
- [ ] Có thể thiết lập cảnh báo cho từng dự án hoặc toàn bộ hệ thống
- [ ] Có thể xác nhận và giải quyết cảnh báo
- [ ] Có thể xuất báo cáo cảnh báo vượt ngân sách
- [ ] Có thể thiết lập lịch trình gửi cảnh báo định kỳ
- [ ] Có thể tùy chỉnh nội dung và định dạng cảnh báo
- [ ] Có thể theo dõi lịch sử cảnh báo và hành động đã thực hiện

---

### Functional Requirements

#### Core Features
1. **Budget Monitoring**
   - Real-time budget tracking
   - Cost vs budget comparison
   - Projected cost analysis
   - Budget threshold monitoring

2. **Alert System**
   - Automatic alert generation
   - Multi-channel notifications
   - Configurable thresholds
   - Alert severity levels

3. **Alert Management**
   - Alert acknowledgment
   - Alert resolution
   - Alert history tracking
   - Alert reporting

4. **Configuration Management**
   - Threshold configuration
   - Alert frequency settings
   - Notification preferences
   - User permissions

#### Business Rules
- Cảnh báo được kích hoạt tự động khi chi phí vượt ngưỡng cấu hình
- Ngưỡng cảnh báo có thể được cấu hình cho từng dự án
- Cảnh báo phải được xác nhận hoặc giải quyết
- Lịch sử cảnh báo được lưu trữ để theo dõi
- Chỉ người dùng có quyền mới có thể cấu hình cảnh báo

#### Alert Types
1. **Budget Overrun Alerts**
   - Actual cost exceeds budget
   - Projected cost exceeds budget
   - Cumulative cost threshold
   - Monthly/quarterly budget alerts

2. **Threshold Alerts**
   - 80% budget utilization
   - 90% budget utilization
   - 95% budget utilization
   - 100% budget exceeded

3. **Trend Alerts**
   - Rapid cost increase
   - Unusual spending patterns
   - Budget burn rate alerts
   - Forecast overrun alerts

4. **Comparison Alerts**
   - Cost vs plan variance
   - Budget vs actual comparison
   - Year-over-year changes
   - Project performance alerts

#### Alert Severity Levels
1. **Low Severity**
   - 80-90% budget utilization
   - Minor cost overruns
   - Informational alerts

2. **Medium Severity**
   - 90-95% budget utilization
   - Moderate cost overruns
   - Warning alerts

3. **High Severity**
   - 95-100% budget utilization
   - Significant cost overruns
   - Critical alerts

4. **Critical Severity**
   - Over 100% budget utilization
   - Major cost overruns
   - Emergency alerts

#### Notification Channels
1. **In-app Notifications**
   - Dashboard alerts
   - Pop-up notifications
   - Alert badges
   - Status indicators

2. **Email Notifications**
   - Daily summaries
   - Immediate alerts
   - Weekly reports
   - Monthly summaries

3. **SMS Notifications**
   - Critical alerts
   - Emergency notifications
   - High-priority alerts

4. **System Messages**
   - Internal messaging
   - Chat notifications
   - Team communications

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng cấu hình cảnh báo ngân sách
CREATE TABLE budget_alert_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NULL,
    alert_name VARCHAR(200) NOT NULL,
    alert_type ENUM('budget_overrun', 'threshold_alert', 'trend_alert', 'comparison_alert') NOT NULL,
    threshold_percentage DECIMAL(5,2) NOT NULL,
    threshold_amount DECIMAL(15,2) NULL,
    alert_conditions JSON NOT NULL,
    notification_channels JSON NOT NULL,
    recipients JSON,
    is_active BOOLEAN DEFAULT TRUE,
    is_global BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_is_active (is_active),
    INDEX idx_is_global (is_global)
);

-- Bảng cảnh báo ngân sách
CREATE TABLE budget_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    alert_config_id INT NOT NULL,
    alert_type ENUM('budget_overrun', 'threshold_alert', 'trend_alert', 'comparison_alert') NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    alert_message TEXT NOT NULL,
    current_amount DECIMAL(15,2) NOT NULL,
    budget_amount DECIMAL(15,2) NOT NULL,
    threshold_amount DECIMAL(15,2) NOT NULL,
    utilization_percentage DECIMAL(5,2) NOT NULL,
    alert_data JSON,
    is_acknowledged BOOLEAN DEFAULT FALSE,
    is_resolved BOOLEAN DEFAULT FALSE,
    acknowledged_by INT NULL,
    acknowledged_at TIMESTAMP NULL,
    resolved_by INT NULL,
    resolved_at TIMESTAMP NULL,
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (alert_config_id) REFERENCES budget_alert_config(id),
    FOREIGN KEY (acknowledged_by) REFERENCES users(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id),
    INDEX idx_project_id (project_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_severity (severity),
    INDEX idx_is_acknowledged (is_acknowledged),
    INDEX idx_is_resolved (is_resolved),
    INDEX idx_created_at (created_at)
);

-- Bảng lịch sử cảnh báo
CREATE TABLE budget_alert_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alert_id INT NOT NULL,
    action_type ENUM('created', 'acknowledged', 'resolved', 'escalated', 'notified') NOT NULL,
    action_description TEXT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data JSON,
    
    FOREIGN KEY (alert_id) REFERENCES budget_alerts(id),
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_alert_id (alert_id),
    INDEX idx_action_type (action_type),
    INDEX idx_performed_at (performed_at)
);

-- Bảng thông báo cảnh báo
CREATE TABLE budget_alert_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alert_id INT NOT NULL,
    notification_type ENUM('email', 'sms', 'in_app', 'system') NOT NULL,
    recipient_id INT NOT NULL,
    notification_content TEXT NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP NULL,
    delivery_status ENUM('pending', 'sent', 'delivered', 'failed') DEFAULT 'pending',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (alert_id) REFERENCES budget_alerts(id),
    FOREIGN KEY (recipient_id) REFERENCES users(id),
    INDEX idx_alert_id (alert_id),
    INDEX idx_notification_type (notification_type),
    INDEX idx_is_sent (is_sent),
    INDEX idx_delivery_status (delivery_status)
);

-- Bảng báo cáo cảnh báo
CREATE TABLE budget_alert_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(200) NOT NULL,
    report_type ENUM('daily', 'weekly', 'monthly', 'custom') NOT NULL,
    report_period JSON NOT NULL,
    report_data JSON,
    generated_by INT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (generated_by) REFERENCES users(id),
    INDEX idx_report_type (report_type),
    INDEX idx_generated_by (generated_by),
    INDEX idx_generated_at (generated_at)
);

-- Insert default alert configurations
INSERT INTO budget_alert_config (alert_name, alert_type, threshold_percentage, alert_conditions, notification_channels, is_global, created_by) VALUES
('Budget 80% Warning', 'threshold_alert', 80.00, '{"condition": "cost_percentage >= threshold", "frequency": "immediate"}', '["in_app", "email"]', true, 1),
('Budget 90% Warning', 'threshold_alert', 90.00, '{"condition": "cost_percentage >= threshold", "frequency": "immediate"}', '["in_app", "email", "sms"]', true, 1),
('Budget 95% Critical', 'threshold_alert', 95.00, '{"condition": "cost_percentage >= threshold", "frequency": "immediate"}', '["in_app", "email", "sms"]', true, 1),
('Budget Overrun', 'budget_overrun', 100.00, '{"condition": "cost_percentage > 100", "frequency": "immediate"}', '["in_app", "email", "sms"]', true, 1);
```

#### API Endpoints
```typescript
# Get Budget Alerts
GET /api/budget-alerts
{
  "project_id": 123,
  "severity": ["high", "critical"],
  "is_acknowledged": false,
  "is_resolved": false,
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "alerts": [
    {
      "id": 1,
      "project_id": 123,
      "project_name": "Dự án A",
      "alert_type": "budget_overrun",
      "severity": "critical",
      "alert_message": "Chi phí đã vượt quá ngân sách được phê duyệt",
      "current_amount": 1600000000,
      "budget_amount": 1500000000,
      "threshold_amount": 1500000000,
      "utilization_percentage": 106.67,
      "is_acknowledged": false,
      "is_resolved": false,
      "created_at": "2024-01-25T10:30:00Z"
    }
  ],
  "summary": {
    "total_alerts": 5,
    "unacknowledged": 3,
    "unresolved": 4,
    "critical_alerts": 2
  }
}

# Acknowledge Budget Alert
POST /api/budget-alerts/{alert_id}/acknowledge
{
  "acknowledgment_notes": "Đã xem xét và đang xử lý",
  "next_action": "review_budget"
}
Response: {
  "success": true,
  "alert_id": 1,
  "acknowledged_by": "Nguyễn Văn A",
  "acknowledged_at": "2024-01-25T11:00:00Z"
}

# Resolve Budget Alert
POST /api/budget-alerts/{alert_id}/resolve
{
  "resolution_notes": "Đã điều chỉnh ngân sách và kiểm soát chi phí",
  "resolution_action": "budget_adjustment"
}
Response: {
  "success": true,
  "alert_id": 1,
  "resolved_by": "Nguyễn Văn A",
  "resolved_at": "2024-01-25T11:30:00Z"
}

# Create Alert Configuration
POST /api/budget-alerts/config
{
  "alert_name": "Cảnh báo ngân sách dự án A",
  "alert_type": "threshold_alert",
  "project_id": 123,
  "threshold_percentage": 85.00,
  "threshold_amount": 1275000000,
  "alert_conditions": {
    "condition": "cost_percentage >= threshold",
    "frequency": "immediate",
    "check_interval": "daily"
  },
  "notification_channels": ["in_app", "email"],
  "recipients": ["user1@example.com", "user2@example.com"],
  "is_active": true
}
Response: {
  "success": true,
  "config_id": 123,
  "message": "Cấu hình cảnh báo đã được tạo thành công"
}

# Get Alert Configurations
GET /api/budget-alerts/config
{
  "project_id": 123,
  "alert_type": "threshold_alert",
  "is_active": true
}
Response: {
  "configurations": [
    {
      "id": 1,
      "alert_name": "Budget 80% Warning",
      "alert_type": "threshold_alert",
      "threshold_percentage": 80.00,
      "notification_channels": ["in_app", "email"],
      "is_active": true,
      "is_global": true
    },
    {
      "id": 2,
      "alert_name": "Cảnh báo ngân sách dự án A",
      "alert_type": "threshold_alert",
      "project_id": 123,
      "threshold_percentage": 85.00,
      "notification_channels": ["in_app", "email"],
      "is_active": true,
      "is_global": false
    }
  ]
}

# Check Budget Status
GET /api/budget-alerts/check-status
{
  "project_id": 123,
  "include_projected": true
}
Response: {
  "project_id": 123,
  "project_name": "Dự án A",
  "budget_info": {
    "approved_budget": 1500000000,
    "current_cost": 1200000000,
    "projected_cost": 1600000000,
    "remaining_budget": 300000000,
    "utilization_percentage": 80.00
  },
  "alerts": [
    {
      "alert_type": "threshold_alert",
      "severity": "medium",
      "message": "Chi phí đã đạt 80% ngân sách",
      "threshold": 80.00,
      "current": 80.00
    }
  ],
  "recommendations": [
    "Kiểm soát chi phí chặt chẽ hơn",
    "Xem xét điều chỉnh ngân sách",
    "Tối ưu hóa các khoản chi phí"
  ]
}

# Generate Alert Report
POST /api/budget-alerts/report
{
  "report_name": "Báo cáo cảnh báo ngân sách tháng 1/2024",
  "report_type": "monthly",
  "project_ids": [123, 124, 125],
  "include_resolved": true,
  "include_history": true
}
Response: {
  "success": true,
  "report_id": "REP-2024-001",
  "report_data": {
    "summary": {
      "total_alerts": 15,
      "acknowledged": 10,
      "resolved": 8,
      "critical_alerts": 3
    },
    "by_project": [
      {
        "project_id": 123,
        "project_name": "Dự án A",
        "alert_count": 5,
        "critical_count": 2
      }
    ],
    "by_severity": {
      "low": 3,
      "medium": 7,
      "high": 3,
      "critical": 2
    },
    "trends": [
      {
        "month": "2024-01",
        "alert_count": 15,
        "resolved_count": 8
      }
    ]
  }
}

# Send Test Alert
POST /api/budget-alerts/test
{
  "project_id": 123,
  "alert_type": "threshold_alert",
  "test_message": "Đây là cảnh báo thử nghiệm",
  "recipients": ["user1@example.com"]
}
Response: {
  "success": true,
  "test_sent": true,
  "delivery_status": "sent"
}
```

#### Frontend Components
```typescript
// Budget Alert Dashboard Component
interface BudgetAlertDashboardComponent {
  alerts: BudgetAlert[]
  alertSummary: AlertSummary
  
  onAlertSelect: (alert: BudgetAlert) => void
  onAlertAcknowledge: (alertId: number) => void
  onAlertResolve: (alertId: number) => void
  onFilterChange: (filters: AlertFilters) => void
}

// Budget Alert Configuration Component
interface BudgetAlertConfigComponent {
  configurations: AlertConfiguration[]
  selectedConfig: AlertConfiguration | null
  
  onConfigCreate: (config: AlertConfiguration) => void
  onConfigUpdate: (configId: number, updates: Partial<AlertConfiguration>) => void
  onConfigDelete: (configId: number) => void
  onConfigTest: (configId: number) => void
}

// Budget Alert Notification Component
interface BudgetAlertNotificationComponent {
  notifications: AlertNotification[]
  
  onNotificationRead: (notificationId: number) => void
  onNotificationAction: (notification: AlertNotification) => void
  onNotificationSettings: () => void
}

// Budget Status Component
interface BudgetStatusComponent {
  budgetStatus: BudgetStatus
  projectId: number
  
  onBudgetView: () => void
  onAlertView: () => void
  onSettingsView: () => void
}

// Alert History Component
interface AlertHistoryComponent {
  alertHistory: AlertHistory[]
  
  onHistoryFilter: (filters: HistoryFilters) => void
  onHistoryExport: () => void
  onHistoryDetail: (history: AlertHistory) => void
}

// Alert Report Component
interface AlertReportComponent {
  reportData: AlertReportData
  
  onReportGenerate: (config: ReportConfig) => void
  onReportExport: (format: string) => void
  onReportSchedule: (schedule: ReportSchedule) => void
}

// Alert Settings Component
interface AlertSettingsComponent {
  settings: AlertSettings
  
  onThresholdChange: (thresholds: AlertThresholds) => void
  onNotificationChange: (notifications: NotificationSettings) => void
  onChannelChange: (channels: NotificationChannels) => void
  onSettingsSave: () => void
}

// Budget Overrun Chart Component
interface BudgetOverrunChartComponent {
  chartData: OverrunChartData
  
  onChartClick: (dataPoint: any) => void
  onChartExport: () => void
  onTimeRangeChange: (range: TimeRange) => void
}

// Alert Escalation Component
interface AlertEscalationComponent {
  alert: BudgetAlert
  escalationLevel: number
  
  onEscalate: (level: number, reason: string) => void
  onEscalationHistory: () => void
  onEscalationSettings: () => void
}
```

---

### UI/UX Design

#### Alert Dashboard Interface
- **Dashboard Layout:**
  - Alert summary cards
  - Alert list with filters
  - Quick action buttons
  - Status indicators

#### Alert Configuration Interface
- **Configuration Layout:**
  - Threshold settings
  - Notification preferences
  - Recipient management
  - Test functionality

#### Alert Notification Interface
- **Notification Design:**
  - Alert badges
  - Pop-up notifications
  - In-app messages
  - Email templates

#### Budget Status Interface
- **Status Layout:**
  - Budget utilization chart
  - Alert indicators
  - Trend analysis
  - Action buttons

---

### Integration Requirements

#### Budget Monitoring Integration
1. **Real-time Monitoring**
   - Cost tracking
   - Budget comparison
   - Threshold checking
   - Alert generation

2. **Data Synchronization**
   - Cost updates
   - Budget changes
   - Project modifications
   - User permissions

#### Notification System Integration
1. **Multi-channel Notifications**
   - Email service
   - SMS service
   - In-app messaging
   - System notifications

2. **Alert Management**
   - Alert routing
   - Escalation rules
   - Response tracking
   - History logging

---

### Security Considerations

#### Data Protection
- Alert access control
- Budget data protection
- Notification security
- Audit logging

#### Alert Security
- Permission validation
- Data filtering
- Escalation control
- Response tracking

---

### Testing Strategy

#### Unit Tests
- Alert generation logic
- Threshold calculation
- Notification delivery
- Escalation rules

#### Integration Tests
- Budget monitoring
- Alert system integration
- Notification delivery
- Data synchronization

#### User Acceptance Tests
- Alert workflow
- Notification delivery
- Configuration management
- Response tracking

---

### Deployment & Configuration

#### Environment Setup
- Alert system setup
- Notification service configuration
- Budget monitoring setup
- Escalation configuration

#### Monitoring & Logging
- Alert monitoring
- Notification tracking
- Performance monitoring
- Error logging

---

### Documentation

#### User Manual
- Alert interpretation
- Configuration procedures
- Response procedures
- Escalation management

#### Technical Documentation
- API documentation
- Alert system architecture
- Integration guides
- Performance optimization 