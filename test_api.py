import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def make_request(url, method='GET', data=None):
    """Utility function to make HTTP requests using urllib.request."""
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data is not None else None
    
    try:
        with urllib.request.urlopen(req, data=body) as response:
            res_body = response.read().decode('utf-8')
            return response.status, json.loads(res_body) if res_body else None
    except urllib.error.HTTPError as e:
        res_body = e.read().decode('utf-8')
        return e.code, json.loads(res_body) if res_body else None
    except urllib.error.URLError as e:
        print(f"❌ Connection Error: Could not connect to {BASE_URL}. Ensure Flask app is running.")
        print(f"   Details: {e.reason}")
        sys.exit(1)

def run_tests():
    print("=" * 60)
    print(" 🚀 SMARTSPEND EXPENSE TRACKER - API TEST SUITE")
    print("=" * 60)

    # 1. GET ALL EXPENSES
    print("\n[Test 1] GET /api/expenses - Fetch All Expenses")
    status, res = make_request(f"{BASE_URL}/api/expenses")
    print(f"   Status Code : {status}")
    print(f"   Total Items : {len(res) if isinstance(res, list) else 0}")
    assert status == 200, f"Expected 200, got {status}"
    print("   Result      : PASS ✅")

    # 2. POST CREATE EXPENSE
    print("\n[Test 2] POST /api/expenses - Create New Expense")
    new_expense_payload = {
        "title": "College Textbooks",
        "amount": 750.50,
        "category": "Education",
        "date": "2026-09-17",
        "payment_method": "UPI",
        "notes": "Computer Science Core Books"
    }
    status, res = make_request(f"{BASE_URL}/api/expenses", method='POST', data=new_expense_payload)
    print(f"   Status Code : {status}")
    print(f"   Created ID  : {res.get('id') if isinstance(res, dict) else None}")
    assert status == 201, f"Expected 201 Created, got {status}"
    assert isinstance(res, dict) and 'id' in res, "Response missing expense ID"
    expense_id = res['id']
    print("   Result      : PASS ✅")

    # 3. GET SINGLE EXPENSE
    print(f"\n[Test 3] GET /api/expenses/{expense_id} - Fetch Expense by ID")
    status, res = make_request(f"{BASE_URL}/api/expenses/{expense_id}")
    print(f"   Status Code : {status}")
    print(f"   Title       : {res.get('title') if isinstance(res, dict) else None}")
    assert status == 200, f"Expected 200, got {status}"
    assert res['title'] == "College Textbooks", f"Title mismatch: {res.get('title')}"
    print("   Result      : PASS ✅")

    # 4. PUT UPDATE EXPENSE
    print(f"\n[Test 4] PUT /api/expenses/{expense_id} - Update Expense")
    update_payload = {
        "title": "College Textbooks & Reference Guides",
        "amount": 890.00,
        "category": "Education",
        "date": "2026-09-17",
        "payment_method": "UPI",
        "notes": "Updated with additional reference notebooks"
    }
    status, res = make_request(f"{BASE_URL}/api/expenses/{expense_id}", method='PUT', data=update_payload)
    print(f"   Status Code : {status}")
    print(f"   New Amount  : ₹{res.get('amount') if isinstance(res, dict) else None}")
    assert status == 200, f"Expected 200, got {status}"
    assert res['amount'] == 890.00, f"Amount mismatch: {res.get('amount')}"
    assert res['title'] == "College Textbooks & Reference Guides"
    print("   Result      : PASS ✅")

    # 5. VALIDATION: EMPTY TITLE
    print("\n[Test 5] POST /api/expenses - Validation: Empty Title")
    invalid_payload = {
        "title": "   ",
        "amount": 100.00,
        "category": "Food",
        "date": "2026-09-17",
        "payment_method": "Cash"
    }
    status, res = make_request(f"{BASE_URL}/api/expenses", method='POST', data=invalid_payload)
    print(f"   Status Code : {status}")
    print(f"   Error Msg   : {res.get('error') if isinstance(res, dict) else None}")
    assert status == 400, f"Expected 400 Bad Request, got {status}"
    print("   Result      : PASS ✅")

    # 6. VALIDATION: NEGATIVE AMOUNT
    print("\n[Test 6] POST /api/expenses - Validation: Negative Amount")
    invalid_amount_payload = {
        "title": "Lunch",
        "amount": -50.00,
        "category": "Food",
        "date": "2026-09-17",
        "payment_method": "Cash"
    }
    status, res = make_request(f"{BASE_URL}/api/expenses", method='POST', data=invalid_amount_payload)
    print(f"   Status Code : {status}")
    print(f"   Error Msg   : {res.get('error') if isinstance(res, dict) else None}")
    assert status == 400, f"Expected 400 Bad Request, got {status}"
    print("   Result      : PASS ✅")

    # 7. INVALID ID / 404 HANDLING
    print("\n[Test 7] GET /api/expenses/999999 - Non-Existent Expense ID (404)")
    status, res = make_request(f"{BASE_URL}/api/expenses/999999")
    print(f"   Status Code : {status}")
    print(f"   Error Msg   : {res.get('error') if isinstance(res, dict) else None}")
    assert status == 404, f"Expected 404 Not Found, got {status}"
    print("   Result      : PASS ✅")

    # 8. DELETE EXPENSE
    print(f"\n[Test 8] DELETE /api/expenses/{expense_id} - Delete Expense")
    status, res = make_request(f"{BASE_URL}/api/expenses/{expense_id}", method='DELETE')
    print(f"   Status Code : {status}")
    print(f"   Response    : {res.get('message') if isinstance(res, dict) else None}")
    assert status == 200, f"Expected 200, got {status}"

    # Confirm record is gone
    status, res = make_request(f"{BASE_URL}/api/expenses/{expense_id}")
    assert status == 404, "Deleted item should return 404"
    print("   Result      : PASS ✅")

    print("\n" + "=" * 60)
    print(" 🎉 ALL 8 API INTEGRATION TESTS COMPLETED & PASSED!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
