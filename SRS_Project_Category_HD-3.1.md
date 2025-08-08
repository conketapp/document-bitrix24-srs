# Software Requirements Specification (SRS)
## Epic: Hợp đồng - Quản lý Hợp đồng

### User Story: HD-3.1
### Đính kèm Tài liệu Hợp đồng và Phụ lục

#### Thông tin User Story
- **Story ID:** HD-3.1
- **Priority:** High
- **Story Points:** 6
- **Sprint:** Sprint 3
- **Status:** To Do
- **Phụ thuộc:** HD-1.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách hợp đồng,  
**Tôi muốn** có thể đính kèm các file tài liệu trực tiếp vào hồ sơ hợp đồng (ví dụ: bản scan hợp đồng gốc, các phụ lục hợp đồng, các quyết định liên quan),  
**Để** tôi có thể lưu trữ tập trung các văn bản gốc và dễ dàng truy xuất khi cần kiểm tra hoặc đối chiếu.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có khu vực tải lên tệp đính kèm trong hồ sơ hợp đồng
- [ ] Hỗ trợ các định dạng file phổ biến (PDF, DOCX, XLSX)
- [ ] Có thể tải lên nhiều file cùng lúc
- [ ] Hiển thị danh sách tài liệu đã đính kèm với thông tin chi tiết
- [ ] Có thể xem trước (preview) tài liệu trực tiếp trên hệ thống
- [ ] Có thể tải xuống tài liệu đã đính kèm
- [ ] Có thể phân loại tài liệu theo loại (hợp đồng gốc, phụ lục, quyết định, v.v.)
- [ ] Có thể thêm mô tả cho từng tài liệu
- [ ] Có thể xóa tài liệu đã đính kèm (với quyền phù hợp)
- [ ] Hệ thống kiểm tra virus và bảo mật cho file upload
- [ ] Có thể tìm kiếm tài liệu theo tên, loại, ngày tải lên
- [ ] Hỗ trợ version control cho tài liệu (cập nhật tài liệu mới)

#### Activity Diagram
![HD-3.1 Activity Diagram](diagrams/HD-3.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý đính kèm và quản lý tài liệu hợp đồng*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Hệ thống Upload File**
   - Giao diện upload kéo thả
   - Chọn nhiều file
   - Chỉ báo tiến trình
   - Xác thực kích thước file
   - Xác thực loại file

2. **Quản lý Tài liệu**
   - Phân loại tài liệu
   - Quản lý metadata
   - Kiểm soát phiên bản
   - Tìm kiếm và lọc
   - Chức năng xem trước

3. **Bảo mật và Xác thực**
   - Quét virus
   - Kiểm tra tính toàn vẹn file
   - Kiểm soát truy cập
   - Ghi log kiểm toán
   - Mã hóa

4. **Tổ chức Tài liệu**
   - Cấu trúc thư mục
   - Hệ thống gắn thẻ
   - Mối quan hệ tài liệu
   - Thao tác hàng loạt
   - Quản lý lưu trữ

#### Quy tắc Kinh doanh
- Giới hạn kích thước file: 50MB mỗi file
- Định dạng hỗ trợ: PDF, DOCX, XLSX, JPG, PNG, TIFF
- Quét virus bắt buộc cho tất cả uploads
- Backup tự động cho tài liệu quan trọng
- Chính sách lưu trữ: 10 năm cho tài liệu hợp đồng
- Kiểm soát truy cập theo vai trò và quyền sở hữu hợp đồng

#### Phân loại Tài liệu
1. **Tài liệu Hợp đồng**
   - Hợp đồng gốc
   - Hợp đồng đã ký
   - Phụ lục hợp đồng
   - Thay đổi hợp đồng

2. **Tài liệu Hỗ trợ**
   - Tài liệu đấu thầu
   - Đặc tả kỹ thuật
   - Tài liệu tài chính
   - Tài liệu pháp lý

3. **Tài liệu Phê duyệt**
   - Quyết định phê duyệt
   - Thư ủy quyền
   - Nghị quyết hội đồng
   - Phê duyệt quản lý

4. **Tài liệu Vận hành**
   - Báo cáo tiến độ
   - Biên bản nghiệm thu
   - Chứng từ thanh toán
   - Chứng nhận hoàn thành

5. **Tài liệu Giao tiếp**
   - Thư từ trao đổi
   - Biên bản họp
   - Thông báo
   - Khiếu nại

---

#### 5.5 Sequence Diagram
![HD-3.1 Sequence Diagram](diagrams/HD-3.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi quản lý tài liệu hợp đồng*

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng tài liệu hợp đồng
CREATE TABLE contract_documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    document_category ENUM('contract', 'supporting', 'approval', 'operational', 'communication') NOT NULL,
    document_subcategory VARCHAR(100),
    description TEXT,
    version_number INT DEFAULT 1,
    is_latest_version BOOLEAN DEFAULT TRUE,
    is_public BOOLEAN DEFAULT FALSE,
    is_encrypted BOOLEAN DEFAULT TRUE,
    checksum VARCHAR(64) NOT NULL,
    virus_scan_status ENUM('pending', 'clean', 'infected', 'error') DEFAULT 'pending',
    virus_scan_result TEXT,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    INDEX idx_contract_category (contract_id, document_category),
    INDEX idx_uploaded_at (uploaded_at),
    INDEX idx_virus_scan_status (virus_scan_status)
);

-- Bảng phiên bản tài liệu
CREATE TABLE document_versions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document_id INT NOT NULL,
    version_number INT NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    change_description TEXT,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES contract_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    UNIQUE KEY unique_document_version (document_id, version_number)
);

