# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-1.1
### Tạo mới một Tài sản/Dịch vụ đầu ra từ dự án

#### Thông tin User Story
- **Story ID:** TSDV-1.1
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 1
- **Status:** To Do
- **Dependencies:** None

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án hoặc Cán bộ quản lý tài sản/dịch vụ,  
**Tôi muốn** có thể tạo mới một khoản mục Tài sản hoặc Dịch vụ được hình thành hoặc là sản phẩm đầu ra từ một dự án đã hoàn thành hoặc đang triển khai  
**Để** tôi có thể ghi nhận và quản lý các sản phẩm hữu hình (thiết bị phần cứng, phần mềm) hoặc vô hình (dịch vụ) mà dự án tạo ra.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có một form nhập liệu cho phép chọn Loại là "Tài sản" hoặc "Dịch vụ"
- [ ] Các trường nhập liệu thay đổi linh hoạt tùy thuộc vào lựa chọn "Loại"
- [ ] Mã Tài sản/Dịch vụ được sinh tự động theo quy tắc định sẵn
- [ ] Thông tin bắt buộc phải được đánh dấu và hệ thống kiểm tra tính hợp lệ trước khi lưu
- [ ] Có thể chọn dự án nguồn từ danh sách dự án có sẵn
- [ ] Có thể đính kèm tài liệu liên quan đến tài sản/dịch vụ
- [ ] Có thể gán người phụ trách cho tài sản/dịch vụ
- [ ] Có thể thiết lập trạng thái ban đầu cho tài sản/dịch vụ
- [ ] Có thể lưu bản nháp và hoàn thiện sau
- [ ] Có thể xem preview trước khi lưu chính thức
- [ ] Có thể tạo nhiều tài sản/dịch vụ cùng lúc từ một dự án
- [ ] Có thể import danh sách tài sản/dịch vụ từ file Excel

