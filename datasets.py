"""
Extended sample datasets for the Placement Preparation & Tracking System.

All data here is ADDITIVE to the synopsis-defined data in app.py and is kept in
plain Python lists/dicts (no database), as specified in the project synopsis.

NOTE: Company names, CTC/package figures, placement statistics and sample student
records are illustrative SAMPLE DATA for academic demonstration only.
"""

import random
from datetime import date, timedelta
from itertools import cycle

# ---------------------------------------------------------------------------
# QUESTION HELPER
# The correct option is inserted at a rotating position (0,1,2,3,0,1,...) so the
# answer key is spread evenly across all new questions.
# ---------------------------------------------------------------------------

_POSITIONS = cycle([2, 0, 3, 1])


def _q(qid, concept, difficulty, question, correct, wrongs, explanation):
    pos = next(_POSITIONS)
    options = list(wrongs)
    options.insert(pos, correct)
    return {
        "id": qid,
        "concept": concept,
        "difficulty": difficulty,
        "question": question,
        "options": options,
        "answer": pos,
        "explanation": explanation,
    }


# Difficulty labels for the ORIGINAL questions already defined in app.py
LEGACY_DIFFICULTY = {
    "syn_html": "Easy", "syn_fifo": "Easy", "syn_py_comment": "Easy",
    "syn_sql": "Easy", "syn_lifo": "Easy",
    "py2": "Easy", "py3": "Easy", "py4": "Medium", "py5": "Medium",
    "c1": "Medium", "c2": "Easy", "c3": "Medium", "c4": "Medium", "c5": "Easy",
    "dsa3": "Medium", "dsa4": "Medium", "dsa5": "Medium",
    "dbms2": "Easy", "dbms3": "Medium", "dbms4": "Medium", "dbms5": "Easy",
    "apt1": "Medium", "apt2": "Easy", "apt3": "Easy", "apt4": "Medium", "apt5": "Easy",
}

# ---------------------------------------------------------------------------
# A1. EXTRA QUESTIONS FOR THE 5 TRACKED SUBJECTS (10 new each -> 15 per subject)
# ---------------------------------------------------------------------------

