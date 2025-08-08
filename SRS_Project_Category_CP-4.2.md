# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-4.2
### Xem và Truy cập Chi phí liên quan từ Tác vụ

#### Thông tin User Story
- **Story ID:** CP-4.2
- **Priority:** Medium
- **Story Points:** 4
- **Sprint:** Sprint 4
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-4.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** khi xem chi tiết một tác vụ, có thể thấy danh sách các chi phí đã được đính kèm vào tác vụ đó và truy cập trực tiếp đến trang chi tiết của từng chi phí  
**Để** tôi có thể nhanh chóng nắm bắt các công việc liên quan đến khoản chi phí này và chuyển đến tác vụ để cập nhật hoặc theo dõi.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Trên trang chi tiết khoản mục tác vụ, có một phần hiển thị danh sách các chi phí liên quan
- [ ] Danh sách chi phí hiển thị thông tin cơ bản: mã chi phí, tên chi phí, trạng thái, số tiền
- [ ] Có thể click vào từng chi phí để chuyển đến trang chi tiết chi phí
- [ ] Có thể lọc và tìm kiếm chi phí trong danh sách
- [ ] Hiển thị tổng số chi phí và tổng số tiền của các chi phí liên quan
- [ ] Có thể thêm chi phí mới vào tác vụ từ giao diện này
- [ ] Có thể xóa chi phí khỏi tác vụ (với quyền phù hợp)
- [ ] Hiển thị trạng thái thanh toán của từng chi phí
- [ ] Có thể sắp xếp danh sách chi phí theo nhiều tiêu chí
- [ ] Hệ thống ghi log khi thêm/xóa chi phí khỏi tác vụ
- [ ] Có thể xuất danh sách chi phí liên quan

---

### Functional Requirements

#### Core Features
1. **Related Costs Display**
   - List of related cost items
   - Cost item summary information
   - Direct navigation to cost details
   - Cost status indicators

2. **Cost Management**
   - Add costs to task
   - Remove costs from task
   - Cost filtering and search
   - Cost sorting options

3. **Cost Information**
   - Cost code and name
   - Cost amount and status
   - Payment status
   - Cost category

4. **Navigation & Access**
   - Direct link to cost details
   - Quick cost preview
   - Cost item actions
   - Context preservation

#### Business Rules
- Chỉ hiển thị chi phí mà người dùng có quyền xem
- Chi phí có thể được liên kết với nhiều tác vụ
- Việc thêm/xóa chi phí khỏi tác vụ phải được ghi log
- Trạng thái chi phí phải được cập nhật real-time
- Tổng số tiền phải được tính toán chính xác

#### Cost Information Display
1. **Basic Information**
   - Mã chi phí (Cost code)
   - Tên chi phí (Cost name)
   - Danh mục chi phí (Cost category)
   - Số tiền (Amount)

2. **Status Information**
   - Trạng thái chi phí (Cost status)
   - Trạng thái thanh toán (Payment status)
   - Trạng thái phê duyệt (Approval status)
   - Ngày tạo (Created date)

3. **Financial Information**
   - Tổng chi phí (Total amount)
   - Số tiền đã thanh toán (Paid amount)
   - Số tiền còn lại (Remaining amount)
   - Đơn vị tiền tệ (Currency)

4. **Related Information**
   - Dự án liên quan (Related project)
   - Hợp đồng liên quan (Related contract)
   - Nhà cung cấp (Supplier)
   - Người tạo (Created by)

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng liên kết tác vụ và chi phí (many-to-many relationship)
CREATE TABLE task_cost_relationships (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT NOT NULL,
    cost_item_id INT NOT NULL,
    relationship_type ENUM('primary', 'secondary', 'related') DEFAULT 'primary',
    added_by INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    
    FOREIGN KEY (task_id) REFERENCES cost_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (added_by) REFERENCES users(id),
    UNIQUE KEY unique_task_cost (task_id, cost_item_id),
    INDEX idx_task_id (task_id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_relationship_type (relationship_type)
);

-- Bảng lịch sử liên kết tác vụ-chi phí
CREATE TABLE task_cost_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT NOT NULL,
    cost_item_id INT NOT NULL,
    action_type ENUM('added', 'removed', 'updated') NOT NULL,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    
    FOREIGN KEY (task_id) REFERENCES cost_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_task_id (task_id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_action_type (action_type)
);

-- Bảng cấu hình hiển thị chi phí trong tác vụ
CREATE TABLE task_cost_display_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_role VARCHAR(50) NOT NULL,
    display_fields JSON NOT NULL,
    default_sort_field VARCHAR(100) DEFAULT 'cost_code',
    default_sort_order ENUM('asc', 'desc') DEFAULT 'asc',
    items_per_page INT DEFAULT 20,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_role (user_role),
    INDEX idx_is_active (is_active)
);

