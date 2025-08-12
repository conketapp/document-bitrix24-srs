# Frontend Tasks - Epic DMDA: Danh mục dự án

## Tổng quan
**Epic ID:** DMDA  
**Epic Name:** Danh mục dự án - Quản lý Danh mục Dự án  
**Frontend Framework:** React/Next.js + TypeScript  
**UI Library:** Tailwind CSS + Shadcn/ui  
**Version:** 1.0  
**Last Updated:** 08-2024  

---

## 📋 Danh sách Task Frontend

### 🎯 **Task Group 1: Core Components & Layout**

#### **FE-DMDA-001: Tạo Layout chính cho trang Danh mục dự án**
**Priority:** Critical  
**Story Points:** 5  
**Description:**  
- Tạo layout responsive cho trang danh mục dự án
- Implement header với navigation và user menu
- Tạo sidebar cho filters và actions
- Implement main content area với grid layout
- Responsive design cho mobile/tablet/desktop

**Acceptance Criteria:**
- Layout hiển thị đúng trên tất cả thiết bị
- Header có logo, navigation, user profile
- Sidebar có thể collapse trên mobile
- Main area có grid layout linh hoạt
- Loading states và error handling

**Tech Stack:**
- Next.js App Router
- Tailwind CSS
- Shadcn/ui Layout components
- React Hook Form cho forms

---

#### **FE-DMDA-001.5: Tạo Component StatusBadge cho trạng thái dự án**
**Priority:** Critical  
**Story Points:** 3  
**Description:**  
- Tạo component StatusBadge với design modern
- Implement dot indicator + text layout
- Tạo color scheme cho 6 trạng thái dự án
- Responsive design và accessibility
- TypeScript interface cho props

**Acceptance Criteria:**
- Design modern với dot indicator + text
- Rounded-full style với subtle background
- Color scheme: Khởi tạo (blue), Chờ phê duyệt (amber), Đã phê duyệt (emerald), Từ chối (red), Dừng (orange), Yêu cầu chỉnh sửa (purple)
- Hover effects và transitions
- Accessibility: ARIA labels, keyboard navigation
- TypeScript interface với status enum

**Tech Stack:**
- React Component với TypeScript
- Shadcn/ui Badge component
- Tailwind CSS cho styling
- Framer Motion cho animations

**Code Example:**
```tsx
import { Badge } from "@/components/ui/badge";

interface StatusBadgeProps {
  status: 'initialized' | 'pending_approval' | 'approved' | 'rejected' | 'suspended' | 'edit_requested';
  className?: string;
}

const StatusBadge = ({ status, className }: StatusBadgeProps) => {
  const statusConfig = {
    initialized: {
      label: 'Khởi tạo',
      color: 'blue',
      bgColor: 'bg-blue-600/10 dark:bg-blue-600/20',
      textColor: 'text-blue-500',
      borderColor: 'border-blue-600/60',
      dotColor: 'bg-blue-500'
    },
    pending_approval: {
      label: 'Chờ phê duyệt',
      color: 'amber',
      bgColor: 'bg-amber-600/10 dark:bg-amber-600/20',
      textColor: 'text-amber-500',
      borderColor: 'border-amber-600/60',
      dotColor: 'bg-amber-500'
    },
    approved: {
      label: 'Đã phê duyệt',
      color: 'emerald',
      bgColor: 'bg-emerald-600/10 dark:bg-emerald-600/20',
      textColor: 'text-emerald-500',
      borderColor: 'border-emerald-600/60',
      dotColor: 'bg-emerald-500'
    },
    rejected: {
      label: 'Từ chối phê duyệt',
      color: 'red',
      bgColor: 'bg-red-600/10 dark:bg-red-600/20',
      textColor: 'text-red-500',
      borderColor: 'border-red-600/60',
      dotColor: 'bg-red-500'
    },
    suspended: {
      label: 'Dừng thực hiện',
      color: 'orange',
      bgColor: 'bg-orange-600/10 dark:bg-orange-600/20',
      textColor: 'text-orange-500',
      borderColor: 'border-orange-600/60',
      dotColor: 'bg-orange-500'
    },
    edit_requested: {
      label: 'Yêu cầu chỉnh sửa',
      color: 'purple',
      bgColor: 'bg-purple-600/10 dark:bg-purple-600/20',
      textColor: 'text-purple-500',
      borderColor: 'border-purple-600/60',
      dotColor: 'bg-purple-500'
    }
  };

  const config = statusConfig[status];

  return (
    <Badge 
      className={`${config.bgColor} hover:${config.bgColor} ${config.textColor} ${config.borderColor} shadow-none rounded-full ${className}`}
    >
      <div className={`h-1.5 w-1.5 rounded-full ${config.dotColor} mr-2`} />
      {config.label}
    </Badge>
  );
};

export default StatusBadge;
```

