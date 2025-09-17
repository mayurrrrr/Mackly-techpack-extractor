# 📄 Mackly Techpack Extractor - User Guide

## What is this? 🤔

This is a web tool that automatically extracts information from your techpack PDFs and puts it into a spreadsheet. No more manual typing!

## How to access it? 🌐

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Go to: **https://mackly-techpack-exctractor.streamlit.app/**
3. The page will load and show "Mackly Techpack Extractor"

## How to use it? 🚀

### Step 1: Upload your PDFs
1. Click on the "Upload Techpack PDF(s)" button
2. Select one or multiple PDF files from your computer
3. You can select multiple files by holding Ctrl (Windows) or Cmd (Mac) while clicking
4. Click "Open" to upload them

### Step 2: Wait for processing
- You'll see a loading spinner saying "Processing X file(s)... This may take a moment"
- A progress bar will show how many files have been processed
- **Don't close the browser** while it's processing!

### Step 3: Review the results
- You'll see a "Summary" table showing all the information found
- The "ITEM NAME LENGTH" column shows character counts:
  - 🟢 **Green** = Good (23 characters or less)
  - 🔴 **Red** = Too long (over 23 characters)

### Step 4: Edit if needed
- Scroll down to "Edit extracted values" section
- Click in any cell to edit the information
- Make sure "ITEM NAME" is not too long (keep it under 23 characters)
- Dates will automatically be formatted as dd/mm/yyyy

### Step 5: Download your spreadsheet
1. Click the "Export to Excel" button
2. Click "Download Excel" when it appears
3. Save the file to your computer
4. Open it in Excel to see your organized data!

## What information does it find? 📋

The tool looks for these things in your PDFs:
- Collection Number
- Item Name (with a character counter - green if under 23, red if over)
- Category
- Silhouette
- Gender
- Style Number
- Website Name
- Sub Category
- Size Range
- Date (automatically formatted as dd/mm/yyyy)
- Fabric Top
- Designer
- Color Combo
- Print Name
- Fabric Bottom
- Fabric Full Garment
- Print Technique

## What information does it find? 📋

The tool automatically finds these fields in your PDFs:
- **Collection Number** - The collection this item belongs to
- **Item Name** - Name of the clothing item (keep under 23 characters!)
- **Category** - Type of clothing (shirt, dress, etc.)
- **Silhouette** - The shape/style of the item
- **Gender** - Men's, Women's, Unisex, etc.
- **Style Number** - Unique code for this item
- **Website Name** - Where it will be sold online
- **Sub Category** - More specific category
- **Size Range** - Available sizes
- **Date** - When it was created (automatically formatted as dd/mm/yyyy)
- **Fabric Top** - Material for the top part
- **Designer** - Who designed it
- **Color Combo** - Color combinations
- **Print Name** - Name of any prints/patterns
- **Fabric Bottom** - Material for the bottom part
- **Fabric Full Garment** - Material for the whole item
- **Print Technique** - How prints are applied

## Tips for best results 💡

### PDF Requirements
- Make sure your PDF has clear text (not just images)
- The tool looks for exact words like "ITEM NAME:", "DATE:", etc.
- PDFs should not be password protected

### Item Name Length
- Keep "Item Name" under 23 characters
- The tool shows green when it's good, red when it's too long
- You can edit it in the table if needed

### Multiple Files
- You can upload many PDFs at once
- Each PDF will be processed separately
- All results will be combined in one Excel file

## Troubleshooting 🔧

**Problem**: "No information found" for some fields
**Solution**: Check that your PDF has the exact labels like "ITEM NAME", "DATE", etc.

**Problem**: Item Name is too long (red color)
**Solution**: Click in the table and make it shorter (under 23 characters)

**Problem**: Dates look wrong
**Solution**: The tool tries to fix dates automatically, but you can edit them in the table

**Problem**: Upload is slow
**Solution**: This is normal for large files or many files. Wait for the progress bar to finish.

## Need Help? 🤝

If something doesn't work:
1. Try refreshing the webpage
2. Make sure your PDF files are not password protected
3. Try with one simple PDF first to test
4. Contact your IT team if problems persist

---

**Made with ❤️ for Mackly Design Team**
