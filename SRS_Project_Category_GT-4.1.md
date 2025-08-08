# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-4.1
### Ghi nhận Lịch sử Thao tác Gói thầu (Log)

#### Thông tin User Story
- **Story ID:** GT-4.1
- **Priority:** High
- **Story Points:** 6
- **Sprint:** Sprint 4
- **Status:** To Do
- **Dependencies:** GT-1.1, GT-2.1, GT-3.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách gói thầu hoặc Quản trị viên hệ thống,  
**Tôi muốn** tất cả các hành động quan trọng liên quan đến gói thầu (ví dụ: tạo mới, chỉnh sửa, xóa, lấy thông tin từ API) đều được ghi lại chính xác với thông tin về người thực hiện, thời gian và nội dung thay đổi,  
**Để** tôi có thể theo dõi toàn bộ lịch sử của gói thầu, phục vụ công tác kiểm tra, đối chiếu và đảm bảo tính minh bạch.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Mỗi gói thầu có một phần "Lịch sử hoạt động" hoặc "Log"
- [ ] Thông tin log bao gồm: thời gian, người thực hiện, loại hành động (tạo mới, chỉnh sửa, xóa, lấy thông tin API), và chi tiết liên quan (ví dụ: các trường đã thay đổi)
- [ ] Dữ liệu log không thể bị chỉnh sửa
- [ ] Có thể xem lịch sử theo thời gian, người thực hiện, loại hành động
- [ ] Có thể export log ra file (PDF, Excel)
- [ ] Có thể tìm kiếm và lọc log theo từ khóa
- [ ] Hiển thị chi tiết thay đổi trước và sau khi chỉnh sửa
- [ ] Có thể xem log của nhiều gói thầu cùng lúc
- [ ] Thông báo real-time cho các thay đổi quan trọng

