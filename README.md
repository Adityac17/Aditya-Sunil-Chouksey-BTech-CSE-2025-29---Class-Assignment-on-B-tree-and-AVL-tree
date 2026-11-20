# University Student Record & Academic Indexing System (AVL Tree vs. B+ Tree)

**Author:** Aditya Sunil Chouksey  
**Program:** B.Tech CSE (2025–29)  
**Course:** Data Structures & Algorithms – II (DSA-II)  

---

## 📌 Overview
This project implements a **University Student Record & Academic Indexing System** in Python using **Student ID** as the primary indexing key. It compares two self-balancing search tree data structures—**AVL Tree** and **B+ Tree**—across core database operations, real-world academic queries, and automated performance benchmarks.

---

## 🚀 Features & Implemented Challenges

### Core Indexing Operations (AVL & B+ Tree)
* **Insert Record:** Adds student records while maintaining strict tree balance (rotations in AVL; node splitting in B+ Tree).
* **Point Search:** Fast $O(\log N)$ lookup by `Student ID`.
* **Range Query:** Efficiently retrieves all students within a specified `Student ID` range (e.g., `1003` to `1007`).
* **Sorted Traversal:** Displays all student records in ascending order of `Student ID`.
* **Delete Record:** Removes records cleanly while preserving tree structure.

### Bonus Challenges Implemented (5 of 8)
1. **Challenge 1 – Top CGPA Filtering:** Queries and displays high-performing students with `CGPA > 9.0`.
2. **Challenge 2 – Duplicate ID Detection:** Validates uniqueness upon insertion and raises an error if a duplicate `Student ID` is detected.
3. **Challenge 3 – CSV Data Persistence:** Automatically saves and loads student records using `students.csv`.
4. **Challenge 5 – Department-Wise Filtering:** Filters records by department (`CSE`, `IT`, `AIML`) while preserving `Student ID` ordering.
5. **Challenge 8 – Automated Performance Benchmarking:** Benchmarks bulk insertion, 1,000 point searches, and 100 range queries across 5,000 synthetic student records.

---

## 📊 Performance Comparison: AVL Tree vs. B+ Tree

| Feature / Metric | AVL Tree | B+ Tree | Key Takeaway |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $O(\log_2 N)$ | $O(\log_m N)$ *(branching factor $m$)* | **B+ Tree** has a significantly smaller height for large datasets. |
| **Data Storage** | Stored in **both** internal and leaf nodes. | Stored **only** in leaf nodes; internal nodes store routing keys. | **B+ Tree** maximizes keys per block and improves cache locality. |
| **Range Queries** | Requires recursive traversal ($O(\log N + k)$). | Locates start key, then traverses **linked leaf pointers** sequentially. | **B+ Tree** is substantially faster for range scans and sorted reports. |
| **Point Search** | Direct comparison at every visited node. | Always traverses down to the leaf level. | **AVL Tree** is slightly faster for small in-memory lookups; **B+ Tree** scales better for disk/DB indexes. |
| **Memory Overhead** | Higher per-node pointer overhead. | Amortized pointer overhead across arrays of keys. | **B+ Tree** is more space-efficient at scale. |

---

## 🛠️ How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Adityac17/Aditya-Sunil-Chouksey-BTech-CSE-2025-29---Class-Assignment-on-B-tree-and-AVL-tree.git](https://github.com/Adityac17/Aditya-Sunil-Chouksey-BTech-CSE-2025-29---Class-Assignment-on-B-tree-and-AVL-tree.git)
   cd Aditya-Sunil-Chouksey-BTech-CSE-2025-29---Class-Assignment-on-B-tree-and-AVL-tree
