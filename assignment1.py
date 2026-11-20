import csv
import os
import time
import random


# ==========================================
# 1. STUDENT RECORD STRUCTURE
# ==========================================
class Student:
   def __init__(self, student_id, name, department, semester, cgpa, city="Unknown"):
       self.student_id = int(student_id)
       self.name = str(name)
       self.department = str(department)
       self.semester = int(semester)
       self.cgpa = float(cgpa)
       self.city = str(city)


   def to_list(self):
       return [self.student_id, self.name, self.department, self.semester, self.cgpa, self.city]


   def __str__(self):
       return (f"ID: {self.student_id:<5} | Name: {self.name:<15} | Dept: {self.department:<5} | "
               f"Sem: {self.semester} | CGPA: {self.cgpa:<4} | City: {self.city}")




# ==========================================
# 2. AVL TREE IMPLEMENTATION
# ==========================================
class AVLNode:
   def __init__(self, student):
       self.student = student
       self.key = student.student_id
       self.left = None
       self.right = None
       self.height = 1


class AVLTree:
   def __init__(self):
       self.root = None


   def _get_height(self, node):
       return node.height if node else 0


   def _get_balance(self, node):
       return self._get_height(node.left) - self._get_height(node.right) if node else 0


   def _right_rotate(self, y):
       x = y.left
       T2 = x.right
       x.right = y
       y.left = T2
       y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
       x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
       return x


   def _left_rotate(self, x):
       y = x.right
       T2 = y.left
       y.left = x
       x.right = T2
       x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
       y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
       return y


   # Challenge 2: Duplicate Record Detection included
   def insert(self, student):
       if self.search(student.student_id) is not None:
           raise ValueError(f"[AVL Error] Duplicate Student ID {student.student_id} cannot be inserted.")
       self.root = self._insert(self.root, student)


   def _insert(self, node, student):
       if not node:
           return AVLNode(student)
       if student.student_id < node.key:
           node.left = self._insert(node.left, student)
       else:
           node.right = self._insert(node.right, student)


       node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
       balance = self._get_balance(node)


       # Left Left
       if balance > 1 and student.student_id < node.left.key:
           return self._right_rotate(node)
       # Right Right
       if balance < -1 and student.student_id > node.right.key:
           return self._left_rotate(node)
       # Left Right
       if balance > 1 and student.student_id > node.left.key:
           node.left = self._left_rotate(node.left)
           return self._right_rotate(node)
       # Right Left
       if balance < -1 and student.student_id < node.right.key:
           node.right = self._right_rotate(node.right)
           return self._left_rotate(node)


       return node


   def search(self, student_id):
       curr = self.root
       while curr:
           if student_id == curr.key:
               return curr.student
           elif student_id < curr.key:
               curr = curr.left
           else:
               curr = curr.right
       return None


   def _get_min_value_node(self, node):
       curr = node
       while curr.left:
           curr = curr.left
       return curr


   def delete(self, student_id):
       self.root = self._delete(self.root, student_id)


   def _delete(self, node, key):
       if not node:
           return node
       if key < node.key:
           node.left = self._delete(node.left, key)
       elif key > node.key:
           node.right = self._delete(node.right, key)
       else:
           if not node.left:
               return node.right
           elif not node.right:
               return node.left
           temp = self._get_min_value_node(node.right)
           node.key = temp.key
           node.student = temp.student
           node.right = self._delete(node.right, temp.key)


       node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
       balance = self._get_balance(node)


       if balance > 1 and self._get_balance(node.left) >= 0:
           return self._right_rotate(node)
       if balance > 1 and self._get_balance(node.left) < 0:
           node.left = self._left_rotate(node.left)
           return self._right_rotate(node)
       if balance < -1 and self._get_balance(node.right) <= 0:
           return self._left_rotate(node)
       if balance < -1 and self._get_balance(node.right) > 0:
           node.right = self._right_rotate(node.right)
           return self._left_rotate(node)


       return node


   def get_sorted_records(self):
       result = []
       self._inorder(self.root, result)
       return result


   def _inorder(self, node, result):
       if node:
           self._inorder(node.left, result)
           result.append(node.student)
           self._inorder(node.right, result)


   def range_search(self, min_id, max_id):
       result = []
       self._range_search(self.root, min_id, max_id, result)
       return result


   def _range_search(self, node, min_id, max_id, result):
       if not node:
           return
       if min_id < node.key:
           self._range_search(node.left, min_id, max_id, result)
       if min_id <= node.key <= max_id:
           result.append(node.student)
       if max_id > node.key:
           self._range_search(node.right, min_id, max_id, result)




# ==========================================
# 3. B+ TREE IMPLEMENTATION
# ==========================================
class BPlusNode:
   def __init__(self, is_leaf=False):
       self.is_leaf = is_leaf
       self.keys = []
       self.children = [] # Stores child nodes if internal, Student objects if leaf
       self.next = None     # Pointer to next leaf node for fast range queries