---

#### **FE-DMDA-002: Tạo Component ProjectCard cho hiển thị dự án**
**Priority:** Critical  
**Story Points:** 8  
**Description:**  
- Tạo component card hiển thị thông tin dự án
- Hiển thị đầy đủ 10 trường thông tin theo SRS
- Implement status badges với màu sắc phân biệt
- Tạo action buttons (Edit, Delete, Approve, etc.)
- Hover effects và animations

**Acceptance Criteria:**
- Hiển thị: Mã dự án, Tên dự án, Nguồn gốc, TMĐT dự kiến, TMĐT phê duyệt, Lũy kế vốn, Vốn năm hiện tại, Dự kiến vốn, Đề xuất năm sau, Trạng thái
- Status badges với design modern: dot indicator + text, rounded-full, subtle background
- Màu sắc status: Khởi tạo (blue), Chờ phê duyệt (amber), Đã phê duyệt (emerald), Từ chối (red), Dừng (orange), Yêu cầu chỉnh sửa (purple)
- Action buttons theo quyền người dùng
- Responsive design
- Loading skeleton

**Tech Stack:**
- React Component với TypeScript
- Tailwind CSS cho styling
- Shadcn/ui Badge component
- Lucide React cho icons
- Framer Motion cho animations

---

#### **FE-DMDA-003: Tạo Component ProjectList với pagination**
**Priority:** Critical  
**Story Points:** 6  
**Description:**  
- Tạo component danh sách dự án với grid/list view
- Implement pagination với 20 items per page
- Tạo loading states và empty states
- Implement infinite scroll (optional)
- Search và filter functionality

**Acceptance Criteria:**
- Hiển thị danh sách dự án dạng grid hoặc list
- Pagination với prev/next, page numbers
- Loading skeleton khi fetch data
- Empty state với illustration
- Search box với debounce
- Filter chips hiển thị active filters

**Tech Stack:**
- React Query cho data fetching
- React Hook Form cho search
- Shadcn/ui Pagination component
- React Virtual cho performance (nếu cần)

---

### 🎯 **Task Group 2: Filter & Search System**

#### **FE-DMDA-004: Tạo Component FilterPanel cho bộ lọc dự án**
**Priority:** High  
**Story Points:** 8  
**Description:**  
- Tạo panel bộ lọc với 4 loại filter chính
- Implement filter theo năm, loại dự án, nguồn gốc, trạng thái
- Tạo filter chips hiển thị active filters
- Implement clear all filters functionality
- Save filter preferences

**Acceptance Criteria:**
- Filter theo năm: Dropdown với các năm có dữ liệu
- Filter theo loại dự án: Đầu tư, Mua sắm, Thuê dịch vụ, Bảo trì
- Filter theo nguồn gốc: Dự án Mới, Dự án Chuyển tiếp
- Filter theo trạng thái: 6 trạng thái với màu sắc
- Filter chips với remove functionality
- Clear all filters button
- Filter preferences được lưu trong localStorage

