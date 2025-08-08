# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-5.1
### Ghi nhận Lịch sử Thao tác Hợp đồng (Log)

#### Thông tin User Story
- **Story ID:** HD-5.1
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 5
- **Status:** To Do
- **Phụ thuộc:** HD-1.1, HD-2.1, HD-2.2

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách hợp đồng hoặc Quản trị viên hệ thống,  
**Tôi muốn** tất cả các hành động quan trọng liên quan đến hợp đồng (ví dụ: tạo mới, chỉnh sửa, xóa, thay đổi trạng thái) đều được ghi lại chính xác với thông tin về người thực hiện, thời gian và nội dung thay đổi,  
**Để** tôi có thể theo dõi toàn bộ lịch sử của hợp đồng, phục vụ công tác kiểm tra, đối chiếu và đảm bảo tính minh bạch.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Mỗi hợp đồng có một phần "Lịch sử hoạt động" hoặc "Log"
- [ ] Thông tin log bao gồm: thời gian, người thực hiện, loại hành động, và chi tiết liên quan
- [ ] Dữ liệu log không thể bị chỉnh sửa
- [ ] Log được ghi tự động cho tất cả các hành động quan trọng
- [ ] Có thể tìm kiếm và lọc log theo thời gian, người thực hiện, loại hành động
- [ ] Có thể xuất báo cáo log cho mục đích kiểm tra
- [ ] Log được lưu trữ an toàn và có thể truy xuất nhanh chóng
- [ ] Có thể xem chi tiết từng log entry với thông tin đầy đủ
- [ ] Hỗ trợ pagination cho danh sách log dài
- [ ] Có thể thiết lập retention policy cho log

#### 2.4 Activity Diagram
![HD-5.1 Activity Diagram](diagrams/HD-5.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý ghi nhận lịch sử thao tác hợp đồng*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Ghi Log Tự động**
   - Tạo log thời gian thực
   - Theo dõi hành động toàn diện
   - Records log không thể thay đổi
   - Tối ưu hóa hiệu suất

2. **Quản lý Log**
   - Phân loại log
   - Tìm kiếm và lọc
   - Chức năng xuất
   - Quản lý retention

3. **Audit Trail**
   - Lịch sử hành động hoàn chỉnh
   - Trách nhiệm người dùng
   - Tính toàn vẹn dữ liệu
   - Hỗ trợ tuân thủ

4. **Bảo mật Log**
   - Records không thể thay đổi
   - Kiểm soát truy cập
   - Mã hóa
   - Backup và khôi phục

#### Quy tắc Kinh doanh
- Tất cả log entries phải immutable (không thể chỉnh sửa)
- Log phải được ghi thời gian thực cho mọi hành động quan trọng
- Retention policy: 10 năm cho log hợp đồng
- Kiểm soát truy cập theo vai trò và quyền sở hữu hợp đồng
- Log phải bao gồm đầy đủ context và metadata

#### Các Hành động được Ghi Log
1. **Hành động Vòng đời Hợp đồng**
   - Tạo hợp đồng
   - Chỉnh sửa hợp đồng
   - Xóa hợp đồng
   - Khôi phục hợp đồng
   - Thay đổi trạng thái

2. **Hành động Tài chính**
   - Cập nhật ngân sách
   - Ghi nhận thanh toán
   - Liên kết chi phí
   - Tính toán tài chính

3. **Hành động Tài liệu**
   - Tải lên tài liệu
   - Chỉnh sửa tài liệu
   - Xóa tài liệu
   - Truy cập tài liệu

4. **Hành động Phân quyền**
   - Cấp quyền
   - Thu hồi quyền
   - Phân công vai trò
   - Thay đổi quyền truy cập

5. **Hành động Tích hợp**
   - Đồng bộ hệ thống bên ngoài
   - Gọi API
   - Nhập dữ liệu
   - Xuất dữ liệu

---

#### 5.5 Sequence Diagram
![HD-5.1 Sequence Diagram](diagrams/HD-5.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi ghi nhận lịch sử thao tác hợp đồng*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng log chính cho hợp đồng
CREATE TABLE contract_activity_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    action_type ENUM('create', 'update', 'delete', 'restore', 'status_change', 'budget_update', 'payment_record', 'cost_link', 'document_upload', 'document_modify', 'document_delete', 'permission_grant', 'permission_revoke', 'role_assignment', 'external_sync', 'api_call', 'data_import', 'data_export') NOT NULL,
    action_category ENUM('lifecycle', 'financial', 'document', 'permission', 'integration') NOT NULL,
    action_description TEXT NOT NULL,
    old_values JSON,
    new_values JSON,
    changed_fields JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_id VARCHAR(100),
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_contract_action (contract_id, action_type),
    INDEX idx_performed_at (performed_at),
    INDEX idx_performed_by (performed_by),
    INDEX idx_action_category (action_category)
);

-- Bảng log chi tiết cho từng thay đổi
CREATE TABLE contract_change_details (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    log_id BIGINT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type ENUM('added', 'modified', 'removed') NOT NULL,
    
    FOREIGN KEY (log_id) REFERENCES contract_activity_logs(id) ON DELETE CASCADE,
    INDEX idx_log_id (log_id),
    INDEX idx_field_name (field_name)
);

-- Bảng metadata cho log
CREATE TABLE contract_log_metadata (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    log_id BIGINT NOT NULL,
    metadata_key VARCHAR(100) NOT NULL,
    metadata_value TEXT,
    
    FOREIGN KEY (log_id) REFERENCES contract_activity_logs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_log_metadata (log_id, metadata_key)
);

-- Bảng cấu hình log
CREATE TABLE contract_log_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action_type VARCHAR(100) NOT NULL,
    is_logged BOOLEAN DEFAULT TRUE,
    log_level ENUM('info', 'warning', 'error', 'critical') DEFAULT 'info',
    retention_days INT DEFAULT 3650, -- 10 years
    include_old_values BOOLEAN DEFAULT TRUE,
    include_new_values BOOLEAN DEFAULT TRUE,
    include_metadata BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_action_type (action_type)
);

