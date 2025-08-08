# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-1.2
### Liên kết khoản mục chi phí với Dự án, Gói thầu và Hợp đồng

#### Thông tin User Story
- **Story ID:** CP-1.2
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 1
- **Status:** To Do
- **Phụ thuộc:** CP-1.1, DMDA-1.1, GT-1.1, HD-1.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** có thể liên kết một khoản mục chi phí với một Dự án, một Gói thầu và/hoặc một Hợp đồng đã có trong hệ thống,  
**Để** tôi có thể phân bổ chi phí đúng đối tượng và tổng hợp báo cáo chi phí theo từng Dự án, Gói thầu hoặc Hợp đồng cụ thể.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có các trường cho phép chọn Dự án, Gói thầu và Hợp đồng từ danh sách các mục đã tồn tại trong các module tương ứng
- [ ] Có thể liên kết chi phí với một hoặc nhiều đối tượng (Dự án, Gói thầu, Hợp đồng)
- [ ] Hiển thị thông tin chi tiết của đối tượng được chọn (mã, tên, trạng thái)
- [ ] Có thể tìm kiếm và lọc đối tượng khi chọn
- [ ] Validation để đảm bảo đối tượng được chọn tồn tại và có trạng thái hợp lệ
- [ ] Có thể thay đổi liên kết sau khi đã tạo chi phí
- [ ] Hiển thị lịch sử thay đổi liên kết
- [ ] Có thể xem danh sách chi phí theo từng đối tượng
- [ ] Hỗ trợ liên kết nhiều chi phí cùng lúc với một đối tượng
- [ ] Có thể xuất báo cáo chi phí theo đối tượng

