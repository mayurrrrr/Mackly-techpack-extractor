import streamlit as st
import pdfplumber
import pandas as pd
import re

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
				data[field] = match.group(1).strip() if match else ""

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

	# Recompute length after edits for export/validation
	edited_df["ITEM NAME LENGTH"] = edited_df["ITEM NAME"].apply(lambda x: len(x) if isinstance(x, str) else 0)

	if st.button("Export to CSV"):
		export_df = edited_df.copy()
		if "FILE" in export_df.columns:
			export_df = export_df.drop(columns=["FILE"])
		export_df.to_csv("output.csv", index=False, encoding="utf-8-sig")
		st.download_button("Download CSV", open("output.csv","rb"), "techpacks.csv")
