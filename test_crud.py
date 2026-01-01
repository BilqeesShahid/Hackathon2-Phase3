#!/usr/bin/env python3
"""
End-to-End CRUD Test Script

Tests all CRUD operations via the chat API endpoint.
"""

import requests
import json
import sys

API_URL = "http://localhost:8000"

# You'll need to replace this with a valid JWT token from your login
# Get it from browser localStorage or by calling the sign-in endpoint
TEST_TOKEN = "YOUR_TOKEN_HERE"
TEST_USER_ID = "YOUR_USER_ID_HERE"

def test_chat(message: str, conversation_id=None):
    """Send a chat message and return the response"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TEST_TOKEN}"
    }

    payload = {"message": message}
    if conversation_id:
        payload["conversation_id"] = conversation_id

    response = requests.post(
        f"{API_URL}/api/{TEST_USER_ID}/chat",
        headers=headers,
        json=payload
    )

    print(f"\n{'='*60}")
    print(f"USER: {message}")
    print(f"{'='*60}")

    if response.status_code == 200:
        data = response.json()
        print(f"ASSISTANT: {data['response']}")
        return data['conversation_id']
    else:
        print(f"ERROR {response.status_code}: {response.text}")
        return conversation_id

def main():
    print("🧪 Testing CRUD Operations via Chat API")
    print(f"API URL: {API_URL}")

    if TEST_TOKEN == "YOUR_TOKEN_HERE":
        print("\n❌ ERROR: Please update TEST_TOKEN and TEST_USER_ID in this script")
        print("You can get these from:")
        print("1. Sign in at http://localhost:3000")
        print("2. Open browser console (F12)")
        print("3. Run: JSON.parse(localStorage.getItem('auth_session'))")
        sys.exit(1)

    conversation_id = None

    # Test 1: CREATE - Add tasks
    print("\n📝 Test 1: CREATE (Add Tasks)")
    conversation_id = test_chat("Add buy milk", conversation_id)
    conversation_id = test_chat("Add call dentist", conversation_id)
    conversation_id = test_chat("Add finish homework", conversation_id)

    # Test 2: READ - List tasks
    print("\n\n📋 Test 2: READ (List Tasks)")
    conversation_id = test_chat("Show my tasks", conversation_id)

    # Test 3: UPDATE - Change task
    print("\n\n✏️ Test 3: UPDATE (Change Task)")
    conversation_id = test_chat("Change task 1 to buy organic milk", conversation_id)
    conversation_id = test_chat("Show my tasks", conversation_id)

    # Test 4: COMPLETE - Mark task done
    print("\n\n✅ Test 4: COMPLETE (Mark Done)")
    conversation_id = test_chat("Complete task 2", conversation_id)
    conversation_id = test_chat("Show my tasks", conversation_id)

    # Test 5: DELETE - Remove task
    print("\n\n🗑️ Test 5: DELETE (Remove Task)")
    conversation_id = test_chat("Delete task 3", conversation_id)
    conversation_id = test_chat("Show my tasks", conversation_id)

    # Test 6: Filter tests
    print("\n\n🔍 Test 6: FILTERS")
    conversation_id = test_chat("Show pending tasks", conversation_id)
    conversation_id = test_chat("Show completed tasks", conversation_id)

    print("\n\n✅ All CRUD tests completed!")
    print(f"Conversation ID: {conversation_id}")

if __name__ == "__main__":
    main()
