# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-1.3
### Cập nhật Trạng thái Thanh toán

#### Thông tin User Story
- **Story ID:** CP-1.3
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** có thể cập nhật trạng thái thanh toán và các mốc thanh toán của mỗi khoản mục chi phí  
**Để** tôi có thể theo dõi tiến độ thanh toán và xác định các khoản chi phí cần xử lý.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Hệ thống có trường "Đã thực hiện" dạng chọn (Có/Không)
- [ ] Nếu chọn "Có" cho "Đã thực hiện", cho phép nhập Ngày thực hiện
- [ ] Hệ thống có trường "Đã nghiệm thu" dạng chọn (Có/Không)
- [ ] Nếu chọn "Có" cho "Đã nghiệm thu", cho phép nhập Ngày nghiệm thu
- [ ] Hệ thống có trường "Ngày hoàn thành thanh toán thực tế" (người dùng cập nhật)
- [ ] Hệ thống tự động xác định trường "Trạng thái thanh toán" với các quy tắc:
  - Nếu chưa đến ngày trong "Thời hạn dự kiến thanh toán", trạng thái = "Chưa đến hạn"
  - Nếu đã có "Ngày hoàn thành thanh toán thực tế", trạng thái = "Đã thanh toán"
  - Nếu đã qua "Thời hạn dự kiến thanh toán" hoặc "Ngày kết thúc kỳ" mà chưa có ngày hoàn thành, trạng thái = "Quá hạn"
- [ ] Giao diện hiển thị rõ ràng trạng thái thanh toán với màu sắc phân biệt
- [ ] Có thể cập nhật thông tin thanh toán từ danh sách chi phí
- [ ] Hệ thống ghi log lịch sử thay đổi trạng thái thanh toán
- [ ] Có thể xuất báo cáo trạng thái thanh toán theo thời gian

---

### Functional Requirements

#### Core Features
1. **Payment Status Management**
   - Implementation status tracking
   - Acceptance status tracking
   - Actual payment completion date
   - Automatic status determination

2. **Status Update Interface**
   - Inline editing capabilities
   - Bulk status updates
   - Status history tracking
   - Visual status indicators

3. **Business Rules Implementation**
   - Automatic status calculation
   - Date-based status logic
   - Payment milestone tracking
   - Overdue detection

4. **Reporting & Analytics**
   - Payment status reports
   - Overdue payment alerts
   - Payment progress tracking
   - Status trend analysis

#### Business Rules
- Trạng thái thanh toán được tính tự động dựa trên ngày thực tế và ngày dự kiến
- "Chưa đến hạn" khi chưa đến thời hạn dự kiến thanh toán
- "Đã thanh toán" khi có ngày hoàn thành thanh toán thực tế
- "Quá hạn" khi đã qua thời hạn dự kiến hoặc ngày kết thúc kỳ mà chưa thanh toán
- Ngày thực hiện và ngày nghiệm thu phải hợp lệ (không trong tương lai)
- Ngày hoàn thành thanh toán thực tế không được trước ngày thực hiện

#### Payment Status Fields
1. **Implementation Status**
   - Đã thực hiện (Yes/No)
   - Ngày thực hiện (Date picker)
   - Ghi chú thực hiện (Text)

2. **Acceptance Status**
   - Đã nghiệm thu (Yes/No)
   - Ngày nghiệm thu (Date picker)
   - Ghi chú nghiệm thu (Text)

3. **Payment Completion**
   - Ngày hoàn thành thanh toán thực tế (Date picker)
   - Số tiền đã thanh toán (Amount)
   - Phương thức thanh toán (Payment method)
   - Số chứng từ thanh toán (Payment reference)