-- Insert default display configuration
INSERT INTO task_cost_display_config (user_role, display_fields, default_sort_field, items_per_page) VALUES
('cost_manager', '["cost_code", "cost_name", "total_amount", "payment_status", "approval_status"]', 'cost_code', 20),
('cost_staff', '["cost_code", "cost_name", "total_amount", "payment_status"]', 'cost_name', 15);
```

#### API Endpoints
```typescript
# Get Related Costs for Task
GET /api/tasks/{task_id}/related-costs
{
  "page": 1,
  "limit": 20,
  "sort_by": "cost_code",
  "sort_order": "asc",
  "status_filter": "active",
  "payment_status_filter": "pending"
}
Response: {
  "related_costs": [
    {
      "id": 123,
      "cost_code": "CP-2024-0001",
      "cost_name": "Chi phí thiết bị văn phòng",
      "cost_category": "Thiết bị",
      "total_amount": 50000000,
      "paid_amount": 30000000,
      "remaining_amount": 20000000,
      "currency": "VND",
      "cost_status": "active",
      "payment_status": "partial",
      "approval_status": "approved",
      "related_project": "Dự án A",
      "supplier": "Công ty ABC",
      "created_date": "2024-01-15",
      "relationship_type": "primary"
    }
  ],
  "pagination": {
    "total": 15,
    "page": 1,
    "limit": 20,
    "total_pages": 1
  },
  "summary": {
    "total_costs": 15,
    "total_amount": 750000000,
    "total_paid_amount": 450000000,
    "total_remaining_amount": 300000000,
    "costs_by_status": {
      "active": 12,
      "completed": 3
    },
    "costs_by_payment_status": {
      "paid": 5,
      "partial": 8,
      "pending": 2
    }
  }
}

# Add Cost to Task
POST /api/tasks/{task_id}/related-costs
{
  "cost_item_id": 124,
  "relationship_type": "primary",
  "notes": "Thêm chi phí thiết bị vào tác vụ thanh toán"
}
Response: {
  "success": true,
  "message": "Chi phí đã được thêm vào tác vụ thành công",
  "relationship_id": 456
}

# Remove Cost from Task
DELETE /api/tasks/{task_id}/related-costs/{cost_item_id}
{
  "reason": "Chi phí không còn liên quan đến tác vụ này"
}
Response: {
  "success": true,
  "message": "Chi phí đã được xóa khỏi tác vụ thành công"
}

# Update Cost Relationship
PUT /api/tasks/{task_id}/related-costs/{cost_item_id}
{
  "relationship_type": "secondary",
  "notes": "Cập nhật mối quan hệ chi phí-tác vụ"
}

# Search Costs for Task
GET /api/tasks/{task_id}/search-costs
{
  "query": "thiết bị",
  "category_filter": "equipment",
  "status_filter": "active",
  "amount_min": 10000000,
  "amount_max": 100000000
}
Response: {
  "available_costs": [
    {
      "id": 125,
      "cost_code": "CP-2024-0002",
      "cost_name": "Chi phí thiết bị máy tính",
      "cost_category": "Thiết bị",
      "total_amount": 25000000,
      "cost_status": "active",
      "payment_status": "pending"
    }
  ]
}

# Get Cost Summary for Task
GET /api/tasks/{task_id}/cost-summary
Response: {
  "total_costs": 15,
  "total_amount": 750000000,
  "total_paid_amount": 450000000,
  "total_remaining_amount": 300000000,
  "average_cost": 50000000,
  "costs_by_category": {
    "Thiết bị": 8,
    "Dịch vụ": 5,
    "Vật tư": 2
  },
  "costs_by_payment_status": {
    "paid": 5,
    "partial": 8,
    "pending": 2
  },
  "costs_by_approval_status": {
    "approved": 12,
    "pending": 2,
    "rejected": 1
  }
}

