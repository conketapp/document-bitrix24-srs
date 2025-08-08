# Software Requirements Specification (SRS)
## Epic: Danh mục dự án - Quản lý Danh mục Dự án

### 1. Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Version:** 1.0  
**Date:** 2024  
**Author:** Development Team  

### 2. Mô tả Epic
Epic này tập trung vào việc phát triển hệ thống quản lý danh mục dự án, cho phép cán bộ quản lý dự án tổ chức và quản lý các dự án theo năm và phân loại một cách hiệu quả.

---

## User Story: DMDA-1.3
### Mã Dự án Tự sinh theo Logic

#### 2.1 Thông tin User Story
- **Story ID:** DMDA-1.3
- **Priority:** High
- **Story Points:** 3
- **Sprint:** Sprint 1
- **Status:** To Do
- **Dependencies:** DMDA-1.1 (Cần có danh sách dự án và loại dự án)

#### 2.2 Mô tả User Story
**Với vai trò là** Cán bộ quản lý dự án,  
**Tôi muốn** mã dự án được tự động sinh ra theo một logic cụ thể (ví dụ: [Năm]-[Phòng]-[Loại]-[STT]) khi tạo dự án mới với đầy đủ thông tin,  
**Để** tôi có thể dễ dàng nhận diện dự án, đảm bảo tính nhất quán và tránh trùng lặp mã dự án.

#### 2.3 Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Mã dự án được sinh tự động ngay khi tạo dự án mới
- [ ] Mã dự án là duy nhất trong toàn hệ thống
- [ ] Format mã dự án: [Mã Loại Dự án]-[Năm]-[Số thứ tự]
- [ ] Số thứ tự được reset mỗi năm
- [ ] Mã dự án không thể chỉnh sửa sau khi tạo
- [ ] Hệ thống xử lý được trường hợp trùng lặp