4. **Automatic Status**
   - Trạng thái thanh toán (Auto-calculated)
   - Ngày cập nhật trạng thái (Auto-timestamp)
   - Lý do trạng thái (Auto-generated)

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng cập nhật khoản mục chi phí với trạng thái thanh toán
ALTER TABLE cost_items ADD COLUMN (
    -- Implementation status
    is_implemented BOOLEAN DEFAULT FALSE,
    implementation_date DATE NULL,
    implementation_notes TEXT,
    
    -- Acceptance status
    is_accepted BOOLEAN DEFAULT FALSE,
    acceptance_date DATE NULL,
    acceptance_notes TEXT,
    
    -- Payment completion
    actual_payment_date DATE NULL,
    actual_payment_amount DECIMAL(15,2) NULL,
    payment_method VARCHAR(100) NULL,
    payment_reference VARCHAR(200) NULL,
    
    -- Automatic status
    payment_status ENUM('not_due', 'paid', 'overdue') DEFAULT 'not_due',
    payment_status_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_status_reason VARCHAR(500) NULL
);

-- Bảng lịch sử thay đổi trạng thái thanh toán
CREATE TABLE payment_status_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    old_status ENUM('not_due', 'paid', 'overdue') NULL,
    new_status ENUM('not_due', 'paid', 'overdue') NOT NULL,
    changed_by INT NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason VARCHAR(500) NULL,
    notes TEXT,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_status_change (old_status, new_status),
    INDEX idx_changed_at (changed_at)
);

-- Bảng cấu hình quy tắc trạng thái thanh toán
CREATE TABLE payment_status_rules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rule_name VARCHAR(100) NOT NULL,
    rule_description TEXT,
    condition_type ENUM('before_due_date', 'after_due_date', 'payment_completed', 'implementation_completed') NOT NULL,
    condition_value VARCHAR(200) NULL,
    status_result ENUM('not_due', 'paid', 'overdue') NOT NULL,
    priority INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_priority (priority),
    INDEX idx_is_active (is_active)
);

-- Insert default payment status rules
INSERT INTO payment_status_rules (rule_name, rule_description, condition_type, condition_value, status_result, priority) VALUES
('Payment Completed', 'Mark as paid when actual payment date is set', 'payment_completed', NULL, 'paid', 1),
('Before Due Date', 'Mark as not due when before planned payment date', 'before_due_date', NULL, 'not_due', 2),
('After Due Date', 'Mark as overdue when past planned payment date', 'after_due_date', NULL, 'overdue', 3);

-- Bảng báo cáo trạng thái thanh toán
CREATE TABLE payment_status_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(200) NOT NULL,
    report_type ENUM('daily', 'weekly', 'monthly', 'custom') NOT NULL,
    report_date DATE NOT NULL,
    total_cost_items INT NOT NULL,
    not_due_count INT DEFAULT 0,
    paid_count INT DEFAULT 0,
    overdue_count INT DEFAULT 0,
    total_amount DECIMAL(15,2) NOT NULL,
    paid_amount DECIMAL(15,2) DEFAULT 0,
    overdue_amount DECIMAL(15,2) DEFAULT 0,
    generated_by INT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (generated_by) REFERENCES users(id),
    INDEX idx_report_date (report_date),
    INDEX idx_report_type (report_type)
);
```

#### API Endpoints
```typescript
# Payment Status Management
GET /api/cost-items/{id}/payment-status
Response: {
  "cost_item_id": 123,
  "is_implemented": true,
  "implementation_date": "2024-01-15",
  "implementation_notes": "Đã hoàn thành triển khai",
  "is_accepted": true,
  "acceptance_date": "2024-01-20",
  "acceptance_notes": "Đã nghiệm thu thành công",
  "actual_payment_date": "2024-01-25",
  "actual_payment_amount": 50000000,
  "payment_method": "Chuyển khoản",
  "payment_reference": "TT-2024-001",
  "payment_status": "paid",
  "payment_status_updated_at": "2024-01-25T10:30:00Z",
  "payment_status_reason": "Đã thanh toán đầy đủ"
}

PUT /api/cost-items/{id}/payment-status
{
  "is_implemented": true,
  "implementation_date": "2024-01-15",
  "implementation_notes": "Đã hoàn thành triển khai",
  "is_accepted": true,
  "acceptance_date": "2024-01-20",
  "acceptance_notes": "Đã nghiệm thu thành công",
  "actual_payment_date": "2024-01-25",
  "actual_payment_amount": 50000000,
  "payment_method": "Chuyển khoản",
  "payment_reference": "TT-2024-001"
}

