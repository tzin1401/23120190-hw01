#!/usr/bin/env bash
set -euo pipefail

report_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$report_dir/build_report.py"
python3 "$report_dir/prepare_latex.py"

if command -v tectonic >/dev/null 2>&1; then
  tectonic_bin="$(command -v tectonic)"
else
  tectonic_bin="$HOME/.local/bin/tectonic"
fi

(cd "$report_dir" && "$tectonic_bin" main.tex --outdir "$report_dir")
mv -f "$report_dir/main.pdf" "$report_dir/HW01_Main_Report.pdf"
rm -f "$report_dir/HW01_HTML_Preview.pdf" "$report_dir/HW01_Main_Report_Body.pdf"
pdfinfo "$report_dir/HW01_Main_Report.pdf" | rg 'Pages|Page size|File size'
