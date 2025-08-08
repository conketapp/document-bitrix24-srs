# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-5.1
### Ghi nhận Lịch sử Thao tác Chi phí (Log)

#### Thông tin User Story
- **Story ID:** CP-5.1
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 5
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-2.1, CP-2.2

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí hoặc Quản trị viên hệ thống,  
**Tôi muốn** tất cả các hành động quan trọng liên quan đến chi phí (ví dụ: tạo mới, chỉnh sửa, xóa, thay đổi trạng thái thanh toán) đều được ghi lại chính xác với thông tin về người thực hiện, thời gian và nội dung thay đổi  
**Để** tôi có thể theo dõi toàn bộ lịch sử của khoản mục chi phí, phục vụ công tác kiểm tra, đối chiếu và đảm bảo tính minh bạch.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Mỗi khoản mục chi phí có một phần "Lịch sử hoạt động" hoặc "Log"
- [ ] Thông tin log bao gồm: thời gian, người thực hiện, loại hành động, và chi tiết liên quan
- [ ] Dữ liệu log không thể bị chỉnh sửa
- [ ] Hệ thống tự động ghi log cho tất cả các hành động quan trọng
- [ ] Có thể xem lịch sử log theo thời gian, người thực hiện, loại hành động
- [ ] Có thể tìm kiếm và lọc log theo nhiều tiêu chí
- [ ] Có thể xuất báo cáo lịch sử log
- [ ] Log được lưu trữ an toàn và có thể sao lưu
- [ ] Hệ thống hiển thị thông báo khi có thay đổi quan trọng
- [ ] Có thể xem chi tiết thay đổi (diff) giữa các phiên bản
- [ ] Log được mã hóa để đảm bảo tính bảo mật

---

### Functional Requirements

#### Core Features
1. **Automatic Logging**
   - Automatic capture of all important actions
   - Real-time log generation
   - Comprehensive action tracking
   - Secure log storage

2. **Log Information**
   - Timestamp and user information
   - Action type and details
   - Field-level change tracking
   - Context preservation

3. **Log Display**
   - Chronological log view
   - Filtered and searchable logs
   - Detailed change information
   - Export capabilities

4. **Log Security**
   - Immutable log records
   - Encrypted log storage
   - Access control
   - Audit trail

#### Business Rules
- Tất cả các hành động quan trọng phải được ghi log tự động
- Log không thể bị chỉnh sửa hoặc xóa
- Log phải được lưu trữ ít nhất 7 năm theo quy định
- Chỉ người có quyền mới được xem log chi tiết
- Log phải được mã hóa để đảm bảo bảo mật

#### Logged Actions
1. **Cost Item Lifecycle**
   - Tạo mới khoản mục chi phí
   - Chỉnh sửa thông tin chi phí
   - Xóa khoản mục chi phí
   - Khôi phục khoản mục chi phí

2. **Status Changes**
   - Thay đổi trạng thái phê duyệt
   - Thay đổi trạng thái thanh toán
   - Thay đổi trạng thái thực hiện
   - Thay đổi trạng thái nghiệm thu

3. **Financial Operations**
   - Cập nhật số tiền
   - Thay đổi tỷ lệ VAT
   - Cập nhật thông tin thanh toán
   - Thay đổi đơn vị tiền tệ

4. **Relationship Changes**
   - Liên kết với dự án
   - Liên kết với hợp đồng
   - Liên kết với gói thầu
   - Thay đổi nhà cung cấp

5. **Document Operations**
   - Tải lên tài liệu
   - Xóa tài liệu
   - Cập nhật tài liệu
   - Thay đổi quyền truy cập

6. **Task Operations**
   - Tạo tác vụ mới
   - Cập nhật tác vụ
   - Hoàn thành tác vụ
   - Gán tác vụ

#### Log Information Fields
1. **Basic Information**
   - Timestamp (thời gian)
   - User ID (người thực hiện)
   - Session ID (phiên làm việc)
   - IP Address (địa chỉ IP)

2. **Action Information**
   - Action type (loại hành động)
   - Action description (mô tả hành động)
   - Entity type (loại đối tượng)
   - Entity ID (ID đối tượng)

