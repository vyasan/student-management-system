# ╔══════════════════════════════════════════════╗
# ║     STUDENT MANAGEMENT SYSTEM                ║
# ║     Phase 1 Module 1 — Capstone Project      ║
# ║     Built with: OOP, CSV, Exceptions,        ║
# ║     Modules, Collections, String Handling    ║
# ╚══════════════════════════════════════════════╝

import csv
import os
import random
import shutil
from datetime import datetime, date
from math import floor

# ── CONSTANTS ─────────────────────────────────────────────
INSTITUTE_NAME  = "Edvube"
PROGRAM_NAME    = "AI & ML Training Program"
CSV_FILE        = "students.csv"
BACKUP_FILE     = "students_backup.csv"
REPORT_FILE     = "class_report.txt"

SUBJECTS        = ["Python", "Mathematics",
                   "Data Science", "AI Fundamentals",
                   "Communication Skills"]

GRADE_SCALE     = (
    (90, "A+", "Outstanding"),
    (75, "A",  "Excellent"),
    (60, "B",  "Good"),
    (40, "C",  "Pass"),
    (0,  "F",  "Fail"),
)

CSV_FIELDS = [
    "roll", "name", "age", "email", "phone",
    "city", "course", "batch",
    "python_marks", "maths_marks",
    "datasci_marks", "ai_marks", "comm_marks",
    "attendance_present", "attendance_total",
    "enrollment_date"
]

# ── CLASS 1: SubjectRecord ─────────────────────────────────

class SubjectRecord:
    """Stores marks and calculates grade for one subject."""

    def __init__(self, subject_name,
                 marks_obtained, total_marks=100):
        self.subject_name    = subject_name
        self.marks_obtained  = float(marks_obtained)
        self.total_marks     = float(total_marks)

    def percentage(self):
        if self.total_marks == 0:
            return 0.0
        return round(
            (self.marks_obtained / self.total_marks) * 100, 2
        )

    def grade(self):
        pct = self.percentage()
        for min_marks, grade, _ in GRADE_SCALE:
            if pct >= min_marks:
                return grade
        return "F"

    def status(self):
        return "Pass" if self.percentage() >= 40 else "Fail"

    def __str__(self):
        return (
            f"{self.subject_name:<22}"
            f"  {self.marks_obtained:>5.1f}/{self.total_marks:<6.0f}"
            f"  {self.percentage():>6.2f}%"
            f"  {self.grade():<3}"
            f"  {self.status()}"
        )


# ── CLASS 2: Student ──────────────────────────────────────

