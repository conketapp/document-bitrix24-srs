# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-3.1
### Đính kèm chứng từ/hóa đơn cho khoản mục chi phí

#### Thông tin User Story
- **Story ID:** CP-3.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 3
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** có thể đính kèm các file chứng từ, hóa đơn hoặc các tài liệu liên quan trực tiếp vào từng khoản mục chi phí  
**Để** tôi có thể lưu trữ tập trung bằng chứng chi tiêu và dễ dàng truy xuất khi cần kiểm tra hoặc đối chiếu.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có khu vực tải lên tệp đính kèm trong hồ sơ khoản mục chi phí
- [ ] Hỗ trợ các định dạng file phổ biến (PDF, JPG, PNG, DOCX, XLSX)
- [ ] Có thể tải lên nhiều file cùng lúc
- [ ] Hiển thị danh sách các file đã đính kèm với thông tin chi tiết
- [ ] Có thể xem trước file (preview) trước khi tải lên
- [ ] Có thể đặt tên và mô tả cho từng file đính kèm
- [ ] Có thể phân loại file theo loại tài liệu (hóa đơn, chứng từ, hợp đồng, v.v.)
- [ ] Có thể tải xuống file đính kèm
- [ ] Có thể xóa file đính kèm (với quyền phù hợp)
- [ ] Hệ thống hiển thị dung lượng file và trạng thái tải lên
- [ ] Có thể tìm kiếm và lọc file đính kèm
- [ ] Hệ thống ghi log lịch sử tải lên/xóa file
- [ ] Hỗ trợ kéo thả (drag & drop) để tải lên file
- [ ] Có thể tải lên file từ URL hoặc cloud storage

---

### Functional Requirements

#### Core Features
1. **File Upload Management**
   - Multiple file upload support
   - Drag & drop functionality
   - File type validation
   - File size limits
   - Upload progress tracking

2. **File Organization**
   - File categorization
   - Custom naming
   - Description management
   - Tagging system
   - Search and filter

3. **File Preview & Access**
   - File preview capabilities
   - Download functionality
   - Version control
   - Access permissions
   - File sharing

4. **Document Management**
   - Document lifecycle
   - Approval workflows
   - Audit trails
   - Backup and recovery
   - Security controls

#### Business Rules
- Chỉ người có quyền mới được tải lên/xóa file
- File size tối đa: 50MB cho mỗi file
- Tổng dung lượng file cho mỗi khoản mục chi phí: 500MB
- File phải được quét virus trước khi lưu trữ
- File nhạy cảm phải được mã hóa
- Lịch sử tải lên/xóa file phải được ghi lại đầy đủ

#### Supported File Types
1. **Documents**: PDF (.pdf), Microsoft Word (.docx, .doc), Microsoft Excel (.xlsx, .xls), Text files (.txt)
2. **Images**: JPEG (.jpg, .jpeg), PNG (.png), GIF (.gif), TIFF (.tiff)
3. **Archives**: ZIP (.zip), RAR (.rar), 7Z (.7z)
4. **Other**: CSV (.csv), XML (.xml), JSON (.json)

#### File Categories
1. **Invoices & Receipts**: Hóa đơn VAT, Biên lai thanh toán, Chứng từ thuế
2. **Contracts & Agreements**: Hợp đồng, Phụ lục hợp đồng, Thỏa thuận
3. **Technical Documents**: Bản vẽ kỹ thuật, Báo cáo kỹ thuật, Tài liệu thiết kế
4. **Financial Documents**: Báo cáo tài chính, Chứng từ kế toán, Bảng giá
5. **Other Documents**: Tài liệu khác, Ghi chú, Báo cáo

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng tài liệu đính kèm chi phí (cập nhật từ CP-1.1)
CREATE TABLE cost_attachments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cost_item_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_extension VARCHAR(20) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    description TEXT,
    category VARCHAR(100) DEFAULT 'other',
    tags JSON,
    is_public BOOLEAN DEFAULT FALSE,
    is_encrypted BOOLEAN DEFAULT FALSE,
    encryption_key VARCHAR(255) NULL,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP NULL,
    access_count INT DEFAULT 0,
    status ENUM('active', 'deleted', 'archived') DEFAULT 'active',
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_file_type (file_type),
    INDEX idx_category (category),
    INDEX idx_uploaded_at (uploaded_at),
    INDEX idx_status (status)
);

