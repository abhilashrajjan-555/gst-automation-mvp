# Analyze GST Notice - Directive

## Goal
Analyze a GST notice (PDF) using AI to explain it in simple language and suggest action items.

## Inputs
- **Notice PDF**: Scanned or digital copy of the notice (e.g., Form GST DRC-01, ASMT-10)

## Process

### Step 1: Text Extraction (OCR)
Extract text from the PDF using `app.ocr`.
- Handle multi-column layouts.
- Extract key metadata: Notice No, Date, Section, Demand Amount.

### Step 2: AI Analysis (LLM)
Send extracted text to LLM (e.g., Claude/Gemini) with a prompt:
"Analyze this GST notice. Summarize the reason for the notice, the amount demanded, the due date, and the required action in simple English/Hindi."

### Step 3: Structured Extraction
Extract specific fields:
- **Notice Type**: SCN / Demand / Scrutiny
- **Section**: e.g., Section 73, Section 74
- **Financial Year**: e.g., 2023-24
- **Amount Demanded**: Tax + Interest + Penalty
- **Due Date**: Date to reply/pay

### Step 4: Action Plan Generation
Based on notice type:
- **DRC-01**: "Pay the amount or file a reply in Form DRC-06."
- **ASMT-10**: "File explanation in Form ASMT-11."
- **GSTR-3A**: "File pending returns within 15 days."

## Outputs
- **Analysis Report**:
    - **Summary**: "You have received a notice for mismatch in ITC between GSTR-3B and 2A."
    - **Severity**: High/Medium/Low
    - **Deadline**: "15th Dec 2025"
    - **Action Items**: Checklist of steps.

## Edge Cases
- **Unclear Scan**: Ask user to re-upload.
- **Complex Legal Language**: Provide a disclaimer ("Consult a CA for legal advice").
- **Unknown Notice Type**: Flag for manual review.

## Success Criteria
- ✅ Correctly identify notice type and amount
- ✅ Provide accurate due date
- ✅ Explanation is understandable by a layman
