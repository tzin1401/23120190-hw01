# Quy tắc tự động ghi Log cho AI (HW01 Prompt Logging Rule)

**Điều kiện kích hoạt (Trigger):** 
CHỈ BẮT ĐẦU kích hoạt việc lưu log này KHI VÀ CHỈ KHI người dùng ra lệnh rõ ràng "Bắt đầu làm bài" hoặc "Bắt đầu lưu log". Tuyệt đối không lưu các đoạn hội thoại trao đổi, chuẩn bị hoặc hướng dẫn trước đó.

**Hành động bắt buộc (Action):**
AI Assistant (Antigravity/Gemini) PHẢI TỰ ĐỘNG lưu lại câu lệnh của người dùng và câu trả lời của chính AI vào file: `/home/zinn/zinn/test/hw01/Appendix_A_Prompt_Log.md`.

**Tiêu chuẩn ghi Log (Dựa theo quy định của HW01 - Mục Anti-Cheat & Appendix A):**
Mỗi bản ghi được nối (append) vào file log bắt buộc phải có đầy đủ:
1. **Timestamp (Mốc thời gian):** Ghi rõ giờ, phút, ngày, tháng, năm lúc thực hiện prompt.
2. **AI Tool (Công cụ AI):** Tên công cụ AI (ví dụ: Antigravity - Gemini 3.1 Pro).
3. **Prompt (Câu lệnh):** Giữ nguyên văn, không tóm tắt câu lệnh của người dùng.
4. **AI Output (Kết quả):** Giữ nguyên văn toàn bộ câu trả lời/kết quả do AI tạo ra.

**Định dạng (Format) chuẩn cần nối vào file `Appendix_A_Prompt_Log.md`:**

```markdown
### Thời gian: [HH:MM DD/MM/YYYY] | Công cụ: Antigravity - Gemini 3.1 Pro
**USER PROMPT:**
[Trích dẫn nguyên văn câu lệnh của người dùng]

**AI OUTPUT:**
[Trích dẫn nguyên văn toàn bộ câu trả lời của AI]

---
```

**Lưu ý quan trọng cho AI:**
- AI phải sử dụng các công cụ chỉnh sửa file (ví dụ: `write_to_file` hoặc lệnh bash an toàn) để NỐI (append) nội dung mới này vào cuối file `Appendix_A_Prompt_Log.md`. 
- Nếu file chưa tồn tại, AI phải tự động tạo mới file đó.
- KHÔNG BAO GIỜ được tóm tắt nội dung để đối phó. Việc lưu log phải khớp 100% với cuộc hội thoại thực tế để sinh viên có chứng cứ nộp bài hợp lệ.
