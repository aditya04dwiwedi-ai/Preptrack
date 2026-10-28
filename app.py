"""
Placement Preparation & Tracking System
AKTU Mini Project - B.Tech CSE (AIML) - Session 2026-27
Student: Aditya Dwivedi (Roll No: 2501721530006)
Department of Computer Science & Engineering
Lloyd Institute of Engineering & Technology, Greater Noida
Affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow

Backend: Flask Web Framework (Python)
Runtime Data Storage: Python variables and lists/dictionaries
"""

import copy
import random
import time

from flask import Flask, render_template, request, jsonify

import datasets as ds

app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------------------------------------------------------------------------
# INITIAL RUNTIME DATA STRUCTURES (Stored in Python variables as per synopsis)
# ---------------------------------------------------------------------------

DEFAULT_STUDENT = {
    "name": "Aditya Dwivedi",
    "roll_no": "2501721530006",
    "branch": "Computer Science & Engineering – AIML",
    "section": "2H",
    "college": "Lloyd Institute of Engineering & Technology",
    "university": "Dr. A.P.J. Abdul Kalam Technical University",
    "cgpa": 8.2,
    "guide": "Mr. Abhishek Suraj(Assistant_Professor, CSE Dept.)"
}

DEFAULT_SUBJECTS = {
    "Python": 70,
    "C": 55,
    "DSA": 42,      # < 50% -> triggers Weak Area Finder
    "DBMS": 60,
    "Aptitude": 35   # < 50% -> triggers Weak Area Finder
}

DEFAULT_COMPANIES = [
    {
        "id": 1,
        "company": "TCS",
        "role": "Graduate Trainee",
        "status": "Interested",
        "package_ctc": "3.6 LPA",
        "notes": "National Qualifier Test (NQT) coming up next month."
    },
    {
        "id": 2,
        "company": "Infosys",
        "role": "Systems Engineer",
        "status": "Applied",
        "package_ctc": "4.0 LPA",
        "notes": "Submitted application through college placement drive."
    },
    {
        "id": 3,
        "company": "Wipro",
        "role": "Project Engineer",
        "status": "Shortlisted",
        "package_ctc": "4.5 LPA",
        "notes": "Online assessment cleared. Awaiting technical round."
    },
    {
        "id": 4,
        "company": "Amazon",
        "role": "Software Development Engineer (Intern)",
        "status": "Interview",
        "package_ctc": "18.0 LPA",
        "notes": "Coding round cleared. Technical interview scheduled for Friday."
    }
]

DEFAULT_GOALS = [
    {"id": 1, "text": "Practice 10 Python coding problems", "completed": True},
    {"id": 2, "text": "Revise DBMS Normalization (1NF to BCNF)", "completed": False},
    {"id": 3, "text": "Solve 5 LeetCode Linked List & Tree problems", "completed": False},
    {"id": 4, "text": "Attempt 1 Aptitude speed mock test (Time & Work)", "completed": False}
]

# Extended sample data (additive): 4 more pipeline rows and 4 more daily goals.
DEFAULT_COMPANIES.extend(ds.EXTRA_DEFAULT_COMPANIES)
for _goal in DEFAULT_GOALS:
    _goal.update(ds.GOAL_META.get(_goal["id"], {}))
DEFAULT_GOALS.extend(ds.EXTRA_DEFAULT_GOALS)

# ---------------------------------------------------------------------------
# PLACEMENT MOCK TEST QUESTIONS
# Core 5 questions covering HTML, FIFO, Python comments, SQL, and LIFO
# (Directly specified in the Project Synopsis page 3)
# ---------------------------------------------------------------------------

SYNOPSIS_MOCK_QUESTIONS = [
    {
        "id": "syn_html",
        "concept": "HTML",
        "question": "Which HTML tag is used to create a hyperlink?",
        "options": ["<a>", "<link>", "<href>", "<anchor>"],
        "answer": 0,
        "explanation": "The <a> (anchor) tag in HTML creates hyperlinks to other web pages, files, locations, or URLs using the 'href' attribute."
    },
    {
        "id": "syn_fifo",
        "concept": "FIFO",
        "question": "Which data structure follows the First-In, First-Out (FIFO) principle?",
        "options": ["Stack", "Queue", "Binary Search Tree", "Max Heap"],
        "answer": 1,
        "explanation": "A Queue operates on the FIFO (First-In, First-Out) principle, meaning the earliest element inserted is the first to be dequeued."
    },
    {
        "id": "syn_py_comment",
        "concept": "Python comments",
        "question": "Which symbol is used for writing a single-line comment in Python?",
        "options": ["//", "/*", "#", "<!--"],
        "answer": 2,
        "explanation": "In Python, the hash symbol (#) marks the start of a single-line comment. Any characters following # on that line are ignored by Python's interpreter."
    },
    {
        "id": "syn_sql",
        "concept": "SQL",
        "question": "Which SQL statement is used to retrieve data from a database table?",
        "options": ["GET", "EXTRACT", "SELECT", "FETCH"],
        "answer": 2,
        "explanation": "The SELECT statement in SQL is used to query and extract records from one or more tables in a relational database."
    },
    {
        "id": "syn_lifo",
        "concept": "LIFO",
        "question": "Which data structure follows the Last-In, First-Out (LIFO) principle?",
        "options": ["Queue", "Stack", "Array", "Linked List"],
        "answer": 1,
        "explanation": "A Stack operates on the LIFO (Last-In, First-Out) principle, where the most recently pushed element is the first one popped off."
    }
]

