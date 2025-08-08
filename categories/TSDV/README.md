# TSDV - Tài sản & Dịch vụ
## Quản lý Tài sản và Dịch vụ

### 📋 Tổng quan
Category TSDV tập trung vào việc quản lý tài sản, dịch vụ, theo dõi bảo hành/bảo trì và nhắc nhở tự động cho hệ thống của Agribank.

### 📊 Thống kê User Stories

| Story ID | Tên User Story | Priority | Story Points | Status |
|----------|----------------|----------|--------------|--------|
| TSDV-1.1 | Quản lý danh mục tài sản cơ bản | High | 8 | ✅ Done |
| TSDV-1.2 | Quản lý thông tin chi tiết tài sản | High | 13 | ✅ Done |
| TSDV-1.3 | Quản lý danh mục dịch vụ | High | 8 | ✅ Done |
| TSDV-2.1 | Quản lý bảo hành tài sản | Medium | 8 | ✅ Done |
| TSDV-2.2 | Quản lý bảo trì tài sản | Medium | 8 | ✅ Done |
| TSDV-2.3 | Quản lý sửa chữa tài sản | Medium | 8 | ✅ Done |
| TSDV-2.4 | Quản lý thanh lý tài sản | Medium | 5 | ✅ Done |
| TSDV-3.1 | Theo dõi lịch sử sử dụng, bảo hành, bảo dưỡng | High | 8 | ✅ Done |
| TSDV-3.2 | Nhắc nhở khi Tài sản/Dịch vụ sắp hết hạn | High | 13 | ✅ Done |

### 🎯 Mục tiêu chính

#### 1. Quản lý Tài sản
- Tạo và quản lý danh mục tài sản
- Theo dõi thông tin chi tiết tài sản
- Quản lý vòng đời tài sản
- Báo cáo tài sản

#### 2. Quản lý Dịch vụ
- Quản lý danh mục dịch vụ
- Theo dõi thời gian sử dụng
- Quản lý gia hạn dịch vụ
- Đánh giá chất lượng dịch vụ

#### 3. Bảo trì và Bảo hành
- Quản lý bảo hành tài sản
- Lập kế hoạch bảo trì
- Theo dõi sửa chữa
- Quản lý thanh lý

#### 4. Nhắc nhở và Cảnh báo
- Nhắc nhở hết hạn bảo hành
- Cảnh báo bảo trì định kỳ
- Thông báo hết hạn dịch vụ
- Email và notification

### 🔗 Liên kết User Stories

#### Epic 1: Quản lý Tài sản và Dịch vụ Cơ bản
- [TSDV-1.1: Quản lý danh mục tài sản cơ bản](TSDV-1.1.md)
- [TSDV-1.2: Quản lý thông tin chi tiết tài sản](TSDV-1.2.md)
- [TSDV-1.3: Quản lý danh mục dịch vụ](TSDV-1.3.md)

#### Epic 2: Bảo trì và Bảo hành
- [TSDV-2.1: Quản lý bảo hành tài sản](TSDV-2.1.md)
- [TSDV-2.2: Quản lý bảo trì tài sản](TSDV-2.2.md)
- [TSDV-2.3: Quản lý sửa chữa tài sản](TSDV-2.3.md)
- [TSDV-2.4: Quản lý thanh lý tài sản](TSDV-2.4.md)

#### Epic 3: Theo dõi và Nhắc nhở
- [TSDV-3.1: Theo dõi lịch sử sử dụng, bảo hành, bảo dưỡng](TSDV-3.1.md)
- [TSDV-3.2: Nhắc nhở khi Tài sản/Dịch vụ sắp hết hạn](TSDV-3.2.md)

### 🏗️ Kiến trúc Hệ thống

#### Core Modules
1. **Asset Management Module**
   - Asset registration and classification
   - Asset lifecycle management
   - Asset tracking and monitoring
   - Asset valuation and depreciation

2. **Service Management Module**
   - Service catalog management
   - Service lifecycle management
   - Service quality monitoring
   - Service renewal management

3. **Maintenance Module**
   - Preventive maintenance planning
   - Corrective maintenance tracking
   - Maintenance scheduling
   - Maintenance cost tracking

4. **Notification Module**
   - Alert configuration
   - Email notification system
   - In-app notification
   - Escalation management

#### Database Schema
```sql
-- Assets
CREATE TABLE assets (
    id INT PRIMARY KEY,
    asset_code VARCHAR(50),
    asset_name VARCHAR(100),
    asset_type VARCHAR(50),
    category VARCHAR(50),
    location VARCHAR(100),
    purchase_date DATE,
    warranty_expiry DATE,
    status VARCHAR(20),
    value DECIMAL(15,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Services
CREATE TABLE services (
    id INT PRIMARY KEY,
    service_code VARCHAR(50),
    service_name VARCHAR(100),
    service_type VARCHAR(50),
    provider VARCHAR(100),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    cost DECIMAL(15,2),
    created_at TIMESTAMP
);

-- Maintenance Records
CREATE TABLE maintenance_records (
    id INT PRIMARY KEY,
    asset_id INT,
    maintenance_type VARCHAR(50),
    maintenance_date DATE,
    description TEXT,
    cost DECIMAL(15,2),
    performed_by VARCHAR(100),
    next_maintenance_date DATE,
    created_at TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    id INT PRIMARY KEY,
    asset_id INT,
    notification_type VARCHAR(50),
    message TEXT,
    sent_date TIMESTAMP,
    recipient_email VARCHAR(255),
    status VARCHAR(20),
    created_at TIMESTAMP
);
```

### 📊 Metrics và KPI

#### Asset Metrics
- **Asset Utilization Rate**: Tỷ lệ sử dụng tài sản
- **Maintenance Cost per Asset**: Chi phí bảo trì/tài sản
- **Asset Lifecycle Duration**: Thời gian vòng đời tài sản
- **Asset Availability**: Tỷ lệ sẵn sàng tài sản

#### Service Metrics
- **Service Uptime**: Thời gian hoạt động dịch vụ
- **Service Response Time**: Thời gian phản hồi
- **Service Cost Efficiency**: Hiệu quả chi phí dịch vụ
- **Service Quality Score**: Điểm chất lượng dịch vụ

### 🔄 Quy trình Workflow

#### 1. Asset Lifecycle
1. Asset registration
2. Asset deployment
3. Asset monitoring
4. Asset maintenance
5. Asset disposal

#### 2. Service Lifecycle
1. Service registration
2. Service activation
3. Service monitoring
4. Service renewal
5. Service termination

#### 3. Maintenance Process
1. Maintenance planning
2. Maintenance scheduling
3. Maintenance execution
4. Maintenance reporting
5. Maintenance follow-up

### 📚 Tài liệu Tham khảo

#### Standards
- [ISO 55001 Asset Management](link)
- [ITIL Service Management](link)
- [Agribank Asset Standards](link)
- [Banking Security Guidelines](link)

#### Templates
- [Asset Registration Template](link)
- [Maintenance Schedule Template](link)
- [Service Level Agreement Template](link)
- [Notification Template](link)

---

**📌 Lưu ý**: Category TSDV cần tích hợp chặt chẽ với hệ thống CP để theo dõi chi phí tài sản và dịch vụ.

**🔄 Cập nhật cuối**: 2024-01-25
**👥 Maintained by**: Asset Management Team 