-- Bảng lịch sử tài liệu
CREATE TABLE attachment_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    attachment_id INT NOT NULL,
    action_type ENUM('uploaded', 'downloaded', 'deleted', 'updated', 'shared') NOT NULL,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    notes TEXT,
    
    FOREIGN KEY (attachment_id) REFERENCES cost_attachments(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_attachment_id (attachment_id),
    INDEX idx_action_type (action_type),
    INDEX idx_performed_at (performed_at)
);

-- Bảng phân quyền tài liệu
CREATE TABLE attachment_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    attachment_id INT NOT NULL,
    user_id INT NULL,
    role_id INT NULL,
    permission_type ENUM('view', 'download', 'edit', 'delete', 'share') NOT NULL,
    granted_by INT NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    
    FOREIGN KEY (attachment_id) REFERENCES cost_attachments(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (granted_by) REFERENCES users(id),
    UNIQUE KEY unique_permission (attachment_id, user_id, role_id, permission_type),
    INDEX idx_attachment_id (attachment_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id)
);

-- Bảng cấu hình tải lên
CREATE TABLE upload_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_type VARCHAR(50) NOT NULL,
    max_file_size BIGINT NOT NULL,
    allowed_extensions JSON NOT NULL,
    mime_types JSON NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_file_type (file_type),
    INDEX idx_is_active (is_active)
);

-- Insert default upload configuration
INSERT INTO upload_config (file_type, max_file_size, allowed_extensions, mime_types) VALUES
('document', 52428800, '["pdf", "doc", "docx", "xls", "xlsx", "txt"]', '["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/plain"]'),
('image', 10485760, '["jpg", "jpeg", "png", "gif", "tiff"]', '["image/jpeg", "image/png", "image/gif", "image/tiff"]'),
('archive', 104857600, '["zip", "rar", "7z"]', '["application/zip", "application/x-rar-compressed", "application/x-7z-compressed"]'),
('other', 52428800, '["csv", "xml", "json"]', '["text/csv", "application/xml", "application/json"]');
```

#### API Endpoints
```typescript
# File Upload Management
POST /api/cost-items/{id}/attachments/upload
Content-Type: multipart/form-data
{
  "files": File[],
  "category": "invoice",
  "description": "Hóa đơn thanh toán tháng 1",
  "tags": ["hóa đơn", "thanh toán"],
  "is_public": false
}

# File List
GET /api/cost-items/{id}/attachments
{
  "category_filter": "invoice",
  "file_type_filter": "document",
  "search_term": "hóa đơn",
  "page": 1,
  "limit": 20
}

# File Download
GET /api/cost-items/{id}/attachments/{attachment_id}/download

# File Preview
GET /api/cost-items/{id}/attachments/{attachment_id}/preview

# File Update
PUT /api/cost-items/{id}/attachments/{attachment_id}
{
  "description": "Hóa đơn thanh toán tháng 1 - Cập nhật",
  "category": "invoice",
  "tags": ["hóa đơn", "thanh toán", "tháng 1"],
  "is_public": false
}

# File Delete
DELETE /api/cost-items/{id}/attachments/{attachment_id}
{
  "reason": "File không còn cần thiết"
}

# File Search
GET /api/cost-items/{id}/attachments/search
{
  "query": "hóa đơn tháng 1",
  "file_types": ["document", "image"],
  "categories": ["invoice", "receipt"],
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}

