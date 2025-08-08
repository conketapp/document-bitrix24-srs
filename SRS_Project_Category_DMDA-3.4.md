# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### User Story: DMDA-3.4
### Từ chối Phê duyệt Dự án

#### Thông tin User Story
- **Story ID:** DMDA-3.4
- **Priority:** High
- **Story Points:** 6
- **Sprint:** Sprint 3
- **Status:** To Do
- **Phụ thuộc:** DMDA-3.1, DMDA-4.1 (Cần có gửi phê duyệt và phê duyệt trước)

#### Mô tả User Story
**Với vai trò là** Người Phê duyệt dự án,  
**Tôi muốn** có thể xem thông tin chi tiết của dự án và từ chối phê duyệt dự án đó, đồng thời nhập lý do từ chối,  
**Để** dự án có thể được trả lại cho người khởi tạo để chỉnh sửa hoặc hủy bỏ, và người khởi tạo hiểu được lý do cần thay đổi.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Từ chối Phê duyệt" trên trang chi tiết dự án
- [ ] Người phê duyệt bắt buộc phải nhập lý do từ chối
- [ ] Sau khi từ chối, trạng thái dự án tự động cập nhật (ví dụ: "Đã từ chối" hoặc "Cần chỉnh sửa")
- [ ] Hệ thống ghi lại thông tin người từ chối, lý do và thời gian từ chối
- [ ] Chỉ hiển thị nút từ chối cho dự án có trạng thái "Chờ phê duyệt"
- [ ] Có hộp thoại xác nhận trước khi từ chối
- [ ] Thông báo kết quả từ chối cho người gửi
- [ ] Ghi log hành động từ chối

