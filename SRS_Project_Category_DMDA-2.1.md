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

## User Story: DMDA-2.1
### Tạo Dự án Mới trong Danh mục

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-2.1
- **Priority:** High
- **Story Points:** 8
- **Sprint:** Sprint 2
- **Status:** To Do
- **Dependencies:** DMDA-1.1, DMDA-1.2, DMDA-1.3 (Cần có danh sách dự án, phân loại và mã tự sinh)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** có thể dễ dàng tạo một dự án mới trực tiếp trong danh mục dự án,  
**Để** tôi có thể bắt đầu nhập các thông tin cần thiết và đưa dự án vào quy trình quản lý.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có nút/chức năng "Tạo Dự án Mới"
- [ ] Form tạo dự án bao gồm các trường thông tin cơ bản
- [ ] Mã dự án được tự động sinh theo logic DMDA-1.3
- [ ] Phân loại dự án được tự động tính toán theo DMDA-1.2
- [ ] Validation đầy đủ cho tất cả trường bắt buộc
- [ ] Lưu dự án thành công và hiển thị trong danh sách
- [ ] Tích hợp với Bitrix24 khi tạo dự án

#### 2.4 Activity Diagram
![DMDA-2.1 Activity Diagram](diagrams/DMDA-2.1%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tạo dự án mới trong danh mục*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Nút Tạo Dự án Mới**
   - Button "Tạo Dự án Mới" ở header hoặc floating action button
   - Modal hoặc trang riêng để tạo dự án
   - Responsive design cho mobile

2. **Form Tạo Dự án**
   - **Thông tin cơ bản**:
     - Tên dự án (projectName) - Bắt buộc
     - Người đầu mối QLDA (projectManager) - Bắt buộc
     - Phòng đầu mối lập dự án (projectDepartment) - Bắt buộc
     - Người đầu mối lập DA (projectCreator) - Bắt buộc
     - Loại dự án (projectType) - Bắt buộc
       - Dự án đầu tư
       - Mua sắm tài sản
       - Thuê dịch vụ
       - Bảo trì
       - Khác

   - **Thông tin bổ sung**:
     - Nguồn vốn (fundingSource)
       - Mua sắm tài sản cố định
       - Đầu tư phát triển
       - Chi phí vận hành
       - Chi phí bảo trì
       - Khác
     - Đề án chiến lược:
       - Thuộc đề án chiến lược (isStrategicProject) - Checkbox
       - Đề án chiến lược (strategicProject) - Text input (hiện khi checkbox được chọn)

   - **Tổng mức đầu tư & Kế hoạch vốn**:
     - TMĐT dự kiến theo KHV (plannedBudget) - Bắt buộc
     - TMĐT theo QĐ phê duyệt CTĐT (investmentApprovalBudget)
     - TMĐT theo QĐ phê duyệt dự án (projectApprovalBudget)
     - KHV trong năm (yearlyBudget)
     - KHV năm sau (nextYearPlan)

   - **Các mốc phê duyệt và quyết định**:
     - Quyết định chủ trương đầu tư:
       - Số quyết định (investmentDecisionNumber)
       - Ngày quyết định (investmentDecisionDate)
       - Số tháng thực hiện (investmentDecisionDuration)
       - Tài liệu QĐ chủ trương đầu tư (investmentDecisionFile) - File upload
     - Quyết định phê duyệt dự án:
       - Số quyết định (projectApprovalNumber)
       - Ngày quyết định (projectApprovalDate)
       - Số tháng thực hiện (projectApprovalDuration)
       - Tài liệu QĐ phê duyệt dự án (projectApprovalFile) - File upload
     - Quyết định quyết toán:
       - Số quyết định (settlementDecisionNumber)
       - Ngày quyết định (settlementDecisionDate)
       - Tài liệu QĐ quyết toán (settlementDecisionFile) - File upload

   - **Thông tin tự động**:
     - Mã dự án (projectCode) - Tự sinh theo DMDA-1.3
     - Phân loại dự án (projectType) - Tự động theo DMDA-1.2
     - Ngày tạo dự án
     - Người tạo dự án

3. **Validation Rules**

   **Thông tin cơ bản (bắt buộc):**
   | Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
   |--------|-----------|---------------|------------|----------|
   | Tên dự án | projectName | Text | 3-255 ký tự | ✅ |
   | Người đầu mối QLDA | projectManager | Text | Không được để trống | ✅ |
   | Phòng đầu mối lập dự án | projectDepartment | Dropdown | Phải chọn từ danh sách | ✅ |
   | Người đầu mối lập DA | projectCreator | Text | Không được để trống | ✅ |
   | Loại dự án | projectType | Dropdown | Phải chọn từ danh sách | ✅ |

   **Thông tin bổ sung (tùy chọn):**
   | Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
   |--------|-----------|---------------|------------|----------|
   | Nguồn vốn | fundingSource | Dropdown | Phải chọn từ danh sách nếu có | ❌ |
   | Thuộc đề án chiến lược | isStrategicProject | Checkbox | Boolean value | ❌ |
   | Đề án chiến lược | strategicProject | Text | Tối đa 500 ký tự, hiện khi checkbox được chọn | ❌ |

   **Tổng mức đầu tư & Kế hoạch vốn:**
   | Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
   |--------|-----------|---------------|------------|----------|
   | TMĐT dự kiến theo KHV | plannedBudget | Number | Số dương, định dạng tiền tệ | ✅ |
   | TMĐT theo QĐ phê duyệt CTĐT | investmentApprovalBudget | Number | Số dương nếu có, định dạng tiền tệ | ❌ |
   | TMĐT theo QĐ phê duyệt dự án | projectApprovalBudget | Number | Số dương nếu có, định dạng tiền tệ | ❌ |
   | KHV trong năm | yearlyBudget | Number | Số dương nếu có, định dạng tiền tệ | ❌ |
   | KHV năm sau | nextYearPlan | Number | Số dương nếu có, định dạng tiền tệ | ❌ |

   **Các mốc phê duyệt và quyết định:**

   **Quyết định chủ trương đầu tư:**
   | Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
   |--------|-----------|---------------|------------|----------|
   | Số quyết định | investmentDecisionNumber | Text | Tối đa 100 ký tự | ❌ |
   | Ngày quyết định | investmentDecisionDate | Date | DD/MM/YYYY, phải hợp lệ | ❌ |
   | Số tháng thực hiện | investmentDecisionDuration | Number | Số nguyên dương, 1-120 tháng | ❌ |
   | Tài liệu QĐ | investmentDecisionFile | File | PDF, DOC, DOCX, tối đa 10MB | ❌ |

   **Quyết định phê duyệt dự án:**
   | Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
   |--------|-----------|---------------|------------|----------|
   | Số quyết định | projectApprovalNumber | Text | Tối đa 100 ký tự | ❌ |
   | Ngày quyết định | projectApprovalDate | Date | DD/MM/YYYY, phải hợp lệ | ❌ |
   | Số tháng thực hiện | projectApprovalDuration | Number | Số nguyên dương, 1-120 tháng | ❌ |
   | Tài liệu QĐ | projectApprovalFile | File | PDF, DOC, DOCX, tối đa 10MB | ❌ |

   **Quyết định quyết toán:**
   | Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
   |--------|-----------|---------------|------------|----------|
   | Số quyết định | settlementDecisionNumber | Text | Tối đa 100 ký tự | ❌ |
   | Ngày quyết định | settlementDecisionDate | Date | DD/MM/YYYY, phải hợp lệ | ❌ |
   | Tài liệu QĐ | settlementDecisionFile | File | PDF, DOC, DOCX, tối đa 10MB | ❌ |

   **Quy tắc chung:**
   - Ngày quyết định không được trong tương lai
   - Số tháng thực hiện phải hợp lý (1-120 tháng)
   - File upload chỉ chấp nhận định dạng PDF, DOC, DOCX
   - Kích thước file tối đa 10MB
   - Số tiền phải là số dương và hợp lệ

#### 3.2 Business Rules
- Dự án mới mặc định có trạng thái "initialized"
- Mã dự án được sinh tự động và không thể chỉnh sửa
- Phân loại dự án được tính toán tự động
- Người tạo dự án được ghi nhận
- Dự án được đồng bộ với Bitrix24

---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian mở form < 1 giây
- Thời gian lưu dự án < 3 giây
- Form responsive trên mobile
- Real-time validation không lag

#### 4.2 Usability
- Form layout rõ ràng và dễ sử dụng
- Validation messages rõ ràng
- Auto-save draft (tùy chọn)
- Keyboard navigation support
- Loading states rõ ràng

#### 4.3 Security
- Xác thực người dùng trước khi tạo
- Phân quyền theo vai trò
- Sanitize input data
- CSRF protection

---

### 5. Technical Specifications

#### 5.1 Database Schema
```sql
-- Bảng dự án (đã có, cập nhật thêm)
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    project_source VARCHAR(100) NOT NULL,
    planned_budget DECIMAL(15,2),
    approved_budget DECIMAL(15,2),
    total_disbursed DECIMAL(15,2) DEFAULT 0,
    current_year_disbursed DECIMAL(15,2) DEFAULT 0,
    expected_disbursement DECIMAL(15,2),
    next_year_plan DECIMAL(15,2),
    status ENUM('initialized', 'pending_approval', 'approved', 'rejected', 'suspended', 'edit_requested') DEFAULT 'initialized',
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Bảng draft projects (tùy chọn)
CREATE TABLE project_drafts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    draft_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 5.2 API Endpoints
```
POST /api/projects
- Request: {
    name: string,
    project_source: string,
    planned_budget?: number,
    approved_budget?: number,
    total_disbursed?: number,
    current_year_disbursed?: number,
    expected_disbursement?: number,
    next_year_plan?: number
}
- Response: Project object with auto-generated fields

GET /api/project-categories
- Response: List of available categories

POST /api/projects/draft
- Request: Draft data
- Response: Draft saved successfully

GET /api/projects/draft/{id}
- Response: Draft data for editing
```

#### 5.3 Data Models
```typescript
interface CreateProjectRequest {
    name: string;
    project_source: string;
    planned_budget?: number;
    approved_budget?: number;
    total_disbursed?: number;
    current_year_disbursed?: number;
    expected_disbursement?: number;
    next_year_plan?: number;
}

interface Project {
    id: number;
    project_code: string; // Auto-generated
    name: string;
    project_source: string;
    planned_budget?: number;
    approved_budget?: number;
    total_disbursed: number;
    current_year_disbursed: number;
    expected_disbursement?: number;
    next_year_plan?: number;
    status: 'initialized' | 'pending_approval' | 'approved' | 'rejected' | 'suspended' | 'edit_requested';
    created_by: number;
    created_by_name: string;
    created_at: string;
    updated_at: string;
}

interface ProjectFormData {
    name: string;
    project_source: string;
    planned_budget: string;
    approved_budget: string;
    total_disbursed: string;
    current_year_disbursed: string;
    expected_disbursement: string;
    next_year_plan: string;
}
```

#### 5.4 Sequence Diagram
![DMDA-2.1 Sequence Diagram](diagrams/DMDA-2.1%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các component trong hệ thống*

#### 5.5 UI Components
- CreateProjectButton: Nút tạo dự án mới
- ProjectForm: Form tạo/chỉnh sửa dự án
- ProjectFormModal: Modal chứa form
- FormValidation: Validation logic
- LoadingState: Trạng thái loading
- SuccessMessage: Thông báo thành công

---

### 6. Integration Requirements

#### 6.1 Bitrix24 Integration
- Tạo deal/lead trong Bitrix24 khi tạo dự án
- Mapping fields:
  - project_code → custom field
  - name → title
  - project_source → custom field
  - planned_budget → amount
  - approved_budget → custom field
  - total_disbursed → custom field
  - current_year_disbursed → custom field
  - expected_disbursement → custom field
  - next_year_plan → custom field
  - status → stage
  - created_at → date_create
  - created_by → assigned_by_id

#### 6.2 Data Flow
1. User nhấn "Tạo Dự án Mới"
2. System mở form với validation
3. User nhập thông tin và submit
4. System validate và tạo dự án
5. Tự động sinh project_code và project_type
6. Lưu vào database
7. Đồng bộ với Bitrix24
8. Chuyển hướng đến danh sách dự án hoặc chi tiết

---

### 7. User Interface Requirements

#### 7.1 Form Layout
- Form tạo dự án được chia thành 4 section chính:
  1. **Thông tin cơ bản**: Tên dự án, người quản lý, phòng ban, loại dự án
  2. **Thông tin bổ sung**: Nguồn vốn, đề án chiến lược
  3. **Tổng mức đầu tư & Kế hoạch vốn**: TMĐT dự kiến, TMĐT phê duyệt, vốn đã ứng, kế hoạch vốn
  4. **Các mốc phê duyệt và quyết định**: Quyết định chủ trương, phê duyệt dự án, quyết toán
- Form có validation real-time và hiển thị lỗi rõ ràng
- Responsive design cho mobile và desktop

#### 7.2 Design Guidelines
- Sử dụng Tailwind CSS cho styling
- Form validation real-time
- Error messages rõ ràng
- Success feedback
- Responsive design

#### 7.3 User Experience
- Tự động focus vào field đầu tiên
- Điều hướng bằng Tab
- Phím tắt (Ctrl+S để lưu)
- Tự động lưu bản nháp (tùy chọn)
- Dialog xác nhận khi hủy

---

### 8. Testing Requirements

#### 8.1 Unit Tests
```typescript
describe('Tạo Dự án', () => {
    test('nên tạo dự án với dữ liệu hợp lệ', async () => {
        const projectData = {
            name: 'Test Project',
            category_id: 1,
            year: 2024,
            start_date: '2024-01-01'
        };
        
        const result = await createProject(projectData);
        expect(result.project_code).toMatch(/^[A-Z]{3}-2024-\d{3}$/);
        expect(result.project_type).toBe('new');
    });

    test('nên validate các trường bắt buộc', async () => {
        const invalidData = {
            name: '',
            category_id: 0
        };
        
        await expect(createProject(invalidData))
            .rejects.toThrow('Validation failed');
    });

    test('nên sinh mã dự án duy nhất', async () => {
        const project1 = await createProject(validData);
        const project2 = await createProject(validData);
        
        expect(project1.project_code).not.toBe(project2.project_code);
    });
});
```

#### 8.2 Integration Tests
- Test form submission
- Test Bitrix24 sync
- Test validation rules
- Test error handling

#### 8.3 User Acceptance Tests
- Test form usability
- Test validation messages
- Test success flow
- Test mobile responsiveness

---

### 9. Deployment Requirements

#### 9.1 Environment Setup
- Form components deployment
- API endpoints deployment
- Database migration
- Bitrix24 integration setup

#### 9.2 Configuration
- Form validation rules
- Auto-save settings
- Bitrix24 field mapping
- Error message templates

---

### 10. Success Criteria
- [ ] User có thể tạo dự án mới dễ dàng
- [ ] Form validation hoạt động chính xác
- [ ] Mã dự án được sinh tự động
- [ ] Phân loại dự án được tính toán đúng
- [ ] Tích hợp thành công với Bitrix24
- [ ] UI/UX thân thiện và responsive
- [ ] Tất cả test cases pass

---

### 11. Rủi ro và Giải pháp

#### 11.1 Rủi ro Kỹ thuật
- **Rủi ro:** Độ phức tạp của validation form
- **Giải pháp:** Sử dụng thư viện form và kiểm thử toàn diện

- **Rủi ro:** Lỗi đồng bộ với Bitrix24
- **Giải pháp:** Triển khai logic thử lại và xử lý lỗi

- **Rủi ro:** Xung đột khi tạo dự án đồng thời
- **Giải pháp:** Sử dụng transaction database và khóa

#### 11.2 Rủi ro Nghiệp vụ
- **Rủi ro:** Lỗi nhập liệu từ người dùng
- **Giải pháp:** Thông báo validation rõ ràng và tự động lưu

- **Rủi ro:** Vấn đề hiệu suất với form lớn
- **Giải pháp:** Tối ưu hóa render form và lazy loading

- **Rủi ro:** Mất dữ liệu khi người dùng chưa lưu
- **Giải pháp:** Tự động lưu bản nháp và cảnh báo khi rời trang

- **Rủi ro:** Người dùng không hiểu cách sử dụng form
- **Giải pháp:** Cung cấp hướng dẫn và tooltip chi tiết

---

### 12. Future Enhancements
- Bulk project creation
- Project templates
- Advanced form validation
- Auto-complete suggestions
- Project duplication
- Import from Excel/CSV

---

### 13. Dependencies
- **DMDA-1.1**: Cần có danh sách dự án
- **DMDA-1.2**: Cần phân loại dự án tự động
- **DMDA-1.3**: Cần mã dự án tự sinh
- **UI Components**: Form components
- **Bitrix24 API**: Integration endpoints

---



---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Next Review:** Sprint 2 