class BPlusTree:
   def __init__(self, order=4):
       self.root = BPlusNode(is_leaf=True)
       self.order = order


   def search(self, student_id):
       curr = self.root
       while not curr.is_leaf:
           i = 0
           while i < len(curr.keys) and student_id >= curr.keys[i]:
               i += 1
           curr = curr.children[i]
       for i, key in enumerate(curr.keys):
           if key == student_id:
               return curr.children[i]
       return None


   # Challenge 2: Duplicate Record Detection included
   def insert(self, student):
       if self.search(student.student_id) is not None:
           raise ValueError(f"[B+ Tree Error] Duplicate Student ID {student.student_id} cannot be inserted.")
      
       root = self.root
       if len(root.keys) == self.order - 1:
           new_root = BPlusNode(is_leaf=False)
           new_root.children.append(self.root)
           self._split_child(new_root, 0)
           self.root = new_root
       self._insert_non_full(self.root, student)


   def _split_child(self, parent, index):
       order = self.order
       node = parent.children[index]
       mid = len(node.keys) // 2
       new_node = BPlusNode(is_leaf=node.is_leaf)


       if node.is_leaf:
           new_node.keys = node.keys[mid:]
           new_node.children = node.children[mid:]
           node.keys = node.keys[:mid]
           node.children = node.children[:mid]
          
           new_node.next = node.next
           node.next = new_node
          
           parent.keys.insert(index, new_node.keys[0])
           parent.children.insert(index + 1, new_node)
       else:
           promote_key = node.keys[mid]
           new_node.keys = node.keys[mid + 1:]
           new_node.children = node.children[mid + 1:]
           node.keys = node.keys[:mid]
           node.children = node.children[:mid + 1]
          
           parent.keys.insert(index, promote_key)
           parent.children.insert(index + 1, new_node)


   def _insert_non_full(self, node, student):
       if node.is_leaf:
           i = 0
           while i < len(node.keys) and student.student_id > node.keys[i]:
               i += 1
           node.keys.insert(i, student.student_id)
           node.children.insert(i, student)
       else:
           i = 0
           while i < len(node.keys) and student.student_id >= node.keys[i]:
               i += 1
           if len(node.children[i].keys) == self.order - 1:
               self._split_child(node, i)
               if student.student_id >= node.keys[i]:
                   i += 1
           self._insert_non_full(node.children[i], student)


   def delete(self, student_id):
       # Standard leaf-level deletion (sufficient for functional academic simulation)
       curr = self.root
       while not curr.is_leaf:
           i = 0
           while i < len(curr.keys) and student_id >= curr.keys[i]:
               i += 1
           curr = curr.children[i]
       if student_id in curr.keys:
           idx = curr.keys.index(student_id)
           curr.keys.pop(idx)
           curr.children.pop(idx)


   def get_sorted_records(self):
       curr = self.root
       while not curr.is_leaf:
           curr = curr.children[0]
       result = []
       while curr:
           result.extend(curr.children)
           curr = curr.next
       return result


   def range_search(self, min_id, max_id):
       curr = self.root
       while not curr.is_leaf:
           i = 0
           while i < len(curr.keys) and min_id >= curr.keys[i]:
               i += 1
           curr = curr.children[i]
      
       result = []
       while curr:
           for i, key in enumerate(curr.keys):
               if min_id <= key <= max_id:
                   result.append(curr.children[i])
               elif key > max_id:
                   return result
           curr = curr.next
       return result




