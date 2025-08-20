# Danh sách API Endpoints - Tổng hợp từ SRS

## Tổng quan
- **Tổng số API endpoints**: ~200+ endpoints
- **Phân loại theo module**: DMDA (Dự án), GT (Gói thầu), HD (Hợp đồng), CP (Chi phí), TSDV (Tài sản & Dịch vụ), BC (Báo cáo)
- **Phương thức chính**: GET, POST, PUT, DELETE
- **Định dạng**: RESTful API với JSON response

---

## 1. DMDA - Dự án (Projects)

### 1.1 Quản lý Dự án Cơ bản
```
GET    /api/projects                    # Lấy danh sách dự án
POST   /api/projects                    # Tạo dự án mới
GET    /api/projects/{id}               # Lấy chi tiết dự án
PUT    /api/projects/{id}               # Cập nhật dự án
DELETE /api/projects/{id}               # Xóa dự án
POST   /api/projects/{id}/restore       # Khôi phục dự án đã xóa
GET    /api/projects/{id}/can-delete    # Kiểm tra có thể xóa không
```

### 1.2 Danh mục Dự án theo Năm
```
GET    /api/project-categories          # Lấy danh mục dự án
POST   /api/project-categories          # Tạo danh mục mới
PUT    /api/project-categories/{id}     # Cập nhật danh mục
DELETE /api/project-categories/{id}     # Xóa danh mục
GET    /api/project-categories/{year}   # Lấy danh mục theo năm
```

### 1.3 Phân tích & Báo cáo Dự án
```
GET    /api/projects/analytics          # Phân tích xu hướng dự án
GET    /api/projects/efficiency         # Phân tích hiệu quả dự án
GET    /api/projects/risk-analysis      # Phân tích rủi ro dự án
GET    /api/projects/comparison         # So sánh dự án
GET    /api/projects/statistics         # Thống kê dự án
```

### 1.4 Dashboard & Kanban
```
GET    /api/projects/dashboard          # Dashboard tổng quan
GET    /api/projects/kanban             # Kanban board
POST   /api/projects/{id}/move-status   # Di chuyển trạng thái
GET    /api/kanban/columns              # Cấu hình cột Kanban
PUT    /api/user/preferences/view       # Cập nhật view preference
```

### 1.5 Thông báo & Cảnh báo
```
GET    /api/projects/notifications      # Thông báo dự án
POST   /api/projects/{id}/notify        # Gửi thông báo
GET    /api/projects/alerts             # Cảnh báo dự án
POST   /api/projects/alerts/config      # Cấu hình cảnh báo
```

### 1.6 Báo cáo & Xuất dữ liệu
```
GET    /api/reports/dashboard           # Báo cáo dashboard
GET    /api/reports/chart/{chart_type}  # Biểu đồ báo cáo
GET    /api/reports/export              # Xuất báo cáo
POST   /api/reports/schedule            # Lập lịch báo cáo
GET    /api/reports/email               # Gửi báo cáo qua email
POST   /api/reports/push-notification   # Push notification
```

---

## 2. GT - Gói thầu (Tender Packages)

### 2.1 Quản lý Gói thầu Cơ bản
```
GET    /api/tender-packages             # Lấy danh sách gói thầu
POST   /api/tender-packages             # Tạo gói thầu mới
GET    /api/tender-packages/{id}        # Lấy chi tiết gói thầu
PUT    /api/tender-packages/{id}        # Cập nhật gói thầu
DELETE /api/tender-packages/{id}        # Xóa gói thầu
POST   /api/tender-packages/create      # Tạo gói thầu (workflow)
POST   /api/tender-packages/draft       # Lưu nháp
GET    /api/tender-packages/preview     # Xem trước
PUT    /api/tender-packages/{id}/confirm # Xác nhận tạo
```

### 2.2 Tích hợp Bitrix
```
POST   /api/tender-packages/{id}/deploy-to-bitrix    # Triển khai lên Bitrix
GET    /api/tender-packages/{id}/bitrix-status       # Trạng thái Bitrix
POST   /api/tender-packages/{id}/sync-from-bitrix    # Đồng bộ từ Bitrix
GET    /api/tender-packages/{id}/workflow-config     # Cấu hình workflow
```

### 2.3 Lịch sử & Audit
```
GET    /api/tender-packages/{id}/history             # Lịch sử gói thầu
POST   /api/tender-packages/{id}/history             # Ghi log
GET    /api/tender-packages/activity-logs            # Log hoạt động
```

