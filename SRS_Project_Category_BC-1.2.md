# Software Requirements Specification (SRS)
## Epic: Báo cáo - Tạo và Quản lý Báo cáo Tổng hợp

### User Story: BC-1.2
### Lựa chọn loại biểu đồ và định dạng hiển thị

#### Thông tin User Story
- **Story ID:** BC-1.2
- **Priority:** High
- **Story Points:** 13
- **Sprint:** Sprint 1
- **Status:** To Do
- **Phụ thuộc:** BC-1.1

#### Mô tả User Story
**Với vai trò là** Quản lý dự án/chương trình,  
**Tôi muốn** có thể lựa chọn loại biểu đồ (ví dụ: biểu đồ cột, biểu đồ đường, biểu đồ tròn) và định dạng hiển thị cho dữ liệu báo cáo,  
**Để** tôi có thể trực quan hóa thông tin một cách hiệu quả, dễ hiểu và phù hợp với mục đích phân tích.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Cung cấp nhiều tùy chọn biểu đồ cho các loại dữ liệu khác nhau (ví dụ: biểu đồ cột cho so sánh, biểu đồ đường cho xu hướng)
- [ ] Cho phép tùy chỉnh màu sắc, nhãn, tiêu đề biểu đồ
- [ ] Có thể thay đổi loại biểu đồ sau khi đã tạo
- [ ] Hỗ trợ biểu đồ tương tác (zoom, pan, drill-down)
- [ ] Có thể thêm nhiều biểu đồ vào cùng một báo cáo
- [ ] Có thể thiết lập layout và kích thước biểu đồ
- [ ] Có thể xuất biểu đồ ra file ảnh (PNG, JPG, SVG)
- [ ] Có thể thiết lập animation cho biểu đồ
- [ ] Hỗ trợ responsive design cho biểu đồ
- [ ] Có thể thiết lập legend và tooltip cho biểu đồ
- [ ] Có thể tạo biểu đồ từ dữ liệu real-time
- [ ] Hệ thống gợi ý loại biểu đồ phù hợp dựa trên dữ liệu