EXTRA_SUBJECT_QUESTIONS = {
    "Python": [
        _q("py6", "Python types", "Easy", "What is the output of `print(type([]))` in Python?",
           "<class 'list'>", ["<class 'tuple'>", "<class 'array'>", "list"],
           "[] creates an empty list, and type() reports its class as <class 'list'>."),
        _q("py7", "Python functions", "Easy", "Which keyword is used to define a function in Python?",
           "def", ["function", "fun", "define"],
           "Functions in Python are defined with the 'def' keyword followed by the name and parameters."),
        _q("py8", "Python sets", "Medium", "What does `len({1, 2, 2, 3})` return?",
           "3", ["4", "2", "It raises an error"],
           "A set stores only unique elements, so the duplicate 2 is dropped and the set has 3 items."),
        _q("py9", "Python operators", "Medium", "What is the output of `print(10 // 3)`?",
           "3", ["3.33", "4", "3.0"],
           "The // operator performs floor division and returns the integer quotient 3 for int operands."),
        _q("py10", "Python range", "Medium", "What does `list(range(2, 10, 3))` produce?",
           "[2, 5, 8]", ["[2, 5, 8, 10]", "[3, 6, 9]", "[2, 3, 4]"],
           "range(start, stop, step) begins at 2 and adds 3 each time while the value is below 10: 2, 5, 8."),
        _q("py11", "Python exceptions", "Medium", "Which construct is used to handle exceptions in Python?",
           "try ... except", ["try ... catch", "do ... handle", "error ... rescue"],
           "Python uses try/except (optionally with else and finally) for exception handling."),
        _q("py12", "Python arguments", "Medium", "What does `*args` allow a Python function to accept?",
           "Any number of positional arguments", ["Only keyword arguments",
                                                   "A pointer to an argument",
                                                   "A single optional argument defaulting to None"],
           "*args collects extra positional arguments into a tuple; **kwargs does the same for keyword arguments."),
        _q("py13", "Python slicing", "Hard", "What is the output of `print([1, 2, 3][::-1])`?",
           "[3, 2, 1]", ["[1, 2, 3]", "[3, 2]", "It raises an error"],
           "A slice step of -1 walks the list backwards, so the list is reversed."),
        _q("py14", "Python decorators", "Hard", "What is a decorator in Python?",
           "A function that wraps another function to extend its behaviour without modifying it",
           ["A keyword used to declare constants", "A class that cannot be instantiated",
            "A comment style used for documentation"],
           "Decorators take a function, return a new function, and are applied with the @decorator syntax."),
        _q("py15", "Python floats", "Hard", "What does `print(0.1 + 0.2 == 0.3)` display in Python?",
           "False", ["True", "None", "It raises a TypeError"],
           "Binary floating point cannot represent 0.1 and 0.2 exactly, so the sum is 0.30000000000000004, not 0.3."),
    ],
    "C": [
        _q("c6", "C pointers", "Easy", "Which operator is used to get the memory address of a variable in C?",
           "&", ["*", "#", "@"],
           "The address-of operator & returns the address of its operand; * dereferences a pointer."),
        _q("c7", "C loops", "Easy", "Which C loop always executes its body at least once?",
           "do-while", ["for", "while", "foreach"],
           "A do-while loop checks its condition after running the body, so the body runs once before any test."),
        _q("c8", "C basics", "Easy", "Where does execution of a standard C program begin?",
           "main()", ["start()", "begin()", "init()"],
           "The C runtime calls main() as the program's entry point."),
        _q("c9", "C data types", "Medium", "On most modern 32-bit and 64-bit compilers, what is `sizeof(int)`?",
           "4 bytes", ["2 bytes", "8 bytes", "1 byte"],
           "int is typically 4 bytes (32 bits), though the C standard only guarantees a minimum of 16 bits."),
        _q("c10", "C strings", "Easy", "What does `strlen(\"HELLO\")` return?",
           "5", ["6", "4", "Undefined"],
           "strlen counts characters up to, but not including, the terminating '\\0', giving 5."),
        _q("c11", "C pointers", "Medium", "What does `int *p = NULL;` mean?",
           "p is a pointer that currently points to nothing", ["p is an integer equal to 100",
                                                              "p is an uninitialised pointer",
                                                              "It causes a compile-time error"],
           "NULL is a null pointer constant; a NULL pointer is a well-defined 'points nowhere' value and must not be dereferenced."),
        _q("c12", "C arrays", "Medium", "Which statement correctly declares an array of 10 integers in C?",
           "int arr[10];", ["int arr(10);", "array int[10];", "int[10] arr;"],
           "C declares arrays as type name[size];."),
        _q("c13", "C operators", "Hard", "What does `printf(\"%d\", 5 / 2);` print in C?",
           "2", ["2.5", "3", "2.0"],
           "Both operands are ints, so C performs integer division and discards the fractional part."),
        _q("c14", "C memory", "Hard", "When does a memory leak occur in C?",
           "When dynamically allocated memory is never freed", ["When a local variable goes out of scope",
                                                               "When a pointer variable is declared",
                                                               "When an array index exceeds its bounds"],
           "Memory obtained with malloc/calloc stays allocated until free() is called; losing the pointer without freeing leaks it."),
        _q("c15", "C storage", "Hard", "What does the `static` keyword do for a local variable inside a C function?",
           "It preserves the variable's value between function calls",
           ["It makes the variable accessible from other files", "It allocates the variable on the heap",
            "It makes the variable read-only"],
           "A static local variable is initialised once and keeps its value for the whole program run, though its scope stays local."),
    ],
    "DSA": [
        _q("dsa6", "DSA searching", "Easy", "What is the time complexity of binary search on a sorted array?",
           "O(log n)", ["O(n)", "O(1)", "O(n log n)"],
           "Binary search halves the search range each step, so it needs about log2(n) comparisons."),
        _q("dsa7", "DSA trees", "Easy", "Which traversal of a Binary Search Tree visits the keys in sorted order?",
           "Inorder", ["Preorder", "Postorder", "Level-order"],
           "Inorder (left, root, right) on a BST produces keys in ascending order."),
        _q("dsa8", "DSA arrays", "Easy", "What is the time complexity of accessing an array element by its index?",
           "O(1)", ["O(n)", "O(log n)", "O(n^2)"],
           "Arrays use contiguous memory, so the address of any element is computed directly from its index."),
        _q("dsa9", "DSA graphs", "Medium", "Which data structure is used to implement iterative Depth-First Search?",
           "Stack", ["Queue", "Min Heap", "Hash Table"],
           "DFS goes as deep as possible before backtracking, which matches the LIFO behaviour of a stack."),
        _q("dsa10", "DSA trees", "Medium", "What is the worst-case time to search in an unbalanced Binary Search Tree with n nodes?",
           "O(n)", ["O(log n)", "O(1)", "O(n log n)"],
           "If keys are inserted in sorted order the tree degenerates into a linked list of height n."),
        _q("dsa11", "DSA sorting", "Medium", "Which sorting algorithm is stable and guarantees O(n log n) time in the worst case?",
           "Merge Sort", ["Quick Sort", "Heap Sort", "Selection Sort"],
           "Merge sort keeps equal elements in order and always runs in O(n log n); quick sort, heap sort and selection sort are not stable."),
        _q("dsa12", "DSA trees", "Medium", "How many edges does a tree with n nodes have?",
           "n - 1", ["n", "n + 1", "n^2"],
           "A tree is a connected acyclic graph, which always has exactly n - 1 edges."),
        _q("dsa13", "DSA linked lists", "Hard", "Which technique detects a cycle in a linked list using O(1) extra space?",
           "Floyd's tortoise and hare (slow and fast pointers)", ["Storing every visited node in a hash set",
                                                                 "Sorting the nodes by address",
                                                                 "Recursively reversing the list"],
           "Two pointers moving at different speeds must meet inside a cycle, and need no extra memory."),
        _q("dsa14", "DSA heaps", "Hard", "What is the time complexity of building a binary heap from n elements using the bottom-up heapify method?",
           "O(n)", ["O(n log n)", "O(log n)", "O(n^2)"],
           "Although each sift-down can cost O(log n), most nodes sit near the leaves, so the total work sums to O(n)."),
        _q("dsa15", "DSA arrays", "Hard", "What is the amortised time complexity of appending an element to a dynamic array such as a Python list?",
           "O(1)", ["O(n)", "O(log n)", "O(n log n)"],
           "Resizing is occasionally O(n), but doubling capacity spreads that cost so each append is O(1) amortised."),
    ],
    "DBMS": [
        _q("dbms6", "SQL clauses", "Easy", "Which SQL clause filters rows BEFORE they are grouped?",
           "WHERE", ["HAVING", "GROUP BY", "ORDER BY"],
           "WHERE filters individual rows; HAVING filters groups after GROUP BY."),
        _q("dbms7", "SQL commands", "Easy", "Which SQL command quickly removes all rows from a table but keeps the table structure?",
           "TRUNCATE", ["DROP", "ALTER", "RENAME"],
           "TRUNCATE empties the table while the definition remains; DROP deletes the table itself."),
        _q("dbms8", "DBMS keys", "Easy", "What is a FOREIGN KEY?",
           "A column that refers to the primary key of another table",
           ["A column that must be unique and non-null in its own table", "A key made from every column of a table",
            "An index that speeds up ORDER BY"],
           "Foreign keys link tables and enforce referential integrity."),
        _q("dbms9", "SQL aggregates", "Medium", "Which expression counts the number of rows in a table?",
           "COUNT(*)", ["SUM(*)", "TOTAL(*)", "NUMBER(*)"],
           "COUNT(*) returns the number of rows; SUM needs a numeric column and TOTAL/NUMBER are not standard SQL aggregates."),
        _q("dbms10", "DBMS normal forms", "Medium", "Which normal form removes transitive dependencies of non-prime attributes?",
           "3NF", ["1NF", "2NF", "4NF"],
           "A relation is in 3NF if it is in 2NF and no non-prime attribute depends transitively on a candidate key."),
        _q("dbms11", "DBMS joins", "Medium", "Which JOIN returns only the rows that have matching values in both tables?",
           "INNER JOIN", ["LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN"],
           "INNER JOIN keeps only matching pairs; outer joins also keep unmatched rows."),
        _q("dbms12", "SQL queries", "Medium", "Which SQL keyword removes duplicate rows from a query result?",
           "DISTINCT", ["UNIQUE", "DIFFERENT", "REMOVE"],
           "SELECT DISTINCT returns each unique row once; UNIQUE is a constraint, not a query modifier."),
        _q("dbms13", "DBMS ACID", "Medium", "What does the letter 'D' stand for in the ACID properties?",
           "Durability", ["Dependency", "Distribution", "Deadlock-freedom"],
           "Durability guarantees that once a transaction commits, its changes survive crashes and power failures."),
        _q("dbms14", "DBMS transactions", "Hard", "Which problem occurs when a transaction reads data that another transaction has changed but not yet committed?",
           "Dirty read", ["Phantom read", "Lost update", "Deadlock"],
           "A dirty read exposes uncommitted data that may later be rolled back."),
        _q("dbms15", "DBMS indexing", "Hard", "What is the main trade-off of adding an index to a table column?",
           "Faster reads at the cost of extra storage and slower writes",
           ["Faster writes at the cost of slower reads", "Less storage at the cost of slower reads",
            "No cost, because indexes are free"],
           "Indexes speed up lookups, but every insert, update or delete must also maintain the index."),
    ],
    "Aptitude": [
        _q("apt6", "Percentages", "Easy", "What is 15% of 240?",
           "36", ["32", "30", "40"],
           "15% of 240 = 0.15 x 240 = 36."),
        _q("apt7", "Averages", "Easy", "What is the average of 10, 20, 30, 40 and 50?",
           "30", ["25", "35", "20"],
           "Sum = 150, and 150 / 5 = 30."),
        _q("apt8", "Simple Interest", "Easy", "What is the simple interest on Rs. 2000 at 5% per annum for 3 years?",
           "Rs. 300", ["Rs. 250", "Rs. 350", "Rs. 330"],
           "SI = (P x R x T) / 100 = (2000 x 5 x 3) / 100 = 300."),
        _q("apt9", "Ratio and Proportion", "Medium", "Two numbers are in the ratio 3:5 and their sum is 64. What is the larger number?",
           "40", ["24", "32", "38"],
           "Total parts = 8, so one part = 64 / 8 = 8. The larger number = 5 x 8 = 40."),
        _q("apt10", "Time and Distance", "Medium", "A car covers 240 km in 4 hours. At the same speed, how long will it take to cover 390 km?",
           "6.5 hours", ["6 hours", "7 hours", "7.5 hours"],
           "Speed = 240 / 4 = 60 km/h. Time = 390 / 60 = 6.5 hours."),
        _q("apt11", "Percentages", "Medium", "A price is increased by 20% and then decreased by 20%. What is the net change?",
           "4% decrease", ["No change", "4% increase", "2% decrease"],
           "Net factor = 1.2 x 0.8 = 0.96, which is a 4% decrease."),
        _q("apt12", "Permutations", "Medium", "In how many ways can the letters of the word CAT be arranged?",
           "6", ["3", "9", "12"],
           "Three distinct letters can be arranged in 3! = 6 ways."),
        _q("apt13", "LCM and HCF", "Medium", "What is the LCM of 12 and 18?",
           "36", ["72", "6", "216"],
           "12 = 2^2 x 3 and 18 = 2 x 3^2, so LCM = 2^2 x 3^2 = 36."),
        _q("apt14", "Pipes and Cisterns", "Hard", "Pipe A fills a tank in 12 hours, pipe B in 15 hours, and pipe C empties it in 20 hours. If all three are open, how long to fill the tank?",
           "10 hours", ["8 hours", "12 hours", "9 hours"],
           "Net rate = 1/12 + 1/15 - 1/20 = (5 + 4 - 3) / 60 = 1/10, so the tank fills in 10 hours."),
        _q("apt15", "Probability", "Hard", "Two fair dice are rolled. What is the probability that the sum is 7?",
           "1/6", ["1/12", "1/9", "5/36"],
           "There are 6 favourable outcomes (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) out of 36, giving 6/36 = 1/6."),
    ],
}

