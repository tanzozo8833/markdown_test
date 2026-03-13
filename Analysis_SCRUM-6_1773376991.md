Chào bạn, với tư cách là phiên bản 3.1 Pro Preview, tôi đã tiếp nhận và phân tích kỹ lưỡng dữ liệu từ Jira. Dưới đây là kết quả phân tích hệ thống chi tiết:

---

### 1. PHÂN LOẠI ĐỐI TƯỢNG
Dựa trên ngôn ngữ tự nhiên, ngữ cảnh mô tả (trải nghiệm người dùng) và mức độ tổng quát của vấn đề, tôi xác định:
*   **Phân loại:** **Khách hàng (End-user)**.
*   **Lý do:** Người dùng mô tả các triệu chứng bề mặt (symptom-based) thay vì chỉ ra các lớp, logic hay tiến trình kỹ thuật (technical-based). Đây là dạng phản hồi "Bug Report" điển hình từ người dùng cuối.

---

### 2. CHIẾT XUẤT BUG
Dựa trên báo cáo, hệ thống đang gặp phải các vấn đề về hiệu năng (Performance) và tính ổn định (Stability).

| ID | Mô tả Bug | Độ nghiêm trọng dự đoán |
| :--- | :--- | :--- |
| **BUG-01** | Các nút bấm không phản hồi (Unresponsive UI elements) | **High** |
| **BUG-02** | Thời gian tải trang quá lâu (Latency/Slow loading) | **Medium** |
| **BUG-03** | Treo màn hình (Screen freezing) | **Critical** |
| **BUG-04** | Ứng dụng tự đóng đột ngột (App crash) | **Critical** |
| **BUG-05** | Tính năng bị vô hiệu hóa sau khi Login | **High** |
| **BUG-06** | Hiển thị dữ liệu sai hoặc mất dữ liệu (Data integrity/Fetch error) | **Critical** |

> **Trích dẫn quan trọng:**
> "Overall, the website feels slow and unstable, so I’m having trouble completing normal actions on the platform."

---

### 3. ĐÁNH GIÁ VÀ KHUYẾN NGHỊ KỸ THUẬT

Dưới đây là checklist các hành động cần thiết cho đội ngũ kỹ thuật để ưu tiên xử lý:

- [ ] **Điều tra nguyên nhân gốc rễ (Root Cause Analysis):** 
    - Kiểm tra logs của server khi xảy ra lỗi `App crash` và `Screen freezing`.
    - Kiểm tra trạng thái của các `API endpoints` sau khi xác thực (đối với BUG-05).
- [ ] **Tối ưu hóa hiệu năng:** 
    - Đánh giá lại `Bundle size` và `Network requests` để giải quyết vấn đề tải trang chậm.
- [ ] **Kiểm tra tính nhất quán dữ liệu:** 
    - Rà soát lại `Database query` và cơ chế `State management` (Redux/Context) để tìm nguyên nhân dữ liệu không hiển thị đúng (BUG-06).

---

### PHÂN TÍCH CHUYÊN GIA (PRO PREVIEW INSIGHT)
Việc người dùng báo cáo nhiều vấn đề xảy ra cùng lúc (từ crash, treo máy đến mất dữ liệu) cho thấy hệ thống đang gặp lỗi nghiêm trọng ở **lớp trung gian (Middle-tier)** hoặc **Quản lý phiên (Session Management)**. 

**Khuyến nghị:**
1. Cần thực hiện **Log Tracing** ngay lập tức trên các request sau khi user đăng nhập.
2. Kiểm tra lại các **Exception Handling** ở phía Client vì ứng dụng tự đóng (Crash) mà không có thông báo lỗi cụ thể cho thấy có thể là lỗi Memory Leak hoặc Uncaught Promise Rejection.
3. Cần cung cấp các câu hỏi hỏi đáp (Follow-up) cho người dùng để biết: *Họ đang sử dụng thiết bị nào? Trình duyệt nào? Thời điểm xảy ra lỗi cụ thể?* để hỗ trợ việc tái hiện lỗi (reproduce).

---
*Báo cáo được tạo bởi AI System Analysis 3.1 Pro Preview.*