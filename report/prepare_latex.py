#!/usr/bin/env python3
"""Convert the fully populated HTML report body to the original LaTeX template."""

import os
import re
import subprocess
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
html_source = (HERE / "HW01_Main_Report.html").read_text()
start = html_source.index('<h1 id="overview"')
end = html_source.index('<h1 class="pagebreak">Phụ lục A')
body = html_source[start:end]


def local_image(match: re.Match[str]) -> str:
    uri = match.group(1)
    path = Path(urllib.parse.urlparse(uri).path)
    return 'src="' + os.path.relpath(path, HERE) + '"'


body = re.sub(r'src="(file://[^"]+)"', local_image, body)
body = re.sub(r'<div class="blank"></div>', '<p> </p>', body)
html_path = HERE / ".hw01_body_for_pandoc.html"
html_path.write_text('<!doctype html><html lang="vi"><meta charset="utf-8"><body>' + body + '</body></html>')
pandoc = Path.home() / ".local/bin/pandoc"
result = subprocess.run([str(pandoc), "--from=html", "--to=latex", "--wrap=none", "--resource-path", str(HERE), str(html_path)], check=True, capture_output=True, text=True)
html_path.unlink()
tex = result.stdout
tex = tex.replace('\\begin{figure}', '\\begin{figure}[H]')
def sized_image(match: re.Match[str]) -> str:
    path = match.group(1)
    height = "0.65" if "01_Device_Photo" in path else ("0.68" if "02_AI_Test_Case_Output_Screenshots" in path else ("0.55" if "06_GitHub_Issues_Evidence" in path else ("0.45" if "Mindmap_QA_QC" in path else "0.42")))
    return "\\includegraphics[width=\\linewidth,height=" + height + "\\textheight,keepaspectratio]{" + path + "}"

tex = re.sub(r'\\pandocbounded\{\\includegraphics\[[^\]]*\]\{([^}]+)\}\}', sized_image, tex)
tex = tex.replace('\\begin{longtable}[]{@{}llll@{}}', '\\begin{longtable}[]{@{}p{0.11\\linewidth}p{0.46\\linewidth}p{0.17\\linewidth}p{0.15\\linewidth}@{}}')
tex = tex.replace('\\begin{longtable}[]{@{}lll@{}}', '\\begin{longtable}[]{@{}p{0.16\\linewidth}p{0.47\\linewidth}p{0.26\\linewidth}@{}}')
tex = tex.replace('\\begin{longtable}[]{@{}ll@{}}', '\\begin{longtable}[]{@{}p{0.34\\linewidth}p{0.58\\linewidth}@{}}')
tex = tex.replace('\\emph{Requirement\\_3\\_Physical\\_Product/05\\_Execution\\_Videos}', '\\path{Requirement_3_Physical_Product/05_Execution_Videos}')
tex = re.sub(r'\.\./05\\_Execution\\_Videos/TC(\d+)\.mp4', r'\\path{../05_Execution_Videos/TC\1.mp4}', tex)
tex = tex.replace('../06\\_GitHub\\_Issues\\_Evidence/TC05\\_Issue\\_Draft.md', '\\path{../06_GitHub_Issues_Evidence/TC05_Issue_Draft.md}')
tex = tex.replace('\\texttt{react-server-dom-turbopack}', '\\texttt{react-server-dom-\\allowbreak{}turbopack}')
(HERE / "content/hw01_report.tex").write_text(tex)
print(HERE / "content/hw01_report.tex", len(tex))