-- Bảng log summary cho báo cáo
CREATE TABLE contract_log_summaries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    summary_date DATE NOT NULL,
    total_actions INT DEFAULT 0,
    actions_by_type JSON,
    actions_by_user JSON,
    actions_by_category JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    UNIQUE KEY unique_contract_date (contract_id, summary_date),
    INDEX idx_summary_date (summary_date)
);

-- Insert default log configuration
INSERT INTO contract_log_config (action_type, is_logged, log_level, retention_days) VALUES
-- Lifecycle actions
('create', TRUE, 'info', 3650),
('update', TRUE, 'info', 3650),
('delete', TRUE, 'warning', 3650),
('restore', TRUE, 'info', 3650),
('status_change', TRUE, 'info', 3650),

-- Financial actions
('budget_update', TRUE, 'info', 3650),
('payment_record', TRUE, 'info', 3650),
('cost_link', TRUE, 'info', 3650),

-- Document actions
('document_upload', TRUE, 'info', 3650),
('document_modify', TRUE, 'info', 3650),
('document_delete', TRUE, 'warning', 3650),

-- Permission actions
('permission_grant', TRUE, 'info', 3650),
('permission_revoke', TRUE, 'warning', 3650),
('role_assignment', TRUE, 'info', 3650),

-- Integration actions
('external_sync', TRUE, 'info', 3650),
('api_call', TRUE, 'info', 3650),
('data_import', TRUE, 'info', 3650),
('data_export', TRUE, 'info', 3650);
```

#### API Endpoints
```
# Contract Activity Logs
GET /api/contracts/{id}/activity-logs
GET /api/contracts/{id}/activity-logs/{log_id}
GET /api/contracts/{id}/activity-logs/summary

# Log Search and Filter
GET /api/contracts/{id}/activity-logs/search
{
  "action_type": "update",
  "action_category": "financial",
  "performed_by": 123,
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "page": 1,
  "limit": 50
}

# Log Export
GET /api/contracts/{id}/activity-logs/export
{
  "format": "excel",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "include_details": true
}

# Log Configuration
GET /api/contracts/activity-logs/config
PUT /api/contracts/activity-logs/config
{
  "action_type": "update",
  "is_logged": true,
  "log_level": "info",
  "retention_days": 3650
}

# Log Statistics
GET /api/contracts/{id}/activity-logs/stats
Response: {
  "total_logs": 150,
  "logs_by_type": {
    "update": 45,
    "status_change": 30,
    "document_upload": 25
  },
  "logs_by_user": {
    "user_123": 50,
    "user_456": 40
  },
  "logs_by_category": {
    "lifecycle": 60,
    "financial": 40,
    "document": 30
  }
}

# Bulk Log Operations
GET /api/contracts/activity-logs/bulk
{
  "contract_ids": [1, 2, 3],
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}

# Log Retention
POST /api/contracts/activity-logs/cleanup
{
  "retention_days": 3650,
  "dry_run": false
}
```

#### Frontend Components
```typescript
// Activity Log Component
interface ActivityLogComponent {
  contractId: number
  logs: ContractActivityLog[]
  isLoading: boolean
  filters: LogFilters
  
  onViewLog: (logId: number) => void
  onFilterLogs: (filters: LogFilters) => void
  onExportLogs: (format: string) => Promise<void>
  onLoadMore: () => void
}

