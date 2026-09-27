# Requirement 3 — kiểm thử quạt đứng Senko L1638

Thiết bị đã chọn: **quạt Senko L1638**, năm **2022** theo thông tin người sở hữu. **Thiết bị không có số serial**, theo xác nhận của người sở hữu; ghi đúng tình trạng này trong báo cáo, không tạo số serial giả.

| Thư mục | Bằng chứng cần đặt vào |
|---|---|
| `01_Device_Photo/` | Một ảnh **JPG do bạn tự chụp**, trong cùng khung hình có quạt thật và thẻ sinh viên. |
| `02_AI_Test_Case_Output_Screenshots/` | Ảnh chụp nguyên cuộc hội thoại/output AI đã đề xuất test case; giữ rõ tên công cụ và nội dung để đối chiếu với prompt log. |
| `03_Edge_Cases/` | Phần giải thích bằng chữ cho **ít nhất 3 edge case bạn tự bổ sung**; đặt ảnh hội thoại chứng minh AI không nêu các case đó trong `AI_Omission_Screenshots/`. Ghi ID của từng case và lý do AI bỏ sót. |
| `04_Test_Cases_Excel/` | Workbook `.xlsx` có **Test Cases / Checklist / Test Summary Report**. Bộ cuối cùng có **15 test case tổng cộng** với Objective, Input, Steps, Expected, Actual, Verdict; ghi `Not Run` cho case chưa thực thi. |
| `05_Execution_Videos/` | Danh sách URL của **ít nhất 5 video YouTube Unlisted**, mỗi video **không quá 60 giây**, có giọng thuyết minh thật của bạn và liên kết rõ với ID test case. Có thể giữ bản video gốc ở đây nếu cần. |
| `06_GitHub_Issues_Evidence/` | Ảnh chụp trang Issues trong repo GitHub của bạn, nhìn rõ username; liên kết Issue của các lỗi **thực sự quan sát được** với test case và video. Đề yêu cầu cố gắng tìm ít nhất 5 lỗi. |
| `07_AI_Audit_Evidence/` | Ảnh AI output có viền đỏ/chú thích nếu dùng cách nộp này cho `[AI-02]`; giữ nguyên bản output gốc ở `02_AI_Test_Case_Output_Screenshots/`. |

Prompt và output nguyên văn đã lưu trong [`Appendix_A_Prompt_Log.md`](../Appendix_A_Prompt_Log.md) ở thư mục gốc; **không tạo lại hoặc sửa lịch sử hội thoại**. Nếu dùng bộ 12 case AI vừa đề xuất, hãy tự bổ sung 3 edge case để đủ 15 và giữ bằng chứng AI đã bỏ sót chúng.

Đã có [bản phân tích TC13–TC15](03_Edge_Cases/TC13_TC15_Analysis.md) và [workbook 15 test case](04_Test_Cases_Excel/Senko_L1638_15_Test_Cases.xlsx). Theo kết quả người kiểm thử xác nhận: **TC03, TC04, TC07, TC14 Pass; TC05 Fail** với hiện tượng mô tả trong [bản nháp Issue](06_GitHub_Issues_Evidence/TC05_Issue_Draft.md). Mười case còn lại là `Not Run`. Đã có [5 link video YouTube](05_Execution_Videos/YouTube_Links.md); người đăng xác nhận đã chuyển cả năm sang Không công khai. Trước khi chạy các case còn lại, xác nhận tính năng thật của quạt, đặc biệt TC06 (hẹn giờ), TC13 (chỉnh cao) và TC15 (chuyển hướng). Nếu TC06 không áp dụng, thay bằng một case khả thi để bộ cuối vẫn có 15 case thực thi được.

Trong bài nộp chung, còn cần **report PDF** (gồm Requirement 3, AI Critique 200–300 từ, Mandatory Disclosure, Self-Assessment và phụ lục `[AI-02]`), cùng biểu mẫu `[AI-03]`, `[AI-05]` đã ký. Các biểu mẫu gốc đang ở thư mục gốc của bài; không cần tạo bản trùng trong thư mục này. Xem [hướng dẫn tổng hợp](../HW01_StepByStep_Guide.md) để đóng gói ZIP.