# ---------------------------------------------------------------------------
# A1. QUIZ-ONLY CATEGORIES (not tracked subjects; do not affect Placement Meter)
# ---------------------------------------------------------------------------

QUIZ_ONLY_QUESTIONS = {
    "OOP": [
        _q("oop1", "Encapsulation", "Easy", "Bundling data and methods inside a class and restricting direct access to the data is called:",
           "Encapsulation", ["Polymorphism", "Inheritance", "Abstraction"],
           "Encapsulation wraps data and the code that works on it together and controls access through access modifiers."),
        _q("oop2", "Polymorphism", "Easy", "The ability of different objects to respond to the same method call in different ways is called:",
           "Polymorphism", ["Encapsulation", "Inheritance", "Composition"],
           "Polymorphism means 'many forms': one interface, many implementations."),
        _q("oop3", "Inheritance", "Easy", "When a class acquires the properties and methods of another class, this is called:",
           "Inheritance", ["Overloading", "Encapsulation", "Instantiation"],
           "Inheritance lets a child class reuse and extend the behaviour of a parent class."),
        _q("oop4", "Objects", "Easy", "In OOP, an object is best described as:",
           "An instance of a class", ["A blueprint for a class", "A standalone function", "A primitive data type"],
           "A class is the blueprint; an object is a concrete instance created from it."),
        _q("oop5", "Overloading", "Medium", "Method overloading means:",
           "Several methods share a name but differ in their parameter lists",
           ["A subclass redefines a method of its parent", "Hiding private data from outside code",
            "Calling a constructor from another constructor"],
           "Overloading is compile-time polymorphism in languages like Java and C++. Python does not support it natively."),
        _q("oop6", "Runtime polymorphism", "Medium", "Which of the following is an example of runtime polymorphism?",
           "Method overriding", ["Method overloading", "Operator overloading", "Using static members"],
           "Overriding is resolved at runtime based on the actual object type, giving dynamic dispatch."),
        _q("oop7", "Constructors", "Medium", "A constructor is:",
           "A special method called automatically when an object is created",
           ["A method that destroys an object", "A static variable shared by all objects", "An abstract class"],
           "Constructors initialise a new object's state (for example __init__ in Python)."),
        _q("oop8", "Abstract classes", "Medium", "Which statement about an abstract class is true?",
           "It cannot be instantiated directly and may declare abstract methods",
           ["It can only contain private variables", "It must not have any child class",
            "It can be instantiated like any normal class"],
           "Abstract classes act as partial blueprints that subclasses must complete."),
        _q("oop9", "SOLID principles", "Hard", "In the SOLID principles, what does the letter 'S' stand for?",
           "Single Responsibility Principle", ["Static Binding Principle", "Simple Syntax Principle",
                                               "Substitution Safety Principle"],
           "A class should have only one reason to change, meaning it should do one job well."),
        _q("oop10", "Inheritance problems", "Hard", "The 'diamond problem' arises in:",
           "Multiple inheritance, when two parent classes share a common base class",
           ["Single inheritance with one child", "Method overloading with identical signatures",
            "Encapsulation with public fields"],
           "A class inheriting from two classes that both derive from one base can face ambiguity about which inherited version to use."),
    ],
    "Operating Systems": [
        _q("os1", "CPU scheduling", "Medium", "Which non-preemptive scheduling algorithm gives the minimum average waiting time?",
           "Shortest Job First (SJF)", ["First Come First Serve (FCFS)", "Round Robin", "Priority Scheduling"],
           "SJF is provably optimal for minimising average waiting time among non-preemptive algorithms."),
        _q("os2", "Deadlocks", "Medium", "Which of the following is NOT a necessary condition for deadlock?",
           "Preemption (resources can be forcibly taken)", ["Mutual exclusion", "Hold and wait", "Circular wait"],
           "Deadlock needs mutual exclusion, hold and wait, NO preemption, and circular wait. Allowing preemption breaks deadlock."),
        _q("os3", "Processes", "Easy", "A program in execution is called a:",
           "Process", ["Compiler", "Kernel", "Shell"],
           "A program is passive code on disk; a process is that program running, with its own state and resources."),
        _q("os4", "Memory management", "Easy", "Which memory-management technique divides physical memory into fixed-size blocks?",
           "Paging", ["Segmentation", "Swapping", "Spooling"],
           "Paging splits memory into frames and logical memory into equal-sized pages."),
        _q("os5", "OS basics", "Easy", "What is the main role of the kernel?",
           "Managing hardware resources and providing core OS services",
           ["Compiling source code into machine code", "Providing only the graphical interface",
            "Storing user files only"],
           "The kernel is the core of the OS: it handles CPU, memory, devices and system calls."),
        _q("os6", "Virtual memory", "Medium", "What is thrashing?",
           "Excessive paging, where the system spends more time swapping pages than executing",
           ["A fast cache replacement policy", "A type of CPU scheduling", "Data corruption on disk"],
           "Thrashing happens when processes lack enough frames, causing constant page faults."),
        _q("os7", "CPU scheduling", "Easy", "Which scheduling algorithm uses a fixed time quantum?",
           "Round Robin", ["Shortest Job First", "First Come First Serve", "Non-preemptive Priority"],
           "Round Robin gives each process a fixed slice of CPU time in turn."),
        _q("os8", "Synchronisation", "Medium", "What is a semaphore mainly used for?",
           "Process synchronisation and controlling access to shared resources",
           ["Allocating disk blocks", "Compressing files", "Formatting storage devices"],
           "Semaphores are counters with atomic wait/signal operations that coordinate concurrent processes."),
        _q("os9", "Page replacement", "Hard", "Which page-replacement algorithm is known to suffer from Belady's anomaly?",
           "FIFO", ["LRU", "Optimal", "None of these"],
           "With FIFO, giving a process more frames can sometimes increase page faults. LRU and Optimal are stack algorithms and do not suffer from it."),
        _q("os10", "Threads", "Hard", "Which of the following is shared by all threads of the same process?",
           "Code, data and heap memory", ["The stack", "The CPU registers", "The program counter"],
           "Threads share the process's address space (code, globals, heap) but each has its own stack, registers and program counter."),
    ],
    "Computer Networks": [
        _q("cn1", "OSI model", "Easy", "Which OSI layer is responsible for routing packets between networks?",
           "Network layer", ["Transport layer", "Data Link layer", "Session layer"],
           "The network layer (Layer 3) handles logical addressing and routing."),
        _q("cn2", "Ports", "Easy", "What is the default port number of HTTP?",
           "80", ["443", "21", "25"],
           "HTTP uses port 80 by default; HTTPS uses 443."),
        _q("cn3", "DNS", "Easy", "Which protocol translates domain names into IP addresses?",
           "DNS", ["DHCP", "ARP", "FTP"],
           "The Domain Name System maps human-readable names to IP addresses."),
        _q("cn4", "IP addressing", "Easy", "How many bits are there in an IPv4 address?",
           "32", ["64", "128", "48"],
           "IPv4 addresses are 32 bits (four octets); IPv6 addresses are 128 bits."),
        _q("cn5", "Transport layer", "Medium", "Which protocol provides connection-oriented, reliable data delivery?",
           "TCP", ["UDP", "IP", "ICMP"],
           "TCP establishes a connection and ensures ordered, acknowledged delivery; UDP is connectionless."),
        _q("cn6", "Network devices", "Medium", "Which device operates primarily at the Network layer?",
           "Router", ["Hub", "Repeater", "Layer-2 switch"],
           "Routers forward packets between networks using IP addresses."),
        _q("cn7", "Addressing", "Medium", "How many bits long is a MAC address?",
           "48", ["32", "64", "128"],
           "A MAC address is 48 bits, usually written as six hexadecimal pairs."),
        _q("cn8", "DHCP", "Medium", "What does DHCP do?",
           "Automatically assigns IP addresses to hosts", ["Translates domain names", "Encrypts web traffic",
                                                          "Transfers files between hosts"],
           "The Dynamic Host Configuration Protocol hands out IP configuration to devices when they join a network."),
        _q("cn9", "TCP", "Hard", "What is the correct sequence of a TCP three-way handshake?",
           "SYN, SYN-ACK, ACK", ["SYN, ACK, FIN", "ACK, SYN, SYN-ACK", "FIN, FIN-ACK, ACK"],
           "The client sends SYN, the server replies SYN-ACK, and the client confirms with ACK."),
        _q("cn10", "IP addressing", "Hard", "Which IPv4 address class has the default subnet mask 255.255.0.0?",
           "Class B", ["Class A", "Class C", "Class D"],
           "Class A uses 255.0.0.0, Class B uses 255.255.0.0, and Class C uses 255.255.255.0."),
    ],
    "Logical Reasoning": [
        _q("lr1", "Number series", "Easy", "Find the next number: 3, 6, 12, 24, ?",
           "48", ["36", "30", "42"],
           "Each term is double the previous one, so the next is 24 x 2 = 48."),
        _q("lr2", "Odd one out", "Easy", "Find the odd one out: Apple, Mango, Potato, Banana",
           "Potato", ["Apple", "Mango", "Banana"],
           "Apple, mango and banana are fruits, while potato is a vegetable."),
        _q("lr3", "Letter coding", "Easy", "If A=1, B=2, C=3, and so on, what is the code for 'CAB'?",
           "312", ["321", "123", "213"],
           "C=3, A=1, B=2, so CAB is written as 312."),
        _q("lr4", "Coding-decoding", "Medium", "If CAT is coded as DBU, how is DOG coded?",
           "EPH", ["EOH", "DPH", "FQI"],
           "Every letter is shifted forward by one: D->E, O->P, G->H."),
        _q("lr5", "Blood relations", "Medium", "Pointing to a man, Riya says, \"He is the son of my mother's only brother.\" How is the man related to Riya?",
           "Cousin", ["Brother", "Uncle", "Nephew"],
           "Riya's mother's brother is her maternal uncle, and his son is her cousin."),
        _q("lr6", "Direction sense", "Medium", "A person walks 5 km north, then 5 km east, then 5 km south. How far is the person from the starting point?",
           "5 km", ["10 km", "15 km", "0 km"],
           "The north and south legs cancel out, leaving only the 5 km eastward displacement."),
        _q("lr7", "Syllogism", "Medium", "All cats are animals. All animals are living beings. Which conclusion definitely follows?",
           "All cats are living beings", ["All living beings are cats", "Some animals are not living beings",
                                          "No cat is a living being"],
           "By transitivity: cats are a subset of animals, which are a subset of living beings."),
        _q("lr8", "Number series", "Medium", "Find the next number: 2, 3, 5, 7, 11, ?",
           "13", ["12", "14", "15"],
           "These are consecutive prime numbers, and the next prime after 11 is 13."),
        _q("lr9", "Clocks", "Hard", "What is the angle between the hour and minute hands of a clock at 3:30?",
           "75 degrees", ["90 degrees", "60 degrees", "105 degrees"],
           "At 3:30 the hour hand is at 3 x 30 + 15 = 105 degrees and the minute hand is at 180 degrees, a difference of 75 degrees."),
        _q("lr10", "Ages", "Hard", "A father is 3 times as old as his son. After 12 years he will be twice as old as the son. What is the son's present age?",
           "12 years", ["10 years", "15 years", "18 years"],
           "Let the son be x: 3x + 12 = 2(x + 12), so x = 12."),
    ],
}