class Student:
    """
    Represents a single enrolled student.
    Stores personal info, subject marks,
    attendance, and computes analytics.
    """

    institute   = INSTITUTE_NAME
    program     = PROGRAM_NAME
    total_enrolled = 0

    def __init__(self, roll, name, age, email,
                 phone, city, course, batch,
                 marks_list=None,
                 attendance_present=0,
                 attendance_total=0,
                 enrollment_date=None):

        # Personal attributes
        self.roll    = int(roll)
        self.name    = name.strip().title()
        self.age     = int(age)
        self.email   = email.strip().lower()
        self.phone   = str(phone).strip()
        self.city    = city.strip().title()
        self.course  = course.strip()
        self.batch   = batch.strip()

        # Subject records
        if marks_list is None:
            marks_list = [0.0] * len(SUBJECTS)

        self.subjects = [
            SubjectRecord(SUBJECTS[i], marks_list[i])
            for i in range(len(SUBJECTS))
        ]

        # Attendance
        self.attendance_present = int(attendance_present)
        self.attendance_total   = int(attendance_total)

        # Enrollment date
        self.enrollment_date = (
            enrollment_date
            if enrollment_date
            else date.today().strftime("%d/%m/%Y")
        )

        Student.total_enrolled += 1

    # ── CALCULATED PROPERTIES ─────────────────────────

    def average_marks(self):
        all_marks = [s.marks_obtained for s in self.subjects]
        if not all_marks:
            return 0.0
        return round(sum(all_marks) / len(all_marks), 2)

    def overall_percentage(self):
        all_pct = [s.percentage() for s in self.subjects]
        if not all_pct:
            return 0.0
        return round(sum(all_pct) / len(all_pct), 2)

    def overall_grade(self):
        pct = self.overall_percentage()
        for min_marks, grade, _ in GRADE_SCALE:
            if pct >= min_marks:
                return grade
        return "F"

    def overall_status(self):
        # Fail if ANY subject is below 40%
        for s in self.subjects:
            if s.percentage() < 40:
                return "Fail"
        return "Pass"

    def attendance_percentage(self):
        if self.attendance_total == 0:
            return 0.0
        return round(
            (self.attendance_present
             / self.attendance_total) * 100, 2
        )

    def attendance_status(self):
        pct = self.attendance_percentage()
        if pct >= 75:
            return "Regular"
        elif pct >= 60:
            return "Low Attendance"
        else:
            return "Detained Risk"

    def is_scholarship_eligible(self):
        return (self.overall_percentage() >= 85
                and self.attendance_percentage() >= 90)

    # ── DATA METHODS ──────────────────────────────────

    def update_marks(self, subject_index, new_marks):
        if not 0 <= subject_index < len(self.subjects):
            raise IndexError("Invalid subject index.")
        if not 0 <= float(new_marks) <= 100:
            raise ValueError(
                "Marks must be between 0 and 100."
            )
        old = self.subjects[subject_index].marks_obtained
        self.subjects[subject_index].marks_obtained = float(
            new_marks
        )
        return old, float(new_marks)

    def update_attendance(self, present, total):
        if present < 0 or total < 0:
            raise ValueError(
                "Attendance values cannot be negative."
            )
        if present > total:
            raise ValueError(
                "Present days cannot exceed total days."
            )
        self.attendance_present = present
        self.attendance_total   = total

    def to_dict(self):
        marks = [s.marks_obtained for s in self.subjects]
        return {
            "roll"              : self.roll,
            "name"              : self.name,
            "age"               : self.age,
            "email"             : self.email,
            "phone"             : self.phone,
            "city"              : self.city,
            "course"            : self.course,
            "batch"             : self.batch,
            "python_marks"      : marks[0],
            "maths_marks"       : marks[1],
            "datasci_marks"     : marks[2],
            "ai_marks"          : marks[3],
            "comm_marks"        : marks[4],
            "attendance_present": self.attendance_present,
            "attendance_total"  : self.attendance_total,
            "enrollment_date"   : self.enrollment_date
        }

    def __str__(self):
        return (
            f"{self.roll:<5} "
            f"{self.name:<22} "
            f"{self.course:<12} "
            f"{self.overall_percentage():>6.2f}% "
            f"{self.overall_grade():<3} "
            f"{self.overall_status():<5} "
            f"{self.attendance_percentage():>6.1f}%"
        )


# ── CLASS 3: StudentDatabase ──────────────────────────────

