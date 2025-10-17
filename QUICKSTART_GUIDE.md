# 🚀 Dialectic: Quickstart Guide for Aria

## 📚 Document Navigation

You have **4 key documents** for the hackathon:

1. **IMPLEMENTATION.md** (Main plan) - Complete team strategy and timeline
2. **ARIA_IMPLEMENTATION_PLAN.md** (Your detailed plan) - Step-by-step code examples
3. **ARIA_TIME_BLOCKS.md** (Quick reference) - Glanceable time blocks
4. **SOPHISTICATED_PATTERNS.md** (Talking points) - How to explain to judges

## ⚡ 30-Second Summary

**What you're building:** The decision logic layer that connects to sponsor MCP servers and decides which agents to spawn.

**What you're NOT building:** MCP servers (Sentry has it), streaming platform (Redpanda has it), orchestration (StackAI has it).

**Your unique contribution:** Dynamic agent generation based on context + learning system.

---

## 🎯 The Core Concept

```
Event (from Sentry) 
    ↓
Context Analysis (your code)
    ↓
Agent Generation Decision (your code)
    ↓
Documentation Update (your code)
    ↓
Learning (your code)
```

**Sponsors provide:** Event detection, streaming, orchestration
**You provide:** Intelligence and decision-making

---

## 📁 What You're Actually Building

### **5 Core Files** (in order):

1. **connectors/sentry_connector.py** (30 min)
   - Connect to Sentry's MCP server
   - Get events using their `list_issues` tool

2. **connectors/senso_connector.py** (10 min)  
   - Connect to Senso's MCP server
   - Use their `inject_markdown` tool

3. **agents/context_analyzer.py** (20 min)
   - Analyze events to detect security/MVP/performance focus
   - Simple keyword matching

4. **agents/agent_generator.py** (20 min)
   - Generate `AgentSpec` objects based on context
   - No actual agents, just specifications

5. **agents/documentation_updater.py** (30 min)
   - Actually modify .cursor folder files
   - Append formatted markdown

**Bonus (if time):**

6. **agents/learning_engine.py** (30 min)
   - Track patterns in JSON file
   - Calculate success rate

7. **demo/live_demo.py** (30 min)
   - Orchestrate demo with dramatic pauses
   - Show system working end-to-end

---

## ⏱️ Your Timeline (At a Glance)

| Time | What | Status |
|------|------|--------|
| 9:30-10:00 | Connect to Sentry & Senso MCP | ✅ Must have |
| 10:00-10:30 | Build Context Analyzer | ✅ Must have |
| 10:30-11:00 | Build Agent Generator | ✅ Must have |
| 11:00-11:30 | Test integrations | ✅ Must have |
| **11:30-12:00** | **Integration Test #1** | **CHECKPOINT** |
| 12:00-12:30 | 🍕 Lunch & review | Break |
| 12:30-13:30 | Build Documentation Updater | ✅ Must have |
| 13:30-14:00 | Build Learning Engine | ⭐ Nice to have |
| **14:00-14:30** | **Integration Test #2** | **CHECKPOINT** |
| 14:30-15:30 | Build Demo Script & Polish | ⭐ Nice to have |
| **15:30-16:00** | **Submit & Prepare Demo** | **DEADLINE** |

---

## 🔧 Code Snippets (Copy-Paste Ready)

### **Minimal Sentry Connector** (10 min)
```python
from mcp import Client

class SentryMCPConnector:
    def __init__(self):
        self.client = Client()
    
    async def connect(self):
        await self.client.connect("sentry-mcp://localhost:3000")
    
    async def get_recent_events(self, project_id):
        return await self.client.call_tool("list_issues", {"project_id": project_id})
```

### **Minimal Context Analyzer** (15 min)
```python
class ContextAnalyzer:
    def analyze_event(self, event_data):
        text = str(event_data.get('files', [])) + event_data.get('message', '')
        return {
            'security_focus': any(kw in text.lower() for kw in ['auth', 'password', 'token']),
            'mvp_focus': any(kw in text.lower() for kw in ['mvp', 'prototype', 'hackathon']),
            'performance_focus': any(kw in text.lower() for kw in ['optimize', 'performance'])
        }
```

