# Expense, Attendance, Grading and Billing Management System

A menu-driven Python application that combines four management modules in one program: expense tracking, attendance recording, student grading, and customer billing.

The project is built with Python's standard library. No third-party packages are required.

## Features

### 1. Expense Management
- Add an expense with a description, category, amount, and date.
- View all recorded expenses.
- Calculate totals for each expense category.
- Display the grand total and the highest and lowest expenses.

Available categories:
- Food
- Travel
- Utilities
- Stationery
- Other

### 2. Attendance Management
- Record a person's name, ID, total working days, and days present.
- Calculate attendance percentage automatically.
- Assign an attendance status:
  - **Eligible:** 75% or above
  - **Warning:** 60% to below 75%
  - **Shortage:** below 60%
- View attendance records, average attendance, and highest and lowest attendance.

### 3. Grading System
- Enter marks for up to 20 subjects.
- Calculate total marks, average, percentage, grade, and final result.
- Generate individual report cards and a class summary.
- A student passes only if every subject mark is at least 35.

| Percentage | Grade | Remark |
|---|---|---|
| 90% and above | A+ | Outstanding |
| 80% to below 90% | A | Excellent |
| 70% to below 80% | B | Very Good |
| 60% to below 70% | C | Good |
| 50% to below 60% | D | Satisfactory |
| 35% to below 50% | E | Pass |
| Below 35% | F | Fail |

### 4. Billing System
- Create customer invoices containing multiple items.
- Enter each item's unit price and quantity.
- Apply a discount according to the invoice subtotal:
  - **5%** for a subtotal of ₹1,000 or more
  - **10%** for a subtotal of ₹5,000 or more
  - **15%** for a subtotal of ₹10,000 or more
- Calculate **18% tax** on the amount after discount.
- View generated invoices.

## Technologies and Concepts

- Python 3
- Functions and modular programming
- Lists and dictionaries
- Loops and conditional statements
- Input validation
- Date handling with `datetime`
- Accurate monetary calculations with `decimal`

## Requirements

- Python 3.8 or newer
- No external Python libraries

## Project Structure

```text
Expense-Attendance-Grading-Billing-System/
│
├── management_system.py
└── README.md
```

## How to Use

1. Run `management_system.py`.
2. Select a module from the main menu:
   - Expense Management
   - Attendance Management
   - Grading System
   - Billing System
   - View All Reports
3. Follow the on-screen instructions to enter information.
4. Open the relevant report option to view the recorded information.
5. Select **Exit** to close the program.

## Data Storage

This version stores information in Python lists while the program is running. Records are temporary and are cleared when the program closes. Permanent database or file storage is not included in this version.

## Future Improvements

- Store records permanently using SQLite or MongoDB.
- Add options to edit and delete records.
- Add user login and role-based access.
- Export invoices and reports to PDF or Excel.
- Develop a graphical user interface.

## Author

Created as a Python programming project.

