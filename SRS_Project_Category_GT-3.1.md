# Software Requirements Specification (SRS)
## Epic: Gói thầu - Quản lý Gói thầu

### User Story: GT-3.1
### Đính kèm Tài liệu liên quan đến Gói thầu

#### Thông tin User Story
- **Story ID:** GT-3.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 3
- **Status:** To Do
- **Dependencies:** GT-1.1, GT-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách gói thầu,  
**Tôi muốn** có thể đính kèm các file tài liệu trực tiếp vào hồ sơ gói thầu (ví dụ: các quyết định phê duyệt liên quan),  
**Để** tôi có thể lưu trữ tập trung các văn bản gốc và dễ dàng truy xuất khi cần kiểm tra.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có khu vực tải lên tệp đính kèm trong hồ sơ gói thầu
- [ ] Hỗ trợ các định dạng file phổ biến (PDF, DOCX, XLSX)
- [ ] Có thể xem trước và tải xuống tài liệu đã đính kèm
- [ ] Có thể phân loại tài liệu theo loại (quyết định phê duyệt, hồ sơ mời thầu, v.v.)
- [ ] Có thể thêm mô tả cho từng tài liệu
- [ ] Hỗ trợ tải lên nhiều file cùng lúc
- [ ] Có thể xóa hoặc thay thế tài liệu đã đính kèm
- [ ] Hiển thị thông tin về kích thước file và ngày tải lên
- [ ] Có thể tìm kiếm và lọc tài liệu theo loại hoặc tên

