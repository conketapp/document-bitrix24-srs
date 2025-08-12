# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-2.1
### Tìm kiếm & Lọc danh sách Tài sản/Dịch vụ đa tiêu chí

#### Thông tin User Story
- **Story ID:** TSDV-2.1
- **Priority:** High
- **Story Points:** 6
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** TSDV-1.1, TSDV-1.2

#### Mô tả User Story
**Với vai trò là** Người dùng hệ thống,  
**Tôi muốn** có thể tìm kiếm và lọc danh sách các tài sản/dịch vụ dựa trên các thuộc tính của chúng  
**Để** tôi có thể nhanh chóng truy xuất thông tin cần thiết và quản lý tập trung.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Giao diện có các trường tìm kiếm và bộ lọc dễ sử dụng, hỗ trợ nhiều tiêu chí cùng lúc
- [ ] Hỗ trợ tìm kiếm theo từ khóa và lọc theo danh sách chọn/khoảng giá trị
- [ ] Có thể tìm kiếm theo mã, tên, mô tả, danh mục của tài sản/dịch vụ
- [ ] Có thể lọc theo loại (tài sản/dịch vụ), trạng thái, người phụ trách
- [ ] Có thể lọc theo dự án nguồn, ngày tạo, ngày cập nhật
- [ ] Có thể lọc theo giá trị, vị trí, nhà cung cấp (cho tài sản)
- [ ] Có thể lọc theo nhà cung cấp dịch vụ, thời gian dịch vụ (cho dịch vụ)
- [ ] Có thể lưu và tái sử dụng các bộ lọc thường dùng
- [ ] Có thể xuất kết quả tìm kiếm ra Excel/PDF
- [ ] Có thể sắp xếp kết quả theo nhiều tiêu chí
- [ ] Có thể xem kết quả dạng danh sách hoặc dạng lưới
- [ ] Có thể tìm kiếm nâng cao với các toán tử logic (AND, OR, NOT)

#### 2.4 Activity Diagram
![TSDV-2.1 Activity Diagram](diagrams/TSDV-2.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tìm kiếm và lọc Tài sản/Dịch vụ*

#### 2.5 Sequence Diagram
![TSDV-2.1 Sequence Diagram](diagrams/TSDV-2.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tìm kiếm và lọc Tài sản/Dịch vụ*

---

### Functional Requirements

#### Core Features
1. **Search Functionality**
   - Keyword search
   - Advanced search
   - Fuzzy search
   - Search suggestions

2. **Filter System**
   - Multi-criteria filtering
   - Range filters
   - Date filters
   - Status filters

3. **Result Management**
   - Sorting options
   - Pagination
   - Export capabilities
   - Saved searches

4. **User Interface**
   - Search bar
   - Filter panel
   - Result display
   - Quick actions

#### Business Rules
- Tìm kiếm phải hỗ trợ từ khóa tiếng Việt và tiếng Anh
- Kết quả tìm kiếm phải được sắp xếp theo độ liên quan
- Bộ lọc phải hỗ trợ nhiều tiêu chí cùng lúc
- Chỉ hiển thị dữ liệu mà người dùng có quyền xem
- Có thể lưu và chia sẻ bộ lọc thường dùng

#### Search Criteria
1. **Basic Search**
   - Asset/Service code
   - Name
   - Description
   - Category
   - Subcategory

2. **Asset-specific Search**
   - Model
   - Serial number
   - Manufacturer
   - Supplier
   - Location
   - Purchase cost range
   - Current value range

3. **Service-specific Search**
   - Service provider
   - Service contact
   - Service level agreement
   - Service cost range
   - Start date
   - End date

4. **Common Search**
   - Status
   - Priority
   - Responsible person
   - Source project
   - Creation date
   - Last modified date

#### Filter Types
1. **Text Filters**
   - Exact match
   - Contains
   - Starts with
   - Ends with

2. **Numeric Filters**
   - Equal to
   - Greater than
   - Less than
   - Between range

3. **Date Filters**
   - Exact date
   - Date range
   - Last N days
   - This week/month/year

4. **List Filters**
   - Single selection
   - Multiple selection
   - Exclude selection
   - All except

#### Advanced Search
1. **Logical Operators**
   - AND (tất cả điều kiện)
   - OR (ít nhất một điều kiện)
   - NOT (loại trừ điều kiện)
   - Parentheses grouping

2. **Search Fields**
   - Full text search
   - Field-specific search
   - Combined search
   - Wildcard search

3. **Search Options**
   - Case sensitive/insensitive
   - Exact phrase
   - Partial match
   - Fuzzy match

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng bộ lọc đã lưu
CREATE TABLE asset_service_saved_filters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filter_name VARCHAR(200) NOT NULL,
    filter_description TEXT,
    filter_criteria JSON NOT NULL,
    filter_type ENUM('search', 'filter', 'combined') NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    is_default BOOLEAN DEFAULT FALSE,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_created_by (created_by),
    INDEX idx_is_public (is_public),
    INDEX idx_is_default (is_default)
);

-- Bảng lịch sử tìm kiếm
CREATE TABLE asset_service_search_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    search_query TEXT NOT NULL,
    search_criteria JSON,
    result_count INT DEFAULT 0,
    search_duration_ms INT,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_search_timestamp (search_timestamp)
);