#### 2.4 Activity Diagram
![DMDA-3.4 Activity Diagram](diagrams/DMDA-3.4%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý từ chối phê duyệt dự án*

---

### Functional Requirements

#### Core Features
1. **Rejection Action**
   - Nút "Từ chối Phê duyệt" cho dự án pending
   - Form bắt buộc nhập lý do từ chối
   - Confirmation dialog trước khi thực hiện
   - Validation lý do từ chối không được để trống

2. **Status Management**
   - Tự động cập nhật trạng thái dự án thành "rejected"
   - Cập nhật thời gian từ chối
   - Ghi log thay đổi trạng thái
   - Sync với Bitrix24

3. **Rejection Tracking**
   - Lưu thông tin người từ chối
   - Lưu lý do từ chối chi tiết
   - Lưu thời gian từ chối
   - Tạo rejection history record

#### Business Rules
- Chỉ dự án có trạng thái "pending_approval" mới có thể được từ chối
- Người từ chối phải có quyền phê duyệt dự án
- Lý do từ chối là bắt buộc và không được để trống
- Không thể từ chối dự án đã được phê duyệt hoặc từ chối trước đó
- Dự án bị từ chối sẽ chuyển về trạng thái "draft" hoặc "rejected"

---

### Technical Specifications

#### Database Schema Updates
```sql
-- Cập nhật bảng project_approvals để hỗ trợ rejection
ALTER TABLE project_approvals 
ADD COLUMN rejection_reason TEXT NOT NULL DEFAULT '',
ADD COLUMN rejection_date TIMESTAMP NULL,
ADD COLUMN rejected_by INT NULL,
ADD FOREIGN KEY (rejected_by) REFERENCES users(id);

-- Bảng lưu lịch sử từ chối chi tiết
CREATE TABLE project_rejection_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    rejected_by INT NOT NULL,
    rejection_reason TEXT NOT NULL,
    rejection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    previous_status VARCHAR(50) NOT NULL,
    additional_notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (rejected_by) REFERENCES users(id)
);

-- Bảng template lý do từ chối
CREATE TABLE rejection_reason_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    reason_code VARCHAR(50) NOT NULL,
    reason_text TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES project_categories(id)
);

-- Index cho performance
CREATE INDEX idx_rejection_history_project ON project_rejection_history(project_id);
CREATE INDEX idx_rejection_history_rejected_by ON project_rejection_history(rejected_by);
CREATE INDEX idx_rejection_templates_category ON rejection_reason_templates(category_id);
```

#### API Endpoints
```
POST /api/projects/{id}/reject
- Request: { 
    rejection_reason: string, 
    additional_notes?: string 
}
- Response: { 
    success: boolean, 
    message: string, 
    new_status: string 
}

GET /api/projects/{id}/rejection-history
- Response: List of rejection history for project

GET /api/rejection-reason-templates
- Response: List of rejection reason templates

POST /api/projects/{id}/request-changes
- Request: { 
    rejection_reason: string, 
    required_changes: string[] 
}
- Response: { 
    success: boolean, 
    message: string 
}
```

#### Data Models
```typescript
interface RejectionRequest {
    rejection_reason: string;
    additional_notes?: string;
    required_changes?: string[];
}

interface RejectionResponse {
    success: boolean;
    message: string;
    new_status: ProjectStatus;
    rejection_date: string;
    rejected_by: User;
}

interface RejectionHistory {
    id: number;
    project_id: number;
    rejected_by: User;
    rejection_reason: string;
    rejection_date: string;
    previous_status: string;
    additional_notes?: string;
}

interface RejectionReasonTemplate {
    id: number;
    category_id: number;
    reason_code: string;
    reason_text: string;
    is_active: boolean;
}

interface ProjectRejectionInfo {
    can_reject: boolean;
    rejection_reasons: RejectionReasonTemplate[];
    previous_rejections: RejectionHistory[];
}
```

---

### User Interface Requirements

#### Project Detail Page with Rejection
```
┌─────────────────────────────────────────────────────────┐
│ Chi tiết Dự án: INV-2024-001                          │
├─────────────────────────────────────────────────────────┤
│ Tên dự án: Dự án đầu tư mới                           │
│ Mã dự án: INV-2024-001                                │
│ Loại: Dự án đầu tư                                     │
│ Năm: 2024                                              │
│ Ngày bắt đầu: 01/03/2024                              │
│ Ngày kết thúc: 31/12/2024                             │
│ Ngân sách: 500,000,000 VND                            │
│ Trạng thái: [Chờ phê duyệt]                           │
│ Loại dự án: [Mới]                                     │
│                                                         │
│ Người tạo: Nguyễn Văn A                               │
│ Ngày tạo: 15/02/2024                                  │
│ Người gửi phê duyệt: Nguyễn Văn A                     │
│ Ngày gửi: 20/02/2024                                  │
│                                                         │
│ [Phê duyệt] [Từ chối] [Yêu cầu chỉnh sửa]            │
└─────────────────────────────────────────────────────────┘
```

#### Rejection Modal
```
┌─────────────────────────────────────┐
│ Từ chối Phê duyệt Dự án            │
├─────────────────────────────────────┤
│ Dự án: INV-2024-001 - Dự án A      │
│                                     │
│ Lý do từ chối *                     │
│ [Dropdown với template reasons]     │
│                                     │
│ Lý do chi tiết *                    │
│ [Textarea - bắt buộc]              │
│                                     │
│ Ghi chú bổ sung (tùy chọn)         │
│ [Textarea]                          │
│                                     │
│ Yêu cầu chỉnh sửa cụ thể            │
│ [Checkbox list]                     │
│ ☐ Cập nhật ngân sách                │
│ ☐ Bổ sung thông tin                 │
│ ☐ Điều chỉnh thời gian              │
│ ☐ Khác: [Text input]                │
│                                     │
│ ⚠️ Lưu ý: Dự án sẽ chuyển về trạng  │
│    thái "Cần chỉnh sửa"             │
│                                     │
│ [Hủy] [Từ chối Phê duyệt]          │
└─────────────────────────────────────┘
```

#### Rejection History
```
┌─────────────────────────────────────┐
│ Lịch sử Từ chối                    │
├─────────────────────────────────────┤
│ 22/02/2024 14:30 - Trần Thị B      │
│ Lý do: Thiếu thông tin chi tiết     │
│ Chi tiết: Cần bổ sung kế hoạch     │
│ thực hiện và timeline cụ thể        │
│                                     │
│ Yêu cầu chỉnh sửa:                  │
│ • Cập nhật ngân sách                │
│ • Bổ sung thông tin                 │
│                                     │
│ Trạng thái trước: Chờ phê duyệt     │
│ Trạng thái sau: Cần chỉnh sửa       │
└─────────────────────────────────────┘
```

#### Success/Error Messages
- **Success**: "Đã từ chối phê duyệt dự án thành công"
- **Error - No Reason**: "Vui lòng nhập lý do từ chối"
- **Error - No Permission**: "Bạn không có quyền từ chối dự án này"
- **Error - Invalid Status**: "Dự án không ở trạng thái chờ phê duyệt"
- **Error - Already Rejected**: "Dự án đã được từ chối trước đó"

---

### Integration Requirements

#### Bitrix24 Integration
- Update deal status thành "REJECTED"
- Create task cho người gửi về lý do từ chối
- Update deal custom fields với thông tin từ chối
- Log rejection action trong Bitrix24 activity feed

#### Notification System
- Email notification cho người gửi về lý do từ chối
- In-app notification cho project manager
- SMS notification (optional) cho urgent rejections
- Rejection summary notification với yêu cầu chỉnh sửa

#### Data Flow
1. Approver access project detail page
2. System validate rejection permissions
3. Display project information và rejection form
4. Approver select rejection reason template
5. Approver enter detailed rejection reason
6. Approver select required changes (optional)
7. Approver click reject button
8. System validate rejection reason
9. System show confirmation dialog
10. Approver confirm rejection
11. System update project status to "rejected"
12. Create rejection history record
13. Sync với Bitrix24
14. Send notifications
15. Log rejection action

---

### Testing Requirements

#### Unit Tests
```typescript
describe('Project Rejection', () => {
    test('should validate rejection reason is required', () => {
        const request = {
            rejection_reason: '',
            additional_notes: 'Test'
        };
        const result = validateRejectionRequest(request);
        expect(result.isValid).toBe(false);
        expect(result.errors).toContain('Lý do từ chối là bắt buộc');
    });

    test('should process rejection correctly', async () => {
        const projectId = 1;
        const rejectedBy = 1;
        const request = {
            rejection_reason: 'Thiếu thông tin chi tiết',
            additional_notes: 'Cần bổ sung kế hoạch thực hiện'
        };
        
        await processRejection(projectId, rejectedBy, request);
        
        const project = await getProject(projectId);
        expect(project.status).toBe('rejected');
        
        const rejection = await getRejectionHistory(projectId);
        expect(rejection.rejection_reason).toBe('Thiếu thông tin chi tiết');
        expect(rejection.rejected_by).toBe(rejectedBy);
    });

    test('should handle rejection with required changes', async () => {
        const request = {
            rejection_reason: 'Cần điều chỉnh',
            required_changes: ['Cập nhật ngân sách', 'Bổ sung thông tin']
        };
        
        const result = await processRejection(1, 1, request);
        expect(result.success).toBe(true);
        expect(result.new_status).toBe('rejected');
    });
});
```

#### Integration Tests
- Test Bitrix24 sync cho rejection actions
- Test notification system cho rejection results
- Test permission system cho rejection
- Test rejection workflow với required changes

#### User Acceptance Tests
- Test rejection workflow end-to-end
- Test rejection reason validation
- Test required changes selection
- Test rejection history display
- Test permission validation

#### 5.5 Sequence Diagram
![DMDA-3.4 Sequence Diagram](diagrams/DMDA-3.4%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi từ chối phê duyệt dự án*

---

### Success Criteria
- [ ] Approver có thể từ chối dự án với lý do bắt buộc
- [ ] Nút từ chối hiển thị đúng cho dự án pending
- [ ] Rejection workflow hoạt động chính xác
- [ ] Status update tự động sau khi từ chối
- [ ] Rejection history được ghi lại đầy đủ
- [ ] Tích hợp thành công với Bitrix24
- [ ] Notification system hoạt động
- [ ] Permission system hoạt động chính xác

---

### Rejection Workflow Rules

#### Rejection Reasons
| Reason Code | Reason Text | Category | Required Changes |
|-------------|-------------|----------|------------------|
| INSUFFICIENT_INFO | Thiếu thông tin chi tiết | All | Bổ sung thông tin |
| BUDGET_ISSUE | Vấn đề về ngân sách | All | Cập nhật ngân sách |
| TIMELINE_ISSUE | Vấn đề về thời gian | All | Điều chỉnh timeline |
| TECHNICAL_ISSUE | Vấn đề kỹ thuật | Technical | Rà soát kỹ thuật |
| COMPLIANCE_ISSUE | Vấn đề tuân thủ | All | Cập nhật tuân thủ |

#### Rejection Actions
| Action | Description | Status Change | Required Fields |
|--------|-------------|---------------|-----------------|
| Reject | Từ chối dự án | pending_approval → rejected | Rejection reason |
| Request Changes | Yêu cầu chỉnh sửa | pending_approval → edit_requested | Required changes |

#### Rejection Validation Rules
- **Project Status**: Chỉ dự án pending_approval mới có thể bị từ chối
- **Rejection Permission**: Người từ chối phải có quyền phê duyệt dự án
- **Reason Required**: Lý do từ chối là bắt buộc và không được để trống
- **Reason Length**: Lý do từ chối phải có ít nhất 10 ký tự
- **No Duplicate Rejection**: Không thể từ chối dự án đã bị từ chối trước đó

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 3 