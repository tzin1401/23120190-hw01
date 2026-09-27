#!/usr/bin/env python3
"""Build the HW01 review PDF from the evidence in the parent directory.

Chrome renders the report body using the layout of the prepared title page.
LibreOffice renders the filled AI-02 form; pdfunite appends it as Appendix A.
"""

from __future__ import annotations

import html
import re
import subprocess
import urllib.parse
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "HW01_Main_Report.html"
PDF_BODY = HERE / "HW01_Main_Report_Body.pdf"
PDF_AUDIT = HERE / "AI-02_Audit_Appendix.pdf"
PDF_FINAL = HERE / "HW01_HTML_Preview.pdf"
ISTQB = "https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf"


def inline(source: str) -> str:
    s = html.escape(source)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def markdown_fragment(source: str, mode: str = "") -> str:
    chunks: list[str] = []
    items: list[str] = []
    paragraph: list[str] = []
    job_title = ""

    def flush_paragraph() -> None:
        if paragraph:
            chunks.append("<p>" + "<br>".join(inline(x) for x in paragraph) + "</p>")
            paragraph.clear()

    def flush_items() -> None:
        if items:
            chunks.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            items.clear()

    for line in source.splitlines():
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_items()
            continue
        if stripped.startswith("#"):
            flush_paragraph()
            flush_items()
            depth = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[depth:].strip()
            if mode == "jobs" and depth == 2:
                job_title = re.sub(r"^\d+\.\s*", "", title)
            level = min(4, depth + (1 if mode in ("jobs", "defects") else 0))
            chunks.append(f"<h{level}>{inline(title)}</h{level}>")
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            content = stripped[2:]
            if mode == "jobs" and "Ảnh bằng chứng:" in content:
                flush_items()
                name_match = re.search(r"\]\((Job_Posting_Screenshots/[^)]+)\)", content)
                if name_match:
                    path = ROOT / "Requirement_1_Job_Market" / name_match.group(1)
                    chunks.append(f'<figure class="job-shot"><img src="{path.as_uri()}" alt="Ảnh tin tuyển dụng"><figcaption>{inline(job_title)}</figcaption></figure>')
                continue
            items.append(content)
            continue
        if stripped.startswith("---"):
            flush_paragraph()
            flush_items()
            chunks.append("<hr>")
            continue
        flush_items()
        paragraph.append(stripped)
    flush_paragraph()
    flush_items()
    return "\n".join(chunks)


def xlsx_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in cell.findall(".//m:t", ns)) for cell in root.findall("m:si", ns)]
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        rows: list[dict[str, str]] = []
        for row in sheet.findall(".//m:sheetData/m:row", ns):
            values: dict[str, str] = {}
            for cell in row.findall("m:c", ns):
                ref = cell.attrib["r"]
                column = re.match(r"[A-Z]+", ref).group(0)
                value = cell.find("m:v", ns)
                rich = cell.find("m:is", ns)
                if cell.attrib.get("t") == "s" and value is not None:
                    result = shared[int(value.text)]
                elif value is not None:
                    result = value.text or ""
                elif rich is not None:
                    result = "".join(t.text or "" for t in rich.findall(".//m:t", ns))
                else:
                    result = ""
                values[column] = result
            rows.append(values)
        headings = [rows[0].get(chr(c), "") for c in range(ord("A"), ord("L"))]
        return headings, rows[1:]


