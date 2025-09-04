import streamlit as st
import pdfplumber
import pandas as pd
import re
from datetime import datetime

st.title("Mackly Techpack Extractor")

st.info("You can upload multiple PDFs at once. Use Ctrl/Shift in the file picker or drag-and-drop several files.")
st.caption("Processing multiple files may take a moment; you'll see a loading indicator while we prepare the summary.")

uploaded_file = st.file_uploader("Upload Techpack PDF(s)", type="pdf", accept_multiple_files=True)

fields = [
	"COLLECTION NUMBER","ITEM NAME","CATEGORY","SILHOUETTE","GENDER",
	"STYLE NUMBER","WEBSITE NAME","SUB CATEGORY","SIZE RANGE","DATE",
	"FABRIC TOP","DESIGNER","COLOR COMBO","PRINT NAME",
	"FABRIC BOTTOM","FABRIC FULL GARMENT","PRINT TECHNIQUE"
]

def _normalize_date_to_ddmmyyyy(raw_value: str) -> str:
	"""Return date in dd/mm/yyyy if parseable; else return original string or empty."""
	if not isinstance(raw_value, str):
		return raw_value
	s = raw_value.strip()
	if not s or s.lower() in {"n/a", "na", "tbd", "-"}:
		return ""
	# Try common formats (month/day/year, year-month-day, day-month-year, textual month)
	candidates = [
		"%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
		"%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y",
		"%Y-%m-%d", "%Y/%m/%d",
		"%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y",
		"%d/%m/%y", "%d-%m-%y", "%m/%d/%y", "%m-%d-%y"
	]
	for fmt in candidates:
		try:
			dt = datetime.strptime(s, fmt)
			return dt.strftime("%d/%m/%Y")
		except ValueError:
			continue
	# Fallback: attempt to normalize separators and re-try day-first heuristic
	s_norm = re.sub(r"[.\-]", "/", s)
	m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{2,4})$", s_norm)
	if m:
		day, month, year = m.groups()
		if len(year) == 2:
			year = ("20" + year) if int(year) <= 68 else ("19" + year)
		try:
			dt = datetime(int(year), int(month), int(day))
			return dt.strftime("%d/%m/%Y")
		except ValueError:
			pass
	return s

fields_to_normalize = {"DATE"}

if uploaded_file:
	# Backward compatibility: single file input returns list when accept_multiple_files=True
	uploaded_files = uploaded_file if isinstance(uploaded_file, list) else [uploaded_file]

	with st.spinner(f"Processing {len(uploaded_files)} file(s)... This may take a moment."):
		progress = st.progress(0, text="Starting…")
		records = []
		for idx, f in enumerate(uploaded_files):
			with pdfplumber.open(f) as pdf:
				text = pdf.pages[0].extract_text()

			# Normalize spacing while preserving line breaks so our regex can stop at newlines
			text = re.sub(r"[ \t]+", " ", text)

			data = {}
			for field in fields:
				# Build a lookahead that stops at the next known label on the same line, or a newline/end
				others = [re.escape(ff) for ff in fields if ff != field]
				others_union = "|".join(sorted(others, key=len, reverse=True))
				lookahead = rf"(?:\s(?:{others_union})\b|\n|$)" if others_union else r"(?:\n|$)"
				pattern = rf"{re.escape(field)}\s*(.*?)(?={lookahead})"
				match = re.search(pattern, text)
				value = match.group(1).strip() if match else ""
				if field in fields_to_normalize:
					value = _normalize_date_to_ddmmyyyy(value)
				data[field] = value

			row = {"FILE": f.name}
			row.update(data)
			row["ITEM NAME LENGTH"] = len(row.get("ITEM NAME", ""))
			records.append(row)

			progress.progress((idx + 1) / len(uploaded_files), text=f"Processed {idx + 1} of {len(uploaded_files)}")

		progress.empty()

	# Create DataFrame in a stable column order
	df = pd.DataFrame(records, columns=["FILE"] + fields + ["ITEM NAME LENGTH"])

	st.write("### Summary")
	styled = df.style.applymap(lambda v: "color: green" if v <= 23 else "color: red", subset=["ITEM NAME LENGTH"]) if not df.empty else df
	st.dataframe(styled, use_container_width=True)

	st.write("### Edit extracted values")
	editable_cols = ["FILE"] + fields
	edited_df = st.data_editor(df[editable_cols], use_container_width=True)

	# Recompute derived fields and normalize DATE after edits
	edited_df["ITEM NAME LENGTH"] = edited_df["ITEM NAME"].apply(lambda x: len(x) if isinstance(x, str) else 0)
	if "DATE" in edited_df.columns:
		edited_df["DATE"] = edited_df["DATE"].apply(_normalize_date_to_ddmmyyyy)

	if st.button("Export to CSV"):
		export_df = edited_df.copy()
		if "FILE" in export_df.columns:
			export_df = export_df.drop(columns=["FILE"])
		export_df.to_csv("output.csv", index=False, encoding="utf-8-sig")
		st.download_button("Download CSV", open("output.csv","rb"), "techpacks.csv")
