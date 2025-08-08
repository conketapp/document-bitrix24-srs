# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-5.2
### Tìm kiếm & Lọc Chi phí Đa tiêu chí

#### Thông tin User Story
- **Story ID:** CP-5.2
- **Priority:** High
- **Story Points:** 6
- **Sprint:** Sprint 5
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** có thể tìm kiếm và lọc các khoản mục chi phí dựa trên nhiều tiêu chí  
**Để** tôi có thể nhanh chóng truy xuất thông tin cần thiết và tổng hợp dữ liệu chi phí.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Giao diện có các trường tìm kiếm và bộ lọc dễ sử dụng
- [ ] Hỗ trợ tìm kiếm theo từ khóa và lọc theo danh sách chọn/khoảng giá trị
- [ ] Có thể tìm kiếm theo mã chi phí, tên chi phí, mô tả
- [ ] Có thể lọc theo danh mục chi phí, loại chi phí, trạng thái
- [ ] Có thể lọc theo khoảng thời gian (ngày tạo, ngày cập nhật)
- [ ] Có thể lọc theo khoảng số tiền (tổng chi phí, số tiền đã thanh toán)
- [ ] Có thể lọc theo dự án, hợp đồng, nhà cung cấp
- [ ] Có thể lọc theo người tạo, người phê duyệt
- [ ] Có thể lọc theo trạng thái thanh toán và phê duyệt
- [ ] Có thể kết hợp nhiều tiêu chí tìm kiếm và lọc
- [ ] Có thể lưu và tái sử dụng các bộ lọc thường dùng
- [ ] Hiển thị số lượng kết quả tìm kiếm
- [ ] Có thể xuất kết quả tìm kiếm

---

### Functional Requirements

#### Core Features
1. **Keyword Search**
   - Search by cost code
   - Search by cost name
   - Search by description
   - Full-text search capabilities

2. **Filter Options**
   - Category and type filters
   - Status and approval filters
   - Date range filters
   - Amount range filters
   - Relationship filters

3. **Advanced Search**
   - Multiple criteria combination
   - Saved search filters
   - Search history
   - Export search results

4. **Search Results**
   - Paginated results
   - Sortable columns
   - Result count display
   - Quick actions

#### Business Rules
- Tìm kiếm phải hỗ trợ từ khóa một phần (partial matching)
- Bộ lọc phải hỗ trợ nhiều giá trị cùng lúc
- Kết quả tìm kiếm phải được sắp xếp theo mức độ liên quan
- Chỉ hiển thị chi phí mà người dùng có quyền xem
- Tìm kiếm phải có hiệu suất tốt với dữ liệu lớn

#### Search Criteria
1. **Basic Information**
   - Mã chi phí (Cost code)
   - Tên chi phí (Cost name)
   - Mô tả chi phí (Cost description)
   - Danh mục chi phí (Cost category)

2. **Financial Information**
   - Tổng chi phí (Total amount)
   - Số tiền đã thanh toán (Paid amount)
   - Số tiền còn lại (Remaining amount)
   - Đơn vị tiền tệ (Currency)

3. **Status Information**
   - Trạng thái chi phí (Cost status)
   - Trạng thái thanh toán (Payment status)
   - Trạng thái phê duyệt (Approval status)
   - Trạng thái thực hiện (Implementation status)

4. **Timeline Information**
   - Ngày tạo (Created date)
   - Ngày cập nhật (Updated date)
   - Ngày bắt đầu (Start date)
   - Ngày kết thúc (End date)

5. **Relationship Information**
   - Dự án liên quan (Related project)
   - Hợp đồng liên quan (Related contract)
   - Gói thầu liên quan (Related tender package)
   - Nhà cung cấp (Supplier)

6. **User Information**
   - Người tạo (Created by)
   - Người cập nhật (Updated by)
   - Người phê duyệt (Approved by)
   - Người thực hiện (Assigned to)

#### Filter Types
1. **Dropdown Filters**
   - Single selection
   - Multiple selection
   - Search within dropdown
   - Clear selection option

2. **Range Filters**
   - Date range picker
   - Amount range slider
   - Number range input
   - Custom range input

3. **Text Filters**
   - Exact match
   - Partial match
   - Case insensitive
   - Regular expressions