# ---------------------------------------------------------------------------
# A2. SAMPLE STUDENTS
# ---------------------------------------------------------------------------

# Extra optional fields for the 5 existing students (ids 1-5)
SAMPLE_STUDENT_EXTRAS = {
    1: {"skills": ["Python", "HTML/CSS", "Flask"], "target_company": "Infosys", "city": "Greater Noida", "weekly_study_hours": 14},
    2: {"skills": ["Python", "Machine Learning", "SQL", "DSA"], "target_company": "Google", "city": "Noida", "weekly_study_hours": 24},
    3: {"skills": ["Java", "DSA", "SQL"], "target_company": "Wipro", "city": "Delhi", "weekly_study_hours": 16},
    4: {"skills": ["Python", "DSA", "Competitive Programming"], "target_company": "TCS", "city": "Ghaziabad", "weekly_study_hours": 18},
    5: {"skills": ["C", "Embedded Systems", "Python"], "target_company": "Cognizant", "city": "Lucknow", "weekly_study_hours": 11},
}

NEW_SAMPLE_STUDENTS = [
    {"id": 6, "name": "Neha Kapoor", "roll_no": "2501721530051", "branch": "CSE - DS", "cgpa": 9.3,
     "subjects": {"Python": 92, "C": 74, "DSA": 85, "DBMS": 88, "Aptitude": 80},
     "mock_score": "4/5 (80%)", "company": "Amazon", "placement_status": "Interview",
     "goals": "4 goals (3 completed)",
     "skills": ["Python", "Pandas", "SQL", "Machine Learning"], "target_company": "Amazon",
     "city": "Noida", "weekly_study_hours": 22},
    {"id": 7, "name": "Vikram Yadav", "roll_no": "2501721530033", "branch": "ECE", "cgpa": 7.1,
     "subjects": {"Python": 48, "C": 66, "DSA": 40, "DBMS": 52, "Aptitude": 58},
     "mock_score": "3/5 (60%)", "company": "Capgemini", "placement_status": "Applied",
     "goals": "3 goals (1 completed)",
     "skills": ["C", "Embedded C", "Verilog"], "target_company": "Capgemini",
     "city": "Ghaziabad", "weekly_study_hours": 10},
    {"id": 8, "name": "Simran Kaur", "roll_no": "2501721530064", "branch": "CSE", "cgpa": 8.8,
     "subjects": {"Python": 82, "C": 70, "DSA": 76, "DBMS": 80, "Aptitude": 72},
     "mock_score": "4/5 (80%)", "company": "Accenture", "placement_status": "Selected",
     "goals": "4 goals (4 completed)",
     "skills": ["Java", "React", "SQL"], "target_company": "Accenture",
     "city": "Delhi", "weekly_study_hours": 18},
    {"id": 9, "name": "Mohit Tiwari", "roll_no": "2501721530019", "branch": "IT", "cgpa": 6.8,
     "subjects": {"Python": 45, "C": 38, "DSA": 32, "DBMS": 50, "Aptitude": 44},
     "mock_score": "2/5 (40%)", "company": "TCS", "placement_status": "Interested",
     "goals": "3 goals (0 completed)",
     "skills": ["HTML/CSS", "JavaScript"], "target_company": "TCS",
     "city": "Greater Noida", "weekly_study_hours": 6},
    {"id": 10, "name": "Ishita Jain", "roll_no": "2501721530082", "branch": "CSE - DS", "cgpa": 9.5,
     "subjects": {"Python": 95, "C": 80, "DSA": 90, "DBMS": 92, "Aptitude": 85},
     "mock_score": "5/5 (100%)", "company": "Microsoft", "placement_status": "Selected",
     "goals": "4 goals (4 completed)",
     "skills": ["Python", "TensorFlow", "SQL", "Statistics"], "target_company": "Microsoft",
     "city": "Jaipur", "weekly_study_hours": 25},
    {"id": 11, "name": "Arjun Mishra", "roll_no": "2501721530057", "branch": "EEE", "cgpa": 7.6,
     "subjects": {"Python": 55, "C": 72, "DSA": 48, "DBMS": 46, "Aptitude": 68},
     "mock_score": "3/5 (60%)", "company": "Wipro", "placement_status": "Rejected",
     "goals": "3 goals (2 completed)",
     "skills": ["C", "MATLAB", "PLC Programming"], "target_company": "Wipro",
     "city": "Lucknow", "weekly_study_hours": 12},
    {"id": 12, "name": "Kritika Saxena", "roll_no": "2501721530038", "branch": "CSE", "cgpa": 8.3,
     "subjects": {"Python": 74, "C": 62, "DSA": 66, "DBMS": 70, "Aptitude": 78},
     "mock_score": "4/5 (80%)", "company": "Infosys", "placement_status": "Shortlisted",
     "goals": "4 goals (3 completed)",
     "skills": ["Java", "SQL", "Spring Boot"], "target_company": "Infosys",
     "city": "Meerut", "weekly_study_hours": 15},
    {"id": 13, "name": "Harsh Vardhan", "roll_no": "2501721530090", "branch": "ME", "cgpa": 6.5,
     "subjects": {"Python": 35, "C": 52, "DSA": 30, "DBMS": 40, "Aptitude": 62},
     "mock_score": "2/5 (40%)", "company": "Cognizant", "placement_status": "Interested",
     "goals": "2 goals (0 completed)",
     "skills": ["AutoCAD", "SolidWorks", "C"], "target_company": "Cognizant",
     "city": "Agra", "weekly_study_hours": 7},
    {"id": 14, "name": "Tanvi Bhatt", "roll_no": "2501721530070", "branch": "IT", "cgpa": 8.1,
     "subjects": {"Python": 70, "C": 60, "DSA": 64, "DBMS": 75, "Aptitude": 70},
     "mock_score": "3/5 (60%)", "company": "HCLTech", "placement_status": "Interview",
     "goals": "3 goals (2 completed)",
     "skills": ["Python", "MySQL", "Flask"], "target_company": "HCLTech",
     "city": "Dehradun", "weekly_study_hours": 14},
    {"id": 15, "name": "Rahul Chauhan", "roll_no": "2501721530026", "branch": "CSE", "cgpa": 8.9,
     "subjects": {"Python": 86, "C": 77, "DSA": 83, "DBMS": 79, "Aptitude": 75},
     "mock_score": "4/5 (80%)", "company": "Razorpay", "placement_status": "Interview",
     "goals": "4 goals (3 completed)",
     "skills": ["Java", "DSA", "Git", "REST APIs"], "target_company": "Razorpay",
     "city": "Pune", "weekly_study_hours": 20},
]

