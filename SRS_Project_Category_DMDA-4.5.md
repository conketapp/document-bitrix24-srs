# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### User Story: DMDA-4.5
### Phân quyền Truy cập và Thao tác Dự án Chi tiết

#### Thông tin User Story
- **Story ID:** DMDA-4.5
- **Priority:** High
- **Story Points:** 13
- **Sprint:** Sprint 4
- **Status:** To Do
- **Phụ thuộc:** DMDA-1.1, DMDA-2.1, DMDA-3.1, DMDA-4.1

#### Mô tả User Story
**Với vai trò là** Quản trị viên hệ thống,  
**Tôi muốn** có thể phân quyền chi tiết cho từng người dùng hoặc nhóm người dùng (ví dụ: chỉ xem, tạo, chỉnh sửa, xóa, gửi phê duyệt) trên danh mục và từng dự án cụ thể,  
**Để** tôi có thể đảm bảo tính bảo mật và đúng thẩm quyền truy cập thông tin dự án trong môi trường ngân hàng.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Hệ thống có giao diện quản lý phân quyền rõ ràng
- [ ] Các quyền được định nghĩa chi tiết theo từng chức năng (ví dụ: xem danh mục, tạo dự án, sửa dự án nháp, sửa dự án đã gửi phê duyệt, xóa dự án, gửi phê duyệt, phê duyệt dự án)
- [ ] Phân quyền có thể áp dụng ở cấp danh mục (tổng thể) và/hoặc cấp từng dự án (chi tiết)
- [ ] Có thể tạo và quản lý các role template cho nhóm người dùng
- [ ] Hệ thống kiểm tra quyền trước mỗi thao tác và hiển thị thông báo phù hợp
- [ ] Có thể xem lịch sử thay đổi phân quyền và audit trail
- [ ] Phân quyền được áp dụng real-time không cần restart hệ thống

