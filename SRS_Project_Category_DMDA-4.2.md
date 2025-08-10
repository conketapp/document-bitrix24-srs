# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### User Story: DMDA-4.2
### Chế độ Xem Kanban cho Danh mục Dự án

#### Thông tin User Story
- **Story ID:** DMDA-4.2
- **Priority:** Medium
- **Story Points:** 12
- **Sprint:** Sprint 4
- **Status:** To Do
- **Phụ thuộc:** DMDA-1.1, DMDA-3.1, DMDA-3.4, DMDA-4.1 (Cần có danh sách dự án và các trạng thái)

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** có thể xem danh mục dự án dưới dạng bảng Kanban (với các cột đại diện cho trạng thái của dự án, ví dụ: "Khởi tạo", "Chờ phê duyệt", "Đã phê duyệt", "Từ chối phê duyệt", "Dừng thực hiện", "Yêu cầu chỉnh sửa"),  
**Để** tôi có thể trực quan hóa quy trình làm việc và nhanh chóng nắm bắt trạng thái của tất cả các dự án.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có tùy chọn chuyển đổi chế độ xem giữa dạng danh sách/bảng và Kanban
- [ ] Các thẻ dự án có thể kéo thả giữa các cột trạng thái (nếu quyền cho phép)
- [ ] Thông tin chính của dự án hiển thị trên mỗi thẻ Kanban
- [ ] Các cột Kanban đại diện cho các trạng thái dự án
- [ ] Có thể filter và search trong chế độ Kanban
- [ ] Hiển thị số lượng dự án trong mỗi cột
- [ ] Responsive design cho mobile và tablet