#### 2.4 Activity Diagram
![GT-3.1 Activity Diagram](diagrams/GT-3.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý đính kèm tài liệu liên quan đến gói thầu*

---

### Functional Requirements

#### Core Features
1. **File Upload System**
   - Drag & drop file upload
   - Multiple file selection
   - Progress indicator
   - File validation và virus scanning
   - Automatic file naming

2. **Document Management**
   - Document categorization
   - Metadata management
   - Version control
   - Document preview
   - Download functionality

3. **File Type Support**
   - PDF documents
   - Microsoft Office documents (DOCX, XLSX, PPTX)
   - Image files (JPG, PNG, TIFF)
   - Text files (TXT, RTF)
   - Archive files (ZIP, RAR)

4. **Document Organization**
   - Folder structure
   - Tagging system
   - Search và filter
   - Bulk operations

#### Business Rules
- File size limit: 50MB per file
- Total storage limit: 1GB per tender package
- Supported file types: PDF, DOCX, XLSX, PPTX, JPG, PNG, TXT
- Virus scanning required cho tất cả uploaded files
- Automatic backup cho uploaded documents
- Version control cho document updates

#### Document Categories
1. **Approval Documents**
   - Quyết định phê duyệt HSMT
   - Quyết định phê duyệt KQLCNT
   - Quyết định phê duyệt giá
   - Quyết định phê duyệt nhà thầu

2. **Tender Documents**
   - Hồ sơ mời thầu
   - Hồ sơ dự thầu
   - Báo cáo đánh giá
   - Biên bản mở thầu

3. **Contract Documents**
   - Hợp đồng
   - Phụ lục hợp đồng
   - Biên bản nghiệm thu
   - Thanh lý hợp đồng

4. **Other Documents**
   - Báo cáo tiến độ
   - Biên bản họp
   - Tài liệu kỹ thuật
   - Văn bản khác

---

### Technical Specifications

#### Sequence Diagram
![GT-3.1 Sequence Diagram](diagrams/GT-3.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi đính kèm tài liệu liên quan đến gói thầu*

#### Database Schema Updates
```sql
-- Bảng quản lý tài liệu đính kèm
CREATE TABLE tender_documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tender_package_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    document_category ENUM('approval', 'tender', 'contract', 'other') NOT NULL,
    document_type VARCHAR(100),
    description TEXT,
    tags JSON,
    version INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tender_package_id) REFERENCES tender_packages(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Bảng lịch sử tài liệu
CREATE TABLE document_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    document_id INT NOT NULL,
    action_type ENUM('upload', 'update', 'delete', 'download', 'preview') NOT NULL,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_file_path VARCHAR(500),
    new_file_path VARCHAR(500),
    notes TEXT,
    
    FOREIGN KEY (document_id) REFERENCES tender_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id)
);

-- Bảng cấu hình loại tài liệu
CREATE TABLE document_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    category_code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_required BOOLEAN DEFAULT FALSE,
    max_files INT DEFAULT 10,
    allowed_file_types JSON,
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng quyền truy cập tài liệu
CREATE TABLE document_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    document_category VARCHAR(50) NOT NULL,
    can_upload BOOLEAN DEFAULT TRUE,
    can_download BOOLEAN DEFAULT TRUE,
    can_delete BOOLEAN DEFAULT FALSE,
    can_preview BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_category (role_id, document_category)
);

-- Insert default document categories
INSERT INTO document_categories (category_name, category_code, description, is_required, allowed_file_types) VALUES
('Quyết định phê duyệt', 'approval_decisions', 'Các quyết định phê duyệt liên quan đến gói thầu', TRUE, '["pdf", "docx"]'),
('Hồ sơ mời thầu', 'tender_documents', 'Hồ sơ mời thầu và tài liệu liên quan', TRUE, '["pdf", "docx", "xlsx"]'),
('Hợp đồng', 'contract_documents', 'Hợp đồng và phụ lục', TRUE, '["pdf", "docx"]'),
('Báo cáo đánh giá', 'evaluation_reports', 'Báo cáo đánh giá nhà thầu', FALSE, '["pdf", "docx", "xlsx"]'),
('Biên bản', 'meeting_minutes', 'Biên bản họp và mở thầu', FALSE, '["pdf", "docx"]'),
('Tài liệu khác', 'other_documents', 'Các tài liệu khác', FALSE, '["pdf", "docx", "xlsx", "jpg", "png"]');

-- Insert default document permissions
INSERT INTO document_permissions (role_id, document_category, can_upload, can_download, can_delete, can_preview) VALUES
-- System Administrator - full access
(1, 'approval_decisions', TRUE, TRUE, TRUE, TRUE),
(1, 'tender_documents', TRUE, TRUE, TRUE, TRUE),
(1, 'contract_documents', TRUE, TRUE, TRUE, TRUE),
(1, 'evaluation_reports', TRUE, TRUE, TRUE, TRUE),
(1, 'meeting_minutes', TRUE, TRUE, TRUE, TRUE),
(1, 'other_documents', TRUE, TRUE, TRUE, TRUE),

-- Category Manager - limited access
(2, 'approval_decisions', TRUE, TRUE, FALSE, TRUE),
(2, 'tender_documents', TRUE, TRUE, FALSE, TRUE),
(2, 'contract_documents', TRUE, TRUE, FALSE, TRUE),
(2, 'evaluation_reports', TRUE, TRUE, FALSE, TRUE),
(2, 'meeting_minutes', TRUE, TRUE, FALSE, TRUE),
(2, 'other_documents', TRUE, TRUE, FALSE, TRUE),

-- Project Manager - project-level access
(3, 'approval_decisions', TRUE, TRUE, FALSE, TRUE),
(3, 'tender_documents', TRUE, TRUE, FALSE, TRUE),
(3, 'contract_documents', TRUE, TRUE, FALSE, TRUE),
(3, 'evaluation_reports', TRUE, TRUE, FALSE, TRUE),
(3, 'meeting_minutes', TRUE, TRUE, FALSE, TRUE),
(3, 'other_documents', TRUE, TRUE, FALSE, TRUE);
```

#### API Endpoints
```
# Document Management
GET /api/tender-packages/{id}/documents
POST /api/tender-packages/{id}/documents/upload
GET /api/tender-packages/{id}/documents/{document_id}
PUT /api/tender-packages/{id}/documents/{document_id}
DELETE /api/tender-packages/{id}/documents/{document_id}

# File Upload
POST /api/documents/upload
{
  "tender_package_id": 123,
  "category": "approval_decisions",
  "description": "Quyết định phê duyệt HSMT",
  "tags": ["phê duyệt", "HSMT"]
}

# Document Download
GET /api/documents/{document_id}/download
GET /api/documents/{document_id}/preview

# Document Categories
GET /api/document-categories
GET /api/document-categories/{category_id}

# Document Search
GET /api/tender-packages/{id}/documents/search
{
  "query": "phê duyệt",
  "category": "approval_decisions",
  "file_type": "pdf"
}

# Bulk Operations
POST /api/tender-packages/{id}/documents/bulk-upload
POST /api/tender-packages/{id}/documents/bulk-delete
```

#### Frontend Components
```typescript
// Document Upload Component
interface DocumentUploadComponent {
  tenderPackageId: number
  allowedCategories: DocumentCategory[]
  maxFileSize: number
  maxFiles: number
  onUpload: (files: File[], category: string, description: string) => Promise<void>
  onUploadProgress: (progress: number) => void
  onUploadError: (error: string) => void
}

// Document List Component
interface DocumentListComponent {
  documents: TenderDocument[]
  categories: DocumentCategory[]
  onViewDocument: (documentId: number) => void
  onDownloadDocument: (documentId: number) => void
  onDeleteDocument: (documentId: number) => void
  onEditDocument: (documentId: number, updates: Partial<TenderDocument>) => Promise<void>
}

// Document Preview Component
interface DocumentPreviewComponent {
  document: TenderDocument
  isVisible: boolean
  onClose: () => void
  onDownload: () => void
  onEdit: () => void
}

// Document Search Component
interface DocumentSearchComponent {
  documents: TenderDocument[]
  searchQuery: string
  selectedCategory: string
  selectedFileType: string
  onSearch: (query: string, filters: SearchFilters) => void
  onClearSearch: () => void
}

// Document Category Selector
interface DocumentCategorySelector {
  categories: DocumentCategory[]
  selectedCategory: string
  onCategoryChange: (category: string) => void
  onAddCategory: (category: DocumentCategory) => void
}

// File Upload Progress
interface FileUploadProgress {
  fileName: string
  progress: number
  status: 'uploading' | 'completed' | 'error'
  errorMessage?: string
}
```

---

### UI/UX Design

#### Document Upload Area
- **Layout:** Drag & drop zone với file list
- **Components:**
  - Upload zone với visual feedback
  - File list với progress indicators
  - Category selector dropdown
  - Description input field
  - Upload button với progress

#### Document Management Interface
- **Layout:** Grid/list view với filters
- **Components:**
  - Document cards với thumbnails
  - Category filters
  - Search bar
  - Bulk action buttons
  - Sort options

#### Document Preview
- **Layout:** Modal với document viewer
- **Components:**
  - PDF viewer cho PDF files
  - Image viewer cho image files
  - Download button
  - Edit metadata button
  - Share button

#### File Type Icons
- **Visual Indicators:**
  - PDF icon cho PDF files
  - Word icon cho DOCX files
  - Excel icon cho XLSX files
  - Image icon cho image files
  - Generic file icon cho other types

---

### Integration Requirements

#### File Storage Integration
1. **Local Storage**
   - Secure file storage
   - File organization
   - Backup và recovery
   - Access control

2. **Cloud Storage (Optional)**
   - AWS S3 integration
   - Google Cloud Storage
   - Azure Blob Storage
   - CDN integration

#### Security Integration
1. **Virus Scanning**
   - Real-time virus scanning
   - Quarantine infected files
   - Scan reports
   - Clean file validation

2. **Access Control**
   - Role-based permissions
   - Document-level permissions
   - Download restrictions
   - Audit logging

---

### Security Considerations

#### File Security
- Virus scanning cho tất cả uploads
- File type validation
- Size limit enforcement
- Secure file storage
- Access control

#### Data Protection
- Encrypt sensitive documents
- Secure transmission
- Backup và recovery
- Audit trail

#### Access Control
- Role-based document access
- Category-based permissions
- Download restrictions
- Preview permissions

---

### Testing Strategy

#### Unit Tests
- File upload validation
- Document management logic
- Permission checking
- Search functionality

#### Integration Tests
- End-to-end upload workflow
- Document preview testing
- Bulk operations testing
- Security testing

#### User Acceptance Tests
- Upload interface usability
- Document management workflow
- Search và filter experience
- Preview functionality

---

### Deployment & Configuration

#### Environment Setup
- File storage configuration
- Virus scanning setup
- Permission configuration
- Backup setup

#### Monitoring & Logging
- Upload activity monitoring
- Storage usage tracking
- Security event logging
- Performance monitoring

---

### Documentation

#### User Manual
- Document upload guide
- Document management procedures
- Search và filter instructions
- Security best practices

#### Technical Documentation
- API documentation
- Storage configuration
- Security implementation
- Performance optimization

---

### Validation Table

#### **Bảng Validation Form Upload Tài liệu**

##### **Thông tin File Upload**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| File tài liệu | document_file | FILE | PDF, DOC, DOCX, XLS, XLSX, JPG, PNG | ✅ | File tài liệu |
| Tên tài liệu | document_name | VARCHAR(200) | 3-200 ký tự | ✅ | Tên hiển thị tài liệu |
| Loại tài liệu | document_type | ENUM | 'hsmt', 'tbmt', 'contract', 'report', 'other' | ✅ | Phân loại tài liệu |
| Mô tả | document_description | TEXT | Tối đa 500 ký tự | ❌ | Mô tả tài liệu |
| Phiên bản | document_version | VARCHAR(20) | Format: v1.0, v2.1 | ❌ | Phiên bản tài liệu |

##### **Thông tin Metadata**

| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc | Mô tả |
|--------|-----------|---------------|------------|----------|-------|
| Kích thước file | file_size | BIGINT | <= 50MB | ✅ | Kích thước file |
| Định dạng file | file_extension | VARCHAR(10) | Các định dạng cho phép | ✅ | Định dạng file |
| Checksum | file_checksum | VARCHAR(64) | SHA-256 hash | ✅ | Checksum file |
| Ngày upload | upload_date | TIMESTAMP | Tự động | ✅ | Thời gian upload |

#### **Quy tắc Validation Upload**

##### **Validation File**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| File size | Kích thước hợp lệ | <= 50MB | "File quá lớn, tối đa 50MB" |
| File type | Định dạng cho phép | PDF, DOC, DOCX, XLS, XLSX, JPG, PNG | "Định dạng file không được hỗ trợ" |
| File content | Nội dung hợp lệ | Không chứa virus | "File có thể chứa nội dung độc hại" |
| File name | Tên hợp lệ | Không chứa ký tự đặc biệt | "Tên file chứa ký tự không hợp lệ" |

##### **Validation Business Rules**

| Quy tắc | Điều kiện | Validation | Thông báo lỗi |
|---------|-----------|------------|---------------|
| Document type | Loại tài liệu | Theo quy định | "Loại tài liệu không hợp lệ" |
| Version format | Định dạng phiên bản | vX.Y format | "Định dạng phiên bản không hợp lệ" |
| Duplicate check | Trùng lặp tên | Kiểm tra trong database | "Tên tài liệu đã tồn tại" | 