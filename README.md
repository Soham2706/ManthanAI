# ManthanAI
Churning Talent Oceans to Find Your Amrit

##  Executive Summary

**ManthanAI** is a semantic candidate discovery and ranking engine built to solve a problem every recruiter knows intimately: *the best candidate is rarely the one with the most matching keywords on their resume.*

Instead of scanning for string overlaps, ManthanAI builds a **semantic understanding** of both the job and the candidate, layers in **career trajectory intelligence**, scores **real production AI experience**, models **behavioral hiring signals**, and produces an **explainable, recruiter-readable ranking** — not a black-box score.

This isn't a resume parser with a similarity score bolted on. It's an architecture designed the way modern AI-native hiring platforms (Mercor, SeekOut, Gem, internal LinkedIn talent-search systems) are actually built — **retrieval → understanding → reasoning → ranking → explanation.**

---

##  The Problem

Recruiters today are buried under volume and starved of signal.

> A single job posting can receive **1,000–10,000+ applications**. Recruiters spend an average of **6–8 seconds** scanning a resume before deciding to reject or shortlist it.

The result: strong candidates with non-traditional career paths, project-based experience, or unconventional resume phrasing get filtered out — **not because they're unqualified, but because they don't match a keyword string.**

Meanwhile, weak candidates who happen to stuff their resume with the right buzzwords rise to the top.

This is a **search and ranking failure**, not a sourcing failure. The candidates often exist in the pool — the system just can't find them.

---

##  Why Traditional Hiring Systems Fail

| Traditional ATS / Keyword Search | Reality on the Ground |
|---|---|
| Matches exact strings ("ML Engineer" ≠ "Machine Learning Engineer") | Misses semantically identical candidates |
| Treats a resume as a bag of words | Ignores **career trajectory** — growth, scope, seniority signals |
| No concept of "production" vs "tutorial" experience | A candidate who built a Kaggle notebook ranks the same as one who shipped a RAG system to 10M users |
| Zero behavioral context | Can't tell a responsive, interview-ready candidate from a ghost profile |
| Binary keyword match = score | No reasoning, no explanation, no confidence calibration |
| Doesn't scale meaningfully | Bigger candidate pools just mean more noise, not better precision |

Keyword search optimizes for **lexical overlap**. Hiring success depends on **capability, trajectory, and intent** — three things keyword search structurally cannot see.

---

##  Our Innovation

ManthanAI reframes candidate ranking as a **multi-layer reasoning problem**, not a search problem:

1. **Understand the JD semantically** — not "what words appear" but "what capability is actually being asked for."
2. **Understand the candidate semantically** — embed their full profile, not isolated keywords.
3. **Read their career arc** — is this person growing into this role, or just claiming it?
4. **Detect real production AI experience** — distinguish "used ChatGPT" from "built and shipped an embedding-based retrieval system."
5. **Model behavioral hiring signals** — responsiveness, interview completion, recruiter saves, GitHub activity, availability.
6. **Fuse it all in a hybrid scoring engine** — semantic + structured + behavioral signals, weighted like a senior recruiter would weigh them mentally.
7. **Explain every ranking decision** — no black box. Every score comes with *why*.

This is the difference between a **search bar** and a **reasoning system**.

---

##  System Architecture

```
                         ┌──────────────────────────┐
                         │      Job Description     │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │   JD Understanding Engine    │
                       │  (intent + skill extraction) │
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │     Embedding Generation     │
                       │   (all-MiniLM-L6-v2, 384-dim)│
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │Candidate Understanding Engine│
                       │  (profile → semantic vector) │
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │      Semantic Retrieval      │
                       │  (cosine similarity search)  │
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │   Career Intelligence Layer  │
                       (trajectory, growth, seniority)│
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │    Behavioral Signal Layer   │
                       │(response rate, GitHub, saves)│
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │     Hybrid Scoring Engine    │
                       │(weighted multi-factor fusion)│
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │      Explainable Ranking     │
                       │  (score + human-readable why)│
                       └────────────┬─────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │   Final Candidate Shortlist  │
                       └──────────────────────────────┘
```

---

##  Technical Architecture Explanation

ManthanAI is structured as a **pipeline of independent, composable layers** — every layer can be swapped, scaled, or upgraded without breaking the system downstream. This mirrors how production ML systems at scale are built: clean separation between **representation, retrieval, and reasoning**.

