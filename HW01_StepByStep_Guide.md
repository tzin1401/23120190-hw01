# Hướng dẫn từng bước làm HW01 — QA/QC Jobs, 20 Defects, Physical Product

> Đối chiếu theo `2026.HW01.Jobs.Defects.PhysicalProduct_En.pdf` (7 trang). Xem deadline và thông báo mới trên Moodle trước khi nộp. Đây là bài **cá nhân**, thời lượng dự kiến **5 giờ**. HW01 **không dùng EShop SUT**.

## 0. Nắm rõ đầu ra và cách chấm

| Hạng mục                            | Yêu cầu chính                                          | Điểm trong rubric |
| ------------------------------------- | --------------------------------------------------------- | ------------------: |
| Thị trường việc làm QA/QC 2026+  | 10 tin tuyển dụng và AI Impact Analysis                |                  40 |
| Lỗi phần mềm 2022–2026            | 20 lỗi, có phân tích sai lệch của AI cho từng lỗi |                  20 |
| Sản phẩm vật lý                   | 15 test case, thực thi/quay ít nhất 5 case             |                  25 |
| AI-02 Audit Report                    | Đủ 5 phần cho từng artifact AI                        |                   8 |
| AI Critique + AI-03                   | Đoạn 200–300 từ và form công bố AI                 |                   4 |
| AI-05 + bằng chứng chống gian lận | Checklist ký tên và bằng chứng thật                 |                   3 |
| **Tổng**                       |                                                           |       **100** |

Trong phần mô tả, Requirement 3 được gọi là **40 điểm**; rubric tách phần này thành **25 điểm cho test sản phẩm** và **15 điểm cho AI compliance**. Dùng bảng rubric trên để tự chấm.

## 1. Chuẩn bị trước khi làm

1. Xem **deadline trên Moodle**. Tin tuyển dụng phải được đăng trong **60 ngày tính tới ngày nộp bài**; khi đổi ngày nộp, kiểm tra lại mốc này.
2. Kiểm tra `[AI-06] Student Acknowledgement` đã được ký ở Tuần 1; đây là điều kiện để bài có dùng AI được chấm.
3. Tạo nơi lưu bằng chứng gốc: ảnh tin tuyển dụng, nguồn lỗi, ảnh thiết bị, ảnh hội thoại AI, video, ảnh GitHub Issues. Giữ URL và ngày tương ứng để đối chiếu.
4. Tạo `Appendix_A_Prompt_Log.md` hoặc `.txt`. Ghi **mọi prompt đã gửi cho AI** theo đúng thứ tự, có thời gian `HH:MM dd/mm/yyyy` và tên công cụ. Giữ nguyên văn prompt và output; không tạo lại hoặc sửa nội dung để thay cho lịch sử thật. Một prompt tạo cả loạt 15 test case vẫn phải được ghi đầy đủ, nhưng trong AI Audit có thể tính là **một artifact**.
5. Chuẩn bị report để cuối cùng xuất **PDF**, file **Excel** cho test case/checklist/test summary, và các biểu mẫu `[AI-02]`, `[AI-03]`, `[AI-05]` trong thư mục AI Templates.
6. Chọn **một thiết bị gia dụng cụ thể mà bạn sở hữu**. Ghi hãng, model, năm, số serial **che 4 ký tự giữa**. Tự chụp **một ảnh JPG có chính thiết bị và thẻ sinh viên trong cùng khung hình**.

### Bằng chứng tuyệt đối không dùng AI tạo ra

- Ảnh thiết bị cùng thẻ sinh viên.
- Video thao tác thật, có **giọng thuyết minh của chính bạn**.
- Cả 10 ảnh chụp tin tuyển dụng, trên đó hiện **login name/display name** của tài khoản bạn trên nền tảng tuyển dụng. **Chỉ thấy avatar là chưa đủ chắc chắn.**
- File prompt log `.md` có mốc thời gian và nội dung trung thực của mọi prompt.

Đề quy định vi phạm các mục trên có thể khiến **toàn bài nhận 0** và bị chuyển xử lý kỷ luật. Không bịa bằng chứng, kết quả test, lỗi thiết bị hoặc sai sót của AI.

