# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-5.2
### Tìm kiếm & Lọc Hợp đồng Đa tiêu chí

#### Thông tin User Story
- **Story ID:** HD-5.2
- **Priority:** Medium
- **Story Points:** 6
- **Sprint:** Sprint 5
- **Status:** To Do
- **Phụ thuộc:** HD-1.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách hợp đồng,  
**Tôi muốn** có thể tìm kiếm và lọc hợp đồng dựa trên các tiêu chí quan trọng (ví dụ: mã hợp đồng, tên hợp đồng, gói thầu liên quan, giá trị hợp đồng, trạng thái, ngày ký/hiệu lực/hết hạn),  
**Để** tôi có thể nhanh chóng truy xuất thông tin cần thiết và hỗ trợ việc tổng hợp báo cáo.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Giao diện có các trường tìm kiếm và bộ lọc dễ sử dụng
- [ ] Hỗ trợ tìm kiếm theo từ khóa và lọc theo danh sách chọn/khoảng giá trị
- [ ] Có thể tìm kiếm theo mã hợp đồng, tên hợp đồng, mô tả
- [ ] Có thể lọc theo gói thầu liên quan, giá trị hợp đồng, trạng thái
- [ ] Có thể lọc theo khoảng thời gian (ngày ký, hiệu lực, hết hạn)
- [ ] Có thể lọc theo người quản lý, người giám sát hợp đồng
- [ ] Hỗ trợ tìm kiếm nâng cao với nhiều tiêu chí kết hợp
- [ ] Có thể lưu và tái sử dụng các bộ lọc thường dùng
- [ ] Hiển thị số lượng kết quả tìm kiếm
- [ ] Có thể xuất kết quả tìm kiếm ra file Excel/PDF
- [ ] Hỗ trợ sắp xếp kết quả theo nhiều tiêu chí
- [ ] Có thể xem preview thông tin hợp đồng trong kết quả tìm kiếm

#### 2.4 Activity Diagram
![HD-5.2 Activity Diagram](diagrams/HD-5.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tìm kiếm và lọc hợp đồng đa tiêu chí*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Tìm kiếm Nâng cao**
   - Tìm kiếm từ khóa
   - Tìm kiếm đa trường
   - Fuzzy matching
   - Gợi ý tìm kiếm

2. **Hệ thống Lọc**
   - Nhiều tiêu chí lọc
   - Bộ lọc khoảng giá trị
   - Bộ lọc khoảng thời gian
   - Bộ lọc dropdown

3. **Kết quả Tìm kiếm**
   - Phân trang
   - Tùy chọn sắp xếp
   - Preview kết quả
   - Chức năng xuất

4. **Bộ lọc Đã lưu**
   - Lưu trữ bộ lọc
   - Chia sẻ bộ lọc
   - Truy cập nhanh
   - Quản lý bộ lọc

#### Quy tắc Kinh doanh
- Tìm kiếm phải hỗ trợ partial matching
- Kết quả tìm kiếm phải được sắp xếp theo relevance
- Bộ lọc phải có thể kết hợp nhiều tiêu chí
- Bộ lọc đã lưu phải có thể chia sẻ giữa các users
- Xuất phải bao gồm tất cả thông tin hiển thị

#### Tiêu chí Tìm kiếm
1. **Thông tin Cơ bản**
   - Mã hợp đồng
   - Tên hợp đồng
   - Mô tả hợp đồng
   - Loại hợp đồng

2. **Thông tin Liên quan**
   - Gói thầu liên quan
   - Dự án
   - Danh mục

3. **Thông tin Tài chính**
   - Khoảng giá trị hợp đồng
   - Trạng thái thanh toán
   - Phân bổ ngân sách

4. **Trạng thái & Ngày tháng**
   - Trạng thái hợp đồng
   - Khoảng ngày ký
   - Khoảng ngày hiệu lực
   - Khoảng ngày hết hạn

5. **Người dùng & Vai trò**
   - Người quản lý
   - Người giám sát
   - Người tạo
   - Người cập nhật

6. **Tiêu chí Nâng cao**
   - Khoảng ngày tạo
   - Last modified date range (khoảng ngày cập nhật)
   - Tags (thẻ)
   - Priority (ưu tiên)
   - Risk level (mức độ rủi ro)

---

#### 5.5 Sequence Diagram
![HD-5.2 Sequence Diagram](diagrams/HD-5.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tìm kiếm và lọc hợp đồng đa tiêu chí*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng lưu trữ bộ lọc đã lưu
CREATE TABLE contract_search_filters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    filter_name VARCHAR(200) NOT NULL,
    filter_description TEXT,
    filter_criteria JSON NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    is_default BOOLEAN DEFAULT FALSE,
    usage_count INT DEFAULT 0,
    last_used_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_filter (user_id, filter_name),
    INDEX idx_user_id (user_id),
    INDEX idx_is_public (is_public)
);

-- Bảng lịch sử tìm kiếm
CREATE TABLE contract_search_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    search_query TEXT,
    search_criteria JSON,
    result_count INT DEFAULT 0,
    search_duration_ms INT,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_performed_at (performed_at)
);