#### 2.4 Activity Diagram
![DMDA-4.2 Activity Diagram](diagrams/DMDA-4.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý chế độ xem Kanban cho danh mục dự án*

---

### Yêu cầu Chức năng

#### Tính năng Chính
1. **Giao diện Bảng Kanban**
   - Hiển thị dự án theo cột trạng thái
   - Chức năng kéo thả
   - Cập nhật thời gian thực
   - Thống kê cột

2. **Chuyển đổi Chế độ Xem**
   - Chuyển đổi giữa chế độ xem danh sách và Kanban
   - Ghi nhớ tùy chọn người dùng
   - Dữ liệu nhất quán giữa các chế độ xem
   - Hiệu ứng chuyển đổi mượt mà

3. **Thẻ Kanban**
   - Hiển thị thông tin chính của dự án
   - Chỉ báo trực quan cho mức độ ưu tiên và trạng thái
   - Nút hành động nhanh
   - Hiệu ứng hover và tooltip

#### Quy tắc Kinh doanh
- Chỉ người dùng có quyền mới có thể kéo thả
- Thay đổi trạng thái phải được xác thực
- Đồng bộ thời gian thực với cơ sở dữ liệu
- Tối ưu hóa hiệu suất cho tập dữ liệu lớn

---

#### 5.5 Sequence Diagram
![DMDA-4.2 Sequence Diagram](diagrams/DMDA-4.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi sử dụng chế độ xem Kanban*

---

### Đặc tả Kỹ thuật

#### Cập nhật Cấu trúc Cơ sở Dữ liệu
```sql
-- Bảng lưu cấu hình Kanban columns
CREATE TABLE kanban_columns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status_code VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    color_code VARCHAR(7) DEFAULT '#3B82F6',
    sort_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng lưu user preferences cho view
CREATE TABLE user_view_preferences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    view_type ENUM('list', 'kanban') DEFAULT 'list',
    kanban_config JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_user_preference (user_id)
);

-- Bảng lưu drag & drop history
CREATE TABLE kanban_drag_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    from_status VARCHAR(50) NOT NULL,
    to_status VARCHAR(50) NOT NULL,
    drag_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert default Kanban columns
INSERT INTO kanban_columns (status_code, display_name, color_code, sort_order) VALUES
('draft', 'Bản nháp', '#6B7280', 1),
('pending_approval', 'Chờ phê duyệt', '#F59E0B', 2),
('approved', 'Đã phê duyệt', '#10B981', 3),
('rejected', 'Đã từ chối', '#EF4444', 4),
('in_progress', 'Đang thực hiện', '#3B82F6', 5),
('completed', 'Hoàn thành', '#8B5CF6', 6),
('suspended', 'Dừng thực hiện', '#F97316', 7);
```

#### API Endpoints
```
GET /api/projects/kanban
- Request: { 
    status_filter?: string[], 
    category_id?: number, 
    year?: number 
}
- Response: { 
    columns: KanbanColumn[], 
    projects: ProjectCard[] 
}

POST /api/projects/{id}/move-status
- Request: { 
    new_status: string, 
    reason?: string 
}
- Response: { 
    success: boolean, 
    message: string 
}

GET /api/kanban/columns
- Response: List of available Kanban columns

PUT /api/user/preferences/view
- Request: { 
    view_type: 'list' | 'kanban', 
    kanban_config?: object 
}
- Response: { success: boolean }
```

#### Data Models
```typescript
interface KanbanColumn {
    id: number;
    status_code: string;
    display_name: string;
    color_code: string;
    sort_order: number;
    is_active: boolean;
    project_count: number;
}

interface ProjectCard {
    id: number;
    project_code: string;
    name: string;
    status: string;
    category: ProjectCategory;
    budget: number;
    start_date: string;
    end_date?: string;
    created_by: User;
    priority: 'low' | 'medium' | 'high';
    is_official: boolean;
    can_drag: boolean;
    quick_actions: QuickAction[];
}

interface QuickAction {
    id: string;
    label: string;
    icon: string;
    action: string;
    disabled: boolean;
}

interface UserViewPreference {
    user_id: number;
    view_type: 'list' | 'kanban';
    kanban_config?: object;
}
```

---

### User Interface Requirements

#### Kanban Board View
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Danh mục Dự án                    [List View] [Kanban View] [Filter] [Search] │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐   │
│ │ Bản nháp    │ │ Chờ phê     │ │ Đã phê      │ │ Đã từ chối  │ │ Hoàn    │   │
│ │ (3)         │ │ duyệt       │ │ duyệt       │ │ (1)         │ │ thành   │   │
│ │             │ │ (2)         │ │ (5)         │ │             │ │ (2)     │   │
│ │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────┐ │   │
│ │ │ INV-001 │ │ │ │ INV-004 │ │ │ │ INV-002 │ │ │ │ INV-005 │ │ │ │ INV-│ │   │
│ │ │ Dự án A │ │ │ │ Dự án D │ │ │ │ Dự án B │ │ │ │ Dự án E │ │ │ │ 003 │ │   │
│ │ │ 500M    │ │ │ │ 300M    │ │ │ │ 800M    │ │ │ │ 150M    │ │ │ │ Dự  │ │   │
│ │ │ 🏛️      │ │ │ │ ⏳      │ │ │ │ ✅      │ │ │ │ ❌      │ │ │ │ án  │ │   │
│ │ │ [Edit]   │ │ │ │ [View]  │ │ │ │ [View]  │ │ │ │ [View]  │ │ │ │ C   │ │   │
│ │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │ │ │ 400M│ │   │
│ │             │ │             │ │             │ │             │ │ │ ✅  │ │   │
│ │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │ │             │ │ │ [V] │ │   │
│ │ │ INV-006 │ │ │ │ INV-007 │ │ │ │ INV-008 │ │ │             │ │ └─────┘ │   │
│ │ │ Dự án F │ │ │ │ Dự án G │ │ │ │ Dự án H │ │ │             │ │         │   │
│ │ │ 400M    │ │ │ │ 250M    │ │ │ │ 600M    │ │ │             │ │ ┌─────┐ │   │
│ │ │ 📝      │ │ │ │ ⏳      │ │ │ │ ✅      │ │ │             │ │ │ INV-│ │   │
│ │ │ [Edit]  │ │ │ │ [View]  │ │ │ │ [View]  │ │ │             │ │ │ 009 │ │   │
│ │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │ │             │ │ │ Dự  │ │   │
│ │             │ │             │ │             │ │             │ │ │ án I│ │   │
│ │ ┌─────────┐ │ │             │ │ ┌─────────┐ │ │             │ │ │ 200M│ │   │
│ │ │ INV-010 │ │ │             │ │ │ INV-011 │ │ │             │ │ │ ✅  │ │   │
│ │ │ Dự án J │ │ │             │ │ │ Dự án K │ │ │             │ │ │ [V] │ │   │
│ │ │ 350M    │ │ │             │ │ │ 450M    │ │ │             │ │ └─────┘ │   │
│ │ │ 📝      │ │ │             │ │ │ ✅      │ │ │             │ │         │   │
│ │ │ [Edit]  │ │ │             │ │ │ [View]  │ │ │             │ │         │   │
│ │ └─────────┘ │ │             │ │ └─────────┘ │ │             │ │         │   │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Project Card Detail
```
┌─────────────────────────────────────┐
│ PRJ-2024-001 - Dự án A             │
├─────────────────────────────────────┤
│ 🏛️ Loại: Dự án Đầu tư               │
│ 📊 TMĐT dự kiến: 500,000,000 VND   │
│ 📊 TMĐT phê duyệt: 450,000,000 VND │
│ 💰 Lũy kế vốn đã ứng: 200,000,000  │
│ 💰 Vốn đã ứng năm nay: 150,000,000 │
│ 💰 Dự kiến vốn sẽ ứng: 250,000,000 │
│ 💰 Đề xuất năm sau: 300,000,000    │
│ 👤 Người tạo: Nguyễn Văn A         │
│ ⏰ Tạo: 15/02/2024                  │
│                                     │
│ [Xem chi tiết] [Chỉnh sửa] [Phê   │
│ duyệt] [Từ chối]                   │
└─────────────────────────────────────┘
```

#### View Toggle Controls
```
┌─────────────────────────────────────────────────────────┐
│ Chế độ xem:                                            │
├─────────────────────────────────────────────────────────┤
│ ☑️ [📋 List View]  ☐ [📊 Kanban View]                │
│                                                         │
│ Bộ lọc:                                                │
│ ☑️ Tất cả dự án                                        │
│ ☐ Chỉ dự án chính thức                                 │
│ ☐ Dự án của tôi                                        │
│                                                         │
│ Loại dự án: [Tất cả ▼]                                │
│ Nguồn gốc: [Tất cả ▼]                                 │
│ Năm: [2024 ▼]                                          │
│                                                         │
│ Tìm kiếm: [Search box]                                 │
│                                                         │
│ [Áp dụng] [Làm mới] [Export]                          │
└─────────────────────────────────────────────────────────┘
```

#### Drag & Drop Confirmation
```
┌─────────────────────────────────────┐
│ Xác nhận thay đổi trạng thái        │
├─────────────────────────────────────┤
│ Dự án: PRJ-2024-001 - Dự án A      │
│                                     │
│ Từ: Chờ phê duyệt                   │
│ Đến: Đã phê duyệt                   │
│                                     │
│ Lý do thay đổi (tùy chọn):         │
│ [Textarea]                           │
│                                     │
│ ⚠️ Lưu ý: Thay đổi này sẽ được ghi  │
│    lại trong lịch sử dự án          │
│                                     │
│ [Hủy] [Xác nhận]                    │
└─────────────────────────────────────┘
```

---

### Integration Requirements

#### Bitrix24 Integration
- Sync status changes với Bitrix24
- Update deal status khi drag & drop
- Create tasks cho status transitions
- Log Kanban actions trong Bitrix24

#### Notification System
- Notification cho status changes
- Real-time updates cho team members
- Email alerts cho important transitions
- In-app notifications cho drag & drop

---

### Testing Requirements

#### Unit Tests
```typescript
describe('Kanban Board', () => {
    test('should load projects grouped by status', async () => {
        const projects = [
            { id: 1, status: 'draft', name: 'Project A' },
            { id: 2, status: 'pending_approval', name: 'Project B' },
            { id: 3, status: 'approved', name: 'Project C' }
        ];
        
        const kanbanData = await loadKanbanData(projects);
        expect(kanbanData.columns).toHaveLength(3);
        expect(kanbanData.columns[0].project_count).toBe(1);
    });

    test('should validate drag & drop permission', () => {
        const user = { id: 1, role: 'manager' };
        const project = { id: 1, status: 'pending_approval' };
        const newStatus = 'approved';
        
        const canDrag = validateDragPermission(user, project, newStatus);
        expect(canDrag).toBe(true);
    });

    test('should update project status on drag & drop', async () => {
        const projectId = 1;
        const newStatus = 'approved';
        const reason = 'Approved by manager';
        
        await updateProjectStatus(projectId, newStatus, reason);
        
        const project = await getProject(projectId);
        expect(project.status).toBe('approved');
    });
});
```

---

### Success Criteria
- [ ] Toggle giữa List và Kanban view hoạt động
- [ ] Drag & drop project cards hoạt động chính xác
- [ ] Project cards hiển thị đầy đủ thông tin
- [ ] Filter và search trong Kanban hoạt động
- [ ] Real-time updates cho status changes
- [ ] Responsive design cho mobile/tablet
- [ ] Performance tốt với large datasets
- [ ] Tích hợp thành công với Bitrix24

---

### Kanban Configuration Rules

#### Default Kanban Columns
| Status Code | Display Name | Color | Sort Order | Description |
|-------------|--------------|-------|------------|-------------|
| draft | Bản nháp | #6B7280 | 1 | Dự án mới tạo |
| pending_approval | Chờ phê duyệt | #F59E0B | 2 | Đã gửi phê duyệt |
| approved | Đã phê duyệt | #10B981 | 3 | Đã được phê duyệt |
| rejected | Đã từ chối | #EF4444 | 4 | Bị từ chối |
| in_progress | Đang thực hiện | #3B82F6 | 5 | Đang triển khai |
| completed | Hoàn thành | #8B5CF6 | 6 | Đã hoàn thành |
| suspended | Dừng thực hiện | #F97316 | 7 | Tạm dừng |

#### Drag & Drop Rules
| From Status | To Status | Allowed Roles | Validation Required |
|-------------|-----------|---------------|-------------------|
| initialized | pending_approval | creator, manager | Yes |
| pending_approval | approved | approver | Yes |
| pending_approval | rejected | approver | Yes |
| approved | in_progress | manager | No |
| in_progress | completed | manager | No |
| any | suspended | manager, admin | Yes |

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 4 