## 2. Requirement 1 — 10 tin tuyển dụng QA/QC (40 điểm)

1. Tìm **10 tin QA/QC được đăng trong vòng 60 ngày trước ngày nộp**. Trong đó **ít nhất 3 vị trí yêu cầu kỹ năng AI/LLM/automation-AI**; không tính vị trí chỉ nhắc AI mơ hồ nếu phần yêu cầu kỹ năng không có.
2. Với **mỗi tin**, lưu:
   - URL trực tiếp và thông tin ngày đăng;
   - ảnh chụp có ngày và **tên đăng nhập/tên hiển thị** của bạn ở góc giao diện;
   - mô tả công việc, kỹ năng bắt buộc, mức lương (nếu tin không công bố, ghi rõ **“không công bố”**, không tự đoán);
   - **1–2 câu AI Impact Analysis** về tác động AI lên công việc đó.
3. Đưa đủ 10 tin vào report, liên kết từng tin với đúng ảnh bằng chứng. Đánh dấu rõ 3 tin đạt điều kiện AI/LLM/automation-AI.
4. Thêm một đoạn tổng hợp ngắn phân biệt việc QA/QC nào AI có thể **thay thế**, việc nào AI **hỗ trợ**, và việc nào AI **không thể thay thế**. Đây là learning outcome của đề.

## 3. Requirement 2 — 20 lỗi phần mềm công bố trong 2022–2026 (20 điểm)

1. Tìm **20 lỗi phần mềm được công bố trong giai đoạn 2022–2026**; ít nhất **5 lỗi liên quan AI/LLM** như hallucination, prompt injection, bias. Ghi ngày công bố để chứng minh khoảng thời gian.
2. Với **mỗi lỗi**, đưa vào report: nguồn/URL, mô tả lỗi, severity, hậu quả và cách khắc phục. Phân biệt cách khắc phục đã được công bố với đề xuất của bạn.
3. Cho AI giải thích từng lỗi hoặc một nhóm lỗi và lưu prompt/output thật. Với **cả 20 lỗi**, chỉ ra **một chỗ AI thiên kiến hoặc bịa/sai sự thật khi giải thích chính lỗi đó**, trích nội dung AI liên quan, giải thích vì sao sai và đối chiếu nguồn. Tổng cộng cần **20 trường hợp**.
4. Nếu AI không mắc lỗi ở một lượt, tiếp tục kiểm tra hoặc hỏi sâu thêm, ghi lại prompt mới. **Không gán lỗi cho AI khi output không có lỗi.**

## 4. Requirement 3 — kiểm thử một thiết bị vật lý cụ thể

### 4.1. Thiết kế 15 test case

1. Mô tả thiết bị đã chọn: **brand, model, year, serial đã che 4 ký tự giữa**; dẫn tới ảnh thiết bị cùng thẻ sinh viên.
2. Có thể dùng AI để đề xuất test case; lưu nguyên prompt và output cho AI Audit. Kiểm tra và sửa để phù hợp đúng model, tính năng và điều kiện sử dụng thực tế.
3. Nộp **15 test case tổng cộng**, mỗi case có đủ **Objective / Input / Steps / Expected / Actual / Verdict**. Đánh số để liên kết với video, kết quả và GitHub Issue.
4. Trong 15 case, có **ít nhất 3 edge case do bạn bổ sung mà AI đã không nêu**. Cần cả **(a) ảnh chụp hội thoại thể hiện output AI thiếu các case đó** và **(b) giải thích bằng chữ vì sao AI bỏ sót**. Nêu rõ ID của ba case.
5. Không điền kết quả thực tế giả cho case chưa chạy: đánh dấu `Not Run`/`Not Executed` ở Actual/Verdict. Nếu một case được chạy, ghi kết quả quan sát được và verdict tương ứng.

### 4.2. Thực thi, video, lỗi và Excel

