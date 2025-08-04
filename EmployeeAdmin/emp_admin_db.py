import mysql.connector
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',       # Palitan kung ibang server ang gamit
    'user': 'root',            # Username ng MySQL mo
    'password': 'ceecaresopc', # Password ng MySQL mo
    'database': 'emp_admin_db' # Pangalan ng database na ginawa mo
}

def connect():
    return mysql.connector.connect(**DB_CONFIG)


def insert_employee(data):
    conn = connect()
    cursor = conn.cursor()
    
    print(f"[DEBUG] Received data: {data}")
    print(f"[DEBUG] Length of data: {len(data)}")


    if len(data) != 19:
        raise ValueError(f"Expected 19 fields, got {len(data)}")

    complete_data = data + ('Active', '1234', 0)
    print(f"[DEBUG] Complete data to insert: {complete_data}")
    print(f"[DEBUG] Length of complete data: {len(complete_data)}")


    sql = """
        INSERT INTO employees (
            employee_id, last_name, first_name, middle_name, marital_status, gender, dob,
            place_of_birth, address, contact_no, email, position, hire_date, salary, sss_no, tin_no, pagibig_no, philhealth_no,
            profile_image, status, password, has_changed_password
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, complete_data)
    conn.commit()
    conn.close()


def generate_employee_id():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id FROM employees ORDER BY id DESC LIMIT 1")
    last = cursor.fetchone()
    conn.close()

    if not last or not last[0] or not last[0].startswith("EMP"):
        return "EMP0001"
    else:
        try:
            num = int(last[0][3:]) + 1
            return f"EMP{num:04d}"
        except ValueError:
            return "EMP0001"


def fetch_all_employees():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_employee(employee_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET status = 'Inactive' WHERE employee_id = %s", (employee_id,))
    conn.commit()
    conn.close()


def update_employee(data):
    conn = connect()
    cursor = conn.cursor()
    sql = """
        UPDATE employees SET
            first_name = %s,
            middle_name = %s,
            last_name = %s,
            marital_status = %s,
            gender = %s,
            dob = %s,
            place_of_birth = %s,
            address = %s,
            contact_no = %s,
            email = %s,
            sss_no = %s,
            tin_no = %s,
            pagibig_no = %s,
            philhealth_no = %s,
            position = %s,
            hire_date = %s,
            salary = %s,
            profile_image = %s
        WHERE employee_id = %s
    """
    cursor.execute(sql, (
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['marital_status'],
        data['gender'],
        data['dob'],
        data['place_of_birth'],
        data['address'],
        data['contact_no'],
        data['email'],
        data['sss_no'],
        data['tin_no'],
        data['pagibig_no'],
        data['philhealth_no'],
        data['position'],
        data['hire_date'],
        data['salary'],
        data['profile_image'],
        data['employee_id']
    
    ))
    conn.commit()
    conn.close()


def get_employee_by_id(employee_id):
    conn = connect()
    cursor = conn.cursor()
    sql = """
        SELECT id, employee_id, last_name, first_name, middle_name, marital_status,
                gender, dob, place_of_birth, address, contact_no, email,
                position, hire_date, salary, sss_no, tin_no, pagibig_no, philhealth_no, profile_image, status, password, has_changed_password
        FROM employees
        WHERE employee_id = %s
    """
    cursor.execute(sql, (employee_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "employee_id": row[1],
            "last_name": row[2],
            "first_name": row[3],
            "middle_name": row[4],
            "marital_status": row[5],
            "gender": row[6],
            "dob": str(row[7]),
            "place_of_birth": row[8],
            "address": row[9],
            "contact_no": row[10],
            "email": row[11],
            "position": row[12],
            "hire_date": str(row[13]),
            "salary": float(row[14]),
            "profile_image": row[19],
            "status": row[20],
            "password": row[21],
            "has_changed_password": row[22],
            "sss_no": row[15],
            "tin_no": row[16],
            "pagibig_no": row[17],
            "philhealth_no": row[18]
        }
    return None


def fetch_employees_by_status(status='Active'):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE status = %s", (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_total_employees():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_active_employees_count():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Active'")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def count_inactive_employees():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees WHERE status != 'Active'")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def update_employee_password(employee_id, new_password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees 
        SET password = %s, has_changed_password = 1 
        WHERE employee_id = %s
    """, (new_password, employee_id))
    conn.commit()
    conn.close()