# Extended Question Bank for topic-specific practice
EXTENDED_QUESTION_BANK = {
    "Python": [
        SYNOPSIS_MOCK_QUESTIONS[2],  # Python comments
        {"id": "py2", "concept": "Python types", "question": "What is the boolean evaluation of an empty list `bool([])` in Python?", "options": ["True", "False", "None", "TypeError"], "answer": 1, "explanation": "Empty collections (lists, tuples, dicts, strings) evaluate to False in boolean contexts in Python."},
        {"id": "py3", "concept": "Python mutability", "question": "Which of the following data types in Python is mutable?", "options": ["tuple", "string", "list", "frozenset"], "answer": 2, "explanation": "Lists can be modified in-place after creation (mutable). Tuples, strings, and frozensets are immutable."},
        {"id": "py4", "concept": "Python operators", "question": "What does the `is` operator check in Python?", "options": ["Value equality", "Identity (memory address)", "Type compatibility", "Subset membership"], "answer": 1, "explanation": "'is' checks object identity (whether two references point to the exact same object in memory), while '==' tests value equality."},
        {"id": "py5", "concept": "Python dictionary", "question": "What is the average time complexity for key lookup in a Python dictionary?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": 0, "explanation": "Python dictionaries are implemented as hash tables, providing O(1) average-case time complexity for key lookups."}
    ],
    "C": [
        {"id": "c1", "concept": "C pointers", "question": "Which format specifier is used to print the memory address of a pointer in C?", "options": ["%d", "%x", "%p", "%u"], "answer": 2, "explanation": "'%p' is the format specifier for printing pointer memory addresses in hexadecimal representation."},
        {"id": "c2", "concept": "C memory", "question": "Which header file is required to use malloc() and free() functions?", "options": ["<stdio.h>", "<stdlib.h>", "<string.h>", "<conio.h>"], "answer": 1, "explanation": "<stdlib.h> declares standard utility functions including dynamic memory allocation routines (malloc, calloc, realloc, free)."},
        {"id": "c3", "concept": "C storage", "question": "What is the default storage class for local variables declared inside a C function?", "options": ["static", "extern", "auto", "register"], "answer": 2, "explanation": "Local variables declared inside functions default to the 'auto' storage class and are allocated on the stack."},
        {"id": "c4", "concept": "C pointer size", "question": "What is the size of any pointer variable on a 64-bit operating system?", "options": ["2 bytes", "4 bytes", "8 bytes", "Depends on pointed data type"], "answer": 2, "explanation": "On a 64-bit architecture, every pointer holds a 64-bit address, occupying exactly 8 bytes of memory."},
        {"id": "c5", "concept": "C strings", "question": "Which character implicitly marks the end of every string literal in C?", "options": ["\\n", "\\0", "\\t", ";"], "answer": 1, "explanation": "Strings in C are null-terminated arrays of characters ending with '\\0' (ASCII code 0)."}
    ],
    "DSA": [
        SYNOPSIS_MOCK_QUESTIONS[1],  # FIFO Queue
        SYNOPSIS_MOCK_QUESTIONS[4],  # LIFO Stack
        {"id": "dsa3", "concept": "DSA sorting", "question": "What is the worst-case time complexity of QuickSort?", "options": ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"], "answer": 2, "explanation": "QuickSort worst-case time complexity is O(n^2), which occurs when the pivot chosen is consistently the smallest or largest element."},
        {"id": "dsa4", "concept": "DSA graph", "question": "Which data structure is primarily used to implement Breadth-First Search (BFS) on a graph?", "options": ["Stack", "Queue", "Priority Queue", "Binary Search Tree"], "answer": 1, "explanation": "BFS uses a Queue to explore graph vertices level-by-level in the order they are discovered."},
        {"id": "dsa5", "concept": "DSA trees", "question": "What is the maximum height of a balanced Binary Search Tree (such as AVL or Red-Black tree) with n nodes?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "answer": 1, "explanation": "Self-balancing binary search trees maintain an upper bound height of O(log n), guaranteeing logarithmic search time."}
    ],
    "DBMS": [
        SYNOPSIS_MOCK_QUESTIONS[3],  # SQL SELECT
        {"id": "dbms2", "concept": "DBMS ACID", "question": "What does the letter 'A' stand for in the ACID properties of database transactions?", "options": ["Accuracy", "Atomicity", "Availability", "Authentication"], "answer": 1, "explanation": "Atomicity ensures that all operations within a database transaction either succeed together completely or are fully rolled back with no partial effects."},
        {"id": "dbms3", "concept": "DBMS normal forms", "question": "Which Normal Form requires eliminating partial functional dependencies on candidate keys?", "options": ["1NF", "2NF", "3NF", "BCNF"], "answer": 1, "explanation": "A relation is in 2NF if it is in 1NF and no non-prime attribute is partially dependent on any candidate key."},
        {"id": "dbms4", "concept": "DBMS keys", "question": "What distinguishes a PRIMARY KEY from a UNIQUE key constraint?", "options": ["Unique allows NULL values; Primary Key cannot", "Primary Key creates an index, Unique does not", "Unique is only for numeric columns", "There is no difference"], "answer": 0, "explanation": "A table can only have one PRIMARY KEY and it strictly prohibits NULL values, while UNIQUE constraints allow NULL values."},
        {"id": "dbms5", "concept": "DBMS joins", "question": "Which JOIN returns all rows from the left table regardless of matching records in the right table?", "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"], "answer": 1, "explanation": "A LEFT (OUTER) JOIN returns all rows from the left table, populating NULL for non-matching columns of the right table."}
    ],
    "Aptitude": [
        {"id": "apt1", "concept": "Time and Distance", "question": "A train 150 meters long passes an electric pole in 9 seconds. What is the speed of the train in km/h?", "options": ["50 km/h", "60 km/h", "75 km/h", "80 km/h"], "answer": 1, "explanation": "Speed = Distance / Time = 150 / 9 m/s = (50/3) * (18/5) = 60 km/h."},
        {"id": "apt2", "concept": "Time and Work", "question": "Person A can complete a work in 10 days, and Person B can complete it in 15 days. Working together, how many days will they take?", "options": ["5 days", "6 days", "7.5 days", "8 days"], "answer": 1, "explanation": "Combined rate per day = (1/10) + (1/15) = 5/30 = 1/6. Total days = 6 days."},
        {"id": "apt3", "concept": "Profit and Loss", "question": "An article bought for Rs. 800 is sold for Rs. 1000. What is the profit percentage?", "options": ["20%", "25%", "15%", "30%"], "answer": 1, "explanation": "Profit = Rs. 1000 - 800 = 200. Profit % = (200 / 800) * 100 = 25%."},
        {"id": "apt4", "concept": "Number Series", "question": "Find the next number in the series: 2, 6, 12, 20, 30, ?", "options": ["40", "42", "44", "46"], "answer": 1, "explanation": "The differences are consecutive even numbers: +4, +6, +8, +10, +12. Therefore, next term = 30 + 12 = 42."},
        {"id": "apt5", "concept": "Probability", "question": "What is the probability of obtaining an odd number when rolling a single fair 6-sided die?", "options": ["1/6", "1/3", "1/2", "2/3"], "answer": 2, "explanation": "Odd numbers are {1, 3, 5} out of 6 possible outcomes {1, 2, 3, 4, 5, 6}. Probability = 3/6 = 1/2."}
    ]
}

# Extended question bank (additive): 10 more questions per tracked subject (15 each)
for _subject, _extra in ds.EXTRA_SUBJECT_QUESTIONS.items():
    EXTENDED_QUESTION_BANK[_subject].extend(_extra)

# Quiz-only categories: appear in the mock-test dropdown but are NOT tracked subjects
QUIZ_ONLY_BANK = ds.QUIZ_ONLY_QUESTIONS


def _all_question_banks():
    """Yields every question list (synopsis, tracked subjects, quiz-only categories)."""
    yield SYNOPSIS_MOCK_QUESTIONS
    for bank in EXTENDED_QUESTION_BANK.values():
        yield bank
    for bank in QUIZ_ONLY_BANK.values():
        yield bank


# Difficulty labels for the original questions (additive field)
for _bank in _all_question_banks():
    for _q in _bank:
        _q.setdefault("difficulty", ds.LEGACY_DIFFICULTY.get(_q["id"], "Medium"))

# Fast id -> question lookup used when scoring submissions
QUESTION_LOOKUP = {}
for _bank in _all_question_banks():
    for _q in _bank:
        QUESTION_LOOKUP[_q["id"]] = _q

MOCK_TEST_COUNTS = (5, 10, 15)
DIFFICULTIES = ("Easy", "Medium", "Hard")

# ---------------------------------------------------------------------------
# SAMPLE STUDENTS DATA (For academic demonstration and profile comparison)
# (Directly specified in the Project Synopsis page 4 & 7)
# ---------------------------------------------------------------------------

SAMPLE_STUDENTS = [
    {
        "id": 1,
        "name": "Aditya Dwivedi",
        "roll_no": "2501721530006",
        "branch": "CSE - AIML",
        "cgpa": 8.2,
        "subjects": {"Python": 70, "C": 55, "DSA": 42, "DBMS": 60, "Aptitude": 35},
        "mock_score": "4/5 (80%)",
        "company": "Infosys",
        "placement_status": "Applied",
        "goals": "3 goals (1 completed)"
    },
    {
        "id": 2,
        "name": "Priya Verma",
        "roll_no": "2501721530045",
        "branch": "CSE - AIML",
        "cgpa": 9.1,
        "subjects": {"Python": 90, "C": 84, "DSA": 88, "DBMS": 86, "Aptitude": 92},
        "mock_score": "5/5 (100%)",
        "company": "Google",
        "placement_status": "Selected",
        "goals": "4 goals (4 completed)"
    },
    {
        "id": 3,
        "name": "Aarav Sharma",
        "roll_no": "2501721530012",
        "branch": "CSE",
        "cgpa": 8.5,
        "subjects": {"Python": 78, "C": 72, "DSA": 80, "DBMS": 74, "Aptitude": 76},
        "mock_score": "4/5 (80%)",
        "company": "Wipro",
        "placement_status": "Shortlisted",
        "goals": "3 goals (2 completed)"
    },
    {
        "id": 4,
        "name": "Rohan Singh",
        "roll_no": "2501721530078",
        "branch": "IT",
        "cgpa": 7.4,
        "subjects": {"Python": 85, "C": 78, "DSA": 90, "DBMS": 70, "Aptitude": 88},
        "mock_score": "2/5 (40%)",
        "company": "TCS",
        "placement_status": "Interview",
        "goals": "2 goals (0 completed)"
    },
    {
        "id": 5,
        "name": "Ananya Gupta",
        "roll_no": "2501721530029",
        "branch": "ECE",
        "cgpa": 8.0,
        "subjects": {"Python": 65, "C": 70, "DSA": 58, "DBMS": 62, "Aptitude": 65},
        "mock_score": "3/5 (60%)",
        "company": "Cognizant",
        "placement_status": "Interested",
        "goals": "3 goals (2 completed)"
    }
]

# Extended sample students (additive): optional fields for ids 1-5, plus 10 new records
for _stu in SAMPLE_STUDENTS:
    _stu.update(ds.SAMPLE_STUDENT_EXTRAS.get(_stu["id"], {}))
SAMPLE_STUDENTS.extend(ds.NEW_SAMPLE_STUDENTS)

# Curated recommendation topics for each subject
SUBJECT_RECOMMENDATIONS = {
    "Python": {
        "topics": ["List Comprehensions & Slicing", "Decorators & Generators", "OOPs & Dunder Methods", "Collections & Dictionaries", "Exception Handling"],
        "advice": "Practice writing clean Python scripts and revise standard built-in functions."
    },
    "C": {
        "topics": ["Pointers & Pointer Arithmetic", "Dynamic Memory (malloc/free)", "Structures & Unions", "Storage Classes", "Macros & Include Guards"],
        "advice": "Debug memory issues, trace pointer values, and master string manipulation in C."
    },
    "DSA": {
        "topics": ["Arrays & Two Pointers", "Linked Lists (Reversal & Fast-Slow)", "Stacks & Queues (FIFO/LIFO)", "Trees & Traversals (BFS/DFS)", "Binary Search"],
        "advice": "Solve at least 2 coding problems every day and analyze time/space complexities."
    },
    "DBMS": {
        "topics": ["ACID Properties & Transactions", "Normalization (1NF, 2NF, 3NF, BCNF)", "SQL SELECT & Joins", "Indexing & B+ Trees", "Keys (Primary, Unique, Foreign)"],
        "advice": "Write hands-on SQL queries and master table schema constraints."
    },
    "Aptitude": {
        "topics": ["Time, Speed & Distance", "Time & Work", "Profit & Loss", "Permutations & Combinations", "Logical Deductions & Syllogisms"],
        "advice": "Practice 10 timed questions daily to sharpen problem-solving speed and accuracy."
    }
}

# ---------------------------------------------------------------------------
# RELATED COMPANY SUGGESTIONS MOCK DATA
# 13 Sample Companies (6 original + 7 extended) with specific hiring thresholds across:
# 1. Mock Test Score & Percentage (0-100)
# 2. Strong Subject Areas (Subjects >= 50%) and Subject Score Minimums
# 3. Daily Goals Consistency Ratio (Completed / Total Goals)
# ---------------------------------------------------------------------------

COMPANY_SUGGESTIONS_DATA = [
    {
        "id": "comp_amazon",
        "company": "Amazon",
        "role": "Software Development Engineer (SDE-1)",
        "tier": "Tier-1 Product",
        "package_ctc": "24.0 - 44.0 LPA",
        "location": "Bengaluru / Hyderabad / Gurugram",
        "badge_color": "warning",
        "min_mock_pct": 80,
        "required_strong_subjects": ["DSA", "Python"],
        "min_subject_scores": {"DSA": 70, "Python": 65},
        "min_goal_consistency": 50,
        "hiring_focus": "Data Structures, High-Performance Algorithms & System Clean Code",
        "description": "Looking for top-tier problem solvers with deep DSA mastery, high mock test scores, and disciplined daily preparation habits."
    },
    {
        "id": "comp_techcorp_ai",
        "company": "TechCorp AI Labs",
        "role": "Junior AI/ML & Python Developer",
        "tier": "AI/ML Product Startup",
        "package_ctc": "8.0 - 12.0 LPA",
        "location": "Noida / Remote",
        "badge_color": "info",
        "min_mock_pct": 70,
        "required_strong_subjects": ["Python", "DBMS"],
        "min_subject_scores": {"Python": 70, "DBMS": 55},
        "min_goal_consistency": 40,
        "hiring_focus": "Python OOPs, SQL Schema Engineering & Daily Code Consistency",
        "description": "Fast-scaling AI startup seeking candidates with solid Python fundamentals, clean database design, and daily task discipline."
    },
    {
        "id": "comp_infosys",
        "company": "Infosys",
        "role": "Specialist Programmer (Digital Track)",
        "tier": "Tier-1 IT / Digital",
        "package_ctc": "6.5 - 9.5 LPA",
        "location": "Pune / Bengaluru / Mysuru",
        "badge_color": "primary",
        "min_mock_pct": 60,
        "required_strong_subjects": ["Python", "DBMS"],
        "min_subject_scores": {"Python": 60, "DBMS": 50},
        "min_goal_consistency": 25,
        "hiring_focus": "Core Python Programming, Relational DBMS & Analytical Skills",
        "description": "Premium digital hiring track for high-performing coders with solid DBMS concepts and strong baseline mock scores."
    },
    {
        "id": "comp_cognizant",
        "company": "Cognizant",
        "role": "GenC Elevate Developer",
        "tier": "Consulting & Enterprise",
        "package_ctc": "4.25 - 5.5 LPA",
        "location": "Gurugram / Kolkata / Chennai",
        "badge_color": "success",
        "min_mock_pct": 60,
        "required_strong_subjects": ["Python", "C"],
        "min_subject_scores": {"Python": 50, "C": 50},
        "min_goal_consistency": 20,
        "hiring_focus": "Multi-Language Programming (Python/C) & Technical Aptitude",
        "description": "Elevated campus track seeking graduates with balanced fundamentals in Python and C without active weak areas."
    },
    {
        "id": "comp_wipro",
        "company": "Wipro",
        "role": "Turbo Developer / Project Engineer",
        "tier": "Global Tech Services",
        "package_ctc": "4.5 - 6.5 LPA",
        "location": "Greater Noida / Hyderabad",
        "badge_color": "secondary",
        "min_mock_pct": 60,
        "required_strong_subjects": ["C", "DBMS"],
        "min_subject_scores": {"C": 50, "DBMS": 50},
        "min_goal_consistency": 20,
        "hiring_focus": "C Pointers, Memory Management, SQL Queries & Engineering Foundations",
        "description": "Assesses foundational C programming, structured database queries, and sustained preparation consistency."
    },
    {
        "id": "comp_tcs",
        "company": "TCS (Tata Consultancy Services)",
        "role": "TCS Digital / Ninja Engineer",
        "tier": "Mass Recruiter / Digital Track",
        "package_ctc": "3.6 - 7.0 LPA",
        "location": "Pan-India (NQT Drive)",
        "badge_color": "dark",
        "min_mock_pct": 40,
        "required_strong_subjects": ["Aptitude"],
        "min_subject_scores": {"Aptitude": 50},
        "min_goal_consistency": 0,
        "hiring_focus": "Quantitative Aptitude, Speed Mathematics & Core CS Concepts",
        "description": "National Qualifier Test gateway where clearing the Aptitude screening round is the primary prerequisite."
    }
]

# Extended company criteria (additive): 7 more companies -> 13 total
COMPANY_SUGGESTIONS_DATA.extend(ds.EXTRA_COMPANY_SUGGESTIONS)

# ---------------------------------------------------------------------------
# RUNTIME IN-MEMORY STATE VARIABLES
# ---------------------------------------------------------------------------

state = {
    "student": dict(DEFAULT_STUDENT),
    "subjects": dict(DEFAULT_SUBJECTS),
    "companies": [dict(c) for c in DEFAULT_COMPANIES],
    "goals": [dict(g) for g in DEFAULT_GOALS],
    # Seeded with 6 past attempts (newest first) so charts and suggestions have data
    "test_history": [dict(t) for t in ds.SEED_TEST_HISTORY],
    "topics": copy.deepcopy(ds.DEFAULT_TOPIC_CHECKLIST),
}

# ---------------------------------------------------------------------------
# CORE BUSINESS LOGIC (Calculations directly matching Synopsis specifications)
# ---------------------------------------------------------------------------

def calculate_summary(subjects_dict):
    """
    Calculates overall score and readiness status based on the 5 tracked subjects:
    - Overall score = average of progress values (0 to 100)
    - Classification:
        Score >= 75: Excellent
        50 <= Score < 75: Good
        Score < 50: Needs Improvement
    - Weak Area Finder: Subjects with score < 50% are flagged dynamically.
    """
    values = list(subjects_dict.values())
    if not values:
        return {"overall_score": 0, "status": "Needs Improvement", "weak_areas": []}
    
    overall_score = round(sum(values) / len(values))
    
    if overall_score >= 75:
        status = "Excellent"
    elif overall_score >= 50:
        status = "Good"
    else:
        status = "Needs Improvement"
        
    weak_areas = []
    for subject, score in subjects_dict.items():
        if score < 50:
            rec = SUBJECT_RECOMMENDATIONS.get(subject, {})
            weak_areas.append({
                "subject": subject,
                "score": score,
                "topics": rec.get("topics", ["Core Fundamentals"]),
                "advice": rec.get("advice", "Review subject basics.")
            })
            
    return {
        "overall_score": overall_score,
        "status": status,
        "weak_areas": weak_areas
    }

def evaluate_company_suggestions(subjects_dict, goals_list, test_history):
    """
    Evaluates student readiness against hiring criteria of target companies based on:
    1. Mock Test Score & Percentage (from test history or default benchmark)
    2. Weak Area Finder (subjects < 50% flagged as weak; subjects >= 50% treated as strong)
    3. Daily Goals Ratio (completed / total goals measuring preparation consistency)

    Returns categorized suggestions with fit percentages, diagnostic advice, and match reasons.
    """
    # 1. Parameter 1: Mock Test Score & Percentage
    if test_history and len(test_history) > 0:
        latest = test_history[0]
        mock_score = latest.get("score", 0)
        mock_total = latest.get("total", 5)
        mock_pct = latest.get("percentage", 0)
    else:
        # Default baseline from student's benchmark profile (4/5 = 80%)
        mock_score = 4
        mock_total = 5
        mock_pct = 80

    # 2. Parameter 2: Weak Area Finder & Strong Areas
    weak_areas = [sub for sub, score in subjects_dict.items() if score < 50]
    strong_areas = [sub for sub, score in subjects_dict.items() if score >= 50]

    # 3. Parameter 3: Daily Goals Completion Consistency Ratio
    total_goals = len(goals_list)
    completed_goals = sum(1 for g in goals_list if g.get("completed", False))
    goal_ratio_pct = round((completed_goals / total_goals) * 100) if total_goals > 0 else 0

    suggestions = []

    for comp in COMPANY_SUGGESTIONS_DATA:
        missing_requirements = []
        matched_strengths = []

        # Check Mock Test Score
        min_mock = comp["min_mock_pct"]
        if mock_pct >= min_mock:
            matched_strengths.append(f"Mock Score: {mock_pct}% (meets >={min_mock}%)")
        else:
            missing_requirements.append(
                f"Mock Test Score is {mock_pct}% (requires at least {min_mock}%)"
            )

        # Check Strong Subject Areas vs Weak Areas
        req_strong = comp.get("required_strong_subjects", [])
        for req_sub in req_strong:
            sub_score = subjects_dict.get(req_sub, 0)
            if req_sub in weak_areas:
                missing_requirements.append(
                    f"{req_sub} is currently a weak area ({sub_score}% < 50%)"
                )
            elif req_sub in strong_areas:
                matched_strengths.append(f"Strong in {req_sub} ({sub_score}%)")

        # Check Specific Subject Score Minimums
        for sub_name, min_score in comp.get("min_subject_scores", {}).items():
            sub_score = subjects_dict.get(sub_name, 0)
            if sub_score < min_score:
                if not any(sub_name in m for m in missing_requirements):
                    missing_requirements.append(
                        f"{sub_name} score is {sub_score}% (requires at least {min_score}%)"
                    )

        # Check Daily Goals Consistency
        min_goals = comp["min_goal_consistency"]
        if goal_ratio_pct >= min_goals:
            if min_goals > 0:
                matched_strengths.append(f"Goal Consistency: {goal_ratio_pct}% (meets >={min_goals}%)")
        else:
            missing_requirements.append(
                f"Goal consistency is {goal_ratio_pct}% ({completed_goals}/{total_goals} done; requires >={min_goals}%)"
            )

        is_eligible = (len(missing_requirements) == 0)

        # Calculate Fit / Match Percentage (0-100)
        # Weighted model: Mock Test (35%), Core Subject Thresholds (45%), Daily Consistency (20%)
        mock_contrib = min(1.0, mock_pct / max(1, min_mock)) * 35.0

        sub_ratios = []
        for s in (req_strong or ["Python", "DSA"]):
            req_min = comp.get("min_subject_scores", {}).get(s, 50)
            sub_ratios.append(min(1.0, subjects_dict.get(s, 0) / max(1, req_min)))
        sub_contrib = (sum(sub_ratios) / len(sub_ratios) if sub_ratios else 1.0) * 45.0

        if min_goals > 0:
            goal_contrib = min(1.0, goal_ratio_pct / min_goals) * 20.0
        else:
            goal_contrib = 20.0

        match_score = max(15, min(100, round(mock_contrib + sub_contrib + goal_contrib)))

        if is_eligible:
            status_label = "Eligible Match"
            status_badge = "success"
        elif len(missing_requirements) <= 2 and match_score >= 60:
            status_label = "Near Match (Minor Gap)"
            status_badge = "warning"
        else:
            status_label = "Target Aspirations"
            status_badge = "secondary"

        suggestions.append({
            "id": comp["id"],
            "company": comp["company"],
            "role": comp["role"],
            "tier": comp["tier"],
            "package_ctc": comp["package_ctc"],
            "location": comp.get("location", "Pan-India"),
            "badge_color": comp.get("badge_color", "primary"),
            "hiring_focus": comp["hiring_focus"],
            "description": comp["description"],
            "is_eligible": is_eligible,
            "match_score": match_score,
            "status_label": status_label,
            "status_badge": status_badge,
            "matched_strengths": matched_strengths,
            "missing_requirements": missing_requirements,
            "criteria": {
                "min_mock_pct": min_mock,
                "required_strong_subjects": req_strong,
                "min_subject_scores": comp.get("min_subject_scores", {}),
                "min_goal_consistency": min_goals
            }
        })

    # Sort suggestions: Eligible first, then descending by match_score
    suggestions.sort(key=lambda x: (x["is_eligible"], x["match_score"]), reverse=True)

    return {
        "metrics": {
            "mock_score": mock_score,
            "mock_total": mock_total,
            "mock_percentage": mock_pct,
            "strong_areas": strong_areas,
            "weak_areas": weak_areas,
            "goals_completed": completed_goals,
            "goals_total": total_goals,
            "goal_completion_pct": goal_ratio_pct
        },
        "suggestions": suggestions,
        "total_companies": len(suggestions),
        "total_eligible": sum(1 for s in suggestions if s["is_eligible"])
    }


def overall_status(score):
    """Maps an overall score to the synopsis readiness band."""
    if score >= 75:
        return "Excellent"
    if score >= 50:
        return "Good"
    return "Needs Improvement"


def topic_progress(topics_by_subject):
    """Per-subject checklist completion: completed / in-progress / not-started counts and a percentage."""
    result = {}
    for subject, topics in topics_by_subject.items():
        total = len(topics)
        done = sum(1 for t in topics if t["status"] == "Completed")
        doing = sum(1 for t in topics if t["status"] == "In Progress")
        result[subject] = {
            "total": total,
            "completed": done,
            "in_progress": doing,
            "not_started": total - done - doing,
            "completion_pct": round((done / total) * 100) if total else 0,
        }
    return result


def get_activity():
    """Builds the 84-day activity log with streak summary (deterministic per calendar date)."""
    log = ds.build_activity_log()
    return log, ds.activity_summary(log)


def evaluate_achievements():
    """Evaluates every badge rule against the live runtime state."""
    _, act = get_activity()
    subjects = state["subjects"]
    summary = calculate_summary(subjects)
    history = state["test_history"]
    goals = state["goals"]
    done_goals = sum(1 for g in goals if g.get("completed"))
    attempts = len(history)
    best_pct = max((t.get("percentage", 0) for t in history), default=0)
    below_50 = sum(1 for v in subjects.values() if v < 50)
    below_60 = sum(1 for v in subjects.values() if v < 60)
    companies = state["companies"]
    selected = sum(1 for c in companies if c.get("status") == "Selected")
    completed_topics = sum(
        1 for topics in state["topics"].values() for t in topics if t["status"] == "Completed"
    )

    def badge(bid, name, description, icon, current, target, hint_locked, hint_done):
        unlocked = current >= target
        return {
            "id": bid,
            "name": name,
            "description": description,
            "icon": icon,
            "unlocked": unlocked,
            "current": min(current, target),
            "target": target,
            "progress_pct": min(100, round((current / target) * 100)) if target else 100,
            "hint": hint_done if unlocked else hint_locked,
        }

    badges = [
        badge("first_mock_test", "First Mock Test", "Attempt your first placement mock test.",
              "bi-patch-question-fill", attempts, 1,
              "Take any mock test to unlock.", f"You have recorded {attempts} mock test attempt(s)."),
        badge("perfect_score", "Perfect Score", "Score 100% on any mock test.",
              "bi-bullseye", best_pct, 100,
              f"Best score so far is {best_pct}%. Aim for 100%.", "You scored 100% on a mock test!"),
        badge("test_veteran", "Test Veteran", "Complete 5 mock tests.",
              "bi-clipboard2-check-fill", attempts, 5,
              f"{attempts}/5 mock tests completed.", f"{attempts} mock tests completed."),
        badge("streak_5", "5-Day Streak", "Study on 5 days in a row.",
              "bi-fire", act["current_streak"], 5,
              f"Current streak is {act['current_streak']} day(s).", f"Current streak: {act['current_streak']} days."),
        badge("no_weak_areas", "No Weak Areas", "Keep all five subjects at 50% or above.",
              "bi-shield-check", 5 - below_50, 5,
              f"{below_50} subject(s) are still below 50%.", "All five subjects are at 50% or above."),
        badge("all_rounder", "All-Rounder", "Reach 60% or above in all five subjects.",
              "bi-stars", 5 - below_60, 5,
              f"{below_60} subject(s) are still below 60%.", "All five subjects are at 60% or above."),
        badge("placement_ready", "Placement Ready", "Reach an overall score of 75% or more.",
              "bi-award-fill", summary["overall_score"], 75,
              f"Overall score is {summary['overall_score']}%. Target is 75%.", "Your overall score is Excellent (75%+)."),
        badge("goal_getter", "Goal Getter", "Complete 5 daily preparation goals.",
              "bi-check2-circle", done_goals, 5,
              f"{done_goals}/5 goals completed.", f"{done_goals} goals completed."),
        badge("pipeline_builder", "Pipeline Builder", "Track 5 or more company applications.",
              "bi-briefcase-fill", len(companies), 5,
              f"{len(companies)}/5 companies tracked.", f"{len(companies)} companies tracked."),
        badge("first_offer", "First Offer", "Move any application to Selected.",
              "bi-trophy-fill", selected, 1,
              "No application is marked Selected yet.", f"{selected} application(s) marked Selected."),
    ]
    return badges, completed_topics

# ---------------------------------------------------------------------------
# FLASK HTTP ROUTES & REST API ENDPOINTS
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serves the main web dashboard."""
    return render_template("index.html")

@app.route("/api/data", methods=["GET"])
def get_all_data():
    """
    Returns complete dashboard data:
    Student Profile, Subject Progress, Preparation Summary, Weak Areas,
    Company Pipeline, Daily Goals, Sample Student Benchmarks, Test History,
    and Related Company Suggestions.
    """
    summary = calculate_summary(state["subjects"])
    suggestions_data = evaluate_company_suggestions(state["subjects"], state["goals"], state["test_history"])
    _, activity_info = get_activity()
    badges, _topics_done = evaluate_achievements()
    return jsonify({
        "success": True,
        "student": state["student"],
        "subjects": state["subjects"],
        "summary": summary,
        "companies": state["companies"],
        "goals": state["goals"],
        "test_history": state["test_history"],
        "sample_students": SAMPLE_STUDENTS,
        "suggestions": suggestions_data["suggestions"],
        "suggestion_metrics": suggestions_data["metrics"],
        "total_eligible_suggestions": suggestions_data["total_eligible"],
        # Additional keys (extended datasets)
        "progress_history": ds.PROGRESS_HISTORY,
        "activity_summary": activity_info,
        "achievements": badges
    })

@app.route("/api/suggestions", methods=["GET"])
def get_company_suggestions_route():
    """
    Evaluates current student metrics (mock test score, strong/weak areas, daily goals)
    against hiring criteria of target companies and returns matched suggestions in JSON format.
    """
    result = evaluate_company_suggestions(state["subjects"], state["goals"], state["test_history"])
    return jsonify({
        "success": True,
        **result
    })

@app.route("/api/profile", methods=["POST"])
def update_profile():
    """Updates the student profile details."""
    data = request.get_json() or {}
    if "name" in data and data["name"].strip():
        state["student"]["name"] = data["name"].strip()
    if "branch" in data and data["branch"].strip():
        state["student"]["branch"] = data["branch"].strip()
    if "roll_no" in data:
        state["student"]["roll_no"] = data["roll_no"].strip()
    if "cgpa" in data:
        try:
            val = float(data["cgpa"])
            state["student"]["cgpa"] = max(0.0, min(10.0, round(val, 2)))
        except (ValueError, TypeError):
            pass
    if "college" in data:
        state["student"]["college"] = data["college"].strip()
        
    return jsonify({"success": True, "student": state["student"], "message": "Profile updated successfully."})

@app.route("/api/subjects", methods=["POST"])
def update_subjects():
    """
    Updates progress values (0-100) for the 5 core subjects:
    Python, C, DSA, DBMS, Aptitude. Recalculates placement score and weak areas.
    """
    data = request.get_json() or {}
    for sub in ["Python", "C", "DSA", "DBMS", "Aptitude"]:
        if sub in data:
            try:
                val = int(data[sub])
                state["subjects"][sub] = max(0, min(100, val))
            except (ValueError, TypeError):
                pass
                
    summary = calculate_summary(state["subjects"])
    return jsonify({
        "success": True,
        "subjects": state["subjects"],
        "summary": summary,
        "message": "Subject progress saved successfully."
    })

@app.route("/api/mock-test", methods=["GET"])
def get_mock_test():
    """
    Returns mock test questions (answer keys are never exposed).

    Query parameters:
      category   Synopsis (default) | Python | C | DSA | DBMS | Aptitude |
                 OOP | Operating Systems | Computer Networks | Logical Reasoning | All
      count      5 (default), 10 or 15; capped at the size of the question pool
      difficulty Optional: Easy | Medium | Hard

    The Synopsis category always returns the same 5 core questions in the same order.
    Every other category returns a fresh random selection on each call.
    """
    category = request.args.get("category", "Synopsis")

    try:
        count = int(request.args.get("count", 5))
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "count must be 5, 10 or 15."}), 400
    if count not in MOCK_TEST_COUNTS:
        return jsonify({"success": False, "error": "count must be 5, 10 or 15."}), 400

    difficulty = request.args.get("difficulty")
    if difficulty is not None:
        difficulty = difficulty.strip().capitalize()
        if difficulty not in DIFFICULTIES:
            return jsonify({"success": False, "error": "difficulty must be Easy, Medium or Hard."}), 400

    if category == "Synopsis":
        # Fixed synopsis test: same 5 questions, same order, difficulty filter not applied
        selected = SYNOPSIS_MOCK_QUESTIONS[:count]
    else:
        if category == "All":
            pool, seen = [], set()
            for bank in _all_question_banks():
                for q in bank:
                    if q["id"] not in seen:
                        seen.add(q["id"])
                        pool.append(q)
        elif category in EXTENDED_QUESTION_BANK:
            pool = list(EXTENDED_QUESTION_BANK[category])
        elif category in QUIZ_ONLY_BANK:
            pool = list(QUIZ_ONLY_BANK[category])
        else:
            return jsonify({"success": False, "error": f"Unknown category '{category}'."}), 400

        if difficulty:
            pool = [q for q in pool if q.get("difficulty") == difficulty]
        if not pool:
            return jsonify({"success": False, "error": "No questions match the selected filters."}), 400
        selected = random.sample(pool, min(count, len(pool)))

    # Send questions without exposing the answer key to the frontend directly
    safe_questions = [
        {
            "id": q["id"],
            "concept": q.get("concept", ""),
            "difficulty": q.get("difficulty", "Medium"),
            "question": q["question"],
            "options": q["options"],
        }
        for q in selected
    ]

    return jsonify({
        "success": True,
        "category": category,
        "difficulty": difficulty,
        "count": len(safe_questions),
        "questions": safe_questions
    })

@app.route("/api/mock-test/submit", methods=["POST"])
def submit_mock_test():
    """
    Evaluates submitted mock test answers on the backend.
    Calculates score, percentage, returns performance message, and records attempt.

    Body: {"answers": {question_id: selected_index}, "category": "...",
           "question_ids": [optional list of every question served, so skipped ones count as wrong]}
    """
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", {})  # dict of {question_id: selected_index}
    category = data.get("category", "Synopsis")

    if not isinstance(answers, dict):
        return jsonify({"success": False, "error": "answers must be an object of {question_id: selected_index}."}), 400

    served_ids = data.get("question_ids")
    if served_ids is not None:
        if not isinstance(served_ids, list):
            return jsonify({"success": False, "error": "question_ids must be a list."}), 400
        question_ids = [str(q) for q in served_ids]
    elif answers:
        question_ids = list(answers.keys())
    else:
        question_ids = [q["id"] for q in SYNOPSIS_MOCK_QUESTIONS]

    score = 0
    review = []

    for q_id in question_ids:
        ref = QUESTION_LOOKUP.get(q_id)
        if not ref:
            continue
        user_choice = answers.get(q_id)
        is_correct = (user_choice == ref["answer"])
        if is_correct:
            score += 1

        review.append({
            "id": q_id,
            "concept": ref.get("concept", ""),
            "difficulty": ref.get("difficulty", "Medium"),
            "question": ref["question"],
            "options": ref["options"],
            "user_choice": user_choice,
            "correct_answer": ref["answer"],
            "is_correct": is_correct,
            "explanation": ref["explanation"]
        })

    total = len(review)
    if total == 0:
        return jsonify({"success": False, "error": "No valid question ids were submitted."}), 400

    pct = round((score / total) * 100)

    # Classification message as specified in Synopsis
    if pct >= 80:
        performance_message = "Outstanding! You demonstrated excellent fundamental knowledge for placement technical rounds."
        rating = "Excellent"
    elif pct >= 60:
        performance_message = "Good effort! Revise weak topics to achieve top placement readiness."
        rating = "Good"
    else:
        performance_message = "Needs Improvement! Focus on core computer science concepts before campus interviews."
        rating = "Needs Improvement"

    attempt_record = {
        "id": int(time.time() * 1000),
        "category": "Core Synopsis (5 Qs)" if category == "Synopsis" else category,
        "score": score,
        "total": total,
        "percentage": pct,
        "rating": rating,
        "date": time.strftime("%d %b %Y, %H:%M")
    }

    state["test_history"].insert(0, attempt_record)

    return jsonify({
        "success": True,
        "score": score,
        "total": total,
        "percentage": pct,
        "rating": rating,
        "performance_message": performance_message,
        "review": review,
        "attempt": attempt_record
    })

@app.route("/api/companies", methods=["POST"])
def add_company():
    """Adds a new company placement application."""
    data = request.get_json() or {}
    company = data.get("company", "").strip()
    role = data.get("role", "").strip()
    status = data.get("status", "Applied").strip()
    package_ctc = data.get("package_ctc", "").strip() or "N/A"
    notes = data.get("notes", "").strip()
    
    valid_statuses = ["Interested", "Applied", "Shortlisted", "Interview", "Selected", "Rejected"]
    if status not in valid_statuses:
        status = "Applied"
        
    if not company or not role:
        return jsonify({"success": False, "error": "Company name and job role are required."}), 400
        
    new_id = int(time.time() * 1000)
    record = {
        "id": new_id,
        "company": company,
        "role": role,
        "status": status,
        "package_ctc": package_ctc,
        "notes": notes
    }
    state["companies"].insert(0, record)
    return jsonify({"success": True, "company": record, "companies": state["companies"]})

@app.route("/api/companies/<int:company_id>", methods=["PUT"])
def update_company(company_id):
    """Updates company application status or details."""
    data = request.get_json() or {}
    for comp in state["companies"]:
        if comp["id"] == company_id:
            if "status" in data:
                comp["status"] = data["status"]
            if "role" in data:
                comp["role"] = data["role"]
            if "package_ctc" in data:
                comp["package_ctc"] = data["package_ctc"]
            if "notes" in data:
                comp["notes"] = data["notes"]
            return jsonify({"success": True, "company": comp, "companies": state["companies"]})
            
    return jsonify({"success": False, "error": "Company not found"}), 404

@app.route("/api/companies/<int:company_id>", methods=["DELETE"])
def delete_company(company_id):
    """Removes a company application from the tracker."""
    state["companies"] = [c for c in state["companies"] if c["id"] != company_id]
    return jsonify({"success": True, "companies": state["companies"]})

@app.route("/api/goals", methods=["POST"])
def add_goal():
    """Adds a new daily preparation goal."""
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"success": False, "error": "Goal description cannot be empty."}), 400
        
    new_id = int(time.time() * 1000)
    new_goal = {"id": new_id, "text": text, "completed": False}
    state["goals"].append(new_goal)
    return jsonify({"success": True, "goal": new_goal, "goals": state["goals"]})

@app.route("/api/goals/<int:goal_id>", methods=["PUT"])
def toggle_goal(goal_id):
    """Toggles or sets the completion status of a daily goal (Pending / Completed)."""
    data = request.get_json(silent=True) or {}
    for goal in state["goals"]:
        if goal["id"] == goal_id:
            if "completed" in data:
                goal["completed"] = bool(data["completed"])
            else:
                goal["completed"] = not goal["completed"]
            return jsonify({"success": True, "goal": goal, "goals": state["goals"]})
            
    return jsonify({"success": False, "error": "Goal not found"}), 404

@app.route("/api/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    """Deletes a daily goal."""
    state["goals"] = [g for g in state["goals"] if g["id"] != goal_id]
    return jsonify({"success": True, "goals": state["goals"]})

@app.route("/api/sample-students", methods=["GET"])
def get_sample_students():
    """Returns sample student records for demonstration and comparison."""
    return jsonify({"success": True, "sample_students": SAMPLE_STUDENTS})

@app.route("/api/sample-students/load/<int:student_id>", methods=["POST"])
def load_sample_student(student_id):
    """Loads a sample student's profile and subject metrics into the active tracker."""
    matched = next((s for s in SAMPLE_STUDENTS if s["id"] == student_id), None)
    if not matched:
        return jsonify({"success": False, "error": "Sample student not found"}), 404
        
    state["student"]["name"] = matched["name"]
    state["student"]["branch"] = matched["branch"]
    state["student"]["roll_no"] = matched["roll_no"]
    state["student"]["cgpa"] = matched["cgpa"]
    state["subjects"] = dict(matched["subjects"])
    
    summary = calculate_summary(state["subjects"])
    return jsonify({
        "success": True,
        "message": f"Loaded profile for {matched['name']}",
        "student": state["student"],
        "subjects": state["subjects"],
        "summary": summary
    })

@app.route("/api/reset", methods=["POST"])
def reset_state():
    """Resets all runtime data back to initial synopsis demo defaults."""
    state["student"] = dict(DEFAULT_STUDENT)
    state["subjects"] = dict(DEFAULT_SUBJECTS)
    state["companies"] = [dict(c) for c in DEFAULT_COMPANIES]
    state["goals"] = [dict(g) for g in DEFAULT_GOALS]
    state["test_history"] = [dict(t) for t in ds.SEED_TEST_HISTORY]
    state["topics"] = copy.deepcopy(ds.DEFAULT_TOPIC_CHECKLIST)
    
    summary = calculate_summary(state["subjects"])
    return jsonify({
        "success": True,
        "message": "System state reset to synopsis default data.",
        "student": state["student"],
        "subjects": state["subjects"],
        "summary": summary,
        "companies": state["companies"],
        "goals": state["goals"],
        "test_history": state["test_history"]
    })

# ---------------------------------------------------------------------------
# EXTENDED DATASET ENDPOINTS
# ---------------------------------------------------------------------------

SUBJECT_NAMES = ["Python", "C", "DSA", "DBMS", "Aptitude"]


def _match_subject(value):
    """Case-insensitive match of a subject name; returns the canonical name or None."""
    if value is None:
        return None
    for name in SUBJECT_NAMES:
        if name.lower() == str(value).strip().lower():
            return name
    return None


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """
    Ranks all sample students plus the active student by overall score (average of the 5 subjects).
    If the active student matches a sample record (same roll number) the live values replace it,
    so nobody appears twice. Ties share a rank.
    """
    active = state["student"]
    active_summary = calculate_summary(state["subjects"])
    rows = []
    for stu in SAMPLE_STUDENTS:
        if stu["roll_no"] == active.get("roll_no"):
            continue
        score = calculate_summary(stu["subjects"])
        rows.append({
            "name": stu["name"],
            "branch": stu["branch"],
            "overall_score": score["overall_score"],
            "status": score["status"],
            "is_active": False,
        })
    rows.append({
        "name": active.get("name", "You"),
        "branch": active.get("branch", ""),
        "overall_score": active_summary["overall_score"],
        "status": active_summary["status"],
        "is_active": True,
    })
    rows.sort(key=lambda r: (-r["overall_score"], r["name"]))

    prev_score, prev_rank = None, 0
    for position, row in enumerate(rows, start=1):
        if row["overall_score"] != prev_score:
            prev_rank = position
            prev_score = row["overall_score"]
        row["rank"] = prev_rank

    active_row = next(r for r in rows if r["is_active"])
    return jsonify({
        "success": True,
        "leaderboard": rows,
        "total": len(rows),
        "active_rank": active_row["rank"],
    })


@app.route("/api/progress-history", methods=["GET"])
def get_progress_history():
    """Returns 8 weekly subject snapshots plus the live current values for charting."""
    return jsonify({
        "success": True,
        "history": ds.PROGRESS_HISTORY,
        "subjects": SUBJECT_NAMES,
        "current": state["subjects"],
    })


@app.route("/api/activity", methods=["GET"])
def get_activity_route():
    """Returns the last 84 days of study activity plus streaks and totals."""
    log, summary = get_activity()
    return jsonify({"success": True, "days": len(log), "log": log, **summary})


@app.route("/api/topics", methods=["GET"])
def get_topics():
    """Returns the topic checklist (optionally for one subject) with completion statistics."""
    subject_arg = request.args.get("subject")
    if subject_arg is not None:
        subject = _match_subject(subject_arg)
        if not subject:
            return jsonify({"success": False, "error": f"Unknown subject '{subject_arg}'."}), 400
        topics = {subject: state["topics"][subject]}
    else:
        topics = state["topics"]
    return jsonify({
        "success": True,
        "statuses": ds.TOPIC_STATUSES,
        "topics": topics,
        "progress": topic_progress(topics),
    })


@app.route("/api/topics/<subject>/<topic_id>", methods=["PUT"])
def update_topic(subject, topic_id):
    """Sets a checklist topic to Not Started, In Progress or Completed."""
    canonical = _match_subject(subject)
    if not canonical:
        return jsonify({"success": False, "error": f"Unknown subject '{subject}'."}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "status" not in data:
        return jsonify({"success": False, "error": "Request body must be JSON with a 'status' field."}), 400
    status = data["status"]
    if status not in ds.TOPIC_STATUSES:
        return jsonify({"success": False,
                        "error": "status must be one of: " + ", ".join(ds.TOPIC_STATUSES) + "."}), 400

    for topic in state["topics"][canonical]:
        if topic["id"] == topic_id:
            topic["status"] = status
            return jsonify({
                "success": True,
                "subject": canonical,
                "topic": topic,
                "topics": state["topics"][canonical],
                "progress": topic_progress({canonical: state["topics"][canonical]})[canonical],
            })
    return jsonify({"success": False, "error": f"Topic '{topic_id}' not found in {canonical}."}), 404


@app.route("/api/resources", methods=["GET"])
def get_resources():
    """Returns curated study resources, optionally filtered by ?subject=."""
    subject_arg = request.args.get("subject")
    if subject_arg is None:
        return jsonify({"success": True, "resources": ds.RESOURCES,
                        "total": sum(len(v) for v in ds.RESOURCES.values())})
    subject = _match_subject(subject_arg)
    if not subject:
        return jsonify({"success": False, "error": f"Unknown subject '{subject_arg}'."}), 400
    return jsonify({"success": True, "subject": subject, "resources": ds.RESOURCES[subject],
                    "total": len(ds.RESOURCES[subject])})


@app.route("/api/achievements", methods=["GET"])
def get_achievements():
    """Returns every badge with unlocked status and a progress hint evaluated from live state."""
    badges, topics_done = evaluate_achievements()
    return jsonify({
        "success": True,
        "achievements": badges,
        "unlocked": sum(1 for b in badges if b["unlocked"]),
        "total": len(badges),
        "topics_completed": topics_done,
    })


@app.route("/api/interview-questions", methods=["GET"])
def get_interview_questions():
    """Returns interview questions, optionally filtered by ?category=HR|Technical|Behavioural."""
    category_arg = request.args.get("category")
    questions = ds.INTERVIEW_QUESTIONS
    if category_arg is not None:
        match = next((c for c in ds.INTERVIEW_CATEGORIES if c.lower() == category_arg.strip().lower()), None)
        if not match:
            return jsonify({"success": False,
                            "error": "category must be one of: " + ", ".join(ds.INTERVIEW_CATEGORIES) + "."}), 400
        questions = [q for q in questions if q["category"] == match]
    return jsonify({"success": True, "categories": ds.INTERVIEW_CATEGORIES,
                    "questions": questions, "total": len(questions)})


@app.route("/api/placement-stats", methods=["GET"])
def get_placement_stats():
    """Returns illustrative placement statistics for four batch years."""
    return jsonify({"success": True, "stats": ds.PLACEMENT_STATS, "note": ds.PLACEMENT_STATS_NOTE})


# ---------------------------------------------------------------------------
# AI CHATBOT (PrepBot) - adds POST /api/chat and GET /api/chat/status (see chatbot.py)
# ---------------------------------------------------------------------------
from chatbot import register_chatbot
register_chatbot(app, state, calculate_summary)

# ---------------------------------------------------------------------------
# REAL-TIME COMMUNITY CHAT
# ---------------------------------------------------------------------------
from chat_server import register_chat_server
register_chat_server(app)

# ---------------------------------------------------------------------------
# APPLICATION ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print(" PLACEMENT PREPARATION & TRACKING SYSTEM (FLASK BACKEND)")
    print(" AKTU B.Tech CSE (AIML) Mini-Project - Session 2026-27")
    print(" Student: Aditya Dwivedi | Roll No: 2501721530006")
    print(" Lloyd Institute of Engineering & Technology, Greater Noida")
    print("=" * 70)
    print(" Running locally at: http://127.0.0.1:5000")
    print(" Community chat: http://127.0.0.1:5000/community-chat")
    print(" Press Ctrl+C to stop the server.")
    print("=" * 70)
    import os
    port = int(os.environ.get("PORT", "5000"))
    # use_reloader=False: the auto-reloader starts the app twice and can leave a stale copy serving old code
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)