### 2.4 Tìm kiếm & Lọc
```
GET    /api/tender-packages/search                   # Tìm kiếm cơ bản
POST   /api/tender-packages/advanced-search          # Tìm kiếm nâng cao
GET    /api/tender-packages/search-suggestions       # Gợi ý tìm kiếm
GET    /api/user/searches                            # Tìm kiếm đã lưu
POST   /api/user/searches                            # Lưu tìm kiếm
PUT    /api/user/searches/{id}                       # Cập nhật tìm kiếm
DELETE /api/user/searches/{id}                       # Xóa tìm kiếm
GET    /api/search/analytics                         # Thống kê tìm kiếm
```

### 2.5 Xuất báo cáo
```
POST   /api/tender-packages/export                   # Xuất báo cáo
POST   /api/tender-packages/export-search-results    # Xuất kết quả tìm kiếm
GET    /api/export/templates                         # Mẫu xuất
POST   /api/export/templates                         # Tạo mẫu xuất
PUT    /api/export/templates/{id}                    # Cập nhật mẫu
DELETE /api/export/templates/{id}                    # Xóa mẫu
GET    /api/export/jobs                              # Danh sách job xuất
GET    /api/export/jobs/{id}                         # Chi tiết job
DELETE /api/export/jobs/{id}                         # Hủy job
GET    /api/export/jobs/{id}/download                # Tải file xuất
GET    /api/export/jobs/{id}/status                  # Trạng thái job
GET    /api/export/scheduled                         # Lịch xuất
POST   /api/export/scheduled                         # Tạo lịch xuất
PUT    /api/export/scheduled/{id}                    # Cập nhật lịch
DELETE /api/export/scheduled/{id}                    # Xóa lịch
GET    /api/export/columns                           # Cột xuất
PUT    /api/export/columns/{id}                      # Cập nhật cột
```

### 2.6 Tài liệu Gói thầu
```
GET    /api/tender-packages/{id}/documents           # Danh sách tài liệu
POST   /api/tender-packages/{id}/documents/upload    # Upload tài liệu
GET    /api/tender-packages/{id}/documents/{doc_id}  # Chi tiết tài liệu
PUT    /api/tender-packages/{id}/documents/{doc_id}  # Cập nhật tài liệu
DELETE /api/tender-packages/{id}/documents/{doc_id}  # Xóa tài liệu
GET    /api/documents/{doc_id}/download              # Tải tài liệu
GET    /api/documents/{doc_id}/preview               # Xem trước tài liệu
```

---

## 3. HD - Hợp đồng (Contracts)

### 3.1 Quản lý Hợp đồng Cơ bản
```
GET    /api/contracts                 # Lấy danh sách hợp đồng
POST   /api/contracts                 # Tạo hợp đồng mới
GET    /api/contracts/{id}            # Lấy chi tiết hợp đồng
PUT    /api/contracts/{id}            # Cập nhật hợp đồng
DELETE /api/contracts/{id}            # Xóa hợp đồng
POST   /api/contracts/create          # Tạo hợp đồng (workflow)
POST   /api/contracts/validate        # Validate hợp đồng
```

### 3.2 Phụ lục Hợp đồng
```
GET    /api/contracts/{id}/amendments           # Danh sách phụ lục
POST   /api/contracts/{id}/amendments           # Tạo phụ lục
PUT    /api/contracts/{id}/amendments/{amend_id} # Cập nhật phụ lục
DELETE /api/contracts/{id}/amendments/{amend_id} # Xóa phụ lục
```

### 3.3 Tài liệu Hợp đồng
```
GET    /api/contracts/{id}/documents            # Danh sách tài liệu
POST   /api/contracts/{id}/documents/upload     # Upload tài liệu
DELETE /api/contracts/{id}/documents/{doc_id}   # Xóa tài liệu
```

### 3.4 Lịch thanh toán
```
GET    /api/contracts/{id}/payment-schedules    # Lịch thanh toán
POST   /api/contracts/{id}/payment-schedules    # Tạo lịch thanh toán
PUT    /api/contracts/{id}/payment-schedules/{schedule_id} # Cập nhật
DELETE /api/contracts/{id}/payment-schedules/{schedule_id} # Xóa
```

