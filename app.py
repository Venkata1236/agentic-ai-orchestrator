import streamlit as st
import asyncio
import json
from pathlib import Path
from orchestrator import DocumentAnalyzer

st.set_page_config(page_title="DocAI Pro", layout="wide")

st.title("🤖 Document Intelligence Pro")
st.markdown("*Extracts Actions + Risks from ANY document*")

uploaded_file = st.file_uploader("📁 Upload", type=['txt','pdf','docx'])

if uploaded_file:
    col1, col2 = st.columns(2)
    col1.metric("📄 File", uploaded_file.name)
    col2.metric("📏 Chars", f"{len(uploaded_file.getvalue()):,}")
    
    if st.button("🚀 ANALYZE", type="primary"):
        with st.spinner("🤖 Processing..."):
            text = uploaded_file.read().decode('utf-8', errors='ignore')
            
            async def analyze():
                analyzer = DocumentAnalyzer()
                return await analyzer.analyze_long_document(text)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(analyze())
            
            # METRICS
            col1, col2, col3 = st.columns(3)
            col1.metric("📊 Actions", len(result.get("actions", [])))
            col2.metric("⚠️ Risks", len(result.get("risks_open_issues", [])))
            col3.metric("🧩 Analyzed", result.get("document_stats", {}).get("chunk_count", 0))
            
            # SUMMARY
            st.markdown("---")
            st.subheader("📋 Executive Summary")
            st.markdown(result.get("executive_summary", ""))
            
            # ACTIONS TABLE
            st.markdown("---")
            st.subheader("📊 Action Items")
            actions = result.get("actions", [])
            if actions:
                table_actions = []
                for i, action in enumerate(actions, 1):
                    table_actions.append({
                        "ID": action.get("id", f"A{i}"),
                        "Task": action.get("description", ""),
                        "Owner": action.get("owner", "TBD"),
                        "Deadline": action.get("deadline", "TBD"),
                        "Priority": action.get("priority", "Medium")
                    })
                st.dataframe(table_actions, use_container_width=True)
            else:
                st.info("No actions found")
            
            # RISKS TABLE
            st.markdown("---")
            st.subheader("⚠️ Risks & Issues")
            risks = result.get("risks_open_issues", [])
            if risks:
                table_risks = []
                for i, risk in enumerate(risks, 1):
                    table_risks.append({
                        "ID": risk.get("id", f"R{i}"),
                        "Risk": risk.get("description", ""),
                        "Impact": risk.get("impact", "Medium")
                    })
                st.dataframe(table_risks, use_container_width=True)
            else:
                st.success("No risks detected")
            
            # DOWNLOAD
            st.download_button(
                "💾 Export JSON",
                json.dumps(result, indent=2),
                f"{Path(uploaded_file.name).stem}_report.json"
            )