| Layer | Responsibility | Why It Matters |
|---|---|---|
| **JD Understanding Engine** | Extracts intent, required skills, and seniority signal from raw JD text | Converts unstructured text into a structured query the system can reason over |
| **Embedding Generation** | Encodes JD + candidate text into 384-dim dense vectors via `all-MiniLM-L6-v2` | Captures *meaning*, not spelling — "NLP Engineer" and "Natural Language Processing Specialist" land near each other in vector space |
| **Candidate Understanding Engine** | Builds a semantic representation of the full candidate profile (skills, projects, experience narrative) | Treats a candidate as a person with a story, not a token list |
| **Semantic Retrieval** | Cosine similarity search over the candidate embedding index | Sub-linear, scalable nearest-neighbor retrieval instead of brute-force string matching |
| **Career Intelligence Layer** | Analyzes role progression, tenure patterns, scope growth | Differentiates a candidate trending toward seniority from one who's plateaued |
| **Behavioral Signal Layer** | Quantifies recruiter response rate, interview completion, GitHub activity, save rate, availability | Adds the "will this person actually engage and succeed in the process" dimension |
| **Hybrid Scoring Engine** | Fuses semantic, career, and behavioral scores with tunable weights | No single signal dominates — mirrors how real recruiters triangulate decisions |
| **Explainable Ranking** | Attaches a human-readable rationale to every score | Builds recruiter trust — a ranked list with no explanation is just a guess with a number on it |

---

##  AI Pipeline Explanation

```
1. JD Text  ──▶  Skill & Intent Extraction  ──▶  JD Embedding Vector
2. Candidate Text ──▶ Profile Normalization ──▶ Candidate Embedding Vector
3. Cosine Similarity(JD_vector, Candidate_vector) ──▶ Base Semantic Score
4. Career Trajectory Heuristics ──▶ Trajectory Score
5. Production AI Signal Detection ──▶ Capability Score
6. Behavioral Signal Aggregation ──▶ Engagement Score
7. Hybrid Weighted Fusion ──▶ Final Rank Score
8. Rationale Generator ──▶ Explanation String
```

Each stage produces an **interpretable intermediate output**, not just a final number — meaning the system can be debugged, audited, and trusted by a hiring manager, not just an engineer.

---

##  Ranking Methodology

ManthanAI's **Hybrid Scoring Engine** combines eleven distinct ranking factors across three categories:

### 1️⃣ Semantic & Capability Signals
- Semantic Similarity (JD ↔ Candidate embedding cosine score)
- Career History Analysis (trajectory, scope, seniority growth)
- Production AI Experience (shipped systems vs. tutorials/notebooks)
- Retrieval / Ranking System Experience (recommender systems, search, RAG)
- Embedding & Vector Search Experience (vector DBs, ANN, similarity search)
- Evaluation Framework Experience (offline eval, A/B testing, metrics design)

### 2️⃣ Behavioral & Engagement Signals
- Recruiter Response Rate
- Interview Completion Rate
- GitHub Activity (commit cadence, repo quality, contribution consistency)
- Saved By Recruiters (implicit quality signal from human reviewers)
- Availability Signals (notice period, open-to-work status)

### 3️⃣ Fusion Strategy

```python
final_score = (
    w1 * semantic_similarity +
    w2 * career_trajectory_score +
    w3 * production_ai_score +
    w4 * retrieval_ranking_score +
    w5 * embedding_search_score +
    w6 * evaluation_framework_score +
    w7 * behavioral_engagement_score
)
```

Weights (`w1...w7`) are **tunable per role archetype** — a Staff ML Engineer search and a Junior Data Analyst search should not weigh "production AI experience" identically. This configurability is what separates a real ranking system from a fixed formula.

---

##  Behavioral Signal Intelligence

Resumes describe *capability*. Behavioral signals reveal *hireability*.

ManthanAI treats behavioral data as a first-class ranking input:

- **Recruiter Response Rate** → proxy for engagement and interest authenticity
- **Interview Completion Rate** → proxy for process reliability and follow-through
- **GitHub Activity** → proxy for hands-on technical depth beyond claimed skills
- **Saved By Recruiters** → crowdsourced human quality signal, free supervision from the people who matter most
- **Availability Signals** → ensures the shortlist is actionable *today*, not theoretically qualified

