# Ba tình huống biên bổ sung cho Senko L1638

## Cơ sở đối chiếu

- Hội thoại gốc: mục **01:29 27/09/2026 — OpenCode / Big Pickle** trong [Appendix A](../../Appendix_A_Prompt_Log.md). Ảnh [2.png](../02_AI_Test_Case_Output_Screenshots/2.png) liệt kê đủ TC01–TC12; ảnh [3.png](../02_AI_Test_Case_Output_Screenshots/3.png), [4.png](../02_AI_Test_Case_Output_Screenshots/4.png) và [5.png](../02_AI_Test_Case_Output_Screenshots/5.png) thể hiện nội dung các case. Không có TC13–TC15 trong output đó.

## TC13 — Độ cao thấp nhất và cao nhất của thân quạt

- **Objective:** Kiểm tra chốt/khớp chỉnh cao giữ chắc thân quạt ở hai giới hạn cơ học; phát hiện lỗi chỉ xuất hiện khi ống nâng kéo hết hành trình hoặc hạ hết cỡ.
- **Input:** Quạt đã tắt, rút phích cắm; mặt sàn phẳng, chắc; thước đo nếu có. Xác nhận chiếc quạt có bộ phận chỉnh cao và xác định giới hạn theo hướng dẫn/điểm chặn thực tế; không ép quá điểm chặn.
- **Steps:** (1) Rút phích cắm, chờ cánh dừng hẳn. (2) Chỉnh về vị trí thấp nhất theo cơ cấu sẵn có; khóa chốt như cách dùng thông thường, quan sát có trượt xuống hoặc lỏng không. (3) Chỉnh tới vị trí cao nhất cho phép, khóa chốt; quan sát và thử lay **nhẹ thân quạt từ bên ngoài** để kiểm tra chốt giữ. (4) Nếu hai vị trí đều cố định chắc, đặt quạt trên sàn phẳng, đứng cách xa cánh/lồng, bật mức gió thấp trong 30 giây ở mỗi vị trí; dừng ngay nếu thân quạt trượt hoặc nghiêng bất thường. (5) Ghi chiều cao thực đo, tình trạng chốt và chuyển động ở từng đầu mút.
- **Expected:** Ở cả hai đầu mút, chốt giữ được chiều cao đã chọn; thân không tự tụt, nghiêng hoặc lắc bất thường khi chạy mức thấp; không cần dùng lực ép để đạt đầu mút. Không dùng khoảng 77–95 cm trên website làm ngưỡng Pass/Fail trước khi xác nhận cách đo của nhà sản xuất và chiếc quạt thực tế.
- **Actual:** Chưa thực hiện.
- **Verdict:** Not Run.
- **Vì sao không có trong 12 case:** TC07 quan sát rung ở tốc độ cao trên nền phẳng, nhưng không thay đổi **chiều cao đến hai giới hạn** hoặc thử chốt khóa. Output Big Pickle cũng không hỏi có bộ phận chỉnh cao hay không, nên bỏ trống một điều kiện biên cơ học của model.

## TC14 — Mất rồi có điện trở lại khi đang chọn tốc độ cao

- **Objective:** Quan sát ứng xử tại ranh giới cấp điện/mất điện, nơi quạt có thể khởi động lại bất ngờ hoặc không hoạt động sau khi điện trở lại.
- **Input:** Ổ cắm có công tắc hoặc ổ nối dài **có công tắc, còn nguyên vẹn, đúng định mức**; sàn phẳng; dây nguồn không căng; người và vật ở ngoài vùng quét của quạt. Nếu không có công tắc cấp điện phù hợp thì **chưa thực hiện**, không giật/rút phích cắm đang tải để giả lập mất điện.
- **Steps:** (1) Kiểm tra dây, phích và công tắc khi chưa cấp điện. (2) Bật quạt ở mức cao nhất, giữ tay và đồ vật xa lồng. (3) Dùng công tắc ngoài ngắt điện, xác nhận cánh dừng hẳn. (4) Sau ít nhất 30 giây, đứng ngoài tầm quạt và cấp điện trở lại bằng chính công tắc đó. (5) Ghi quạt có tự chạy lại hay không, trạng thái tốc độ và có âm thanh/mùi/tia lửa bất thường không. (6) Tắt quạt bằng nút OFF của quạt sau khi quan sát.
- **Expected:** Khi mất điện, cánh giảm tốc rồi dừng; khi điện trở lại không có khói, mùi khét, tiếng bất thường hoặc sự cố của công tắc/ổ. **Việc quạt tự khởi động lại hay chờ thao tác chưa có tiêu chí hãng được kiểm chứng:** ghi nhận thực tế, đối chiếu hướng dẫn sử dụng rồi mới đánh giá hành vi này; không tự kết luận tự khởi động là lỗi.
- **Actual:** Chưa thực hiện.
- **Verdict:** Not Run.
- **Vì sao không có trong 12 case:** TC01/TC02 kiểm tra khởi động bằng nút điều khiển khi nguồn vẫn có; TC11 chỉ kiểm tra tình trạng dây/phích. Không case nào thử **chuyển trạng thái nguồn cấp** khi quạt đang chạy.