**Tech Stack:**
- Shadcn/ui Select, Checkbox components
- React Hook Form cho form handling
- Zustand cho state management
- LocalStorage cho preferences

---

#### **FE-DMDA-005: Tạo Component SearchBox với advanced search**
**Priority:** High  
**Story Points:** 5  
**Description:**  
- Tạo search box với debounce
- Implement search theo tên dự án, mã dự án
- Tạo search suggestions/autocomplete
- Implement search history
- Highlight search results

**Acceptance Criteria:**
- Search box với debounce 300ms
- Search theo: tên dự án, mã dự án
- Autocomplete suggestions
- Search history (5 items gần nhất)
- Highlight search terms trong results
- Clear search functionality

**Tech Stack:**
- React Hook Form
- Debounce hook
- Shadcn/ui Input component
- Fuse.js cho fuzzy search

---

### 🎯 **Task Group 3: Project Management Forms**

#### **FE-DMDA-006: Tạo Component CreateProjectForm**
**Priority:** Critical  
**Story Points:** 12  
**Description:**  
- Tạo form tạo dự án mới với 4 sections
- Implement validation cho tất cả fields
- Tạo multi-step form hoặc single page form
- Implement auto-save draft functionality
- Integration với API

**Acceptance Criteria:**
- Form chia 4 sections: Thông tin cơ bản, Thông tin bổ sung, Tổng mức đầu tư & Kế hoạch vốn, Các mốc phê duyệt
- Validation real-time cho tất cả fields
- Auto-save draft mỗi 30 giây
- Submit form với loading state
- Success/error handling
- Redirect sau khi tạo thành công

**Tech Stack:**
- React Hook Form + Zod validation
- Shadcn/ui Form components
- Multi-step form hoặc Accordion
- React Query cho API calls
- Toast notifications

---

#### **FE-DMDA-007: Tạo Component EditProjectForm**
**Priority:** High  
**Story Points:** 10  
**Description:**  
- Tạo form chỉnh sửa dự án
- Implement conditional editing theo trạng thái
- Tạo edit request modal cho dự án đã phê duyệt
- Implement change tracking
- Auto-save functionality

**Acceptance Criteria:**
- Form chỉnh sửa với pre-filled data
- Conditional editing: có thể edit trực tiếp nếu initialized/pending_approval
- Edit request modal nếu approved
- Change tracking với diff view
- Auto-save mỗi 30 giây
- Validation và error handling

**Tech Stack:**
- React Hook Form
- Shadcn/ui Dialog/Modal
- React Diff Viewer
- Zustand cho state management

---

#### **FE-DMDA-008: Tạo Component ProjectDetailModal**
**Priority:** Medium  
**Story Points:** 6  
**Description:**  
- Tạo modal hiển thị chi tiết dự án
- Implement tabs cho different sections
- Tạo action buttons theo quyền
- Implement project history timeline
- Responsive design

**Acceptance Criteria:**
- Modal với tabs: Thông tin chung, Tài chính, Lịch sử, Hoạt động
- Action buttons: Edit, Delete, Approve, Suspend
- Project history timeline
- Responsive design
- Keyboard navigation

**Tech Stack:**
- Shadcn/ui Dialog, Tabs components
- React Timeline component
- Framer Motion cho animations

---

### 🎯 **Task Group 4: Approval Workflow**

#### **FE-DMDA-009: Tạo Component ApprovalWorkflow**
**Priority:** High  
**Story Points:** 10  
**Description:**  
- Tạo workflow cho quá trình phê duyệt
- Implement approval buttons và modals
- Tạo approval history timeline
- Implement bulk approval functionality
- Status transition animations

**Acceptance Criteria:**
- Approval buttons: Submit for Approval, Approve, Reject
- Approval modal với comment field
- Bulk approval với multi-select
- Approval history timeline
- Status transition animations
- Email notifications (mock)

**Tech Stack:**
- React Hook Form
- Shadcn/ui Dialog, Button components
- Framer Motion cho animations
- React Query cho API calls