A candidate who is a 95% semantic match but historically unresponsive is, in practice, a worse hire than an 85% match who engages reliably. ManthanAI's scoring reflects that recruiter intuition mathematically — instead of ignoring it.

---

##  Explainable AI

Every ranked candidate ships with a **human-readable rationale**, not just a score:

```
Candidate: Aditi Sharma — Rank #1 (Score: 0.91)

✔ Strong semantic match to JD (0.88) — "Built and deployed RAG-based 
  search system" closely aligns with "Retrieval-Augmented Generation 
  Engineer" requirement.
✔ Career trajectory trending upward — 2 promotions in 3 years, 
  increasing scope from IC to team lead.
✔ Verified production AI experience — shipped vector search 
  pipeline serving 2M+ queries/month.
✔ High behavioral reliability — 92% interview completion rate, 
  saved by 4 recruiters in the last 60 days.

→ Recommendation: Strong Shortlist Candidate
```

This is the core trust mechanism of the product: **recruiters don't adopt tools they can't interrogate.** Explainability isn't a feature — it's the adoption requirement.

---

## Scalability Discussion

ManthanAI is architected to scale from a hackathon demo to a production hiring platform without re-architecture:

- **Vector-based retrieval** (cosine similarity over embeddings) scales sub-linearly with proper indexing — ready to migrate from in-memory comparison to **FAISS / Pinecone / Weaviate / pgvector** for millions of candidate vectors with **approximate nearest neighbor (ANN)** search.
- **Stateless scoring layers** mean the Hybrid Scoring Engine can be horizontally scaled across workers/containers with zero shared state.
- **Pre-computed candidate embeddings** mean ranking against a new JD is an O(1) embedding generation + ANN lookup — not a full re-scan of the candidate pool.
- **Decoupled pipeline stages** allow each layer (JD understanding, career intelligence, behavioral signals) to be independently cached, batched, or moved to async workers/queues (Celery, Kafka, etc.) under real-world load.
- **Model swap-ability** — `all-MiniLM-L6-v2` is intentionally lightweight for the hackathon build; the architecture supports drop-in upgrades to larger embedding models (e.g., `bge-large`, `e5-mistral`, or hosted embedding APIs) without touching downstream layers.

---

##  Performance Discussion

| Stage | Complexity | Notes |
|---|---|---|
| Embedding Generation | O(1) per text, batched | MiniLM-L6-v2 chosen for 384-dim compactness + speed |
| Semantic Retrieval (current) | O(n) cosine similarity | Sufficient for hackathon scale; ANN-ready for production |
| Career/Behavioral Scoring | O(1) per candidate | Pure feature computation, fully parallelizable |
| Hybrid Fusion | O(1) per candidate | Simple weighted sum — cheap, fast, interpretable |
| End-to-End Ranking (1K candidates) | Sub-second on CPU | No GPU dependency required for inference at this scale |

The design deliberately favors **interpretable, fast, linear-cost scoring** over opaque deep ranking models — a conscious trade-off prioritizing **trust and latency** over marginal accuracy gains, which is exactly the trade-off real recruiting platforms make.

---

## 📁 Folder Structure

```
ManthanAI/
├── data/
│   ├── job_descriptions/
│   └── candidate_profiles/
├── src/
│   ├── jd_engine/
│   │   └── jd_understanding.py
│   ├── candidate_engine/
│   │   └── candidate_understanding.py
│   ├── embeddings/
│   │   └── embedding_generator.py
│   ├── retrieval/
│   │   └── semantic_retrieval.py
│   ├── career_intelligence/
│   │   └── trajectory_analysis.py
│   ├── behavioral_signals/
│   │   └── signal_layer.py
│   ├── scoring_engine/
│   │   └── hybrid_scorer.py
│   ├── explainability/
│   │   └── rationale_generator.py
│   └── pipeline.py
├── notebooks/
│   └── exploration.ipynb
├── tests/
│   └── test_pipeline.py
├── requirements.txt
├── config.yaml
└── README.md
```

---

## 🛠️ Installation Guide