-- Bảng quyền truy cập tài liệu
CREATE TABLE document_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document_id INT NOT NULL,
    role_id INT NOT NULL,
    can_view BOOLEAN DEFAULT TRUE,
    can_download BOOLEAN DEFAULT TRUE,
    can_upload BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE,
    can_update BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES contract_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_document_role (document_id, role_id)
);

-- Bảng lịch sử truy cập tài liệu
CREATE TABLE document_access_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document_id INT NOT NULL,
    user_id INT NOT NULL,
    action_type ENUM('view', 'download', 'upload', 'delete', 'update') NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES contract_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_document_action (document_id, action_type),
    INDEX idx_accessed_at (accessed_at)
);

-- Bảng cấu hình tài liệu
CREATE TABLE document_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng thẻ tài liệu
CREATE TABLE document_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document_id INT NOT NULL,
    tag_name VARCHAR(100) NOT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES contract_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE KEY unique_document_tag (document_id, tag_name)
);

-- Insert default document configuration
INSERT INTO document_config (config_key, config_value, description) VALUES
('max_file_size_mb', '50', 'Maximum file size in MB'),
('allowed_file_types', 'pdf,docx,xlsx,jpg,png,tiff', 'Allowed file extensions'),
('virus_scan_enabled', 'true', 'Enable virus scanning for uploads'),
('encryption_enabled', 'true', 'Enable file encryption'),
('retention_years', '10', 'Document retention period in years'),
('backup_enabled', 'true', 'Enable automatic backup'),
('preview_enabled', 'true', 'Enable document preview'),
('watermark_enabled', 'true', 'Enable watermark for sensitive documents');

-- Insert default document permissions
INSERT INTO document_permissions (document_id, role_id, can_view, can_download, can_upload, can_delete, can_update) VALUES
-- Contract Manager - full access
(1, 1, TRUE, TRUE, TRUE, TRUE, TRUE),
-- Contract Supervisor - limited access
(1, 2, TRUE, TRUE, TRUE, FALSE, TRUE),
-- Contract Officer - view and download only
(1, 3, TRUE, TRUE, FALSE, FALSE, FALSE);
```

#### API Endpoints
```
# Document Upload
POST /api/contracts/{id}/documents/upload
Content-Type: multipart/form-data
{
  "files": [File1, File2, ...],
  "category": "contract",
  "subcategory": "original",
  "description": "Original contract document",
  "tags": ["important", "signed"]
}

# Document Management
GET /api/contracts/{id}/documents
GET /api/contracts/{id}/documents/{document_id}
PUT /api/contracts/{id}/documents/{document_id}
DELETE /api/contracts/{id}/documents/{document_id}

# Document Download
GET /api/contracts/{id}/documents/{document_id}/download
GET /api/contracts/{id}/documents/{document_id}/preview

# Document Search
GET /api/contracts/{id}/documents/search
{
  "query": "contract",
  "category": "contract",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "tags": ["important"]
}

# Document Versioning
GET /api/contracts/{id}/documents/{document_id}/versions
POST /api/contracts/{id}/documents/{document_id}/versions
{
  "file": File,
  "change_description": "Updated contract terms"
}

# Document Permissions
GET /api/contracts/{id}/documents/{document_id}/permissions
PUT /api/contracts/{id}/documents/{document_id}/permissions
{
  "role_id": 1,
  "can_view": true,
  "can_download": true,
  "can_upload": false,
  "can_delete": false,
  "can_update": false
}

# Document Tags
GET /api/contracts/{id}/documents/{document_id}/tags
POST /api/contracts/{id}/documents/{document_id}/tags
{
  "tags": ["important", "signed", "approved"]
}

# Bulk Operations
POST /api/contracts/{id}/documents/bulk-upload
POST /api/contracts/{id}/documents/bulk-delete
POST /api/contracts/{id}/documents/bulk-download

# Document Statistics
GET /api/contracts/{id}/documents/stats
Response: {
  "total_documents": 15,
  "total_size_mb": 245.6,
  "by_category": {
    "contract": 5,
    "supporting": 8,
    "approval": 2
  },
  "by_type": {
    "pdf": 10,
    "docx": 3,
    "xlsx": 2
  }
}
```

#### Frontend Components
```typescript
// Document Upload Component
interface DocumentUploadComponent {
  contractId: number
  isUploading: boolean
  uploadProgress: number
  allowedFileTypes: string[]
  maxFileSize: number
  