3. **Change Information**
   - Field name (tên trường)
   - Old value (giá trị cũ)
   - New value (giá trị mới)
   - Change type (loại thay đổi)

4. **Context Information**
   - Related entities (đối tượng liên quan)
   - Business context (ngữ cảnh nghiệp vụ)
   - System context (ngữ cảnh hệ thống)
   - User context (ngữ cảnh người dùng)

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng log chính cho khoản mục chi phí
CREATE TABLE cost_item_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    log_type ENUM('create', 'update', 'delete', 'restore', 'status_change', 'payment_change', 'document_change', 'task_change', 'relationship_change') NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    action_description TEXT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    business_context JSON,
    system_context JSON,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_log_type (log_type),
    INDEX idx_performed_at (performed_at),
    INDEX idx_performed_by (performed_by),
    INDEX idx_session_id (session_id)
);

-- Bảng chi tiết thay đổi trong log
CREATE TABLE cost_item_log_changes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    log_id BIGINT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    field_label VARCHAR(200) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_type ENUM('added', 'updated', 'deleted', 'unchanged') NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (log_id) REFERENCES cost_item_logs(id) ON DELETE CASCADE,
    INDEX idx_log_id (log_id),
    INDEX idx_field_name (field_name),
    INDEX idx_change_type (change_type)
);

-- Bảng log bảo mật
CREATE TABLE cost_item_security_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    security_event_type ENUM('access_granted', 'access_denied', 'permission_changed', 'data_exported', 'data_imported', 'audit_reviewed') NOT NULL,
    event_description TEXT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    security_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_security_event_type (security_event_type),
    INDEX idx_performed_at (performed_at),
    INDEX idx_security_level (security_level)
);

-- Bảng cấu hình log
CREATE TABLE cost_log_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    log_type VARCHAR(100) NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    log_level ENUM('basic', 'detailed', 'verbose') DEFAULT 'detailed',
    retention_days INT DEFAULT 2555, -- 7 years
    encryption_enabled BOOLEAN DEFAULT TRUE,
    compression_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_log_type (log_type),
    INDEX idx_is_enabled (is_enabled),
    INDEX idx_log_level (log_level)
);

-- Bảng thống kê log
CREATE TABLE cost_log_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    total_logs INT DEFAULT 0,
    logs_by_type JSON,
    logs_by_user JSON,
    last_activity_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    UNIQUE KEY unique_cost_item (cost_item_id),
    INDEX idx_total_logs (total_logs),
    INDEX idx_last_activity (last_activity_at)
);

-- Insert default log configuration
INSERT INTO cost_log_config (log_type, is_enabled, log_level, retention_days) VALUES
('create', TRUE, 'detailed', 2555),
('update', TRUE, 'detailed', 2555),
('delete', TRUE, 'detailed', 2555),
('restore', TRUE, 'detailed', 2555),
('status_change', TRUE, 'detailed', 2555),
('payment_change', TRUE, 'detailed', 2555),
('document_change', TRUE, 'detailed', 2555),
('task_change', TRUE, 'detailed', 2555),
('relationship_change', TRUE, 'detailed', 2555),
('security_event', TRUE, 'verbose', 2555);
```

#### API Endpoints
```typescript
# Get Cost Item Logs
GET /api/cost-items/{id}/logs
{
  "page": 1,
  "limit": 50,
  "log_type_filter": "update",
  "user_filter": 456,
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "include_changes": true
}
Response: {
  "logs": [
    {
      "id": 123,
      "log_type": "update",
      "action_type": "cost_item_updated",
      "action_description": "Cập nhật thông tin chi phí thiết bị",
      "performed_by": 456,
      "performed_by_name": "Nguyễn Văn A",
      "performed_at": "2024-01-25T10:30:00Z",
      "session_id": "session_123",
      "ip_address": "192.168.1.100",
      "changes": [
        {
          "field_name": "cost_name",
          "field_label": "Tên chi phí",
          "old_value": "Chi phí thiết bị văn phòng",
          "new_value": "Chi phí thiết bị văn phòng - Cập nhật",
          "change_type": "updated",
          "data_type": "string"
        },
        {
          "field_name": "total_amount",
          "field_label": "Tổng chi phí",
          "old_value": "50000000",
          "new_value": "55000000",
          "change_type": "updated",
          "data_type": "decimal"
        }
      ],
      "business_context": {
        "project_id": 123,
        "contract_id": 456,
        "reason": "Cập nhật theo yêu cầu của ban quản lý"
      }
    }
  ],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 50,
    "total_pages": 3
  },
  "statistics": {
    "total_logs": 150,
    "logs_by_type": {
      "create": 1,
      "update": 120,
      "status_change": 20,
      "payment_change": 9
    },
    "logs_by_user": {
      "user_456": 80,
      "user_789": 70
    }
  }
}

