"""
tasks.py — HR Interview Tasks (Easy / Medium / Hard)
Each task defines: question, candidate_answer, expected_score, keywords, difficulty
"""

TASKS = [
    # ─────────────────────────────────────────────
    # 🟢 TASK 1 — Easy: Basic factual question
    # ─────────────────────────────────────────────
    {
        "id": 1,
        "difficulty": "easy",
        "question": "What is Python?",
        "answer": (
            "Python is a high-level, interpreted programming language known for its "
            "simple and readable syntax. It supports multiple programming paradigms "
            "including procedural, object-oriented, and functional programming. "
            "Python is widely used in web development, data science, automation, "
            "and artificial intelligence."
        ),
        "expected_score": 0.85,
        "keywords": ["programming language", "interpreted", "syntax", "object-oriented",
                     "data science", "high-level", "automation"],
        "rubric": {
            "keyword_weight": 0.50,
            "explanation_weight": 0.30,
            "clarity_weight": 0.20,
        },
    },

    # ─────────────────────────────────────────────
    # 🟡 TASK 2 — Medium: Concept explanation
    # ─────────────────────────────────────────────
    {
        "id": 2,
        "difficulty": "medium",
        "question": "Explain Machine Learning.",
        "answer": (
            "Machine Learning is a subset of Artificial Intelligence that enables "
            "systems to learn and improve from experience without being explicitly "
            "programmed. It focuses on building algorithms that can access data and "
            "use it to learn for themselves. There are three main types: supervised "
            "learning, unsupervised learning, and reinforcement learning. ML is used "
            "in applications like recommendation systems, image recognition, and "
            "natural language processing."
        ),
        "expected_score": 0.90,
        "keywords": ["subset", "artificial intelligence", "algorithms", "supervised",
                     "unsupervised", "reinforcement", "data", "learn", "model"],
        "rubric": {
            "keyword_weight": 0.50,
            "explanation_weight": 0.30,
            "clarity_weight": 0.20,
        },
    },

    # ─────────────────────────────────────────────
    # 🔴 TASK 3 — Hard: Real interview project answer
    # ─────────────────────────────────────────────
    {
        "id": 3,
        "difficulty": "hard",
        "question": "Describe a challenging project you worked on and how you handled it.",
        "answer": (
            "I led the development of a real-time fraud detection system for an "
            "e-commerce platform handling over 500,000 daily transactions. The main "
            "challenge was achieving low-latency decisions (under 100ms) while "
            "maintaining high accuracy. I designed a microservices architecture using "
            "Python and Kafka for event streaming. I implemented an ensemble ML model "
            "combining gradient boosting and neural networks, trained on 2 years of "
            "labeled transaction data. I collaborated with the data engineering team "
            "to build a feature store and set up automated retraining pipelines. "
            "The result was a 40% reduction in fraudulent transactions and a 99.8% "
            "system uptime over six months. I also mentored two junior engineers "
            "throughout the project, conducting weekly code reviews and knowledge "
            "sharing sessions."
        ),
        "expected_score": 0.92,
        "keywords": ["challenge", "architecture", "team", "result", "impact",
                     "design", "implement", "collaborate", "mentor", "pipeline",
                     "metric", "performance", "solution"],
        "rubric": {
            "keyword_weight": 0.40,
            "explanation_weight": 0.35,
            "clarity_weight": 0.25,
        },
    },
]
