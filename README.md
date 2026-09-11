# RepoMind

**AI Codebase Intelligence System using Retrieval-Augmented Generation (RAG).**

RepoMind is an AI-powered system for understanding software repositories through natural-language questions.

It ingests a repository, analyzes its source code, creates code-aware chunks and embeddings, stores them in PostgreSQL with pgvector, retrieves relevant code using hybrid search and reranking, and generates grounded answers with source citations.

---

## Overview

RepoMind is designed to help developers understand unfamiliar codebases by combining code-aware retrieval with large language models.

### High-Level Architecture

```text
GitHub Repository
       │
       ▼
Repository Loader
       │
       ▼
File Discovery & Filtering
       │
       ▼
Code-Aware Chunking
       │
       ▼
Embedding Generation
       │
       ▼
PostgreSQL + pgvector
       │
       ▼
   User Question
       │
       ▼
   Query Routing
       │
       ├──────────────┐
       ▼              ▼
Semantic Search   Keyword Search
       │              │
       └──────┬───────┘
              ▼
       Hybrid Search
            (RRF)
              │
              ▼
         Reranking
              │
              ▼
       Context Builder
              │
              ▼
          Gemini LLM
              │
              ▼
   Grounded Answer + Citations