// Log Detail Component
interface LogDetailComponent {
  log: ContractActivityLog
  isOpen: boolean
  
  onClose: () => void
  onExportDetail: () => void
  onViewRelatedLogs: () => void
}

// Log Search Component
interface LogSearchComponent {
  searchQuery: string
  searchResults: ContractActivityLog[]
  isSearching: boolean
  
  onSearch: (query: string, filters: SearchFilters) => Promise<void>
  onClearSearch: () => void
  onSelectResult: (log: ContractActivityLog) => void
}

// Log Filter Component
interface LogFilterComponent {
  filters: LogFilters
  availableFilters: FilterOptions
  
  onFilterChange: (filters: LogFilters) => void
  onResetFilters: () => void
  onSaveFilter: (filterName: string) => void
  onLoadFilter: (filterName: string) => void
}

// Log Statistics Component
interface LogStatisticsComponent {
  contractId: number
  statistics: LogStatistics
  
  onViewTypeDetails: (actionType: string) => void
  onViewUserDetails: (userId: number) => void
  onViewCategoryDetails: (category: string) => void
  onExportStatistics: () => void
}

// Log Configuration Component
interface LogConfigurationComponent {
  config: LogConfig[]
  
  onUpdateConfig: (actionType: string, config: Partial<LogConfig>) => Promise<void>
  onResetConfig: () => Promise<void>
  onExportConfig: () => void
}

// Log Timeline Component
interface LogTimelineComponent {
  logs: ContractActivityLog[]
  timelineView: 'list' | 'timeline' | 'calendar'
  
  onViewChange: (view: string) => void
  onTimelineClick: (log: ContractActivityLog) => void
  onDateRangeChange: (startDate: Date, endDate: Date) => void
}

// Log Export Component
interface LogExportComponent {
  contractId: number
  exportOptions: ExportOptions
  
  onExport: (options: ExportOptions) => Promise<void>
  onScheduleExport: (schedule: ExportSchedule) => Promise<void>
  onViewExportHistory: () => void
}

// Log Retention Component
interface LogRetentionComponent {
  retentionConfig: RetentionConfig
  
  onUpdateRetention: (config: RetentionConfig) => Promise<void>
  onRunCleanup: (dryRun: boolean) => Promise<void>
  onViewRetentionStats: () => void
}
```

---

### UI/UX Design

#### Activity Log Interface
- **Log List View:**
  - Chronological timeline
  - Action type icons
  - User avatars
  - Timestamp formatting
  - Action descriptions

#### Log Detail View
- **Detail Modal:**
  - Complete log information
  - Before/after values
  - Metadata display
  - Related actions
  - Export options

#### Log Search Interface
- **Search Bar:**
  - Real-time search
  - Filter options
  - Search suggestions
  - Advanced search

#### Log Statistics Dashboard
- **Statistics Cards:**
  - Action type distribution
  - User activity heatmap
  - Time-based trends
  - Category breakdown

---

### Integration Requirements

#### Logging System Integration
1. **Automatic Logging**
   - Hook into all contract actions
   - Capture complete context
   - Performance optimization
   - Error handling

2. **Data Synchronization**
   - Real-time log generation
   - Cross-module logging
   - External system integration
   - Audit trail maintenance

#### Security Integration
1. **Log Security**
   - Immutable log storage
   - Access control
   - Encryption at rest
   - Secure transmission

2. **Compliance Support**
   - Regulatory requirements
   - Audit trail preservation
   - Data retention policies
   - Legal hold support

---

### Security Considerations

#### Log Protection
- Immutable log records
- Encrypted log storage
- Access control for log viewing
- Secure log transmission

#### Data Integrity
- Tamper-proof logging
- Hash verification
- Backup and recovery
- Audit trail preservation

#### Access Control
- Role-based log access
- Sensitive data masking
- Export restrictions
- Retention enforcement

---

### Testing Strategy

#### Unit Tests
- Log generation accuracy
- Data capture completeness
- Performance optimization
- Error handling

#### Integration Tests
- Cross-module logging
- External system integration
- Real-time synchronization
- Export functionality

#### User Acceptance Tests
- Log interface usability
- Search and filter functionality
- Export capabilities
- Performance under load

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Log configuration setup
- Retention policy configuration
- Performance monitoring

#### Monitoring & Logging
- Log generation monitoring
- Performance tracking
- Storage usage monitoring
- Error tracking

---

### Documentation

#### User Manual
- Log viewing guide
- Search and filter instructions
- Export procedures
- Configuration management

#### Technical Documentation
- API documentation
- Logging architecture
- Security implementation
- Performance optimization 