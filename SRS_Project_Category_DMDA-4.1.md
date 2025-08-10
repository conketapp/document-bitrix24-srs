# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### User Story: DMDA-4.1
### Ghi nhận Lịch sử Thao tác Dự án (Log)

#### Thông tin User Story
- **Story ID:** DMDA-4.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 4
- **Status:** To Do
- **Dependencies:** DMDA-3.1, DMDA-3.4, DMDA-4.1

#### Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án hoặc Quản trị viên hệ thống,  
**Tôi muốn** tất cả các hành động liên quan đến quy trình phê duyệt (gửi phê duyệt, từ chối, chỉnh sửa lại, phê duyệt lại) đều được ghi lại chính xác với thông tin về người thực hiện, thời gian và nội dung thay đổi,  
**Để** tôi có thể theo dõi toàn bộ lịch sử của dự án, phục vụ công tác kiểm tra, đối chiếu và đảm bảo tính minh bạch.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Mỗi dự án có một phần "Lịch sử hoạt động" hoặc "Log"
- [ ] Thông tin log bao gồm: thời gian, người thực hiện, loại hành động (gửi phê duyệt, từ chối, chỉnh sửa, phê duyệt), và chi tiết liên quan (ví dụ: lý do từ chối)
- [ ] Dữ liệu log không thể bị chỉnh sửa
- [ ] Log được ghi lại tự động cho mọi action
- [ ] Có thể xem lịch sử theo thời gian
- [ ] Có thể filter log theo loại hành động
- [ ] Có thể export log cho audit purposes

#### 2.4 Activity Diagram
![DMDA-4.1 Activity Diagram](diagrams/DMDA-4.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý ghi nhận lịch sử thao tác dự án*

---

### Functional Requirements

#### Core Features
1. **Automatic Logging**
   - Ghi log tự động cho mọi action
   - Capture user information và timestamp
   - Capture action type và details
   - Immutable log records

2. **Project Activity History**
   - Hiển thị lịch sử hoạt động của dự án
   - Chronological order với timestamp
   - User-friendly display format
   - Pagination cho large logs

3. **Log Management**
   - Filter log theo action type
   - Search trong log content
   - Export log data
   - Archive old logs

#### Business Rules
- Tất cả actions phải được log lại
- Log records không thể bị chỉnh sửa hoặc xóa
- Log phải có đầy đủ context information
- Log phải được backup định kỳ
- Log phải tuân thủ retention policy

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Bảng chính lưu log hoạt động dự án
CREATE TABLE project_activity_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    action_type ENUM(
        'project_created',
        'project_updated',
        'project_deleted',
        'approval_submitted',
        'approval_approved',
        'approval_rejected',
        'approval_requested_changes',
        'project_suspended',
        'project_resumed',
        'project_completed',
        'project_cancelled',
        'edit_requested',
        'edit_approved',
        'edit_rejected',
        'bulk_approval_submitted',
        'bulk_approval_processed'
    ) NOT NULL,
    action_details JSON NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_project_activity_logs_project (project_id),
    INDEX idx_project_activity_logs_user (user_id),
    INDEX idx_project_activity_logs_action (action_type),
    INDEX idx_project_activity_logs_created (created_at)
);

-- Bảng lưu chi tiết thay đổi dự án
CREATE TABLE project_change_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_reason TEXT,
    log_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (log_id) REFERENCES project_activity_logs(id)
);
```

#### API Endpoints
```
GET /api/projects/{id}/activity-logs
- Request: { 
    page?: number, 
    limit?: number, 
    action_type?: string, 
    start_date?: string, 
    end_date?: string 
}
- Response: { 
    logs: ActivityLog[], 
    total: number, 
    page: number, 
    limit: number 
}

GET /api/projects/{id}/activity-logs/export
- Request: { 
    format: 'csv' | 'excel' | 'pdf', 
    action_type?: string, 
    start_date?: string, 
    end_date?: string 
}
- Response: File download

GET /api/projects/{id}/change-logs
- Response: List of field changes for project
```

#### Data Models
```typescript
interface ActivityLog {
    id: number;
    project_id: number;
    user_id: number;
    user: User;
    action_type: ActionType;
    action_details: ActionDetails;
    ip_address?: string;
    user_agent?: string;
    created_at: string;
}

interface ActionDetails {
    old_status?: string;
    new_status?: string;
    approval_comment?: string;
    rejection_reason?: string;
    required_changes?: string[];
    field_changes?: FieldChange[];
    bulk_count?: number;
    batch_id?: string;
}

interface FieldChange {
    field_name: string;
    old_value: string;
    new_value: string;
    change_reason?: string;
}

type ActionType = 
    | 'project_created'
    | 'project_updated'
    | 'project_deleted'
    | 'approval_submitted'
    | 'approval_approved'
    | 'approval_rejected'
    | 'approval_requested_changes'
    | 'project_suspended'
    | 'project_resumed'
    | 'project_completed'
    | 'project_cancelled'
    | 'edit_requested'
    | 'edit_approved'
    | 'edit_rejected'
    | 'bulk_approval_submitted'
    | 'bulk_approval_processed';