## TC15 — Tắt từ tốc độ cao khi cơ cấu chuyển hướng đang hoạt động

- **Objective:** Kiểm tra lệnh OFF ở trạng thái kết hợp hai chức năng, đặc biệt khi đầu quạt đang gần điểm đổi chiều; phát hiện cơ cấu còn chạy, kẹt hoặc phát tiếng va sau khi tắt.
- **Input:** Chiếc quạt có chức năng chuyển hướng cơ đã được xác nhận; sàn phẳng, không có vật cản gần đầu quạt; xác định nút OFF từ trước. Nếu không có chuyển hướng, thay TC15 bằng case khác và giải thích trong bộ 15 case cuối.
- **Steps:** (1) Đặt quạt ở tốc độ cao nhất và bật chuyển hướng, giữ dây nguồn gọn, không căng. (2) Quan sát một vòng chuyển hướng đủ hai biên. (3) Khi đầu quạt gần một biên, nhấn OFF một lần; không chạm vào cánh hoặc cơ cấu chuyển hướng. (4) Quan sát từ ngoài lồng đến khi cánh dừng; ghi xem đầu quạt còn chuyển hướng, có tiếng va/kẹt, mùi bất thường hoặc tự chạy lại không. (5) Lặp lại một lần ở biên đối diện sau khi máy dừng hẳn.
- **Expected:** Sau lệnh OFF, cánh giảm tốc rồi dừng; cơ cấu chuyển hướng cũng ngừng sau khi truyền động dừng; không có tiếng va/kẹt, mùi bất thường hay tự khởi động lại. Không áp đặt thời gian dừng cụ thể nếu hãng không công bố.
- **Actual:** Chưa thực hiện.
- **Verdict:** Not Run.
- **Vì sao không có trong 12 case:** TC04 kiểm tra phản hồi nút riêng lẻ, TC05 kiểm tra chuyển hướng khi đang chạy, còn TC07 kiểm tra tốc độ cao; không case nào thử **OFF tại hai điểm đổi chiều trong lúc vừa chạy tốc độ cao vừa chuyển hướng**. Đây là điều kiện chuyển trạng thái và tương tác chức năng.

## Giới hạn bằng chứng và phần phải hoàn tất

1. Ảnh hội thoại gốc [1.png](../02_AI_Test_Case_Output_Screenshots/1.png)–[7.png](../02_AI_Test_Case_Output_Screenshots/7.png) đã có. Ảnh **2.png** là bằng chứng gọn nhất cho danh sách chỉ có TC01–TC12. Nên tự chụp thêm một ảnh đối chiếu nguyên màn hình nếu giảng viên yêu cầu chỉ rõ từng case vắng mặt; không chỉnh sửa ảnh gốc để tạo bằng chứng.
2. Kiểm tra model, tính năng chỉnh cao/chuyển hướng, năm trên tem và serial của **chiếc quạt thực tế**. Chỉ báo serial thật với **bốn ký tự giữa được che**; chưa có serial thì ghi “chưa xác định”, không tự đặt.
3. Điền Actual/Verdict sau khi thử thật; quay ít nhất 5 video, mỗi video tối đa 60 giây và có giọng của chính bạn. Chỉ tạo GitHub Issue cho lỗi đã quan sát, kèm video/ảnh thật. Ảnh quạt và thẻ sinh viên phải cùng một khung hình do bạn tự chụp.
4. Vì ba case này cũng có hỗ trợ AI, phần AI Audit phải ghi một artifact riêng cho lượt Codex này, kèm prompt/output nguyên văn nếu đưa vào bài nộp; phần Disclosure không được ghi ba case là “viết hoàn toàn bởi tôi”.
5. Để kiểm tra chặt hơn yêu cầu “AI Tool could NOT find”, hãy yêu cầu **chính Big Pickle** tự tìm thêm các tình huống biên cho L1638 mà không tiết lộ trước TC13–TC15, rồi lưu prompt/output và ảnh màn hình thật. Nếu AI nêu được case nào trong ba case này, case đó không còn là bằng chứng AI đã bỏ sót sau khi được hỏi sâu; cần chọn case khác và cập nhật cả phân tích lẫn workbook. Chỉ riêng lượt trả lời 12 case hiện tại chưa đủ để khẳng định AI không thể tìm ra chúng.
