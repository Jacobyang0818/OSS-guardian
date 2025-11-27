import os
from src.utils.report_generator import generate_pdf

def test_pdf_generation():
    print("Testing PDF Generation with Chinese characters...")
    
    markdown_content = """
# 測試報告

這是一個測試報告，包含中文字元。

## 章節 1

- 項目 A
- 項目 B

```python
print("Hello World")
```

| 標題 1 | 標題 2 |
| :--- | :--- |
| 內容 1 | 內容 2 |
    """
    
    try:
        # html = generate_html(markdown_content)
        # print("HTML generated successfully.")
        
        pdf_bytes = generate_pdf(markdown_content)
        print(f"PDF generated successfully. Size: {len(pdf_bytes)} bytes")
        
        with open("test_output.pdf", "wb") as f:
            f.write(pdf_bytes)
        print("PDF saved to test_output.pdf")
        
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    test_pdf_generation()