def cases_html() -> str:
    _, rows = xlsx_rows(ROOT / "Requirement_3_Physical_Product/04_Test_Cases_Excel/Senko_L1638_15_Test_Cases.xlsx")
    assert len(rows) == 15, f"Expected 15 test cases, found {len(rows)}"
    parts = ['<h2>3.2. Danh mục và kết quả 15 test case</h2>', '<table class="compact"><thead><tr><th>ID</th><th>Test case</th><th>Nguồn</th><th>Verdict</th></tr></thead><tbody>']
    for row in rows:
        parts.append("<tr>" + "".join(f"<td>{inline(row.get(c, ''))}</td>" for c in "ABCI") + "</tr>")
    parts.append("</tbody></table>")
    parts.append('<p>Workbook gốc gồm ba sheet <strong>Test Cases</strong>, <strong>Checklist</strong> và <strong>Test Summary Report</strong>. Phần dưới đây chép các trường bắt buộc của cả 15 case để có thể đọc report độc lập với Excel.</p>')
    fieldnames = [("D", "Objective"), ("E", "Input"), ("F", "Steps"), ("G", "Expected"), ("H", "Actual"), ("I", "Verdict"), ("J", "Bằng chứng"), ("K", "Ghi chú rà soát")]
    for row in rows:
        parts.append(f'<div class="testcase"><h3>{inline(row.get("A", ""))} — {inline(row.get("B", ""))}</h3><dl>')
        for key, label in fieldnames:
            value = row.get(key, "")
            if key in ("J", "K") and not value:
                continue
            if key == "J":
                video_link = re.search(r"https?://[^\s;]+", value)
                if not video_link:
                    continue
                url = html.escape(video_link.group(0))
                rendered = f'<a href="{url}">{url}</a>'
            else:
                rendered = inline(value).replace("\n", "<br>")
            parts.append(f"<dt>{label}</dt><dd>{rendered}</dd>")
        parts.append("</dl></div>")
    return "\n".join(parts)