# Get Log Details
GET /api/cost-items/{id}/logs/{log_id}
Response: {
  "log": {
    "id": 123,
    "log_type": "update",
    "action_type": "cost_item_updated",
    "action_description": "Cập nhật thông tin chi phí thiết bị",
    "performed_by": 456,
    "performed_by_name": "Nguyễn Văn A",
    "performed_at": "2024-01-25T10:30:00Z",
    "session_id": "session_123",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "changes": [
      {
        "field_name": "cost_name",
        "field_label": "Tên chi phí",
        "old_value": "Chi phí thiết bị văn phòng",
        "new_value": "Chi phí thiết bị văn phòng - Cập nhật",
        "change_type": "updated",
        "data_type": "string"
      }
    ],
    "business_context": {
      "project_id": 123,
      "contract_id": 456,
      "reason": "Cập nhật theo yêu cầu của ban quản lý"
    },
    "system_context": {
      "module": "cost_management",
      "submodule": "cost_item_edit",
      "workflow_step": "edit_form"
    }
  }
}

# Search Logs
GET /api/cost-items/{id}/logs/search
{
  "query": "thiết bị",
  "log_types": ["update", "status_change"],
  "users": [456, 789],
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "include_changes": true
}

# Export Logs
GET /api/cost-items/{id}/logs/export
{
  "format": "excel",
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "include_changes": true,
  "include_context": true
}
Response: File download with log data

# Get Log Statistics
GET /api/cost-items/{id}/logs/statistics
Response: {
  "total_logs": 150,
  "logs_by_type": {
    "create": 1,
    "update": 120,
    "status_change": 20,
    "payment_change": 9
  },
  "logs_by_user": {
    "user_456": 80,
    "user_789": 70
  },
  "logs_by_date": {
    "2024-01-25": 15,
    "2024-01-24": 12,
    "2024-01-23": 8
  },
  "most_active_users": [
    {
      "user_id": 456,
      "user_name": "Nguyễn Văn A",
      "log_count": 80,
      "last_activity": "2024-01-25T10:30:00Z"
    }
  ],
  "most_changed_fields": [
    {
      "field_name": "cost_name",
      "change_count": 45
    },
    {
      "field_name": "total_amount",
      "change_count": 30
    }
  ]
}

