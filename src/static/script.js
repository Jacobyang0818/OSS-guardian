document.addEventListener('DOMContentLoaded', () => {
    const queryInput = document.getElementById('queryInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    // const providerSelect = document.getElementById('providerSelect'); // Removed
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const reportContent = document.getElementById('reportContent');
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');
    const steps = document.querySelectorAll('.steps li');

    let currentReportMarkdown = "";

    analyzeBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        // const provider = providerSelect.value; // Removed provider selection
        if (!query) return;

        // UI Reset
        analyzeBtn.disabled = true;
        resultDiv.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        reportContent.innerHTML = "";
        currentReportMarkdown = "";

        // Reset steps
        steps.forEach(s => {
            s.classList.remove('active');
            s.style.opacity = "0.5";
        });

        // SSE Connection
        const eventSource = new EventSource(`/stream_analysis?query=${encodeURIComponent(query)}`);

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.type === 'status') {
                // Update status message
                const msg = data.message.toLowerCase();

                // Simple logic to highlight steps based on message content
                if (msg.includes('scout')) {
                    activateStep(0);
                } else if (msg.includes('risk')) {
                    activateStep(1);
                } else if (msg.includes('security')) {
                    activateStep(2);
                } else if (msg.includes('technical') || msg.includes('cto')) {
                    activateStep(3);
                }

            } else if (data.type === 'result') {
                currentReportMarkdown = data.report;
                currentReportMarkdown = data.report;
                try {
                    if (typeof marked !== 'undefined') {
                        // Check if marked.parse exists (v4+), otherwise use marked()
                        const html = marked.parse ? marked.parse(currentReportMarkdown) : marked(currentReportMarkdown);
                        reportContent.innerHTML = html;
                    } else {
                        console.error("marked library not found!");
                        reportContent.innerText = currentReportMarkdown; // Fallback to text
                        alert("Markdown library not loaded. Showing raw text.");
                    }
                } catch (e) {
                    console.error("Error parsing markdown:", e);
                    reportContent.innerText = currentReportMarkdown;
                }
                loadingDiv.classList.add('hidden');
                resultDiv.classList.remove('hidden');
                eventSource.close();
                analyzeBtn.disabled = false;
            } else if (data.type === 'error') {
                alert(`發生錯誤: ${data.message}`);
                loadingDiv.classList.add('hidden');
                eventSource.close();
                analyzeBtn.disabled = false;
            }
        };

        eventSource.onerror = () => {
            // Only alert if we haven't finished (sometimes connection closes abruptly)
            if (!currentReportMarkdown) {
                alert("連線中斷");
                loadingDiv.classList.add('hidden');
                analyzeBtn.disabled = false;
            }
            eventSource.close();
        };
    });

    function activateStep(index) {
        steps.forEach((s, i) => {
            if (i === index) {
                s.classList.add('active');
                s.style.opacity = "1";
            } else {
                s.classList.remove('active');
            }
        });
    }

    downloadPdfBtn.addEventListener('click', async () => {
        if (!currentReportMarkdown) return;

        try {
            const response = await fetch('/report/pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ markdown: currentReportMarkdown })
            });

            if (!response.ok) throw new Error("PDF generation failed");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `OSS_Guardian_Report_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

        } catch (error) {
            alert(`PDF 下載失敗: ${error.message}`);
        }
    });
});
