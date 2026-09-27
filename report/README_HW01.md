# HW01 main report

- `HW01_Main_Report.pdf`: **bản xem chính**, biên dịch từ `main.tex` bằng Tectonic; 193 trang, gồm phần report, phụ lục AI-02 và toàn văn output của 25 artifact.
- `main.tex` và `content/title.tex`: nguồn LaTeX dùng đúng bìa đã chuẩn bị.
- `content/hw01_report.tex`: nội dung report LaTeX từ toàn bộ hồ sơ bài làm.
- `AI-02_Audit_Appendix.pdf`: biểu mẫu AI-02 được ghép vào cuối PDF chính.
- `build_latex.sh`: tái tạo dữ liệu report, chuyển sang LaTeX và biên dịch PDF. Tectonic và Pandoc đã được tải vào `~/.local/bin`.

Chạy từ thư mục gốc:

```sh
report/build_latex.sh
```

Mục 3.4 chứa ảnh GitHub Issues của TC05; mục 3.5 chứa ảnh hội thoại gốc và giải thích TC13–TC15. Mười ảnh tuyển dụng có chú thích theo tên tin. Các link prompt log trong phần Requirement 2 trỏ tới `Appendix_A_Prompt_Log.md` cùng thư mục với PDF, cả trong `report/` và thư mục nộp `23120190_HW01_AI_100/`. Bảng tự chấm ghi **100/100** theo yêu cầu người nộp. Biểu mẫu AI-02 vẫn cần rà verdict trước khi nộp.
