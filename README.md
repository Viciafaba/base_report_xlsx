# base_report_xlsx
Base XLSX Reports (Server Action Helper)
Unlock the power of real Excel (.xlsx) generation directly inside Odoo Server Actions.

If you have ever tried to create an Excel file using a Python Server Action in Odoo, you likely encountered the infamous ValueError: forbidden opcode(s): IMPORT_NAME. Odoo's safe_eval sandbox blocks standard Python libraries like xlsxwriter, io, and base64, making it impossible to generate native Excel files on the fly.

This module provides an elegant, secure, and universal solution. It introduces a global helper model (export.xlsx.helper) that acts as an engine for your Server Actions, allowing you to generate perfectly formatted, binary .xlsx files with just a few lines of code.

🌟 Key Features
Bypass Sandbox Limitations: Safely generate Excel files from Server Actions without modifying Odoo's core security settings.

Universal Engine: Pass any list of headers and data rows. The engine does the heavy lifting and returns a ready-to-use base64 encoded file.

Smart Number Formatting: Automatically detects long numeric strings (like EAN, UPC, or Barcodes) and forces them into a text format. Say goodbye to Excel converting your barcodes into scientific notation (e.g., 5.9E+12)!

Clean and Native: Uses Odoo's built-in xlsxwriter library under the hood. No external dependencies required.

🚀 How to Use (Example)
Once the module is installed, you can call the helper from any Server Action. Here is a complete example of how to generate an Excel file and attach it to a record:

Python
<pre>
# 1. Define your headers and data
headers = [&#39;Order Reference&#39;, &#39;Product Name&#39;, &#39;SKU&#39;, &#39;EAN Barcode&#39;, &#39;Quantity&#39;]
data_rows = []

for line in record.move_ids_without_package:
    data_rows.append([
        record.name,
        line.product_id.name or &#39;&#39;,
        line.product_id.default_code or &#39;&#39;,
        line.product_id.barcode or &#39;&#39;, # Will be safely formatted as text
        line.quantity
    ])

# 2. Call the helper engine
xlsx_base64 = env[&#39;export.xlsx.helper&#39;].generate_xlsx(
    headers=headers, 
    data_rows=data_rows, 
    sheet_name=&#39;Delivery Data&#39;
)

# 3. Create the attachment
attachment = env[&#39;ir.attachment&#39;].create({
    &#39;name&#39;: &#39;Delivery_Data_%s.xlsx&#39; % record.name,
    &#39;type&#39;: &#39;binary&#39;,
    &#39;datas&#39;: xlsx_base64,
    &#39;res_model&#39;: record._name,
    &#39;res_id&#39;: record.id,
    &#39;mimetype&#39;: &#39;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet&#39;,
})
</pre>

🛠️ Technical Details
Model: export.xlsx.helper

Method: generate_xlsx(headers, data_rows, sheet_name='Data')

headers: A list of strings (e.g., ['Name', 'Price'])

data_rows: A list of lists containing the row values (e.g., [['Apple', 1.50], ['Banana', 2.00]])

sheet_name: (Optional) The name of the Excel worksheet. Defaults to 'Data'.

Returns: A base64 encoded string containing the binary .xlsx file data.

📝 License
This module is licensed under the LGPL-3.0 License.
