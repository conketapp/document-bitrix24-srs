# Software Requirements Specification (SRS)
## Epic: Chi phí - Quản lý Chi phí

### User Story: CP-4.1
### Đính kèm Tác vụ đến Khoản mục Chi phí

#### Thông tin User Story
- **Story ID:** CP-4.1
- **Priority:** High
- **Story Points:** 6
- **Sprint:** Sprint 4
- **Status:** To Do
- **Dependencies:** CP-1.1, CP-1.2, CP-2.1

#### Mô tả User Story
**Với vai trò là** Cán bộ phụ trách chi phí,  
**Tôi muốn** có thể đính kèm một hoặc nhiều tác vụ (ví dụ: "Yêu cầu thanh toán", "Gửi hồ sơ quyết toán", "Đối chiếu công nợ") trực tiếp vào một khoản mục chi phí  
**Để** tôi có thể theo dõi các công việc cần làm liên quan đến khoản chi phí đó và đảm bảo không bỏ sót.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có khả năng thêm tác vụ vào trang chi tiết của khoản mục chi phí
- [ ] Tác vụ có thể được xem trong danh sách tác vụ tổng thể hoặc trực tiếp trên hồ sơ chi phí
- [ ] Có thể tạo tác vụ mới hoặc gán tác vụ đã tồn tại cho khoản mục chi phí
- [ ] Tác vụ có các trường: tên tác vụ, mô tả, ngày bắt đầu, ngày kết thúc, ưu tiên, trạng thái
- [ ] Có thể gán người thực hiện cho tác vụ
- [ ] Có thể theo dõi tiến độ hoàn thành của tác vụ
- [ ] Hệ thống hiển thị thông báo khi tác vụ đến hạn hoặc quá hạn
- [ ] Có thể lọc và tìm kiếm tác vụ theo nhiều tiêu chí
- [ ] Có thể xuất báo cáo tác vụ theo khoản mục chi phí
- [ ] Tác vụ có thể được liên kết với các tác vụ khác (dependency)
- [ ] Hệ thống ghi log lịch sử thay đổi trạng thái tác vụ

---

### Functional Requirements

#### Core Features
1. **Task Creation & Assignment**
   - Create new tasks for cost items
   - Assign existing tasks to cost items
   - Task template system
   - Bulk task assignment

2. **Task Management**
   - Task status tracking
   - Priority management
   - Due date monitoring
   - Progress tracking

3. **Task Monitoring**
   - Deadline notifications
   - Overdue alerts
   - Progress reports
   - Task analytics

4. **Task Integration**
   - Cost item integration
   - User assignment
   - Dependency management
   - Workflow integration

#### Business Rules
- Mỗi tác vụ phải có tên và mô tả rõ ràng
- Tác vụ phải có ngày bắt đầu và ngày kết thúc dự kiến
- Tác vụ có thể được gán cho một hoặc nhiều người thực hiện
- Tác vụ có thể có dependency với các tác vụ khác
- Trạng thái tác vụ phải được cập nhật thường xuyên
- Tác vụ quá hạn phải được đánh dấu và thông báo

#### Task Types
1. **Payment Tasks**
   - Yêu cầu thanh toán
   - Chuẩn bị hồ sơ thanh toán
   - Gửi hồ sơ thanh toán
   - Theo dõi thanh toán

2. **Settlement Tasks**
   - Gửi hồ sơ quyết toán
   - Đối chiếu công nợ
   - Kiểm tra hồ sơ quyết toán
   - Hoàn tất quyết toán

3. **Documentation Tasks**
   - Thu thập chứng từ
   - Kiểm tra tính hợp lệ
   - Scan và lưu trữ
   - Cập nhật hệ thống

4. **Approval Tasks**
   - Gửi phê duyệt
   - Theo dõi phê duyệt
   - Xử lý phản hồi
   - Hoàn tất phê duyệt

5. **Follow-up Tasks**
   - Theo dõi tiến độ
   - Liên hệ nhà cung cấp
   - Cập nhật thông tin
   - Báo cáo tình hình

#### Task Status
1. **Not Started** - Chưa bắt đầu
2. **In Progress** - Đang thực hiện
3. **On Hold** - Tạm dừng
4. **Completed** - Hoàn thành
5. **Cancelled** - Đã hủy
6. **Overdue** - Quá hạn