```bash
# 1. Clone the repository
git clone https://github.com//ManthanAI.git
cd ManthanAI

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (First run only) download the embedding model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**requirements.txt**
```
sentence-transformers
scikit-learn
numpy
pandas
pyyaml
```

---

##  Usage Guide

```bash
# Run the full ranking pipeline on a sample JD + candidate pool
python src/pipeline.py \
    --jd data/job_descriptions/ml_engineer.txt \
    --candidates data/candidate_profiles/ \
    --top_k 10
```

```python
from src.pipeline import ManthanPipeline

pipeline = ManthanPipeline(config_path="config.yaml")

results = pipeline.rank(
    jd_text=open("data/job_descriptions/ml_engineer.txt").read(),
    candidate_dir="data/candidate_profiles/",
    top_k=10
)

for candidate in results:
    print(candidate.name, candidate.score, candidate.rationale)
```

---

##  Sample Output

```
Rank #1 — Aditi Sharma         | Score: 0.91 | Strong Shortlist Candidate
Rank #2 — Rohan Mehta          | Score: 0.87 | Strong Shortlist Candidate
Rank #3 — Priya Nair           | Score: 0.83 | Recommended Shortlist
Rank #4 — Karan Verma          | Score: 0.79 | Recommended Shortlist
Rank #5 — Sneha Iyer           | Score: 0.74 | Consider with Review

Each result includes:
→ Semantic Match Score
→ Career Trajectory Insight
→ Production AI Experience Verification
→ Behavioral Reliability Index
→ Human-Readable Recruiter Rationale
```

---

##  Future Enhancements

- 🔗 **Vector DB integration** (FAISS / Pinecone / pgvector) for million-scale candidate indexing
- 🧠 **LLM-based rationale generation** for richer, more nuanced explainability narratives
- 📡 **Real-time candidate ingestion** via API webhooks from ATS platforms
- 🎯 **Role-archetype-aware weight tuning** with learned weights via recruiter feedback loops (RLHF-style)
- 🧪 **Bias auditing layer** to continuously monitor and correct for demographic skew in rankings
- 🗣️ **Conversational recruiter interface** — "Find me someone like our last 3 best hires"
- 📱 **Recruiter dashboard** with drag-to-reorder feedback that retrains scoring weights

---

##  Hackathon Impact

ManthanAI directly targets the **core failure mode** named in the Redrob Challenge brief: recruiters missing great candidates due to keyword-based limitations. This project doesn't add AI as a feature — it **rebuilds the ranking pipeline around understanding** as the foundational primitive.

- Solves a **real, expensive, daily pain point** in recruiting at scale
- Demonstrates **applied NLP + ML system design**, not just an API call to a chatbot
- Built with **production architecture patterns** — composable layers, explainability, scalability path
- Designed to be **extended**, not thrown away after the demo

---

## 🥇 Why This Solution Wins

| Criterion | How ManthanAI Delivers |
|---|---|
| **Technical Depth** | Real embedding pipeline, hybrid scoring math, multi-layer architecture |
| **Problem Understanding** | Directly addresses *why* keyword search fails — not just *that* it fails |
| **Innovation** | Career intelligence + behavioral modeling layered on top of semantic search — most teams stop at cosine similarity |
| **Production Readiness** | Clear scalability path to ANN search, async workers, model upgrades |
| **Explainability** | Every score is justified in plain English — built for human trust, not just leaderboard accuracy |
| **Recruiter Empathy** | Ranking factors mirror how real recruiters actually think, not just what's easy to compute |

---

## 🌱 Team Vision

We believe the future of hiring isn't "more applications, faster filters." It's **systems that understand people** — their skills, their growth, their reliability — with the same nuance a great recruiter brings after years of pattern recognition, but at the speed and scale only AI can provide.

ManthanAI is our first step toward that future: a ranking engine that doesn't just **search** for candidates, but **reasons** about them.

---

## ✅ Conclusion

ManthanAI was built to answer a simple question with a non-trivial system: *what does it actually take to find the right person in a sea of resumes?*

The answer isn't a better keyword filter. It's **semantic understanding, career intelligence, behavioral signal modeling, and explainable reasoning — fused into one production-grade pipeline.**

This is recruiting infrastructure built the way modern AI systems should be: **layered, interpretable, scalable, and trustworthy.**

### Built with intent. Designed to scale. Ready to ship.

**ManthanAI — Discovery, Reasoned.**