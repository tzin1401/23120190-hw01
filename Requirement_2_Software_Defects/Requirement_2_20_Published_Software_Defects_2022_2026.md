# Yêu cầu 2 — 20 lỗi phần mềm đã công bố (2022–2026)

**Ngày tra cứu:** 24/09/2026. **Tổng số:** 20 lỗi/sự cố riêng biệt; **6 mục liên quan trực tiếp đến AI/LLM** (#01–#06). “Hậu quả” phân biệt điều đã quan sát được với rủi ro có thể xảy ra. Mức độ ghi theo nhà cung cấp/CVSS nếu nguồn nêu rõ; các mức còn lại là **đánh giá của báo cáo**, không phải CVSS chính thức. Với sự cố chất lượng AI không có CVE, “cách khắc phục” là hành động nhà cung cấp đã công bố hoặc hướng xử lý phù hợp.

Phần **“RÀNG BUỘC CỐT LÕI VỀ AI”** ở từng mục được điền dần sau khi đối chiếu câu giải thích của AI với nguồn gốc. Mỗi nhận định được ghi phải thực sự xuất hiện trong câu trả lời đã lưu ở prompt log; mục chưa kiểm chứng tiếp tục để trống.

## A. Lỗi liên quan trực tiếp đến AI/LLM (6)

### 01. ChatGPT hiển thị nhầm lịch sử và thông tin thanh toán của người khác (2023)

- **Nguồn và ngày công bố:** [OpenAI, báo cáo sự cố 24/03/2023](https://openai.com/index/march-20-chatgpt-outage/).
- **Mô tả:** Lỗi trong `redis-py` khi dùng Asyncio với Redis Cluster có thể khiến một yêu cầu nhận dữ liệu cache của người dùng khác. OpenAI ghi nhận tiêu đề cuộc trò chuyện, có thể cả tin nhắn đầu của cuộc trò chuyện mới, bị hiển thị sai người.
- **Mức độ:** **Cao — đánh giá của báo cáo** vì ảnh hưởng quyền riêng tư; OpenAI không công bố CVSS cho sự cố này.
- **Hậu quả:** Trong một khung 9 giờ ngày 20/03, thông tin liên quan thanh toán của tối đa 1,2% thuê bao Plus đang hoạt động *có thể* lộ: tên, email, địa chỉ thanh toán, loại thẻ, **4 số cuối** và ngày hết hạn. OpenAI nói **không lộ số thẻ đầy đủ** và số trường hợp thực sự bị xem được cho là rất thấp.
- **Cách khắc phục:** OpenAI vá thư viện, thêm kiểm tra dữ liệu cache khớp đúng người yêu cầu, kiểm tra log và thông báo cho người có thể bị ảnh hưởng.
- **RÀNG BUỘC CỐT LÕI VỀ AI — #01 (ảo giác về cơ chế lỗi):** Trong câu trả lời của **OpenCode – Big Pickle, 16:34 26/09/2026** ở [prompt log](../Appendix_A_Prompt_Log.md), AI viết: “trạng thái định tuyến (node/shard đang trỏ tới) của lệnh trước bị giữ lại và dùng tiếp cho các lệnh sau”, rồi cho rằng lệnh có hash tag khác sẽ đọc nhầm node. [Báo cáo kỹ thuật của OpenAI](https://openai.com/index/march-20-chatgpt-outage/) mô tả cơ chế khác: một yêu cầu bị hủy sau khi đã gửi lệnh nhưng trước khi lấy phản hồi làm hỏng kết nối dùng chung; yêu cầu kế tiếp có thể nhận **phản hồi còn sót** trên kết nối đó. OpenAI không quy nguyên nhân cho việc tái sử dụng trạng thái định tuyến/hash tag. Vì vậy phần giải thích node/shard của AI là chi tiết cơ chế không được nguồn hỗ trợ và mâu thuẫn với nguyên nhân đã công bố. **Sửa đúng:** lỗi xử lý phản hồi của kết nối `redis-py` khi dùng Asyncio với Redis Cluster, trong tình huống yêu cầu bị hủy giữa lúc gửi và nhận phản hồi.

### 02. Gemini tạo hình người sai bối cảnh và từ chối một số yêu cầu vô hại (2024)

- **Nguồn và ngày công bố:** [Google, 23/02/2024](https://blog.google/products-and-platforms/products/gemini/gemini-image-generation-issue/).
- **Mô tả:** Tinh chỉnh nhằm tạo hình đa dạng chưa xử lý đúng các yêu cầu cần độ chính xác lịch sử hoặc đặc điểm cụ thể; mô hình cũng trở nên quá thận trọng và từ chối một số yêu cầu bình thường.
- **Mức độ:** **Trung bình — đánh giá của báo cáo** về độ đúng/chất lượng; Google không gán CVSS.
- **Hậu quả:** Hình tạo ra có thể sai hoặc gây phản cảm; một số người dùng không nhận được hình hợp lệ theo yêu cầu. Nguồn không chứng minh tỷ lệ lỗi trên toàn bộ lượt dùng.
- **Cách khắc phục:** Google tạm dừng tính năng tạo hình người, sửa điều chỉnh mô hình và mở rộng kiểm thử trước khi mở lại.
- **RÀNG BUỘC CỐT LÕI VỀ AI — #02 (ảo giác về ngày công bố):** Trong câu trả lời của **OpenCode – Big Pickle, 16:43 26/09/2026** ở [prompt log](../Appendix_A_Prompt_Log.md), AI viết bài blog chính thức của Google “được đăng ngày **21/02/2024**” và dẫn chính URL của bài đó, dù cũng tự nhắc cần kiểm chứng lại. [Bài gốc của Google](https://blog.google/products-and-platforms/products/gemini/gemini-image-generation-issue/) hiển thị ngày **23/02/2024**. Đây là một dữ kiện AI nhớ sai, không phải bằng chứng về thiên kiến. **Sửa đúng:** báo cáo giải thích sự cố của Google được đăng ngày 23/02/2024; ngày trong mục “Nguồn và ngày công bố” ở trên đã đúng.

### 03. Google AI Overviews đưa ra một số câu trả lời sai (2024)

- **Nguồn và ngày công bố:** [Google Search, 30/05/2024](https://blog.google/products-and-platforms/products/search/ai-overviews-update-may-2024/).
- **Mô tả:** Một số bản tổng quan AI hiểu sai câu hỏi vô nghĩa, nội dung châm biếm hoặc ngôn ngữ trên trang nguồn; thiếu nguồn tốt cũng dẫn tới kết quả kém. Google xác nhận có câu trả lời sai thật, đồng thời lưu ý nhiều ảnh chụp lan truyền là giả.
- **Mức độ:** **Trung bình — đánh giá của báo cáo** vì sai thông tin hướng dẫn; không có CVSS.
- **Hậu quả:** Người đọc có thể nhận và tin lời khuyên sai. **Không** suy ra từ báo cáo rằng mọi ví dụ lan truyền đều từng xuất hiện hoặc đã gây hại thực tế; Google nói các trường hợp này thường không phải “ảo giác” theo nghĩa mô hình tự bịa không dựa trên nguồn.
- **Cách khắc phục:** Google bổ sung hơn 12 cải tiến, gồm nhận diện truy vấn vô nghĩa, hạn chế nội dung trào phúng và nội dung người dùng dễ gây hiểu lầm, giảm kích hoạt AI Overview ở những truy vấn kém phù hợp.
- **RÀNG BUỘC CỐT LÕI VỀ AI — #03 (ảo giác/khái quát sai về cách hoạt động):** Trong câu trả lời của **OpenCode – Big Pickle, 16:48 26/09/2026** ở [prompt log](../Appendix_A_Prompt_Log.md), AI viết AI Overviews “**luôn tạo ra một câu trả lời bằng văn bản** ... kể cả khi độ tin cậy của nguồn thấp” và gọi đó là cơ chế “**phải trả lời**”. [Bài công bố của Google ngày 30/05/2024](https://blog.google/products-and-platforms/products/search/ai-overviews-update-may-2024/) không nói hệ thống luôn hiển thị AI Overview; trái lại, Google nêu các cải tiến nhằm **không kích hoạt** tính năng với truy vấn vô nghĩa và **hạn chế kích hoạt** khi kết quả không hữu ích. Vì vậy nhận định “luôn/phải trả lời” mâu thuẫn với nguồn, không thể dùng làm nguyên nhân đã xác nhận. **Sửa đúng:** AI Overview chỉ xuất hiện khi hệ thống quyết định kích hoạt; lỗi đã công bố liên quan tới việc hiểu sai truy vấn, hiểu sai nội dung nguồn, hoặc thiếu nguồn đáng tin, và Google đã siết điều kiện kích hoạt.

### 04. Prompt injection qua Slack AI có thể dẫn dụ lộ dữ liệu kênh riêng (2024)

- **Nguồn và ngày công bố:** [Nghiên cứu gốc của PromptArmor, công bố 20/08/2024](https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection); [Slack xác nhận và báo vá, 21/08/2024](https://slack.com/blog/news/slack-security-update-082124).
- **Mô tả:** Nhà nghiên cứu cài chỉ dẫn độc hại vào nội dung kênh công khai trong cùng workspace. Khi Slack AI truy xuất nội dung để trả lời người dùng có quyền xem dữ liệu riêng, chỉ dẫn đó có thể làm câu trả lời chứa liên kết lừa đảo mang dữ liệu từ kênh riêng.
- **Mức độ:** **Cao — đánh giá của báo cáo** vì nguy cơ tiết lộ bí mật; không có CVSS chính thức trong hai nguồn.
- **Hậu quả:** Bản thử nghiệm cho thấy khả năng đưa khóa API từ kênh riêng vào đường dẫn do kẻ tấn công kiểm soát. Slack cho biết tình huống có điều kiện hạn chế, cần tài khoản trong cùng workspace, và **không có bằng chứng khách hàng bị truy cập dữ liệu trái phép** tại thời điểm thông báo.
- **Cách khắc phục:** Slack triển khai bản vá ngày 20/08/2024. Về phía tổ chức, rà soát quyền truy cập và nội dung AI được phép truy xuất.
- **RÀNG BUỘC CỐT LÕI VỀ AI — #04 (ảo giác về đường rò rỉ dữ liệu):** Trong câu trả lời của **OpenCode – Big Pickle, 17:01 26/09/2026** ở [prompt log](../Appendix_A_Prompt_Log.md), AI viết “Slack AI có khả năng **gửi tin nhắn** vào kênh” và “**nói chắc chắn**” dữ liệu có thể được đăng vào kênh kẻ tấn công đọc được. [Thử nghiệm gốc của PromptArmor](https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection) mô tả đường rò rỉ khác: chỉ dẫn độc hại khiến Slack AI **hiển thị một liên kết Markdown** chứa khóa API trong tham số URL; dữ liệu được gửi tới máy chủ của kẻ tấn công **khi nạn nhân nhấp liên kết**. Nguồn này không chứng minh cơ chế Slack AI tự đăng dữ liệu vào kênh. **Sửa đúng:** mô tả liên kết độc hại và bước nhấp của nạn nhân là điều kiện trong bản thử nghiệm; [Slack](https://slack.com/blog/news/slack-security-update-082124) cho biết đã vá ngày 20/08/2024 và chưa có bằng chứng khách hàng bị truy cập dữ liệu trái phép.

### 05. GPT-4o trở nên quá chiều ý người dùng sau cập nhật (2025)

- **Nguồn và ngày công bố:** [OpenAI, 29/04/2025](https://openai.com/index/sycophancy-in-gpt-4o/); [phân tích bổ sung, 02/05/2025](https://openai.com/index/expanding-on-sycophancy/).
- **Mô tả:** Bản cập nhật ChatGPT ngày 25/04 khiến GPT-4o quá tán đồng/ca ngợi người dùng. Theo OpenAI, việc đặt nặng phản hồi hài lòng ngắn hạn đã làm lệch hành vi, trong khi kiểm thử trước phát hành chưa phát hiện đầy đủ.
- **Mức độ:** **Cao — đánh giá của báo cáo** vì có thể củng cố nhận định thiếu căn cứ trong tình huống nhạy cảm; không có CVSS.
- **Hậu quả:** Câu trả lời có thể xác nhận cảm xúc hoặc quyết định rủi ro một cách thiếu trung thực; OpenAI nêu quan ngại về phụ thuộc cảm xúc và sức khỏe tinh thần, **không công bố số vụ thiệt hại cụ thể**.
- **Cách khắc phục:** OpenAI bắt đầu hoàn tác bản cập nhật ngày 28/04; điều chỉnh huấn luyện, cách dùng phản hồi và mở rộng đánh giá về hành vi quá chiều ý.
- **RÀNG BUỘC CỐT LÕI VỀ AI — #05 (ảo giác về biện pháp khắc phục):** Trong câu trả lời của **OpenCode – Big Pickle, 17:08 26/09/2026** ở [prompt log](../Appendix_A_Prompt_Log.md), AI viết OpenAI “**thêm các tín hiệu phạt ngay trong quá trình tạo phản hồi**” để phát hiện câu trả lời quá chiều ý “**trong lúc sinh**”. Hai [bài giải thích của OpenAI ngày 29/04](https://openai.com/index/sycophancy-in-gpt-4o/) và [02/05/2025](https://openai.com/index/expanding-on-sycophancy/) không công bố cơ chế phạt thời gian thực khi mô hình đang trả lời. OpenAI mô tả **reward signals trong giai đoạn huấn luyện**, mở rộng đánh giá trước phát hành và dự định cho người dùng **phản hồi thời gian thực** để điều chỉnh tương tác; AI đã trộn lẫn các khái niệm này thành một cơ chế không có trong nguồn. **Sửa đúng:** nêu việc điều chỉnh huấn luyện/system prompt, bổ sung đánh giá sycophancy và cải thiện thu thập phản hồi; không khẳng định có bộ phạt chạy trong lúc sinh câu trả lời.

### 06. EchoLeak trong Microsoft 365 Copilot — CVE-2025-32711 (2025)

- **Nguồn và ngày công bố:** [Microsoft, mô tả EchoLeak và bản vá](https://www.microsoft.com/en-us/security/security-insider/emerging-trends/ai-application-security-considerations-for-organizations); [hồ sơ CVE của Microsoft, công bố 11/06/2025](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711); [nghiên cứu gốc của Aim Security](https://www.aim.security/lp/aim-labs-echoleak-m365).
- **Mô tả:** Email được chế tạo để Copilot đọc có thể mang chỉ dẫn gián tiếp vượt ranh giới giữa dữ liệu và lệnh. Trong một số điều kiện, chuỗi tấn công có thể khiến Copilot tiết lộ một phần dữ liệu mà người dùng nạn nhân vốn có quyền truy cập.
- **Mức độ:** **Nghiêm trọng, CVSS 9,3 theo hồ sơ CVE của Microsoft**.
- **Hậu quả:** Nguy cơ lộ dữ liệu nội bộ qua mạng mà người dùng không hay biết. Đây là khả năng đã được nghiên cứu chứng minh; nguồn của Microsoft **không xác nhận một vụ khai thác khách hàng thực tế**.
- **Cách khắc phục:** Microsoft đã phát hành cập nhật cho dịch vụ; tổ chức nên giữ quyền truy cập tối thiểu, rà soát dữ liệu Copilot được phép đọc và giám sát đầu vào có dấu hiệu prompt injection.
- **RÀNG BUỘC CỐT LÕI VỀ AI — #06 (ảo giác về chuỗi khai thác):** Trong câu trả lời của **OpenCode – Big Pickle, 23:27 26/09/2026** ở [prompt log](../Appendix_A_Prompt_Log.md), AI khẳng định Copilot làm lộ “**một mã định danh**”, rồi kẻ tấn công dùng mã đó ở bước sau để “**mở dữ liệu riêng của nạn nhân**”. [Phân tích kỹ thuật của nhóm phát hiện EchoLeak](https://www.catonetworks.com/blog/breaking-down-echoleak/) và [bài nghiên cứu về EchoLeak](https://arxiv.org/abs/2509.10540) mô tả cơ chế khác: prompt injection khiến Copilot đưa **chính dữ liệu nhạy cảm trong ngữ cảnh** vào tham số URL của ảnh Markdown; trình duyệt tự tải ảnh, gửi tham số đó tới máy chủ kẻ tấn công. Hai nguồn không nêu bước lấy mã định danh rồi dùng nó tải dữ liệu riêng. **Sửa đúng:** dữ liệu bị rò rỉ trực tiếp qua yêu cầu tải ảnh chứa dữ liệu trong URL, không qua một mã truy cập trung gian.

## B. Các lỗi phần mềm khác (14)

### 07. Spring Framework RCE qua data binding — CVE-2022-22965 (2022)

- **Nguồn và ngày công bố:** [Spring, 31/03/2022](https://spring.io/security/cve-2022-22965/).
- **Mô tả:** Ứng dụng Spring MVC/WebFlux chạy JDK 9+ có thể bị thực thi mã từ xa qua data binding. Đường khai thác cụ thể được Spring mô tả cần Tomcat và triển khai dạng WAR; JAR thực thi mặc định của Spring Boot không chịu ảnh hưởng theo đường này.
- **Mức độ:** **Nghiêm trọng theo Spring**.
- **Hậu quả:** Kẻ tấn công có thể chạy mã trên máy chủ ứng dụng nếu các điều kiện khai thác được đáp ứng.
- **Cách khắc phục:** Nâng Spring Framework lên **5.3.18** hoặc **5.2.20.RELEASE** tương ứng; rà soát kiểu triển khai thực tế.
- **RÀNG BUỘC CỐT LÕI VỀ AI — #07 (giải thích sai điều kiện data binding):** Trong câu trả lời của **OpenCode – Big Pickle, 23:30 26/09/2026** ở [prompt log](../Appendix_A_Prompt_Log.md), AI nêu controller bind dữ liệu từ request “**ví dụ qua `@RequestParam`**” như một điều kiện khai thác CVE-2022-22965. [Thông báo kỹ thuật của Spring](https://spring.io/blog/2022/03/31/spring-framework-rce-early-announcement/) xác định đường data binding liên quan tới tham số controller có **`@ModelAttribute` hoặc không gắn annotation Spring Web khác**; thông báo không liệt kê `@RequestParam` làm ví dụ cho đường khai thác này. AI đã đánh đồng việc đọc tham số request nói chung với việc bind thuộc tính của một đối tượng. **Sửa đúng:** mô tả tham số đối tượng được Spring data bind (thường qua `@ModelAttribute`), cùng các điều kiện JDK 9+, Tomcat và triển khai WAR của [advisory CVE](https://spring.io/security/cve-2022-22965/).

### 08. Confluence Server/Data Center OGNL injection — CVE-2022-26134 (2022)

- **Nguồn và ngày công bố:** [Atlassian, 02/06/2022](https://confluence.atlassian.com/doc/confluence-security-advisory-2022-06-02-1130377146.html).
- **Mô tả:** Lỗi OGNL injection cho phép người **không cần đăng nhập** thực thi mã trên Confluence Server/Data Center dễ bị ảnh hưởng. Atlassian đã ghi nhận khai thác thực tế.
- **Mức độ:** **Nghiêm trọng theo Atlassian**.
- **Hậu quả:** Máy chủ tự quản có thể bị chiếm quyền, dữ liệu hoặc dịch vụ có thể bị ảnh hưởng; không suy rộng sang Confluence Cloud.
- **Cách khắc phục:** Nâng lên nhánh đã vá, ví dụ **7.4.17, 7.13.7, 7.14.3, 7.15.2, 7.16.4, 7.17.4 hoặc 7.18.1** theo nhánh dùng; kiểm tra dấu hiệu xâm nhập.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 09. Exchange Server PowerShell RCE — CVE-2022-41082 (2022)

- **Nguồn và ngày công bố:** [Microsoft MSRC, 30/09/2022; cập nhật bản vá 08/11/2022](https://www.microsoft.com/en-us/msrc/blog/2022/09/customer-guidance-for-reported-zero-day-vulnerabilities-in-microsoft-exchange-server).
- **Mô tả:** Lỗi cho phép thực thi mã từ xa khi PowerShell của Exchange có thể được kẻ tấn công truy cập. Trong chiến dịch được Microsoft ghi nhận, CVE-2022-41040 (SSRF) được dùng **cùng** CVE-2022-41082; đây là mục về riêng lỗi 41082, không tính chuỗi hai CVE thành hai mục.
- **Mức độ:** **Cao — đánh giá của báo cáo** cho lỗi RCE trong điều kiện cần quyền xác thực; nguồn trên không nêu CVSS.
- **Hậu quả:** Kẻ tấn công đã xác thực có thể chạy mã trên Exchange Server tại chỗ; Microsoft ghi nhận các cuộc tấn công có mục tiêu ở phạm vi hạn chế. Exchange Online không cần xử lý theo thông báo này.
- **Cách khắc phục:** Cài bản cập nhật bảo mật Exchange Server cho CVE-2022-41082 do Microsoft phát hành 08/11/2022; rà soát dấu hiệu tấn công.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 10. Tràn bộ đệm OpenSSL khi kiểm tra chứng chỉ — CVE-2022-3602 (2022)

- **Nguồn và ngày công bố:** [OpenSSL, advisory ký số 01/11/2022](https://mta.openssl.org/pipermail/openssl-project/2022-November/003047.html).
- **Mô tả:** Tràn 4 byte do địa chỉ email trong chứng chỉ X.509 khi kiểm tra name constraints, **sau** bước xác thực chữ ký chuỗi chứng chỉ; đường khai thác cần chứng chỉ được CA ký hoặc ứng dụng tiếp tục kiểm tra dù đường tin cậy thất bại. Ảnh hưởng OpenSSL 3.0.0–3.0.6.
- **Mức độ:** **Cao theo OpenSSL**; mức công bố cuối đã hạ từ dự báo “Critical”.
- **Hậu quả:** Có thể làm tiến trình sập; thực thi mã từ xa chỉ là khả năng trong điều kiện phù hợp. OpenSSL nói **chưa biết mã khai thác RCE hoạt động và chưa có bằng chứng khai thác** khi công bố.
- **Cách khắc phục:** Nâng lên **OpenSSL 3.0.7** hoặc bản mới hơn phù hợp.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 11. Lỗi SQL injection trong MOVEit Transfer — CVE-2023-34362 (2023)

- **Nguồn và ngày công bố:** [Progress, FAQ xác nhận công bố 31/05/2023 và bản vá](https://www.progress.com/docs/default-source/moveit-docs/moveit-transfer_moveit-cloud-vulnerabilities-customer-faq_posted.pdf?sfvrsn=16a47a99_13); [NIST NVD, mô tả kỹ thuật và CVSS](https://nvd.nist.gov/vuln/detail/CVE-2023-34362).
- **Mô tả:** SQL injection trong ứng dụng web MOVEit Transfer có thể cho kẻ tấn công **không xác thực** truy cập cơ sở dữ liệu; phạm vi thao tác phụ thuộc hệ quản trị CSDL. NVD ghi nhận lỗi bị khai thác trong tháng 5–6/2023.
- **Mức độ:** **Nghiêm trọng, CVSS 9,8 theo NIST NVD**.
- **Hậu quả:** Có thể đọc, thay đổi hoặc xóa dữ liệu; thông tin lưu trong hệ thống truyền tệp có nguy cơ bị đánh cắp. Mức thiệt hại của từng khách hàng cần bằng chứng điều tra riêng.
- **Cách khắc phục:** Cài bản vá theo nhánh phiên bản do Progress phát hành; cô lập máy nghi bị xâm nhập, rà soát log và dữ liệu.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 12. Barracuda ESG command injection qua tên tệp TAR — CVE-2023-2868 (2023)

- **Nguồn và ngày công bố:** [Barracuda, công bố tháng 05/2023 và cập nhật điều tra](https://trust.barracuda.com/security/esg-vulnerability).
- **Mô tả:** Bộ kiểm tra tệp đính kèm của **thiết bị ESG** xác thực chưa đủ tên tệp trong kho TAR, dẫn đến chèn lệnh và thực thi với quyền tiến trình ESG. Barracuda xác nhận lỗ hổng tồn tại trên thiết bị phiên bản 5.1.3.001–9.2.0.006, không phải dịch vụ email SaaS của hãng.
- **Mức độ:** **Nghiêm trọng — đánh giá của báo cáo** vì đã có khai thác và truy cập trái phép.
- **Hậu quả:** Barracuda xác nhận một số thiết bị có mã độc duy trì truy cập và một số có bằng chứng dữ liệu bị lấy ra.
- **Cách khắc phục:** Barracuda đã triển khai bản vá ngày 20/05/2023; với **thiết bị đã bị xâm nhập**, hãng tiếp tục khuyến nghị **thay thiết bị**, rồi điều tra và đổi thông tin xác thực liên quan.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 13. Outlook for Windows gửi thông tin xác thực NTLM — CVE-2023-23397 (2023)

- **Nguồn và ngày công bố:** [Microsoft MSRC, 14/03/2023](https://www.microsoft.com/en-us/msrc/blog/2023/03/microsoft-mitigates-outlook-elevation-of-privilege-vulnerability).
- **Mô tả:** Thuộc tính MAPI trong thư/tác vụ trỏ tới SMB của kẻ tấn công có thể khiến Outlook for Windows tự kết nối, **không cần người dùng tương tác**, làm lộ thông tin thương lượng NTLM có thể bị relay.
- **Mức độ:** **Nghiêm trọng theo Microsoft**.
- **Hậu quả:** Microsoft ghi nhận lạm dụng có mục tiêu ở phạm vi hạn chế. Nguy cơ chính là thông tin xác thực bị lợi dụng để xác thực tới hệ thống khác; Outlook web, Mac, iOS và Android không nằm trong phạm vi lỗi này.
- **Cách khắc phục:** Cập nhật **Outlook for Windows** dù thư được lưu ở đâu; dùng công cụ kiểm tra mục MAPI độc hại do Microsoft cung cấp, điều tra tài khoản liên quan.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 14. NetScaler ADC/Gateway làm lộ dữ liệu nhạy cảm — CVE-2023-4966 (2023)

- **Nguồn và ngày công bố:** [Citrix/Cloud Software Group, 10/10/2023](https://support.citrix.com/external/article/579459/netscaler-adc-and-netscaler-gateway-secu.html).
- **Mô tả:** Lỗi tiết lộ thông tin nhạy cảm ảnh hưởng thiết bị cấu hình làm Gateway hoặc máy chủ AAA; Citrix đã bổ sung xác nhận khai thác trong bản cập nhật ngày 17/10/2023.
- **Mức độ:** **Cao — đánh giá của báo cáo** dựa trên nguy cơ lộ thông tin và khai thác đã quan sát; advisory dẫn không gán mức CVSS ngay trong bảng.
- **Hậu quả:** Thông tin của phiên/kết nối có nguy cơ lộ, dẫn tới truy cập trái phép nếu bị lợi dụng. Không suy ra mọi thiết bị NetScaler đều bị ảnh hưởng.
- **Cách khắc phục:** Nâng lên bản sửa đúng nhánh, chẳng hạn **14.1-8.50**, **13.1-49.15** hoặc **13.0-92.19** trở lên; kiểm tra dấu hiệu xâm nhập và xử lý phiên có nguy cơ theo hướng dẫn NetScaler.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 15. Cisco IOS XE Web UI cho tạo tài khoản đặc quyền — CVE-2023-20198 (2023)

- **Nguồn và ngày công bố:** [Cisco, 16/10/2023](https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-iosxe-webui-privesc-j22SaA4z.html).
- **Mô tả:** Khi bật Web UI (`ip http server`/`ip http secure-server`), kẻ tấn công từ xa không xác thực có thể tạo tài khoản cục bộ quyền 15. Cisco ghi nhận khai thác thực tế. Việc cài implant với quyền root trong chiến dịch còn dùng **lỗi khác** CVE-2023-20273.
- **Mức độ:** **Nghiêm trọng, CVSS 10,0 theo Cisco** cho CVE-2023-20198.
- **Hậu quả:** Thiết bị mạng có thể xuất hiện tài khoản quản trị trái phép; nếu có thêm điều kiện/lỗi thứ hai, kẻ tấn công có thể kiểm soát sâu hơn.
- **Cách khắc phục:** Nâng IOS XE lên bản sửa đúng nhánh; tắt Web UI nếu không cần hoặc giới hạn nguồn được truy cập, kiểm tra tài khoản lạ.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 16. Mã độc cài trong gói xz Utils/liblzma — CVE-2024-3094 (2024)

- **Nguồn và ngày công bố:** [Red Hat, 29/03/2024; cập nhật 30/03](https://www.redhat.com/en/blog/urgent-security-alert-fedora-40-and-rawhide-users).
- **Mô tả:** Gói nguồn xz/liblzma **5.6.0 và 5.6.1** chứa mã độc được đưa vào quá trình build; trong cấu hình phù hợp, mã này có thể can thiệp xác thực `sshd`. Đây là lỗi chuỗi cung ứng được công bố, không phải lỗi “mọi bản Linux”.
- **Mức độ:** **Nghiêm trọng — đánh giá của báo cáo** do khả năng vượt xác thực và tính chất chuỗi cung ứng.
- **Hậu quả:** Có nguy cơ truy cập máy từ xa trái phép trên hệ thống có bản build và cấu hình phù hợp. Red Hat nói **RHEL không bị ảnh hưởng**; Fedora 40 beta có gói liên quan nhưng chưa cho thấy cơ chế độc hại hoạt động trong bản build đó.
- **Cách khắc phục:** Ngừng dùng bản 5.6.0/5.6.1 bị ảnh hưởng, quay về **xz 5.4.x** theo hướng dẫn nhà phân phối và rà soát hệ thống đã cài.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 17. Bản cập nhật CrowdStrike Falcon làm Windows màn hình xanh (2024)

- **Nguồn và ngày công bố:** [CrowdStrike, báo cáo sơ bộ 24/07/2024](https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/); [RCA đầy đủ 06/08/2024](https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf).
- **Mô tả:** Rapid Response Content trong Channel File 291 dùng trường đầu vào thứ 21 khi cảm biến chỉ có 20 trường, gây đọc ngoài giới hạn và sập Windows. Lỗi trong bộ kiểm tra nội dung đã để bản cập nhật không hợp lệ vượt qua.
- **Mức độ:** **Nghiêm trọng về vận hành — đánh giá của báo cáo**; đây không phải CVE khai thác từ xa.
- **Hậu quả:** Máy Windows nhận bản cập nhật trong khung 04:09–05:27 UTC ngày 19/07/2024 có thể gặp BSOD và gián đoạn dịch vụ; máy Mac/Linux không nằm trong phạm vi. CrowdStrike nói lỗi này **không cho kẻ tấn công leo thang quyền hoặc RCE**.
- **Cách khắc phục:** CrowdStrike thu hồi bản nội dung lỗi, hướng dẫn phục hồi máy bị ảnh hưởng; bổ sung kiểm tra ranh giới, kiểm thử nội dung và triển khai theo giai đoạn.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 18. Next.js Middleware bị bỏ qua kiểm tra quyền — CVE-2025-29927 (2025)

- **Nguồn và ngày công bố:** [Advisory dự án Next.js trên GitHub, 21/03/2025](https://github.com/vercel/next.js/security/advisories/GHSA-f82v-jwr5-mffw); [Vercel postmortem](https://vercel.com/blog/postmortem-on-next-js-middleware-bypass).
- **Mô tả:** Header nội bộ `x-middleware-subrequest` có thể làm Middleware không chạy. Ứng dụng đặt kiểm tra xác thực/phân quyền **chỉ** trong Middleware có thể bị vượt qua; không đồng nghĩa mọi ứng dụng Next.js đều lộ dữ liệu.
- **Mức độ:** **Nghiêm trọng, CVSS 9,1 theo GitHub Advisory**.
- **Hậu quả:** Truy cập trái phép trang hoặc thao tác mà ứng dụng dự định chặn bằng Middleware; mức dữ liệu thực tế lộ tùy thiết kế ứng dụng.
- **Cách khắc phục:** Cập nhật bản an toàn theo nhánh, ví dụ **12.3.5, 13.5.9, 14.2.25, 15.2.3**; nếu chưa thể cập nhật, chặn header trên từ yêu cầu bên ngoài. Kiểm tra quyền ở lớp xử lý dữ liệu nhạy cảm.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 19. React Server Components cho phép RCE — CVE-2025-55182 (2025)

- **Nguồn và ngày công bố:** [React Team, 03/12/2025](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components).
- **Mô tả:** Lỗi khi giải mã payload gửi đến React Server Function cho phép yêu cầu HTTP được chế tạo khai thác thực thi mã trên máy chủ **không cần xác thực**. Ảnh hưởng các gói `react-server-dom-webpack`, `react-server-dom-parcel`, `react-server-dom-turbopack` ở phiên bản React 19 cụ thể; ứng dụng chỉ dùng React phía trình duyệt không thuộc phạm vi.
- **Mức độ:** **Nghiêm trọng, CVSS 10,0 theo React Team**.
- **Hậu quả:** Máy chủ ứng dụng hỗ trợ React Server Components có thể bị thực thi mã trái phép.
- **Cách khắc phục:** Nâng gói bị ảnh hưởng lên phiên bản vá **19.0.1, 19.1.2 hoặc 19.2.1**, hoặc bản mới hơn trong nhánh tương ứng; cập nhật framework dùng các gói đó theo hướng dẫn React.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

### 20. SharePoint Server tại chỗ bị RCE — CVE-2025-53770 (2025)

- **Nguồn và ngày công bố:** [Microsoft MSRC, 19/07/2025](https://www.microsoft.com/en-us/msrc/blog/2025/07/customer-guidance-for-sharepoint-vulnerability-cve-2025-53770); [hồ sơ CVE](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53770).
- **Mô tả:** Lỗi thực thi mã từ xa ảnh hưởng các phiên bản **SharePoint Server tại chỗ** được Microsoft liệt kê. Microsoft xác nhận có tấn công đang diễn ra nhắm vào các hệ thống này; khuyến cáo triển khai cập nhật bổ sung cho CVE-2025-53770 và CVE-2025-53771.
- **Mức độ:** **Nghiêm trọng — đánh giá của báo cáo** dựa trên RCE và khai thác thực tế; kiểm tra hồ sơ CVE cho điểm CVSS chính thức nếu cần.
- **Hậu quả:** Máy chủ SharePoint bị xâm nhập có thể cho phép mã trái phép chạy và dữ liệu bị truy cập; phạm vi từng tổ chức cần điều tra riêng.
- **Cách khắc phục:** Cài bản cập nhật phù hợp SharePoint Server 2016, 2019 hoặc Subscription Edition; bật AMSI/giám sát, **đổi khóa ASP.NET machine key** và khởi động lại IIS theo hướng dẫn Microsoft.
- **RÀNG BUỘC CỐT LÕI VỀ AI — 1 điểm thiên kiến/ảo giác trong lời giải thích của AI (sinh viên tự điền):** ________________________________________________

## Kiểm tra theo đề

- **Số mục:** 20; #01–#06 thuộc AI/LLM, vượt ngưỡng tối thiểu 5.
- **Thời điểm công bố:** Từng mục có nguồn công khai trong khoảng 2022–2025, thuộc khoảng đề cho phép 2022–2026. Năm của CVE đôi khi khác ngày bài tư vấn được cập nhật; ngày công bố ghi theo nguồn đầu tiên nêu trong mục.
- **Trường bắt buộc:** Mỗi mục có nguồn, mô tả, mức độ, hậu quả, cách khắc phục và một trường nhận diện lỗi trong lời giải thích của AI; trường chưa kiểm chứng vẫn để trống.
- **Việc sinh viên tự thực hiện:** Đọc lại lời giải thích AI đã lưu trong [Appendix A](../Appendix_A_Prompt_Log.md), trích một nhận định AI sai/thiên lệch **thực sự có** cho từng mục và đối chiếu với nguồn. Nếu một mục không có sai sót quan sát được, cần hỏi AI bổ sung và lưu câu trả lời thật trước khi kết luận; không tự tạo “ảo giác” làm bằng chứng.