# ---------------------------------------------------------------------------
# A3. COMPANIES
# ---------------------------------------------------------------------------

# 7 additional companies (the original 6 stay in app.py) -> 13 total
EXTRA_COMPANY_SUGGESTIONS = [
    {
        "id": "comp_microsoft", "company": "Microsoft", "role": "Software Engineer (Entry Level)",
        "tier": "Tier-1 Product", "package_ctc": "30.0 - 48.0 LPA", "location": "Hyderabad / Noida / Bengaluru",
        "badge_color": "danger", "min_mock_pct": 85, "required_strong_subjects": ["DSA", "Python"],
        "min_subject_scores": {"DSA": 75, "Python": 70}, "min_goal_consistency": 60,
        "hiring_focus": "Advanced DSA, Problem Solving & Software Design Fundamentals",
        "description": "Highly selective product role expecting excellent DSA depth, very strong mock performance and disciplined preparation.",
    },
    {
        "id": "comp_razorpay", "company": "Razorpay", "role": "Software Development Engineer (SDE-1)",
        "tier": "Fintech Product", "package_ctc": "18.0 - 28.0 LPA", "location": "Bengaluru",
        "badge_color": "primary", "min_mock_pct": 80, "required_strong_subjects": ["DSA", "DBMS"],
        "min_subject_scores": {"DSA": 65, "DBMS": 65}, "min_goal_consistency": 40,
        "hiring_focus": "DSA, SQL & Transaction Design for Payment Systems",
        "description": "Fast-growing fintech hiring engineers with solid algorithms and strong database and transaction fundamentals.",
    },
    {
        "id": "comp_accenture", "company": "Accenture", "role": "Associate Software Engineer",
        "tier": "Consulting & Technology Services", "package_ctc": "4.5 - 6.5 LPA", "location": "Pan-India",
        "badge_color": "info", "min_mock_pct": 55, "required_strong_subjects": ["Python", "Aptitude"],
        "min_subject_scores": {"Python": 55, "Aptitude": 50}, "min_goal_consistency": 20,
        "hiring_focus": "Cognitive & Technical Assessment, Python Basics & Communication",
        "description": "Large consulting campus drive that combines cognitive aptitude screening with a technical assessment.",
    },
    {
        "id": "comp_capgemini", "company": "Capgemini", "role": "Analyst (Software Engineer)",
        "tier": "Global IT Services", "package_ctc": "3.8 - 4.5 LPA", "location": "Noida / Mumbai / Pune",
        "badge_color": "success", "min_mock_pct": 50, "required_strong_subjects": ["C", "Python"],
        "min_subject_scores": {"C": 50, "Python": 50}, "min_goal_consistency": 15,
        "hiring_focus": "Programming Fundamentals, Pseudo-code & Basic Aptitude",
        "description": "Mass-recruitment track focused on programming fundamentals and a balanced baseline across core subjects.",
    },
    {
        "id": "comp_hcltech", "company": "HCLTech", "role": "Graduate Engineer Trainee",
        "tier": "Global IT Services", "package_ctc": "3.5 - 4.5 LPA", "location": "Noida / Chennai / Lucknow",
        "badge_color": "secondary", "min_mock_pct": 60, "required_strong_subjects": ["DBMS", "C"],
        "min_subject_scores": {"DBMS": 55, "C": 55}, "min_goal_consistency": 20,
        "hiring_focus": "C Programming, DBMS & Networking Basics",
        "description": "Trainee programme looking for sound C and DBMS fundamentals along with steady preparation habits.",
    },
    {
        "id": "comp_upgrad", "company": "upGrad", "role": "Associate Software Developer",
        "tier": "EdTech Product", "package_ctc": "6.0 - 10.0 LPA", "location": "Mumbai / Remote",
        "badge_color": "warning", "min_mock_pct": 65, "required_strong_subjects": ["Python", "DSA"],
        "min_subject_scores": {"Python": 60, "DSA": 55}, "min_goal_consistency": 30,
        "hiring_focus": "Python Development, Core DSA & Product Thinking",
        "description": "EdTech product team hiring developers with solid Python skills, DSA basics and consistent daily practice.",
    },
    {
        "id": "comp_datanova", "company": "DataNova Analytics", "role": "Junior Data Scientist",
        "tier": "AI/ML Startup", "package_ctc": "10.0 - 16.0 LPA", "location": "Bengaluru / Remote",
        "badge_color": "dark", "min_mock_pct": 85, "required_strong_subjects": ["Python", "DSA"],
        "min_subject_scores": {"Python": 75, "DSA": 60}, "min_goal_consistency": 50,
        "hiring_focus": "Advanced Python, Algorithmic Thinking & Data Handling",
        "description": "Sample AI/ML startup expecting very strong Python, algorithmic fundamentals and high daily consistency.",
    },
]