#### 2.4 Activity Diagram
![GT-4.1 Activity Diagram](diagrams/GT-4.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý ghi nhận lịch sử thao tác gói thầu*

---

### Functional Requirements

#### Core Features
1. **Activity Logging System**
   - Automatic logging cho tất cả actions
   - Detailed change tracking
   - User action identification
   - Timestamp recording
   - IP address tracking

2. **Log Management**
   - Log storage và retrieval
   - Log filtering và search
   - Log export functionality
   - Log retention policies
   - Log backup và recovery

3. **Change Tracking**
   - Before/after value comparison
   - Field-level change tracking
   - Bulk change logging
   - API call logging
   - Error logging

4. **Audit Trail**
   - Immutable log records
   - Digital signatures
   - Tamper detection
   - Compliance reporting
   - Legal evidence support

#### Business Rules
- Tất cả actions phải được logged
- Log records không thể bị modified hoặc deleted
- Log retention: 7 năm theo quy định pháp luật
- Real-time logging không được delay
- Log data phải được encrypted
- Backup logs hàng ngày

#### Logged Actions
1. **Tender Package Actions**
   - CREATE_TENDER_PACKAGE
   - UPDATE_TENDER_PACKAGE
   - DELETE_TENDER_PACKAGE
   - RESTORE_TENDER_PACKAGE
   - CHANGE_STATUS

2. **Document Actions**
   - UPLOAD_DOCUMENT
   - DELETE_DOCUMENT
   - UPDATE_DOCUMENT
   - DOWNLOAD_DOCUMENT
   - PREVIEW_DOCUMENT

3. **API Integration Actions**
   - FETCH_PORTAL_DATA
   - SYNC_BITRIX_DATA
   - API_CALL_SUCCESS
   - API_CALL_ERROR

4. **Permission Actions**
   - GRANT_PERMISSION
   - REVOKE_PERMISSION
   - CHANGE_ROLE
   - APPROVE_CHANGE
   - REJECT_CHANGE

5. **System Actions**
   - LOGIN
   - LOGOUT
   - PASSWORD_CHANGE
   - PROFILE_UPDATE
   - SYSTEM_ERROR

---

### Technical Specifications

#### Sequence Diagram
![GT-4.1 Sequence Diagram](diagrams/GT-4.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi ghi nhận lịch sử thao tác gói thầu*

#### Database Schema Updates
```sql
-- Bảng lịch sử hoạt động chính
CREATE TABLE activity_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT,
    user_id INT NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    action_category ENUM('tender_package', 'document', 'api_integration', 'permission', 'system') NOT NULL,
    action_description TEXT NOT NULL,
    old_values JSON,
    new_values JSON,
    changed_fields JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bảng log chi tiết cho từng action
CREATE TABLE detailed_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    activity_log_id BIGINT NOT NULL,
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    change_type ENUM('added', 'modified', 'deleted') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (activity_log_id) REFERENCES activity_logs(id) ON DELETE CASCADE
);

-- Bảng cấu hình logging
CREATE TABLE logging_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action_type VARCHAR(100) NOT NULL,
    is_logged BOOLEAN DEFAULT TRUE,
    log_level ENUM('info', 'warning', 'error', 'critical') DEFAULT 'info',
    retention_days INT DEFAULT 2555, -- 7 years
    include_details BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_action_type (action_type)
);

-- Bảng log exports
CREATE TABLE log_exports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    export_name VARCHAR(255) NOT NULL,
    export_type ENUM('pdf', 'excel', 'csv') NOT NULL,
    date_range_start DATE,
    date_range_end DATE,
    filters JSON,
    file_path VARCHAR(500),
    file_size BIGINT,
    exported_by INT NOT NULL,
    exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (exported_by) REFERENCES users(id)
);

-- Bảng digital signatures cho logs
CREATE TABLE log_signatures (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    activity_log_id BIGINT NOT NULL,
    signature_hash VARCHAR(255) NOT NULL,
    signature_algorithm VARCHAR(50) NOT NULL,
    signed_by INT NOT NULL,
    signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (activity_log_id) REFERENCES activity_logs(id) ON DELETE CASCADE,
    FOREIGN KEY (signed_by) REFERENCES users(id)
);

-- Insert default logging configuration
INSERT INTO logging_config (action_type, is_logged, log_level, retention_days) VALUES
-- Tender Package Actions
('CREATE_TENDER_PACKAGE', TRUE, 'info', 2555),
('UPDATE_TENDER_PACKAGE', TRUE, 'info', 2555),
('DELETE_TENDER_PACKAGE', TRUE, 'warning', 2555),
('RESTORE_TENDER_PACKAGE', TRUE, 'info', 2555),
('CHANGE_STATUS', TRUE, 'info', 2555),

-- Document Actions
('UPLOAD_DOCUMENT', TRUE, 'info', 2555),
('DELETE_DOCUMENT', TRUE, 'warning', 2555),
('UPDATE_DOCUMENT', TRUE, 'info', 2555),
('DOWNLOAD_DOCUMENT', TRUE, 'info', 2555),
('PREVIEW_DOCUMENT', TRUE, 'info', 2555),

-- API Integration Actions
('FETCH_PORTAL_DATA', TRUE, 'info', 2555),
('SYNC_BITRIX_DATA', TRUE, 'info', 2555),
('API_CALL_SUCCESS', TRUE, 'info', 2555),
('API_CALL_ERROR', TRUE, 'error', 2555),

-- Permission Actions
('GRANT_PERMISSION', TRUE, 'warning', 2555),
('REVOKE_PERMISSION', TRUE, 'warning', 2555),
('CHANGE_ROLE', TRUE, 'warning', 2555),
('APPROVE_CHANGE', TRUE, 'info', 2555),
('REJECT_CHANGE', TRUE, 'info', 2555),

-- System Actions
('LOGIN', TRUE, 'info', 2555),
('LOGOUT', TRUE, 'info', 2555),
('PASSWORD_CHANGE', TRUE, 'warning', 2555),
('PROFILE_UPDATE', TRUE, 'info', 2555),
('SYSTEM_ERROR', TRUE, 'error', 2555);
```

#### API Endpoints
```
# Activity Logs
GET /api/tender-packages/{id}/activity-logs
GET /api/activity-logs
GET /api/activity-logs/{log_id}

# Log Filtering và Search
GET /api/activity-logs/search
{
  "tender_package_id": 123,
  "user_id": 456,
  "action_type": "UPDATE_TENDER_PACKAGE",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "action_category": "tender_package"
}

# Log Export
POST /api/activity-logs/export
{
  "export_type": "pdf",
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  },
  "filters": {
    "tender_package_ids": [1, 2, 3],
    "action_types": ["UPDATE_TENDER_PACKAGE", "DELETE_TENDER_PACKAGE"]
  }
}

# Log Statistics
GET /api/activity-logs/statistics
{
  "total_actions": 1500,
  "actions_by_type": {
    "UPDATE_TENDER_PACKAGE": 500,
    "UPLOAD_DOCUMENT": 300,
    "API_CALL_SUCCESS": 200
  },
  "actions_by_user": {
    "user_1": 200,
    "user_2": 150
  }
}

# Real-time Log Streaming
GET /api/activity-logs/stream
{
  "tender_package_id": 123,
  "action_types": ["UPDATE_TENDER_PACKAGE", "UPLOAD_DOCUMENT"]
}
```

#### Frontend Components
```typescript
// Activity Log Component
interface ActivityLogComponent {
  tenderPackageId?: number
  logs: ActivityLog[]
  isLoading: boolean
  onLoadMore: () => void
  onFilter: (filters: LogFilters) => void
  onExport: (exportOptions: ExportOptions) => void
}

// Activity Log Item
interface ActivityLogItem {
  log: ActivityLog
  onViewDetails: (logId: number) => void
  onCompareChanges: (logId: number) => void
  onExportLog: (logId: number) => void
}

// Log Filter Component
interface LogFilterComponent {
  filters: LogFilters
  onFilterChange: (filters: LogFilters) => void
  onClearFilters: () => void
  onApplyFilters: () => void
}

// Log Export Component
interface LogExportComponent {
  exportOptions: ExportOptions
  onExportTypeChange: (type: ExportType) => void
  onDateRangeChange: (range: DateRange) => void
  onFilterChange: (filters: LogFilters) => void
  onExport: () => Promise<void>
}

// Change Comparison Component
interface ChangeComparisonComponent {
  oldValues: Record<string, any>
  newValues: Record<string, any>
  changedFields: string[]
  onClose: () => void
}

// Real-time Log Stream
interface LogStreamComponent {
  tenderPackageId?: number
  actionTypes?: string[]
  onNewLog: (log: ActivityLog) => void
  onError: (error: string) => void
  onConnect: () => void
  onDisconnect: () => void
}

// Log Statistics Component
interface LogStatisticsComponent {
  statistics: LogStatistics
  onDateRangeChange: (range: DateRange) => void
  onRefresh: () => void
}
```

---

### UI/UX Design

#### Activity Log Interface
- **Layout:** Timeline view với filters
- **Components:**
  - Log timeline với timestamps
  - User avatars và names
  - Action type icons
  - Change indicators
  - Export buttons

#### Log Detail View
- **Layout:** Modal với detailed information
- **Components:**
  - Action summary
  - Before/after comparison
  - Changed fields highlight
  - User information
  - System context

#### Log Filter Panel
- **Layout:** Collapsible sidebar
- **Components:**
  - Date range picker
  - User selector
  - Action type checkboxes
  - Category filters
  - Search input

#### Export Interface
- **Layout:** Modal với export options
- **Components:**
  - Export format selector
  - Date range picker
  - Filter options
  - Preview button
  - Download button

---

### Integration Requirements

#### Logging System Integration
1. **Automatic Logging**
   - Intercept tất cả actions
   - Capture user context
   - Record system state
   - Generate unique IDs

2. **Real-time Processing**
   - Stream logs to UI
   - Process logs asynchronously
   - Handle high-volume logging
   - Error recovery

#### Security Integration
1. **Log Protection**
   - Encrypt log data
   - Digital signatures
   - Tamper detection
   - Access control

2. **Compliance Features**
   - Audit trail
   - Legal evidence
   - Retention policies
   - Reporting tools

---

### Security Considerations

#### Log Security
- Encrypt sensitive log data
- Digital signatures cho logs
- Tamper detection mechanisms
- Access control cho log viewing

#### Data Protection
- Secure log storage
- Backup và recovery
- Retention policies
- Privacy protection

#### Audit Compliance
- Immutable log records
- Legal evidence support
- Compliance reporting
- Digital signatures

---

### Testing Strategy

#### Unit Tests
- Logging logic validation
- Change tracking accuracy
- Export functionality
- Security mechanisms

#### Integration Tests
- End-to-end logging workflow
- Real-time log streaming
- Export process testing
- Security testing

#### User Acceptance Tests
- Log interface usability
- Filter và search experience
- Export functionality
- Real-time updates

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Logging configuration
- Security setup
- Backup configuration

#### Monitoring & Logging
- Log performance monitoring
- Storage usage tracking
- Error tracking
- Compliance monitoring

---

### Documentation

#### User Manual
- Log viewing guide
- Filter và search instructions
- Export procedures
- Real-time monitoring

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Performance optimization 