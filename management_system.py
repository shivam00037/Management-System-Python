"""Expense, Attendance, Grading and Billing Management System."""
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# ----------------------------- DATA ---------------------------------
CATEGORIES = ["Food", "Travel", "Utilities", "Stationery", "Other"]
SUBJECTS = ["Maths", "Science", "English", "History", "Computer"]
expenses, attendance, students, invoices = [], [], [], []
PASS_MARK, TAX_RATE = 35, Decimal("0.18")


# ----------------------------- INPUTS -------------------------------
def integer(prompt, low=None, high=None):
    while True:
        try:
            n = int(input(prompt))
            if (low is not None and n < low) or (high is not None and n > high):
                print("Value outside the allowed range.")
            else:
                return n
        except ValueError:
            print("Enter a valid whole number.")


def number(prompt, low=0, high=100):
    while True:
        try:
            n = float(input(prompt))
            if low <= n <= high:
                return n
            print(f"Enter a value from {low} to {high}.")
        except ValueError:
            print("Enter a valid number.")


def money_input(prompt):
    while True:
        try:
            raw = input(prompt).strip()
            value = Decimal(raw)
            if value.is_finite() and value > 0 and value.as_tuple().exponent >= -2:
                return value.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
            print("Enter a positive amount with at most 2 decimal places.")
        except InvalidOperation:
            print("Enter a valid amount.")


def text_input(prompt, minimum=1, maximum=60, letters=False):
    while True:
        value = " ".join(input(prompt).strip().split())
        valid = minimum <= len(value) <= maximum
        if letters:
            valid = valid and all(c.isalpha() or c.isspace() for c in value)
        if valid:
            return value
        print(f"Enter {minimum}-{maximum} " + ("letters/spaces." if letters else "characters."))


def choose(prompt, options):
    while True:
        value = input(prompt).strip().casefold()
        for option in options:
            if value == option.casefold():
                return option
        print("Choose: " + ", ".join(options))


def pause():
    input("\nPress Enter to continue...")


def heading(title):
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def empty(message):
    print(message)


# ----------------------------- EXPENSES ------------------------------
def add_expense():
    heading("ADD EXPENSE")
    expenses.append({
        "description": text_input("Description: ", 2, 60),
        "category": choose("Category: ", CATEGORIES),
        "amount": money_input("Amount: "),
        "date": date.today().isoformat()
    })
    print("Expense saved.")


def expense_report():
    heading("EXPENSE REPORT")
    if not expenses:
        return empty("No expense records.")
    totals = {c: sum((e["amount"] for e in expenses if e["category"] == c), Decimal("0")) for c in CATEGORIES}
    for category, total in totals.items():
        print(f"{category:<16} ₹{total:>10.2f}")
    total = sum(totals.values(), Decimal("0"))
    print("-" * 30, f"\nGrand total: ₹{total:.2f}")
    print("Highest:", max(expenses, key=lambda e: e["amount"]))
    print("Lowest :", min(expenses, key=lambda e: e["amount"]))
    print("\nNo.  Description                 Category        Amount       Date")
    for i, e in enumerate(expenses, 1):
        print(f"{i:<5}{e['description']:<28}{e['category']:<16}{e['amount']:>8.2f}   {e['date']}")


# ----------------------------- ATTENDANCE -----------------------------
def add_attendance():
    heading("MARK ATTENDANCE")
    days = integer("Total working days: ", 1)
    print("Enter 'done' as the name to finish.")
    while True:
        name = input("Name: ").strip()
        if name.casefold() == "done":
            break
        if not (2 <= len(name) <= 40 and all(c.isalpha() or c.isspace() for c in name)):
            print("Use a name containing 2-40 letters.")
            continue
        person_id = text_input("Person ID: ", 1, 20)
        present = integer(f"Days present (0-{days}): ", 0, days)
        percent = present / days * 100
        status = "Eligible" if percent >= 75 else "Warning" if percent >= 60 else "Shortage"
        attendance.append({"name": name, "id": person_id, "present": present,
                           "days": days, "percent": percent, "status": status})
        print("Attendance saved.")


def attendance_report():
    heading("ATTENDANCE REPORT")
    if not attendance:
        return empty("No attendance records.")
    for a in attendance:
        print(f"{a['name']:<20} {a['id']:<12} {a['present']:>3}/{a['days']:<3} "
              f"{a['percent']:>6.2f}%  {a['status']}")
    avg = sum(a["percent"] for a in attendance) / len(attendance)
    print(f"\nPeople: {len(attendance)} | Average: {avg:.2f}%")
    print("Highest:", max(attendance, key=lambda a: a["percent"])["name"])
    print("Lowest :", min(attendance, key=lambda a: a["percent"])["name"])


# ----------------------------- GRADING --------------------------------
def grade(percent):
    for limit, letter, remark in [
        (90, "A+", "Outstanding"), (80, "A", "Excellent"),
        (70, "B", "Very Good"), (60, "C", "Good"),
        (50, "D", "Satisfactory"), (35, "E", "Pass")
    ]:
        if percent >= limit:
            return letter, remark
    return "F", "Fail"


def show_student(s):
    heading("STUDENT REPORT CARD")
    print("Student:", s["name"])
    for subject, mark in zip(s["subjects"], s["marks"]):
        print(f"{subject:<20} {mark:>6.2f}")
    print(f"Total: {s['total']:.2f} | Average: {s['average']:.2f}")
    print(f"Percentage: {s['percent']:.2f}% | Grade: {s['grade']} ({s['remark']})")
    print("Result:", s["result"])


