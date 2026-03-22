
    
from app.core.config import client

class SummarizerAgent:
    def summarize(self, text):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Summarize this research paper in 3 bullet points:\n{text}"
            )
            return response.text

        except Exception as e:
            print("Gemini error:", e)
            return text[:200] + "..."  # ✅ fallback summary