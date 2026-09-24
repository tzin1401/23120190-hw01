# HW01 - CONSTRAINTS AND RULES CONTEXT

*Đây là file tổng hợp toàn bộ quy tắc, tiêu chuẩn và các ràng buộc (constraints) từ đề bài gốc `2026.HW01.Jobs.Defects.PhysicalProduct_En.pdf`. File này được dùng làm "system prompt" hoặc tài liệu tham chiếu nghiêm ngặt khi bắt đầu thực hiện bài tập.*

---

## 1. QUY TẮC CHỐNG GIAN LẬN (ANTI-CHEAT MECHANISMS)

**TUYỆT ĐỐI KHÔNG SỬ DỤNG AI ĐỂ TẠO RA CÁC TÀI LIỆU SAU ĐÂY:**

1. **Ảnh chụp thiết bị:** Phải là ảnh thật, có chứa Thẻ sinh viên (Student-ID card) trong cùng 1 khung hình.
2. **Video thực hành:** Phải có giọng nói thuyết minh (voice narration) của chính sinh viên.
3. **Ảnh chụp màn hình tin tuyển dụng:** Cả 10 ảnh chụp phải hiển thị tên đăng nhập/tên tài khoản (login/username) của sinh viên ở góc màn hình.
4. **Lịch sử chat AI (Prompt log):** Phải là file `.md` hoặc `.txt` có chứa mốc thời gian thực (timestamps) cho TỪNG câu lệnh gửi cho AI.

*Hình phạt: Nếu phát hiện bất kỳ mục nào trên đây là do AI tạo ra (fake), bài tập nhận 0 điểm và sinh viên bị đưa lên Hội đồng kỷ luật.*

---

## 2. RÀNG BUỘC CHO YÊU CẦU 1: JOB MARKET 2026+ (10 Jobs)

- **Số lượng:** Đúng 10 tin tuyển dụng QA/QC.
- **Thời gian:** Tin đăng trong vòng **60 ngày** tính đến ngày nộp bài.
- **Phân loại bắt buộc:** Ít nhất **3/10** vị trí phải yêu cầu kỹ năng AI / LLM / Automation-AI.
- **Thông tin cho mỗi tin tuyển dụng:**
  - Link gốc.
  - Ảnh chụp màn hình có ngày tháng & tên tài khoản.
  - Mô tả công việc (Job description).
  - Kỹ năng yêu cầu (Required skills).
  - Mức lương (Salary).
  - **Phân tích (AI Impact Analysis):** Đúng 1-2 câu tự viết đánh giá tác động của AI đến công việc này.

---

## 3. RÀNG BUỘC CHO YÊU CẦU 2: 20 SOFTWARE DEFECTS (20 Lỗi)

- **Số lượng:** Đúng 20 lỗi phần mềm đã được công bố.
- **Thời gian:** Từ năm 2022 đến 2026.
- **Phân loại bắt buộc:** Ít nhất **5/20** lỗi liên quan trực tiếp đến AI/LLM (ảo giác, prompt injection, thiên kiến).
- **Thông tin cho mỗi lỗi:**
  - Nguồn (Source link).
  - Mô tả (Description).
  - Mức độ nghiêm trọng (Severity).
  - Hậu quả (Consequences).
  - Cách khắc phục (Solution).
- **RÀNG BUỘC CỐT LÕI VỀ AI (BẮT BUỘC CHO CẢ 20 LỖI):**
  - Phải yêu cầu AI giải thích về lỗi này.
  - Với **MỖI LỖI (100% cả 20 lỗi)**, sinh viên phải tìm ra và chỉ định đúng **1 điểm mà AI đã bị thiên kiến hoặc ảo giác (bias/hallucination)** trong phần giải thích của AI.

---

## 4. RÀNG BUỘC CHO YÊU CẦU 3: PHYSICAL PRODUCT TESTING