1. **Thực thi ít nhất 5 trong 15 test case trên thiết bị thật**. Quay video ngắn **không quá 60 giây mỗi video**, có **giọng thật của bạn** thuyết minh. Video cần đủ rõ để nối với ID case và kết quả quan sát.
2. Đưa **ít nhất 5 video** lên **YouTube Unlisted** và lưu URL. Nền tảng khác như Google Drive/OneDrive chỉ được chấp nhận nếu video YouTube bị gỡ/chặn vì khiếu nại bản quyền, sau khi đã thực sự cố gắng tải lên YouTube.
3. **Cố gắng tìm ít nhất 5 lỗi thật** trong lúc thực thi. Ghi những lỗi quan sát được thành **Issues trong repo GitHub của chính bạn**; kèm bước tái hiện, expected/actual và bằng chứng phù hợp. Chụp trang Issues thấy **GitHub username**. Không tạo Issue giả chỉ để đủ số lượng.
4. File Excel cần có **Test Cases / Checklist / Test Summary Report** (cập nhật dần). Test Summary tổng hợp số case đã chạy, pass/fail/not run và lỗi tìm thấy; bảo đảm khớp report, video và Issues.

## 5. Mindmap bắt buộc cho G9.1

1. Hỏi một AI Tool vẽ mindmap về **vai trò QA/QC gắn với quy trình kiểm thử ISTQB**. Cách viết này bao phủ cả phần Outcomes (“ISTQB-process mindmap”) và bảng CLO (“QA/QC role mindmap”) trong đề.
2. Lưu output gốc, prompt/timestamp và xuất mindmap **PNG hoặc Markdown**.
3. **Tự tìm 3 lỗi cụ thể** trong mindmap, giải thích cách sửa và viện dẫn slide môn học hoặc mục phù hợp của ISTQB. Đưa phần nhận xét này vào report và AI Audit.

## 6. AI Collaboration Protocol — phải có trong report

### 6.1. AI-02 AI Audit Report

Đính kèm `[AI-02]` như **phụ lục của report PDF**. Mỗi artifact do AI tạo ra cần một mục **5 phần**; một loạt kết quả tạo bằng một prompt được tính là **một artifact**, không cần 15 mục riêng cho 15 test case cùng một lần tạo.

| Phần            | Nội dung bắt buộc                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Prompt + tool | **Toàn bộ prompt**, tên AI Tool, thời gian `HH:MM dd/mm/yyyy`                                                             |
| 2. AI output     | **Toàn bộ output nguyên văn**, hoặc ảnh chụp có **viền đỏ và chú thích**; không tóm tắt/diễn đạt lại |
| 3. Verdict       | `VALID`, `INVALID` hoặc `INCOMPLETE`, kèm lý do dựa trên ISTQB/tài liệu môn học                                        |
| 4. Reasoning     | **2–5 câu** dẫn đúng slide hoặc mục ISTQB tương ứng                                                                   |
| 5. Student fix   | Bản đã sửa,**đánh dấu nội dung thay đổi**                                                                             |

Làm Audit cho các artifact AI đã dùng, chẳng hạn mindmap, phần giải thích lỗi và bộ test case. Cuối Audit, tính **tỷ lệ phần trăm VALID / INVALID / INCOMPLETE** và kết luận **khi nào nên dùng hoặc không nên dùng AI cho công việc này**. Khai báo tất cả công cụ AI đã dùng. Prompt log vẫn phải ghi **mọi prompt**, kể cả prompt không tạo một artifact nộp bài.

### 6.2. AI Critique và Mandatory Disclosure

1. Viết **một đoạn AI Critique dài 200–300 từ**: AI sai, thiên kiến hoặc thiếu ở đâu; vì sao bỏ sót; bạn rút ra nguyên tắc gì khi cộng tác với AI.
2. Dán **Mandatory Disclosure ở cuối nội dung report, trước các phụ lục**, điền đúng các phần trong ngoặc vuông theo bài thật:

   > “[Test cases / script / dataset / report] was initially generated by [AI tool name]; I reviewed and modified [section X], added [edge cases Y, Z]; [section W] was written entirely by me. The detailed AI Audit Report is attached as Appendix A. I confirm I did not use AI to generate any artifact listed in the prohibited category below.”
   >

   Câu mẫu gọi AI Audit là “Appendix A”, còn danh sách nộp bài gọi **full prompt log** là “Appendix A”. Đề dùng cùng nhãn cho hai thứ: nên đặt **AI Audit Report là Appendix A trong PDF**, còn log là file riêng `Appendix_A_Prompt_Log.md` trong ZIP; ghi rõ tên từng thành phần để người chấm tìm được, và giữ câu công bố theo mẫu.