#### 2.4 Activity Diagram
![BC-1.2 Activity Diagram](diagrams/BC-1.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý lựa chọn loại biểu đồ và định dạng hiển thị*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Loại Biểu đồ**
   - Biểu đồ cột (dọc/ngang)
   - Biểu đồ đường
   - Biểu đồ tròn
   - Biểu đồ vùng
   - Biểu đồ phân tán
   - Biểu đồ bong bóng
   - Biểu đồ nhiệt
   - Biểu đồ Gantt
   - Biểu đồ thác nước
   - Biểu đồ phễu

2. **Tùy chỉnh Biểu đồ**
   - Bảng màu
   - Kiểu font
   - Tiêu đề biểu đồ
   - Nhãn trục
   - Nhãn dữ liệu
   - Legend
   - Đường lưới
   - Kiểu nền

3. **Tính năng Tương tác**
   - Zoom in/out
   - Pan navigation
   - Khả năng drill-down
   - Hover tooltips
   - Click events
   - Highlight selection
   - Hiệu ứng animation

4. **Quản lý Layout**
   - Layout nhiều biểu đồ
   - Vị trí biểu đồ
   - Điều chỉnh kích thước
   - Responsive design
   - Print layout
   - Export layout

#### Quy tắc Kinh doanh
- Biểu đồ phải phản ánh chính xác dữ liệu gốc
- Màu sắc phải đảm bảo khả năng phân biệt cho người mù màu
- Kích thước biểu đồ phải phù hợp với thiết bị hiển thị
- Animation không được làm chậm hiệu suất hệ thống
- Dữ liệu nhạy cảm phải được ẩn trong tooltip
- Biểu đồ phải có title và legend rõ ràng

#### Danh mục Biểu đồ
1. **Biểu đồ So sánh**
   - Biểu đồ cột
   - Biểu đồ cột dọc
   - Biểu đồ cột nhóm
   - Biểu đồ cột xếp chồng
   - Biểu đồ radar
   - Biểu đồ nhện

2. **Biểu đồ Xu hướng**
   - Biểu đồ đường
   - Biểu đồ vùng
   - Biểu đồ bậc thang
   - Biểu đồ spline
   - Biểu đồ đa đường
   - Time series charts

3. **Distribution Charts**
   - Pie charts
   - Donut charts
   - Histogram charts
   - Box plots
   - Violin plots
   - Scatter plots

4. **Relationship Charts**
   - Scatter plots
   - Bubble charts
   - Heat maps
   - Correlation matrices
   - Network graphs
   - Sankey diagrams

5. **Progress Charts**
   - Gantt charts
   - Waterfall charts
   - Funnel charts
   - Progress bars
   - Bullet charts
   - Speedometer charts

---

### Non-Functional Requirements

#### Performance Requirements
- Biểu đồ phải render trong vòng 3 giây
- Animation phải mượt mà (60fps)
- Hỗ trợ hiển thị tối đa 10,000 điểm dữ liệu
- Zoom/pan phải responsive trong vòng 100ms
- Export ảnh phải hoàn thành trong vòng 10 giây

#### Usability Requirements
- Giao diện chọn biểu đồ trực quan, dễ sử dụng
- Preview biểu đồ trước khi áp dụng
- Undo/redo cho các thay đổi biểu đồ
- Keyboard shortcuts cho thao tác nhanh
- Hỗ trợ touch gestures trên mobile
- Accessibility compliance (WCAG 2.1)

#### Compatibility Requirements
- Hỗ trợ tất cả trình duyệt hiện đại
- Responsive design cho mobile/tablet
- Print-friendly layout
- High DPI display support
- Dark/light theme support

#### Security Requirements
- Validate dữ liệu trước khi render biểu đồ
- Sanitize user input cho customization
- Prevent XSS trong chart labels
- Encrypt sensitive data trong tooltips
- Log chart creation and modification

---

### Technical Requirements

#### Chart Library Integration
1. **Chart.js Integration**
   - Core chart types
   - Custom plugins
   - Animation support
   - Responsive design
   - Export capabilities

2. **D3.js Integration**
   - Custom visualizations
   - Advanced interactions
   - Data binding
   - SVG manipulation
   - Animation control

3. **Highcharts Integration**
   - Professional charts
   - Export options
   - Theme support
   - Accessibility features
   - Mobile optimization

4. **Custom Chart Engine**
   - Custom chart types
   - Performance optimization
   - Memory management
   - Error handling
   - Debug tools

#### Database Schema
```sql
-- Chart Templates
CREATE TABLE chart_templates (
    id INT PRIMARY KEY,
    template_name VARCHAR(100),
    chart_type VARCHAR(50),
    chart_config JSON,
    created_by INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN
);

-- Chart Customizations
CREATE TABLE chart_customizations (
    id INT PRIMARY KEY,
    chart_id INT,
    color_scheme VARCHAR(50),
    font_family VARCHAR(50),
    font_size INT,
    title_text VARCHAR(255),
    legend_position VARCHAR(20),
    animation_enabled BOOLEAN,
    responsive_enabled BOOLEAN
);

-- Chart Data Sources
CREATE TABLE chart_data_sources (
    id INT PRIMARY KEY,
    chart_id INT,
    data_source_type VARCHAR(50),
    data_source_config JSON,
    refresh_interval INT,
    last_refresh TIMESTAMP
);

-- Chart Permissions
CREATE TABLE chart_permissions (
    id INT PRIMARY KEY,
    user_id INT,
    chart_id INT,
    permission_type VARCHAR(50),
    granted_at TIMESTAMP
);
```

#### API Endpoints
```typescript
// Chart Management
GET /api/charts
POST /api/charts
PUT /api/charts/{id}
DELETE /api/charts/{id}

// Chart Templates
GET /api/charts/templates
POST /api/charts/templates
PUT /api/charts/templates/{id}
DELETE /api/charts/templates/{id}

// Chart Customization
GET /api/charts/{id}/customization
PUT /api/charts/{id}/customization
POST /api/charts/{id}/preview

// Chart Export
POST /api/charts/{id}/export
GET /api/charts/{id}/export/{format}

// Chart Data
GET /api/charts/{id}/data
POST /api/charts/{id}/data
PUT /api/charts/{id}/data
```

---

### User Interface Requirements

#### Chart Selection Interface
1. **Chart Type Gallery**
   - Visual chart type preview
   - Chart type categories
   - Chart type descriptions
   - Recommended use cases
   - Data requirements

2. **Chart Type Wizard**
   - Step-by-step chart creation
   - Data type analysis
   - Chart type recommendations
   - Preview functionality
   - Quick apply options

3. **Chart Type Comparison**
   - Side-by-side comparison
   - Pros and cons
   - Data suitability
   - Performance impact
   - Accessibility features

#### Chart Customization Panel
1. **Visual Customization**
   - Color palette selection
   - Font family and size
   - Chart title and subtitle
   - Axis labels and titles
   - Data labels format

2. **Layout Customization**
   - Chart size and position
   - Legend position and style
   - Grid lines and background
   - Margins and padding
   - Responsive breakpoints

3. **Interactive Customization**
   - Tooltip content and style
   - Click event handlers
   - Animation settings
   - Zoom and pan options
   - Drill-down configuration

#### Chart Preview and Export
1. **Preview Options**
   - Real-time preview
   - Different device previews
   - Print preview
   - Full-screen preview
   - Comparison preview

2. **Export Options**
   - Image formats (PNG, JPG, SVG)
   - PDF export
   - Excel export with chart
   - HTML export
   - Embed code generation

---

### Integration Requirements

#### Data Source Integration
- Real-time data feeds
- Database connections
- API data sources
- File imports
- WebSocket connections

#### Export Service Integration
- Image processing service
- PDF generation service
- Email service
- File storage service
- Cloud storage

#### Third-party Services
- Chart.js library
- D3.js library
- Highcharts library
- Canvas API
- SVG manipulation

#### Analytics Integration
- Chart usage analytics
- Performance monitoring
- User behavior tracking
- Error reporting
- A/B testing

---

### Testing Requirements

#### Unit Testing
- Chart rendering logic
- Data transformation
- Customization functions
- Export functionality
- Animation handling

#### Integration Testing
- Chart library integration
- Data source connections
- Export service integration
- Third-party service integration
- API endpoint testing

#### User Acceptance Testing
- Chart selection interface
- Customization features
- Export functionality
- Interactive features
- Responsive design

#### Performance Testing
- Large dataset rendering
- Animation performance
- Export performance
- Memory usage optimization
- Concurrent user testing

---

### Deployment Requirements

#### Environment Setup
- Chart rendering server
- Image processing server
- CDN for chart assets
- Backup systems
- Monitoring tools

#### Monitoring & Alerting
- Chart rendering performance
- Export service monitoring
- Error rate tracking
- User experience metrics
- System resource usage

#### Security Considerations
- Data validation
- Input sanitization
- XSS prevention
- CSRF protection
- Rate limiting

#### Backup & Recovery
- Chart template backup
- Customization backup
- Configuration backup
- Disaster recovery plan

---

### Documentation Requirements

#### User Documentation
- Chart selection guide
- Customization guide
- Export options guide
- Best practices guide
- Troubleshooting guide

#### Technical Documentation
- Chart library integration
- API documentation
- Performance guidelines
- Security guidelines
- Deployment guide

#### Admin Documentation
- System configuration
- Monitoring setup
- Security guidelines
- Maintenance procedures

---

### Data Requirements

#### Chart Data Types
1. **Numerical Data**
   - Integer values
   - Decimal values
   - Percentage values
   - Currency values
   - Scientific notation

2. **Categorical Data**
   - Text labels
   - Category codes
   - Hierarchical data
   - Multi-level categories
   - Time-based categories

3. **Time Series Data**
   - Date/time values
   - Time intervals
   - Seasonal patterns
   - Trend analysis
   - Forecasting data

4. **Geographic Data**
   - Location coordinates
   - Geographic regions
   - Spatial relationships
   - Map overlays
   - Location-based data

#### Data Quality
- Data validation rules
- Data type checking
- Missing data handling
- Outlier detection
- Data consistency validation

#### Data Performance
- Data caching strategies
- Lazy loading
- Data compression
- Query optimization
- Memory management

#### 5.5 Sequence Diagram
![BC-1.2 Sequence Diagram](diagrams/BC-1.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi lựa chọn loại biểu đồ và định dạng hiển thị* 