def render() -> None:
    job_source = (ROOT / "Requirement_1_Job_Market/Requirement_1_10_QA_QC_Job_Postings.md").read_text()
    defect_source = (ROOT / "Requirement_2_Software_Defects/Requirement_2_20_Published_Software_Defects_2022_2026.md").read_text()
    critique = (ROOT / "AI_Critique.md").read_text().strip() if (ROOT / "AI_Critique.md").exists() else ""
    if not 200 <= len(critique.split()) <= 300:
        critique = (HERE / "content/AI_Critique.md").read_text().strip()
    disclosure = (ROOT / "Mandatory_Disclosure.md").read_text().strip() if (ROOT / "Mandatory_Disclosure.md").exists() else ""
    if "Gemini 3.1 Pro" not in disclosure:
        disclosure = (HERE / "content/Mandatory_Disclosure.md").read_text().strip()
    assert len(re.findall(r"^## \d+\.", job_source, re.M)) == 10
    assert len(re.findall(r"^### \d\d\.", defect_source, re.M)) == 20
    assert 200 <= len(critique.split()) <= 300
    assert "Gemini 3.1 Pro" in disclosure

    videos = [
        ("TC03", "https://youtube.com/shorts/jRWrYvkZZvo", "Pass", "54 giây"),
        ("TC04", "https://youtube.com/shorts/N0rbUCy_uAg", "Pass", "54 giây"),
        ("TC05", "https://youtube.com/shorts/b-d0SKiaxsM", "Fail", "58 giây"),
        ("TC07", "https://youtube.com/shorts/Btv0goBYFrg", "Pass", "60 giây"),
        ("TC14", "https://youtube.com/shorts/ZATVQeFVcuQ", "Pass", "34 giây"),
    ]
    video_rows = "".join(f'<tr><td>{id_}</td><td><a href="{url}">{url}</a></td><td>{verdict}</td><td>{duration}</td></tr>' for id_, url, verdict, duration in videos)
    jobs = markdown_fragment(job_source, "jobs")
    defects = markdown_fragment(defect_source, "defects").replace('href="../Appendix_A_Prompt_Log.md"', 'href="Appendix_A_Prompt_Log.md"')
    cases = cases_html()
    device = (ROOT / "Requirement_3_Physical_Product/01_Device_Photo/device.jpg").as_uri()
    issue = (ROOT / "Requirement_3_Physical_Product/06_GitHub_Issues_Evidence/TC05_GitHub_Issue.png").as_uri()
    chat_dir = ROOT / "Requirement_3_Physical_Product/02_AI_Test_Case_Output_Screenshots"
    chat_images = "\n".join(
        f'<figure class="chat-shot"><img src="{(chat_dir / f"{number}.png").as_uri()}" alt="Ảnh hội thoại AI {number}"><figcaption>Ảnh hội thoại gốc {number}/5: {caption}</figcaption></figure>'
        for number, caption in [
            (1, "prompt yêu cầu 12 test case"),
            (2, "danh sách TC01–TC12"),
            (3, "nội dung TC01–TC04"),
            (4, "nội dung TC05–TC08"),
            (5, "nội dung TC09–TC12"),
        ]
    )
    mindmap_file = ROOT / "Mindmap_QA_QC_ISTQB.png"
    if not mindmap_file.exists():
        mindmap_file = ROOT / "23120190_HW01_AI_100/Mindmap_QA_QC_ISTQB.png"
    mindmap = mindmap_file.as_uri()
    logo = (HERE / "img/hcmus-logo.png").as_uri()
    sources = """<ol>
      <li>Đề HW01: <em>2026.HW01.Jobs.Defects.PhysicalProduct_En.pdf</em>, bản trong thư mục bài.</li>
      <li><a href="https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf">ISTQB Certified Tester Foundation Level Syllabus v4.0.1</a>, §1.3, §1.4 và §5.3.</li>
      <li>Các thông báo gốc của nhà cung cấp/nhóm nghiên cứu được dẫn ngay tại từng lỗi trong Requirement 2.</li>
      <li>Excel kết quả thử quạt, video gốc, ảnh thiết bị, ảnh LinkedIn và <em>Appendix_A_Prompt_Log.md</em> trong thư mục bài.</li>
    </ol>"""
    content = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>HW01 – QA/QC Jobs, Defects, Physical Product</title>
    <style>
      @page {{ size: A4; margin: 20mm 18mm 18mm 18mm; }}
      * {{ box-sizing: border-box; }} html,body {{ margin:0; padding:0; }}
      body {{ font-family: 'Times New Roman', 'Liberation Serif', serif; font-size: 11pt; line-height:1.4; color:#171a20; }}
      a {{ color:#064e86; text-decoration:none; overflow-wrap:anywhere; }} h1,h2,h3 {{ color:#172b4d; line-height:1.25; break-after:avoid; }}
      h1 {{ font-size:19pt; margin:22pt 0 10pt; }} h2 {{ font-size:15pt; margin:17pt 0 8pt; }} h3 {{ font-size:12pt; margin:13pt 0 5pt; }}
      p {{ margin:5pt 0 8pt; text-align:justify; }} ul,ol {{ margin:4pt 0 10pt 0; padding-left:20pt; }} li {{ margin:3pt 0; }}
      code {{ font-size:9pt; white-space:normal; overflow-wrap:anywhere; }} table {{ border-collapse:collapse; width:100%; margin:8pt 0 14pt; }}
      th,td {{ border:1px solid #8491a0; padding:5pt 6pt; vertical-align:top; overflow-wrap:anywhere; }} th {{ background:#e7edf4; text-align:left; }}
      .compact {{ font-size:9pt; }} .compact th,.compact td {{ padding:3pt 4pt; }}
      .cover {{ height:255mm; text-align:center; break-after:page; display:flex; flex-direction:column; align-items:center; justify-content:space-between; }}
      .cover-head {{ text-transform:uppercase; font-size:14pt; font-variant:small-caps; line-height:1.8; }} .cover-head div:first-child {{ font-size:17pt; }}
      .rule {{ width:100%; border-top:2px solid #111; margin:15pt 0; }} .cover-title {{ font-size:25pt; font-weight:bold; line-height:1.3; }}
      .cover-sub {{ font-size:17pt; font-weight:bold; }} .cover-course {{ font-size:15pt; }} .cover-meta {{ display:flex; width:100%; justify-content:space-between; text-align:left; gap:30pt; font-size:12pt; }} .cover-meta div:last-child {{ text-align:right; }}
      .logo {{ width:95px; height:auto; }} .cover-date {{ font-size:13pt; }}
      .pagebreak {{ break-before:page; }} .job-shot {{ margin:5pt auto 14pt; text-align:center; break-inside:avoid; }} .job-shot img {{ max-width:100%; max-height:105mm; border:1px solid #aaa; }} figcaption {{ font-size:8pt; color:#555; }}
      .device-photo {{ display:block; max-height:145mm; max-width:100%; margin:auto; }} .issue-shot {{ display:block; max-width:100%; max-height:135mm; margin:auto; }} .mindmap {{ display:block; width:100%; max-height:150mm; object-fit:contain; }}
      .chat-shot {{ margin:9pt auto 14pt; text-align:center; break-inside:avoid; }} .chat-shot img {{ display:block; max-width:100%; max-height:175mm; margin:auto; }}
      .testcase {{ border-top:1px solid #cbd5df; margin-top:10pt; padding-top:3pt; }} dl {{ display:grid; grid-template-columns:72pt 1fr; gap:3pt 6pt; margin:4pt 0; font-size:9.6pt; }} dt {{ font-weight:bold; }} dd {{ margin:0; white-space:normal; }}
      .blank {{ min-height:40mm; border:1px solid #aab3bc; margin:12pt 0 22pt; }} .note {{ background:#f1f5f9; border-left:3px solid #59718e; padding:7pt 9pt; }}
      .toc a {{ color:#172b4d; }} .toc li {{ margin:5pt 0; }} .footer-note {{ font-size:9pt; color:#59636e; }}
    </style></head><body>
    <div class="cover">
      <div class="cover-head"><div>ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH</div><div>TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN</div><div>KHOA CÔNG NGHỆ THÔNG TIN</div><div>BỘ MÔN CÔNG NGHỆ TRI THỨC</div></div>
      <div style="width:100%"><div class="rule"></div><div class="cover-title">BÁO CÁO BÀI TẬP HW01</div><div class="cover-sub">QA/QC Jobs · Software Defects · Physical Product Testing</div><div class="rule"></div><div class="cover-course"><strong>Môn học:</strong> CSC13003 – Software Testing</div></div>
      <div class="cover-meta"><div><em>Sinh viên thực hiện:</em><br>Nguyễn Lê Thế Vinh<br>MSSV: 23120190<br>Lớp: CQ2023/31</div><div><em>Giảng viên phụ trách:</em><br>Trần Thị Bích Hạnh<br>Trương Phước Lộc<br>Hồ Tuấn Thanh</div></div>
      <div class="cover-date">TP. Hồ Chí Minh, ngày 28 tháng 09 năm 2026</div><img class="logo" src="{logo}" alt="Logo HCMUS"><div></div>
    </div>
    <h1>Mục lục</h1><ol class="toc"><li><a href="#overview">Tổng quan và phạm vi</a></li><li><a href="#jobs">Yêu cầu 1 — 10 tin tuyển dụng QA/QC</a></li><li><a href="#defects">Yêu cầu 2 — 20 lỗi phần mềm</a></li><li><a href="#product">Yêu cầu 3 — Kiểm thử quạt Senko L1638</a></li><li><a href="#mindmap">Mindmap QA/QC theo ISTQB</a></li><li><a href="#audit">AI Audit Report, Critique và Disclosure</a></li><li><a href="#self">Self-Assessment và tài liệu tham khảo</a></li><li>Phụ lục A — AI-02 Audit Report (ghép sau phần chính)</li></ol>

    <h1 id="overview" class="pagebreak">Tổng quan và phạm vi</h1>
    <p>Báo cáo này trình bày ba yêu cầu của HW01-AI: khảo sát 10 tin tuyển dụng QA/QC, đối chiếu 20 lỗi phần mềm đã công bố, và thiết kế/thực thi test case trên quạt đứng Senko L1638. Phần kiểm thử thiết bị sử dụng kết quả quan sát trực tiếp do người kiểm thử xác nhận: 15 test case được thiết kế, 5 case đã chạy (4 Pass, 1 Fail), 10 case chưa chạy. Nguồn dữ liệu đầy đủ gồm ảnh, workbook, video và prompt log được lưu cùng bài.</p>
    <p class="note">Ngày đăng tin tuyển dụng trong các ảnh là thời gian tương đối tại ngày chụp 24/09/2026. Điều kiện “trong 60 ngày” cần được đối chiếu một lần nữa theo ngày nộp thực tế. Không suy diễn kết quả cho những case chưa thực thi.</p>

    <h1 id="jobs" class="pagebreak">1. Yêu cầu 1 — Thị trường tuyển dụng QA/QC</h1>
    {jobs}
    <h2>1.1. Tổng hợp vai trò của AI trong QA/QC</h2>
    <p>Những tác vụ lặp lại như tạo bản nháp test case, tổng hợp tài liệu, phân nhóm defect hoặc đề xuất dữ liệu thử có thể được tự động hóa một phần. AI hỗ trợ tester mở rộng ý tưởng, tìm mẫu sai lệch và duy trì script, nhưng kết quả phải được rà theo yêu cầu, rủi ro và môi trường thực. Việc xác nhận expected/actual, đánh giá tác động lên người dùng, phát hiện lỗi trên thiết bị thật và quyết định phát hành cần bằng chứng và trách nhiệm của con người; công cụ AI không tự thay thế các phán đoán này.</p>

    <h1 id="defects" class="pagebreak">2. Yêu cầu 2 — 20 lỗi phần mềm công bố 2022–2026</h1>
    {defects}

    <h1 id="product" class="pagebreak">3. Yêu cầu 3 — Kiểm thử quạt đứng Senko L1638</h1>
    <h2>3.1. Thiết bị và phạm vi</h2>
    <p><strong>Hãng/model:</strong> Senko L1638. <strong>Năm:</strong> 2022. <strong>Serial:</strong> người sở hữu xác nhận thiết bị không có số serial; không tạo số giả. Thiết bị có ba mức tốc độ, chức năng chuyển hướng, hẹn giờ và điều chỉnh chiều cao theo người sở hữu xác nhận. Ảnh dưới đây chứa chính thiết bị và thẻ sinh viên trong cùng khung hình.</p>
    <figure><img class="device-photo" src="{device}" alt="Quạt Senko và thẻ sinh viên"><figcaption>Ảnh thiết bị và thẻ sinh viên trong cùng khung hình.</figcaption></figure>
    {cases}
    <h2>3.3. Tóm tắt thực thi và video</h2>
    <p>Đã chạy TC03, TC04, TC05, TC07, TC14: <strong>4 Pass, 1 Fail</strong>. Mười case còn lại giữ trạng thái <strong>Not Run</strong>. TC03 ghi góc nâng tờ giấy 45°, 50°, 70° theo thứ tự ba mức tốc độ; phương pháp đo góc chưa được mô tả. TC04 ghi 5/5 lần bấm phản hồi ngay. TC07 dùng đế tròn thực tế, đặt giấy dưới và trước đế; giấy không dịch chuyển. TC14 thực tế ngắt/cấp điện bằng rút rồi cắm phích, khác thao tác công tắc ngoài trong Steps; quạt chạy ổn định ở mức đã chọn khi có điện lại.</p>
    <table><thead><tr><th>Case</th><th>Video YouTube Unlisted</th><th>Verdict</th><th>Thời lượng theo bảng link</th></tr></thead><tbody>{video_rows}</tbody></table>
    <h2>3.4. Bằng chứng GitHub Issues</h2>
    <p>Ảnh chụp trang Issues của repository <strong>tzin1401/23120190-hw01</strong> hiển thị tài khoản <strong>tzin1401</strong> và một Issue đang mở cho lỗi quan sát ở TC05.</p>
    <figure><img class="issue-shot" src="{issue}" alt="Trang GitHub Issues hiển thị TC05 và tài khoản tzin1401"><figcaption>GitHub Issues — TC05: đầu quạt nghiêng hành trình về bên phải và có tiếng động khi đi qua giữa.</figcaption></figure>
    <h2>3.5. Bằng chứng AI bỏ sót TC13–TC15</h2>
    <p>Ảnh chụp hội thoại gốc ngày 27/09/2026 dưới đây ghi lại prompt và đầu ra của OpenCode / Big Pickle. Prompt yêu cầu đúng 12 test case; bảng danh mục trong ảnh 2 kết thúc ở TC12, còn ảnh 3–5 thể hiện nội dung của 12 case này. Ba tình huống TC13–TC15 không xuất hiện trong danh sách AI đưa ra và được bổ sung vào bộ 15 case trong Excel.</p>
    <table><thead><tr><th>Case bổ sung</th><th>Vì sao không có trong 12 case AI đưa ra</th></tr></thead><tbody>
      <tr><td>TC13 — Chỉnh chiều cao tới hai giới hạn</td><td>TC07 thử độ ổn định khi chạy tốc độ cao, nhưng không đưa thân quạt tới mức thấp nhất và cao nhất để kiểm tra chốt giữ ở hai đầu hành trình.</td></tr>
      <tr><td>TC14 — Mất rồi có điện trở lại</td><td>TC01–TC02 thử khởi động bằng nút điều khiển; TC11 kiểm tra dây và phích. Không case nào thử trạng thái quạt khi nguồn điện bị ngắt rồi được cấp lại trong lúc đã chọn tốc độ. TC14 đã được thực thi và ghi kết quả ở mục 3.2–3.3.</td></tr>
      <tr><td>TC15 — Nhấn OFF khi đang chạy tốc độ cao và chuyển hướng</td><td>TC04 thử phản hồi nút, TC05 thử chuyển hướng và TC07 thử tốc độ cao riêng lẻ. Không case nào kết hợp các trạng thái đó để quan sát lệnh OFF gần điểm đổi chiều.</td></tr>
    </tbody></table>
    {chat_images}

    <h1 id="mindmap" class="pagebreak">4. Mindmap QA/QC theo quy trình ISTQB</h1>
    <figure><img class="mindmap" src="{mindmap}" alt="Mindmap QA/QC ISTQB"><figcaption>Mindmap do công cụ AI tạo, giữ nguyên bản để đối chiếu.</figcaption></figure>
    <p>Ba điểm dưới đây là nhận xét và cách sửa nhãn dựa trên bản hình hiện có; ảnh gốc ở trên được giữ nguyên để thấy rõ đầu ra trước khi sửa.</p>
    <table><thead><tr><th>Trên hình</th><th>Vì sao cần sửa</th><th>Nhãn sửa đề xuất</th></tr></thead><tbody>
      <tr><td>8 AI Hỗ trợ</td><td>Đánh số AI như hoạt động thứ tám. ISTQB §1.4.1 mô tả các hoạt động từ planning đến completion; §6.1 xem công cụ là phần hỗ trợ nhiều hoạt động.</td><td>AI hỗ trợ xuyên suốt, không đánh số.</td></tr>
      <tr><td>Summary Report dưới Monitoring &amp; Control</td><td>ISTQB §1.4.3 và §5.3.2 phân biệt progress report khi theo dõi với completion report tại lúc hoàn tất.</td><td>Giữ Progress Report tại Monitoring &amp; Control; đặt Test Completion Report tại Completion.</td></tr>
      <tr><td>QC Phản ánh CL thật</td><td>Cụm này dễ khẳng định quá mức. ISTQB §1.3 nêu kiểm thử có thể cho thấy lỗi nhưng không chứng minh không còn lỗi.</td><td>QC ghi nhận actual/expected, lỗi và rủi ro còn lại.</td></tr>
    </tbody></table><p>Đối chiếu: <a href="{ISTQB}">ISTQB CTFL v4.0.1</a>. Bản giải thích đầy đủ được lưu trong <em>Mindmap_3_Errors_ISTQB.md</em>.</p>

    <h1 id="audit" class="pagebreak">5. AI Audit Report, AI Critique và công bố sử dụng AI</h1>
    <h2>5.1. AI Audit Report</h2><p>Phụ lục A của chính PDF này chứa biểu mẫu AI-02 đã điền cho 25 artifact với năm trường: prompt + công cụ + thời gian, output, verdict, reasoning và bản sửa. Bảng dùng trích đoạn output để dễ đọc; phần Phụ lục B ngay sau biểu mẫu chép toàn văn AI Output cho cả 25 artifact. Kết quả phân loại là 0 VALID, 1 INVALID, 24 INCOMPLETE. Full prompt log là tệp riêng <a href="Appendix_A_Prompt_Log.md">Appendix_A_Prompt_Log.md</a> có 28 lượt.</p>
    <h2>5.2. AI Critique (200–300 từ)</h2><p>{inline(critique)}</p>
    <h2>5.3. Mandatory Disclosure</h2><p lang="en">{inline(disclosure)}</p>

    <h1 id="self" class="pagebreak">6. Self-Assessment và tài liệu tham khảo</h1>
    <p>Bảng tự chấm theo rubric đề HW01; đây không phải điểm do giảng viên chấm.</p>
    <table><thead><tr><th>Mục</th><th>Tiêu chí</th><th>Điểm tối đa</th><th>Điểm tự chấm</th></tr></thead><tbody>
      <tr><td>1</td><td>Job Market 2026+ — 10 jobs và AI Impact</td><td>40</td><td>40</td></tr>
      <tr><td>2</td><td>Software Defects 2022–2026 — 20 defects</td><td>20</td><td>20</td></tr>
      <tr><td>3</td><td>Physical-product test design — 15 TCs và 5 videos</td><td>25</td><td>25</td></tr>
      <tr><td>AI-1</td><td>AI-02 Audit Report</td><td>8</td><td>8</td></tr>
      <tr><td>AI-2</td><td>AI Critique và AI-03 Disclosure</td><td>4</td><td>4</td></tr>
      <tr><td>AI-3</td><td>AI-05 Checklist và bằng chứng</td><td>3</td><td>3</td></tr>
      <tr><th colspan="2">Tổng</th><th>100</th><th>100</th></tr>
    </tbody></table>
    <h2>Tài liệu tham khảo</h2>{sources}
    <h1 class="pagebreak">Phụ lục A — AI-02 Audit Report</h1><p>Biểu mẫu AI-02 đầy đủ bắt đầu ngay trang tiếp theo. Prompt log nguyên văn được nộp dưới dạng tệp riêng để đối chiếu.</p>
    </body></html>"""
    OUT.write_text(content)


def build_pdf() -> None:
    chrome = ["google-chrome", "--headless", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files", "--no-pdf-header-footer", f"--print-to-pdf={PDF_BODY}", OUT.as_uri()]
    subprocess.run(chrome, cwd=HERE, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    audit_docx = ROOT / "23120190_HW01_AI_100/[AI-02] - FIT@HCMUS - AI Audit Report.docx"
    subprocess.run(["libreoffice", "-env:UserInstallation=file:///tmp/lo_hw01_report", "--headless", "--convert-to", "pdf", "--outdir", str(HERE), str(audit_docx)], cwd=HERE, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    generated = HERE / f"{audit_docx.stem}.pdf"
    generated.replace(PDF_AUDIT)
    subprocess.run(["pdfunite", str(PDF_BODY), str(PDF_AUDIT), str(PDF_FINAL)], check=True)


if __name__ == "__main__":
    render()
    build_pdf()
    print(PDF_FINAL)