4. **Boolean Filters**
   - Yes/No options
   - Checkbox selection
   - Radio button selection
   - Toggle switches

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lưu trữ bộ lọc đã lưu
CREATE TABLE saved_search_filters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    filter_name VARCHAR(200) NOT NULL,
    filter_description TEXT,
    filter_criteria JSON NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_is_public (is_public),
    INDEX idx_is_default (is_default)
);

-- Bảng lịch sử tìm kiếm
CREATE TABLE search_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    search_query TEXT,
    filter_criteria JSON,
    result_count INT DEFAULT 0,
    search_duration_ms INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- Bảng thống kê tìm kiếm
CREATE TABLE search_statistics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    search_term VARCHAR(500),
    search_count INT DEFAULT 1,
    average_result_count DECIMAL(10,2) DEFAULT 0,
    last_searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_search_term (search_term),
    INDEX idx_search_count (search_count),
    INDEX idx_last_searched (last_searched_at)
);

-- Bảng cấu hình tìm kiếm
CREATE TABLE search_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    search_field VARCHAR(100) NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    search_weight DECIMAL(3,2) DEFAULT 1.00,
    search_type ENUM('exact', 'partial', 'fuzzy', 'fulltext') DEFAULT 'partial',
    is_required BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_search_field (search_field),
    INDEX idx_is_enabled (is_enabled),
    INDEX idx_sort_order (sort_order)
);

-- Bảng cấu hình bộ lọc
CREATE TABLE filter_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filter_name VARCHAR(100) NOT NULL,
    filter_type ENUM('dropdown', 'range', 'text', 'boolean') NOT NULL,
    filter_options JSON,
    is_enabled BOOLEAN DEFAULT TRUE,
    is_required BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_filter_name (filter_name),
    INDEX idx_is_enabled (is_enabled),
    INDEX idx_sort_order (sort_order)
);

-- Insert default search configuration
INSERT INTO search_config (search_field, is_enabled, search_weight, search_type, sort_order) VALUES
('cost_code', TRUE, 1.00, 'exact', 1),
('cost_name', TRUE, 0.90, 'partial', 2),
('cost_description', TRUE, 0.70, 'partial', 3),
('supplier_name', TRUE, 0.60, 'partial', 4),
('project_name', TRUE, 0.50, 'partial', 5);

-- Insert default filter configuration
INSERT INTO filter_config (filter_name, filter_type, filter_options, sort_order) VALUES
('cost_category', 'dropdown', '{"source": "cost_categories", "multiple": true}', 1),
('cost_status', 'dropdown', '{"options": ["active", "completed", "cancelled"], "multiple": true}', 2),
('payment_status', 'dropdown', '{"options": ["pending", "partial", "paid", "overdue"], "multiple": true}', 3),
('approval_status', 'dropdown', '{"options": ["draft", "pending", "approved", "rejected"], "multiple": true}', 4),
('total_amount', 'range', '{"min": 0, "max": 1000000000, "step": 1000000}', 5),
('created_date', 'range', '{"type": "date", "format": "YYYY-MM-DD"}', 6),
('supplier', 'dropdown', '{"source": "suppliers", "multiple": true}', 7),
('project', 'dropdown', '{"source": "projects", "multiple": true}', 8);
```

#### API Endpoints
```typescript
# Search Cost Items
POST /api/cost-items/search
{
  "query": "thiết bị văn phòng",
  "filters": {
    "cost_category": ["Thiết bị", "Văn phòng"],
    "cost_status": ["active"],
    "payment_status": ["pending", "partial"],
    "total_amount": {
      "min": 10000000,
      "max": 100000000
    },
    "created_date": {
      "from": "2024-01-01",
      "to": "2024-01-31"
    },
    "supplier": ["Công ty ABC"],
    "project": ["Dự án A"]
  },
  "sort_by": "created_date",
  "sort_order": "desc",
  "page": 1,
  "limit": 20
}
Response: {
  "results": [
    {
      "id": 123,
      "cost_code": "CP-2024-0001",
      "cost_name": "Chi phí thiết bị văn phòng",
      "cost_category": "Thiết bị",
      "total_amount": 50000000,
      "paid_amount": 30000000,
      "payment_status": "partial",
      "approval_status": "approved",
      "supplier": "Công ty ABC",
      "project": "Dự án A",
      "created_date": "2024-01-15",
      "created_by": "Nguyễn Văn A",
      "relevance_score": 0.95
    }
  ],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "total_pages": 8
  },
  "search_metadata": {
    "query_time_ms": 245,
    "total_results": 150,
    "search_query": "thiết bị văn phòng",
    "applied_filters": {
      "cost_category": ["Thiết bị", "Văn phòng"],
      "payment_status": ["pending", "partial"]
    }
  }
}