# Bulk Payment Status Update
PUT /api/cost-items/bulk-payment-status
{
  "cost_item_ids": [123, 124, 125],
  "updates": {
    "is_implemented": true,
    "implementation_date": "2024-01-15",
    "payment_method": "Chuyển khoản"
  }
}

# Payment Status History
GET /api/cost-items/{id}/payment-status-history
Response: [
  {
    "id": 1,
    "old_status": "not_due",
    "new_status": "paid",
    "changed_by": 456,
    "changed_at": "2024-01-25T10:30:00Z",
    "reason": "Thanh toán hoàn tất",
    "notes": "Đã thanh toán đầy đủ theo hóa đơn"
  }
]

# Payment Status Rules
GET /api/payment-status-rules
PUT /api/payment-status-rules/{id}
{
  "rule_name": "Custom Payment Rule",
  "condition_type": "payment_completed",
  "status_result": "paid",
  "priority": 1
}

# Payment Status Reports
GET /api/payment-status-reports
{
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "status_filter": "overdue"
}

POST /api/payment-status-reports/generate
{
  "report_type": "monthly",
  "report_date": "2024-01-31",
  "include_details": true
}

# Payment Status Statistics
GET /api/payment-status/statistics
Response: {
  "total_cost_items": 150,
  "not_due_count": 50,
  "paid_count": 80,
  "overdue_count": 20,
  "total_amount": 5000000000,
  "paid_amount": 3000000000,
  "overdue_amount": 500000000,
  "payment_completion_rate": 60.0,
  "overdue_rate": 13.3
}

# Payment Status Alerts
GET /api/payment-status/alerts
Response: {
  "overdue_alerts": [
    {
      "cost_item_id": 123,
      "cost_name": "Chi phí thiết bị",
      "days_overdue": 15,
      "overdue_amount": 50000000,
      "planned_payment_date": "2024-01-10"
    }
  ],
  "upcoming_payments": [
    {
      "cost_item_id": 124,
      "cost_name": "Chi phí dịch vụ",
      "days_until_due": 5,
      "planned_amount": 30000000,
      "planned_payment_date": "2024-02-05"
    }
  ]
}
```

#### Frontend Components
```typescript
// Payment Status Component
interface PaymentStatusComponent {
  costItemId: number
  paymentStatus: PaymentStatus
  isEditing: boolean
  
  onStatusChange: (status: Partial<PaymentStatus>) => Promise<void>
  onEditMode: () => void
  onSaveChanges: () => Promise<void>
  onCancelEdit: () => void
}

// Implementation Status Component
interface ImplementationStatusComponent {
  isImplemented: boolean
  implementationDate: Date | null
  implementationNotes: string
  
  onImplementationChange: (implemented: boolean) => void
  onDateChange: (date: Date | null) => void
  onNotesChange: (notes: string) => void
}

// Acceptance Status Component
interface AcceptanceStatusComponent {
  isAccepted: boolean
  acceptanceDate: Date | null
  acceptanceNotes: string
  
  onAcceptanceChange: (accepted: boolean) => void
  onDateChange: (date: Date | null) => void
  onNotesChange: (notes: string) => void
}

// Payment Completion Component
interface PaymentCompletionComponent {
  actualPaymentDate: Date | null
  actualPaymentAmount: number
  paymentMethod: string
  paymentReference: string
  
  onDateChange: (date: Date | null) => void
  onAmountChange: (amount: number) => void
  onMethodChange: (method: string) => void
  onReferenceChange: (reference: string) => void
}

// Payment Status Display Component
interface PaymentStatusDisplayComponent {
  paymentStatus: 'not_due' | 'paid' | 'overdue'
  statusReason: string
  lastUpdated: Date
  
  getStatusColor: () => string
  getStatusIcon: () => string
  getStatusText: () => string
}

