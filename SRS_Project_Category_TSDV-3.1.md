# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-3.1
### Theo dõi lịch sử sử dụng, bảo hành, bảo dưỡng của Tài sản

#### Thông tin User Story
- **Story ID:** TSDV-3.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 3
- **Status:** To Do
- **Dependencies:** TSDV-1.1, TSDV-1.2

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý tài sản,  
**Tôi muốn** có thể theo dõi chi tiết lịch sử sử dụng, bảo hành và bảo dưỡng của từng tài sản,  
**Để** tôi có thể nắm bắt toàn bộ các sự kiện quan trọng liên quan đến tài sản, hỗ trợ việc ra quyết định về sửa chữa, thay thế hoặc thanh lý.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Trên trang chi tiết của mỗi tài sản, có một phần "Lịch sử" hiển thị các sự kiện (ví dụ: đưa vào sử dụng, bảo dưỡng định kỳ, sửa chữa, thay thế linh kiện, kiểm tra, v.v.)
- [ ] Mỗi sự kiện bao gồm: ngày thực hiện, mô tả, người thực hiện, chi phí liên quan (nếu có)
- [ ] Có thể thêm sự kiện mới vào lịch sử tài sản
- [ ] Có thể chỉnh sửa thông tin sự kiện đã tạo
- [ ] Có thể xóa sự kiện không cần thiết
- [ ] Có thể lọc lịch sử theo loại sự kiện, khoảng thời gian
- [ ] Có thể tìm kiếm trong lịch sử theo từ khóa
- [ ] Có thể xuất lịch sử ra file Excel/PDF
- [ ] Có thể thiết lập cảnh báo cho các sự kiện sắp đến (bảo dưỡng, bảo hành)
- [ ] Có thể gắn file đính kèm cho từng sự kiện
- [ ] Có thể tính toán tổng chi phí bảo dưỡng, sửa chữa theo thời gian
- [ ] Có thể xem báo cáo thống kê về tình trạng tài sản

#### 2.4 Activity Diagram
![TSDV-3.1 Activity Diagram](diagrams/TSDV-3.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý theo dõi lịch sử Tài sản*

#### 2.5 Sequence Diagram
![TSDV-3.1 Sequence Diagram](diagrams/TSDV-3.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi theo dõi lịch sử Tài sản*

---

### Functional Requirements

#### Core Features
1. **History Tracking**
   - Event logging
   - Event categorization
   - Event details
   - Event timeline

2. **Event Types**
   - Usage events
   - Maintenance events
   - Warranty events
   - Repair events
   - Inspection events
   - Custom events

3. **Event Management**
   - Add events
   - Edit events
   - Delete events
   - Event validation

4. **History Analysis**
   - Cost analysis
   - Frequency analysis
   - Trend analysis
   - Performance metrics

#### Business Rules
- Mỗi sự kiện phải có ngày thực hiện và người thực hiện
- Sự kiện không thể được xóa sau khi đã được xác nhận
- Chi phí liên quan phải được ghi nhận chính xác
- Cảnh báo phải được gửi trước thời hạn bảo dưỡng/bảo hành
- File đính kèm phải có kích thước và định dạng phù hợp

#### Event Categories
1. **Usage Events**
   - Put into use
   - Take out of use
   - Transfer location
   - Change status
   - Assign user

2. **Maintenance Events**
   - Preventive maintenance
   - Corrective maintenance
   - Emergency maintenance
   - Scheduled maintenance
   - Maintenance inspection

3. **Warranty Events**
   - Warranty claim
   - Warranty service
   - Warranty extension
   - Warranty expiration
   - Warranty validation

4. **Repair Events**
   - Minor repair
   - Major repair
   - Component replacement
   - System upgrade
   - Emergency repair

5. **Inspection Events**
   - Regular inspection
   - Safety inspection
   - Quality inspection
   - Performance test
   - Compliance check

6. **Custom Events**
   - Custom event type
   - User-defined events
   - Special circumstances
   - External events

#### Event Details
1. **Basic Information**
   - Event date
   - Event type
   - Event description
   - Performed by
   - Location

2. **Cost Information**
   - Labor cost
   - Material cost
   - Service cost
   - Total cost
   - Cost breakdown

3. **Technical Information**
   - Technical details
   - Specifications
   - Measurements
   - Test results
   - Recommendations

4. **Documentation**
   - Attached files
   - Photos
   - Reports
   - Certificates
   - Manuals

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lịch sử sự kiện tài sản
CREATE TABLE asset_history_events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    event_type ENUM('usage', 'maintenance', 'warranty', 'repair', 'inspection', 'custom') NOT NULL,
    event_subtype VARCHAR(100),
    event_date DATE NOT NULL,
    event_time TIME,
    event_description TEXT NOT NULL,
    event_details JSON,
    performed_by INT NOT NULL,
    location VARCHAR(200),
    status ENUM('planned', 'in_progress', 'completed', 'cancelled', 'failed') DEFAULT 'completed',
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_asset_id (asset_id),
    INDEX idx_event_type (event_type),
    INDEX idx_event_date (event_date),
    INDEX idx_performed_by (performed_by),
    INDEX idx_status (status)
);

-- Bảng chi phí sự kiện
CREATE TABLE asset_event_costs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    cost_type ENUM('labor', 'material', 'service', 'other') NOT NULL,
    cost_description VARCHAR(200) NOT NULL,
    cost_amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'VND',
    cost_date DATE NOT NULL,
    invoice_number VARCHAR(100),
    supplier VARCHAR(200),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (event_id) REFERENCES asset_history_events(id) ON DELETE CASCADE,
    INDEX idx_event_id (event_id),
    INDEX idx_cost_type (cost_type),
    INDEX idx_cost_date (cost_date)
);

