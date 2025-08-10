# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### User Story: DMDA-3.5
### Phân biệt & Hiển thị Dự án Chính thức

#### Thông tin User Story
- **Story ID:** DMDA-3.5
- **Priority:** Medium
- **Story Points:** 5
- **Sprint:** Sprint 3
- **Status:** To Do
- **Phụ thuộc:** DMDA-4.1, DMDA-3.4 (Cần có phê duyệt và từ chối trước)

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** chỉ các dự án đã được phê duyệt thông qua quy trình của hệ thống (Module Dự án) mới được coi là "dự án chính thức" và hiển thị nổi bật trong danh mục, đồng thời được phân biệt rõ ràng với các dự án tạo tự do trên Bitrix24 (nếu có),  
**Để** tôi có thể dễ dàng nhận biết và quản lý các dự án đã được cấp phép và chịu trách nhiệm chính thức của ngân hàng, phục vụ đúng mục đích quản lý.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Chỉ các dự án có trạng thái "Đã phê duyệt" (thông qua quy trình tùy chỉnh của Module Dự án) mới xuất hiện trong danh sách chính của Module Dự án này
- [ ] Các dự án chính thức có thể được hiển thị với biểu tượng đặc biệt hoặc nằm trong một phần riêng biệt của giao diện để dễ nhận diện
- [ ] Có thể lọc và hiển thị riêng biệt dự án chính thức và dự án Bitrix24
- [ ] Dự án chính thức có badge hoặc indicator đặc biệt
- [ ] Có thể xem thống kê số lượng dự án chính thức
- [ ] Export danh sách dự án chính thức riêng biệt