#### Task Priority
1. **Low** - Thấp
2. **Medium** - Trung bình
3. **High** - Cao
4. **Critical** - Khẩn cấp

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng tác vụ
CREATE TABLE cost_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_code VARCHAR(50) NOT NULL UNIQUE,
    task_name VARCHAR(200) NOT NULL,
    task_description TEXT,
    cost_item_id INT NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    status ENUM('not_started', 'in_progress', 'on_hold', 'completed', 'cancelled', 'overdue') DEFAULT 'not_started',
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    completed_date DATE NULL,
    estimated_hours DECIMAL(5,2) DEFAULT 0,
    actual_hours DECIMAL(5,2) DEFAULT 0,
    progress_percentage INT DEFAULT 0,
    assigned_to INT NULL,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_cost_item_id (cost_item_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_due_date (due_date),
    INDEX idx_assigned_to (assigned_to)
);

-- Bảng dependency giữa các tác vụ
CREATE TABLE task_dependencies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    dependent_task_id INT NOT NULL,
    prerequisite_task_id INT NOT NULL,
    dependency_type ENUM('finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish') DEFAULT 'finish_to_start',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (dependent_task_id) REFERENCES cost_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_task_id) REFERENCES cost_tasks(id) ON DELETE CASCADE,
    UNIQUE KEY unique_dependency (dependent_task_id, prerequisite_task_id),
    INDEX idx_dependent_task (dependent_task_id),
    INDEX idx_prerequisite_task (prerequisite_task_id)
);

-- Bảng lịch sử tác vụ
CREATE TABLE task_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT NOT NULL,
    action_type ENUM('created', 'updated', 'status_changed', 'assigned', 'completed') NOT NULL,
    field_name VARCHAR(100) NULL,
    old_value TEXT,
    new_value TEXT,
    performed_by INT NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    
    FOREIGN KEY (task_id) REFERENCES cost_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (performed_by) REFERENCES users(id),
    INDEX idx_task_id (task_id),
    INDEX idx_action_type (action_type),
    INDEX idx_performed_at (performed_at)
);

-- Bảng template tác vụ
CREATE TABLE task_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(200) NOT NULL,
    template_description TEXT,
    task_type VARCHAR(100) NOT NULL,
    default_priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    default_duration_days INT DEFAULT 1,
    default_description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_task_type (task_type),
    INDEX idx_is_active (is_active)
);

-- Bảng thông báo tác vụ
CREATE TABLE task_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT NOT NULL,
    notification_type ENUM('due_soon', 'overdue', 'completed', 'assigned') NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    sent_to INT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (task_id) REFERENCES cost_tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (sent_to) REFERENCES users(id),
    INDEX idx_task_id (task_id),
    INDEX idx_notification_type (notification_type),
    INDEX idx_is_read (is_read),
    INDEX idx_sent_to (sent_to)
);

-- Bảng báo cáo tác vụ
CREATE TABLE task_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    report_name VARCHAR(200) NOT NULL,
    report_type ENUM('daily', 'weekly', 'monthly', 'custom') NOT NULL,
    report_date DATE NOT NULL,
    cost_item_id INT NULL,
    total_tasks INT NOT NULL,
    completed_tasks INT DEFAULT 0,
    overdue_tasks INT DEFAULT 0,
    in_progress_tasks INT DEFAULT 0,
    generated_by INT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id),
    FOREIGN KEY (generated_by) REFERENCES users(id),
    INDEX idx_report_date (report_date),
    INDEX idx_report_type (report_type)
);

-- Insert default task templates
INSERT INTO task_templates (template_name, template_description, task_type, default_priority, default_duration_days, default_description) VALUES
('Yêu cầu thanh toán', 'Tạo yêu cầu thanh toán cho khoản mục chi phí', 'payment', 'high', 3, 'Chuẩn bị và gửi yêu cầu thanh toán'),
('Gửi hồ sơ quyết toán', 'Gửi hồ sơ quyết toán cho khoản mục chi phí', 'settlement', 'critical', 5, 'Thu thập và gửi hồ sơ quyết toán'),
('Đối chiếu công nợ', 'Đối chiếu công nợ với nhà cung cấp', 'settlement', 'medium', 2, 'Đối chiếu và xác nhận công nợ'),
('Thu thập chứng từ', 'Thu thập chứng từ cho khoản mục chi phí', 'documentation', 'medium', 3, 'Thu thập đầy đủ chứng từ cần thiết'),
('Phê duyệt chi phí', 'Gửi phê duyệt cho khoản mục chi phí', 'approval', 'high', 2, 'Gửi yêu cầu phê duyệt chi phí');
```

#### API Endpoints
```typescript
# Task Management
POST /api/cost-items/{id}/tasks
{
  "task_name": "Yêu cầu thanh toán",
  "task_description": "Chuẩn bị và gửi yêu cầu thanh toán cho khoản mục chi phí",
  "task_type": "payment",
  "priority": "high",
  "start_date": "2024-01-25",
  "due_date": "2024-01-28",
  "estimated_hours": 8.0,
  "assigned_to": 456
}
Response: {
  "id": 123,
  "task_code": "TASK-2024-0001",
  "task_name": "Yêu cầu thanh toán",
  "task_description": "Chuẩn bị và gửi yêu cầu thanh toán cho khoản mục chi phí",
  "cost_item_id": 789,
  "task_type": "payment",
  "priority": "high",
  "status": "not_started",
  "start_date": "2024-01-25",
  "due_date": "2024-01-28",
  "assigned_to": 456,
  "created_by": 123,
  "created_at": "2024-01-25T10:30:00Z"
}

