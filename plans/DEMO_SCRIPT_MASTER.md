# 🎭 Demo Script Master: Dialectic - Self-Learning Cursor Community

## 🎯 Demo Overview

**Duration**: 3 minutes  
**Target**: Judges and VCs  
**Goal**: Demonstrate autonomous documentation maintenance that learns from codebase changes

## 🎬 Demo Script

### **Opening Hook (30 seconds)**

**Aria**: "Every developer has a `.cursor` folder - but maintaining it manually is impossible. What if your development environment could maintain itself?"

**Visual**: Show the revolutionary `.cursor` folder structure
- 60+ specialized commands
- Comprehensive rules and patterns
- Structured knowledge management
- Cross-referenced documentation

**Aria**: "This is already revolutionary - but it requires constant manual updates. Meet Dialectic."

### **Core Demo (2 minutes)**

#### **Minute 1: Event Detection & Agent Generation (60 seconds)**

**Aria**: "Dialectic learns from your codebase and generates the right agents automatically."

**Demo Action**: Make a security-focused code change
```bash
# Simulate security-focused commit
git commit -m "Add authentication security measures"
```

**Visual**: Show Sentry MCP server detecting the change
- Real-time event detection
- Context analysis
- Development focus identification

**Aria**: "Watch as the system analyzes this security-focused change..."

**Visual**: Dynamic agent generation
- Security Specialist agent appears
- Agent prompt generated based on context
- Expertise domains automatically assigned

**Aria**: "No hardcoded agents - the system generates exactly what your codebase needs."

#### **Minute 2: Real-Time Collaboration (60 seconds)**

**Aria**: "Now watch agents collaborate in real-time to maintain your documentation."

**Visual**: Redpanda streams showing A2A communication
- Security agent analyzing implications
- Documentation agent updating guides
- Rule agent updating security patterns

**Aria**: "Agents communicate via Redpanda streams, orchestrated by StackAI workflows."

**Visual**: Live documentation updates
- `docs/security_patterns.md` updated automatically
- `rules/security_guidelines.mdc` enhanced
- `commands/security_debugging.md` created

**Aria**: "Documentation updates automatically as your codebase evolves."

#### **Minute 3: Context Adaptation & Learning (60 seconds)**

**Aria**: "But here's the magic - the system adapts to different development contexts."

**Demo Action**: Switch to MVP mode
```bash
# Simulate MVP-focused commit
git commit -m "Add MVP prototype endpoints"
```

**Visual**: Context switching
- Security agent disappears
- MVP Strategist agent emerges
- Focus shifts to rapid prototyping

**Aria**: "Watch agents adapt from security focus to MVP mode based on your actual development needs."

**Visual**: Learning demonstration
- System remembers previous patterns
- Documentation quality improves
- Agents get better at their roles

**Aria**: "The system learns from every development session, making your documentation better over time."

### **Closing Impact (30 seconds)**

**Aria**: "This isn't just documentation - it's a living development environment that grows with your codebase."

**Visual**: Show the evolution
- Documentation quality improving over time
- Agents becoming more specialized
- System adapting to different contexts

**Aria**: "Dialectic transforms your `.cursor` folder into an autonomous community of AI agents devoted to maintaining your development environment."

**Final Visual**: "Living Development Environment" with pulsing agents

## 🎭 Demo Scenarios

### **Scenario 1: Security Focus**
**Trigger**: `git commit -m "Add authentication security measures"`
**Expected Agents**: Security Specialist
**Expected Updates**: 
- `docs/security_patterns.md`
- `rules/security_guidelines.mdc`
- `commands/security_debugging.md`

### **Scenario 2: MVP Focus**
**Trigger**: `git commit -m "Add MVP prototype endpoints"`
**Expected Agents**: MVP Strategist
**Expected Updates**:
- `docs/mvp_guidelines.md`
- `rules/rapid_prototyping.mdc`
- `commands/mvp_development.md`

### **Scenario 3: Performance Focus**
**Trigger**: `git commit -m "Optimize database queries"`
**Expected Agents**: Performance Expert
**Expected Updates**:
- `docs/performance_patterns.md`
- `rules/optimization_guidelines.mdc`
- `commands/performance_debugging.md`