### 3.5 Theo dõi Tiến độ
```
GET    /api/contracts/{id}/progress             # Tiến độ hợp đồng
POST   /api/contracts/{id}/progress             # Cập nhật tiến độ
GET    /api/contracts/{id}/milestones           # Mốc quan trọng
POST   /api/contracts/{id}/milestones           # Tạo mốc
PUT    /api/contracts/{id}/milestones/{milestone_id} # Cập nhật mốc
```

### 3.6 Thanh toán & Nghiệm thu
```
GET    /api/contracts/{id}/payments             # Danh sách thanh toán
POST   /api/contracts/{id}/payments             # Tạo thanh toán
PUT    /api/contracts/{id}/payments/{payment_id} # Cập nhật thanh toán
GET    /api/contracts/{id}/acceptance           # Nghiệm thu
POST   /api/contracts/{id}/acceptance           # Tạo nghiệm thu
```

### 3.7 Báo cáo & Phân tích
```
GET    /api/contracts/reports                   # Báo cáo hợp đồng
GET    /api/contracts/analytics                 # Phân tích hiệu quả
GET    /api/contracts/expiring                  # Hợp đồng sắp hết hạn
GET    /api/contracts/overdue                   # Hợp đồng quá hạn
```

### 3.8 Activity Logs
```
GET    /api/contracts/{id}/activity-logs        # Log hoạt động
GET    /api/contracts/{id}/activity-logs/{log_id} # Chi tiết log
GET    /api/contracts/{id}/activity-logs/summary # Tóm tắt log
GET    /api/contracts/{id}/activity-logs/search # Tìm kiếm log
GET    /api/contracts/{id}/activity-logs/export # Xuất log
GET    /api/contracts/activity-logs/config      # Cấu hình log
PUT    /api/contracts/activity-logs/config      # Cập nhật cấu hình
GET    /api/contracts/{id}/activity-logs/stats  # Thống kê log
GET    /api/contracts/activity-logs/bulk        # Log hàng loạt
POST   /api/contracts/activity-logs/cleanup     # Dọn dẹp log
```

---

## 4. CP - Chi phí (Cost Items)

### 4.1 Quản lý Chi phí Cơ bản
```
GET    /api/cost-items                 # Lấy danh sách chi phí
POST   /api/cost-items                 # Tạo chi phí mới
GET    /api/cost-items/{id}            # Lấy chi tiết chi phí
PUT    /api/cost-items/{id}            # Cập nhật chi phí
DELETE /api/cost-items/{id}            # Xóa chi phí
POST   /api/cost-items/bulk-delete     # Xóa hàng loạt
DELETE /api/cost-items/{id}/permanent  # Xóa vĩnh viễn
POST   /api/cost-items/{id}/restore    # Khôi phục chi phí
GET    /api/cost-items/deleted         # Chi phí đã xóa
```

### 4.2 Liên kết & Validation
```
POST   /api/cost-items/{id}/link-project      # Liên kết dự án
POST   /api/cost-items/{id}/link-tender       # Liên kết gói thầu
POST   /api/cost-items/{id}/link-contract     # Liên kết hợp đồng
GET    /api/cost-items/{id}/delete-constraints # Ràng buộc xóa
GET    /api/cost-items/{id}/delete-history    # Lịch sử xóa
GET    /api/cost-items/delete-statistics      # Thống kê xóa
```

### 4.3 Chi phí Định kỳ
```
GET    /api/cost-items/{id}/periods           # Kỳ thanh toán
POST   /api/cost-items/{id}/periods           # Tạo kỳ
PUT    /api/cost-items/{id}/periods/{period_id} # Cập nhật kỳ
DELETE /api/cost-items/{id}/periods/{period_id} # Xóa kỳ
POST   /api/cost-items/{id}/periods/bulk-update # Cập nhật hàng loạt
```

### 4.4 Tài liệu Đính kèm
```
GET    /api/cost-items/{id}/attachments       # Tài liệu đính kèm
POST   /api/cost-items/{id}/attachments       # Upload tài liệu
DELETE /api/cost-items/{id}/attachments/{att_id} # Xóa tài liệu
```

### 4.5 Lịch sử & Audit
```
GET    /api/cost-items/{id}/history           # Lịch sử chi phí
POST   /api/cost-items/history                # Ghi log
```