// Payment Status History Component
interface PaymentStatusHistoryComponent {
  costItemId: number
  history: PaymentStatusHistory[]
  
  onViewHistory: () => void
  onExportHistory: () => void
}

// Bulk Payment Status Update Component
interface BulkPaymentStatusUpdateComponent {
  selectedCostItems: number[]
  updateData: Partial<PaymentStatus>
  
  onSelectItems: (itemIds: number[]) => void
  onUpdateData: (data: Partial<PaymentStatus>) => void
  onApplyBulkUpdate: () => Promise<void>
  onClearSelection: () => void
}

// Payment Status Report Component
interface PaymentStatusReportComponent {
  reportFilters: PaymentStatusReportFilters
  reportData: PaymentStatusReport
  
  onFilterChange: (filters: PaymentStatusReportFilters) => void
  onGenerateReport: () => Promise<void>
  onExportReport: (format: 'pdf' | 'excel') => void
}

// Payment Status Alert Component
interface PaymentStatusAlertComponent {
  alerts: PaymentStatusAlert[]
  
  onViewAlert: (alert: PaymentStatusAlert) => void
  onDismissAlert: (alertId: number) => void
  onMarkAsResolved: (alertId: number) => Promise<void>
}

// Payment Status Statistics Component
interface PaymentStatusStatisticsComponent {
  statistics: PaymentStatusStatistics
  
  onRefreshStatistics: () => Promise<void>
  onViewDetails: (status: string) => void
}

// Payment Status Rules Component
interface PaymentStatusRulesComponent {
  rules: PaymentStatusRule[]
  
  onAddRule: (rule: PaymentStatusRule) => Promise<void>
  onEditRule: (ruleId: number, updates: Partial<PaymentStatusRule>) => Promise<void>
  onDeleteRule: (ruleId: number) => Promise<void>
  onToggleRule: (ruleId: number, isActive: boolean) => Promise<void>
}
```

---

### UI/UX Design

#### Payment Status Interface
- **Status Display:**
  - Color-coded status indicators
  - Status icons and badges
  - Real-time status updates
  - Hover tooltips with details

#### Status Update Form
- **Form Layout:**
  - Collapsible sections
  - Conditional field display
  - Real-time validation
  - Auto-save functionality

#### Status History View
- **History Display:**
  - Timeline view
  - Change details
  - User attribution
  - Export functionality

#### Bulk Update Interface
- **Bulk Operations:**
  - Multi-select functionality
  - Batch update form
  - Progress indicators
  - Confirmation dialogs

---

### Integration Requirements

#### Cost Item Integration
1. **Status Synchronization**
   - Real-time status updates
   - Automatic recalculation
   - Status propagation
   - Conflict resolution

2. **Data Consistency**
   - Validation rules
   - Business logic enforcement
   - Data integrity checks
   - Error handling

#### Reporting Integration
1. **Report Generation**
   - Scheduled reports
   - Custom report builder
   - Export functionality
   - Email notifications

2. **Analytics Integration**
   - Dashboard widgets
   - Trend analysis
   - Performance metrics
   - KPI tracking

---

### Security Considerations

#### Data Protection
- Status change logging
- User permission checks
- Audit trail maintenance
- Data validation

#### Access Control
- Role-based status updates
- Approval workflows
- Change authorization
- Sensitive data protection

---

### Testing Strategy

#### Unit Tests
- Status calculation logic
- Business rule validation
- Date comparison functions
- Status transition rules

#### Integration Tests
- Database operations
- API endpoint testing
- Bulk update functionality
- Report generation

#### User Acceptance Tests
- Status update workflow
- Bulk operations
- Report generation
- Alert functionality

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Status rule configuration
- Report template setup
- Alert configuration

#### Monitoring & Logging
- Status change tracking
- Performance monitoring
- Error logging
- User activity tracking

---

### Documentation

#### User Manual
- Status update procedures
- Bulk operation guide
- Report generation
- Alert management

#### Technical Documentation
- API documentation
- Database schema
- Business rules
- Integration guides 