-- Bảng cấu hình tìm kiếm
CREATE TABLE contract_search_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng từ khóa tìm kiếm phổ biến
CREATE TABLE contract_search_keywords (
    id INT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(200) NOT NULL,
    search_count INT DEFAULT 0,
    last_searched_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_keyword (keyword),
    INDEX idx_search_count (search_count),
    INDEX idx_last_searched (last_searched_at)
);

-- Bảng kết quả tìm kiếm được lưu
CREATE TABLE contract_search_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    search_session_id VARCHAR(100) NOT NULL,
    contract_id INT NOT NULL,
    relevance_score DECIMAL(5,2),
    result_position INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    INDEX idx_session_id (search_session_id),
    INDEX idx_user_session (user_id, search_session_id)
);

-- Insert default search configuration
INSERT INTO contract_search_config (config_key, config_value, description) VALUES
('max_results_per_page', '50', 'Maximum number of results per page'),
('search_timeout_ms', '5000', 'Search timeout in milliseconds'),
('fuzzy_match_threshold', '0.8', 'Fuzzy matching threshold'),
('enable_search_suggestions', 'true', 'Enable search suggestions'),
('enable_search_history', 'true', 'Enable search history'),
('enable_saved_filters', 'true', 'Enable saved filters'),
('default_sort_field', 'created_at', 'Default sort field'),
('default_sort_order', 'desc', 'Default sort order'),
('export_max_records', '10000', 'Maximum records for export'),
('search_cache_ttl', '300', 'Search cache TTL in seconds');
```

#### API Endpoints
```
# Contract Search
GET /api/contracts/search
{
  "query": "contract name",
  "filters": {
    "contract_code": "HD-2024-001",
    "contract_type": ["service", "goods"],
    "contract_status": "active",
    "contract_value_min": 1000000,
    "contract_value_max": 10000000,
    "tender_package_id": 123,
    "contract_manager_id": 456,
    "signing_date_from": "2024-01-01",
    "signing_date_to": "2024-12-31",
    "effective_date_from": "2024-01-01",
    "effective_date_to": "2024-12-31",
    "expiry_date_from": "2024-01-01",
    "expiry_date_to": "2024-12-31"
  },
  "sort": {
    "field": "contract_value",
    "order": "desc"
  },
  "page": 1,
  "limit": 50
}

# Advanced Search
POST /api/contracts/search/advanced
{
  "search_criteria": [
    {
      "field": "contract_name",
      "operator": "contains",
      "value": "construction"
    },
    {
      "field": "contract_value",
      "operator": "between",
      "value": [1000000, 10000000]
    },
    {
      "field": "contract_status",
      "operator": "in",
      "value": ["active", "pending"]
    }
  ],
  "logical_operator": "AND",
  "sort": [
    {
      "field": "contract_value",
      "order": "desc"
    },
    {
      "field": "created_at",
      "order": "desc"
    }
  ]
}

# Saved Filters
GET /api/contracts/search/filters
POST /api/contracts/search/filters
{
  "filter_name": "Active High Value Contracts",
  "filter_description": "Contracts with value > 1B and status active",
  "filter_criteria": {
    "contract_status": "active",
    "contract_value_min": 1000000000
  },
  "is_public": false
}

PUT /api/contracts/search/filters/{filter_id}
DELETE /api/contracts/search/filters/{filter_id}

# Search History
GET /api/contracts/search/history
DELETE /api/contracts/search/history/{history_id}

# Search Suggestions
GET /api/contracts/search/suggestions
{
  "query": "const",
  "limit": 10
}

# Search Statistics
GET /api/contracts/search/stats
Response: {
  "total_searches": 1500,
  "popular_keywords": [
    {"keyword": "construction", "count": 150},
    {"keyword": "service", "count": 120}
  ],
  "popular_filters": [
    {"filter_name": "Active Contracts", "usage_count": 50},
    {"filter_name": "High Value", "usage_count": 30}
  ]
}

# Export Search Results
POST /api/contracts/search/export
{
  "search_criteria": {...},
  "export_format": "excel",
  "include_details": true,
  "columns": ["contract_code", "contract_name", "contract_value", "status"]
}

# Search Configuration
GET /api/contracts/search/config
PUT /api/contracts/search/config
{
  "max_results_per_page": 100,
  "search_timeout_ms": 10000,
  "fuzzy_match_threshold": 0.9
}
```

#### Frontend Components
```typescript
// Contract Search Component
interface ContractSearchComponent {
  searchQuery: string
  searchResults: Contract[]
  isLoading: boolean
  totalResults: number
  
  onSearch: (query: string, filters: SearchFilters) => Promise<void>
  onClearSearch: () => void
  onLoadMore: () => void
  onExportResults: (format: string) => Promise<void>
}