## 🎬 Demo Preparation

### **Pre-Demo Setup**
```bash
# Start all services
python -m mcp_server.dialectic_mcp &
python -m streams.redpanda_client &
python -m orchestration.stackai_client &

# Open dashboard
open frontend/dashboard.html

# Test demo scenarios
python -m demo.test_scenarios --all
```

### **Demo Data Preparation**
```python
# Create demo data
demo_data = {
    "security_scenario": {
        "commit_message": "Add authentication security measures",
        "files_changed": ["src/auth/login.py", "src/auth/permissions.py"],
        "expected_agents": ["Security Specialist"],
        "expected_updates": ["security_patterns.md", "security_guidelines.mdc"]
    },
    "mvp_scenario": {
        "commit_message": "Add MVP prototype endpoints", 
        "files_changed": ["src/api/endpoints.py", "src/api/routes.py"],
        "expected_agents": ["MVP Strategist"],
        "expected_updates": ["mvp_guidelines.md", "rapid_prototyping.mdc"]
    },
    "performance_scenario": {
        "commit_message": "Optimize database queries",
        "files_changed": ["src/db/queries.py", "src/db/optimization.py"],
        "expected_agents": ["Performance Expert"],
        "expected_updates": ["performance_patterns.md", "optimization_guidelines.mdc"]
    }
}
```

### **Backup Demo Recording**
```bash
# Record backup demo
python -m demo.record_demo --scenario=all --backup

# Create highlights
python -m demo.create_highlights --30-seconds

# Test playback
python -m demo.test_playback --full-test
```

## 🎯 Demo Success Criteria

### **Must Work (Non-Negotiable)**
- [ ] Agents generate dynamically based on context
- [ ] Documentation updates automatically
- [ ] Real-time communication visible
- [ ] Context switching demonstrated

### **Should Work (Strong Demo)**
- [ ] Learning demonstration over time
- [ ] Multiple sponsor integrations visible
- [ ] Smooth transitions between scenarios
- [ ] Clear value proposition communicated

### **Nice to Have (Legendary Demo)**
- [ ] Agents adapt to completely different contexts
- [ ] System shows improvement over time
- [ ] Judges are blown away by concept
- [ ] Memorable "living environment" moment

## 🎭 Demo Flow Diagram

```
Start Demo
    ↓
Show .cursor folder (30s)
    ↓
Make security commit
    ↓
Show agent generation (60s)
    ↓
Show real-time collaboration (60s)
    ↓
Switch to MVP mode
    ↓
Show context adaptation (60s)
    ↓
Show learning demonstration
    ↓
Closing impact (30s)
    ↓
End Demo
```

## 🎬 Demo Script Variations

### **Technical Audience**
- Focus on architecture and implementation details
- Show code examples and technical integration
- Emphasize scalability and performance

### **Business Audience**
- Focus on value proposition and ROI
- Show time savings and productivity gains
- Emphasize competitive advantage

### **Mixed Audience**
- Balance technical innovation with business value
- Use analogies and metaphors
- Focus on memorable moments

## 🎯 Demo Troubleshooting

### **If Agent Generation Fails**
- Use predefined agent templates
- Show rule-based agent selection
- Focus on documentation updates

### **If Real-Time Communication Fails**
- Use WebSocket fallback
- Show local message queue
- Use pre-recorded interactions

### **If Documentation Updates Fail**
- Use mock documentation updates
- Show simulated file changes
- Focus on agent collaboration

### **If Time Runs Out**
- Use backup recording
- Focus on core value proposition
- Prepare 60-second pitch

## 🎭 Demo Metrics

### **Engagement Metrics**
- Judges lean forward during agent generation
- Questions about learning mechanisms
- Interest in technical implementation

### **Memory Metrics**
- Judges remember "living environment" concept
- Recall dynamic agent generation
- Reference autonomous documentation

### **Impact Metrics**
- Judges want to use the system
- Interest in commercial application
- Recognition of innovation

---

**This demo script ensures a compelling, memorable demonstration of Dialectic's autonomous documentation maintenance capabilities.** 🎭