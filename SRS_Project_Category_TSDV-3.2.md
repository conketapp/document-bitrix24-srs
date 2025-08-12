# Software Requirements Specification (SRS)
## Epic: Tài sản & Dịch vụ - Tạo & Quản lý Danh mục Tài sản và Dịch vụ

### User Story: TSDV-3.2
### Nhắc nhở khi Tài sản/Dịch vụ sắp hết hạn bảo hành/bảo trì/sử dụng

#### Thông tin User Story
- **Story ID:** TSDV-3.2
- **Priority:** High
- **Story Points:** 13
- **Sprint:** Sprint 3
- **Status:** To Do
- **Dependencies:** TSDV-1.1, TSDV-1.2, TSDV-3.1

#### Mô tả User Story
**Với vai trò là** Người quản lý tài sản/dịch vụ,  
**Tôi muốn** hệ thống có khả năng nhắc nhở tự động (qua giao diện, email) khi:
- Các tài sản sắp hết hạn bảo hành
- Các tài sản sắp đến kỳ bảo trì
- Các dịch vụ sắp hết thời gian sử dụng  
**Để** tôi có thể chủ động lên kế hoạch tiếp theo (gia hạn, sửa chữa, thay thế, chấm dứt) đối với các tài sản, dịch vụ đó, tránh gián đoạn hoạt động hoặc phát sinh chi phí không mong muốn.

#### Điều kiện chấp nhận (Acceptance Criteria)
- [ ] Có thể cấu hình ngưỡng nhắc nhở (ví dụ: cảnh báo 30 ngày trước khi hết hạn)
- [ ] Thông báo hiển thị rõ ràng và có thể liên kết trực tiếp đến tài sản/dịch vụ liên quan
- [ ] Cho phép người dùng thiết lập nhận thông báo qua email hoặc trên giao diện hệ thống (notifications)
- [ ] Hệ thống tự động kiểm tra và gửi nhắc nhở hàng ngày
- [ ] Có thể thiết lập nhiều mức cảnh báo (ví dụ: 7 ngày, 30 ngày, 60 ngày trước hết hạn)
- [ ] Thông báo bao gồm thông tin chi tiết về tài sản/dịch vụ và thời gian còn lại
- [ ] Có thể tắt/bật thông báo cho từng loại sự kiện
- [ ] Có thể xem lịch sử các thông báo đã gửi
- [ ] Có thể thiết lập người nhận thông báo khác nhau cho từng loại tài sản/dịch vụ
- [ ] Có thể xuất báo cáo về các tài sản/dịch vụ sắp hết hạn
- [ ] Có thể thiết lập template thông báo tùy chỉnh
- [ ] Hệ thống ghi log đầy đủ các hoạt động gửi thông báo

#### 2.4 Activity Diagram
![TSDV-3.2 Activity Diagram](diagrams/TSDV-3.2%20Activity%20Diagram.png)

*Activity Diagram mô tả luồng xử lý nhắc nhở Tài sản/Dịch vụ*

#### 2.5 Sequence Diagram
![TSDV-3.2 Sequence Diagram](diagrams/TSDV-3.2%20Sequence%20Diagram.png)

*Sequence Diagram mô tả tương tác giữa các thành phần khi nhắc nhở Tài sản/Dịch vụ*

---

### Functional Requirements

#### Core Features
1. **Reminder Configuration**
   - Threshold settings
   - Notification types
   - Recipient management
   - Template customization

2. **Notification Types**
   - Warranty expiration
   - Maintenance due
   - Service expiration
   - Custom reminders
   - Escalation notifications

3. **Notification Channels**
   - In-app notifications
   - Email notifications
   - SMS notifications (optional)
   - Dashboard alerts
   - Calendar integration

4. **Reminder Management**
   - Automatic checking
   - Manual triggering
   - Notification history
   - Status tracking
   - Acknowledgment handling

#### Business Rules
- Hệ thống phải kiểm tra hàng ngày để tìm các sự kiện sắp đến
- Thông báo phải được gửi đúng thời gian đã cấu hình
- Người dùng phải có thể tùy chỉnh thời gian nhắc nhở
- Thông báo phải bao gồm link trực tiếp đến tài sản/dịch vụ
- Hệ thống phải ghi log đầy đủ các hoạt động gửi thông báo
- Không gửi thông báo trùng lặp trong cùng một ngày

#### Notification Categories
1. **Warranty Expiration**
   - Hardware warranty
   - Software warranty
   - Extended warranty
   - Service warranty
   - Parts warranty

2. **Maintenance Due**
   - Preventive maintenance
   - Scheduled maintenance
   - Equipment inspection
   - Calibration due
   - Safety check

3. **Service Expiration**
   - Software license
   - Cloud service
   - Support contract
   - Insurance policy
   - Lease agreement

4. **Custom Reminders**
   - Renewal dates
   - Review periods
   - Audit dates
   - Compliance checks
   - Performance reviews

---

### Non-Functional Requirements

#### Performance Requirements
- Hệ thống phải xử lý kiểm tra thông báo trong vòng 5 phút
- Email thông báo phải được gửi trong vòng 10 phút sau khi phát hiện
- Giao diện thông báo phải load trong vòng 2 giây
- Hệ thống phải hỗ trợ tối đa 1000 thông báo đồng thời