def check_employee_credentials(employee_id, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM employees WHERE employee_id = %s AND status = 'Active'", (employee_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0] == password
    return False

def time_in(employee_id, date_str, time_str):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM attendance WHERE employee_id = %s AND date = %s", (employee_id, date_str))
        row = cursor.fetchone()

        if row:
            cursor.execute("UPDATE attendance SET time_in = %s WHERE employee_id = %s AND date = %s",
                            (time_str, employee_id, date_str))
        else:
            cursor.execute("INSERT INTO attendance (employee_id, date, time_in) VALUES (%s, %s, %s)",
                            (employee_id, date_str, time_str))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("[DB ERROR - time_in]:", e)
        return False


def time_out(employee_id, date_str, time_str):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Check kung may existing record na for that date
        cursor.execute("SELECT id FROM attendance WHERE employee_id = %s AND date = %s", (employee_id, date_str))
        row = cursor.fetchone()

        if row:
            # Update kung may existing record
            cursor.execute("UPDATE attendance SET time_out = %s WHERE employee_id = %s AND date = %s", (time_str, employee_id, date_str))
        else:
            # Insert kung wala pa
            cursor.execute("INSERT INTO attendance (employee_id, date, time_out) VALUES (%s, %s, %s)", (employee_id, date_str, time_str))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("[DB ERROR - time_out]:", e)
        return False
    
def get_my_attendance_records(employee_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, time_in, time_out
        FROM attendance
        WHERE employee_id = %s
        ORDER BY date DESC
    """, (employee_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_attendance_by_date(employee_id, date):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, time_in, time_out
        FROM attendance
        WHERE employee_id = %s AND date = %s
    """, (employee_id, date))
    record = cursor.fetchone()
    conn.close()
    return record

def get_attendance_range(employee_id, start_date, end_date):
    """
    Fetch attendance records for a specific employee between two dates (inclusive).
    """
    conn = connect()
    cursor = conn.cursor()

    query = """
        SELECT date, time_in, time_out
        FROM attendance
        WHERE employee_id = %s
        AND date BETWEEN %s AND %s
        ORDER BY date ASC
    """
    cursor.execute(query, (employee_id, start_date, end_date))
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    return records

def add_manual_attendance(employee_id, date_str, time_in_str, time_out_str):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Check if entry already exists
        cursor.execute("SELECT id FROM attendance WHERE employee_id = %s AND date = %s", (employee_id, date_str))
        row = cursor.fetchone()

        if row:
            # Update both time_in and time_out
            cursor.execute("""
                UPDATE attendance 
                SET time_in = %s, time_out = %s 
                WHERE employee_id = %s AND date = %s
            """, (time_in_str, time_out_str, employee_id, date_str))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO attendance (employee_id, date, time_in, time_out) 
                VALUES (%s, %s, %s, %s)
            """, (employee_id, date_str, time_in_str, time_out_str))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("[DB ERROR - add_manual_attendance]:", e)
        return False

def get_all_attendance_records():
    conn = connect()
    cursor = conn.cursor()
    query = """
    SELECT 
        a.employee_id, 
        a.date, 
        e.first_name, 
        e.last_name, 
        e.profile_image, 
        a.time_in, 
        a.time_out
    FROM attendance a
    JOIN employees e ON a.employee_id = e.employee_id
    ORDER BY a.date DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def get_attendance_history(employee_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.date, a.time_in, a.time_out, ar.status
        FROM attendance a
        LEFT JOIN attendance_requests ar
            ON a.employee_id = ar.employee_id AND a.date = ar.date
        WHERE a.employee_id = %s
        ORDER BY a.date DESC
    """, (employee_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_approved_time_entries(employee_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, time_in, time_out, status
        FROM attendance_requests
        WHERE employee_id = %s AND status IN ('Approved', 'Rejected')
        ORDER BY date DESC
    """, (employee_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def submit_attendance_request(employee_id, date_str, time_in_str, time_out_str, reason='', request_type='manual'):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance_requests (
                employee_id, date, time_in, time_out, reason, request_type, status
            ) VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        """, (employee_id, date_str, time_in_str, time_out_str, reason, request_type))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("[DB ERROR - submit_attendance_request]:", e)
        return False

def get_pending_attendance_requests():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ar.id, ar.employee_id, e.first_name, e.last_name,
                ar.date, ar.time_in, ar.time_out, ar.reason, ar.submitted_at
        FROM attendance_requests ar
        JOIN employees e ON ar.employee_id = e.employee_id
        WHERE ar.status = 'pending'
        ORDER BY ar.submitted_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def process_attendance_request(request_id, approve: bool, admin_id='admin123'):
    conn = connect()
    cursor = conn.cursor()

    # Get request details
    cursor.execute("SELECT employee_id, date, time_in, time_out FROM attendance_requests WHERE id = %s", (request_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    employee_id, date_str, time_in_str, time_out_str = row

    if approve:
        # Upsert to attendance table
        cursor.execute("SELECT id FROM attendance WHERE employee_id = %s AND date = %s", (employee_id, date_str))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE attendance SET time_in = %s, time_out = %s
                WHERE employee_id = %s AND date = %s
            """, (time_in_str, time_out_str, employee_id, date_str))
        else:
            cursor.execute("""
                INSERT INTO attendance (employee_id, date, time_in, time_out)
                VALUES (%s, %s, %s, %s)
            """, (employee_id, date_str, time_in_str, time_out_str))

        cursor.execute("""
            UPDATE attendance_requests
            SET status = 'approved', reviewed_at = NOW(), reviewed_by = %s
            WHERE id = %s
        """, (admin_id, request_id))

    else:
        # Just reject it
        cursor.execute("""
            UPDATE attendance_requests
            SET status = 'rejected', reviewed_at = NOW(), reviewed_by = %s
            WHERE id = %s
        """, (admin_id, request_id))

    conn.commit()
    conn.close()
    return True

def get_pending_requests_with_name():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ar.employee_id,
            e.first_name,
            e.last_name,
            ar.date,
            ar.time_in,
            ar.time_out,
            ar.reason,
            ar.status,
            ar.id AS request_id
        FROM attendance_requests ar
        JOIN employees e ON ar.employee_id = e.employee_id
        WHERE ar.status = 'pending'
        ORDER BY ar.submitted_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def submit_time_entry_request(employee_id, date, time_type, time_value):
    conn = connect()
    cursor = conn.cursor()

    if time_type == "IN":
        cursor.execute("""
            INSERT INTO attendance_requests (employee_id, date, time_in, reason, status, submitted_at)
            VALUES (%s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP)
        """, (employee_id, date, time_value, 'Manual time in request'))
    elif time_type == "OUT":
        cursor.execute("""
            INSERT INTO attendance_requests (employee_id, date, time_out, reason, status, submitted_at)
            VALUES (%s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP)
        """, (employee_id, date, time_value, 'Manual time out request'))

    conn.commit()
    conn.close()
    
def get_history_requests_with_name():
    conn = connect()
    cursor = conn.cursor()

    query = """
        SELECT 
            ar.employee_id,
            e.first_name,
            e.last_name,
            ar.date,
            ar.time_in,
            ar.time_out,
            ar.reason,
            ar.status,
            ar.submitted_at
        FROM attendance_requests ar
        JOIN employees e ON ar.employee_id = e.employee_id
        ORDER BY ar.submitted_at DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def approve_request(request_id):
    if not isinstance(request_id, (str, int)):
        raise ValueError("request_id must be a string or integer")

    conn = connect()
    cursor = conn.cursor()

    try:
        print(f"[DB] Approving request ID: {request_id}")

        # 1. Fetch the request details
        cursor.execute(
            "SELECT employee_id, date, time_in, time_out FROM attendance_requests WHERE id = %s",
            (request_id,)
        )
        request = cursor.fetchone()

        if not request:
            print(f"[DB ERROR] No request found with ID: {request_id}")
            return

        employee_id, date, time_in, time_out = request

        # 2. Update the request's status to 'approved'
        cursor.execute(
            "UPDATE attendance_requests SET status = %s WHERE id = %s",
            ('approved', request_id)
        )

        if cursor.rowcount == 0:
            print(f"[DB WARNING] Request status not updated for ID: {request_id}")
        else:
            print(f"[DB] Request status updated for ID: {request_id}")

        # 3. Check if an attendance record already exists
        cursor.execute(
            "SELECT id FROM attendance WHERE employee_id = %s AND date = %s",
            (employee_id, date)
        )
        attendance = cursor.fetchone()

        if attendance:
            # If record exists, update both time_in and time_out if NULL
            cursor.execute(
                """
                UPDATE attendance
                SET time_in = COALESCE(time_in, %s),
                    time_out = COALESCE(time_out, %s)
                WHERE employee_id = %s AND date = %s
                """,
                (time_in, time_out, employee_id, date)
            )
            print(f"[DB] Attendance updated for {employee_id} on {date}")
        else:
            # Insert new record with both time_in and time_out
            cursor.execute(
                "INSERT INTO attendance (employee_id, date, time_in, time_out) VALUES (%s, %s, %s, %s)",
                (employee_id, date, time_in, time_out)
            )
            print(f"[DB] Attendance inserted for {employee_id} on {date}")

        conn.commit()

    except Exception as e:
        print("[DB ERROR - approve_request]:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def reject_request(request_id):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE attendance_requests
            SET status = 'rejected'
            WHERE id = %s
        """, (request_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"[DB ERROR] Failed to reject request: {e}")
        return False
    finally:
        conn.close()
        
def submit_leave_request(employee_id, leave_type, paid_status, start_date, end_date, reason):
    conn = connect()
    cursor = conn.cursor()
    sql = """
        INSERT INTO leave_requests 
        (employee_id, leave_type, paid_status, start_date, end_date, reason, status, applied_at)
        VALUES (%s, %s, %s, %s, %s, %s, 'Pending', NOW())
    """
    cursor.execute(sql, (employee_id, leave_type, paid_status, start_date, end_date, reason))
    conn.commit()
    conn.close()


def get_employee_leaves(employee_id):
    conn = connect()
    cursor = conn.cursor()
    sql = """
        SELECT leave_type, paid_status, start_date, end_date, reason, status, reviewed_by
        FROM leave_requests
        WHERE employee_id = %s
        ORDER BY start_date DESC
    """
    cursor.execute(sql, (employee_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_leave_requests():
    conn = connect()
    cursor = conn.cursor()
    sql = """
        SELECT 
            lr.id,
            lr.employee_id,
            e.first_name,
            e.last_name,
            lr.leave_type,
            lr.paid_status,
            lr.start_date,
            lr.end_date,
            lr.reason,
            lr.status,
            lr.reviewed_by,
            lr.reviewed_at
        FROM leave_requests lr
        JOIN employees e ON lr.employee_id = e.employee_id
        ORDER BY lr.start_date DESC
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def get_pending_leave_requests():
    conn = connect()
    cursor = conn.cursor()
    sql = """
        SELECT 
            lr.id,
            lr.employee_id,
            e.first_name,
            e.last_name,
            lr.leave_type,
            lr.paid_status,
            lr.start_date,
            lr.end_date,
            lr.reason,
            lr.status
        FROM leave_requests lr
        JOIN employees e ON lr.employee_id = e.employee_id
        WHERE lr.status = 'Pending'
        ORDER BY lr.start_date DESC
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


def update_leave_status(request_id, status, reviewed_by):
    conn = connect()
    cursor = conn.cursor()
    sql = """
        UPDATE leave_requests
        SET status = %s, reviewed_by = %s
        WHERE id = %s
    """
    cursor.execute(sql, (status, reviewed_by, request_id))
    conn.commit()
    conn.close()

def save_payroll_record(data):
    conn = connect()
    cursor = conn.cursor()

    query = """
        INSERT INTO payroll_records (
            employee_id, period_start, period_end, basic_salary, allowance, overtime_pay,
            gross_salary, late_deduction, sss, philhealth, pagibig, loan, other_deductions,
            total_deductions, net_salary, processed_by
        ) VALUES (
            %(employee_id)s, %(period_start)s, %(period_end)s, %(basic_salary)s, %(allowance)s,
            %(overtime_pay)s, %(gross_salary)s, %(late_deduction)s, %(sss)s, %(philhealth)s,
            %(pagibig)s, %(loan)s, %(other_deductions)s, %(total_deductions)s, %(net_salary)s,
            %(processed_by)s
        )
    """

    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()
    
def get_payroll_profile(employee_id):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM payroll_profiles WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    result = cursor.fetchone()
    conn.close()
    return result



def save_or_update_payroll_profile(data):
    conn = connect()
    cursor = conn.cursor()
    existing = get_payroll_profile(data['employee_id'])
    if existing:
        query = """
            UPDATE payroll_profiles
            SET allowance = %s, sss = %s, philhealth = %s,
                pagibig = %s, loan = %s, other_deductions = %s,
                updated_at = NOW()
            WHERE employee_id = %s
        """
        values = (
            data['allowance'], data['sss'], data['philhealth'],
            data['pagibig'], data['loan'], data['other_deductions'],
            data['employee_id']
        )
    else:
        query = """
            INSERT INTO payroll_profiles (
                employee_id, allowance, sss, philhealth,
                pagibig, loan, other_deductions, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        values = (
            data['employee_id'], data['allowance'], data['sss'], data['philhealth'],
            data['pagibig'], data['loan'], data['other_deductions']
        )

    cursor.execute(query, values)
    conn.commit()
    
def get_regular_holidays(start_date, end_date):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT holiday_date
        FROM holidays
        WHERE holiday_type = 'Regular' AND holiday_date BETWEEN %s AND %s
    """, (start_date, end_date))
    holidays = [row['holiday_date'] for row in cursor.fetchall()]
    conn.close()
    return holidays

def get_all_registered_profiles():
    conn = connect()
    cursor = conn.cursor()
    query = """
        SELECT e.employee_id, e.first_name, e.last_name, e.position, e.hire_date, e.salary
        FROM employees e
        JOIN registered_payroll_profiles r ON e.employee_id = r.employee_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return [
        {
            'employee_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'position': row[3],
            'hire_date': row[4],
            'salary': row[5]
        } for row in results
    ]
    
def register_payroll_profile(employee_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO registered_payroll_profiles (employee_id) VALUES (%s)
    """, (employee_id,))
    conn.commit()
    conn.close()
    
def delete_payroll_profile(employee_id):
    conn = connect()
    cursor = conn.cursor()

    # Delete from payroll_profiles
    cursor.execute("DELETE FROM payroll_profiles WHERE employee_id = %s", (employee_id,))
    deleted_rows_pp = cursor.rowcount

    # Delete from registered_payroll_profiles
    cursor.execute("DELETE FROM registered_payroll_profiles WHERE employee_id = %s", (employee_id,))
    deleted_rows_rpp = cursor.rowcount

    conn.commit()
    conn.close()

    # You can return the total or separate counts
    return deleted_rows_pp + deleted_rows_rpp

from datetime import datetime

def get_enrolled_payroll_profiles(force_show_all=False):
    """
    Return registered profiles scheduled for payroll today,
    or all if force_show_all is True (for testing).
    """
    profiles = get_all_registered_profiles()

    today = datetime.today().day
    eligible_days = [14, 29, 30]  # 30 kapag walang 31

    if force_show_all or today in eligible_days:
        return profiles
    else:
        return []  # Walang payroll ngayon
    
def get_login_logs(limit=50):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM login_logs ORDER BY login_time DESC LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows





if __name__ == "__main__":
    print("Database connection successful. Ready to use.")