// Search Filter Component
interface SearchFilterComponent {
  filters: SearchFilters
  availableFilters: FilterOptions
  
  onFilterChange: (filters: SearchFilters) => void
  onResetFilters: () => void
  onSaveFilter: (filterName: string) => Promise<void>
  onLoadFilter: (filterId: number) => void
}

// Advanced Search Component
interface AdvancedSearchComponent {
  searchCriteria: SearchCriterion[]
  logicalOperator: 'AND' | 'OR'
  
  onAddCriterion: (criterion: SearchCriterion) => void
  onRemoveCriterion: (index: number) => void
  onUpdateCriterion: (index: number, criterion: SearchCriterion) => void
  onSearch: () => Promise<void>
}

// Saved Filters Component
interface SavedFiltersComponent {
  savedFilters: SavedFilter[]
  isLoading: boolean
  
  onLoadFilter: (filter: SavedFilter) => void
  onSaveFilter: (filter: Partial<SavedFilter>) => Promise<void>
  onDeleteFilter: (filterId: number) => Promise<void>
  onShareFilter: (filterId: number, userIds: number[]) => Promise<void>
}

// Search History Component
interface SearchHistoryComponent {
  searchHistory: SearchHistoryEntry[]
  isLoading: boolean
  
  onLoadHistory: (entry: SearchHistoryEntry) => void
  onDeleteHistory: (entryId: number) => Promise<void>
  onClearHistory: () => Promise<void>
}

// Search Suggestions Component
interface SearchSuggestionsComponent {
  suggestions: string[]
  isLoading: boolean
  
  onSelectSuggestion: (suggestion: string) => void
  onLoadSuggestions: (query: string) => Promise<void>
}

// Search Results Component
interface SearchResultsComponent {
  results: Contract[]
  totalResults: number
  currentPage: number
  pageSize: number
  sortField: string
  sortOrder: 'asc' | 'desc'
  
  onPageChange: (page: number) => void
  onSortChange: (field: string, order: string) => void
  onViewContract: (contractId: number) => void
  onExportResults: (format: string) => Promise<void>
}

// Search Statistics Component
interface SearchStatisticsComponent {
  statistics: SearchStatistics
  
  onViewPopularKeywords: () => void
  onViewPopularFilters: () => void
  onExportStatistics: () => void
}

// Search Configuration Component
interface SearchConfigurationComponent {
  config: SearchConfig
  
  onUpdateConfig: (config: Partial<SearchConfig>) => Promise<void>
  onResetConfig: () => Promise<void>
  onExportConfig: () => void
}

// Quick Search Component
interface QuickSearchComponent {
  searchQuery: string
  recentSearches: string[]
  
  onSearch: (query: string) => void
  onSelectRecent: (query: string) => void
  onClearRecent: () => void
}
```

---

### UI/UX Design

#### Search Interface
- **Search Bar:**
  - Auto-complete suggestions
  - Recent searches
  - Quick filters
  - Search button

#### Filter Panel
- **Filter Layout:**
  - Collapsible filter sections
  - Range sliders
  - Date pickers
  - Multi-select dropdowns

#### Search Results
- **Results View:**
  - List/grid toggle
  - Sort options
  - Pagination
  - Export button

#### Advanced Search
- **Advanced Interface:**
  - Criteria builder
  - Logical operators
  - Field selection
  - Operator selection

---

### Integration Requirements

#### Search Engine Integration
1. **Full-text Search**
   - Elasticsearch integration
   - Fuzzy matching
   - Relevance scoring
   - Search suggestions

2. **Filter Integration**
   - Real-time filtering
   - Dynamic filter options
   - Filter persistence
   - Filter sharing

#### Performance Optimization
1. **Search Performance**
   - Database indexing
   - Query optimization
   - Result caching
   - Pagination

2. **User Experience**
   - Real-time search
   - Progressive loading
   - Search suggestions
   - Recent searches

---

### Security Considerations

#### Search Security
- Role-based search access
- Data filtering by permissions
- Sensitive data masking
- Search audit logging

#### Data Protection
- Search query encryption
- Result data protection
- Export restrictions
- Access control

---

### Testing Strategy

#### Unit Tests
- Search algorithm accuracy
- Filter logic validation
- Export functionality
- Performance testing

#### Integration Tests
- Search engine integration
- Database query optimization
- Real-time search testing
- Export system testing

#### User Acceptance Tests
- Search interface usability
- Filter functionality testing
- Export capabilities
- Performance under load

---

### Deployment & Configuration

#### Environment Setup
- Search engine configuration
- Database indexing setup
- Cache configuration
- Performance monitoring

#### Monitoring & Logging
- Search performance monitoring
- User search behavior tracking
- Export activity monitoring
- Error tracking

---

### Documentation

#### User Manual
- Search interface guide
- Filter usage instructions
- Export procedures
- Advanced search guide

#### Technical Documentation
- API documentation
- Search architecture
- Performance optimization
- Security implementation 