def add_student():
    heading("ENTER STUDENT MARKS")
    name = text_input("Student name: ", 2, 40, True)
    count = integer("Number of subjects (1-20, enter 5 for default): ", 1, 20)
    subjects, marks = [], []
    for i in range(count):
        subject = SUBJECTS[i] if i < len(SUBJECTS) else f"Subject {i + 1}"
        subjects.append(subject)
        marks.append(number(f"{subject} marks (0-100): "))
    total = sum(marks)
    average = total / count
    percent = total / (count * 100) * 100
    letter, remark = grade(percent)
    result = "PASS" if all(m >= PASS_MARK for m in marks) else "FAIL"
    student = {"name": name, "subjects": subjects, "marks": marks, "total": total,
               "average": average, "percent": percent, "grade": letter,
               "remark": remark, "result": result}
    students.append(student)
    show_student(student)


def grading_report():
    heading("CLASS REPORT")
    if not students:
        return empty("No student records.")
    for s in students:
        show_student(s)
    average = sum(s["percent"] for s in students) / len(students)
    topper = max(students, key=lambda s: s["percent"])
    passed = sum(s["result"] == "PASS" for s in students)
    print(f"\nStudents: {len(students)} | Class average: {average:.2f}%")
    print(f"Topper: {topper['name']} ({topper['percent']:.2f}%)")
    print(f"Passed: {passed} | Failed: {len(students) - passed}")


# ----------------------------- BILLING --------------------------------
def add_invoice():
    heading("CREATE CUSTOMER BILL")
    customer = text_input("Customer name: ", 2, 40, True)
    items = []
    print("Enter 'done' as item name to finish.")
    while True:
        name = input("Item name: ").strip()
        if name.casefold() == "done":
            break
        if not 1 <= len(name) <= 40:
            print("Item name must contain 1-40 characters.")
            continue
        price, quantity = money_input("Unit price: "), integer("Quantity: ", 1)
        items.append({"name": name, "price": price, "quantity": quantity,
                      "total": price * quantity})
    if not items:
        return empty("No items entered. Invoice not created.")
    subtotal = sum((i["total"] for i in items), Decimal("0"))
    rate = Decimal(".15") if subtotal >= 10000 else Decimal(".10") if subtotal >= 5000 else Decimal(".05") if subtotal >= 1000 else Decimal("0")
    discount = (subtotal * rate).quantize(Decimal(".01"))
    taxable = subtotal - discount
    tax = (taxable * TAX_RATE).quantize(Decimal(".01"))
    invoice = {"number": f"INV-{len(invoices)+1:04d}", "date": date.today().isoformat(),
               "customer": customer, "items": items, "subtotal": subtotal,
               "discount": discount, "rate": rate, "tax": tax, "total": taxable + tax}
    invoices.append(invoice)
    show_invoice(invoice)


def show_invoice(inv):
    heading("INVOICE")
    print(f"Bill: {inv['number']} | Date: {inv['date']} | Customer: {inv['customer']}")
    print(f"{'Item':<24}{'Price':>10}{'Qty':>6}{'Total':>12}")
    for item in inv["items"]:
        print(f"{item['name']:<24}{item['price']:>10.2f}{item['quantity']:>6}{item['total']:>12.2f}")
    print("-" * 52)
    print(f"Subtotal:       ₹{inv['subtotal']:.2f}")
    print(f"Discount ({inv['rate']*100:.0f}%): ₹{inv['discount']:.2f}")
    print(f"Tax (18%):      ₹{inv['tax']:.2f}")
    print(f"GRAND TOTAL:    ₹{inv['total']:.2f}")
    print("Thank you for your purchase!")


def billing_report():
    heading("BILLING REPORT")
    if not invoices:
        return empty("No invoices available.")
    for invoice in invoices:
        show_invoice(invoice)


# ----------------------------- MENUS ----------------------------------
def menu(title, actions):
    while True:
        heading(title)
        for key, (label, _) in enumerate(actions, 1):
            print(f"{key}. {label}")
        choice = integer("Choice: ", 1, len(actions))
        if actions[choice - 1][1] is None:
            break
        actions[choice - 1][1]()
        pause()


def main():
    actions = [
        ("Expense Management", lambda: menu("EXPENSE MANAGEMENT", [
            ("Add Expense", add_expense), ("View Expenses and Summary", expense_report),
            ("Back", None)])),
        ("Attendance Management", lambda: menu("ATTENDANCE MANAGEMENT", [
            ("Add Attendance", add_attendance), ("Attendance Report", attendance_report),
            ("Back", None)])),
        ("Grading System", lambda: menu("GRADING SYSTEM", [
            ("Enter Student Marks", add_student), ("Class Report", grading_report),
            ("Back", None)])),
        ("Billing System", lambda: menu("BILLING SYSTEM", [
            ("Create Invoice", add_invoice), ("View Invoices", billing_report),
            ("Back", None)])),
        ("View All Reports", lambda: (expense_report(), attendance_report(),
                                      grading_report(), billing_report())),
        ("Exit", None)
    ]
    try:
        menu("MANAGEMENT SYSTEM", actions)
    except (EOFError, KeyboardInterrupt):
        print("\nProgram stopped safely.")
    print("Thank you. Session ended.")


if __name__ == "__main__":
    main()