# Export Related Costs
GET /api/tasks/{task_id}/export-costs
{
  "format": "excel",
  "include_details": true,
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
Response: File download with cost data

# Get Cost History for Task
GET /api/tasks/{task_id}/cost-history
Response: [
  {
    "id": 1,
    "cost_item_id": 123,
    "action_type": "added",
    "performed_by": 456,
    "performed_at": "2024-01-25T10:30:00Z",
    "notes": "Thêm chi phí thiết bị vào tác vụ"
  },
  {
    "id": 2,
    "cost_item_id": 124,
    "action_type": "removed",
    "performed_by": 456,
    "performed_at": "2024-01-26T15:20:00Z",
    "notes": "Xóa chi phí không liên quan"
  }
]
```

#### Frontend Components
```typescript
// Related Costs List Component
interface RelatedCostsListComponent {
  taskId: number
  relatedCosts: CostItem[]
  filters: CostFilters
  
  onCostSelect: (cost: CostItem) => void
  onAddCost: () => void
  onRemoveCost: (cost: CostItem) => Promise<void>
  onFilterChange: (filters: CostFilters) => void
  onSortChange: (sortBy: string, sortOrder: string) => void
}

// Cost Item Card Component
interface CostItemCardComponent {
  cost: CostItem
  isSelectable: boolean
  isSelected: boolean
  
  onSelect: (cost: CostItem) => void
  onViewDetails: (cost: CostItem) => void
  onQuickActions: (cost: CostItem, action: string) => void
}

// Add Cost to Task Component
interface AddCostToTaskComponent {
  taskId: number
  availableCosts: CostItem[]
  isVisible: boolean
  
  onAddCost: (costId: number, relationshipType: string) => Promise<void>
  onSearchCosts: (query: string) => Promise<void>
  onCancel: () => void
}

// Cost Summary Component
interface CostSummaryComponent {
  taskId: number
  summary: CostSummary
  
  onRefreshSummary: () => Promise<void>
  onViewDetails: (category: string) => void
  onExportSummary: () => void
}

// Cost Search Component
interface CostSearchComponent {
  taskId: number
  searchQuery: string
  searchFilters: CostSearchFilters
  
  onSearch: (query: string) => void
  onFilterChange: (filters: CostSearchFilters) => void
  onClearSearch: () => void
}

// Cost Relationship Component
interface CostRelationshipComponent {
  taskId: number
  costId: number
  relationship: CostRelationship
  
  onUpdateRelationship: (updates: Partial<CostRelationship>) => Promise<void>
  onRemoveRelationship: () => Promise<void>
}

// Cost History Component
interface CostHistoryComponent {
  taskId: number
  costHistory: CostHistory[]
  
  onViewHistory: () => void
  onExportHistory: () => void
  onFilterHistory: (filters: HistoryFilters) => void
}

// Cost Quick Actions Component
interface CostQuickActionsComponent {
  cost: CostItem
  availableActions: string[]
  
  onActionClick: (action: string) => void
  onViewDetails: () => void
  onEditCost: () => void
  onViewPayments: () => void
}

// Cost Status Indicator Component
interface CostStatusIndicatorComponent {
  cost: CostItem
  
  getStatusColor: () => string
  getStatusIcon: () => string
  getStatusText: () => string
  getPaymentStatusColor: () => string
}

// Cost Export Component
interface CostExportComponent {
  taskId: number
  exportOptions: ExportOptions
  
  onExport: (format: string, options: ExportOptions) => Promise<void>
  onPreviewExport: () => void
}
```

---

### UI/UX Design

#### Related Costs Display
- **Cost List Layout:**
  - Card-based design
  - Status indicators
  - Quick action buttons
  - Summary information

#### Cost Management Interface
- **Add/Remove Costs:**
  - Search functionality
  - Bulk selection
  - Confirmation dialogs
  - Progress indicators

#### Cost Information Cards
- **Cost Card Design:**
  - Key information display
  - Status badges
  - Action buttons
  - Hover effects

#### Cost Summary Dashboard
- **Summary Display:**
  - Total amounts
  - Status breakdown
  - Category distribution
  - Payment progress

---

### Integration Requirements

#### Task Integration
1. **Cost Association**
   - Direct linking
   - Relationship management
   - Status synchronization
   - Context preservation

2. **Navigation Integration**
   - Seamless navigation
   - Context switching
   - State preservation
   - Breadcrumb support

#### Cost Item Integration
1. **Cost Information**
   - Real-time updates
   - Status synchronization
   - Amount calculations
   - Payment tracking

2. **Permission Management**
   - Access control
   - View permissions
   - Edit permissions
   - Export permissions

---

### Security Considerations

#### Data Protection
- Cost access validation
- Relationship authorization
- Export permission checks
- Audit logging

#### Access Control
- Role-based cost access
- Task-cost relationship permissions
- Navigation security
- Data privacy

---

### Testing Strategy

#### Unit Tests
- Cost relationship logic
- Permission validation
- Navigation functionality
- Export capabilities

#### Integration Tests
- Database operations
- API endpoint testing
- Navigation flow
- Export functionality

#### User Acceptance Tests
- Cost viewing workflow
- Navigation accuracy
- Export functionality
- Permission validation

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Permission configuration
- Export setup
- Navigation configuration

#### Monitoring & Logging
- Cost access tracking
- Navigation monitoring
- Export logging
- Performance tracking

---

### Documentation

#### User Manual
- Cost viewing procedures
- Navigation guidelines
- Export functionality
- Permission management

#### Technical Documentation
- API documentation
- Database schema
- Navigation implementation
- Integration guides 