- **Đối tượng:** MỘT (1) thiết bị gia dụng cụ thể (quạt, máy lọc, nồi cơm, bóng đèn...). Không test phần mềm.
- **Thông tin khai báo:** Tên Hãng (Brand), Dòng máy (Model), Năm SX (Year), Số Serial (Che 4 ký tự ở giữa).
- **Thiết kế Test Cases:**
  - Số lượng: **15 Test cases**.
  - Format: Objective / Input / Steps / Expected / Actual / Verdict.
  - **Edge Cases:** Ít nhất **3 test cases** phải là trường hợp ngoại lệ mà **AI KHÔNG THỂ TÌM RA**. Yêu cầu đính kèm ảnh chụp màn hình chứng minh AI không tạo ra 3 test case này + Lời giải thích bằng văn bản vì sao AI lại bỏ sót.
- **Thực thi:**
  - Thực hiện trên thiết bị thật ít nhất **5 test cases**.
  - Quay ít nhất **5 video ngắn (<=60s)** up lên YouTube (Unlisted).
  - Mục tiêu: Cố gắng tìm ra >= 5 defects thật từ thiết bị.
  - **Report Bug:** Không dùng Mantis. Báo cáo mọi lỗi tìm được lên trang **Issues** trên GitHub repository của cá nhân sinh viên (Có chụp màn hình chứa username GitHub).
- **Mindmap (Outcome G9.1):** Yêu cầu AI vẽ 1 sơ đồ tư duy (ISTQB/QA Role mindmap). Sinh viên phải tìm ra **3 chỗ sai** của AI trong sơ đồ đó.

---

## 5. RÀNG BUỘC VỀ THỦ TỤC VÀ HỒ SƠ AI (AI COMPLIANCE)

*Thiếu bất kỳ hồ sơ nào trong phần này sẽ bị trừ toàn bộ điểm Cột AI (15-20 điểm).*

1. **AI Audit Report (Form AI-02):** Bắt buộc điền cho mỗi batch nội dung do AI tạo (test case, giải thích defect, mindmap...). Gồm 5 mục:
   - (1) Prompt + Tên tool AI + Timestamp (Giờ:Phút Ngày/Tháng/Năm).
   - (2) Full kết quả AI (Hoặc ảnh chụp có khoanh đỏ), không tóm tắt.
   - (3) Verdict: VALID / INVALID / INCOMPLETE.
   - (4) Lý do (2-5 câu) đối chiếu với tài liệu/ISTQB.
   - (5) Cách sinh viên sửa lại kết quả của AI.
     *(Tính tổng kết tỷ lệ phần trăm VALID/INVALID ở cuối báo cáo).*
2. **AI Critique:** Viết 1 đoạn **200-300 chữ** đánh giá lỗi sai/thiên kiến của AI, lý do AI bỏ sót, và bài học rút ra.
3. **Mandatory Disclosure:** Chèn đoạn văn bản cam kết theo mẫu (Mục 5 trong đề) vào trước các Phụ lục trong file Report.
4. **Ký Form:** Phải nộp kèm bản đã ký của `[AI-03] Disclosure Form` và `[AI-05] Privacy Checklist`.
5. **Appendix A (Phụ lục A):** Chứa file log `.md` hoặc `.txt` ghi lại TOÀN BỘ prompt và response, bắt buộc có Timestamps.

---

## 6. QUY TẮC ĐÓNG GÓI VÀ NỘP BÀI (SUBMISSION)

- **Định dạng tên file Zip:** `StudentID_HW01_AI_<grade>.zip` (grade là điểm tự đánh giá, 3 chữ số `[000, 100]`).
- **Nội dung bên trong file Zip:**
  - File Report chính (PDF), chứa Audit Report, AI Critique, Mandatory Disclosure.
  - Appendix A (Full prompt log có timestamps).
  - File Excel (Test Cases / Checklist / Test Summary Report).
  - Ảnh chụp màn hình trang GitHub Issues (Ghi nhận lỗi phần cứng).
  - 1 Ảnh chụp thiết bị cùng Thẻ sinh viên (`.jpg`).
  - File Mindmap (PNG hoặc Markdown).
  - Các Form AI-03, AI-05 (PDF/Ảnh).
- **Vấn đáp:** Chuẩn bị tinh thần chạy live test case, giải thích lý do thiết kế, chỉ ra lỗi của AI. Rớt >= 2 câu hỏi sẽ bị chia đôi (x0.5) tổng điểm HW.