```

---

### User Interface Requirements

#### Project Activity History Page
```
┌─────────────────────────────────────────────────────────┐
│ Lịch sử Hoạt động - Dự án INV-2024-001                │
├─────────────────────────────────────────────────────────┤
│ Bộ lọc: [Tất cả] [Phê duyệt] [Chỉnh sửa] [Khác]      │
│ Tìm kiếm: [Search box]                                 │
│ Thời gian: [Từ ngày] [Đến ngày] [Áp dụng]            │
├─────────────────────────────────────────────────────────┤
│ 📅 22/02/2024 14:30 - Trần Thị B                      │
│ ✅ Phê duyệt dự án                                     │
│ Ghi chú: "Dự án đáp ứng yêu cầu"                      │
│ Trạng thái: Draft → Approved                           │
│                                                         │
│ 📅 20/02/2024 09:15 - Nguyễn Văn A                    │
│ 📤 Gửi phê duyệt                                       │
│ Người phê duyệt: Trần Thị B                            │
│ Trạng thái: Draft → Pending Approval                   │
│                                                         │
│ 📅 18/02/2024 16:45 - Nguyễn Văn A                    │
│ ✏️ Chỉnh sửa dự án                                     │
│ Thay đổi: Ngân sách 400M → 500M VND                   │
│ Lý do: "Điều chỉnh theo yêu cầu mới"                  │
│                                                         │
│ 📅 15/02/2024 10:30 - Nguyễn Văn A                    │
│ ➕ Tạo dự án mới                                        │
│ Dự án: INV-2024-001 - Dự án đầu tư mới                 │
│ Ngân sách: 400,000,000 VND                             │
│                                                         │
│ [Export Log] [Xem chi tiết] [Làm mới]                 │
└─────────────────────────────────────────────────────────┘
```

#### Activity Log Detail View
```
┌─────────────────────────────────────────────────────────┐
│ Chi tiết Hoạt động - ID: 12345                         │
├─────────────────────────────────────────────────────────┤
│ Thời gian: 22/02/2024 14:30:25                        │
│ Người thực hiện: Trần Thị B (trantb@bank.com)         │
│ Loại hành động: Phê duyệt dự án                        │
│ IP Address: 192.168.1.100                              │
│ User Agent: Mozilla/5.0...                             │
│                                                         │
│ Chi tiết thay đổi:                                     │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Trạng thái: Draft → Approved                       │
│ │ Ghi chú: "Dự án đáp ứng yêu cầu"                  │
│ │ Người phê duyệt: Trần Thị B                       │
│ │ Cấp độ phê duyệt: Level 1                         │
│ │ Thời gian phê duyệt: 22/02/2024 14:30:25         │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ [Quay lại] [Export] [In PDF]                          │
└─────────────────────────────────────────────────────────┘
```

---

### Integration Requirements

#### Bitrix24 Integration
- Sync activity logs với Bitrix24
- Create tasks cho audit purposes
- Update deal custom fields với log information
- Log Bitrix24 actions trong activity feed

#### Notification System
- Notification cho important log events
- Email summary cho daily/weekly activity
- Alert cho suspicious activities
- Audit trail notifications

---

### Testing Requirements

#### Unit Tests
```typescript
describe('Project Activity Logging', () => {
    test('should log project creation', async () => {
        const project = {
            id: 1,
            name: 'Test Project',
            created_by: 1
        };
        
        await logProjectAction(project.id, 1, 'project_created', {
            project_name: project.name,
            budget: 500000000
        });
        
        const logs = await getProjectActivityLogs(project.id);
        expect(logs).toHaveLength(1);
        expect(logs[0].action_type).toBe('project_created');
    });

    test('should prevent log modification', async () => {
        const logId = 1;
        
        try {
            await updateActivityLog(logId, { action_type: 'modified' });
            fail('Should not allow log modification');
        } catch (error) {
            expect(error.message).toContain('Log records cannot be modified');
        }
    });
});
```

---

### Success Criteria
- [ ] Tất cả actions được log tự động
- [ ] Log records không thể bị chỉnh sửa
- [ ] Activity history hiển thị đầy đủ thông tin
- [ ] Filter và search log hoạt động chính xác
- [ ] Export log thành công
- [ ] Tích hợp thành công với Bitrix24
- [ ] Log archiving hoạt động
- [ ] Performance tốt với large log volumes

---

### Log Retention Rules

#### Log Types và Retention
| Log Type | Retention Period | Archive Policy | Description |
|----------|------------------|----------------|-------------|
| Activity Logs | 7 years | Compressed archive | Main activity records |
| Change Logs | 7 years | Compressed archive | Field change details |
| Audit Logs | 10 years | Encrypted archive | Security audit data |

#### Log Security Rules
- **Immutable Records**: Log records không thể bị chỉnh sửa hoặc xóa
- **Access Control**: Chỉ authorized users mới có thể xem logs
- **Data Encryption**: Sensitive log data được mã hóa
- **Backup Policy**: Logs được backup định kỳ
- **Audit Trail**: Access to logs được ghi lại

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 4 