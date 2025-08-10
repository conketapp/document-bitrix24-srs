# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### 1. Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Date:** 07-2025  
**Author:** Công ty Thiên Phú Digital  

### 2. Mô tả Epic
Epic này tập trung vào việc phát triển hệ thống quản lý danh mục dự án, cho phép cán bộ quản lý dự án tổ chức và quản lý các dự án theo năm và phân loại một cách hiệu quả.

---

## User Story: DMDA-1.2
### Tự động Phân biệt Dự án Chuyển tiếp và Dự án Mới

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-1.2
- **Priority:** High
- **Story Points:** 5
- **Sprint:** Sprint 1
- **Status:** To Do
- **Dependencies:** DMDA-1.1 (Cần có danh sách dự án trước)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** các dự án trong danh mục được hệ thống tự động phân biệt và đánh dấu là "Dự án Chuyển tiếp" (dự án từ năm trước chưa hoàn thành) hoặc "Dự án Mới" (dự án bắt đầu trong năm hiện tại),  
**Để** tôi có thể nhanh chóng xác định nguồn gốc và tình trạng liên tục của dự án phục vụ công tác báo cáo và quản lý ngân sách mà không cần nhập liệu thủ công.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Hệ thống tự động gán trạng thái "Chuyển tiếp" hoặc "Mới" dựa trên năm tạo dự án và năm hiện tại
- [ ] "Dự án Mới" nếu năm tạo = năm hiện tại
- [ ] "Dự án Chuyển tiếp" nếu năm tạo < năm hiện tại và trạng thái ≠ "approved"
- [ ] Thông tin này hiển thị rõ ràng trong danh sách dự án và chi tiết dự án
- [ ] Người dùng không thể chỉnh sửa thủ công trường này
- [ ] Hệ thống tự động cập nhật khi năm tạo hoặc trạng thái dự án thay đổi

