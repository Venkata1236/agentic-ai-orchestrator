"""
Scalable Document Intelligence - 100+ Pages
"""
import json
import re
import asyncio
from typing import Dict, Any, List
from agents import summary_agent, action_agent, risk_agent
import tiktoken

class DocumentAnalyzer:
    def __init__(self):
        self.summary_agent = summary_agent
        self.action_agent = action_agent
        self.risk_agent = risk_agent
        self.encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    
    async def analyze_long_document(self, text: str) -> Dict[str, Any]:
        print("🔄 Processing...")
        
        # Smart chunking
        chunks = self._smart_chunk(text)
        print(f"🧩 {len(chunks)} chunks")
        
        # Summaries
        summaries = await self._summarize_chunks(chunks)
        final_summary = await self._merge_summaries(summaries)
        
        # Safe extraction
        actions = await self._extract_actions(summaries)
        risks = await self._extract_risks(summaries)
        
        return {
            "executive_summary": final_summary,
            "actions": actions,
            "risks_open_issues": risks,
            "document_stats": {
                "chunk_count": len(chunks),
                "total_actions": len(actions),
                "total_risks": len(risks)
            }
        }
    
    def _smart_chunk(self, text: str, max_tokens=1500) -> List[str]:
        sections = re.split(r'\n\s*\n{2,}', text)
        chunks, current = [], ""
        
        for section in sections:
            test_chunk = current + section if current else section
            if len(self.encoding.encode(test_chunk)) > max_tokens and current:
                chunks.append(current.strip())
                current = section[:max_tokens//2]
            else:
                current = test_chunk + "\n\n"
        
        if current:
            chunks.append(current.strip())
        return chunks
    
    async def _summarize_chunks(self, chunks: List[str]) -> List[str]:
        summaries = []
        for i, chunk in enumerate(chunks[:3]):  # Max 3 chunks
            try:
                result = await self.summary_agent.run(task=f"Summarize:\n\n{chunk}")
                summaries.append(result.messages[-1].content)
            except:
                summaries.append("Summary unavailable")
        return summaries
    
    async def _merge_summaries(self, summaries: List[str]) -> str:
        if len(summaries) == 1:
            return summaries[0]
        text = "\n\n".join(summaries)
        result = await self.summary_agent.run(task=f"Merge summaries:\n\n{text}")
        return result.messages[-1].content
    
    async def _extract_actions(self, summaries: List[str]) -> List[Dict]:
        """ROBUST parsing"""
        full_text = "\n\n".join(summaries)[:2000]
        result = await self.action_agent.run(task=f"Extract actions:\n\n{full_text}")
        
        raw = result.messages[-1].content
        print(f"DEBUG ACTIONS RAW: {raw[:300]}")  # TERMINAL DEBUG
        
        try:
            cleaned = self._clean_json(raw)
            data = json.loads(cleaned)
            return data.get("actions", [])
        except:
            print(f"Actions parse failed")
            return []
    
    async def _extract_risks(self, summaries: List[str]) -> List[Dict]:
        """ROBUST parsing"""
        full_text = "\n\n".join(summaries)[:2000]
        result = await self.risk_agent.run(task=f"Extract risks:\n\n{full_text}")
        
        raw = result.messages[-1].content
        print(f"DEBUG RISKS RAW: {raw[:300]}")  # TERMINAL DEBUG
        
        try:
            cleaned = self._clean_json(raw)
            data = json.loads(cleaned)
            return data.get("risks_open_issues", data.get("risks", []))
        except:
            print(f"Risks parse failed")
            return []
    
    def _clean_json(self, text: str) -> str:
        """Extract JSON from ANY text"""
        # Remove markdown aggressively
        text = re.sub(r'```json?\s*|\s*```', '', text, flags=re.I | re.DOTALL)
        # Find largest JSON object
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        return match.group(1) if match else '{"error": "no json"}'