# File Statistics
GET /api/cost-items/{id}/attachments/statistics
Response: {
  "total_files": 15,
  "total_size": 52428800,
  "file_types": {
    "document": 8,
    "image": 5,
    "archive": 2
  },
  "categories": {
    "invoice": 10,
    "contract": 3,
    "other": 2
  },
  "storage_usage": {
    "used": 52428800,
    "limit": 524288000,
    "percentage": 10.0
  }
}
```

#### Frontend Components
```typescript
// File Upload Component
interface FileUploadComponent {
  costItemId: number
  maxFiles: number
  maxFileSize: number
  allowedFileTypes: string[]
  
  onFileSelect: (files: File[]) => void
  onUpload: (files: File[], metadata: FileMetadata) => Promise<void>
  onUploadProgress: (progress: number) => void
  onUploadComplete: (results: UploadResult[]) => void
  onUploadError: (error: UploadError) => void
}

// File List Component
interface FileListComponent {
  costItemId: number
  files: Attachment[]
  filters: FileFilters
  
  onFileSelect: (file: Attachment) => void
  onFileDownload: (file: Attachment) => void
  onFileDelete: (file: Attachment) => Promise<void>
  onFileUpdate: (file: Attachment, updates: Partial<Attachment>) => Promise<void>
  onFilterChange: (filters: FileFilters) => void
}

// File Preview Component
interface FilePreviewComponent {
  file: Attachment
  isVisible: boolean
  
  onClose: () => void
  onDownload: () => void
  onShare: () => void
  onPrint: () => void
}

// File Search Component
interface FileSearchComponent {
  searchQuery: string
  filters: SearchFilters
  
  onSearch: (query: string) => void
  onFilterChange: (filters: SearchFilters) => void
  onClearSearch: () => void
}

// File Statistics Component
interface FileStatisticsComponent {
  statistics: FileStatistics
  
  onRefreshStatistics: () => Promise<void>
  onViewDetails: (category: string) => void
}

// File Drag Drop Component
interface FileDragDropComponent {
  isDragOver: boolean
  acceptedFileTypes: string[]
  maxFileSize: number
  
  onFilesDrop: (files: File[]) => void
  onDragEnter: () => void
  onDragLeave: () => void
  onDragOver: (event: DragEvent) => void
}
```

---

### UI/UX Design

#### File Upload Interface
- **Upload Area:**
  - Drag & drop zone
  - File selection button
  - Progress indicators
  - File type validation

#### File Management Interface
- **File List:**
  - Grid/list view options
  - File thumbnails
  - File information display
  - Action buttons

#### File Preview Interface
- **Preview Window:**
  - Document viewer
  - Image gallery
  - Zoom controls
  - Navigation tools

#### File Organization Interface
- **Category Management:**
  - Category selection
  - Tag management
  - Search functionality
  - Filter options

---

### Integration Requirements

#### Storage Integration
1. **File Storage**
   - Cloud storage support
   - Local storage backup
   - CDN integration
   - Version control

2. **Security Integration**
   - Virus scanning
   - File encryption
   - Access control
   - Audit logging

#### Document Processing
1. **File Processing**
   - Thumbnail generation
   - Text extraction
   - Metadata extraction
   - Format conversion

2. **Preview Generation**
   - PDF preview
   - Image preview
   - Document preview
   - Video preview

---

### Security Considerations

#### File Security
- File type validation
- Virus scanning
- File encryption
- Access control

#### Data Protection
- Secure file storage
- Encrypted transmission
- Audit logging
- Backup procedures

---

### Testing Strategy

#### Unit Tests
- File upload validation
- File type checking
- Size limit enforcement
- Permission validation

#### Integration Tests
- Storage integration
- File processing
- Preview generation
- Download functionality

#### User Acceptance Tests
- Upload workflow
- File management
- Search functionality
- Preview capabilities

---

### Deployment & Configuration

#### Environment Setup
- Storage configuration
- File processing setup
- Security configuration
- Backup procedures

#### Monitoring & Logging
- Upload monitoring
- Storage usage tracking
- Performance monitoring
- Error logging

---

### Documentation

#### User Manual
- Upload procedures
- File management
- Search and filter
- Preview usage

#### Technical Documentation
- API documentation
- Storage configuration
- Security implementation
- Integration guides 