### 4.6 Tìm kiếm & Lọc
```
POST   /api/cost-items/search                 # Tìm kiếm chi phí
GET    /api/cost-items/search-suggestions     # Gợi ý tìm kiếm
POST   /api/cost-items/save-search-filter     # Lưu bộ lọc
GET    /api/cost-items/saved-filters          # Bộ lọc đã lưu
```

### 4.7 Danh mục Chi phí
```
GET    /api/cost-categories                   # Danh mục chi phí
POST   /api/cost-categories                   # Tạo danh mục
PUT    /api/cost-categories/{id}              # Cập nhật danh mục
DELETE /api/cost-categories/{id}              # Xóa danh mục
```

### 4.8 Phê duyệt
```
POST   /api/cost-items/{id}/approve           # Phê duyệt chi phí
POST   /api/cost-items/{id}/reject            # Từ chối chi phí
GET    /api/cost-items/approval-config        # Cấu hình phê duyệt
PUT    /api/cost-items/approval-config        # Cập nhật cấu hình
```

### 4.9 Báo cáo & Thống kê
```
GET    /api/cost-items/statistics             # Thống kê chi phí
GET    /api/cost-items/reports                # Báo cáo chi phí
POST   /api/cost-items/export                 # Xuất chi phí
```

### 4.10 Chỉ số Tài chính
```
GET    /api/project-indicators/{project_id}   # Chỉ số dự án
POST   /api/project-indicators/multi          # Nhiều chỉ số
POST   /api/project-indicators/calculate      # Tính toán chỉ số
GET    /api/project-indicators/{project_id}/trends # Xu hướng
GET    /api/project-indicators/alerts         # Cảnh báo chỉ số
POST   /api/project-indicators/report         # Báo cáo chỉ số
```

### 4.11 Cảnh báo Ngân sách
```
GET    /api/budget-alerts                     # Cảnh báo ngân sách
POST   /api/budget-alerts/{alert_id}/acknowledge # Xác nhận cảnh báo
POST   /api/budget-alerts/{alert_id}/resolve  # Giải quyết cảnh báo
POST   /api/budget-alerts/config              # Cấu hình cảnh báo
GET    /api/budget-alerts/config              # Lấy cấu hình
GET    /api/budget-alerts/check-status        # Kiểm tra trạng thái
POST   /api/budget-alerts/report              # Báo cáo cảnh báo
POST   /api/budget-alerts/test                # Test cảnh báo
```

---

## 5. TSDV - Tài sản & Dịch vụ (Assets & Services)

### 5.1 Quản lý Tài sản/Dịch vụ Cơ bản
```
GET    /api/assets-services              # Danh sách tài sản/dịch vụ
POST   /api/assets-services              # Tạo mới
GET    /api/assets-services/{id}         # Chi tiết
PUT    /api/assets-services/{id}         # Cập nhật
DELETE /api/assets-services/{id}         # Xóa
POST   /api/assets-services/create       # Tạo (workflow)
POST   /api/assets-services/save-draft   # Lưu nháp
```

### 5.2 Tạo & Cấu hình
```
GET    /api/assets-services/form-config  # Cấu hình form
POST   /api/assets-services/validate     # Validate dữ liệu
GET    /api/assets-services/generate-code # Sinh mã tự động
GET    /api/assets-services/available-projects # Dự án có sẵn
```

### 5.3 Tài liệu Đính kèm
```
GET    /api/assets-services/{id}/attachments     # Tài liệu
POST   /api/assets-services/{id}/attachments     # Upload
DELETE /api/assets-services/{id}/attachments/{att_id} # Xóa
```

### 5.4 Import/Export
```
POST   /api/assets-services/import       # Import từ Excel
GET    /api/assets-services/export       # Xuất dữ liệu
POST   /api/assets-services/import       # Import (với config)
```

### 5.5 Tìm kiếm & Lọc
```
GET    /api/assets-services/search       # Tìm kiếm
POST   /api/assets-services/filter       # Lọc nâng cao
GET    /api/assets-services/categories   # Danh mục
```

### 5.6 Theo dõi & Bảo trì
```
GET    /api/assets-services/{id}/maintenance # Bảo trì
POST   /api/assets-services/{id}/maintenance # Tạo bảo trì
GET    /api/assets-services/warranty-alerts # Cảnh báo bảo hành
POST   /api/assets-services/warranty-alerts # Xử lý cảnh báo
```

---

## 6. BC - Báo cáo (Reports)