class StudentDatabase:
    """
    Manages the full collection of students.
    Handles all CRUD operations and CSV persistence.
    """

    def __init__(self):
        self.students  = []
        self._load()

    # ── PERSISTENCE ───────────────────────────────────

    def _load(self):
        if not os.path.exists(CSV_FILE):
            print("No existing data found. Fresh start.")
            return
        try:
            loaded = 0
            with open(CSV_FILE, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    marks_list = [
                        float(row["python_marks"]),
                        float(row["maths_marks"]),
                        float(row["datasci_marks"]),
                        float(row["ai_marks"]),
                        float(row["comm_marks"]),
                    ]
                    s = Student(
                        roll     = row["roll"],
                        name     = row["name"],
                        age      = row["age"],
                        email    = row["email"],
                        phone    = row["phone"],
                        city     = row["city"],
                        course   = row["course"],
                        batch    = row["batch"],
                        marks_list          = marks_list,
                        attendance_present  = row[
                            "attendance_present"
                        ],
                        attendance_total    = row[
                            "attendance_total"
                        ],
                        enrollment_date     = row[
                            "enrollment_date"
                        ]
                    )
                    self.students.append(s)
                    loaded += 1
            print(f"Loaded {loaded} student(s) from {CSV_FILE}.")
        except FileNotFoundError:
            print("Data file not found. Starting fresh.")
        except Exception as e:
            print(f"Load error: {e}")

    def _save(self):
        try:
            self._backup()
            with open(CSV_FILE, "w", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=CSV_FIELDS
                )
                writer.writeheader()
                writer.writerows(
                    [s.to_dict() for s in self.students]
                )
        except Exception as e:
            print(f"Save error: {e}")

    def _backup(self):
        if os.path.exists(CSV_FILE):
            try:
                shutil.copy(CSV_FILE, BACKUP_FILE)
            except Exception:
                pass    # backup failure is non-critical

    # ── CRUD OPERATIONS ───────────────────────────────

    def add(self, roll, name, age, email, phone,
            city, course, batch, marks_list,
            att_present, att_total):

        # Validate roll uniqueness
        if self.find_by_roll(roll):
            raise ValueError(
                f"Roll number {roll} already exists."
            )

        # Validate email format minimally
        if "@" not in email or "." not in email:
            raise ValueError(
                f"Invalid email format: {email}"
            )

        # Validate phone
        if not str(phone).isdigit() or len(str(phone)) != 10:
            raise ValueError(
                "Phone must be exactly 10 digits."
            )

        # Validate age
        if not 15 <= int(age) <= 60:
            raise ValueError(
                "Age must be between 15 and 60."
            )

        student = Student(
            roll, name, age, email, phone,
            city, course, batch,
            marks_list, att_present, att_total
        )
        self.students.append(student)
        self._save()
        return student

    def find_by_roll(self, roll):
        roll = int(roll)
        for s in self.students:
            if s.roll == roll:
                return s
        return None

    def search(self, keyword):
        keyword = str(keyword).lower().strip()
        results = []
        for s in self.students:
            if (keyword in s.name.lower()
                    or keyword == str(s.roll)
                    or keyword in s.email.lower()
                    or keyword in s.city.lower()
                    or keyword in s.batch.lower()):
                results.append(s)
        return results

    def update_marks(self, roll, subject_index, new_marks):
        student = self.find_by_roll(roll)
        if not student:
            raise LookupError(
                f"No student with roll {roll}."
            )
        old, new = student.update_marks(
            subject_index, new_marks
        )
        self._save()
        return student, old, new

    def update_attendance(self, roll, present, total):
        student = self.find_by_roll(roll)
        if not student:
            raise LookupError(
                f"No student with roll {roll}."
            )
        student.update_attendance(present, total)
        self._save()
        return student

    def delete(self, roll):
        student = self.find_by_roll(roll)
        if not student:
            raise LookupError(
                f"No student with roll {roll}."
            )
        self.students.remove(student)
        Student.total_enrolled -= 1
        self._save()
        return student

    # ── DISPLAY METHODS ───────────────────────────────

    def display_all(self):
        if not self.students:
            print("No student records found.")
            return

        print(f"\n{'=' * 70}")
        print(f"  {INSTITUTE_NAME} — Student Records".center(70))
        print(f"  {PROGRAM_NAME}".center(70))
        print(f"{'=' * 70}")
        print(
            f"{'Roll':<5} "
            f"{'Name':<22} "
            f"{'Course':<12} "
            f"{'Avg %':>6}  "
            f"{'Gr':<3} "
            f"{'Res':<5} "
            f"{'Att %':>6}"
        )
        print("-" * 70)
        for s in self.students:
            print(s)
        print("=" * 70)
        print(f"  Total Records : {len(self.students)}")
        print(f"  File          : {CSV_FILE}")
        print(f"  Last Updated  : "
              f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(f"{'=' * 70}\n")

    def display_student_profile(self, roll):
        student = self.find_by_roll(roll)
        if not student:
            print(f"No student found with roll {roll}.")
            return

        print(f"\n{'=' * 50}")
        print(f"  STUDENT PROFILE".center(50))
        print(f"{'=' * 50}")
        print(f"  Roll No      : {student.roll}")
        print(f"  Name         : {student.name}")
        print(f"  Age          : {student.age}")
        print(f"  Email        : {student.email}")
        print(f"  Phone        : {student.phone}")
        print(f"  City         : {student.city}")
        print(f"  Course       : {student.course}")
        print(f"  Batch        : {student.batch}")
        print(f"  Enrolled On  : {student.enrollment_date}")
        print(f"{'=' * 50}")
        print(f"  ACADEMIC PERFORMANCE")
        print(f"{'=' * 50}")
        print(
            f"  {'Subject':<22}"
            f"  {'Marks':>11}"
            f"  {'  %':>8}"
            f"  {'Gr':<3}"
            f"  Status"
        )
        print(f"  {'-' * 46}")
        for subj in student.subjects:
            print(f"  {subj}")
        print(f"  {'-' * 46}")
        print(f"  {'OVERALL AVERAGE':<22}"
              f"  {student.average_marks():>7.1f}/100  "
              f"  {student.overall_percentage():>5.2f}%"
              f"  {student.overall_grade():<3}"
              f"  {student.overall_status()}")
        print(f"{'=' * 50}")
        print(f"  ATTENDANCE")
        print(f"{'=' * 50}")
        print(f"  Classes Attended : {student.attendance_present}"
              f" / {student.attendance_total}")
        print(f"  Percentage       : "
              f"{student.attendance_percentage():.2f}%")
        print(f"  Status           : {student.attendance_status()}")
        print(f"{'=' * 50}")
        if student.is_scholarship_eligible():
            print(f"  ★  SCHOLARSHIP ELIGIBLE")
        print(f"{'=' * 50}\n")

    # ── STATISTICS ────────────────────────────────────

    def statistics(self):
        if not self.students:
            print("No data available.")
            return

        n          = len(self.students)
        all_pct    = [s.overall_percentage()
                      for s in self.students]
        passed     = [s for s in self.students
                      if s.overall_status() == "Pass"]
        failed     = [s for s in self.students
                      if s.overall_status() == "Fail"]
        scholars   = [s for s in self.students
                      if s.is_scholarship_eligible()]

        topper     = max(self.students,
                         key=lambda s: s.overall_percentage())
        weakest    = min(self.students,
                         key=lambda s: s.overall_percentage())

        low_att    = [s for s in self.students
                      if s.attendance_percentage() < 75]

        batches    = set(s.batch for s in self.students)
        cities     = set(s.city for s in self.students)

        grade_count = {}
        for s in self.students:
            g = s.overall_grade()
            grade_count[g] = grade_count.get(g, 0) + 1

        print(f"\n{'=' * 50}")
        print(f"  CLASS ANALYTICS REPORT".center(50))
        print(f"  {INSTITUTE_NAME}".center(50))
        print(f"{'=' * 50}")
        print(f"  Total Students     : {n}")
        print(f"  Passed             : {len(passed)} "
              f"({round(len(passed)/n*100, 1)}%)")
        print(f"  Failed             : {len(failed)} "
              f"({round(len(failed)/n*100, 1)}%)")
        print(f"  Class Average      : "
              f"{round(sum(all_pct)/n, 2):.2f}%")
        print(f"  Highest Marks      : "
              f"{max(all_pct):.2f}%")
        print(f"  Lowest Marks       : "
              f"{min(all_pct):.2f}%")
        print(f"  Class Topper       : "
              f"{topper.name} "
              f"({topper.overall_percentage():.2f}%)")
        print(f"  Needs Support      : "
              f"{weakest.name} "
              f"({weakest.overall_percentage():.2f}%)")
        print(f"  Scholarship Eligible: {len(scholars)}")
        print(f"  Low Attendance     : {len(low_att)}")
        print(f"  Batches            : "
              f"{', '.join(sorted(batches))}")
        print(f"  Cities             : "
              f"{', '.join(sorted(cities))}")
        print(f"{'=' * 50}")
        print(f"  GRADE DISTRIBUTION")
        print(f"{'=' * 50}")
        for grade in ["A+", "A", "B", "C", "F"]:
            count = grade_count.get(grade, 0)
            bar   = "█" * count
            print(f"  {grade:<3} : {bar:<20} {count}")
        print(f"{'=' * 50}\n")

    # ── REPORT EXPORT ─────────────────────────────────

    def export_report(self):
        if not self.students:
            print("No data to export.")
            return

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            with open(REPORT_FILE, "w") as f:

                f.write("=" * 60 + "\n")
                f.write(
                    f"  {INSTITUTE_NAME}\n"
                    f"  {PROGRAM_NAME}\n"
                    f"  CLASS REPORT CARD\n"
                    f"  Generated: {now}\n"
                )
                f.write("=" * 60 + "\n\n")

                for s in self.students:
                    f.write("=" * 60 + "\n")
                    f.write(
                        f"  STUDENT: {s.name}  "
                        f"(Roll: {s.roll})\n"
                    )
                    f.write("=" * 60 + "\n")
                    f.write(
                        f"  Course  : {s.course}\n"
                        f"  Batch   : {s.batch}\n"
                        f"  Email   : {s.email}\n"
                        f"  City    : {s.city}\n"
                    )
                    f.write("-" * 60 + "\n")
                    f.write("  SUBJECT PERFORMANCE:\n")

                    for subj in s.subjects:
                        f.write(f"    {subj}\n")

                    f.write("-" * 60 + "\n")
                    f.write(
                        f"  Overall %  : "
                        f"{s.overall_percentage():.2f}%\n"
                        f"  Grade      : {s.overall_grade()}\n"
                        f"  Result     : {s.overall_status()}\n"
                        f"  Attendance : "
                        f"{s.attendance_percentage():.1f}% "
                        f"({s.attendance_status()})\n"
                    )
                    if s.is_scholarship_eligible():
                        f.write(
                            "  ★ SCHOLARSHIP ELIGIBLE\n"
                        )
                    f.write("\n")

                # Summary at the end
                all_pct = [s.overall_percentage()
                           for s in self.students]
                passed  = sum(
                    1 for s in self.students
                    if s.overall_status() == "Pass"
                )
                f.write("=" * 60 + "\n")
                f.write("  CLASS SUMMARY\n")
                f.write("=" * 60 + "\n")
                f.write(
                    f"  Total Students : {len(self.students)}\n"
                    f"  Class Average  : "
                    f"{sum(all_pct)/len(all_pct):.2f}%\n"
                    f"  Passed         : {passed}\n"
                    f"  Failed         : "
                    f"{len(self.students) - passed}\n"
                )
                f.write("=" * 60 + "\n")

            print(f"Report exported to '{REPORT_FILE}'.")

        except Exception as e:
            print(f"Export error: {e}")

# ── INPUT HELPERS ─────────────────────────────────────────

def get_int(prompt, min_v=None, max_v=None):
    while True:
        try:
            val = int(input(prompt))
            if min_v is not None and val < min_v:
                print(f"  Minimum value: {min_v}")
                continue
            if max_v is not None and val > max_v:
                print(f"  Maximum value: {max_v}")
                continue
            return val
        except ValueError:
            print("  Please enter a whole number.")

def get_float(prompt, min_v=0.0, max_v=100.0):
    while True:
        try:
            val = float(input(prompt))
            if val < min_v or val > max_v:
                print(f"  Enter value between {min_v} and {max_v}.")
                continue
            return val
        except ValueError:
            print("  Please enter a number.")

def get_string(prompt, min_len=1, alpha_only=False):
    while True:
        val = input(prompt).strip()
        if len(val) < min_len:
            print(f"  Minimum {min_len} character(s) required.")
            continue
        if alpha_only and not val.replace(" ", "").isalpha():
            print("  Letters only — no numbers or symbols.")
            continue
        return val

def get_marks_for_all_subjects():
    print(f"\n  Enter marks for each subject (0 — 100):")
    marks = []
    for subject in SUBJECTS:
        m = get_float(f"  {subject:<25}: ", 0.0, 100.0)
        marks.append(m)
    return marks

def confirm(prompt="Confirm? (yes/no): "):
    return input(prompt).strip().lower() == "yes"

# ── MENU ACTION FUNCTIONS ──────────────────────────────────

def menu_add_student(db):
    print(f"\n{'=' * 44}")
    print("  ADD NEW STUDENT")
    print(f"{'=' * 44}")

    try:
        roll   = get_int("  Roll Number  : ", 1, 9999)
        name   = get_string("  Full Name    : ",
                             min_len=2, alpha_only=True)
        age    = get_int("  Age          : ", 15, 60)
        email  = get_string("  Email        : ", min_len=6)
        phone  = get_string("  Phone (10d)  : ", min_len=10)
        city   = get_string("  City         : ",
                             min_len=2, alpha_only=True)
        course = get_string("  Course       : ", min_len=2)
        batch  = get_string("  Batch        : ", min_len=2)

        marks  = get_marks_for_all_subjects()

        print("\n  Attendance:")
        att_total   = get_int(
            "  Total classes held : ", 0, 365
        )
        att_present = get_int(
            "  Classes attended   : ", 0, att_total
        )

        student = db.add(
            roll, name, age, email, phone,
            city, course, batch, marks,
            att_present, att_total
        )

        print(f"\n  ✓ Student added successfully!")
        print(f"  Name    : {student.name}")
        print(f"  Grade   : {student.overall_grade()}")
        print(f"  Status  : {student.overall_status()}")
        print(f"  Avg %   : {student.overall_percentage()}%")

    except ValueError as e:
        print(f"\n  Validation Error: {e}")
    except Exception as e:
        print(f"\n  Error: {e}")

def menu_search_student(db):
    print(f"\n{'=' * 44}")
    print("  SEARCH STUDENT")
    print(f"{'=' * 44}")
    keyword = input("  Enter name, roll, email, "
                    "city or batch: ").strip()

    if not keyword:
        print("  Search keyword cannot be empty.")
        return

    results = db.search(keyword)

    if not results:
        print(f"\n  No students found matching '{keyword}'.")
        return

    print(f"\n  Found {len(results)} result(s):")
    for s in results:
        print(f"  {s}")

    if len(results) == 1:
        if confirm("\n  View full profile? (yes/no): "):
            db.display_student_profile(results[0].roll)

def menu_view_profile(db):
    roll = get_int("\n  Enter Roll Number: ", 1, 9999)
    db.display_student_profile(roll)

def menu_update_marks(db):
    print(f"\n{'=' * 44}")
    print("  UPDATE SUBJECT MARKS")
    print(f"{'=' * 44}")

    try:
        roll    = get_int("  Roll Number: ", 1, 9999)
        student = db.find_by_roll(roll)

        if not student:
            print(f"  No student with roll {roll}.")
            return

        print(f"\n  Student: {student.name}")
        print(f"  Current marks:")
        for i, s in enumerate(student.subjects):
            print(f"    {i+1}. {s.subject_name:<22}: "
                  f"{s.marks_obtained:.1f}")

        sub_idx = get_int(
            "\n  Select subject (1-5): ", 1, 5
        ) - 1

        current = student.subjects[sub_idx].marks_obtained
        print(f"\n  Subject : "
              f"{student.subjects[sub_idx].subject_name}")
        print(f"  Current : {current:.1f}")

        new_marks = get_float(
            f"  New marks (0-100): ", 0.0, 100.0
        )

        if confirm(
            f"  Update {student.name}'s "
            f"{SUBJECTS[sub_idx]} from "
            f"{current} to {new_marks}? (yes/no): "
        ):
            s, old, new = db.update_marks(
                roll, sub_idx, new_marks
            )
            print(f"\n  ✓ Updated: {old:.1f} → {new:.1f}")
            print(f"  New grade: {s.overall_grade()}")
            print(f"  New avg  : {s.overall_percentage():.2f}%")

    except (ValueError, LookupError, IndexError) as e:
        print(f"\n  Error: {e}")

def menu_update_attendance(db):
    print(f"\n{'=' * 44}")
    print("  UPDATE ATTENDANCE")
    print(f"{'=' * 44}")

    try:
        roll    = get_int("  Roll Number: ", 1, 9999)
        student = db.find_by_roll(roll)

        if not student:
            print(f"  No student with roll {roll}.")
            return

        print(f"\n  Student      : {student.name}")
        print(f"  Current      : "
              f"{student.attendance_present} / "
              f"{student.attendance_total} classes")
        print(f"  Percentage   : "
              f"{student.attendance_percentage():.1f}%")

        total   = get_int(
            "\n  Total classes held   : ", 0, 365
        )
        present = get_int(
            "  Classes attended     : ", 0, total
        )

        s = db.update_attendance(roll, present, total)
        print(f"\n  ✓ Attendance updated.")
        print(f"  {s.attendance_present}/{s.attendance_total}"
              f" = {s.attendance_percentage():.1f}% "
              f"({s.attendance_status()})")

    except (ValueError, LookupError) as e:
        print(f"\n  Error: {e}")

def menu_delete_student(db):
    print(f"\n{'=' * 44}")
    print("  DELETE STUDENT")
    print(f"{'=' * 44}")

    try:
        roll    = get_int("  Roll Number: ", 1, 9999)
        student = db.find_by_roll(roll)

        if not student:
            print(f"  No student with roll {roll}.")
            return

        print(f"\n  Student: {student.name}")
        print(f"  Roll   : {student.roll}")
        print(f"  Course : {student.course}")

        if confirm(
            f"\n  Permanently delete {student.name}? "
            f"(yes/no): "
        ):
            deleted = db.delete(roll)
            print(f"\n  ✓ {deleted.name} deleted. "
                  f"Backup saved to {BACKUP_FILE}.")

    except LookupError as e:
        print(f"\n  Error: {e}")

# ── MAIN PROGRAM ──────────────────────────────────────────

def display_main_menu():
    print(f"\n{'=' * 44}")
    print(f"  {INSTITUTE_NAME}".center(44))
    print(f"  {PROGRAM_NAME}".center(44))
    print(f"  STUDENT MANAGEMENT SYSTEM".center(44))
    print(f"{'=' * 44}")
    print("  1.  Add New Student")
    print("  2.  View All Students")
    print("  3.  View Student Profile")
    print("  4.  Search Student")
    print("  5.  Update Subject Marks")
    print("  6.  Update Attendance")
    print("  7.  Delete Student")
    print("  8.  Class Analytics")
    print("  9.  Export Full Report")
    print("  10. Exit")
    print(f"{'=' * 44}")
    print(f"  Records : {Student.total_enrolled} "
          f"| File: {CSV_FILE}")
    print(f"{'=' * 44}")

def main():
    print(f"\n{'=' * 44}")
    print(f"  Welcome to {INSTITUTE_NAME}".center(44))
    print(f"  Student Management System".center(44))
    print(f"  Version 1.0".center(44))
    print(f"{'=' * 44}\n")

    db = StudentDatabase()

    while True:
        display_main_menu()

        try:
            choice = input("  Enter choice (1-10): ").strip()

            if choice == "1":
                menu_add_student(db)

            elif choice == "2":
                db.display_all()

            elif choice == "3":
                menu_view_profile(db)

            elif choice == "4":
                menu_search_student(db)

            elif choice == "5":
                menu_update_marks(db)

            elif choice == "6":
                menu_update_attendance(db)

            elif choice == "7":
                menu_delete_student(db)

            elif choice == "8":
                db.statistics()

            elif choice == "9":
                db.export_report()
                print(f"  Open '{REPORT_FILE}' "
                      f"to view the full report.")

            elif choice == "10":
                print(f"\n  Thank you for using "
                      f"{INSTITUTE_NAME} SMS.")
                print(f"  Data saved to {CSV_FILE}.")
                print(f"  Goodbye!\n")
                break

            else:
                print("  Invalid choice. Enter 1 to 10.")

        except KeyboardInterrupt:
            print("\n\n  Interrupted. Returning to menu.")
        except Exception as e:
            print(f"\n  Unexpected error: {e}")
            print("  Please try again.")


# Entry point
if __name__ == "__main__":
    main()