#### 2.4 Activity Diagram
![DMDA-1.2 Activity Diagram](diagrams/DMDA-1.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tự động phân loại dự án*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Tự động Phân loại Dự án**
   - Logic phân loại tự động dựa trên ngày bắt đầu
   - Cập nhật real-time khi có thay đổi
   - Không cho phép chỉnh sửa thủ công

2. **Quy tắc Phân loại**
   - **Dự án Mới**: YEAR(created_at) = current_year
   - **Dự án Chuyển tiếp**: YEAR(created_at) < current_year AND status ≠ "approved"

3. **Hiển thị Thông tin**
   - Badge/Label rõ ràng trong danh sách
   - Màu sắc phân biệt
   - Tooltip giải thích logic phân loại

#### 3.2 Business Rules
- Phân loại được tính toán tự động, không thể chỉnh sửa
- Cập nhật ngay khi năm tạo hoặc trạng thái thay đổi
- Dự án đã phê duyệt không được phân loại là "Chuyển tiếp"
- Năm hiện tại được lấy từ hệ thống

#### 3.3 Validation Rules
**Validation cho Phân loại Dự án:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| Loại dự án | projectType | ENUM | 'new' hoặc 'carryover' | ✅ |
| Ngày bắt đầu | startDate | Date | Định dạng YYYY-MM-DD | ✅ |
| Trạng thái dự án | status | ENUM | 'initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested' | ✅ |
| Năm hiện tại | currentYear | Number | Lấy từ hệ thống | ✅ |

**Logic Phân loại:**
| Điều kiện | Kết quả | Validation |
|-----------|---------|------------|
| YEAR(created_at) = currentYear | Dự án Mới | projectType = 'new' |
| YEAR(created_at) < currentYear AND status ≠ 'approved' | Dự án Chuyển tiếp | projectType = 'carryover' |
| status = 'approved' | Dự án Mới | projectType = 'new' |

**Validation cho Database:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| project_type | ENUM | Text | 'new', 'carryover', NOT NULL | ✅ |
| created_at | TIMESTAMP | DateTime | NOT NULL | ✅ |
| status | ENUM | Text | 'initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested' | ✅ |

**Quy tắc chung:**
- Phân loại được tính toán tự động, không thể chỉnh sửa thủ công
- Cập nhật real-time khi có thay đổi năm tạo hoặc trạng thái
- Dự án đã phê duyệt luôn được phân loại là "Mới"
- Năm hiện tại được lấy từ hệ thống, không phụ thuộc vào user input

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian tính toán phân loại < 100ms
- Không ảnh hưởng đến performance của danh sách dự án
- Cập nhật real-time không gây lag

#### 4.2 Usability
- Badge/Label dễ nhận biết
- Màu sắc có độ tương phản tốt
- Tooltip hướng dẫn rõ ràng
- Responsive trên mobile

#### 4.3 Data Integrity
- Phân loại luôn chính xác theo quy tắc
- Không có trường hợp "undefined" hoặc "null"
- Logging để audit trail

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Thêm trường project_type vào bảng projects
ALTER TABLE projects ADD COLUMN project_type ENUM('new', 'carryover') NOT NULL DEFAULT 'new';

-- Thêm index để tối ưu query
CREATE INDEX idx_projects_start_date ON projects(start_date);
CREATE INDEX idx_projects_type_status ON projects(project_type, status);

-- Trigger để tự động cập nhật project_type
DELIMITER //
CREATE TRIGGER update_project_type
BEFORE INSERT ON projects
FOR EACH ROW
BEGIN
    SET NEW.project_type = CASE
        WHEN YEAR(NEW.start_date) = YEAR(CURDATE()) THEN 'new'
        WHEN YEAR(NEW.start_date) < YEAR(CURDATE()) AND NEW.status != 'completed' THEN 'carryover'
        ELSE 'new'
    END;
END//

CREATE TRIGGER update_project_type_on_update
BEFORE UPDATE ON projects
FOR EACH ROW
BEGIN
    SET NEW.project_type = CASE
        WHEN YEAR(NEW.start_date) = YEAR(CURDATE()) THEN 'new'
        WHEN YEAR(NEW.start_date) < YEAR(CURDATE()) AND NEW.status != 'completed' THEN 'carryover'
        ELSE 'new'
    END;
END//
DELIMITER ;
```

#### 5.2 API Endpoints
```
GET /api/projects
- Parameters: year (optional), category_id (optional), project_type (optional)
- Response: List of projects with project_type field

GET /api/projects/{id}
- Response: Project details with project_type field

PUT /api/projects/{id}
- Note: project_type field is read-only, cannot be modified
```

#### 5.3 Data Models
```typescript
interface Project {
    id: number;
    name: string;
    start_date: string;
    end_date?: string;
    status: 'active' | 'completed' | 'cancelled';
    project_type: 'new' | 'carryover'; // Auto-calculated
    year: number;
    category_id: number;
    budget?: number;
    created_at: string;
    updated_at: string;
}

interface ProjectTypeConfig {
    new: {
        label: 'Dự án Mới';
        icon: 'plus-circle';
    };
    carryover: {
        label: 'Dự án Chuyển tiếp';
        icon: 'arrow-right';
    };
}
```

#### 5.4 Sequence Diagram
![DMDA-1.2 Sequence Diagram](diagrams/DMDA-1.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các component trong hệ thống*

#### 5.5 UI Components
- ProjectTypeBadge: Hiển thị badge phân loại
- ProjectTypeFilter: Filter theo loại dự án
- ProjectTypeTooltip: Tooltip giải thích logic
- ProjectTypeIndicator: Indicator trong project card

---

### 6. Integration Requirements

#### 6.1 Bitrix24 Integration
- Đồng bộ trường project_type với Bitrix24
- Mapping: project_type → custom field trong Bitrix24
- Real-time sync khi có thay đổi

#### 6.2 Data Flow
1. User tạo/cập nhật dự án
2. System tự động tính toán project_type
3. Lưu vào database
4. Sync với Bitrix24
5. Hiển thị badge trong UI

---

### 7. User Interface Requirements

#### 7.1 Visual Design
- **Dự án Mới**: Badge phân loại
- **Dự án Chuyển tiếp**: Badge phân loại
- Icon tương ứng cho mỗi loại
- Tooltip hiển thị logic phân loại

#### 7.2 Layout Integration
- Badge hiển thị bên cạnh tên dự án
- Filter dropdown thêm option "Loại dự án"
- Column trong table view
- Detail view hiển thị rõ ràng

#### 7.3 Responsive Design
- Badge responsive trên mobile
- Tooltip touch-friendly
- Filter dropdown mobile-friendly

---

### 8. Testing Requirements

#### 8.1 Unit Tests
```typescript
describe('Phân loại Loại Dự án', () => {
    test('nên phân loại là dự án mới khi start_date là năm hiện tại', () => {
        const project = {
            start_date: '2024-01-15',
            status: 'active'
        };
        expect(classifyProjectType(project)).toBe('new');
    });

    test('nên phân loại là dự án chuyển tiếp khi start_date là năm trước và chưa hoàn thành', () => {
        const project = {
            start_date: '2023-06-01',
            status: 'active'
        };
        expect(classifyProjectType(project)).toBe('carryover');
    });

    test('không nên phân loại là dự án chuyển tiếp khi dự án đã hoàn thành', () => {
        const project = {
            start_date: '2023-06-01',
            status: 'completed'
        };
        expect(classifyProjectType(project)).toBe('new');
    });
});
```

#### 8.2 Integration Tests
- Kiểm tra database triggers
- Kiểm tra API endpoints
- Kiểm tra đồng bộ Bitrix24

#### 8.3 User Acceptance Tests
- Kiểm tra phân loại tự động
- Kiểm tra hiển thị UI
- Kiểm tra chức năng filter
- Kiểm tra hành vi chỉ đọc

---

### 9. Deployment Requirements

#### 9.1 Database Migration
```sql
-- Migration script
BEGIN;
ALTER TABLE projects ADD COLUMN project_type ENUM('new', 'carryover') NOT NULL DEFAULT 'new';
CREATE INDEX idx_projects_start_date ON projects(start_date);
CREATE INDEX idx_projects_type_status ON projects(project_type, status);
-- Create triggers
-- Update existing data
UPDATE projects SET project_type = CASE
    WHEN YEAR(start_date) = YEAR(CURDATE()) THEN 'new'
    WHEN YEAR(start_date) < YEAR(CURDATE()) AND status != 'completed' THEN 'carryover'
    ELSE 'new'
END;
COMMIT;
```

#### 9.2 Environment Configuration
- Cấu hình năm hiện tại
- Cài đặt timezone
- Mapping trường Bitrix24

---

### 10. Success Criteria
- [ ] Hệ thống tự động phân loại chính xác 100%
- [ ] UI hiển thị rõ ràng và dễ hiểu
- [ ] Performance không bị ảnh hưởng
- [ ] Tích hợp thành công với Bitrix24
- [ ] Tất cả test cases pass
- [ ] User không thể chỉnh sửa thủ công

---

### 11. Risks and Mitigation

#### 11.1 Technical Risks
- **Risk:** Vấn đề hiệu suất database trigger
- **Mitigation:** Tối ưu indexes và batch updates

- **Risk:** Vấn đề timezone ảnh hưởng tính toán năm
- **Mitigation:** Sử dụng UTC và xử lý timezone đúng cách

- **Risk:** Xung đột đồng bộ Bitrix24
- **Mitigation:** Triển khai chiến lược giải quyết xung đột

#### 11.2 Business Risks
- **Risk:** Người dùng bối rối về logic phân loại
- **Mitigation:** Tài liệu rõ ràng và tooltips

- **Risk:** Dữ liệu không nhất quán trong quá trình migration
- **Mitigation:** Kiểm tra kỹ lưỡng và kế hoạch rollback

---

### 12. Future Enhancements
- Quy tắc phân loại nâng cao (theo quý, năm tài chính)
- Nhãn phân loại tùy chỉnh
- Theo dõi lịch sử phân loại
- Cập nhật phân loại hàng loạt
- Phân tích và báo cáo phân loại

---

### 13. Dependencies
- **DMDA-1.1**: Cần có danh sách dự án trước
- **Database schema**: Cần thêm trường project_type
- **Bitrix24 API**: Cần custom field mapping
- **UI Components**: Cần badge và filter components

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 2 