### 6.1 Báo cáo Dự án
```
GET    /api/reports/project-progress     # Báo cáo tiến độ
GET    /api/reports/project-financial    # Báo cáo tài chính
GET    /api/reports/project-summary      # Báo cáo tổng hợp
```

### 6.2 Templates & Schedules
```
GET    /api/reports/templates            # Mẫu báo cáo
POST   /api/reports/templates            # Tạo mẫu
PUT    /api/reports/templates/{id}       # Cập nhật mẫu
DELETE /api/reports/templates/{id}       # Xóa mẫu
POST   /api/reports/generate             # Tạo báo cáo
GET    /api/reports/generate/{id}/status # Trạng thái tạo
GET    /api/reports/generate/{id}/download # Tải báo cáo
GET    /api/reports/schedules            # Lịch báo cáo
POST   /api/reports/schedules            # Tạo lịch
PUT    /api/reports/schedules/{id}       # Cập nhật lịch
DELETE /api/reports/schedules/{id}       # Xóa lịch
GET    /api/reports/history              # Lịch sử báo cáo
GET    /api/reports/history/{id}         # Chi tiết lịch sử
GET    /api/reports/permissions          # Quyền báo cáo
POST   /api/reports/permissions          # Cấp quyền
DELETE /api/reports/permissions/{id}     # Thu hồi quyền
```

---

## 7. Hệ thống & Quản trị

### 7.1 Quản lý Người dùng
```
GET    /api/users                        # Danh sách người dùng
POST   /api/users                        # Tạo người dùng
GET    /api/users/{id}                   # Chi tiết người dùng
PUT    /api/users/{id}                   # Cập nhật người dùng
DELETE /api/users/{id}                   # Xóa người dùng
POST   /api/users/{id}/change-password   # Đổi mật khẩu
```

### 7.2 Quản lý Vai trò & Quyền
```
GET    /api/roles                        # Danh sách vai trò
POST   /api/roles                        # Tạo vai trò
PUT    /api/roles/{id}                   # Cập nhật vai trò
DELETE /api/roles/{id}                   # Xóa vai trò
GET    /api/permissions                  # Danh sách quyền
POST   /api/permissions                  # Cấp quyền
DELETE /api/permissions/{id}             # Thu hồi quyền
```

### 7.3 Cấu hình Hệ thống
```
GET    /api/system/config                # Cấu hình hệ thống
PUT    /api/system/config                # Cập nhật cấu hình
GET    /api/system/health                # Trạng thái hệ thống
GET    /api/system/logs                  # Log hệ thống
```

### 7.4 Backup & Restore
```
GET    /api/system/backup                # Tạo backup
POST   /api/system/backup                # Backup thủ công
GET    /api/system/backup/{id}/download  # Tải backup
POST   /api/system/restore               # Khôi phục
```

---

## 8. Tích hợp & Webhook

### 8.1 Tích hợp Bitrix
```
POST   /api/integrations/bitrix/sync     # Đồng bộ Bitrix
GET    /api/integrations/bitrix/status   # Trạng thái tích hợp
POST   /api/integrations/bitrix/webhook  # Webhook từ Bitrix
```

### 8.2 Email & Notification
```
POST   /api/notifications/email          # Gửi email
POST   /api/notifications/push           # Push notification
GET    /api/notifications/templates      # Mẫu thông báo
POST   /api/notifications/templates      # Tạo mẫu
```

### 8.3 File Storage
```
POST   /api/files/upload                 # Upload file
GET    /api/files/{id}/download          # Tải file
DELETE /api/files/{id}                   # Xóa file
GET    /api/files/{id}/metadata          # Metadata file
```

---

## Ghi chú Triển khai

### Authentication & Authorization
- Sử dụng JWT token cho authentication
- Role-based access control (RBAC) cho authorization
- API key cho tích hợp bên thứ 3

### Rate Limiting
- 100 requests/minute cho user thường
- 1000 requests/minute cho admin
- 5000 requests/minute cho API key

### Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Thành công",
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

### Error Handling
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dữ liệu không hợp lệ",
    "details": {}
  }
}
```

### Versioning
- API versioning: `/api/v1/`
- Backward compatibility trong 12 tháng
- Deprecation notice trước 6 tháng

### Documentation
- Swagger/OpenAPI 3.0 cho tất cả endpoints
- Postman collection cho testing
- SDK cho các ngôn ngữ phổ biến
