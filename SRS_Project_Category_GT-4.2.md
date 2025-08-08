# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-4.2
### Tìm kiếm & Lọc Gói thầu Đa tiêu chí

#### Thông tin User Story
- **Story ID:** GT-4.2
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 4
- **Status:** To Do
- **Dependencies:** GT-1.1, GT-2.1, GT-3.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể tìm kiếm và lọc gói thầu dựa trên các tiêu chí quan trọng (ví dụ: mã gói thầu, tên gói thầu, dự án liên quan, giá trúng thầu),  
**Để** tôi có thể nhanh chóng truy xuất thông tin cần thiết và hỗ trợ việc tổng hợp báo cáo.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Giao diện có các trường tìm kiếm và bộ lọc dễ sử dụng
- [ ] Hỗ trợ tìm kiếm theo từ khóa và lọc theo danh sách chọn/khoảng giá trị
- [ ] Có thể tìm kiếm theo mã gói thầu, tên gói thầu, dự án liên quan
- [ ] Có thể lọc theo trạng thái, hình thức lựa chọn nhà thầu, khoảng giá trị
- [ ] Có thể lọc theo thời gian (ngày tạo, ngày kết thúc)
- [ ] Có thể lưu và tái sử dụng các bộ lọc thường dùng
- [ ] Hiển thị số lượng kết quả tìm kiếm
- [ ] Có thể sắp xếp kết quả theo các tiêu chí khác nhau
- [ ] Hỗ trợ tìm kiếm nâng cao với nhiều điều kiện kết hợp
- [ ] Có thể export kết quả tìm kiếm