---

#### **FE-DMDA-010: Tạo Component BulkActions**
**Priority:** Medium  
**Story Points:** 8  
**Description:**  
- Tạo bulk actions cho nhiều dự án
- Implement multi-select với checkboxes
- Tạo bulk approval, delete, export
- Implement progress indicator
- Error handling cho bulk operations

**Acceptance Criteria:**
- Multi-select với select all/none
- Bulk actions: Approve, Delete, Export
- Progress indicator cho bulk operations
- Error handling với retry functionality
- Success/error notifications

**Tech Stack:**
- React Hook Form
- Shadcn/ui Checkbox, Button components
- React Query cho API calls
- Toast notifications

---

### 🎯 **Task Group 5: Data Visualization & Export**

#### **FE-DMDA-011: Tạo Component ProjectStats**
**Priority:** Medium  
**Story Points:** 6  
**Description:**  
- Tạo dashboard với project statistics
- Implement charts và graphs
- Tạo summary cards
- Implement real-time updates
- Responsive design

**Acceptance Criteria:**
- Summary cards: Tổng dự án, Đã phê duyệt, Chờ phê duyệt, Từ chối
- Charts: Dự án theo loại, Dự án theo tháng, Budget allocation
- Real-time updates
- Responsive design
- Export charts functionality

**Tech Stack:**
- Recharts hoặc Chart.js
- Shadcn/ui Card components
- React Query cho real-time data
- React Window cho performance

---

#### **FE-DMDA-012: Tạo Component ExportManager**
**Priority:** Medium  
**Story Points:** 5  
**Description:**  
- Tạo export functionality cho Excel/PDF
- Implement export templates
- Tạo export history
- Implement progress tracking
- Download management

**Acceptance Criteria:**
- Export to Excel/PDF
- Export templates: Full list, Filtered results
- Export history với status
- Progress tracking
- Download management
- Email export (optional)

**Tech Stack:**
- XLSX.js cho Excel export
- jsPDF cho PDF export
- React Query cho API calls
- Shadcn/ui Progress component

---

### 🎯 **Task Group 6: Advanced Features**

#### **FE-DMDA-013: Tạo Component KanbanBoard**
**Priority:** Low  
**Story Points:** 12  
**Description:**  
- Tạo Kanban board view cho dự án
- Implement drag & drop functionality
- Tạo columns theo trạng thái
- Implement card details modal
- Real-time updates

**Acceptance Criteria:**
- Kanban columns: Khởi tạo, Chờ phê duyệt, Đã phê duyệt, Từ chối, Dừng, Yêu cầu chỉnh sửa
- Drag & drop giữa columns
- Card details modal
- Real-time updates
- Responsive design
- Column collapse/expand

**Tech Stack:**
- React DnD hoặc @dnd-kit
- Framer Motion cho animations
- React Query cho real-time data
- Shadcn/ui components

---

#### **FE-DMDA-014: Tạo Component ActivityLog**
**Priority:** Low  
**Story Points:** 6  
**Description:**  
- Tạo activity log cho dự án
- Implement timeline view
- Tạo filter theo action type
- Implement real-time updates
- Export log functionality

**Acceptance Criteria:**
- Timeline view của activities
- Filter theo action type
- Real-time updates
- Export log
- Responsive design
- Search trong log

**Tech Stack:**
- React Timeline component
- React Query cho real-time data
- Fuse.js cho search
- Shadcn/ui components

---

### 🎯 **Task Group 7: Performance & Optimization**

#### **FE-DMDA-015: Implement Virtual Scrolling**
**Priority:** Medium  
**Story Points:** 8  
**Description:**  
- Implement virtual scrolling cho large lists
- Optimize rendering performance
- Implement lazy loading
- Memory management
- Performance monitoring

**Acceptance Criteria:**
- Virtual scrolling cho lists > 1000 items
- Smooth scrolling performance
- Lazy loading images
- Memory usage optimization
- Performance metrics tracking