# Get Tasks for Cost Item
GET /api/cost-items/{id}/tasks
{
  "status_filter": "in_progress",
  "priority_filter": "high",
  "assigned_to": 456,
  "page": 1,
  "limit": 20
}
Response: {
  "tasks": [
    {
      "id": 123,
      "task_code": "TASK-2024-0001",
      "task_name": "Yêu cầu thanh toán",
      "task_description": "Chuẩn bị và gửi yêu cầu thanh toán",
      "task_type": "payment",
      "priority": "high",
      "status": "in_progress",
      "start_date": "2024-01-25",
      "due_date": "2024-01-28",
      "progress_percentage": 60,
      "assigned_to": 456,
      "assigned_user_name": "Nguyễn Văn A"
    }
  ],
  "pagination": {
    "total": 15,
    "page": 1,
    "limit": 20,
    "total_pages": 1
  },
  "statistics": {
    "total_tasks": 15,
    "completed_tasks": 8,
    "in_progress_tasks": 5,
    "overdue_tasks": 2,
    "not_started_tasks": 0
  }
}

# Update Task
PUT /api/cost-items/{id}/tasks/{task_id}
{
  "status": "completed",
  "progress_percentage": 100,
  "actual_hours": 10.0,
  "completed_date": "2024-01-26"
}

# Task Dependencies
POST /api/cost-items/{id}/tasks/{task_id}/dependencies
{
  "prerequisite_task_id": 124,
  "dependency_type": "finish_to_start"
}

# Task Templates
GET /api/task-templates
Response: {
  "templates": [
    {
      "id": 1,
      "template_name": "Yêu cầu thanh toán",
      "template_description": "Tạo yêu cầu thanh toán cho khoản mục chi phí",
      "task_type": "payment",
      "default_priority": "high",
      "default_duration_days": 3,
      "default_description": "Chuẩn bị và gửi yêu cầu thanh toán"
    }
  ]
}

# Task Notifications
GET /api/tasks/notifications
Response: {
  "notifications": [
    {
      "id": 1,
      "task_id": 123,
      "notification_type": "due_soon",
      "message": "Tác vụ 'Yêu cầu thanh toán' sẽ đến hạn trong 2 ngày",
      "is_read": false,
      "sent_at": "2024-01-25T10:30:00Z"
    }
  ]
}

# Task Reports
GET /api/cost-items/{id}/task-reports
{
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "include_details": true
}
Response: {
  "report_data": {
    "total_tasks": 25,
    "completed_tasks": 18,
    "overdue_tasks": 3,
    "in_progress_tasks": 4,
    "completion_rate": 72.0,
    "overdue_rate": 12.0,
    "tasks_by_type": {
      "payment": 10,
      "settlement": 8,
      "documentation": 5,
      "approval": 2
    },
    "tasks_by_priority": {
      "critical": 5,
      "high": 12,
      "medium": 6,
      "low": 2
    }
  }
}

# Task Statistics
GET /api/tasks/statistics
Response: {
  "total_tasks": 150,
  "completed_tasks": 120,
  "overdue_tasks": 15,
  "in_progress_tasks": 15,
  "completion_rate": 80.0,
  "overdue_rate": 10.0,
  "average_completion_time": 4.5,
  "tasks_by_cost_item": {
    "cost_item_123": 25,
    "cost_item_124": 20,
    "cost_item_125": 15
  }
}
```

#### Frontend Components
```typescript
// Task List Component
interface TaskListComponent {
  costItemId: number
  tasks: Task[]
  filters: TaskFilters
  
  onTaskSelect: (task: Task) => void
  onTaskCreate: () => void
  onTaskUpdate: (task: Task, updates: Partial<Task>) => Promise<void>
  onTaskDelete: (task: Task) => Promise<void>
  onFilterChange: (filters: TaskFilters) => void
}