-- Bảng file đính kèm sự kiện
CREATE TABLE asset_event_attachments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    file_type VARCHAR(100),
    file_description TEXT,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (event_id) REFERENCES asset_history_events(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    INDEX idx_event_id (event_id),
    INDEX idx_file_type (file_type),
    INDEX idx_uploaded_at (uploaded_at)
);

-- Bảng cảnh báo sự kiện
CREATE TABLE asset_event_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    alert_type ENUM('maintenance', 'warranty', 'inspection', 'custom') NOT NULL,
    alert_title VARCHAR(200) NOT NULL,
    alert_description TEXT,
    alert_date DATE NOT NULL,
    alert_time TIME,
    alert_priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    is_active BOOLEAN DEFAULT TRUE,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP NULL,
    recipients JSON,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_asset_id (asset_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_alert_date (alert_date),
    INDEX idx_is_active (is_active),
    INDEX idx_is_sent (is_sent)
);

-- Bảng thống kê sự kiện
CREATE TABLE asset_event_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    statistic_date DATE NOT NULL,
    total_events INT DEFAULT 0,
    total_cost DECIMAL(15,2) DEFAULT 0,
    events_by_type JSON,
    costs_by_type JSON,
    maintenance_frequency DECIMAL(5,2) DEFAULT 0,
    average_repair_cost DECIMAL(15,2) DEFAULT 0,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    warranty_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    UNIQUE KEY unique_asset_date (asset_id, statistic_date),
    INDEX idx_asset_id (asset_id),
    INDEX idx_statistic_date (statistic_date)
);
```

#### API Endpoints
```typescript
# Get Asset History Events
GET /api/assets-services/{asset_id}/history
{
  "page": 1,
  "page_size": 20,
  "event_type": "maintenance",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "events": [
    {
      "id": 123,
      "asset_id": 456,
      "event_type": "maintenance",
      "event_subtype": "preventive",
      "event_date": "2024-01-15",
      "event_time": "09:30:00",
      "event_description": "Bảo dưỡng định kỳ máy chủ Dell PowerEdge R740",
      "event_details": {
        "maintenance_type": "preventive",
        "maintenance_items": ["CPU check", "Memory test", "Disk health", "Network test"],
        "findings": "Tất cả thành phần hoạt động bình thường",
        "recommendations": "Tiếp tục sử dụng bình thường"
      },
      "performed_by": "Nguyễn Văn A",
      "location": "Data Center A",
      "status": "completed",
      "priority": "medium",
      "total_cost": 500000,
      "attachments_count": 2,
      "created_at": "2024-01-15T09:30:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "page_size": 20
  },
  "statistics": {
    "total_events": 100,
    "total_cost": 15000000,
    "events_by_type": {
      "maintenance": 40,
      "repair": 25,
      "inspection": 20,
      "usage": 15
    },
    "costs_by_type": {
      "maintenance": 8000000,
      "repair": 5000000,
      "inspection": 1500000,
      "usage": 500000
    }
  }
}

# Create Asset History Event
POST /api/assets-services/{asset_id}/history
{
  "event_type": "maintenance",
  "event_subtype": "preventive",
  "event_date": "2024-01-20",
  "event_time": "10:00:00",
  "event_description": "Bảo dưỡng định kỳ máy chủ Dell PowerEdge R740",
  "event_details": {
    "maintenance_type": "preventive",
    "maintenance_items": ["CPU check", "Memory test", "Disk health", "Network test"],
    "findings": "Tất cả thành phần hoạt động bình thường",
    "recommendations": "Tiếp tục sử dụng bình thường"
  },
  "performed_by": 1,
  "location": "Data Center A",
  "status": "completed",
  "priority": "medium",
  "costs": [
    {
      "cost_type": "labor",
      "cost_description": "Chi phí nhân công bảo dưỡng",
      "cost_amount": 300000,
      "currency": "VND"
    },
    {
      "cost_type": "material",
      "cost_description": "Chi phí vật tư thay thế",
      "cost_amount": 200000,
      "currency": "VND"
    }
  ]
}
Response: {
  "success": true,
  "event_id": 124,
  "message": "Sự kiện đã được tạo thành công"
}

# Update Asset History Event
PUT /api/assets-services/{asset_id}/history/{event_id}
{
  "event_description": "Bảo dưỡng định kỳ máy chủ Dell PowerEdge R740 - Cập nhật",
  "event_details": {
    "maintenance_type": "preventive",
    "maintenance_items": ["CPU check", "Memory test", "Disk health", "Network test", "Fan check"],
    "findings": "Tất cả thành phần hoạt động bình thường, quạt làm mát cần vệ sinh",
    "recommendations": "Vệ sinh quạt làm mát định kỳ"
  },
  "status": "completed",
  "costs": [
    {
      "cost_type": "labor",
      "cost_description": "Chi phí nhân công bảo dưỡng",
      "cost_amount": 350000,
      "currency": "VND"
    },
    {
      "cost_type": "material",
      "cost_description": "Chi phí vật tư thay thế",
      "cost_amount": 250000,
      "currency": "VND"
    }
  ]
}
Response: {
  "success": true,
  "message": "Sự kiện đã được cập nhật thành công"
}

# Delete Asset History Event
DELETE /api/assets-services/{asset_id}/history/{event_id}
Response: {
  "success": true,
  "message": "Sự kiện đã được xóa thành công"
}

# Get Event Costs
GET /api/assets-services/{asset_id}/history/{event_id}/costs
Response: {
  "costs": [
    {
      "id": 456,
      "event_id": 123,
      "cost_type": "labor",
      "cost_description": "Chi phí nhân công bảo dưỡng",
      "cost_amount": 300000,
      "currency": "VND",
      "cost_date": "2024-01-15",
      "invoice_number": "INV-2024-001",
      "supplier": "Công ty Bảo dưỡng ABC",
      "notes": "Chi phí nhân công theo hợp đồng"
    },
    {
      "id": 457,
      "event_id": 123,
      "cost_type": "material",
      "cost_description": "Chi phí vật tư thay thế",
      "cost_amount": 200000,
      "currency": "VND",
      "cost_date": "2024-01-15",
      "invoice_number": "INV-2024-002",
      "supplier": "Công ty Vật tư XYZ",
      "notes": "Vật tư thay thế theo yêu cầu"
    }
  ],
  "total_cost": 500000,
  "cost_breakdown": {
    "labor": 300000,
    "material": 200000,
    "service": 0,
    "other": 0
  }
}

# Get Asset Statistics
GET /api/assets-services/{asset_id}/statistics
{
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "statistics": {
    "total_events": 100,
    "total_cost": 15000000,
    "events_by_type": {
      "maintenance": 40,
      "repair": 25,
      "inspection": 20,
      "usage": 15
    },
    "costs_by_type": {
      "labor": 8000000,
      "material": 5000000,
      "service": 1500000,
      "other": 500000
    },
    "maintenance_frequency": 2.5,
    "average_repair_cost": 200000,
    "last_maintenance_date": "2024-01-15",
    "next_maintenance_date": "2024-02-20",
    "warranty_status": "active",
    "performance_metrics": {
      "uptime_percentage": 99.5,
      "availability_score": 95.2,
      "reliability_index": 92.8
    }
  }
}

# Export Asset History
POST /api/assets-services/{asset_id}/history/export
{
  "export_format": "excel",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "event_types": ["maintenance", "repair", "inspection"],
  "include_costs": true,
  "include_attachments": false
}
Response: File download with asset history

# Get Asset Timeline
GET /api/assets-services/{asset_id}/timeline
{
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "timeline": [
    {
      "date": "2024-01-15",
      "events": [
        {
          "id": 123,
          "event_type": "maintenance",
          "event_subtype": "preventive",
          "event_description": "Bảo dưỡng định kỳ máy chủ Dell PowerEdge R740",
          "performed_by": "Nguyễn Văn A",
          "status": "completed",
          "total_cost": 500000
        }
      ]
    },
    {
      "date": "2024-01-20",
      "events": [
        {
          "id": 124,
          "event_type": "inspection",
          "event_subtype": "regular",
          "event_description": "Kiểm tra định kỳ máy chủ Dell PowerEdge R740",
          "performed_by": "Trần Thị B",
          "status": "completed",
          "total_cost": 100000
        }
      ]
    }
  ]
}
```

#### Frontend Components
```typescript
// Asset History Component
interface AssetHistoryComponent {
  assetId: number
  events: AssetEvent[]
  statistics: AssetStatistics
  pagination: PaginationInfo
  
  onEventSelect: (event: AssetEvent) => void
  onEventAdd: (event: AssetEvent) => Promise<void>
  onEventEdit: (event: AssetEvent) => Promise<void>
  onEventDelete: (eventId: number) => Promise<void>
  onEventFilter: (filters: EventFilters) => void
  onPageChange: (page: number) => void
}

// Event Form Component
interface EventFormComponent {
  event: AssetEvent
  assetId: number
  eventTypes: EventType[]
  
  onEventSave: (event: AssetEvent) => Promise<void>
  onEventCancel: () => void
  onEventValidate: (event: AssetEvent) => boolean
  onCostAdd: (cost: EventCost) => void
  onCostRemove: (costId: number) => void
}

// Event Details Component
interface EventDetailsComponent {
  event: AssetEvent
  costs: EventCost[]
  attachments: EventAttachment[]
  
  onEventEdit: (event: AssetEvent) => void
  onEventDelete: (eventId: number) => void
  onCostAdd: (cost: EventCost) => Promise<void>
  onCostEdit: (cost: EventCost) => Promise<void>
  onCostDelete: (costId: number) => Promise<void>
  onAttachmentUpload: (file: File) => Promise<void>
  onAttachmentDownload: (attachment: EventAttachment) => void
  onAttachmentDelete: (attachmentId: number) => Promise<void>
}

// Event Timeline Component
interface EventTimelineComponent {
  timeline: TimelineEvent[]
  selectedDate: Date
  
  onDateSelect: (date: Date) => void
  onEventSelect: (event: AssetEvent) => void
  onTimelineFilter: (filters: TimelineFilters) => void
  onTimelineExport: () => void
}

// Asset Statistics Component
interface AssetStatisticsComponent {
  statistics: AssetStatistics
  assetId: number
  
  onDateRangeChange: (range: DateRange) => void
  onStatisticsRefresh: () => void
  onStatisticsExport: () => void
  onMetricsView: (metrics: PerformanceMetrics) => void
}

// Cost Analysis Component
interface CostAnalysisComponent {
  costs: CostAnalysis
  assetId: number
  
  onCostBreakdown: (breakdown: CostBreakdown) => void
  onCostTrend: (trend: CostTrend) => void
  onCostComparison: (comparison: CostComparison) => void
  onCostExport: () => void
}
```

---

### UI/UX Design

#### Asset History Layout
- **History Layout:**
  - Event timeline
  - Event list
  - Event details
  - Statistics panel

#### Event Timeline Design
- **Timeline Design:**
  - Chronological view
  - Event markers
  - Date navigation
  - Event grouping

#### Event Details Interface
- **Details Layout:**
  - Event information
  - Cost breakdown
  - Attachments
  - Action buttons

#### Statistics Dashboard
- **Dashboard Design:**
  - Cost charts
  - Event frequency
  - Performance metrics
  - Trend analysis

---

### Integration Requirements

#### Asset Management Integration
1. **Asset Data**
   - Asset information
   - Asset status
   - Asset location
   - Asset assignment

2. **User Management**
   - User permissions
   - User roles
   - User assignments
   - User notifications

#### Financial Integration
1. **Cost Tracking**
   - Cost categories
   - Cost allocation
   - Budget tracking
   - Financial reporting

2. **Invoice Management**
   - Invoice generation
   - Payment tracking
   - Supplier management
   - Expense approval

---

### Security Considerations

#### Data Protection
- Event permission validation
- Cost data protection
- File access control
- Audit logging

#### History Security
- Data integrity
- Change tracking
- Access control
- Backup protection

---

### Testing Strategy

#### Unit Tests
- Event creation validation
- Cost calculation
- Timeline generation
- Statistics calculation

#### Integration Tests
- Asset data integration
- User management integration
- Financial system integration
- Notification system testing

#### User Acceptance Tests
- Event workflow
- Cost tracking
- Timeline navigation
- Statistics reporting

---

### Deployment & Configuration

#### Environment Setup
- Database configuration
- File storage setup
- Notification system
- Reporting engine

#### Monitoring & Logging
- Event tracking
- Cost monitoring
- Performance metrics
- Error logging

---

### Documentation

#### User Manual
- Event management
- Cost tracking
- Timeline navigation
- Statistics interpretation

#### Technical Documentation
- API documentation
- Database schema
- Integration guides
- Performance optimization 