#### 2.4 Activity Diagram
![DMDA-4.5 Activity Diagram](diagrams/DMDA-4.5%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý phân quyền truy cập và thao tác dự án chi tiết*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Kiểm soát Truy cập Dựa trên Vai trò (RBAC)**
   - Tạo và quản lý vai trò
   - Gán quyền cho từng vai trò
   - Áp dụng vai trò cho người dùng hoặc nhóm người dùng
   - Cấu trúc vai trò phân cấp

2. **Quản lý Phân quyền**
   - Phân quyền cấp danh mục
   - Phân quyền cấp dự án
   - Kiểm soát phân quyền chi tiết
   - Quy tắc kế thừa phân quyền

3. **Quản lý Người dùng và Nhóm**
   - Gán vai trò cho người dùng
   - Gán phân quyền dựa trên nhóm
   - Cập nhật phân quyền hàng loạt
   - Tổng quan phân quyền người dùng

4. **Ma trận Phân quyền**
   - Ma trận phân quyền trực quan
   - Công cụ so sánh vai trò
   - Phát hiện xung đột phân quyền
   - Đề xuất tối ưu hóa phân quyền

#### Quy tắc Kinh doanh
- Quản trị viên có toàn quyền quản lý phân quyền
- Phân quyền được kiểm tra trước mỗi hành động
- Ghi log cho tất cả thay đổi phân quyền
- Kế thừa phân quyền từ danh mục xuống dự án
- Mẫu vai trò có thể được tái sử dụng

#### Mapping Trạng thái Dự án

**Trạng thái Phê duyệt Dự án:**
| Key (Database) | Label (Hiển thị) | Mô tả |
|----------------|-------------------|-------|
| initialized | Khởi tạo | Dự án mới được tạo |
| pending_approval | Chờ phê duyệt | Dự án đã gửi chờ phê duyệt |
| approved | Đã phê duyệt | Dự án đã được phê duyệt |
| rejected | Từ chối phê duyệt | Dự án bị từ chối phê duyệt |

**Trạng thái Thực hiện Dự án:**
| Key (Database) | Label (Hiển thị) | Mô tả |
|----------------|-------------------|-------|
| not_started | Chưa bắt đầu | Dự án chưa triển khai |
| in_progress | Đang thực hiện | Dự án đang được triển khai |
| suspended | Tạm dừng | Dự án tạm dừng thực hiện |
| completed | Hoàn thành | Dự án đã hoàn thành |

**Trạng thái Yêu cầu Chỉnh sửa:**
| Key (Database) | Label (Hiển thị) | Mô tả |
|----------------|-------------------|-------|
| none | Không có yêu cầu | Không có yêu cầu chỉnh sửa |
| edit_requested | Yêu cầu chỉnh sửa | Dự án yêu cầu chỉnh sửa |

#### Các Loại Phân quyền
1. **Phân quyền Danh mục**
   - VIEW_CATEGORY: Xem danh mục
   - CREATE_PROJECT: Tạo dự án mới
   - EDIT_CATEGORY: Chỉnh sửa thông tin danh mục
   - DELETE_CATEGORY: Xóa danh mục
   - MANAGE_CATEGORY_PERMISSIONS: Quản lý phân quyền danh mục

2. **Phân quyền Dự án**
   - VIEW_PROJECT: Xem thông tin dự án
   - CREATE_PROJECT: Tạo dự án mới
   - EDIT_INITIALIZED_PROJECT: Sửa dự án khởi tạo
- EDIT_PENDING_APPROVAL_PROJECT: Sửa dự án chờ phê duyệt
   - DELETE_PROJECT: Xóa dự án
   - SUBMIT_FOR_APPROVAL: Gửi phê duyệt
   - APPROVE_PROJECT: Phê duyệt dự án
   - REJECT_PROJECT: Từ chối dự án
   - MANAGE_PROJECT_PERMISSIONS: Quản lý phân quyền dự án

---

#### 5.5 Sequence Diagram
![DMDA-4.5 Sequence Diagram](diagrams/DMDA-4.5%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi quản lý phân quyền dự án*

---

### Đặc tả Kỹ thuật

#### Cập nhật Cấu trúc Cơ sở Dữ liệu
```sql
-- Bảng roles (vai trò)
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_system_role BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng permissions (quyền)
CREATE TABLE permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(200) NOT NULL,
    description TEXT,
    resource_type ENUM('category', 'project', 'system') NOT NULL,
    action VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng role_permissions (quyền của vai trò)
CREATE TABLE role_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    resource_id INT, -- NULL cho system permissions, category_id cho category permissions, project_id cho project permissions
    granted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE KEY unique_role_permission (role_id, permission_id, resource_id)
);

-- Bảng user_roles (vai trò của user)
CREATE TABLE user_roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    resource_id INT, -- NULL cho system roles, category_id cho category roles, project_id cho project roles
    assigned_by INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id),
    UNIQUE KEY unique_user_role (user_id, role_id, resource_id)
);

-- Bảng permission_audit_log (lịch sử thay đổi phân quyền)
CREATE TABLE permission_audit_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action_type ENUM('grant', 'revoke', 'modify') NOT NULL,
    target_type ENUM('user', 'role', 'permission') NOT NULL,
    target_id INT NOT NULL,
    resource_type ENUM('category', 'project', 'system') NOT NULL,
    resource_id INT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_value JSON,
    new_value JSON,
    reason TEXT,
    FOREIGN KEY (performed_by) REFERENCES users(id)
);

-- Insert default system roles
INSERT INTO roles (name, description, is_system_role) VALUES
('System Administrator', 'Quản trị viên hệ thống với toàn quyền', TRUE),
('Category Manager', 'Quản lý danh mục dự án', TRUE),
('Project Manager', 'Quản lý dự án', TRUE),
('Project Member', 'Thành viên dự án', TRUE),
('Viewer', 'Chỉ xem thông tin', TRUE);

-- Insert default permissions
INSERT INTO permissions (name, display_name, description, resource_type, action) VALUES
-- Category permissions
('VIEW_CATEGORY', 'Xem danh mục', 'Quyền xem thông tin danh mục dự án', 'category', 'view'),
('CREATE_PROJECT', 'Tạo dự án', 'Quyền tạo dự án mới trong danh mục', 'category', 'create'),
('EDIT_CATEGORY', 'Sửa danh mục', 'Quyền chỉnh sửa thông tin danh mục', 'category', 'edit'),
('DELETE_CATEGORY', 'Xóa danh mục', 'Quyền xóa danh mục dự án', 'category', 'delete'),
('MANAGE_CATEGORY_PERMISSIONS', 'Quản lý phân quyền danh mục', 'Quyền quản lý phân quyền của danh mục', 'category', 'manage_permissions'),

-- Project permissions
('VIEW_PROJECT', 'Xem dự án', 'Quyền xem thông tin dự án', 'project', 'view'),
('CREATE_PROJECT', 'Tạo dự án', 'Quyền tạo dự án mới', 'project', 'create'),
('EDIT_INITIALIZED_PROJECT', 'Sửa dự án khởi tạo', 'Quyền chỉnh sửa dự án ở trạng thái khởi tạo', 'project', 'edit_initialized'),
('EDIT_PENDING_APPROVAL_PROJECT', 'Sửa dự án chờ phê duyệt', 'Quyền chỉnh sửa dự án đã gửi chờ phê duyệt', 'project', 'edit_pending_approval'),
('DELETE_PROJECT', 'Xóa dự án', 'Quyền xóa dự án', 'project', 'delete'),
('SUBMIT_FOR_APPROVAL', 'Gửi phê duyệt', 'Quyền gửi dự án để phê duyệt', 'project', 'submit'),
('APPROVE_PROJECT', 'Phê duyệt dự án', 'Quyền phê duyệt dự án', 'project', 'approve'),
('REJECT_PROJECT', 'Từ chối dự án', 'Quyền từ chối dự án', 'project', 'reject'),
('MANAGE_PROJECT_PERMISSIONS', 'Quản lý phân quyền dự án', 'Quyền quản lý phân quyền của dự án', 'project', 'manage_permissions'),

-- System permissions
('MANAGE_USERS', 'Quản lý người dùng', 'Quyền quản lý người dùng hệ thống', 'system', 'manage_users'),
('MANAGE_ROLES', 'Quản lý vai trò', 'Quyền quản lý vai trò hệ thống', 'system', 'manage_roles'),
('VIEW_AUDIT_LOG', 'Xem lịch sử', 'Quyền xem lịch sử thay đổi', 'system', 'view_audit');
```

#### API Endpoints
```
# Role Management
GET /api/roles
POST /api/roles
PUT /api/roles/{id}
DELETE /api/roles/{id}

# Permission Management
GET /api/permissions
GET /api/permissions/{resource_type}
POST /api/permissions
PUT /api/permissions/{id}

# User Role Assignment
GET /api/users/{user_id}/roles
POST /api/users/{user_id}/roles
DELETE /api/users/{user_id}/roles/{role_id}

# Resource Permissions
GET /api/categories/{category_id}/permissions
POST /api/categories/{category_id}/permissions
GET /api/projects/{project_id}/permissions
POST /api/projects/{project_id}/permissions

# Permission Check
POST /api/permissions/check
{
  "user_id": 1,
  "resource_type": "project",
  "resource_id": 123,
  "action": "edit"
}

# Audit Log
GET /api/permissions/audit-log
GET /api/permissions/audit-log/{id}
```

#### Frontend Components
```typescript
// Permission Management Interface
interface PermissionManager {
  // Role Management
  createRole(role: Role): Promise<Role>
  updateRole(id: number, role: Partial<Role>): Promise<Role>
  deleteRole(id: number): Promise<void>
  getRoles(): Promise<Role[]>
  
  // Permission Assignment
  assignRoleToUser(userId: number, roleId: number, resourceId?: number): Promise<void>
  revokeRoleFromUser(userId: number, roleId: number, resourceId?: number): Promise<void>
  getUserRoles(userId: number): Promise<UserRole[]>
  
  // Permission Check
  checkPermission(userId: number, resourceType: string, resourceId: number, action: string): Promise<boolean>
  
  // Audit Log
  getAuditLog(filters: AuditLogFilters): Promise<AuditLogEntry[]>
}

// Permission Matrix Component
interface PermissionMatrix {
  roles: Role[]
  permissions: Permission[]
  matrix: PermissionMatrixData
  onPermissionChange: (roleId: number, permissionId: number, granted: boolean) => void
}

// User Permission Overview
interface UserPermissionOverview {
  user: User
  roles: UserRole[]
  permissions: UserPermission[]
  effectivePermissions: Permission[]
}
```

---

### UI/UX Design

#### Permission Management Dashboard
- **Layout:** Sidebar navigation với main content area
- **Components:** 
  - Role management table
  - Permission matrix grid
  - User assignment interface
  - Audit log viewer
- **Features:**
  - Drag & drop role assignment
  - Bulk permission updates
  - Visual permission indicators
  - Search and filter capabilities

#### Permission Matrix Interface
- **Grid Layout:** Roles (columns) x Permissions (rows)
- **Visual Indicators:**
  - ✅ Granted permission
  - ❌ Denied permission
  - ⚠️ Inherited permission
  - 🔒 System permission (read-only)
- **Interactive Elements:**
  - Checkbox toggles for permissions
  - Tooltip with permission description
  - Bulk selection options

#### User Permission Overview
- **User Profile Section:**
  - User information
  - Assigned roles
  - Effective permissions
- **Permission Tree:**
  - Hierarchical view of permissions
  - Source indication (direct/inherited)
  - Permission status indicators

---

### Security Considerations

#### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (RBAC)
- Permission-based authorization
- Session management with timeout

#### Data Protection
- Encrypted sensitive data
- Audit trail for all permission changes
- Data backup and recovery
- GDPR compliance considerations

#### Access Control
- Principle of least privilege
- Permission inheritance rules
- Conflict resolution for overlapping permissions
- Emergency access procedures

---

### Testing Strategy

#### Unit Tests
- Permission checking logic
- Role assignment validation
- Permission inheritance rules
- Audit log functionality

#### Integration Tests
- API endpoint testing
- Database transaction testing
- Permission caching mechanism
- Cross-module permission integration

#### User Acceptance Tests
- Permission management workflow
- User role assignment process
- Permission matrix interface
- Audit log review process

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Default role and permission seeding
- Configuration file setup
- Environment-specific settings

#### Monitoring & Logging
- Permission access logs
- Performance monitoring
- Error tracking and alerting
- Usage analytics

---

### Documentation

#### User Manual
- Permission management guide
- Role assignment procedures
- Troubleshooting common issues
- Best practices for permission design

#### Technical Documentation
- API documentation
- Database schema documentation
- Security implementation details
- Performance optimization guidelines 

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 4