# ==========================================
# 4. CHALLENGES & SYSTEM MANAGER
# ==========================================
class UniversitySystem:
   def __init__(self, filename="students.csv"):
       self.avl = AVLTree()
       self.bplus = BPlusTree(order=4)
       self.filename = filename


   def add_student(self, student):
       self.avl.insert(student)
       self.bplus.insert(student)


   # Challenge 1: Top CGPA Students (> 9.0)
   def get_top_cgpa_students(self, threshold=9.0):
       all_students = self.bplus.get_sorted_records()
       return [s for s in all_students if s.cgpa > threshold]


   # Challenge 5: Department Filtering (maintaining ID-based indexing)
   def filter_by_department(self, dept):
       all_students = self.bplus.get_sorted_records() # Already sorted by ID
       return [s for s in all_students if s.department.lower() == dept.lower()]


   # Challenge 3: Data Persistence (Save & Load CSV)
   def save_to_csv(self):
       records = self.bplus.get_sorted_records()
       with open(self.filename, mode="w", newline="") as file:
           writer = csv.writer(file)
           writer.writerow(["Student ID", "Student Name", "Department", "Semester", "CGPA", "City"])
           for s in records:
               writer.writerow(s.to_list())
       print(f"Saved {len(records)} records to {self.filename}.")


   def load_from_csv(self):
       if not os.path.exists(self.filename):
           return False
       with open(self.filename, mode="r") as file:
           reader = csv.DictReader(file)
           for row in reader:
               s = Student(row["Student ID"], row["Student Name"], row["Department"],
                           row["Semester"], row["CGPA"], row["City"])
               self.add_student(s)
       return True


   # Challenge 8: Automated Performance Comparison
   def run_automated_benchmark(self, num_records=5000):
       print("\n" + "="*55)
       print(f"CHALLENGE 8: AUTOMATED PERFORMANCE REPORT ({num_records} Records)")
       print("="*55)
      
       test_avl = AVLTree()
       test_bplus = BPlusTree(order=32) # Realistic disk-block branching factor
      
       ids = random.sample(range(10000, 10000 + num_records * 2), num_records)
       students = [Student(sid, f"Student_{sid}", random.choice(["CSE", "IT", "AIML"]),
                           random.randint(1, 8), round(random.uniform(6.0, 9.9), 2), "Mumbai")
                   for sid in ids]


       # 1. Insertion Benchmark
       t0 = time.perf_counter()
       for s in students: test_avl.insert(s)
       avl_insert_time = (time.perf_counter() - t0) * 1000


       t0 = time.perf_counter()
       for s in students: test_bplus.insert(s)
       bplus_insert_time = (time.perf_counter() - t0) * 1000


       # 2. Exact Search Benchmark (1,000 queries)
       search_ids = random.sample(ids, 1000)
       t0 = time.perf_counter()
       for sid in search_ids: test_avl.search(sid)
       avl_search_time = (time.perf_counter() - t0) * 1000


       t0 = time.perf_counter()
       for sid in search_ids: test_bplus.search(sid)
       bplus_search_time = (time.perf_counter() - t0) * 1000


       # 3. Range Search Benchmark (100 range queries)
       t0 = time.perf_counter()
       for _ in range(100): test_avl.range_search(12000, 15000)
       avl_range_time = (time.perf_counter() - t0) * 1000


       t0 = time.perf_counter()
       for _ in range(100): test_bplus.range_search(12000, 15000)
       bplus_range_time = (time.perf_counter() - t0) * 1000


       print(f"{'Operation':<25} | {'AVL Tree (ms)':<15} | {'B+ Tree (ms)':<15}")
       print("-" * 55)
       print(f"{'Bulk Insertion':<25} | {avl_insert_time:<15.3f} | {bplus_insert_time:<15.3f}")
       print(f"{'1,000 Point Searches':<25} | {avl_search_time:<15.3f} | {bplus_search_time:<15.3f}")
       print(f"{'100 Range Queries':<25} | {avl_range_time:<15.3f} | {bplus_range_time:<15.3f}")
       print("="*55)




# ==========================================
# 5. MAIN EXECUTION (USING DATASET FROM DOC)
# ==========================================
if __name__ == "__main__":
   sys_db = UniversitySystem()


   # Load from CSV if exists, otherwise load initial dataset from assignment
   if not sys_db.load_from_csv():
       initial_data = [
           Student(1001, "Aditi Sharma", "CSE", 5, 8.7, "Pune"),
           Student(1002, "Rahul Patil", "IT", 5, 7.9, "Mumbai"),
           Student(1003, "Neha Desai", "AIML", 3, 9.1, "Nashik"),
           Student(1004, "Arjun Mehta", "CSE", 7, 8.2, "Nagpur"),
           Student(1005, "Sneha Kulkarni", "IT", 3, 8.5, "Pune"),
           Student(1006, "Rohan Shah", "AIML", 5, 7.6, "Thane"),
           Student(1007, "Priya Nair", "CSE", 3, 9.3, "Mumbai"),
           Student(1008, "Karan Joshi", "IT", 7, 8.0, "Kharghar"),
           Student(1009, "Isha Gupta", "AIML", 5, 8.9, "Navi Mumbai"),
           Student(1010, "Aditya Rao", "CSE", 7, 7.8, "Panvel")
       ]
       for student in initial_data:
           sys_db.add_student(student)
       sys_db.save_to_csv() # Challenge 3


   print("\n--- 1. SORTED RECORDS (B+ TREE LEAF TRAVERSAL) ---")
   for s in sys_db.bplus.get_sorted_records():
       print(s)


   print("\n--- 2. POINT SEARCH (ID: 1007) ---")
   print("AVL Result:   ", sys_db.avl.search(1007))
   print("B+ Tree Result:", sys_db.bplus.search(1007))


   print("\n--- 3. RANGE QUERY (IDs 1003 to 1007) ---")
   for s in sys_db.bplus.range_search(1003, 1007):
       print(s)


   print("\n--- 4. CHALLENGE 1: TOP CGPA STUDENTS (> 9.0) ---")
   for s in sys_db.get_top_cgpa_students(9.0):
       print(s)


   print("\n--- 5. CHALLENGE 2: DUPLICATE ID DETECTION ---")
   try:
       sys_db.add_student(Student(1001, "Duplicate User", "CSE", 1, 8.0, "Mumbai"))
   except ValueError as e:
       print(e)


   print("\n--- 6. CHALLENGE 5: DEPARTMENT FILTERING (CSE) ---")
   for s in sys_db.filter_by_department("CSE"):
       print(s)


   # Challenge 8: Run automated comparison
   sys_db.run_automated_benchmark(5000)