// Task Creation Component
interface TaskCreationComponent {
  costItemId: number
  templates: TaskTemplate[]
  isVisible: boolean
  
  onCreateTask: (task: Partial<Task>) => Promise<void>
  onUseTemplate: (template: TaskTemplate) => void
  onCancel: () => void
}

// Task Detail Component
interface TaskDetailComponent {
  task: Task
  isVisible: boolean
  
  onUpdateTask: (updates: Partial<Task>) => Promise<void>
  onDeleteTask: () => Promise<void>
  onClose: () => void
}

// Task Status Component
interface TaskStatusComponent {
  task: Task
  
  onStatusChange: (status: TaskStatus) => Promise<void>
  onProgressUpdate: (progress: number) => Promise<void>
}

// Task Assignment Component
interface TaskAssignmentComponent {
  task: Task
  availableUsers: User[]
  
  onAssignTask: (userId: number) => Promise<void>
  onUnassignTask: () => Promise<void>
}

// Task Dependency Component
interface TaskDependencyComponent {
  task: Task
  availableTasks: Task[]
  
  onAddDependency: (prerequisiteTaskId: number) => Promise<void>
  onRemoveDependency: (dependencyId: number) => Promise<void>
}

// Task Notification Component
interface TaskNotificationComponent {
  notifications: TaskNotification[]
  
  onMarkAsRead: (notificationId: number) => Promise<void>
  onViewTask: (taskId: number) => void
  onDismissNotification: (notificationId: number) => Promise<void>
}

// Task Report Component
interface TaskReportComponent {
  costItemId: number
  reportData: TaskReport
  
  onGenerateReport: () => Promise<void>
  onExportReport: (format: 'pdf' | 'excel') => void
  onFilterReport: (filters: ReportFilters) => void
}

// Task Statistics Component
interface TaskStatisticsComponent {
  statistics: TaskStatistics
  
  onRefreshStatistics: () => Promise<void>
  onViewDetails: (category: string) => void
}

// Task Template Component
interface TaskTemplateComponent {
  templates: TaskTemplate[]
  selectedTemplate: TaskTemplate | null
  
  onTemplateSelect: (template: TaskTemplate) => void
  onUseTemplate: (template: TaskTemplate) => void
  onCreateTemplate: (template: TaskTemplate) => Promise<void>
}

// Task Calendar Component
interface TaskCalendarComponent {
  tasks: Task[]
  selectedDate: Date
  
  onDateSelect: (date: Date) => void
  onTaskSelect: (task: Task) => void
  onTaskCreate: (date: Date) => void
}
```

---

### UI/UX Design

#### Task Management Interface
- **Task List:**
  - Grid/list view options
  - Status indicators
  - Priority badges
  - Progress bars

#### Task Creation Interface
- **Creation Form:**
  - Template selection
  - Form validation
  - Auto-save functionality
  - Quick create options

#### Task Detail Interface
- **Detail View:**
  - Task information
  - Status updates
  - Assignment management
  - Dependency tracking

#### Task Monitoring Interface
- **Monitoring Dashboard:**
  - Task overview
  - Deadline alerts
  - Progress tracking
  - Performance metrics

---

### Integration Requirements

#### Cost Item Integration
1. **Task Association**
   - Direct linking
   - Context preservation
   - Status synchronization
   - Progress tracking

2. **User Integration**
   - Assignment management
   - Notification system
   - Permission control
   - Activity tracking

#### Workflow Integration
1. **Task Workflow**
   - Status transitions
   - Approval processes
   - Dependency management
   - Completion tracking

2. **Notification System**
   - Deadline alerts
   - Status updates
   - Assignment notifications
   - Overdue warnings

---

### Security Considerations

#### Data Protection
- Task permission validation
- Assignment authorization
- Status change logging
- Access control

#### User Management
- Role-based task access
- Assignment permissions
- Notification preferences
- Privacy controls

---

### Testing Strategy

#### Unit Tests
- Task creation logic
- Status transition rules
- Assignment validation
- Dependency checking

#### Integration Tests
- Database operations
- API endpoint testing
- Notification system
- Report generation

#### User Acceptance Tests
- Task workflow completion
- Assignment process
- Notification delivery
- Report accuracy

---

### Deployment & Configuration

#### Environment Setup
- Database migration scripts
- Template configuration
- Notification setup
- Report configuration

#### Monitoring & Logging
- Task activity tracking
- Performance monitoring
- Error logging
- User behavior analytics

---

### Documentation

#### User Manual
- Task creation procedures
- Assignment guidelines
- Status management
- Report generation

#### Technical Documentation
- API documentation
- Database schema
- Workflow implementation
- Integration guides 