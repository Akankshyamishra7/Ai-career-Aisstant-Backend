import io
import re
from typing import Tuple, Dict, Any, Optional
from pypdf import PdfReader

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
        """
        Extracts clean text from raw PDF bytes using pypdf.
        """
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            extracted_pages = []
            for idx, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(page_text)
            
            full_text = "\n".join(extracted_pages)
            return ResumeParser.clean_text(full_text)
        except Exception as e:
            print(f"[ResumeParser] Error extracting PDF text: {e}")
            raise ValueError(f"Failed to read PDF document: {str(e)}")

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """
        Cleans up excessive whitespace, special symbols, and organizes resume lines.
        """
        if not raw_text:
            return ""

        # Replace non-breaking spaces and irregular whitespace
        text = raw_text.replace("\xa0", " ").replace("\r\n", "\n").replace("\r", "\n")
        # Remove consecutive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Remove repeated tabs and multiple spaces
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    @staticmethod
    def extract_candidate_details(text: str) -> Dict[str, Any]:
        """
        Extracts candidate metadata including Name, Email, Phone, LinkedIn, and GitHub.
        """
        details = {
            "name": "Candidate",
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None,
            "word_count": len(text.split()) if text else 0
        }

        if not text:
            return details

        # 1. Email extraction
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        if email_match:
            details["email"] = email_match.group(0)

        # 2. Phone extraction (international or US formats)
        phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        if phone_match:
            details["phone"] = phone_match.group(0)

        # 3. LinkedIn extraction
        linkedin_match = re.search(r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[\w\-]+", text, re.IGNORECASE)
        if linkedin_match:
            details["linkedin"] = linkedin_match.group(0)

        # 4. GitHub extraction
        github_match = re.search(r"(?:https?:\/\/)?(?:www\.)?github\.com\/[\w\-]+", text, re.IGNORECASE)
        if github_match:
            details["github"] = github_match.group(0)

        # 5. Name extraction heuristic: First meaningful line without contact info
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines[:5]:
            # Skip if line looks like header, contact, or title
            if any(term in line.lower() for term in ["resume", "curriculum", "email", "@", "phone", "http", "github", "linkedin", "page"]):
                continue
            # Remove trailing title e.g. "John Doe - Fullstack Engineer"
            name_candidate = line.split("-")[0].split("|")[0].strip()
            words = name_candidate.split()
            if 1 <= len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
                details["name"] = name_candidate
                break

        return details

resume_parser = ResumeParser()