  onFileSelect: (files: File[]) => void
  onUpload: (files: File[], metadata: DocumentMetadata) => Promise<void>
  onCancel: () => void
}

// Document List Component
interface DocumentListComponent {
  documents: ContractDocument[]
  isLoading: boolean
  filters: DocumentFilters
  
  onViewDocument: (documentId: number) => void
  onDownloadDocument: (documentId: number) => void
  onDeleteDocument: (documentId: number) => Promise<void>
  onUpdateDocument: (documentId: number, updates: Partial<ContractDocument>) => Promise<void>
  onFilterChange: (filters: DocumentFilters) => void
}

// Document Preview Component
interface DocumentPreviewComponent {
  document: ContractDocument
  isOpen: boolean
  
  onClose: () => void
  onDownload: () => void
  onPrint: () => void
  onShare: () => void
}

// Document Search Component
interface DocumentSearchComponent {
  searchQuery: string
  searchResults: ContractDocument[]
  isSearching: boolean
  
  onSearch: (query: string, filters: SearchFilters) => Promise<void>
  onClearSearch: () => void
  onSelectResult: (document: ContractDocument) => void
}

// Document Version Component
interface DocumentVersionComponent {
  document: ContractDocument
  versions: DocumentVersion[]
  
  onViewVersion: (versionNumber: number) => void
  onRestoreVersion: (versionNumber: number) => Promise<void>
  onCompareVersions: (version1: number, version2: number) => void
}

// Document Permission Component
interface DocumentPermissionComponent {
  document: ContractDocument
  permissions: DocumentPermission[]
  availableRoles: UserRole[]
  
  onUpdatePermission: (roleId: number, permissions: Partial<DocumentPermission>) => Promise<void>
  onAddPermission: (roleId: number, permissions: DocumentPermission) => Promise<void>
  onRemovePermission: (roleId: number) => Promise<void>
}

// Document Tag Component
interface DocumentTagComponent {
  document: ContractDocument
  tags: string[]
  availableTags: string[]
  
  onAddTag: (tag: string) => Promise<void>
  onRemoveTag: (tag: string) => Promise<void>
  onCreateTag: (tag: string) => Promise<void>
}

// Document Statistics Component
interface DocumentStatisticsComponent {
  contractId: number
  statistics: DocumentStatistics
  
  onExportStatistics: () => void
  onViewCategoryDetails: (category: string) => void
}

// Document Bulk Operations Component
interface DocumentBulkOperationsComponent {
  selectedDocuments: ContractDocument[]
  
  onBulkDownload: () => Promise<void>
  onBulkDelete: () => Promise<void>
  onBulkUpdate: (updates: Partial<ContractDocument>) => Promise<void>
  onSelectAll: () => void
  onDeselectAll: () => void
}
```

---

### UI/UX Design

#### Upload Interface
- **Drag & Drop Zone:**
  - Visual drop zone với border dashed
  - File type icons
  - Progress bars cho uploads
  - Error messages cho invalid files

#### Document List
- **Document Grid:**
  - Thumbnail previews
  - File type icons
  - Metadata display (size, date, category)
  - Action buttons (view, download, delete)

#### Document Preview
- **Preview Modal:**
  - Full-screen preview
  - Zoom controls
  - Page navigation
  - Download/print buttons

#### Search Interface
- **Search Bar:**
  - Auto-complete suggestions
  - Filter options
  - Search history
  - Advanced search

---

### Integration Requirements

#### File Storage Integration
1. **Storage System**
   - Secure file storage
   - Backup system
   - CDN integration
   - Encryption at rest

2. **Virus Scanning**
   - Real-time scanning
   - Quarantine infected files
   - Scan reports
   - Clean file processing

#### Document Processing
1. **File Processing**
   - Thumbnail generation
   - Metadata extraction
   - Text extraction (OCR)
   - Format conversion

2. **Preview Generation**
   - PDF preview
   - Image preview
   - Document conversion
   - Watermarking

---

### Security Considerations

#### File Security
- Encrypted file storage
- Secure file transfer
- Access control
- Audit logging

#### Virus Protection
- Real-time virus scanning
- File integrity checks
- Quarantine system
- Clean file processing

#### Access Control
- Role-based permissions
- Document-level security
- Time-based access
- IP restrictions

---

### Testing Strategy

#### Unit Tests
- File upload validation
- Virus scanning logic
- Permission checking
- Document processing

#### Integration Tests
- End-to-end upload workflow
- File storage integration
- Preview generation
- Search functionality

#### User Acceptance Tests
- Upload interface usability
- Document management workflow
- Search and filter testing
- Preview functionality testing

---

### Deployment & Configuration

#### Environment Setup
- File storage configuration
- Virus scanning setup
- Backup system configuration
- CDN integration

#### Monitoring & Logging
- Upload activity monitoring
- Storage usage tracking
- Virus scan monitoring
- Performance monitoring

---

### Documentation

#### User Manual
- Upload interface guide
- Document management procedures
- Search and filter instructions
- Preview functionality guide

#### Technical Documentation
- API documentation
- Storage architecture
- Security implementation
- Performance optimization 