#### 2.4 Activity Diagram
![GT-4.2 Activity Diagram](diagrams/GT-4.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tìm kiếm và lọc gói thầu đa tiêu chí*

---

### Functional Requirements

#### Core Features
1. **Search Interface**
   - Keyword search với autocomplete
   - Advanced search với multiple criteria
   - Search suggestions và recent searches
   - Search history và saved searches

2. **Filter System**
   - Multiple filter categories
   - Range filters cho numeric values
   - Date range filters
   - Multi-select filters
   - Filter combinations

3. **Result Management**
   - Pagination cho large result sets
   - Sorting options
   - Result count display
   - Export functionality
   - Bulk operations

4. **Search Analytics**
   - Search performance tracking
   - Popular search terms
   - Search suggestions
   - User search patterns

#### Business Rules
- Search results phải real-time
- Filters có thể kết hợp với nhau
- Search history được lưu trong 30 ngày
- Saved searches có thể được shared
- Export limit: 10,000 records per export
- Search timeout: 30 seconds

#### Search Criteria
1. **Basic Search**
   - Tender code (mã gói thầu)
   - Tender name (tên gói thầu)
   - Project name (tên dự án)
   - Description (mô tả)

2. **Advanced Filters**
   - Status (trạng thái)
   - Tender method (hình thức lựa chọn)
   - Estimated value range (khoảng giá trị)
   - Winning bid value range (khoảng giá trúng thầu)
   - Date range (khoảng thời gian)
   - Created by (người tạo)
   - Assigned to (người phụ trách)

3. **Document Filters**
   - Document type (loại tài liệu)
   - Document category (danh mục tài liệu)
   - Upload date range (khoảng ngày tải lên)

4. **API Integration Filters**
   - Portal data sync status
   - Bitrix workflow status
   - API call success/failure

---

### Technical Specifications

#### Sequence Diagram
![GT-4.2 Sequence Diagram](diagrams/GT-4.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tìm kiếm và lọc gói thầu đa tiêu chí*

#### Database Schema Updates
```sql
-- Bảng lưu trữ tìm kiếm của user
CREATE TABLE user_searches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    search_name VARCHAR(255) NOT NULL,
    search_type ENUM('basic', 'advanced', 'saved') NOT NULL,
    search_criteria JSON NOT NULL,
    result_count INT,
    is_shared BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Bảng lịch sử tìm kiếm
CREATE TABLE search_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    search_query TEXT NOT NULL,
    search_filters JSON,
    result_count INT,
    search_duration_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Bảng cấu hình tìm kiếm
CREATE TABLE search_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    search_field VARCHAR(100) NOT NULL,
    field_type ENUM('text', 'number', 'date', 'select', 'multiselect') NOT NULL,
    is_searchable BOOLEAN DEFAULT TRUE,
    is_filterable BOOLEAN DEFAULT TRUE,
    is_sortable BOOLEAN DEFAULT TRUE,
    search_weight FLOAT DEFAULT 1.0,
    filter_options JSON,
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_search_field (search_field)
);

-- Bảng thống kê tìm kiếm
CREATE TABLE search_analytics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    search_term VARCHAR(255) NOT NULL,
    search_count INT DEFAULT 1,
    avg_result_count FLOAT,
    avg_search_duration_ms FLOAT,
    first_searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_search_term (search_term)
);

-- Insert default search configuration
INSERT INTO search_config (search_field, field_type, is_searchable, is_filterable, is_sortable, search_weight, filter_options) VALUES
-- Basic search fields
('tender_code', 'text', TRUE, TRUE, TRUE, 10.0, '{"exact_match": true}'),
('tender_name', 'text', TRUE, TRUE, TRUE, 8.0, '{"fuzzy_search": true}'),
('project_name', 'text', TRUE, TRUE, TRUE, 7.0, '{"fuzzy_search": true}'),
('description', 'text', TRUE, FALSE, FALSE, 3.0, '{"fuzzy_search": true}'),

-- Advanced filter fields
('status', 'select', FALSE, TRUE, TRUE, 1.0, '{"options": ["draft", "created", "in_progress", "completed", "cancelled"]}'),
('tender_method', 'select', FALSE, TRUE, TRUE, 1.0, '{"options": ["open_tender", "limited_tender", "direct_appointment", "competitive_consultation", "other"]}'),
('estimated_value', 'number', FALSE, TRUE, TRUE, 1.0, '{"range_filter": true, "currency": "VND"}'),
('winning_bid_value', 'number', FALSE, TRUE, TRUE, 1.0, '{"range_filter": true, "currency": "VND"}'),
('start_date', 'date', FALSE, TRUE, TRUE, 1.0, '{"date_range": true}'),
('end_date', 'date', FALSE, TRUE, TRUE, 1.0, '{"date_range": true}'),
('created_at', 'date', FALSE, TRUE, TRUE, 1.0, '{"date_range": true}'),
('created_by', 'select', FALSE, TRUE, TRUE, 1.0, '{"user_list": true}'),
('assigned_to', 'select', FALSE, TRUE, TRUE, 1.0, '{"user_list": true}'),

-- Document filter fields
('document_type', 'multiselect', FALSE, TRUE, FALSE, 1.0, '{"options": ["approval", "tender", "contract", "other"]}'),
('document_category', 'multiselect', FALSE, TRUE, FALSE, 1.0, '{"options": ["approval_decisions", "tender_documents", "contract_documents", "evaluation_reports", "meeting_minutes", "other_documents"]}'),
('upload_date', 'date', FALSE, TRUE, TRUE, 1.0, '{"date_range": true}'),

-- API integration filter fields
('portal_sync_status', 'select', FALSE, TRUE, TRUE, 1.0, '{"options": ["synced", "pending", "failed"]}'),
('bitrix_workflow_status', 'select', FALSE, TRUE, TRUE, 1.0, '{"options": ["active", "completed", "cancelled", "error"]}');
```

#### API Endpoints
```
# Search và Filter
GET /api/tender-packages/search
{
  "query": "gói thầu IT",
  "filters": {
    "status": ["in_progress", "completed"],
    "tender_method": "open_tender",
    "estimated_value_range": {
      "min": 1000000000,
      "max": 5000000000
    },
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  },
  "sort": {
    "field": "created_at",
    "order": "desc"
  },
  "page": 1,
  "limit": 20
}

# Advanced Search
POST /api/tender-packages/advanced-search
{
  "criteria": [
    {
      "field": "tender_name",
      "operator": "contains",
      "value": "mua sắm"
    },
    {
      "field": "estimated_value",
      "operator": "between",
      "value": [1000000000, 5000000000]
    },
    {
      "field": "status",
      "operator": "in",
      "value": ["in_progress", "completed"]
    }
  ],
  "logic": "AND"
}

# Search Suggestions
GET /api/tender-packages/search-suggestions
{
  "query": "gói thầu",
  "limit": 10
}

# Saved Searches
GET /api/user/searches
POST /api/user/searches
PUT /api/user/searches/{id}
DELETE /api/user/searches/{id}

# Search Analytics
GET /api/search/analytics
{
  "popular_terms": [
    {"term": "gói thầu IT", "count": 150},
    {"term": "mua sắm thiết bị", "count": 120}
  ],
  "search_performance": {
    "avg_duration_ms": 250,
    "success_rate": 98.5
  }
}

# Export Search Results
POST /api/tender-packages/export-search-results
{
  "search_criteria": {...},
  "export_format": "excel",
  "include_columns": ["tender_code", "tender_name", "status", "estimated_value"]
}
```

#### Frontend Components
```typescript
// Search Interface Component
interface SearchInterface {
  searchQuery: string
  filters: SearchFilters
  sortOptions: SortOption[]
  onSearch: (query: string, filters: SearchFilters) => void
  onClearSearch: () => void
  onSaveSearch: (name: string) => void
}

// Advanced Filter Component
interface AdvancedFilterComponent {
  filters: SearchFilters
  availableFilters: FilterConfig[]
  onFilterChange: (filters: SearchFilters) => void
  onAddFilter: (filter: FilterConfig) => void
  onRemoveFilter: (filterName: string) => void
  onClearAllFilters: () => void
}

// Search Results Component
interface SearchResultsComponent {
  results: TenderPackage[]
  totalCount: number
  currentPage: number
  pageSize: number
  sortField: string
  sortOrder: 'asc' | 'desc'
  onPageChange: (page: number) => void
  onSortChange: (field: string, order: 'asc' | 'desc') => void
  onExportResults: (format: ExportFormat) => void
}

// Saved Searches Component
interface SavedSearchesComponent {
  savedSearches: SavedSearch[]
  onLoadSearch: (searchId: number) => void
  onDeleteSearch: (searchId: number) => void
  onShareSearch: (searchId: number) => void
}

// Search Suggestions Component
interface SearchSuggestionsComponent {
  suggestions: string[]
  recentSearches: string[]
  onSelectSuggestion: (suggestion: string) => void
  onSelectRecentSearch: (search: string) => void
}

// Filter Config Interface
interface FilterConfig {
  field: string
  type: 'text' | 'number' | 'date' | 'select' | 'multiselect'
  label: string
  options?: string[]
  range?: boolean
  currency?: string
}

// Search Filters Interface
interface SearchFilters {
  status?: string[]
  tender_method?: string[]
  estimated_value_range?: {
    min?: number
    max?: number
  }
  winning_bid_value_range?: {
    min?: number
    max?: number
  }
  date_range?: {
    start?: string
    end?: string
  }
  created_by?: string[]
  assigned_to?: string[]
  document_type?: string[]
  portal_sync_status?: string[]
  bitrix_workflow_status?: string[]
}
```

---

### UI/UX Design

#### Search Interface
- **Layout:** Header search bar với advanced filters panel
- **Components:**
  - Search input với autocomplete
  - Filter toggle button
  - Sort dropdown
  - Export button
  - Saved searches dropdown

#### Advanced Filters Panel
- **Layout:** Collapsible sidebar hoặc modal
- **Components:**
  - Filter categories (Basic, Status, Value, Date, etc.)
  - Range sliders cho numeric values
  - Date pickers cho date ranges
  - Multi-select dropdowns
  - Clear all filters button

#### Search Results
- **Layout:** Table hoặc card grid
- **Components:**
  - Result count display
  - Pagination controls
  - Sort column headers
  - Bulk action checkboxes
  - Quick action buttons

#### Search Suggestions
- **Layout:** Dropdown below search input
- **Components:**
  - Recent searches list
  - Popular search terms
  - Search suggestions
  - Clear history button

---

### Integration Requirements

#### Search Engine Integration
1. **Full-text Search**
   - Elasticsearch integration
   - Fuzzy matching
   - Relevance scoring
   - Search suggestions

2. **Database Search**
   - SQL-based search
   - Index optimization
   - Query performance
   - Result caching

#### Filter System Integration
1. **Dynamic Filters**
   - Filter options loading
   - Filter validation
   - Filter combinations
   - Filter persistence

2. **Range Filters**
   - Numeric range validation
   - Date range validation
   - Currency formatting
   - Range visualization

---

### Security Considerations

#### Search Security
- Input validation cho search queries
- SQL injection prevention
- XSS protection
- Rate limiting cho search requests

#### Data Protection
- User permission-based search results
- Sensitive data filtering
- Search log privacy
- Export data security

#### Access Control
- Search permission validation
- Filter access control
- Export permission checking
- Saved search sharing controls

---

### Testing Strategy

#### Unit Tests
- Search query validation
- Filter logic testing
- Sort functionality
- Export functionality

#### Integration Tests
- End-to-end search workflow
- Filter combination testing
- Performance testing
- Security testing

#### User Acceptance Tests
- Search interface usability
- Filter experience testing
- Result display testing
- Export functionality

---

### Deployment & Configuration

#### Environment Setup
- Search engine configuration
- Database indexing
- Cache configuration
- Performance monitoring

#### Monitoring & Logging
- Search performance tracking
- User search patterns
- Error tracking
- Usage analytics

---

### Documentation

#### User Manual
- Search interface guide
- Filter usage instructions
- Advanced search procedures
- Export functionality

#### Technical Documentation
- API documentation
- Search engine configuration
- Performance optimization
- Security implementation 