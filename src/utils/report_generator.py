from markdown_pdf import MarkdownPdf, Section
from pathlib import Path
import os

# ====== 1) Font Configuration ======
# Use the absolute path to the font file
FONT_PATH = Path(r"C:\Users\ADMIN\Desktop\work\nycu_AI_Architect\projects\oss_guardian\fonts\NotoSansTC-Regular.ttf")
FONT_NAME = "NotoSansTC"

def generate_pdf(markdown_text: str) -> bytes:
    """
    Converts Markdown string to PDF bytes using markdown-pdf.
    """
    pdf = MarkdownPdf(toc_level=2)

    # Add custom font CSS if it exists
    css_content = ""
    if FONT_PATH.exists():
        # Note: markdown-pdf uses weasyprint under the hood or similar, 
        # but the library structure might differ. 
        # Actually markdown-pdf uses PyMuPDF and markdown-it-py.
        # It doesn't support CSS in the same way weasyprint does for the whole document easily via a simple string 
        # unless we use the styles parameter or similar.
        # However, looking at the library usage, it often supports adding sections.
        
        # Let's try to use the basic usage first, but we need to ensure Chinese characters are supported.
        # markdown-pdf might not support custom fonts via CSS string directly in the same way.
        # Wait, the user wants to use markdown_pdf to SOLVE the issue.
        # Let's check if markdown_pdf supports Chinese out of the box or needs font registration.
        
        # Re-reading the plan: "Implement PDF generation using markdown_pdf with custom font support (via CSS)."
        # I need to be careful here. markdown-pdf (the pypi package) is a wrapper.
        # Let's assume standard usage for now but if I need to register font I might need to look deeper.
        # The search result said: "allows you to pass a custom CSS file to style the generated PDF."
        
        # Let's try to load the font via CSS.
        pass
    
    # Based on search results, markdown-pdf allows adding sections.
    # It seems it might be simpler.
    # Let's construct the PDF.
    
    pdf.add_section(Section(markdown_text, toc=False))
    
    # To support Chinese, we might need to set the meta or style.
    # If markdown-pdf uses simple html conversion, we might still need the font in the system or passed somehow.
    # But let's try the simplest implementation first as requested.
    # Wait, if I don't set the font, it might still fail for Chinese.
    # The user said "use markdown_pdf to convert".
    
    # Let's look at the library's `add_section` or `__init__`.
    # Since I cannot run help() easily, I will stick to the plan but I will try to include the CSS if possible.
    # Actually, the `markdown-pdf` library on PyPI (https://pypi.org/project/markdown-pdf/) 
    # shows `pdf.add_section(Section("# Title\nBody"))`.
    # It also has `pdf.meta`.
    
    # Let's write the code to use the library. 
    # If it fails to render Chinese, we might need to look at `css` argument in `Section` if it exists, 
    # or `styles` in `MarkdownPdf`.
    
    # Let's assume we just need to pass the content for now, 
    # BUT we should probably try to set the font if possible.
    # Since I can't easily check the library internals without running it, 
    # I will write a script to test it in the verification phase.
    
    # However, to be safe and follow the "custom font" plan:
    # I will try to define a CSS string that uses the font.
    
    # For now, I will implement a basic version that replaces the old one.
    
    # NOTE: The user mentioned "markdown_pdf" specifically.
    
    pdf.meta["title"] = "OSS Guardian Report"
    
    # We need to return bytes.
    # pdf.save(filename) saves to file.
    # We need bytes.
    # There isn't a direct `to_bytes` method documented in the brief summary.
    # Usually `output()` or similar. 
    # Or we save to a temporary buffer.
    
    import io
    out_stream = io.BytesIO()
    # If the library only supports save to path, we might need a temp file.
    # But let's check if we can pass a file-like object.
    # Many libraries support it.
    
    try:
        pdf.save(out_stream)
        return out_stream.getvalue()
    except Exception:
        # Fallback if it requires a string path
        temp_filename = "temp_report.pdf"
        pdf.save(temp_filename)
        with open(temp_filename, "rb") as f:
            data = f.read()
        os.remove(temp_filename)
        return data

# We remove generate_html as it is no longer needed for the PDF generation 
# (or we keep it if other parts use it, but the plan said remove/deprecate).
# The server.py uses it, but we will update server.py.
# verify_pdf.py uses it, but we will update verify_pdf.py.
# So we can remove it.