# 4 additional pipeline rows (the original 4 stay first in app.py) -> 8 total
EXTRA_DEFAULT_COMPANIES = [
    {"id": 5, "company": "Capgemini", "role": "Analyst", "status": "Selected",
     "package_ctc": "3.8 LPA", "notes": "Offer letter received. Joining date awaiting confirmation."},
    {"id": 6, "company": "Zoho", "role": "Member Technical Staff", "status": "Rejected",
     "package_ctc": "6.0 LPA", "notes": "Did not clear the second technical round. Plan to reapply next year."},
    {"id": 7, "company": "HCLTech", "role": "Graduate Engineer Trainee", "status": "Applied",
     "package_ctc": "4.25 LPA", "notes": "Applied through the campus portal. Online test link expected soon."},
    {"id": 8, "company": "Cognizant", "role": "Programmer Analyst Trainee", "status": "Interested",
     "package_ctc": "4.0 LPA", "notes": "GenC registration opens next week."},
]

# ---------------------------------------------------------------------------
# A4. GOALS
# ---------------------------------------------------------------------------

# Optional metadata for the original 4 goals (text/completed stay unchanged)
GOAL_META = {
    1: {"category": "Coding", "priority": "Medium"},
    2: {"category": "Theory", "priority": "High"},
    3: {"category": "Coding", "priority": "High"},
    4: {"category": "Aptitude", "priority": "Medium"},
}

EXTRA_DEFAULT_GOALS = [
    {"id": 5, "text": "Solve 10 Percentage questions on IndiaBix", "completed": True,
     "category": "Aptitude", "priority": "Medium"},
    {"id": 6, "text": "Revise C pointers and write 3 pointer programs", "completed": False,
     "category": "Coding", "priority": "Medium"},
    {"id": 7, "text": "Prepare a 2-minute 'Tell me about yourself' answer", "completed": False,
     "category": "Interview", "priority": "High"},
    {"id": 8, "text": "Revise OS process scheduling algorithms", "completed": False,
     "category": "Theory", "priority": "Low"},
]

# ---------------------------------------------------------------------------
# A5. PROGRESS HISTORY (8 weekly snapshots ending at DEFAULT_SUBJECTS)
# ---------------------------------------------------------------------------

_PROGRESS_WEEK_STARTS = [
    "2026-09-07", "2026-09-14", "2026-09-21", "2026-09-28",
    "2026-10-05", "2026-10-12", "2026-10-19", "2026-10-26",
]
_PROGRESS_SERIES = {
    "Python":   [38, 44, 49, 54, 58, 63, 67, 70],
    "C":        [30, 34, 38, 42, 46, 50, 53, 55],
    "DSA":      [15, 19, 24, 28, 32, 36, 40, 42],
    "DBMS":     [28, 33, 38, 43, 48, 53, 57, 60],
    "Aptitude": [18, 20, 23, 25, 28, 31, 33, 35],
}

PROGRESS_HISTORY = [
    {
        "week": i + 1,
        "label": f"Week {i + 1}",
        "date": _PROGRESS_WEEK_STARTS[i],
        "subjects": {sub: vals[i] for sub, vals in _PROGRESS_SERIES.items()},
    }
    for i in range(8)
]

# ---------------------------------------------------------------------------
# A5. ACTIVITY LOG (84 days, deterministic per calendar date)
# ---------------------------------------------------------------------------

ACTIVITY_DAYS = 84


def build_activity_log(today=None):
    """
    Returns the last 84 days of {date, problems_solved, minutes_studied}, oldest first.
    Each calendar date always produces the same values (the RNG is seeded with the date).
    The most recent 6 days are always active and the day before them is always idle,
    so the demo streak stays realistic.
    """
    today = today or date.today()
    log = []
    for offset in range(ACTIVITY_DAYS - 1, -1, -1):
        day = today - timedelta(days=offset)
        rng = random.Random(day.toordinal() * 7919 + 13)
        weekend = day.weekday() >= 5
        idle = rng.random() < (0.38 if weekend else 0.16)
        if offset <= 5:
            idle = False
        elif offset == 6:
            idle = True
        if idle:
            solved, minutes = 0, 0
        else:
            solved = rng.randint(1, 4) if weekend else rng.randint(2, 9)
            minutes = solved * rng.randint(9, 22) + rng.randint(5, 30)
        log.append({"date": day.isoformat(), "problems_solved": solved, "minutes_studied": minutes})
    return log


def activity_summary(log):
    """Computes streaks and totals for an activity log (oldest first)."""
    longest = run = 0
    for entry in log:
        if entry["problems_solved"] > 0 or entry["minutes_studied"] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0

    current = 0
    idx = len(log) - 1
    # An idle "today" does not break a streak that ran up to yesterday
    if idx >= 0 and log[idx]["problems_solved"] == 0 and log[idx]["minutes_studied"] == 0:
        idx -= 1
    while idx >= 0 and (log[idx]["problems_solved"] > 0 or log[idx]["minutes_studied"] > 0):
        current += 1
        idx -= 1

    active_days = sum(1 for e in log if e["problems_solved"] > 0 or e["minutes_studied"] > 0)
    return {
        "current_streak": current,
        "longest_streak": longest,
        "total_problems_solved": sum(e["problems_solved"] for e in log),
        "total_minutes_studied": sum(e["minutes_studied"] for e in log),
        "active_days": active_days,
        "total_days": len(log),
    }