**Tech Stack:**
- React Virtual hoặc React Window
- React Query cho data fetching
- Performance monitoring tools
- React DevTools Profiler

---

#### **FE-DMDA-016: Implement Caching Strategy**
**Priority:** Medium  
**Story Points:** 6  
**Description:**  
- Implement caching cho API responses
- Optimize data fetching
- Implement offline support
- Cache invalidation strategy
- Performance optimization

**Acceptance Criteria:**
- React Query caching
- Offline support với Service Worker
- Cache invalidation rules
- Background sync
- Performance improvements

**Tech Stack:**
- React Query
- Service Worker
- IndexedDB cho offline storage
- React Query DevTools

---

### 🎯 **Task Group 8: UI/UX Enhancements**

#### **FE-DMDA-017: Tạo Component LoadingStates**
**Priority:** Medium  
**Story Points:** 4  
**Description:**  
- Tạo loading states cho tất cả components
- Implement skeleton loaders
- Tạo loading animations
- Implement error states
- Accessibility improvements

**Acceptance Criteria:**
- Skeleton loaders cho lists, cards, forms
- Loading animations
- Error states với retry functionality
- Accessibility improvements
- Consistent loading experience

**Tech Stack:**
- Shadcn/ui Skeleton components
- Framer Motion cho animations
- React Error Boundary
- Accessibility testing tools

---

#### **FE-DMDA-018: Implement Dark Mode**
**Priority:** Low  
**Story Points:** 5  
**Description:**  
- Implement dark mode theme
- Tạo theme toggle
- Implement system preference detection
- Theme persistence
- Accessibility considerations

**Acceptance Criteria:**
- Dark mode theme
- Theme toggle button
- System preference detection
- Theme persistence
- Accessibility compliance

**Tech Stack:**
- Next.js Theme Provider
- Tailwind CSS dark mode
- LocalStorage cho persistence
- Accessibility testing

---

## 📊 **Task Summary**

### **Priority Distribution:**
- **Critical:** 5 tasks (FE-DMDA-001, 001.5, 002, 003, 006)
- **High:** 4 tasks (FE-DMDA-004, 005, 007, 009)
- **Medium:** 6 tasks (FE-DMDA-008, 010, 011, 012, 015, 016, 017)
- **Low:** 4 tasks (FE-DMDA-013, 014, 018)

### **Story Points Distribution:**
- **Total Story Points:** 123+
- **Critical:** 34 points
- **High:** 31 points
- **Medium:** 45 points
- **Low:** 23 points

### **Estimated Timeline:**
- **Sprint 1 (2 weeks):** Critical tasks (34 points)
- **Sprint 2 (2 weeks):** High priority tasks (31 points)
- **Sprint 3 (3 weeks):** Medium priority tasks (45 points)
- **Sprint 4 (2 weeks):** Low priority tasks + polish (23 points)

### **Tech Stack Summary:**
- **Framework:** Next.js 14 + TypeScript
- **Styling:** Tailwind CSS + Shadcn/ui
- **State Management:** Zustand + React Query
- **Forms:** React Hook Form + Zod
- **Animations:** Framer Motion
- **Charts:** Recharts
- **Testing:** Jest + React Testing Library
- **Performance:** React Virtual, Service Worker

---

## 🚀 **Getting Started**

### **Setup Commands:**
```bash
# Install dependencies
npm install

# Install Shadcn/ui
npx shadcn@latest init

# Add required components
npx shadcn@latest add button card dialog form input select tabs

# Start development
npm run dev
```

### **Development Guidelines:**
1. **Component Structure:** Atomic design principles
2. **TypeScript:** Strict mode enabled
3. **Testing:** Minimum 80% coverage
4. **Performance:** Lighthouse score > 90
5. **Accessibility:** WCAG 2.1 AA compliance

---

**Document Version:** 1.0  
**Last Updated:** 08-2024  
**Created By:** AI Assistant  
**Review By:** Frontend Team