3. Điền và ký `[AI-03] AI Disclosure Form` cùng `[AI-05] Privacy & Responsible Use Checklist`. `[AI-04] Reflective Statement` chỉ được nêu cho **Major Projects**, không phải thành phần bắt buộc riêng của HW01.

## 7. Sắp xếp report và tự chấm

Report chính phải là **PDF**. Một bố cục dễ kiểm tra:

1. Thông tin bài và thiết bị.
2. Requirement 1: 10 tin, ảnh, AI Impact Analysis, tổng kết AI thay thế/hỗ trợ/không thể thay thế.
3. Requirement 2: 20 lỗi và 20 chỗ AI sai/thiên kiến đã kiểm chứng.
4. Requirement 3: thiết bị, ảnh, cách thiết kế 15 case, ba edge case, kết quả thực thi, link video, link Issues và tổng kết lỗi.
5. Mindmap và ba chỗ sai đã sửa.
6. AI Critique 200–300 từ.
7. Mandatory Disclosure **trước phụ lục**.
8. Phụ lục: AI-02 Audit Report; các biểu mẫu AI-03/AI-05 đã ký và bằng chứng liên quan (hoặc đính kèm thành file riêng nhưng phải có đủ trong ZIP).
9. **Mục Self-Assessment ở cuối report** theo rubric 100 điểm; dùng các dòng 40, 20, 25, 8, 4, 3 và ghi điểm tự chấm cho từng dòng.

## 8. Đóng gói và nộp

Đặt tên ZIP **`StudentID_HW01_AI_<grade>.zip`**, trong đó `<grade>` là **3 chữ số từ `000` đến `100`**; ví dụ `2112345_HW01_AI_090.zip`. Kiểm tra ZIP có đủ:

- [X] Report PDF với **AI Audit Report, AI Critique, Mandatory Disclosure, Self-Assessment**.
- [X] Full prompt log `.md` hoặc `.txt` với timestamps.
- [X] Excel gồm **Test Cases / Checklist / Test Summary Report**.
- [X] **10 ảnh chụp tin tuyển dụng** thấy tên tài khoản và ngày, cùng URL tương ứng trong report.
- [X] Ảnh JPG **thiết bị + thẻ sinh viên cùng khung hình**.
- [X] Mindmap QA/QC/ISTQB dạng **PNG hoặc Markdown**, cùng ba lỗi đã phân tích.
- [X] Ảnh hội thoại AI chứng minh **3 edge case bị bỏ sót**.
- [X] **Ít nhất 5 link video YouTube Unlisted**, mỗi video tối đa 60 giây, có giọng bạn.
- [X] GitHub Issues ghi các lỗi thật tìm được và **ảnh trang Issues có GitHub username**.
- [X] `[AI-02]` đã điền đủ 5 phần; `[AI-03]` và `[AI-05]` đã ký; xác nhận `[AI-06]` đã ký từ Tuần 1.

Nộp **report/ZIP trên Moodle theo link của môn học** và cung cấp **link GitHub repo chứa artifacts**. Xem deadline trực tiếp trên Moodle; đề ghi **không chấp nhận nộp muộn**.

## 9. Chuẩn bị vấn đáp

Ngẫu nhiên **30% sinh viên** có thể được mời vấn đáp **5–7 phút trong tuần sau deadline**. Chuẩn bị chạy lại một test case/tình huống, giải thích vì sao chọn input đó, và nêu một lỗi AI bạn đã sửa. Theo đề, không trả lời được **từ 2 câu trở lên** thì điểm HW bị nhân **0,5**.