# ---------------------------------------------------------------------------
# A5. SEEDED MOCK TEST HISTORY (newest first; newest is 4/5 = 80%)
# ---------------------------------------------------------------------------

SEED_TEST_HISTORY = [
    {"id": 9001, "category": "Core Synopsis (5 Qs)", "score": 4, "total": 5, "percentage": 80,
     "rating": "Excellent", "date": "26 Oct 2026, 18:40"},
    {"id": 9002, "category": "DBMS", "score": 3, "total": 5, "percentage": 60,
     "rating": "Good", "date": "22 Oct 2026, 20:15"},
    {"id": 9003, "category": "DSA", "score": 2, "total": 5, "percentage": 40,
     "rating": "Needs Improvement", "date": "18 Oct 2026, 19:05"},
    {"id": 9004, "category": "Aptitude", "score": 5, "total": 10, "percentage": 50,
     "rating": "Needs Improvement", "date": "13 Oct 2026, 17:30"},
    {"id": 9005, "category": "Python", "score": 3, "total": 5, "percentage": 60,
     "rating": "Good", "date": "08 Oct 2026, 21:00"},
    {"id": 9006, "category": "Core Synopsis (5 Qs)", "score": 2, "total": 5, "percentage": 40,
     "rating": "Needs Improvement", "date": "02 Oct 2026, 16:20"},
]

# ---------------------------------------------------------------------------
# A5. TOPIC CHECKLIST (9 topics per tracked subject)
# ---------------------------------------------------------------------------

TOPIC_STATUSES = ["Not Started", "In Progress", "Completed"]

_C, _P, _N = "Completed", "In Progress", "Not Started"


def _topics(prefix, rows):
    return [{"id": f"{prefix}-{i + 1}", "topic": name, "status": status} for i, (name, status) in enumerate(rows)]


DEFAULT_TOPIC_CHECKLIST = {
    "Python": _topics("py", [
        ("Syntax, Variables & Input/Output", _C), ("Data Types & Operators", _C),
        ("Control Flow & Loops", _C), ("Functions & Scope", _C),
        ("Lists, Tuples, Sets & Dictionaries", _C), ("String Handling", _C),
        ("OOP in Python", _P), ("File Handling & Exceptions", _P),
        ("Decorators & Generators", _N),
    ]),
    "C": _topics("c", [
        ("Basics, Data Types & Operators", _C), ("Control Statements & Loops", _C),
        ("Functions & Recursion", _C), ("Arrays", _C), ("Strings", _C),
        ("Pointers", _P), ("Structures & Unions", _P),
        ("Dynamic Memory Allocation", _N), ("File Handling", _N),
    ]),
    "DSA": _topics("dsa", [
        ("Time & Space Complexity", _C), ("Arrays & Strings", _C),
        ("Searching & Sorting", _C), ("Stacks & Queues", _C),
        ("Linked Lists", _P), ("Recursion & Backtracking", _P),
        ("Trees & BST", _N), ("Graphs (BFS/DFS)", _N), ("Dynamic Programming", _N),
    ]),
    "DBMS": _topics("dbms", [
        ("ER Model", _C), ("Relational Model & Keys", _C), ("SQL Basics (DDL/DML)", _C),
        ("Joins & Subqueries", _C), ("Normalization", _C),
        ("Transactions & ACID", _P), ("Indexing & B+ Trees", _P),
        ("Concurrency Control", _N), ("NoSQL Basics", _N),
    ]),
    "Aptitude": _topics("apt", [
        ("Percentages", _C), ("Ratio & Proportion", _C), ("Profit & Loss", _C),
        ("Time & Work", _P), ("Time, Speed & Distance", _P),
        ("Permutations & Combinations", _N), ("Probability", _N),
        ("Number Series & Puzzles", _N), ("Data Interpretation", _N),
    ]),
}

# ---------------------------------------------------------------------------
# A5. STUDY RESOURCES (well-known sites; top-level or long-standing URLs only)
# ---------------------------------------------------------------------------

RESOURCES = {
    "Python": [
        {"title": "Official Python Tutorial", "type": "Article", "url": "https://docs.python.org/3/tutorial/", "difficulty": "Easy"},
        {"title": "W3Schools Python Tutorial", "type": "Article", "url": "https://www.w3schools.com/python/", "difficulty": "Easy"},
        {"title": "freeCodeCamp Python Learning Path", "type": "Course", "url": "https://www.freecodecamp.org/", "difficulty": "Easy"},
        {"title": "GeeksforGeeks Python Programming", "type": "Article", "url": "https://www.geeksforgeeks.org/", "difficulty": "Medium"},
        {"title": "NPTEL Python Programming Lectures", "type": "Video", "url": "https://nptel.ac.in/", "difficulty": "Medium"},
        {"title": "LeetCode Problem Set (solve in Python)", "type": "Practice", "url": "https://leetcode.com/problemset/", "difficulty": "Hard"},
    ],
    "C": [
        {"title": "W3Schools C Tutorial", "type": "Article", "url": "https://www.w3schools.com/c/", "difficulty": "Easy"},
        {"title": "GeeksforGeeks C Programming", "type": "Article", "url": "https://www.geeksforgeeks.org/", "difficulty": "Easy"},
        {"title": "NPTEL Programming in C Lectures", "type": "Video", "url": "https://nptel.ac.in/", "difficulty": "Medium"},
        {"title": "freeCodeCamp C Programming Tutorials", "type": "Video", "url": "https://www.freecodecamp.org/", "difficulty": "Medium"},
        {"title": "LeetCode Problem Set (solve in C)", "type": "Practice", "url": "https://leetcode.com/problemset/", "difficulty": "Hard"},
    ],
    "DSA": [
        {"title": "W3Schools DSA Tutorial", "type": "Article", "url": "https://www.w3schools.com/dsa/", "difficulty": "Easy"},
        {"title": "GeeksforGeeks Data Structures & Algorithms", "type": "Article", "url": "https://www.geeksforgeeks.org/", "difficulty": "Medium"},
        {"title": "NPTEL Data Structures & Algorithms Lectures", "type": "Video", "url": "https://nptel.ac.in/", "difficulty": "Medium"},
        {"title": "freeCodeCamp Algorithms Courses", "type": "Course", "url": "https://www.freecodecamp.org/", "difficulty": "Medium"},
        {"title": "LeetCode Explore Cards", "type": "Course", "url": "https://leetcode.com/explore/", "difficulty": "Medium"},
        {"title": "LeetCode Problem Set", "type": "Practice", "url": "https://leetcode.com/problemset/", "difficulty": "Hard"},
    ],
    "DBMS": [
        {"title": "W3Schools SQL Tutorial", "type": "Article", "url": "https://www.w3schools.com/sql/", "difficulty": "Easy"},
        {"title": "GeeksforGeeks DBMS Tutorial", "type": "Article", "url": "https://www.geeksforgeeks.org/", "difficulty": "Medium"},
        {"title": "NPTEL Database Management System Lectures", "type": "Video", "url": "https://nptel.ac.in/", "difficulty": "Medium"},
        {"title": "freeCodeCamp Relational Database Course", "type": "Course", "url": "https://www.freecodecamp.org/", "difficulty": "Medium"},
        {"title": "LeetCode SQL / Database Problems", "type": "Practice", "url": "https://leetcode.com/problemset/", "difficulty": "Hard"},
    ],
    "Aptitude": [
        {"title": "IndiaBix Aptitude Questions", "type": "Practice", "url": "https://www.indiabix.com/aptitude/questions-and-answers/", "difficulty": "Easy"},
        {"title": "IndiaBix Logical Reasoning", "type": "Practice", "url": "https://www.indiabix.com/logical-reasoning/questions-and-answers/", "difficulty": "Medium"},
        {"title": "IndiaBix Data Interpretation", "type": "Practice", "url": "https://www.indiabix.com/data-interpretation/questions-and-answers/", "difficulty": "Medium"},
        {"title": "IndiaBix Verbal Ability", "type": "Practice", "url": "https://www.indiabix.com/verbal-ability/questions-and-answers/", "difficulty": "Easy"},
        {"title": "GeeksforGeeks Aptitude Preparation", "type": "Article", "url": "https://www.geeksforgeeks.org/", "difficulty": "Medium"},
    ],
}