# Get Search Suggestions
GET /api/cost-items/search-suggestions
{
  "query": "thiết bị",
  "limit": 10
}
Response: {
  "suggestions": [
    {
      "type": "cost_name",
      "value": "Chi phí thiết bị văn phòng",
      "count": 15
    },
    {
      "type": "cost_code",
      "value": "CP-2024-0001",
      "count": 1
    },
    {
      "type": "supplier",
      "value": "Công ty thiết bị ABC",
      "count": 8
    }
  ]
}

# Save Search Filter
POST /api/cost-items/save-search-filter
{
  "filter_name": "Chi phí thiết bị chưa thanh toán",
  "filter_description": "Tìm kiếm các chi phí thiết bị chưa thanh toán đầy đủ",
  "filter_criteria": {
    "query": "thiết bị",
    "filters": {
      "cost_category": ["Thiết bị"],
      "payment_status": ["pending", "partial"]
    }
  },
  "is_public": false
}
Response: {
  "success": true,
  "filter_id": 123,
  "message": "Bộ lọc đã được lưu thành công"
}

# Get Saved Search Filters
GET /api/cost-items/saved-filters
{
  "include_public": true,
  "user_id": 456
}
Response: {
  "saved_filters": [
    {
      "id": 123,
      "filter_name": "Chi phí thiết bị chưa thanh toán",
      "filter_description": "Tìm kiếm các chi phí thiết bị chưa thanh toán đầy đủ",
      "filter_criteria": {
        "query": "thiết bị",
        "filters": {
          "cost_category": ["Thiết bị"],
          "payment_status": ["pending", "partial"]
        }
      },
      "is_public": false,
      "created_at": "2024-01-25T10:30:00Z"
    }
  ]
}