# Get Security Logs
GET /api/cost-items/{id}/security-logs
{
  "page": 1,
  "limit": 20,
  "security_level": "high",
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
Response: {
  "security_logs": [
    {
      "id": 1,
      "security_event_type": "access_granted",
      "event_description": "Người dùng được cấp quyền truy cập chi phí",
      "performed_by": 456,
      "performed_at": "2024-01-25T10:30:00Z",
      "ip_address": "192.168.1.100",
      "security_level": "medium"
    }
  ]
}

# Get Log Configuration
GET /api/cost-items/log-config
Response: {
  "log_config": {
    "create": {
      "is_enabled": true,
      "log_level": "detailed",
      "retention_days": 2555
    },
    "update": {
      "is_enabled": true,
      "log_level": "detailed",
      "retention_days": 2555
    }
  }
}
```

#### Frontend Components
```typescript
// Cost Item Log List Component
interface CostItemLogListComponent {
  costItemId: number
  logs: CostItemLog[]
  filters: LogFilters
  
  onLogSelect: (log: CostItemLog) => void
  onFilterChange: (filters: LogFilters) => void
  onSearchLogs: (query: string) => void
  onExportLogs: () => void
}

// Log Detail Component
interface LogDetailComponent {
  log: CostItemLog
  isVisible: boolean
  
  onClose: () => void
  onExportLog: () => void
  onViewChanges: () => void
}

// Log Changes Component
interface LogChangesComponent {
  changes: LogChange[]
  
  onViewFieldDetails: (change: LogChange) => void
  onCompareValues: (oldValue: any, newValue: any) => void
}

// Log Filter Component
interface LogFilterComponent {
  filters: LogFilters
  
  onFilterChange: (filters: LogFilters) => void
  onClearFilters: () => void
  onSaveFilter: (filterName: string) => void
}

// Log Statistics Component
interface LogStatisticsComponent {
  costItemId: number
  statistics: LogStatistics
  
  onRefreshStatistics: () => Promise<void>
  onViewDetails: (category: string) => void
  onExportStatistics: () => void
}

// Log Search Component
interface LogSearchComponent {
  searchQuery: string
  searchFilters: LogSearchFilters
  
  onSearch: (query: string) => void
  onFilterChange: (filters: LogSearchFilters) => void
  onClearSearch: () => void
}

// Security Log Component
interface SecurityLogComponent {
  costItemId: number
  securityLogs: SecurityLog[]
  
  onViewSecurityLog: (log: SecurityLog) => void
  onExportSecurityLogs: () => void
  onFilterSecurityLogs: (filters: SecurityLogFilters) => void
}

// Log Export Component
interface LogExportComponent {
  costItemId: number
  exportOptions: LogExportOptions
  
  onExport: (format: string, options: LogExportOptions) => Promise<void>
  onPreviewExport: () => void
}

// Log Timeline Component
interface LogTimelineComponent {
  logs: CostItemLog[]
  
  onLogSelect: (log: CostItemLog) => void
  onTimelineFilter: (filters: TimelineFilters) => void
}

// Log Comparison Component
interface LogComparisonComponent {
  oldLog: CostItemLog
  newLog: CostItemLog
  
  onViewDiff: () => void
  onExportComparison: () => void
}
```

---

### UI/UX Design

#### Log Display Interface
- **Log List Layout:**
  - Timeline view
  - Filtered display
  - Search functionality
  - Export options

#### Log Detail Interface
- **Detail View:**
  - Complete log information
  - Change details
  - Context information
  - Security information

#### Log Filter Interface
- **Filter Controls:**
  - Date range selection
  - User filtering
  - Action type filtering
  - Advanced search

#### Log Statistics Interface
- **Statistics Dashboard:**
  - Activity overview
  - User activity
  - Change patterns
  - Security events

---

### Integration Requirements

#### Cost Item Integration
1. **Automatic Logging**
   - Real-time log capture
   - Change detection
   - Context preservation
   - Security tracking

2. **Log Retrieval**
   - Efficient querying
   - Filtered access
   - Secure retrieval
   - Performance optimization

#### Security Integration
1. **Access Control**
   - Permission-based access
   - Role-based filtering
   - Audit trail
   - Security monitoring

2. **Data Protection**
   - Encrypted storage
   - Immutable records
   - Backup procedures
   - Retention policies

---

### Security Considerations

#### Data Protection
- Log encryption
- Immutable log records
- Access control
- Audit trail

#### Log Security
- Secure storage
- Tamper detection
- Access logging
- Data integrity

---

### Testing Strategy

#### Unit Tests
- Log generation logic
- Change detection
- Security validation
- Export functionality

#### Integration Tests
- Database operations
- API endpoint testing
- Security integration
- Performance testing

#### User Acceptance Tests
- Log viewing workflow
- Search functionality
- Export capabilities
- Security validation

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Log configuration
- Security setup
- Retention policies

#### Monitoring & Logging
- Log performance monitoring
- Storage monitoring
- Security monitoring
- Error tracking

---

### Documentation

#### User Manual
- Log viewing procedures
- Search and filter
- Export functionality
- Security guidelines

#### Technical Documentation
- API documentation
- Database schema
- Security implementation
- Integration guides 