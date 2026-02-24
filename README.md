# Agentic AI Orchestrator

A multi-agent Agentic AI system for structured document intelligence.

This project demonstrates role-specialized autonomous agents coordinated through a central orchestration layer to extract:

- Executive Summary  
- Action Items (Owner, Department, Deadline)  
- Risks & Open Issues  

---

##  Agentic Architecture

The system follows a modular multi-agent design:

### 🔹 Orchestrator
- Splits long documents  
- Coordinates specialized agents  
- Aggregates structured outputs  
- Enforces schema validation  

### 🔹 Summary Agent
- Context-aware summarization  
- Preserves decisions and constraints  
- Handles long-document chunking  

### 🔹 Action Extraction Agent
- Extracts atomic task assignments  
- Captures owner, department, deadline  
- Prevents aggregation drift  
- Focuses on accountability  

### 🔹 Risk & Issues Agent
- Identifies unresolved risks  
- Detects compliance gaps  
- Flags operational concerns  

---

##  System Flow

            Document Input
                  |
                  v
           +--------------+
           | Orchestrator |
           +------+-------+
                  |
  -------------------------------------
  |                |                 |

+--------------+ +--------------+ +--------------+
| Summary | | Action | | Risk & |
| Agent | | Agent | | Issues Agent |
+--------------+ +--------------+ +--------------+
| | |
----------- Structured JSON Output ----------


---

##  Tech Stack

- Python  
- AutoGen (Multi-Agent Framework)  
- LLM-based Structured Extraction  
- Streamlit UI  
- JSON Schema Enforcement  

---

##  Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
 Key Agentic Concepts Implemented

Role-based agent specialization

Structured JSON-only outputs

Deterministic post-processing

Long-document chunking

Multi-agent orchestration

Accountability-focused extraction

 Future Improvements

Inter-agent memory

Dependency extraction

Confidence scoring

Evaluation metrics

Agent-to-agent reasoning