#### 2.4 Activity Diagram
![TSDV-1.1 Activity Diagram](diagrams/TSDV-1.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tạo mới Tài sản/Dịch vụ*

#### 2.5 Sequence Diagram
![TSDV-1.1 Sequence Diagram](diagrams/TSDV-1.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi tạo mới Tài sản/Dịch vụ*

---

### Functional Requirements

#### Core Features
1. **Asset/Service Creation**
   - Dynamic form based on type
   - Auto-generated codes
   - Project association
   - Validation rules

2. **Form Management**
   - Type selection (Asset/Service)
   - Dynamic field display
   - Required field validation
   - Data validation

3. **Code Generation**
   - Automatic code generation
   - Customizable rules
   - Unique code validation
   - Code format configuration

4. **Project Integration**
   - Project selection
   - Project validation
   - Project status check
   - Project association

#### Business Rules
- Mã tài sản/dịch vụ phải duy nhất trong hệ thống
- Chỉ có thể tạo tài sản/dịch vụ từ dự án đang triển khai hoặc đã hoàn thành
- Thông tin bắt buộc phải được nhập đầy đủ trước khi lưu
- Người tạo phải có quyền truy cập vào dự án nguồn
- Tài sản/dịch vụ phải được gán người phụ trách

#### Asset Types
1. **Hardware Assets**: Computer equipment, network devices, office equipment, industrial equipment
2. **Software Assets**: Custom software, licensed software, open source software, cloud services
3. **Infrastructure Assets**: Buildings, facilities, systems, networks

#### Service Types
1. **Consulting Services**: Technical consulting, business consulting, training services, support services
2. **Development Services**: Software development, system integration, custom development, maintenance services
3. **Operational Services**: Managed services, outsourced services, professional services, support services

#### Form Fields by Type
1. **Asset Fields**: Asset name, category, model/specifications, serial number, purchase date, purchase cost, warranty information, location, status
2. **Service Fields**: Service name, category, description, service level agreement, start date, end date, service cost, service provider, status
3. **Common Fields**: Asset/Service code, name, description, category, project association, responsible person, status

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng tài sản và dịch vụ
CREATE TABLE assets_services (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    type ENUM('asset', 'service') NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    
    -- Thông tin dự án
    source_project_id INT NOT NULL,
    project_phase VARCHAR(100),
    creation_date DATE NOT NULL,
    completion_date DATE,
    
    -- Thông tin người phụ trách
    responsible_person_id INT NOT NULL,
    assigned_by INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Trạng thái
    status ENUM('draft', 'active', 'inactive', 'maintenance', 'retired', 'disposed') DEFAULT 'draft',
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    
    -- Metadata
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (source_project_id) REFERENCES projects(id),
    FOREIGN KEY (responsible_person_id) REFERENCES users(id),
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    INDEX idx_asset_service_code (asset_service_code),
    INDEX idx_type (type),
    INDEX idx_category (category),
    INDEX idx_source_project_id (source_project_id),
    INDEX idx_status (status),
    INDEX idx_responsible_person_id (responsible_person_id)
);

-- Bảng thông tin chi tiết tài sản
CREATE TABLE asset_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_id INT NOT NULL,
    
    -- Thông tin kỹ thuật
    model VARCHAR(200),
    specifications TEXT,
    serial_number VARCHAR(100),
    manufacturer VARCHAR(200),
    supplier VARCHAR(200),
    
    -- Thông tin tài chính
    purchase_date DATE,
    purchase_cost DECIMAL(15,2),
    current_value DECIMAL(15,2),
    depreciation_rate DECIMAL(5,2),
    
    -- Thông tin bảo hành
    warranty_start_date DATE,
    warranty_end_date DATE,
    warranty_terms TEXT,
    
    -- Thông tin vị trí
    location VARCHAR(200),
    building VARCHAR(100),
    floor VARCHAR(50),
    room VARCHAR(50),
    
    -- Thông tin bảo trì
    maintenance_schedule TEXT,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    
    FOREIGN KEY (asset_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    INDEX idx_asset_id (asset_id),
    INDEX idx_serial_number (serial_number),
    INDEX idx_location (location)
);

-- Bảng thông tin chi tiết dịch vụ
CREATE TABLE service_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    service_id INT NOT NULL,
    
    -- Thông tin dịch vụ
    service_level_agreement TEXT,
    service_provider VARCHAR(200),
    service_contact VARCHAR(200),
    service_phone VARCHAR(50),
    service_email VARCHAR(200),
    
    -- Thông tin thời gian
    start_date DATE,
    end_date DATE,
    renewal_date DATE,
    contract_period VARCHAR(100),
    
    -- Thông tin tài chính
    service_cost DECIMAL(15,2),
    billing_frequency ENUM('monthly', 'quarterly', 'annually', 'one_time'),
    payment_terms TEXT,
    
    -- Thông tin hiệu suất
    performance_metrics TEXT,
    uptime_requirement DECIMAL(5,2),
    response_time_requirement VARCHAR(100),
    
    FOREIGN KEY (service_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    INDEX idx_service_id (service_id),
    INDEX idx_service_provider (service_provider),
    INDEX idx_start_date (start_date),
    INDEX idx_end_date (end_date)
);

-- Bảng tài liệu đính kèm
CREATE TABLE asset_service_attachments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    asset_service_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    file_type VARCHAR(100),
    description TEXT,
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (asset_service_id) REFERENCES assets_services(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    INDEX idx_asset_service_id (asset_service_id),
    INDEX idx_file_type (file_type)
);

-- Bảng cấu hình mã tự động
CREATE TABLE asset_service_code_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code_type ENUM('asset', 'service') NOT NULL,
    prefix VARCHAR(10) NOT NULL,
    sequence_format VARCHAR(20) NOT NULL,
    current_sequence INT DEFAULT 1,
    year_format VARCHAR(4),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_code_type (code_type),
    INDEX idx_is_active (is_active)
);

-- Insert default code configurations
INSERT INTO asset_service_code_config (code_type, prefix, sequence_format, year_format) VALUES
('asset', 'TS', '000000', 'YYYY'),
('service', 'DV', '000000', 'YYYY');
```

#### API Endpoints
```typescript
# Create New Asset/Service
POST /api/assets-services/create
{
  "type": "asset",
  "name": "Máy chủ Dell PowerEdge R740",
  "description": "Máy chủ vật lý cho hệ thống ERP",
  "category": "Hardware",
  "subcategory": "Server",
  "source_project_id": 123,
  "project_phase": "Implementation",
  "responsible_person_id": 456,
  "status": "draft",
  "priority": "high",
  "asset_details": {
    "model": "PowerEdge R740",
    "specifications": "Intel Xeon, 32GB RAM, 2TB SSD",
    "serial_number": "DELL123456789",
    "manufacturer": "Dell Technologies",
    "supplier": "Dell Vietnam",
    "purchase_date": "2024-01-15",
    "purchase_cost": 45000000,
    "location": "Data Center A",
    "building": "Building 1",
    "floor": "2",
    "room": "DC-201"
  }
}
Response: {
  "success": true,
  "asset_service_id": 789,
  "asset_service_code": "TS2024000001",
  "message": "Tài sản đã được tạo thành công"
}

# Get Asset/Service Form Configuration
GET /api/assets-services/form-config
{
  "type": "asset"
}
Response: {
  "type": "asset",
  "fields": [
    {
      "name": "name",
      "label": "Tên tài sản",
      "type": "text",
      "required": true,
      "validation": "min_length:3,max_length:200"
    },
    {
      "name": "category",
      "label": "Danh mục",
      "type": "select",
      "required": true,
      "options": ["Hardware", "Software", "Infrastructure"]
    },
    {
      "name": "model",
      "label": "Model",
      "type": "text",
      "required": false,
      "validation": "max_length:200"
    },
    {
      "name": "serial_number",
      "label": "Số serial",
      "type": "text",
      "required": false,
      "validation": "unique:asset_details,serial_number"
    },
    {
      "name": "purchase_cost",
      "label": "Giá mua",
      "type": "number",
      "required": false,
      "validation": "min:0"
    }
  ],
  "code_config": {
    "prefix": "TS",
    "format": "YYYY000000",
    "next_sequence": 2
  }
}

# Validate Asset/Service Data
POST /api/assets-services/validate
{
  "type": "asset",
  "data": {
    "name": "Máy chủ Dell PowerEdge R740",
    "category": "Hardware",
    "serial_number": "DELL123456789",
    "purchase_cost": 45000000
  }
}
Response: {
  "valid": true,
  "errors": [],
  "warnings": [
    "Serial number already exists in system"
  ],
  "suggestions": [
    "Consider adding warranty information",
    "Specify location for asset tracking"
  ]
}

# Generate Asset/Service Code
GET /api/assets-services/generate-code
{
  "type": "asset"
}
Response: {
  "code": "TS2024000002",
  "format": "TS + YYYY + 6-digit sequence",
  "next_sequence": 3
}

# Get Available Projects
GET /api/assets-services/available-projects
{
  "status": ["active", "completed"],
  "user_id": 456
}
Response: {
  "projects": [
    {
      "id": 123,
      "name": "Dự án triển khai ERP",
      "status": "active",
      "phase": "Implementation",
      "completion_percentage": 75
    },
    {
      "id": 124,
      "name": "Dự án nâng cấp hạ tầng",
      "status": "completed",
      "phase": "Completed",
      "completion_percentage": 100
    }
  ]
}

# Upload Asset/Service Attachment
POST /api/assets-services/{id}/attachments
{
  "file": "binary_data",
  "description": "Tài liệu kỹ thuật máy chủ"
}
Response: {
  "success": true,
  "attachment_id": 123,
  "file_name": "technical_specs.pdf",
  "file_size": 1024000,
  "download_url": "/api/assets-services/attachments/123/download"
}

# Save Draft Asset/Service
POST /api/assets-services/save-draft
{
  "type": "asset",
  "name": "Máy chủ Dell PowerEdge R740",
  "description": "Máy chủ vật lý cho hệ thống ERP",
  "category": "Hardware",
  "source_project_id": 123,
  "responsible_person_id": 456,
  "draft_data": {
    "asset_details": {
      "model": "PowerEdge R740",
      "specifications": "Intel Xeon, 32GB RAM, 2TB SSD"
    }
  }
}
Response: {
  "success": true,
  "draft_id": "DRAFT-2024-001",
  "message": "Bản nháp đã được lưu thành công"
}

# Import Assets/Services from Excel
POST /api/assets-services/import
{
  "file": "binary_data",
  "import_config": {
    "type": "asset",
    "source_project_id": 123,
    "responsible_person_id": 456,
    "skip_duplicates": true,
    "validate_data": true
  }
}
Response: {
  "success": true,
  "import_summary": {
    "total_records": 50,
    "imported": 45,
    "skipped": 3,
    "errors": 2
  },
  "errors": [
    {
      "row": 5,
      "field": "serial_number",
      "error": "Serial number already exists"
    }
  ],
  "import_id": "IMP-2024-001"
}
```

#### Frontend Components
```typescript
// Asset/Service Creation Form Component
interface AssetServiceFormComponent {
  type: 'asset' | 'service'
  formData: FormData
  formConfig: FormConfig
  
  onTypeChange: (type: 'asset' | 'service') => void
  onFieldChange: (field: string, value: any) => void
  onValidation: (data: any) => Promise<ValidationResult>
  onSubmit: (data: any) => Promise<void>
  onSaveDraft: (data: any) => Promise<void>
}

// Dynamic Form Fields Component
interface DynamicFormFieldsComponent {
  fields: FormField[]
  formData: any
  validationErrors: ValidationError[]
  
  onFieldChange: (field: string, value: any) => void
  onFieldBlur: (field: string) => void
  onFieldFocus: (field: string) => void
}

// Project Selection Component
interface ProjectSelectionComponent {
  availableProjects: Project[]
  selectedProject: Project | null
  
  onProjectSelect: (project: Project) => void
  onProjectSearch: (query: string) => void
  onProjectFilter: (filters: ProjectFilters) => void
}

// Code Generation Component
interface CodeGenerationComponent {
  codeConfig: CodeConfig
  generatedCode: string
  
  onGenerateCode: () => void
  onCodeChange: (code: string) => void
  onCodeValidation: (code: string) => Promise<boolean>
}

// Attachment Upload Component
interface AttachmentUploadComponent {
  attachments: Attachment[]
  maxFileSize: number
  allowedTypes: string[]
  
  onFileUpload: (file: File) => Promise<void>
  onFileRemove: (attachmentId: number) => void
  onFilePreview: (attachment: Attachment) => void
}

// Form Validation Component
interface FormValidationComponent {
  validationRules: ValidationRule[]
  validationErrors: ValidationError[]
  
  onValidate: (data: any) => ValidationResult
  onClearErrors: () => void
  onShowErrors: (errors: ValidationError[]) => void
}

// Preview Component
interface PreviewComponent {
  assetService: AssetService
  previewMode: boolean
  
  onEdit: () => void
  onSave: () => void
  onCancel: () => void
}

// Import Component
interface ImportComponent {
  importConfig: ImportConfig
  importTemplate: ImportTemplate
  
  onFileSelect: (file: File) => void
  onImportConfig: (config: ImportConfig) => void
  onImportStart: () => Promise<ImportResult>
  onTemplateDownload: () => void
}
```

---

### UI/UX Design

#### Creation Form Interface
- **Form Layout:**
  - Type selection tabs
  - Dynamic form fields
  - Validation indicators
  - Action buttons

#### Project Selection Interface
- **Selection Design:**
  - Project search
  - Project filters
  - Project cards
  - Selection indicators

#### Code Generation Interface
- **Code Display:**
  - Auto-generated code
  - Code format info
  - Manual override option
  - Code validation

#### Attachment Interface
- **Upload Design:**
  - Drag-and-drop area
  - File list
  - Upload progress
  - File preview

---

### Integration Requirements

#### Project Module Integration
1. **Project Data**
   - Project information
   - Project status
   - Project phases
   - Project permissions

2. **User Management**
   - User permissions
   - User roles
   - User assignments
   - User validation

#### File Management Integration
1. **File Upload**
   - File validation
   - File storage
   - File security
   - File access

2. **Document Management**
   - Document types
   - Document metadata
   - Document search
   - Document versioning

---

### Security Considerations

#### Data Protection
- Form data validation
- File upload security
- User permission checks
- Data encryption

#### Access Control
- Project access validation
- User role validation
- Form field permissions
- File access control

---

### Testing Strategy

#### Unit Tests
- Form validation logic
- Code generation
- Data validation
- File upload

#### Integration Tests
- Project integration
- File system integration
- User management
- Database operations

#### User Acceptance Tests
- Form workflow
- File upload
- Validation feedback
- Error handling

---

### Deployment & Configuration

#### Environment Setup
- File storage configuration
- Code generation setup
- Form validation rules
- Import/export setup

#### Monitoring & Logging
- Form submission monitoring
- File upload tracking
- Error logging
- Performance monitoring

---

### Documentation

#### User Manual
- Form completion guide
- File upload procedures
- Validation rules
- Import procedures

#### Technical Documentation
- API documentation
- Database schema
- Integration guides
- Configuration guides 