### **Minimal Agent Generator** (15 min)
```python
from dataclasses import dataclass

@dataclass
class AgentSpec:
    agent_type: str
    focus_area: str
    documentation_targets: list
    priority: int

class DynamicAgentGenerator:
    def generate_agents(self, event_data, context):
        agents = []
        if context['security_focus']:
            agents.append(AgentSpec('security_specialist', 'security', ['.cursor/rules/security_rules.md'], 1))
        if context['mvp_focus']:
            agents.append(AgentSpec('mvp_strategist', 'mvp', ['.cursor/rules/mvp_guidelines.md'], 2))
        return sorted(agents, key=lambda x: x.priority)
```

---

## 🎭 Demo Flow (What Judges Will See)

### **Opening (15 seconds)**
"Watch what happens when I commit code to a project..."

### **Scenario 1: Security Event (45 seconds)**
```
Event: "Add JWT authentication"
Files: auth/jwt.py, middleware/auth.py

→ System detects "auth" keyword
→ Spawns Security Specialist agent  
→ Updates security_rules.md automatically
→ Shows learning stats
```

### **Scenario 2: MVP Event (45 seconds)**
```
Event: "Quick MVP prototype for demo"
Files: prototype/feature.py

→ System detects "MVP" + "prototype"
→ Spawns MVP Strategist agent
→ Updates mvp_guidelines.md automatically
→ Shows pattern learned
```

### **Scenario 3: Performance Event (45 seconds)**
```
Event: "Optimize API with Redis caching"
Files: api/optimize.py, cache/redis.py

→ System detects "optimize" + "cache"
→ Spawns Performance Expert agent
→ Updates performance_rules.md automatically
→ Shows improvement over time
```

### **Closing (15 seconds)**
"The system learned from 3 events, spawned 3 different agents, and updated documentation automatically. **This is a living development environment.**"

---

## 🚨 Fallback Plan (If Things Break)

### **If Sentry MCP fails:**
```python
# Use file system watcher instead
import watchdog
watcher = FileSystemWatcher()
watcher.watch(project_path)
```

### **If Senso MCP fails:**
```python
# Use simple file reading
with open('.cursor/context.md', 'r') as f:
    context = f.read()
```

### **If demo fails:**
- Have pre-recorded video ready
- Show screenshots of working system
- Walk through code and explain logic

---

## 💬 What to Say to Judges

### **When they ask: "What makes this different?"**
> "Most systems use hardcoded agents. We built a system where agents **emerge dynamically** based on what your codebase actually needs. Security code gets security agents. MVP code gets MVP agents. **The system adapts to context, not rules.**"

### **When they ask: "How are you using sponsors?"**
> "We're using **Sentry's MCP server** for event detection, **Senso's MCP server** for context management, **Redpanda** for agent communication streams, and **StackAI** for orchestration. We didn't rebuild any of these – we built the **intelligence layer** that connects them."

### **When they ask: "Does it really learn?"**
> "Yes. Watch – first time I commit auth code, it tries several agents. **Second time**, it learned which agent was most effective and prioritized that one. It's tracking patterns in real-time."

### **When they ask: "Is this production-ready?"**
> "We built in **graceful degradation**. If Sentry goes down, it falls back to file watching. If agent generation fails, it uses safe defaults. **Every component has a fallback.**"

---

## ✅ Success Checklist

### **Minimum Viable (Must Have for Demo)**
- [ ] Connected to Sentry MCP server
- [ ] Connected to Senso MCP server  
- [ ] Context analyzer detects security/MVP/performance
- [ ] Agent generator creates different agents for different contexts
- [ ] Documentation updater modifies .cursor files
- [ ] Demo script runs 3 scenarios smoothly

### **Strong Demo (Nice to Have)**
- [ ] Learning engine tracks patterns
- [ ] Success rate improves over time
- [ ] Dashboard shows real-time updates
- [ ] All 3 sponsors integrated meaningfully

### **Legendary (If Extra Time)**
- [ ] Agents adapt to completely different contexts
- [ ] Visual agent generation animation
- [ ] Learning recommendations based on history
- [ ] Judges say "wow, this is impressive"

---

## 🎯 Remember

**Core principle:** Connect to sponsors, don't rebuild them.

**Unique value:** Decision logic – which agents to spawn based on context.

**Demo impact:** Visual, dramatic, memorable. Agents spawning/disappearing dynamically.

**Story:** "Living development environment that grows with your codebase."

---

**You've got this! Focus on the intelligence layer and let sponsors handle infrastructure.** 🚀

*See ARIA_TIME_BLOCKS.md for detailed time blocks*
*See SOPHISTICATED_PATTERNS.md for technical talking points*