#### Activity Diagram
![DMDA-3.5 Activity Diagram](diagrams/DMDA-3.5%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý phân biệt và hiển thị dự án chính thức*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Nhận diện Dự án Chính thức**
   - Chỉ dự án có trạng thái "approved" mới được coi là chính thức
   - Badge/icon đặc biệt cho dự án chính thức
   - Phân biệt với dự án Bitrix24 tự do
   - Chỉ báo trực quan cho trạng thái chính thức

2. **Lọc Danh sách Dự án**
   - Lọc theo trạng thái chính thức
   - Tách biệt hiển thị dự án chính thức và không chính thức
   - Chuyển đổi xem giữa tất cả và chỉ dự án chính thức
   - Tìm kiếm và lọc trong dự án chính thức

3. **Quản lý Dự án Chính thức**
   - Thống kê dự án chính thức
   - Xuất danh sách dự án chính thức
   - Bảng điều khiển cho dự án chính thức
   - Báo cáo cho dự án chính thức

#### Quy tắc Kinh doanh
- Chỉ dự án có trạng thái "approved" mới được coi là chính thức
- Dự án chính thức phải có đầy đủ thông tin phê duyệt
- Dự án Bitrix24 tự do không được hiển thị trong danh sách chính thức
- Dự án chính thức có thể được quản lý và báo cáo riêng biệt

---

### Đặc tả Kỹ thuật

#### Cập nhật Cấu trúc Cơ sở Dữ liệu
```sql
-- Thêm trường official_project vào bảng projects
ALTER TABLE projects ADD COLUMN is_official BOOLEAN DEFAULT FALSE;
ALTER TABLE projects ADD COLUMN official_approval_date TIMESTAMP NULL;
ALTER TABLE projects ADD COLUMN official_approver_id INT NULL;
ALTER TABLE projects ADD FOREIGN KEY (official_approver_id) REFERENCES users(id);

-- Bảng lưu lịch sử chuyển đổi trạng thái chính thức
CREATE TABLE project_official_status_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    status_change ENUM('became_official', 'lost_official') NOT NULL,
    changed_by INT NOT NULL,
    change_reason TEXT,
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (changed_by) REFERENCES users(id)
);

-- Bảng cấu hình hiển thị dự án chính thức
CREATE TABLE official_project_display_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index cho performance
CREATE INDEX idx_projects_official ON projects(is_official);
CREATE INDEX idx_projects_approved ON projects(status) WHERE status = 'approved';
CREATE INDEX idx_official_status_history_project ON project_official_status_history(project_id);
```

#### API Endpoints
```
GET /api/projects/official
- Response: List of official projects only

GET /api/projects/official/stats
- Response: Statistics of official projects

GET /api/projects/official/export
- Response: Export data of official projects

GET /api/projects/filter
- Request: { 
    official_only: boolean, 
    status?: string, 
    category_id?: number 
}
- Response: Filtered list of projects

POST /api/projects/{id}/mark-official
- Request: { 
    approver_id: number, 
    approval_date: string 
}
- Response: { success: boolean, message: string }

GET /api/projects/official/dashboard
- Response: Dashboard data for official projects
```

#### Data Models
```typescript
interface OfficialProject {
    id: number;
    project_code: string;
    name: string;
    status: 'approved';
    is_official: true;
    official_approval_date: string;
    official_approver: User;
    category: ProjectCategory;
    year: number;
    budget: number;
    created_by: User;
    created_at: string;
}

interface OfficialProjectStats {
    total_official: number;
    total_approved: number;
    total_pending: number;
    by_category: CategoryStats[];
    by_year: YearStats[];
    by_status: StatusStats[];
}

interface CategoryStats {
    category_id: number;
    category_name: string;
    official_count: number;
    total_count: number;
    percentage: number;
}

interface YearStats {
    year: number;
    official_count: number;
    total_count: number;
}

interface StatusStats {
    status: string;
    count: number;
    percentage: number;
}

interface ProjectFilter {
    official_only: boolean;
    status?: string;
    category_id?: number;
    year?: number;
    search?: string;
    page?: number;
    limit?: number;
}

interface OfficialProjectConfig {
    show_badge: boolean;
    badge_text: string;
    badge_color: string;
    separate_section: boolean;
    section_title: string;
    export_enabled: boolean;
    dashboard_enabled: boolean;
}
```

---

### User Interface Requirements

#### Project List with Official Filter
```
┌─────────────────────────────────────────────────────────┐
│ Danh mục Dự án                    [Tất cả] [Chính thức] │
├─────────────────────────────────────────────────────────┤
│ Tìm kiếm: [Search box]                                │
│ Lọc: [Category] [Year] [Status] [Official Only ✓]     │
├─────────────────────────────────────────────────────────┤
│ Dự án Chính thức (5)                                  │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🏛️ INV-2024-001 | Dự án A | Approved | 500M VND  │ │
│ │ 🏛️ INV-2024-002 | Dự án B | Approved | 300M VND  │ │
│ │ 🏛️ INV-2024-003 | Dự án C | Approved | 800M VND  │ │
│ │ 🏛️ INV-2024-004 | Dự án D | Approved | 200M VND  │ │
│ │ 🏛️ INV-2024-005 | Dự án E | Approved | 600M VND  │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Dự án Khác (3)                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 📝 INV-2024-006 | Dự án F | Draft | 400M VND      │ │
│ │ 📝 INV-2024-007 | Dự án G | Pending | 250M VND    │ │
│ │ 📝 INV-2024-008 | Dự án H | Rejected | 150M VND   │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

#### Official Project Badge
```
┌─────────────────────────────────────────────────────────┐
│ Chi tiết Dự án: INV-2024-001                          │
├─────────────────────────────────────────────────────────┤
│ 🏛️ Dự án Chính thức                                   │
│                                                         │
│ Tên dự án: Dự án đầu tư mới                           │
│ Mã dự án: INV-2024-001                                │
│ Loại: Dự án đầu tư                                     │
│ Năm: 2024                                              │
│ Ngày bắt đầu: 01/03/2024                              │
│ Ngày kết thúc: 31/12/2024                             │
│ Ngân sách: 500,000,000 VND                            │
│ Trạng thái: [Đã phê duyệt]                            │
│ Loại dự án: [Mới]                                     │
│                                                         │
│ Người tạo: Nguyễn Văn A                               │
│ Ngày tạo: 15/02/2024                                  │
│ Người phê duyệt: Trần Thị B                            │
│ Ngày phê duyệt: 22/02/2024                            │
│                                                         │
│ [Chỉnh sửa] [Xem lịch sử] [Export]                   │
└─────────────────────────────────────────────────────────┘
```

#### Official Projects Dashboard
```
┌─────────────────────────────────────────────────────────┐
│ Dashboard Dự án Chính thức                             │
├─────────────────────────────────────────────────────────┤
│ 📊 Thống kê tổng quan                                 │
│ ┌─────────────┬─────────────┬─────────────┬─────────┐ │
│ │ Tổng chính  │ Đã phê duyệt│ Đang chờ   │ Tỷ lệ   │ │
│ │ thức: 15    │ : 12        │ : 3         │ : 80%   │ │
│ └─────────────┴─────────────┴─────────────┴─────────┘ │
│                                                         │
│ 📈 Phân bố theo loại dự án                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Dự án đầu tư: ████████████ 8 dự án (53%)          │ │
│ │ Mua sắm tài sản: ████████ 5 dự án (33%)           │ │
│ │ Thuê dịch vụ: ███ 2 dự án (14%)                   │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ 📅 Phân bố theo năm                                    │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 2024: ████████████████████ 12 dự án (80%)         │ │
│ │ 2023: ████ 3 dự án (20%)                          │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ [Export Báo cáo] [Xem chi tiết] [Cập nhật]           │
└─────────────────────────────────────────────────────────┘
```

#### Filter Options
```
┌─────────────────────────────────────────────────────────┐
│ Bộ lọc Dự án                                          │
├─────────────────────────────────────────────────────────┤
│ ☑️ Chỉ dự án chính thức                               │
│ ☐ Tất cả dự án                                        │
│ ☐ Dự án Bitrix24                                      │
│                                                         │
│ Trạng thái:                                            │
│ ☑️ Đã phê duyệt                                        │
│ ☐ Đang chờ phê duyệt                                  │
│ ☐ Đã từ chối                                          │
│ ☐ Đang chỉnh sửa                                      │
│                                                         │
│ Loại dự án:                                            │
│ ☑️ Dự án đầu tư                                        │
│ ☑️ Mua sắm tài sản                                     │
│ ☑️ Thuê dịch vụ                                        │
│ ☑️ Bảo trì                                             │
│                                                         │
│ Năm: [2024]                                            │
│                                                         │
│ [Áp dụng] [Xóa bộ lọc]                                │
└─────────────────────────────────────────────────────────┘
```

---

### Yêu cầu Tích hợp

#### Bitrix24 Integration
- Sync official project status với Bitrix24
- Update deal custom fields với official status
- Create tasks cho official project management
- Log official project actions trong Bitrix24 activity feed

#### Notification System
- Notification khi dự án trở thành chính thức
- Notification cho official project updates
- Email summary cho official projects
- Dashboard notifications cho official project stats

#### Data Flow
1. System check project approval status
2. Mark project as official if approved
3. Update official project indicators
4. Sync với Bitrix24
5. Update dashboard statistics
6. Send notifications
7. Log official status change

---

### Yêu cầu Kiểm thử

#### Kiểm thử Đơn vị
```typescript
describe('Official Project Management', () => {
    test('should mark project as official when approved', () => {
        const project = {
            id: 1,
            status: 'approved',
            approval_date: '2024-02-22',
            approver_id: 1
        };
        
        const result = markProjectAsOfficial(project);
        expect(result.is_official).toBe(true);
        expect(result.official_approval_date).toBe('2024-02-22');
    });

    test('should filter official projects correctly', () => {
        const projects = [
            { id: 1, status: 'approved', is_official: true },
            { id: 2, status: 'draft', is_official: false },
            { id: 3, status: 'approved', is_official: true }
        ];
        
        const officialProjects = filterOfficialProjects(projects);
        expect(officialProjects).toHaveLength(2);
        expect(officialProjects[0].id).toBe(1);
        expect(officialProjects[1].id).toBe(3);
    });

    test('should generate official project statistics', () => {
        const projects = [
            { status: 'approved', is_official: true, category_id: 1 },
            { status: 'approved', is_official: true, category_id: 1 },
            { status: 'draft', is_official: false, category_id: 2 }
        ];
        
        const stats = generateOfficialProjectStats(projects);
        expect(stats.total_official).toBe(2);
        expect(stats.total_approved).toBe(2);
        expect(stats.by_category[0].official_count).toBe(2);
    });
});
```

#### Integration Tests
- Test Bitrix24 sync cho official projects
- Test notification system cho official status changes
- Test dashboard data generation
- Test export functionality

#### User Acceptance Tests
- Test official project filtering
- Test official project display
- Test dashboard functionality
- Test export functionality
- Test badge display

---

### Success Criteria
- [ ] Chỉ dự án approved hiển thị trong danh sách chính thức
- [ ] Badge/icon đặc biệt cho dự án chính thức
- [ ] Filter và search dự án chính thức hoạt động
- [ ] Dashboard thống kê dự án chính thức chính xác
- [ ] Export dự án chính thức thành công
- [ ] Tích hợp thành công với Bitrix24
- [ ] Notification system hoạt động
- [ ] Visual indicators rõ ràng

---

### Official Project Rules

#### Official Project Criteria
| Criteria | Requirement | Description |
|----------|-------------|-------------|
| Status | Must be "approved" | Dự án phải được phê duyệt |
| Approval Process | Must go through custom workflow | Phải qua quy trình phê duyệt tùy chỉnh |
| Approval Date | Must have approval date | Phải có ngày phê duyệt |
| Approver | Must have approver information | Phải có thông tin người phê duyệt |
| Complete Information | Must have all required fields | Phải có đầy đủ thông tin bắt buộc |

#### Display Rules
| Project Type | Display Location | Badge/Icon | Description |
|--------------|------------------|------------|-------------|
| Official Project | Main list, Official section | 🏛️ | Dự án đã được phê duyệt |
| Non-Official Project | Other section | 📝 | Dự án chưa được phê duyệt |
| Bitrix24 Project | Separate section | 🔗 | Dự án từ Bitrix24 |

#### Filter Options
| Filter Type | Options | Description |
|-------------|---------|-------------|
| Official Status | Official Only, All, Non-Official | Lọc theo trạng thái chính thức |
| Project Status | Approved, Pending, Rejected, Draft | Lọc theo trạng thái dự án |
| Category | Investment, Procurement, Service, Maintenance | Lọc theo loại dự án |
| Year | 2023, 2024, 2025 | Lọc theo năm |

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 3 