#### 2.4 Activity Diagram
![DMDA-1.3 Activity Diagram](diagrams/DMDA-1.3%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý tự động sinh mã dự án*

---

### 3. Functional Requirements

#### 3.1 Core Features
1. **Tự động Sinh Mã Dự án**
   - Logic sinh mã: [Năm]-[Phòng]-[Loại]-[STT]
   - Sinh ngay khi tạo dự án mới với đầy đủ thông tin
   - Đảm bảo tính duy nhất

2. **Format Mã Dự án**
   - **Năm**: 4 chữ số (2024, 2025, v.v.)
   - **Phòng**: Mã phòng ban (IT, HR, FIN, v.v.)
   - **Loại**: Mã loại dự án (INV, PUR, SER, MAI, OTH)
   - **STT**: 3 chữ số, bắt đầu từ 001

3. **Quy tắc Sinh Mã**
   - **Đầu tư**: 2024-IT-INV-001, 2024-IT-INV-002, v.v.
   - **Mua sắm**: 2024-IT-PUR-001, 2024-IT-PUR-002, v.v.
   - **Thuê dịch vụ**: 2024-IT-SER-001, 2024-IT-SER-002, v.v.
   - **Bảo trì**: 2024-IT-MAI-001, 2024-IT-MAI-002, v.v.
   - **Khác**: 2024-IT-OTH-001, 2024-IT-OTH-002, v.v.

#### 3.2 Business Rules
- Mã dự án được sinh tự động, không thể chỉnh sửa
- Số thứ tự reset về 001 mỗi năm mới
- Mã dự án phải duy nhất trong toàn hệ thống
- Format mã phải nhất quán và dễ đọc

#### 3.3 Validation Rules
**Validation cho Mã Dự án:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| Mã dự án | projectCode | Text | Format: [Năm]-[Phòng]-[Loại]-[STT], duy nhất | ✅ |
| Năm | year | Number | 4 chữ số (2024, 2025, v.v.) | ✅ |
| Phòng ban | department | Text | Mã phòng ban hợp lệ (IT, HR, FIN, v.v.) | ✅ |
| Loại dự án | category | Text | Mã loại dự án hợp lệ (INV, PUR, SER, MAI, OTH) | ✅ |
| Số thứ tự | sequence | Number | 3 chữ số, bắt đầu từ 001 | ✅ |

**Validation cho Database:**
| Trường | Tên Field | Kiểu dữ liệu | Validation | Bắt buộc |
|--------|-----------|---------------|------------|----------|
| project_code | VARCHAR(20) | Text | UNIQUE, NOT NULL | ✅ |
| category_code | VARCHAR(3) | Text | UNIQUE, NOT NULL | ✅ |
| current_sequence | INT | Number | NOT NULL, DEFAULT 0 | ✅ |

**Quy tắc chung:**
- Mã dự án phải duy nhất trong toàn hệ thống
- Số thứ tự phải tăng dần theo thứ tự tạo
- Format mã phải nhất quán: [Năm]-[Phòng]-[Loại]-[STT]
- Ví dụ: 2024-IT-INV-001, 2024-IT-INV-002, v.v.



---

### 4. Non-Functional Requirements

#### 4.1 Performance
- Thời gian sinh mã < 50ms
- Không ảnh hưởng đến performance tạo dự án
- Xử lý concurrent requests an toàn

#### 4.2 Data Integrity
- Mã dự án luôn duy nhất
- Không có trường hợp trùng lặp
- Atomic transaction khi tạo dự án

#### 4.3 Usability
- Mã dự án dễ đọc và nhớ
- Format nhất quán
- Hiển thị rõ ràng trong UI

---

### 5. Technical Specifications

#### 5.1 Database Schema Updates
```sql
-- Thêm trường project_code vào bảng projects
ALTER TABLE projects ADD COLUMN project_code VARCHAR(20) NOT NULL UNIQUE;

-- Thêm trường category_code vào bảng project_categories
ALTER TABLE project_categories ADD COLUMN code VARCHAR(3) NOT NULL UNIQUE;

-- Thêm index để tối ưu query
CREATE INDEX idx_projects_code ON projects(project_code);
CREATE INDEX idx_projects_year_category ON projects(year, category_id);

-- Bảng để track sequence numbers
CREATE TABLE project_sequences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    year INT NOT NULL,
    current_sequence INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_category_year (category_id, year),
    FOREIGN KEY (category_id) REFERENCES project_categories(id)
);

-- Insert default category codes
INSERT INTO project_categories (name, code, description) VALUES
('Dự án đầu tư', 'INV', 'Dự án đầu tư mới'),
('Mua sắm tài sản', 'PUR', 'Mua sắm tài sản, thiết bị'),
('Thuê dịch vụ', 'SER', 'Thuê dịch vụ, tư vấn'),
('Bảo trì', 'MAI', 'Bảo trì, sửa chữa');
```

#### 5.2 Code Generation Logic
```typescript
interface ProjectCodeGenerator {
    generateCode(categoryId: number, year: number): Promise<string>;
    getNextSequence(categoryId: number, year: number): Promise<number>;
    validateCode(code: string): boolean;
}

class ProjectCodeGeneratorImpl implements ProjectCodeGenerator {
    async generateCode(categoryId: number, year: number): Promise<string> {
        const category = await this.getCategory(categoryId);
        const sequence = await this.getNextSequence(categoryId, year);
        
        return `${category.code}-${year}-${sequence.toString().padStart(3, '0')}`;
    }

    async getNextSequence(categoryId: number, year: number): Promise<number> {
        // Use database transaction to ensure atomicity
        const sequence = await this.db.transaction(async (trx) => {
            let record = await trx('project_sequences')
                .where({ category_id: categoryId, year })
                .first();

            if (!record) {
                record = await trx('project_sequences').insert({
                    category_id: categoryId,
                    year,
                    current_sequence: 1
                }).returning('*');
            } else {
                record = await trx('project_sequences')
                    .where({ category_id: categoryId, year })
                    .increment('current_sequence', 1)
                    .returning('*');
            }

            return record.current_sequence;
        });

        return sequence;
    }

    validateCode(code: string): boolean {
        const pattern = /^[A-Z]{3}-\d{4}-\d{3}$/;
        return pattern.test(code);
    }
}
```

#### 5.3 API Endpoints
```
POST /api/projects
- Request: Project data without project_code
- Response: Project with auto-generated project_code

GET /api/projects/{code}
- Response: Project details by code

GET /api/project-categories
- Response: List of categories with codes

POST /api/projects/validate-code
- Request: { code: string }
- Response: { isValid: boolean, isUnique: boolean }
```

#### 5.4 Sequence Diagram
![DMDA-1.3 Sequence Diagram](diagrams/DMDA-1.3%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các component trong hệ thống*

#### 5.5 Data Models
```typescript
interface Project {
    id: number;
    project_code: string; // Auto-generated
    name: string;
    category_id: number;
    year: number;
    start_date: string;
    end_date?: string;
    status: 'active' | 'completed' | 'cancelled';
    budget?: number;
    created_at: string;
    updated_at: string;
}

interface ProjectCategory {
    id: number;
    name: string;
    code: string; // 3-letter code
    description?: string;
    is_active: boolean;
}

interface ProjectSequence {
    id: number;
    category_id: number;
    year: number;
    current_sequence: number;
    created_at: string;
    updated_at: string;
}
```

---

### 6. Integration Requirements

#### 6.1 Bitrix24 Integration
- Đồng bộ project_code với Bitrix24
- Mapping: project_code → custom field trong Bitrix24
- Sync khi tạo dự án mới

#### 6.2 Data Flow
1. User tạo dự án mới
2. System lấy category_id và year
3. Generate project_code theo logic
4. Lưu vào database với project_code
5. Sync với Bitrix24
6. Hiển thị project_code trong UI

---

### 7. User Interface Requirements

#### 7.1 Display Format
- **Project Code**: Hiển thị rõ ràng trong danh sách
- **Format**: `INV-2024-001`, `PUR-2024-001`, v.v.
- **Color coding**: Màu khác nhau cho từng loại dự án
- **Tooltip**: Hiển thị ý nghĩa của mã

#### 7.2 Input/Output
- **Input**: Không cho phép nhập project_code
- **Output**: Hiển thị project_code sau khi tạo
- **Search**: Có thể tìm kiếm theo project_code
- **Filter**: Có thể lọc theo project_code pattern

#### 7.3 Validation
- Real-time validation khi nhập
- Error message rõ ràng
- Success confirmation khi tạo thành công

---

### 8. Testing Requirements

#### 8.1 Unit Tests
```typescript
describe('Project Code Generation', () => {
    test('should generate correct format for investment project', async () => {
        const code = await generator.generateCode(1, 2024); // INV category
        expect(code).toMatch(/^INV-2024-\d{3}$/);
    });

    test('should generate unique codes for same category and year', async () => {
        const code1 = await generator.generateCode(1, 2024);
        const code2 = await generator.generateCode(1, 2024);
        expect(code1).not.toBe(code2);
    });

    test('should reset sequence for new year', async () => {
        const code2023 = await generator.generateCode(1, 2023);
        const code2024 = await generator.generateCode(1, 2024);
        expect(code2023).toMatch(/^INV-2023-\d{3}$/);
        expect(code2024).toMatch(/^INV-2024-001$/);
    });

    test('should validate correct code format', () => {
        expect(generator.validateCode('INV-2024-001')).toBe(true);
        expect(generator.validateCode('INV-2024-1')).toBe(false);
        expect(generator.validateCode('INV-2024-001-EXTRA')).toBe(false);
    });
});
```

#### 8.2 Integration Tests
- Test database transactions
- Test concurrent code generation
- Test Bitrix24 sync
- Test API endpoints

#### 8.3 User Acceptance Tests
- Test automatic code generation
- Test code uniqueness
- Test UI display
- Test search and filter functionality

---

### 9. Deployment Requirements

#### 9.1 Database Migration
```sql
-- Migration script
BEGIN;
-- Add project_code column
ALTER TABLE projects ADD COLUMN project_code VARCHAR(20) NOT NULL UNIQUE;

-- Add category_code column
ALTER TABLE project_categories ADD COLUMN code VARCHAR(3) NOT NULL UNIQUE;

-- Create sequences table
CREATE TABLE project_sequences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    year INT NOT NULL,
    current_sequence INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_category_year (category_id, year),
    FOREIGN KEY (category_id) REFERENCES project_categories(id)
);

-- Insert default category codes
INSERT INTO project_categories (name, code, description) VALUES
('Dự án đầu tư', 'INV', 'Dự án đầu tư mới'),
('Mua sắm tài sản', 'PUR', 'Mua sắm tài sản, thiết bị'),
('Thuê dịch vụ', 'SER', 'Thuê dịch vụ, tư vấn'),
('Bảo trì', 'MAI', 'Bảo trì, sửa chữa');

-- Generate codes for existing projects
UPDATE projects p 
JOIN project_categories pc ON p.category_id = pc.id
SET p.project_code = CONCAT(pc.code, '-', p.year, '-', LPAD(p.id, 3, '0'))
WHERE p.project_code IS NULL;

COMMIT;
```

#### 9.2 Environment Configuration
- Category code mappings
- Sequence number settings
- Code format configuration

---

### 10. Success Criteria
- [ ] Mã dự án được sinh tự động khi tạo dự án mới
- [ ] Mã dự án duy nhất 100%
- [ ] Format mã nhất quán và dễ đọc
- [ ] Performance không bị ảnh hưởng
- [ ] Tích hợp thành công với Bitrix24
- [ ] Tất cả test cases pass

---

### 11. Risks and Mitigation

#### 11.1 Technical Risks
- **Risk:** Concurrent code generation conflicts
- **Mitigation:** Use database transactions và locks

- **Risk:** Performance issues với large datasets
- **Mitigation:** Optimize indexes và batch processing

- **Risk:** Code format inconsistencies
- **Mitigation:** Strict validation và unit tests

#### 11.2 Business Risks
- **Risk:** User confusion about code format
- **Mitigation:** Clear documentation và tooltips

- **Risk:** Code collision during migration
- **Mitigation:** Thorough testing và rollback plan

---

### 12. Future Enhancements
- Custom code format configuration
- Code prefix/suffix options
- Bulk code generation
- Code history tracking
- Advanced code validation rules

---

### 13. Dependencies
- **DMDA-1.1**: Cần có danh sách dự án và loại dự án
- **Database schema**: Cần thêm trường project_code và sequences table
- **Bitrix24 API**: Cần custom field mapping
- **UI Components**: Cần hiển thị project_code

---

### 14. Code Examples

#### 14.1 Generated Codes Examples
```
INV-2024-001  // Dự án đầu tư đầu tiên năm 2024
PUR-2024-001  // Dự án mua sắm đầu tiên năm 2024
SER-2024-001  // Dự án thuê dịch vụ đầu tiên năm 2024
MAI-2024-001  // Dự án bảo trì đầu tiên năm 2024
INV-2024-002  // Dự án đầu tư thứ 2 năm 2024
INV-2025-001  // Dự án đầu tư đầu tiên năm 2025 (reset sequence)
```

#### 14.2 Category Code Mapping
```
Dự án đầu tư → INV
Mua sắm tài sản → PUR
Thuê dịch vụ → SER
Bảo trì → MAI
```

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Next Review:** Sprint 2 