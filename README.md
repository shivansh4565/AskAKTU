# AKTU B.Tech Chatbot Workflow (Conditional RAG)

## Scenario

Suppose a college affiliated with **Dr. A.P.J. Abdul Kalam Technical University (AKTU)** offers a **B.Tech** program.

Students can access an AI-powered chatbot to ask questions related to academics, fees, university regulations, and general technical concepts.

Since the Large Language Model (LLM) does not have knowledge of the college-specific or AKTU-specific curriculum, regulations, and fee structure, the chatbot uses **Retrieval-Augmented Generation (RAG)** with dedicated PDF knowledge bases.

---

# Knowledge Base

## 1. AKTU Academic PDF

Contains information such as:

- Semester-wise syllabus
- Subjects
- Curriculum (2023/2024 Scheme)
- Credit structure
- Academic calendar
- Examination pattern
- Internal & external marking scheme
- Attendance rules
- Eligibility criteria
- Carry-over rules
- University regulations

---

## 2. College Fee PDF

Contains information such as:

- Tuition fee
- Admission fee
- Examination fee
- Hostel fee
- Scholarship details
- Payment schedule
- Refund policy

---

# Conditional Workflow

The chatbot classifies the user's query and routes it to the appropriate knowledge source.

---

## Path 1: Academic Questions (RAG)

Questions related to AKTU academics are answered using the **Academic PDF**.

### Examples

- What is the syllabus of Data Structures?
- Which subjects are there in 4th Semester?
- What are the credits for Operating Systems?
- What is the passing criteria in AKTU?
- What is the attendance requirement?
- What is the examination pattern?

---

## Path 2: Fee-Related Questions (RAG)

Questions related to college fees are answered using the **Fee PDF**.

### Examples

- What is the tuition fee for B.Tech?
- What is the hostel fee?
- What is the examination fee?
- Is there any scholarship available?
- What is the refund policy?

---

## Path 3: General Questions (LLM)

General technical questions that do not require AKTU documents are answered directly by the LLM.

### Examples

- What is Artificial Intelligence?
- Explain Machine Learning.
- What is DBMS?
- Explain Operating Systems.
- How should I prepare for placements?
- What is Cloud Computing?

---

# Workflow Diagram

```text
                Student Opens
            AKTU B.Tech Chatbot
                     │
                     ▼
             User Asks Question
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
 Academic Query  Fee Query  General Query
        │            │            │
        ▼            ▼            ▼
 AKTU Academic   College Fee      LLM
      PDF            PDF     General Knowledge
      (RAG)         (RAG)
        └────────────┼────────────┘
                     ▼
              Final Response
```

---

# Technologies Used

- **LangGraph** – Workflow orchestration
- **LangChain** – RAG pipeline
- **ChromaDB** – Vector database
- **Google Gemini / Mistral** – LLM
- **HuggingFace Embeddings** – Text embeddings
- **PyPDFLoader** – PDF loading
- **RecursiveCharacterTextSplitter** – Document chunking
- **Streamlit** – User Interface

---

# Summary

The chatbot intelligently routes every user query through a conditional workflow:

1. **Academic Questions** → AKTU Academic PDF (RAG)
2. **Fee-Related Questions** → College Fee PDF (RAG)
3. **General Technical Questions** → LLM Knowledge

This architecture ensures that students receive accurate, context-aware, and reliable answers while leveraging both institutional documents and the reasoning capabilities of modern Large Language Models.# AKTU B.Tech Chatbot Workflow (Conditional RAG)

## Scenario

Suppose a college affiliated with **Dr. A.P.J. Abdul Kalam Technical University (AKTU)** offers a **B.Tech** program.

Students can access an AI-powered chatbot to ask questions related to academics, fees, university regulations, and general technical concepts.

Since the Large Language Model (LLM) does not have knowledge of the college-specific or AKTU-specific curriculum, regulations, and fee structure, the chatbot uses **Retrieval-Augmented Generation (RAG)** with dedicated PDF knowledge bases.

---

# Knowledge Base

## 1. AKTU Academic PDF

Contains information such as:

- Semester-wise syllabus
- Subjects
- Curriculum (2023/2024 Scheme)
- Credit structure
- Academic calendar
- Examination pattern
- Internal & external marking scheme
- Attendance rules
- Eligibility criteria
- Carry-over rules
- University regulations

---

## 2. College Fee PDF

Contains information such as:

- Tuition fee
- Admission fee
- Examination fee
- Hostel fee
- Scholarship details
- Payment schedule
- Refund policy

---

# Conditional Workflow

The chatbot classifies the user's query and routes it to the appropriate knowledge source.

---

## Path 1: Academic Questions (RAG)

Questions related to AKTU academics are answered using the **Academic PDF**.

### Examples

- What is the syllabus of Data Structures?
- Which subjects are there in 4th Semester?
- What are the credits for Operating Systems?
- What is the passing criteria in AKTU?
- What is the attendance requirement?
- What is the examination pattern?

---

## Path 2: Fee-Related Questions (RAG)

Questions related to college fees are answered using the **Fee PDF**.

### Examples

- What is the tuition fee for B.Tech?
- What is the hostel fee?
- What is the examination fee?
- Is there any scholarship available?
- What is the refund policy?

---

## Path 3: General Questions (LLM)

General technical questions that do not require AKTU documents are answered directly by the LLM.

### Examples

- What is Artificial Intelligence?
- Explain Machine Learning.
- What is DBMS?
- Explain Operating Systems.
- How should I prepare for placements?
- What is Cloud Computing?

---

# Workflow Diagram

```text
                Student Opens
            AKTU B.Tech Chatbot
                     │
                     ▼
             User Asks Question
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
 Academic Query  Fee Query  General Query
        │            │            │
        ▼            ▼            ▼
 AKTU Academic   College Fee      LLM
      PDF            PDF     General Knowledge
      (RAG)         (RAG)
        └────────────┼────────────┘
                     ▼
              Final Response
```

---

# Technologies Used

- **LangGraph** – Workflow orchestration
- **LangChain** – RAG pipeline
- **ChromaDB** – Vector database
- **Google Gemini / Mistral** – LLM
- **HuggingFace Embeddings** – Text embeddings
- **PyPDFLoader** – PDF loading
- **RecursiveCharacterTextSplitter** – Document chunking
- **Streamlit** – User Interface

---

# Summary

The chatbot intelligently routes every user query through a conditional workflow:

1. **Academic Questions** → AKTU Academic PDF (RAG)
2. **Fee-Related Questions** → College Fee PDF (RAG)
3. **General Technical Questions** → LLM Knowledge

This architecture ensures that students receive accurate, context-aware, and reliable answers while leveraging both institutional documents and the reasoning capabilities of modern Large Language Models.