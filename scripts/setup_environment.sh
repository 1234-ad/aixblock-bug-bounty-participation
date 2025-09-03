#!/bin/bash

# AIxBlock Bug Bounty Environment Setup Script
# Run this script to set up your testing environment

echo "🚀 Setting up AIxBlock Bug Bounty Testing Environment..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "📥 Installing required Python packages..."
pip3 install requests beautifulsoup4 pyjwt sqlparse urllib3 colorama

# Create directories for findings
echo "📁 Creating directory structure..."
mkdir -p research/findings/critical
mkdir -p research/findings/high
mkdir -p research/findings/medium
mkdir -p research/findings/low
mkdir -p research/poc
mkdir -p research/fixes
mkdir -p logs

# Create log files
touch logs/testing.log
touch logs/vulnerabilities.log

# Make scripts executable
chmod +x scripts/*.py
chmod +x scripts/*.sh

# Download additional tools (optional)
echo "🛠️ Setting up additional security tools..."

# Create a tools directory
mkdir -p tools/external

# Download common wordlists
echo "📝 Downloading wordlists..."
curl -s https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt -o tools/external/common_endpoints.txt
curl -s https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/XSS/XSS-Jhaddix.txt -o tools/external/xss_payloads.txt

# Create configuration file
echo "⚙️ Creating configuration file..."
cat > config/testing_config.json << EOF
{
    "target_domains": [
        "app.aixblock.io",
        "api.aixblock.io", 
        "workflow.aixblock.io",
        "mcp.aixblock.io",
        "webhook.aixblock.io"
    ],
    "test_accounts": {
        "primary": {
            "username": "",
            "password": "",
            "email": ""
        },
        "secondary": {
            "username": "",
            "password": "",
            "email": ""
        }
    },
    "session_cookies": {
        "sessionid": "",
        "csrftoken": ""
    },
    "testing_settings": {
        "max_concurrent_requests": 10,
        "request_delay": 1,
        "timeout": 30
    }
}
EOF

# Create testing checklist
echo "📋 Creating testing checklist..."
cat > TESTING_CHECKLIST.md << EOF
# AIxBlock Security Testing Checklist

## 🔧 Environment Setup
- [x] Virtual environment created
- [x] Dependencies installed
- [x] Directory structure created
- [ ] Test accounts created on AIxBlock platform
- [ ] Session cookies configured
- [ ] Burp Suite configured

## 🎯 Testing Phases

### Phase 1: Reconnaissance
- [ ] Platform exploration completed
- [ ] API endpoints mapped
- [ ] Technology stack analyzed
- [ ] Attack surface documented

### Phase 2: Automated Testing
- [ ] IDOR vulnerability testing
- [ ] File upload security testing
- [ ] Authentication bypass testing
- [ ] Rate limiting testing
- [ ] XSS vulnerability testing

### Phase 3: Manual Testing
- [ ] Business logic testing
- [ ] Session management testing
- [ ] CSRF protection testing
- [ ] Input validation testing
- [ ] Authorization testing

### Phase 4: Reporting
- [ ] Vulnerabilities documented
- [ ] Proof of concepts created
- [ ] Fixes implemented
- [ ] GitHub issues submitted
- [ ] Pull requests created

## 📊 Progress Tracking
- **Vulnerabilities Found**: 0
- **Issues Submitted**: 0
- **Pull Requests**: 0
- **Estimated Reward**: \$0 + 0 AXB tokens
EOF

echo "✅ Environment setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Create test accounts on https://app.aixblock.io"
echo "2. Update config/testing_config.json with your account details"
echo "3. Configure Burp Suite proxy"
echo "4. Run: python3 scripts/automated_testing.py"
echo "5. Follow the testing checklist in TESTING_CHECKLIST.md"
echo ""
echo "🔍 Happy bug hunting!"