# Get Search Statistics
GET /api/cost-items/search-statistics
{
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
Response: {
  "total_searches": 1250,
  "unique_searches": 450,
  "average_results_per_search": 15.5,
  "most_searched_terms": [
    {
      "term": "thiết bị",
      "count": 85,
      "average_results": 12.3
    },
    {
      "term": "văn phòng",
      "count": 65,
      "average_results": 8.7
    }
  ],
  "search_by_category": {
    "Thiết bị": 300,
    "Dịch vụ": 250,
    "Vật tư": 200
  },
  "search_by_status": {
    "active": 400,
    "pending": 350,
    "completed": 200
  }
}

# Export Search Results
POST /api/cost-items/export-search-results
{
  "search_criteria": {
    "query": "thiết bị văn phòng",
    "filters": {
      "cost_category": ["Thiết bị"],
      "payment_status": ["pending", "partial"]
    }
  },
  "export_format": "excel",
  "include_details": true
}
Response: File download with search results

# Get Search History
GET /api/cost-items/search-history
{
  "page": 1,
  "limit": 20,
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
Response: {
  "search_history": [
    {
      "id": 1,
      "search_query": "thiết bị văn phòng",
      "filter_criteria": {
        "cost_category": ["Thiết bị"],
        "payment_status": ["pending"]
      },
      "result_count": 15,
      "search_duration_ms": 245,
      "created_at": "2024-01-25T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "total_pages": 8
  }
}
```

#### Frontend Components
```typescript
// Search Interface Component
interface SearchInterfaceComponent {
  searchQuery: string
  filters: SearchFilters
  searchResults: CostItem[]
  
  onSearch: (query: string, filters: SearchFilters) => Promise<void>
  onFilterChange: (filters: SearchFilters) => void
  onClearSearch: () => void
  onExportResults: () => void
}

// Search Input Component
interface SearchInputComponent {
  query: string
  placeholder: string
  suggestions: SearchSuggestion[]
  
  onQueryChange: (query: string) => void
  onSearch: (query: string) => void
  onSuggestionSelect: (suggestion: SearchSuggestion) => void
  onClearQuery: () => void
}

// Filter Panel Component
interface FilterPanelComponent {
  filters: SearchFilters
  availableFilters: FilterConfig[]
  
  onFilterChange: (filterName: string, value: any) => void
  onClearFilters: () => void
  onApplyFilters: () => void
  onSaveFilter: (filterName: string) => void
}

// Filter Component
interface FilterComponent {
  filterConfig: FilterConfig
  value: any
  isVisible: boolean
  
  onValueChange: (value: any) => void
  onClear: () => void
  onApply: () => void
}

// Search Results Component
interface SearchResultsComponent {
  results: CostItem[]
  pagination: Pagination
  sortOptions: SortOption[]
  
  onResultSelect: (result: CostItem) => void
  onSortChange: (sortBy: string, sortOrder: string) => void
  onPageChange: (page: number) => void
  onExportResults: () => void
}

// Saved Filters Component
interface SavedFiltersComponent {
  savedFilters: SavedFilter[]
  
  onFilterSelect: (filter: SavedFilter) => void
  onFilterDelete: (filterId: number) => void
  onFilterEdit: (filter: SavedFilter) => void
  onFilterShare: (filter: SavedFilter) => void
}

// Search Statistics Component
interface SearchStatisticsComponent {
  statistics: SearchStatistics
  
  onRefreshStatistics: () => Promise<void>
  onViewDetails: (category: string) => void
  onExportStatistics: () => void
}

// Search History Component
interface SearchHistoryComponent {
  searchHistory: SearchHistory[]
  
  onHistorySelect: (history: SearchHistory) => void
  onHistoryDelete: (historyId: number) => void
  onClearHistory: () => void
}

// Advanced Search Component
interface AdvancedSearchComponent {
  searchCriteria: AdvancedSearchCriteria
  isVisible: boolean
  
  onSearch: (criteria: AdvancedSearchCriteria) => Promise<void>
  onSaveCriteria: (name: string) => void
  onLoadCriteria: (criteriaId: number) => void
  onClose: () => void
}

// Search Suggestions Component
interface SearchSuggestionsComponent {
  suggestions: SearchSuggestion[]
  isVisible: boolean
  
  onSuggestionSelect: (suggestion: SearchSuggestion) => void
  onSuggestionHover: (suggestion: SearchSuggestion) => void
}
```

---

### UI/UX Design

#### Search Interface Layout
- **Search Bar:**
  - Prominent search input
  - Auto-suggestions
  - Search button
  - Clear button

#### Filter Panel Design
- **Filter Layout:**
  - Collapsible sections
  - Clear filter options
  - Apply/reset buttons
  - Saved filters

#### Search Results Display
- **Results Layout:**
  - List/grid view options
  - Sortable columns
  - Pagination controls
  - Export options

#### Advanced Search Interface
- **Advanced Layout:**
  - Multiple criteria sections
  - Complex filter combinations
  - Saved search management
  - Search history

---

### Integration Requirements

#### Cost Item Integration
1. **Search Performance**
   - Indexed search fields
   - Optimized queries
   - Caching mechanisms
   - Result ranking

2. **Filter Integration**
   - Real-time filtering
   - Dynamic filter options
   - Filter validation
   - Filter persistence

#### User Experience Integration
1. **Search Experience**
   - Auto-complete suggestions
   - Search history
   - Saved searches
   - Quick filters

2. **Result Management**
   - Export functionality
   - Bulk operations
   - Result sharing
   - Result analytics

---

### Security Considerations

#### Data Protection
- Search permission validation
- Result access control
- Filter security
- Export security

#### Search Security
- Query validation
- SQL injection prevention
- Rate limiting
- Access logging

---

### Testing Strategy

#### Unit Tests
- Search logic validation
- Filter functionality
- Result ranking
- Export capabilities

#### Integration Tests
- Database search performance
- API endpoint testing
- Filter integration
- Export functionality

#### User Acceptance Tests
- Search workflow completion
- Filter accuracy
- Export functionality
- Performance validation

---

### Deployment & Configuration

#### Environment Setup
- Database indexing
- Search configuration
- Filter setup
- Export configuration

#### Monitoring & Logging
- Search performance monitoring
- User behavior tracking
- Error logging
- Analytics collection

---

### Documentation

#### User Manual
- Search procedures
- Filter guidelines
- Export functionality
- Advanced search

#### Technical Documentation
- API documentation
- Database schema
- Search implementation
- Integration guides 