-- Bảng thống kê tìm kiếm
CREATE TABLE asset_service_search_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    search_date DATE NOT NULL,
    total_searches INT DEFAULT 0,
    unique_users INT DEFAULT 0,
    average_result_count DECIMAL(10,2) DEFAULT 0,
    average_search_duration_ms INT DEFAULT 0,
    most_popular_queries JSON,
    search_by_type JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_search_date (search_date),
    INDEX idx_search_date (search_date)
);

-- Bảng cấu hình tìm kiếm
CREATE TABLE asset_service_search_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_name VARCHAR(100) NOT NULL,
    config_type ENUM('search_fields', 'filter_options', 'sort_options', 'display_options') NOT NULL,
    config_data JSON NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_config_name (config_name),
    INDEX idx_config_type (config_type),
    INDEX idx_is_active (is_active),
    INDEX idx_sort_order (sort_order)
);

-- Bảng chỉ mục tìm kiếm
CREATE TABLE asset_service_search_index (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    search_text TEXT NOT NULL,
    search_metadata JSON,
    last_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    FULLTEXT INDEX idx_search_text (search_text),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_last_indexed (last_indexed)
);

-- Insert default search configurations
INSERT INTO asset_service_search_config (config_name, config_type, config_data, sort_order) VALUES
('search_fields', 'search_fields', '["code", "name", "description", "category", "model", "serial_number", "manufacturer", "location", "service_provider"]', 1),
('filter_options', 'filter_options', '{"status": ["active", "inactive", "maintenance", "retired"], "type": ["asset", "service"], "priority": ["low", "medium", "high", "critical"]}', 2),
('sort_options', 'sort_options', '["name", "code", "created_at", "updated_at", "status", "priority", "responsible_person"]', 3),
('display_options', 'display_options', '{"view_mode": ["list", "grid"], "page_size": [10, 25, 50, 100], "show_details": true}', 4);
```

#### API Endpoints
```typescript
# Search Assets/Services
POST /api/assets-services/search
{
  "query": "máy chủ dell",
  "filters": {
    "type": ["asset"],
    "status": ["active", "maintenance"],
    "category": ["Hardware"],
    "cost_range": {
      "min": 10000000,
      "max": 50000000
    },
    "created_date": {
      "from": "2024-01-01",
      "to": "2024-12-31"
    }
  },
  "sort_by": "name",
  "sort_order": "asc",
  "page": 1,
  "page_size": 25,
  "include_details": true
}
Response: {
  "results": [
    {
      "id": 123,
      "asset_service_code": "TS2024000001",
      "name": "Máy chủ Dell PowerEdge R740",
      "type": "asset",
      "category": "Hardware",
      "subcategory": "Server",
      "status": "active",
      "priority": "high",
      "responsible_person": "Nguyễn Văn A",
      "location": "Data Center A",
      "purchase_cost": 45000000,
      "current_value": 40000000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 125,
    "page_size": 25
  },
  "search_metadata": {
    "query_time_ms": 150,
    "result_count": 25,
    "filters_applied": 5,
    "suggestions": ["dell server", "poweredge", "r740"]
  }
}

# Get Search Suggestions
GET /api/assets-services/search/suggestions
{
  "query": "máy chủ",
  "limit": 10
}
Response: {
  "suggestions": [
    {
      "text": "Máy chủ Dell PowerEdge R740",
      "type": "asset",
      "category": "Hardware",
      "relevance_score": 0.95
    },
    {
      "text": "Máy chủ HP ProLiant DL380",
      "type": "asset",
      "category": "Hardware",
      "relevance_score": 0.85
    },
    {
      "text": "Dịch vụ bảo trì máy chủ",
      "type": "service",
      "category": "Maintenance",
      "relevance_score": 0.75
    }
  ]
}

# Get Filter Options
GET /api/assets-services/filters/options
{
  "filter_type": "category"
}
Response: {
  "filter_options": {
    "categories": [
      {"value": "Hardware", "label": "Phần cứng", "count": 150},
      {"value": "Software", "label": "Phần mềm", "count": 80},
      {"value": "Infrastructure", "label": "Hạ tầng", "count": 45}
    ],
    "statuses": [
      {"value": "active", "label": "Đang hoạt động", "count": 200},
      {"value": "inactive", "label": "Không hoạt động", "count": 30},
      {"value": "maintenance", "label": "Bảo trì", "count": 15}
    ],
    "types": [
      {"value": "asset", "label": "Tài sản", "count": 180},
      {"value": "service", "label": "Dịch vụ", "count": 95}
    ]
  }
}

# Save Search Filter
POST /api/assets-services/filters/save
{
  "filter_name": "Tài sản phần cứng đang hoạt động",
  "filter_description": "Lọc các tài sản phần cứng đang hoạt động",
  "filter_criteria": {
    "type": ["asset"],
    "category": ["Hardware"],
    "status": ["active"]
  },
  "is_public": false
}
Response: {
  "success": true,
  "filter_id": 123,
  "message": "Bộ lọc đã được lưu thành công"
}

# Get Saved Filters
GET /api/assets-services/filters/saved
{
  "include_public": true
}
Response: {
  "saved_filters": [
    {
      "id": 123,
      "filter_name": "Tài sản phần cứng đang hoạt động",
      "filter_description": "Lọc các tài sản phần cứng đang hoạt động",
      "filter_criteria": {
        "type": ["asset"],
        "category": ["Hardware"],
        "status": ["active"]
      },
      "is_public": false,
      "created_by": "Nguyễn Văn A",
      "created_at": "2024-01-25T10:30:00Z"
    }
  ]
}

# Advanced Search
POST /api/assets-services/search/advanced
{
  "search_conditions": [
    {
      "field": "name",
      "operator": "contains",
      "value": "máy chủ"
    },
    {
      "field": "category",
      "operator": "equals",
      "value": "Hardware"
    },
    {
      "field": "purchase_cost",
      "operator": "between",
      "value": [10000000, 50000000]
    }
  ],
  "logical_operator": "AND",
  "sort_by": "created_at",
  "sort_order": "desc"
}
Response: {
  "results": [
    {
      "id": 123,
      "asset_service_code": "TS2024000001",
      "name": "Máy chủ Dell PowerEdge R740",
      "type": "asset",
      "category": "Hardware",
      "purchase_cost": 45000000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "search_metadata": {
    "conditions_applied": 3,
    "logical_operator": "AND",
    "result_count": 15
  }
}

# Export Search Results
POST /api/assets-services/search/export
{
  "search_criteria": {
    "query": "máy chủ dell",
    "filters": {
      "type": ["asset"],
      "status": ["active"]
    }
  },
  "export_format": "excel",
  "include_details": true
}
Response: File download with search results

# Get Search Statistics
GET /api/assets-services/search/statistics
{
  "date_from": "2024-01-01",
  "date_to": "2024-12-31"
}
Response: {
  "statistics": {
    "total_searches": 1250,
    "unique_users": 45,
    "average_result_count": 23.5,
    "average_search_duration_ms": 180,
    "most_popular_queries": [
      {"query": "máy chủ", "count": 150},
      {"query": "dell", "count": 120},
      {"query": "server", "count": 100}
    ],
    "search_by_type": {
      "asset": 800,
      "service": 450
    }
  }
}
```

#### Frontend Components
```typescript
// Search Interface Component
interface SearchInterfaceComponent {
  searchQuery: string
  searchFilters: SearchFilters
  searchResults: SearchResult[]
  
  onSearch: (query: string, filters: SearchFilters) => Promise<void>
  onFilterChange: (filters: SearchFilters) => void
  onSortChange: (sortBy: string, sortOrder: string) => void
  onExportResults: () => void
}

// Search Bar Component
interface SearchBarComponent {
  query: string
  suggestions: SearchSuggestion[]
  
  onQueryChange: (query: string) => void
  onSuggestionSelect: (suggestion: SearchSuggestion) => void
  onSearchSubmit: (query: string) => void
  onClearSearch: () => void
}

// Filter Panel Component
interface FilterPanelComponent {
  filters: FilterOption[]
  appliedFilters: AppliedFilter[]
  
  onFilterApply: (filter: AppliedFilter) => void
  onFilterRemove: (filterId: string) => void
  onFilterClear: () => void
  onFilterSave: (filterName: string) => void
}

// Search Results Component
interface SearchResultsComponent {
  results: SearchResult[]
  pagination: PaginationInfo
  
  onResultSelect: (result: SearchResult) => void
  onPageChange: (page: number) => void
  onPageSizeChange: (pageSize: number) => void
  onViewModeChange: (viewMode: string) => void
}

// Advanced Search Component
interface AdvancedSearchComponent {
  searchConditions: SearchCondition[]
  logicalOperator: string
  
  onConditionAdd: (condition: SearchCondition) => void
  onConditionRemove: (conditionId: string) => void
  onConditionUpdate: (conditionId: string, condition: SearchCondition) => void
  onOperatorChange: (operator: string) => void
  onAdvancedSearch: () => Promise<void>
}

// Saved Filters Component
interface SavedFiltersComponent {
  savedFilters: SavedFilter[]
  
  onFilterSelect: (filter: SavedFilter) => void
  onFilterEdit: (filter: SavedFilter) => void
  onFilterDelete: (filterId: number) => void
  onFilterShare: (filter: SavedFilter) => void
}

// Search Statistics Component
interface SearchStatisticsComponent {
  statistics: SearchStatistics
  
  onDateRangeChange: (range: DateRange) => void
  onStatisticsExport: () => void
  onStatisticsRefresh: () => void
}

// Search Suggestions Component
interface SearchSuggestionsComponent {
  suggestions: SearchSuggestion[]
  isVisible: boolean
  
  onSuggestionClick: (suggestion: SearchSuggestion) => void
  onSuggestionHover: (suggestion: SearchSuggestion) => void
  onSuggestionsClose: () => void
}

// Filter Options Component
interface FilterOptionsComponent {
  filterType: string
  options: FilterOption[]
  
  onOptionSelect: (option: FilterOption) => void
  onOptionDeselect: (option: FilterOption) => void
  onOptionsClear: () => void
  onOptionsApply: () => void
}

// Search History Component
interface SearchHistoryComponent {
  searchHistory: SearchHistory[]
  
  onHistorySelect: (history: SearchHistory) => void
  onHistoryClear: () => void
  onHistoryExport: () => void
}
```

---

### UI/UX Design

#### Search Interface Layout
- **Search Layout:**
  - Search bar with suggestions
  - Filter panel
  - Results display
  - Pagination controls

#### Filter Panel Design
- **Filter Design:**
  - Collapsible filter sections
  - Multi-select options
  - Range sliders
  - Date pickers

#### Results Display Interface
- **Results Layout:**
  - List/grid view toggle
  - Sort options
  - Export buttons
  - Quick actions

#### Advanced Search Interface
- **Advanced Design:**
  - Condition builder
  - Logical operators
  - Field selection
  - Operator selection

---

### Integration Requirements

#### Search Engine Integration
1. **Full-text Search**
   - Elasticsearch or similar
   - Fuzzy matching
   - Relevance scoring
   - Search suggestions

2. **Filter System**
   - Dynamic filtering
   - Range queries
   - Date filtering
   - Aggregation queries

#### Data Management Integration
1. **Index Management**
   - Search index updates
   - Data synchronization
   - Index optimization
   - Performance monitoring

2. **Export System**
   - Excel export
   - PDF export
   - CSV export
   - Custom formats

---

### Security Considerations

#### Data Protection
- Search permission validation
- Data filtering by user rights
- Export restrictions
- Audit logging

#### Search Security
- Query validation
- SQL injection prevention
- Rate limiting
- Access control

---

### Testing Strategy

#### Unit Tests
- Search logic validation
- Filter functionality
- Sort operations
- Export functionality

#### Integration Tests
- Search engine integration
- Database queries
- Export system
- Performance testing

#### User Acceptance Tests
- Search workflow
- Filter operations
- Export functionality
- Performance validation

---

### Deployment & Configuration

#### Environment Setup
- Search engine setup
- Index configuration
- Filter system setup
- Export configuration

#### Monitoring & Logging
- Search performance monitoring
- Query analytics
- Error logging
- Usage tracking

---

### Documentation

#### User Manual
- Search procedures
- Filter usage
- Export procedures
- Advanced search

#### Technical Documentation
- API documentation
- Search configuration
- Integration guides
- Performance optimization 