#### Security Requirements
- Chỉ người dùng có quyền mới có thể cấu hình thông báo
- Thông tin nhạy cảm không được gửi qua email
- Log đầy đủ các hoạt động gửi thông báo
- Mã hóa thông tin người nhận thông báo

#### Usability Requirements
- Giao diện cấu hình thông báo dễ sử dụng
- Thông báo hiển thị rõ ràng, dễ đọc
- Có thể tắt/bật thông báo dễ dàng
- Hỗ trợ đa ngôn ngữ cho thông báo

#### Reliability Requirements
- Hệ thống phải hoạt động 24/7
- Có cơ chế backup cho cấu hình thông báo
- Tự động khôi phục khi có lỗi
- Monitoring và alerting cho hệ thống thông báo

---

### Technical Requirements

#### System Architecture
1. **Notification Engine**
   - Background job processing
   - Queue management
   - Retry mechanism
   - Error handling

2. **Email Service**
   - SMTP integration
   - Template engine
   - Attachment support
   - Delivery tracking

3. **In-App Notifications**
   - Real-time updates
   - Push notifications
   - Notification center
   - Read/unread status

4. **Configuration Management**
   - User preferences
   - System settings
   - Template management
   - Recipient lists

#### Database Schema
```sql
-- Notification Settings
CREATE TABLE notification_settings (
    id INT PRIMARY KEY,
    user_id INT,
    asset_id INT,
    notification_type VARCHAR(50),
    threshold_days INT,
    email_enabled BOOLEAN,
    in_app_enabled BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Notification History
CREATE TABLE notification_history (
    id INT PRIMARY KEY,
    asset_id INT,
    notification_type VARCHAR(50),
    recipient_email VARCHAR(255),
    sent_at TIMESTAMP,
    status VARCHAR(20),
    message TEXT
);

-- Notification Templates
CREATE TABLE notification_templates (
    id INT PRIMARY KEY,
    template_name VARCHAR(100),
    template_type VARCHAR(50),
    subject VARCHAR(255),
    body TEXT,
    is_active BOOLEAN
);
```

#### API Endpoints
```typescript
// Notification Settings
GET /api/notifications/settings
POST /api/notifications/settings
PUT /api/notifications/settings/{id}
DELETE /api/notifications/settings/{id}

// Notification History
GET /api/notifications/history
GET /api/notifications/history/{id}

// Notification Templates
GET /api/notifications/templates
POST /api/notifications/templates
PUT /api/notifications/templates/{id}
DELETE /api/notifications/templates/{id}

// Manual Trigger
POST /api/notifications/trigger
POST /api/notifications/test
```

---

### User Interface Requirements

#### Notification Settings Page
1. **General Settings**
   - Enable/disable notifications
   - Default threshold days
   - Default notification channels
   - Time zone settings

2. **Asset-Specific Settings**
   - Individual asset notification settings
   - Bulk settings management
   - Category-based settings
   - Priority levels

3. **Template Management**
   - Email template editor
   - In-app notification templates
   - Variable placeholders
   - Preview functionality

4. **Recipient Management**
   - Add/remove recipients
   - Role-based recipients
   - Department-based recipients
   - Custom recipient lists

#### Notification Center
1. **Notification List**
   - All notifications view
   - Filter by type/status
   - Search functionality
   - Pagination

2. **Notification Details**
   - Full notification content
   - Related asset information
   - Action buttons
   - Mark as read/unread

3. **Quick Actions**
   - Acknowledge notification
   - Snooze notification
   - Dismiss notification
   - Take action

#### Dashboard Widgets
1. **Upcoming Expirations**
   - Count of items expiring soon
   - List of critical items
   - Quick access to details
   - Action buttons

2. **Notification Statistics**
   - Notifications sent today
   - Pending notifications
   - Acknowledged notifications
   - Failed notifications

---

### Integration Requirements

#### Email Service Integration
- SMTP server configuration
- Email template system
- Delivery tracking
- Bounce handling

#### Calendar Integration
- Google Calendar
- Outlook Calendar
- iCal format support
- Event creation

#### Reporting Integration
- Export to Excel/PDF
- Scheduled reports
- Custom report builder
- Data visualization

#### Third-party Services
- Slack notifications
- Microsoft Teams
- SMS gateway
- Push notification service

---

### Testing Requirements

#### Unit Testing
- Notification engine logic
- Email service functions
- Template rendering
- Configuration validation

#### Integration Testing
- Email delivery testing
- Database operations
- API endpoint testing
- Third-party service integration

#### User Acceptance Testing
- Notification configuration
- Email template testing
- User interface testing
- End-to-end workflow

#### Performance Testing
- Load testing for notification processing
- Email delivery performance
- Database query optimization
- System resource usage

---

### Deployment Requirements

#### Environment Setup
- Production notification server
- Staging environment
- Development environment
- Backup systems

#### Monitoring & Alerting
- System health monitoring
- Email delivery monitoring
- Error rate tracking
- Performance metrics

#### Security Considerations
- Email encryption
- Access control
- Data protection
- Audit logging

#### Backup & Recovery
- Configuration backup
- Database backup
- Template backup
- Disaster recovery plan

---

### Documentation Requirements

#### User Documentation
- Notification setup guide
- Email template guide
- Troubleshooting guide
- Best practices

#### Technical Documentation
- API documentation
- Database schema
- System architecture
- Deployment guide

#### Admin Documentation
- System configuration
- Monitoring setup
- Security guidelines
- Maintenance procedures 