#### 2.4 Activity Diagram
![CP-1.2 Activity Diagram](diagrams/CP-1.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý liên kết khoản mục chi phí với Dự án, Gói thầu và Hợp đồng*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Liên kết Đối tượng**
   - Liên kết dự án
   - Liên kết gói thầu
   - Liên kết hợp đồng
   - Hỗ trợ nhiều đối tượng

2. **Chọn Đối tượng**
   - Chức năng tìm kiếm
   - Tùy chọn lọc
   - Quy tắc validation
   - Auto-complete

3. **Quản lý Liên kết**
   - Tạo liên kết
   - Chỉnh sửa liên kết
   - Xóa liên kết
   - Lịch sử liên kết

4. **Tích hợp Báo cáo**
   - Tổng hợp chi phí
   - Báo cáo theo đối tượng
   - Phân bổ chi phí
   - Theo dõi ngân sách

#### Quy tắc Kinh doanh
- Chi phí có thể liên kết với một hoặc nhiều đối tượng
- Đối tượng được chọn phải có trạng thái active
- Không thể liên kết với đối tượng đã bị xóa
- Chi phí định kỳ phải liên kết với ít nhất một đối tượng
- Tổng chi phí được phân bổ không được vượt quá 100%

#### Kịch bản Liên kết
1. **Liên kết Đơn Đối tượng**
   - Liên kết với một dự án
   - Liên kết với một gói thầu
   - Liên kết với một hợp đồng

2. **Liên kết Nhiều Đối tượng**
   - Liên kết với nhiều dự án
   - Liên kết với dự án và hợp đồng
   - Liên kết với cả ba đối tượng

3. **Phân bổ Chi phí**
   - Phân bổ đều
   - Phân bổ theo phần trăm
   - Phân bổ theo số tiền
   - Phân bổ tùy chỉnh

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng liên kết chi phí với dự án
CREATE TABLE cost_project_links (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    project_id INT NOT NULL,
    allocation_percentage DECIMAL(5,2) DEFAULT 100.00,
    allocation_amount DECIMAL(15,2),
    allocation_type ENUM('percentage', 'amount', 'equal') DEFAULT 'percentage',
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    linked_by INT NOT NULL,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (linked_by) REFERENCES users(id),
    UNIQUE KEY unique_cost_project (cost_item_id, project_id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_project_id (project_id)
);

-- Bảng liên kết chi phí với gói thầu
CREATE TABLE cost_tender_links (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    tender_package_id INT NOT NULL,
    allocation_percentage DECIMAL(5,2) DEFAULT 100.00,
    allocation_amount DECIMAL(15,2),
    allocation_type ENUM('percentage', 'amount', 'equal') DEFAULT 'percentage',
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    linked_by INT NOT NULL,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id) ON DELETE CASCADE,
    FOREIGN KEY (linked_by) REFERENCES users(id),
    UNIQUE KEY unique_cost_tender (cost_item_id, tender_package_id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_tender_package_id (tender_package_id)
);

-- Bảng liên kết chi phí với hợp đồng
CREATE TABLE cost_contract_links (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    contract_id INT NOT NULL,
    allocation_percentage DECIMAL(5,2) DEFAULT 100.00,
    allocation_amount DECIMAL(15,2),
    allocation_type ENUM('percentage', 'amount', 'equal') DEFAULT 'percentage',
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    linked_by INT NOT NULL,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (linked_by) REFERENCES users(id),
    UNIQUE KEY unique_cost_contract (cost_item_id, contract_id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_contract_id (contract_id)
);

-- Bảng lịch sử thay đổi liên kết
CREATE TABLE cost_link_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    entity_type ENUM('project', 'tender_package', 'contract') NOT NULL,
    entity_id INT NOT NULL,
    action_type ENUM('linked', 'unlinked', 'modified') NOT NULL,
    old_allocation_percentage DECIMAL(5,2),
    new_allocation_percentage DECIMAL(5,2),
    old_allocation_amount DECIMAL(15,2),
    new_allocation_amount DECIMAL(15,2),
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_entity_type (entity_type),
    INDEX idx_action_type (action_type)
);

-- Bảng cấu hình liên kết
CREATE TABLE cost_link_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng thống kê liên kết
CREATE TABLE cost_link_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    entity_type ENUM('project', 'tender_package', 'contract') NOT NULL,
    entity_id INT NOT NULL,
    total_cost_items INT DEFAULT 0,
    total_amount DECIMAL(15,2) DEFAULT 0,
    total_allocated_amount DECIMAL(15,2) DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_entity_type (entity_type),
    INDEX idx_entity_id (entity_id),
    UNIQUE KEY unique_entity_stat (entity_type, entity_id)
);

-- Insert default link configuration
INSERT INTO cost_link_config (config_key, config_value, description) VALUES
('allow_multiple_links', 'true', 'Allow linking to multiple entities'),
('require_at_least_one_link', 'true', 'Require at least one entity link'),
('max_allocation_percentage', '100.00', 'Maximum allocation percentage'),
('default_allocation_type', 'percentage', 'Default allocation type'),
('enable_link_validation', 'true', 'Enable link validation'),
('enable_auto_allocation', 'false', 'Enable automatic allocation'),
('link_history_retention_days', '365', 'Link history retention in days');
```

#### API Endpoints
```
# Cost Project Links
GET /api/cost-items/{id}/project-links
POST /api/cost-items/{id}/project-links
{
  "project_id": 123,
  "allocation_percentage": 50.00,
  "allocation_amount": 25000000,
  "allocation_type": "percentage"
}

PUT /api/cost-items/{id}/project-links/{link_id}
DELETE /api/cost-items/{id}/project-links/{link_id}

# Cost Tender Package Links
GET /api/cost-items/{id}/tender-links
POST /api/cost-items/{id}/tender-links
{
  "tender_package_id": 456,
  "allocation_percentage": 30.00,
  "allocation_amount": 15000000,
  "allocation_type": "percentage"
}

PUT /api/cost-items/{id}/tender-links/{link_id}
DELETE /api/cost-items/{id}/tender-links/{link_id}

# Cost Contract Links
GET /api/cost-items/{id}/contract-links
POST /api/cost-items/{id}/contract-links
{
  "contract_id": 789,
  "allocation_percentage": 20.00,
  "allocation_amount": 10000000,
  "allocation_type": "percentage"
}

PUT /api/cost-items/{id}/contract-links/{link_id}
DELETE /api/cost-items/{id}/contract-links/{link_id}

# Entity Search
GET /api/cost-items/link-entities
{
  "entity_type": "project",
  "search_query": "construction",
  "status": "active",
  "limit": 20
}

# Bulk Linking
POST /api/cost-items/bulk-link
{
  "cost_item_ids": [1, 2, 3],
  "entity_type": "project",
  "entity_id": 123,
  "allocation_percentage": 100.00,
  "allocation_type": "percentage"
}

# Link History
GET /api/cost-items/{id}/link-history
GET /api/cost-items/{id}/link-history/{entity_type}

# Link Statistics
GET /api/cost-items/link-statistics
{
  "entity_type": "project",
  "entity_id": 123,
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}

# Cost Allocation
POST /api/cost-items/{id}/allocate
{
  "allocations": [
    {
      "entity_type": "project",
      "entity_id": 123,
      "allocation_percentage": 50.00
    },
    {
      "entity_type": "contract",
      "entity_id": 456,
      "allocation_percentage": 50.00
    }
  ]
}

# Entity Cost Report
GET /api/cost-items/entity-report
{
  "entity_type": "project",
  "entity_id": 123,
  "report_type": "summary",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}

Response: {
  "entity_info": {
    "id": 123,
    "name": "Dự án Xây dựng",
    "code": "DA-2024-001"
  },
  "cost_summary": {
    "total_cost_items": 25,
    "total_amount": 500000000,
    "total_allocated": 500000000,
    "by_category": {
      "Nhân sự": 150000000,
      "Vật tư": 200000000,
      "Thiết bị": 100000000,
      "Dịch vụ": 50000000
    }
  },
  "cost_items": [
    {
      "id": 1,
      "cost_code": "CP-2024-001",
      "cost_name": "Chi phí nhân sự",
      "amount": 150000000,
      "allocation_percentage": 100.00
    }
  ]
}
```

#### Frontend Components
```typescript
// Entity Link Selection Component
interface EntityLinkSelectionComponent {
  costItemId: number
  entityType: 'project' | 'tender_package' | 'contract'
  selectedEntities: LinkedEntity[]
  availableEntities: Entity[]
  
  onEntitySelect: (entity: Entity) => void
  onEntityRemove: (entityId: number) => void
  onAllocationChange: (entityId: number, allocation: number) => void
  onSearchEntities: (query: string) => Promise<void>
}

// Entity Search Component
interface EntitySearchComponent {
  entityType: string
  searchQuery: string
  searchResults: Entity[]
  isLoading: boolean
  
  onSearch: (query: string) => Promise<void>
  onSelectEntity: (entity: Entity) => void
  onClearSearch: () => void
}

// Cost Allocation Component
interface CostAllocationComponent {
  costItem: CostItem
  linkedEntities: LinkedEntity[]
  totalAllocation: number
  
  onAddEntity: (entity: Entity) => void
  onRemoveEntity: (entityId: number) => void
  onUpdateAllocation: (entityId: number, allocation: number) => void
  onAutoAllocate: () => void
  onValidateAllocation: () => boolean
}

// Link History Component
interface LinkHistoryComponent {
  costItemId: number
  linkHistory: LinkHistoryEntry[]
  isLoading: boolean
  
  onViewDetails: (entryId: number) => void
  onFilterHistory: (filters: HistoryFilters) => void
  onExportHistory: () => void
}

// Entity Cost Report Component
interface EntityCostReportComponent {
  entityType: string
  entityId: number
  reportData: EntityCostReport
  isLoading: boolean
  
  onGenerateReport: (params: ReportParams) => Promise<void>
  onExportReport: (format: string) => Promise<void>
  onViewCostDetails: (costItemId: number) => void
}

// Bulk Link Component
interface BulkLinkComponent {
  selectedCostItems: CostItem[]
  targetEntity: Entity
  allocationType: 'percentage' | 'amount' | 'equal'
  
  onSelectTargetEntity: (entity: Entity) => void
  onSetAllocationType: (type: string) => void
  onSetAllocationValue: (value: number) => void
  onExecuteBulkLink: () => Promise<void>
}

// Link Validation Component
interface LinkValidationComponent {
  costItem: CostItem
  linkedEntities: LinkedEntity[]
  validationErrors: ValidationError[]
  
  onValidate: () => ValidationError[]
  onShowErrors: () => void
  onFixErrors: () => void
}

// Entity Link Summary Component
interface EntityLinkSummaryComponent {
  costItem: CostItem
  linkedEntities: LinkedEntity[]
  
  onViewEntityDetails: (entityId: number) => void
  onEditAllocation: (entityId: number) => void
  onRemoveLink: (entityId: number) => Promise<void>
}

// Link Statistics Component
interface LinkStatisticsComponent {
  entityType: string
  entityId: number
  statistics: LinkStatistics
  
  onViewCostBreakdown: () => void
  onViewTrendAnalysis: () => void
  onExportStatistics: () => void
}
```

---

### UI/UX Design

#### Entity Selection Interface
- **Selection Panel:**
  - Search input with auto-complete
  - Filter options (status, type, date)
  - Entity list with details
  - Selection checkboxes

#### Allocation Interface
- **Allocation Panel:**
  - Percentage/amount toggles
  - Allocation input fields
  - Total allocation display
  - Validation indicators

#### Link Management
- **Link Display:**
  - Linked entities list
  - Allocation percentages
  - Quick actions
  - Link history

#### Validation Feedback
- **Validation Display:**
  - Error messages
  - Warning indicators
  - Success confirmations
  - Progress indicators

---

### Integration Requirements

#### Module Integration
1. **Project Module**
   - Project data access
   - Project status validation
   - Project cost tracking
   - Budget integration

2. **Tender Package Module**
   - Tender package data access
   - Package status validation
   - Package cost tracking
   - Budget allocation

3. **Contract Module**
   - Contract data access
   - Contract status validation
   - Contract cost tracking
   - Payment integration

#### Data Synchronization
1. **Real-time Updates**
   - Link status changes
   - Cost amount updates
   - Allocation modifications
   - History tracking

2. **Validation Rules**
   - Entity existence checks
   - Status validation
   - Allocation validation
   - Business rule enforcement

---

### Security Considerations

#### Access Control
- Entity-based permissions
- Link modification rights
- Data visibility control
- Audit trail maintenance

#### Data Integrity
- Link validation
- Allocation verification
- History preservation
- Consistency checks

---

### Testing Strategy

#### Unit Tests
- Link creation logic
- Allocation calculations
- Validation rules
- Business logic

#### Integration Tests
- Module integration
- Data synchronization
- API endpoints
- Workflow testing

#### User Acceptance Tests
- Entity selection usability
- Allocation interface
- Link management
- Report functionality

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Module integration setup
- Validation rule configuration
- Report template setup

#### Monitoring & Logging
- Link creation tracking
- Allocation monitoring
- Performance tracking
- Error monitoring

---

### Documentation

#### User Manual
- Entity linking guide
- Allocation procedures
- Report generation
- Link management

#### Technical Documentation
- API documentation
- Integration architecture
- Validation rules
- Performance optimization

#### 5.5 Sequence Diagram
![CP-1.2 Sequence Diagram](diagrams/CP-1.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi liên kết khoản mục chi phí với Dự án, Gói thầu và Hợp đồng* 