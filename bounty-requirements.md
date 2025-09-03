# AIxBlock Bug Bounty Requirements Checklist

## 📋 Mandatory Requirements

### ✅ Repository Actions (COMPLETED)
- [x] **Star the target repository** - Shows engagement and stays updated
- [x] **Fork the target repository** - Required for contribution and token claims
- [x] **Create participation repository** - Track research and progress

### 🎯 Submission Requirements

#### For Each Vulnerability Report:
- [ ] **Create GitHub Issue** using bug report template
- [ ] **Include vulnerability description** with technical details
- [ ] **Provide impact assessment** (concise but comprehensive)
- [ ] **Add screenshots/video evidence** for proof of concept
- [ ] **Create dedicated branch** (e.g., `bugfix/issue-123`)
- [ ] **Submit Pull Request** with working fix
- [ ] **Reference original issue** in PR description

## 💰 Reward Structure & Requirements

### Full Reward Eligibility (100%)
**Requirements**: Vulnerability report + Working code fix in PR
- **Critical** (9.0-10.0 CVSS): $750 + 1,500 AXB tokens + revenue share
- **High** (7.0-8.9 CVSS): $450 + 1,000 AXB tokens + revenue share  
- **Medium** (4.0-6.9 CVSS): $200 + 500 AXB tokens + revenue share
- **Low** (0.1-3.9 CVSS): 200 AXB tokens + revenue share

### Partial Reward (50%)
**Requirements**: Vulnerability report only (no working fix)
- Receive 50% of listed cash reward
- Full token reward still applies

### No Reward
- Duplicate reports
- Out-of-scope issues
- No security impact
- Invalid vulnerabilities

## 🎯 In-Scope Targets

| Domain | Priority | Asset Value | Description |
|--------|----------|-------------|-------------|
| `api.aixblock.io` | **Critical** | High | Model management & workflow execution |
| `workflow.aixblock.io` | **Critical** | High | Core automation workflow engine |
| `app.aixblock.io` | **High** | High | Primary UI for AI workflows |
| `webhook.aixblock.io` | **Medium** | Medium | Third-party integration hooks |
| `mcp.aixblock.io` | **Medium** | Medium | MCP layer connectors |
| `*.aixblock.io` | **Low** | Low | All first-party subdomains |

## ❌ Out-of-Scope Items

- Third-party services (Solana L1, Hugging Face, Roboflow)
- DoS/DDoS or spam/flood tests
- UI bugs with no security impact
- Proprietary/private models not in public repo

## 📝 Report Quality Standards

### Technical Description Must Include:
- **Vulnerability type** (XSS, IDOR, Auth bypass, etc.)
- **Root cause analysis** 
- **Attack vector explanation**
- **Affected components/endpoints**

### Impact Assessment Must Cover:
- **CVSS v3.1 scoring** with justification
- **Business impact** description
- **Potential data exposure** risks
- **System compromise** possibilities

### Proof of Concept Requirements:
- **Step-by-step reproduction** instructions
- **Working exploit code** (if applicable)
- **Screenshots/videos** demonstrating impact
- **Test environment** details

### Fix Implementation Standards:
- **Root cause** addressed in code
- **Security best practices** implemented
- **No breaking changes** to functionality
- **Testing verification** included

## ⏰ Response Timeline

| Stage | Target SLA | Description |
|-------|------------|-------------|
| **Acknowledgment** | < 48 hours | AIxBlock team confirms receipt |
| **Validation** | ≤ 7 business days | Severity assessment and reward confirmation |
| **Fix Review** | Variable | Code review and merge process |
| **Disclosure** | Post-merge | Public disclosure permitted after fix |

## 🔒 Rules of Engagement

### ✅ Allowed Activities:
- Testing with owned accounts only
- Responsible vulnerability disclosure
- Professional communication
- Collaborative fix development

### ❌ Prohibited Activities:
- Social engineering attacks
- Physical security testing
- Privacy violations
- Public disclosure before fix
- Service disruption (DoS/DDoS)
- Testing on accounts you don't own

## 💡 Success Tips

### Maximize Reward Potential:
1. **Always provide working fixes** - Required for full reward
2. **Target critical/high severity** - Higher cash rewards
3. **Include detailed PoCs** - Bonus rewards possible
4. **Focus on new features** - Automation workflows, MCP integration
5. **Chain vulnerabilities** - Single bounty for related issues

### Quality Over Quantity:
- **Thorough documentation** beats rushed reports
- **Working code fixes** are mandatory for full rewards
- **Professional presentation** improves acceptance chances
- **Clear impact demonstration** helps severity assessment

## 📞 Communication Channels

- **Primary**: GitHub Issues on target repository
- **Discord**: [AIxBlock Community](https://discord.gg/nePjg9g5v6)
- **Twitter**: [@AixBlock](https://x.com/AixBlock)
- **Telegram**: [AIxBlock Discussion](https://t.me/AIxBlock)

## 🏆 Payment Information

### Cash Rewards:
- Paid via bank transfer (fiat) or USDC (crypto)
- Distributed when total pool reaches $10,000 USD
- Public announcement across all channels

### Token Rewards:
- AXB tokens distributed on TGE date or 1 day after
- Additional revenue sharing opportunities
- Long-term token claim benefits

### Total Pool:
- **$10,000** cash rewards
- **$30,000** worth of AXB tokens

---

**Requirements Version**: 1.0  
**Last Updated**: September 3, 2025  
**Source**: [AIxBlock Bug Bounty Program](https://github.com/AIxBlock-2023/awesome-ai-dev-platform-opensource/blob/main/BugBounty.md)