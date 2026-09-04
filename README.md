# RepoMind

**AI Codebase Intelligence System using Retrieval-Augmented Generation (RAG).**

RepoMind is a production-oriented system that allows users to ask natural-language questions about a software repository and receive answers grounded in the actual codebase.

The system processes a repository, creates code-aware chunks, generates embeddings, stores them in PostgreSQL with pgvector, retrieves relevant code using semantic search, and uses an LLM to generate a grounded answer.

---

## Phase 1 — Minimal RAG

### Objective

Build the first complete end-to-end RAG pipeline for understanding a software repository.

The Phase 1 pipeline is:

```text
Repository ZIP
      ↓
Extract Repository
      ↓
Discover Files
      ↓
Code-Aware Chunking
      ↓
Generate Embeddings
      ↓
PostgreSQL + pgvector
      ↓
Semantic Search
      ↓
Top-K Retrieval
      ↓
LLM
      ↓
Grounded Answer
```

---

## 1. Repository Ingestion

RepoMind will initially accept a repository as a ZIP file.

```text
project.zip
    ↓
Extract
    ↓
Repository Files
```

The system will:

* Accept a ZIP archive
* Extract the repository
* Discover files
* Filter irrelevant files
* Process supported source and documentation files

Tests will initially be treated as regular source files.

Files such as `.git/`, `venv/`, `node_modules/`, cache files, compiled files, and other irrelevant files should not be processed.

---

## 2. Code-Aware Chunking

The repository will not be split using only arbitrary fixed-size text chunks.

RepoMind will use **code-aware chunking**, with AST-based analysis where supported.

The goal is to preserve meaningful code structures such as:

* Functions
* Classes
* Methods
* Routes
* Decorators
* Relevant surrounding context

For example:

```python
@app.get("/users")
def get_users():
    return User.query.all()
```

The route decorator and function should remain together because they represent one meaningful code unit.

Chunks should preserve relevant context when necessary, including:

* Decorators
* SDK usage
* Configuration
* Database interactions
* Middleware
* Related code structures

---

## 3. Chunk Metadata

Every chunk will contain the actual code plus metadata describing its source.

Example:

```text
content:
@app.get("/users")
def get_users():
    return User.query.all()

file_path:
app/routes/users.py

start_line:
12

end_line:
14

chunk_type:
function
```

The metadata will allow RepoMind to:

* Locate the original code
* Understand the chunk's structure
* Generate source citations
* Associate chunks with their files and repository

---

## 4. Database

Phase 1 will use:

```text
PostgreSQL
     +
pgvector
```

The initial conceptual relationship is:

```text
Repository
    │
    └── 1:N ── File
                  │
                  └── 1:N ── Chunk
```

### Repository

Represents an uploaded repository.

Possible information:

* `id`
* `name`
* Repository metadata
* Number of files

### File

Represents a file belonging to a repository.

Possible information:

* `id`
* `repository_id`
* `file_path`
* Number of lines
* Number of classes
* Number of functions
* Number of blocks

### Chunk

Represents a searchable portion of a file.

Core information:

* `id`
* `file_id`
* `content`
* `embedding`
* `start_line`
* `end_line`
* Chunk metadata

The final database schema will be established before implementation.

---

## 5. Embeddings

Each code chunk will be converted into a vector embedding.

```text
Code Chunk
    ↓
Embedding Model
    ↓
Vector
    ↓
PostgreSQL + pgvector
```

The embedding represents the semantic meaning of the chunk and allows similar code concepts to be retrieved.

---

## 6. Semantic Search

When the user asks a question, the query will also be converted into an embedding.

```text
User Question
      ↓
Query Embedding
      ↓
Vector Similarity Search
      ↓
Top-K Relevant Chunks
```

The retrieved chunks will be used as context for the LLM.

Phase 1 uses **semantic search only**.

---

## 7. LLM Generation

The LLM will not receive the entire repository.

Instead:

```text
User Question
      ↓
Semantic Retrieval
      ↓
Relevant Chunks
      ↓
Context
      ↓
LLM
      ↓
Answer
```

The LLM should answer using the retrieved repository context.

It should:

* Ground answers in the retrieved code
* Avoid inventing repository-specific information
* State when the requested information cannot be found
* Reference the relevant source files and lines

---

## 8. Source Citations

Answers should identify where the information came from.

Example:

```text
The GET /users endpoint is defined in:

File: app/routes/users.py
Lines: 12-14
```

Citations will be based on chunk metadata:

```text
file_path
start_line
end_line
```

This makes the generated answer traceable to the original repository.

---

## 9. Not Found Handling

RepoMind should not hallucinate repository information.

If the retrieved repository context does not contain enough information to answer a question, the system should explicitly indicate that the information was not found.

Example:

```text
Question:
"Which payment provider does this project use?"

Answer:
"The repository does not contain enough information to determine this."
```

---

## 10. Phase 1 Scope

### Included

* [x] Project initialization
* [x] Git/GitHub repository
* [x] Python virtual environment
* [ ] ZIP repository ingestion
* [ ] File discovery
* [ ] File filtering
* [ ] Code-aware chunking
* [ ] Chunk metadata
* [ ] PostgreSQL setup
* [ ] pgvector extension
* [ ] Database schema
* [ ] Embedding generation
* [ ] Vector storage
* [ ] Semantic search
* [ ] Top-K retrieval
* [ ] LLM generation
* [ ] Basic source citations
* [ ] Basic not-found handling

### Not Included in Phase 1

* Keyword search
* Hybrid search
* Reranking
* Retrieval evaluation
* Recall@K
* Change-impact analysis
* Git-history reasoning
* Conversation memory
* Advanced agents
* Production deployment
* Advanced observability

---

## 11. Phase 1 Success Criteria

Phase 1 is complete when RepoMind can perform the following end-to-end flow:

```text
project.zip
     ↓
Extract repository
     ↓
Process files
     ↓
Create code-aware chunks
     ↓
Generate embeddings
     ↓
Store chunks + embeddings
     ↓
Receive user question
     ↓
Perform semantic search
     ↓
Retrieve Top-K chunks
     ↓
Send retrieved context to LLM
     ↓
Generate grounded answer
     ↓
Provide file + line references
```

### Example Query

```text
"Where are the GET API endpoints defined?"
```

Expected behavior:

```text
1. Convert the question into an embedding
2. Search the stored code chunks
3. Retrieve the most relevant chunks
4. Give those chunks to the LLM
5. Generate an answer based on the retrieved code
6. Include file paths and line ranges
```

---

## 12. Initial Technology Stack

```text
Python
PostgreSQL
pgvector
SQLAlchemy
Sentence Transformers
LLM API
```

---

## 13. Initial Project Structure

```text
RepoMind/
├── README.md
├── main.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── venv/
```

`venv/` is a local development environment and is ignored by Git.

---

## Phase 1 Goal

Build a **minimal but complete RAG pipeline for codebases**:

```text
ZIP → Files → Code Chunks → Embeddings → PostgreSQL/pgvector
                                      ↓
                                  Semantic Search
                                      ↓
                                  Top-K Chunks
                                      ↓
                                     LLM
                                      ↓
                              Grounded Answer
```

The priority of Phase 1 is to establish a correct and understandable foundation before adding more advanced retrieval and engineering capabilities.