# ---------------------------------------------------------------------------
# A5. INTERVIEW QUESTIONS (25)
# ---------------------------------------------------------------------------

INTERVIEW_CATEGORIES = ["HR", "Technical", "Behavioural"]

INTERVIEW_QUESTIONS = [
    # HR (8)
    {"id": 1, "category": "HR", "difficulty": "Easy", "question": "Tell me about yourself.",
     "tip": "Keep it to about 2 minutes: education, key skills or projects, and why you want this role."},
    {"id": 2, "category": "HR", "difficulty": "Easy", "question": "Why do you want to join our company?",
     "tip": "Mention something specific about the company's work or culture and link it to your goals."},
    {"id": 3, "category": "HR", "difficulty": "Medium", "question": "What are your strengths and weaknesses?",
     "tip": "Pick real strengths with an example, and a genuine weakness you are actively improving."},
    {"id": 4, "category": "HR", "difficulty": "Easy", "question": "Where do you see yourself in five years?",
     "tip": "Show ambition tied to growth in the role, such as skills gained and responsibility taken on."},
    {"id": 5, "category": "HR", "difficulty": "Medium", "question": "Are you willing to relocate or work in shifts?",
     "tip": "Be honest. If flexible, say so clearly; if not, explain constraints politely."},
    {"id": 6, "category": "HR", "difficulty": "Medium", "question": "Why should we hire you over other candidates?",
     "tip": "Match your skills and projects to the job description and give one concrete proof point."},
    {"id": 7, "category": "HR", "difficulty": "Easy", "question": "What do you know about our company?",
     "tip": "Research products, recent news, and values beforehand, then mention two or three facts."},
    {"id": 8, "category": "HR", "difficulty": "Hard", "question": "What are your salary expectations?",
     "tip": "Research the typical fresher range, stay flexible, and say you value learning and growth."},
    # Technical (10)
    {"id": 9, "category": "Technical", "difficulty": "Easy", "question": "What is the difference between a list and a tuple in Python?",
     "tip": "Lists are mutable and tuples are immutable. Mention hashability and typical use cases."},
    {"id": 10, "category": "Technical", "difficulty": "Easy", "question": "Explain the difference between a stack and a queue.",
     "tip": "LIFO versus FIFO, with one real-world example each (undo history, print queue)."},
    {"id": 11, "category": "Technical", "difficulty": "Medium", "question": "What is normalization and why is it used in databases?",
     "tip": "Reduces redundancy and anomalies. Briefly describe 1NF, 2NF, 3NF and BCNF."},
    {"id": 12, "category": "Technical", "difficulty": "Medium", "question": "Explain the four pillars of Object-Oriented Programming.",
     "tip": "Encapsulation, abstraction, inheritance, polymorphism, each with a one-line example."},
    {"id": 13, "category": "Technical", "difficulty": "Medium", "question": "What is the difference between a process and a thread?",
     "tip": "Processes have separate memory; threads share memory inside a process and are lighter weight."},
    {"id": 14, "category": "Technical", "difficulty": "Medium", "question": "What happens when you type a URL into a browser and press Enter?",
     "tip": "DNS lookup, TCP/TLS connection, HTTP request, server response, then rendering."},
    {"id": 15, "category": "Technical", "difficulty": "Medium", "question": "Explain the difference between INNER JOIN and LEFT JOIN with an example.",
     "tip": "Use two small tables on a whiteboard to show which rows each join keeps."},
    {"id": 16, "category": "Technical", "difficulty": "Hard", "question": "How would you detect a cycle in a linked list?",
     "tip": "Describe Floyd's slow/fast pointers and state O(n) time with O(1) space."},
    {"id": 17, "category": "Technical", "difficulty": "Hard", "question": "Explain time and space complexity with an example of binary search.",
     "tip": "Show how the search range halves each step, giving O(log n) time and O(1) iterative space."},
    {"id": 18, "category": "Technical", "difficulty": "Hard", "question": "What are ACID properties? Why do they matter in transactions?",
     "tip": "Define each letter and use a bank-transfer example to show why atomicity matters."},
    # Behavioural (7)
    {"id": 19, "category": "Behavioural", "difficulty": "Medium", "question": "Describe a time you faced a difficult challenge in a project and how you handled it.",
     "tip": "Use the STAR method: Situation, Task, Action, Result, and quantify the result if possible."},
    {"id": 20, "category": "Behavioural", "difficulty": "Medium", "question": "Tell me about a time you worked in a team and there was a disagreement.",
     "tip": "Focus on listening, finding common ground, and the outcome, not on blaming others."},
    {"id": 21, "category": "Behavioural", "difficulty": "Medium", "question": "Describe a situation where you had to learn a new technology quickly.",
     "tip": "Explain your learning plan, resources used, and what you built to prove the skill."},
    {"id": 22, "category": "Behavioural", "difficulty": "Hard", "question": "Tell me about a time you failed. What did you learn?",
     "tip": "Choose a real but modest failure, take ownership, and emphasise the lesson and change afterward."},
    {"id": 23, "category": "Behavioural", "difficulty": "Medium", "question": "How do you prioritise tasks when you have multiple deadlines?",
     "tip": "Mention urgency versus importance, communicating early, and a concrete example from academics."},
    {"id": 24, "category": "Behavioural", "difficulty": "Easy", "question": "Describe a time you took the initiative.",
     "tip": "Pick an example where you noticed a problem and acted without being asked."},
    {"id": 25, "category": "Behavioural", "difficulty": "Hard", "question": "Tell me about a time you had to meet a tight deadline.",
     "tip": "Show planning, trade-offs you made, and how you kept quality while delivering on time."},
]

# ---------------------------------------------------------------------------
# A5. PLACEMENT STATS (illustrative sample data)
# ---------------------------------------------------------------------------

PLACEMENT_STATS = [
    {"year": 2023, "offers": 142, "average_ctc": 4.1, "highest_ctc": 18.0,
     "top_recruiters": ["TCS", "Infosys", "Wipro", "Cognizant"]},
    {"year": 2024, "offers": 168, "average_ctc": 4.4, "highest_ctc": 24.0,
     "top_recruiters": ["TCS", "Infosys", "Capgemini", "Accenture"]},
    {"year": 2025, "offers": 190, "average_ctc": 4.8, "highest_ctc": 32.0,
     "top_recruiters": ["Infosys", "Accenture", "HCLTech", "Amazon"]},
    {"year": 2026, "offers": 215, "average_ctc": 5.2, "highest_ctc": 41.0,
     "top_recruiters": ["Amazon", "Microsoft", "Accenture", "Capgemini"]},
]
PLACEMENT_STATS_NOTE = "Illustrative sample data for academic demonstration only."
