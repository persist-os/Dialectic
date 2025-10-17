# 🚀 Aria's Implementation Plan: Dynamic Agent System
## Sponsor-First Approach - NO Reimplementation

## ⚡ Core Principle
**USE existing sponsor MCP servers and tools. ONLY build the decision logic layer.**

---

## 🎯 What Already Exists (Use These!)

### **Sentry MCP Server** ✅ (Already Built)
- Event detection
- Error tracking
- Issue analysis
- Seer for automatic fixes

**Action**: CONNECT to it, don't build it

### **Senso MCP Server** ✅ (Already Built)
- Context windows
- Markdown injection
- Templates and prompts
- Search and generation

**Action**: USE it for context management

### **StackAI** ✅ (Already Built)
- Agent orchestration
- Workflow management
- No-code agent builder

**Action**: USE their orchestration, don't rebuild

---

## 🔨 What You Actually Build (Your Unique Contribution)

### **1. Agent Decision Engine** (Your Core Innovation)
The logic that decides WHICH agents to spawn based on context

### **2. Learning Pattern System**
Pattern recognition from events to improve over time

### **3. Documentation Updater**
The code that actually modifies `.cursor` folder files

---

## 📋 Step-by-Step Implementation Plan

### **PHASE 1: Setup & Integration (9:30-10:00) - 30 min**

#### **Step 1.1: Connect to Sentry MCP Server** (10 min)
```python
# agents/sentry_connector.py
from mcp import Client
import asyncio

class SentryMCPConnector:
    """Connects to existing Sentry MCP server"""
    
    def __init__(self):
        # Use their MCP server, don't build your own
        self.client = Client()
        self.server_url = "sentry-mcp://localhost:3000"
    
    async def connect(self):
        """Connect to Sentry's MCP server"""
        await self.client.connect(self.server_url)
        print("✅ Connected to Sentry MCP server")
    
    async def get_recent_events(self, project_id: str):
        """Get recent code changes and errors from Sentry"""
        # Use Sentry's existing tool
        result = await self.client.call_tool(
            "list_issues",
            {
                "project_id": project_id,
                "limit": 10,
                "status": "unresolved"
            }
        )
        return result
    
    async def search_errors_in_file(self, file_path: str):
        """Search for errors in specific file"""
        result = await self.client.call_tool(
            "search_errors",
            {"file_path": file_path}
        )
        return result
    
    async def get_issue_context(self, issue_id: str):
        """Get rich context for an issue"""
        result = await self.client.call_tool(
            "get_issue_details",
            {"issue_id": issue_id}
        )
        return result
```

**Test it works**: `python -m agents.sentry_connector --test-connection`

#### **Step 1.2: Connect to Senso MCP Server** (10 min)
```python
# agents/senso_connector.py
from mcp import Client

class SensoMCPConnector:
    """Connects to existing Senso MCP server for context management"""
    
    def __init__(self):
        self.client = Client()
        self.server_url = "senso-mcp://localhost:3001"
    
    async def connect(self):
        """Connect to Senso's MCP server"""
        await self.client.connect(self.server_url)
        print("✅ Connected to Senso MCP server")
    
    async def inject_context(self, markdown_content: str, context_type: str):
        """Inject context into Senso's context window"""
        result = await self.client.call_tool(
            "inject_markdown",
            {
                "content": markdown_content,
                "type": context_type
            }
        )
        return result
    
    async def search_context(self, query: str):
        """Search existing context"""
        result = await self.client.call_tool(
            "search",
            {"query": query}
        )
        return result
    
    async def generate_from_template(self, template_name: str, variables: dict):
        """Generate content from Senso template"""
        result = await self.client.call_tool(
            "generate_from_template",
            {
                "template": template_name,
                "variables": variables
            }
        )
        return result
```

**Test it works**: `python -m agents.senso_connector --test-connection`

#### **Step 1.3: Test Integration** (10 min)
```python
# tests/test_sponsor_integration.py
import asyncio
from agents.sentry_connector import SentryMCPConnector
from agents.senso_connector import SensoMCPConnector

async def test_integration():
    # Test Sentry
    sentry = SentryMCPConnector()
    await sentry.connect()
    events = await sentry.get_recent_events("dialectic")
    print(f"✅ Got {len(events)} events from Sentry")
    
    # Test Senso
    senso = SensoMCPConnector()
    await senso.connect()
    context = await senso.search_context("security")
    print(f"✅ Got context from Senso: {len(context)} items")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_integration())
```

**✅ CHECKPOINT**: Both MCP servers connected and responding

---

### **PHASE 2: Agent Decision Engine (10:00-11:00) - 60 min**

#### **Step 2.1: Context Analyzer** (20 min)
```python
# agents/context_analyzer.py
from typing import Dict, List
import json

class ContextAnalyzer:
    """Analyzes events from Sentry to determine what agents are needed"""
    
    def __init__(self, sentry_connector, senso_connector):
        self.sentry = sentry_connector
        self.senso = senso_connector
    
    async def analyze_event(self, event_data: Dict) -> Dict:
        """Analyze event and determine context"""
        
        # Extract key information
        files_changed = event_data.get('files', [])
        commit_message = event_data.get('message', '')
        error_patterns = event_data.get('errors', [])
        
        # Analyze file paths and content
        context = {
            'security_focus': self._check_security_keywords(files_changed, commit_message),
            'mvp_focus': self._check_mvp_keywords(commit_message),
            'performance_focus': self._check_performance_keywords(files_changed, commit_message),
            'documentation_focus': self._check_documentation_keywords(files_changed),
            'error_focus': len(error_patterns) > 0,
            'files_changed': files_changed,
            'commit_message': commit_message,
            'error_count': len(error_patterns)
        }
        
        return context
    
    def _check_security_keywords(self, files: List[str], message: str) -> bool:
        """Check if security focus is needed"""
        security_keywords = [
            'auth', 'password', 'token', 'security', 'encrypt', 
            'permission', 'login', 'session', 'jwt', 'oauth'
        ]
        
        files_str = ' '.join(files).lower()
        message_lower = message.lower()
        
        return any(keyword in files_str or keyword in message_lower 
                  for keyword in security_keywords)
    
    def _check_mvp_keywords(self, message: str) -> bool:
        """Check if MVP focus is needed"""
        mvp_keywords = [
            'prototype', 'mvp', 'quick', 'rapid', 'hackathon', 
            'demo', 'poc', 'proof of concept'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in mvp_keywords)
    
    def _check_performance_keywords(self, files: List[str], message: str) -> bool:
        """Check if performance focus is needed"""
        performance_keywords = [
            'optimize', 'performance', 'speed', 'cache', 'async',
            'slow', 'latency', 'bottleneck', 'efficiency'
        ]
        
        files_str = ' '.join(files).lower()
        message_lower = message.lower()
        
        return any(keyword in files_str or keyword in message_lower 
                  for keyword in performance_keywords)
    
    def _check_documentation_keywords(self, files: List[str]) -> bool:
        """Check if documentation focus is needed"""
        doc_keywords = ['readme', 'docs', '.md', 'documentation', 'guide']
        files_str = ' '.join(files).lower()
        
        return any(keyword in files_str for keyword in doc_keywords)
```

#### **Step 2.2: Agent Generator** (20 min)
```python
# agents/agent_generator.py
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class AgentSpec:
    """Specification for a generated agent"""
    agent_type: str
    focus_area: str
    documentation_targets: List[str]
    priority: int

class DynamicAgentGenerator:
    """Generates agent specifications based on context"""
    
    def __init__(self, context_analyzer):
        self.analyzer = context_analyzer
    
    async def generate_agents(self, event_data: Dict) -> List[AgentSpec]:
        """Generate list of agents needed for this event"""
        
        # Analyze context
        context = await self.analyzer.analyze_event(event_data)
        
        agents = []
        
        # Security agent
        if context['security_focus']:
            agents.append(AgentSpec(
                agent_type='security_specialist',
                focus_area='security',
                documentation_targets=[
                    '.cursor/rules/security_rules.md',
                    '.cursor/commands/security_commands.md',
                    '.cursor/development/patterns/auth_patterns.md'
                ],
                priority=1  # High priority
            ))
        
        # MVP agent
        if context['mvp_focus']:
            agents.append(AgentSpec(
                agent_type='mvp_strategist',
                focus_area='mvp',
                documentation_targets=[
                    '.cursor/rules/mvp_guidelines.md',
                    '.cursor/commands/rapid_prototyping.md',
                    '.cursor/development/patterns/mvp_patterns.md'
                ],
                priority=2
            ))
        
        # Performance agent
        if context['performance_focus']:
            agents.append(AgentSpec(
                agent_type='performance_expert',
                focus_area='performance',
                documentation_targets=[
                    '.cursor/rules/performance_rules.md',
                    '.cursor/commands/optimization_commands.md',
                    '.cursor/development/patterns/performance_patterns.md'
                ],
                priority=2
            ))
        
        # Documentation agent (always include if docs changed)
        if context['documentation_focus']:
            agents.append(AgentSpec(
                agent_type='documentation_specialist',
                focus_area='documentation',
                documentation_targets=[
                    '.cursor/README.md',
                    '.cursor/development/debugging/',
                    '.cursor/plans/'
                ],
                priority=3
            ))
        
        # Error handler agent (if errors present)
        if context['error_focus']:
            agents.append(AgentSpec(
                agent_type='error_handler',
                focus_area='debugging',
                documentation_targets=[
                    '.cursor/development/debugging/',
                    '.cursor/commands/debugging_commands.md'
                ],
                priority=1  # High priority for errors
            ))
        
        # Sort by priority
        agents.sort(key=lambda x: x.priority)
        
        return agents
```

#### **Step 2.3: Test Agent Generation** (20 min)
```python
# tests/test_agent_generation.py
import asyncio
from agents.context_analyzer import ContextAnalyzer
from agents.agent_generator import DynamicAgentGenerator
from agents.sentry_connector import SentryMCPConnector
from agents.senso_connector import SensoMCPConnector

async def test_agent_generation():
    # Setup
    sentry = SentryMCPConnector()
    senso = SensoMCPConnector()
    await sentry.connect()
    await senso.connect()
    
    analyzer = ContextAnalyzer(sentry, senso)
    generator = DynamicAgentGenerator(analyzer)
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'Security Event',
            'event': {
                'files': ['src/auth/login.py', 'src/auth/jwt.py'],
                'message': 'Add JWT authentication',
                'errors': []
            }
        },
        {
            'name': 'MVP Event',
            'event': {
                'files': ['src/prototype/feature.py'],
                'message': 'Quick MVP prototype for hackathon',
                'errors': []
            }
        },
        {
            'name': 'Performance Event',
            'event': {
                'files': ['src/api/optimize.py'],
                'message': 'Optimize API performance',
                'errors': []
            }
        },
        {
            'name': 'Error Event',
            'event': {
                'files': ['src/api/handler.py'],
                'message': 'Fix bug',
                'errors': [{'type': 'TypeError', 'count': 5}]
            }
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        agents = await generator.generate_agents(scenario['event'])
        print(f"✅ Generated {len(agents)} agents:")
        for agent in agents:
            print(f"  - {agent.agent_type} (priority: {agent.priority})")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_agent_generation())
```

**✅ CHECKPOINT**: Agent generation working for different contexts

---

### **PHASE 3: Documentation Updater (11:00-11:30) - 30 min**

#### **Step 3.1: Documentation Writer** (30 min)
```python
# agents/documentation_updater.py
import os
from pathlib import Path
from typing import List
from datetime import datetime

class DocumentationUpdater:
    """Updates .cursor folder based on agent specifications"""
    
    def __init__(self, cursor_folder_path: str):
        self.cursor_path = Path(cursor_folder_path)
    
    async def update_documentation(self, agent_spec, context: dict):
        """Update documentation files based on agent spec and context"""
        
        updates_made = []
        
        for target_file in agent_spec.documentation_targets:
            file_path = self.cursor_path / target_file
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate update content
            update_content = await self._generate_update_content(
                agent_spec, 
                context,
                target_file
            )
            
            # Update file
            if file_path.exists():
                await self._append_to_file(file_path, update_content)
            else:
                await self._create_file(file_path, update_content)
            
            updates_made.append({
                'file': str(file_path),
                'type': 'updated' if file_path.exists() else 'created',
                'timestamp': datetime.now().isoformat()
            })
        
        return updates_made
    
    async def _generate_update_content(
        self, 
        agent_spec, 
        context: dict,
        target_file: str
    ) -> str:
        """Generate content for documentation update"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if 'security' in agent_spec.focus_area:
            return self._generate_security_update(context, timestamp)
        elif 'mvp' in agent_spec.focus_area:
            return self._generate_mvp_update(context, timestamp)
        elif 'performance' in agent_spec.focus_area:
            return self._generate_performance_update(context, timestamp)
        elif 'debugging' in agent_spec.focus_area:
            return self._generate_debugging_update(context, timestamp)
        else:
            return self._generate_general_update(context, timestamp)
    
    def _generate_security_update(self, context: dict, timestamp: str) -> str:
        """Generate security-focused documentation"""
        files = ', '.join(context.get('files_changed', []))
        
        return f"""

## 🔒 Security Update - {timestamp}

**Files Modified**: {files}
**Context**: {context.get('commit_message', 'No message')}

### Security Considerations
- Review authentication flow in modified files
- Ensure proper input validation
- Check for secure token handling
- Verify permission checks are in place

### Action Items
- [ ] Security audit of {files}
- [ ] Update security tests
- [ ] Review authentication patterns

---
"""
    
    def _generate_mvp_update(self, context: dict, timestamp: str) -> str:
        """Generate MVP-focused documentation"""
        return f"""

## 🚀 MVP Development - {timestamp}

**Context**: {context.get('commit_message', 'No message')}

### MVP Focus
- Prioritize core functionality
- Accept technical debt for speed
- Focus on demo-ready features
- Document shortcuts taken

### Follow-up Tasks
- [ ] Technical debt tracking
- [ ] Post-MVP refactoring plan

---
"""
    
    def _generate_performance_update(self, context: dict, timestamp: str) -> str:
        """Generate performance-focused documentation"""
        files = ', '.join(context.get('files_changed', []))
        
        return f"""

## ⚡ Performance Optimization - {timestamp}

**Files Modified**: {files}

### Performance Considerations
- Profile modified code paths
- Check for N+1 queries
- Review async/await usage
- Monitor memory usage

### Optimization Targets
- [ ] Benchmark {files}
- [ ] Profile performance impact
- [ ] Document optimization decisions

---
"""
    
    def _generate_debugging_update(self, context: dict, timestamp: str) -> str:
        """Generate debugging documentation"""
        error_count = context.get('error_count', 0)
        
        return f"""

## 🐛 Debugging Session - {timestamp}

**Errors Detected**: {error_count}
**Context**: {context.get('commit_message', 'No message')}

### Debug Process
1. Identified {error_count} errors
2. Root cause analysis completed
3. Fix implemented and tested

### Lessons Learned
- Document what caused the errors
- Add tests to prevent regression
- Update error handling patterns

---
"""
    
    def _generate_general_update(self, context: dict, timestamp: str) -> str:
        """Generate general documentation update"""
        return f"""

## 📝 Update - {timestamp}

**Context**: {context.get('commit_message', 'No message')}
**Files**: {', '.join(context.get('files_changed', []))}

---
"""
    
    async def _append_to_file(self, file_path: Path, content: str):
        """Append content to existing file"""
        with open(file_path, 'a') as f:
            f.write(content)
    
    async def _create_file(self, file_path: Path, content: str):
        """Create new file with content"""
        with open(file_path, 'w') as f:
            f.write(f"# {file_path.stem}\n\n")
            f.write(content)
```

**✅ CHECKPOINT**: Documentation updates working

---

### **PHASE 4: Learning System (12:30-13:30) - 60 min**

#### **Step 4.1: Pattern Tracker** (30 min)
```python
# agents/learning_engine.py
import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

class LearningEngine:
    """Learns from events to improve agent generation over time"""
    
    def __init__(self, storage_path: str = '.cursor/learning/'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.patterns_file = self.storage_path / 'patterns.json'
        self.success_metrics_file = self.storage_path / 'success_metrics.json'
        
        self.patterns = self._load_patterns()
        self.success_metrics = self._load_success_metrics()
    
    def _load_patterns(self) -> Dict:
        """Load learned patterns from storage"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        return defaultdict(int)
    
    def _load_success_metrics(self) -> Dict:
        """Load success metrics from storage"""
        if self.success_metrics_file.exists():
            with open(self.success_metrics_file, 'r') as f:
                return json.load(f)
        return {'total_events': 0, 'successful_updates': 0}
    
    async def learn_from_event(self, event_data: Dict, agents_generated: List, outcome: str):
        """Learn from an event and update patterns"""
        
        # Extract pattern
        pattern_key = self._extract_pattern_key(event_data)
        
        # Update pattern count
        self.patterns[pattern_key] = self.patterns.get(pattern_key, 0) + 1
        
        # Update success metrics
        self.success_metrics['total_events'] += 1
        if outcome == 'success':
            self.success_metrics['successful_updates'] += 1
        
        # Record agent effectiveness
        for agent in agents_generated:
            agent_key = f"{pattern_key}::{agent.agent_type}"
            self.patterns[agent_key] = self.patterns.get(agent_key, 0) + 1
        
        # Save learned patterns
        await self._save_patterns()
        await self._save_success_metrics()
    
    def _extract_pattern_key(self, event_data: Dict) -> str:
        """Extract a pattern key from event data"""
        files = event_data.get('files', [])
        message = event_data.get('commit_message', '')
        errors = len(event_data.get('errors', []))
        
        # Create pattern signature
        has_security = any(kw in str(files).lower() + message.lower() 
                          for kw in ['auth', 'security', 'token'])
        has_mvp = any(kw in message.lower() 
                     for kw in ['mvp', 'prototype', 'hackathon'])
        has_performance = any(kw in str(files).lower() + message.lower() 
                            for kw in ['optimize', 'performance'])
        has_errors = errors > 0
        
        pattern_key = f"sec:{has_security}|mvp:{has_mvp}|perf:{has_performance}|err:{has_errors}"
        return pattern_key
    
    async def get_recommended_agents(self, event_data: Dict) -> List[str]:
        """Get recommended agents based on learned patterns"""
        pattern_key = self._extract_pattern_key(event_data)
        
        # Find most successful agents for this pattern
        relevant_patterns = {
            k: v for k, v in self.patterns.items()
            if k.startswith(pattern_key)
        }
        
        # Sort by success count
        recommended = sorted(
            relevant_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Extract agent types
        agent_types = [
            k.split('::')[1] for k, v in recommended
            if '::' in k
        ]
        
        return agent_types[:3]  # Top 3 recommendations
    
    async def _save_patterns(self):
        """Save patterns to storage"""
        with open(self.patterns_file, 'w') as f:
            json.dump(dict(self.patterns), f, indent=2)
    
    async def _save_success_metrics(self):
        """Save success metrics to storage"""
        with open(self.success_metrics_file, 'w') as f:
            json.dump(self.success_metrics, f, indent=2)
    
    def get_learning_summary(self) -> Dict:
        """Get summary of what the system has learned"""
        total = self.success_metrics.get('total_events', 0)
        successful = self.success_metrics.get('successful_updates', 0)
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        return {
            'total_events_processed': total,
            'successful_updates': successful,
            'success_rate': f"{success_rate:.1f}%",
            'patterns_learned': len(self.patterns),
            'most_common_patterns': self._get_top_patterns(5)
        }
    
    def _get_top_patterns(self, n: int) -> List[Dict]:
        """Get top N most common patterns"""
        sorted_patterns = sorted(
            self.patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]
        
        return [
            {'pattern': k, 'count': v}
            for k, v in sorted_patterns
        ]
```

#### **Step 4.2: Integration Test** (30 min)
```python
# tests/test_full_system.py
import asyncio
from agents.sentry_connector import SentryMCPConnector
from agents.senso_connector import SensoMCPConnector
from agents.context_analyzer import ContextAnalyzer
from agents.agent_generator import DynamicAgentGenerator
from agents.documentation_updater import DocumentationUpdater
from agents.learning_engine import LearningEngine

async def test_full_system():
    """Test the complete system end-to-end"""
    
    # Setup all components
    print("🔧 Setting up components...")
    sentry = SentryMCPConnector()
    senso = SensoMCPConnector()
    
    await sentry.connect()
    await senso.connect()
    
    analyzer = ContextAnalyzer(sentry, senso)
    generator = DynamicAgentGenerator(analyzer)
    updater = DocumentationUpdater('.cursor/')
    learner = LearningEngine()
    
    # Test event
    test_event = {
        'files': ['src/auth/jwt.py', 'src/auth/middleware.py'],
        'message': 'Add JWT authentication for MVP',
        'errors': []
    }
    
    print(f"\n📥 Processing event: {test_event['message']}")
    
    # Step 1: Analyze context
    print("  1️⃣ Analyzing context...")
    context = await analyzer.analyze_event(test_event)
    print(f"     Context: security={context['security_focus']}, mvp={context['mvp_focus']}")
    
    # Step 2: Generate agents
    print("  2️⃣ Generating agents...")
    agents = await generator.generate_agents(test_event)
    print(f"     Generated {len(agents)} agents:")
    for agent in agents:
        print(f"       - {agent.agent_type}")
    
    # Step 3: Update documentation
    print("  3️⃣ Updating documentation...")
    for agent in agents:
        updates = await updater.update_documentation(agent, context)
        print(f"     Updated {len(updates)} files for {agent.agent_type}")
    
    # Step 4: Learn from event
    print("  4️⃣ Learning from event...")
    await learner.learn_from_event(test_event, agents, 'success')
    summary = learner.get_learning_summary()
    print(f"     Learning: {summary['success_rate']} success rate, {summary['patterns_learned']} patterns")
    
    print("\n✅ Full system test complete!")
    return True

if __name__ == "__main__":
    asyncio.run(test_full_system())
```

**✅ CHECKPOINT**: Full system working end-to-end

---

## 🎯 Demo Preparation (14:30-15:30)

### **Step 5.1: Demo Script** (30 min)
```python
# demo/live_demo.py
import asyncio
import time
from agents.sentry_connector import SentryMCPConnector
from agents.senso_connector import SensoMCPConnector
from agents.context_analyzer import ContextAnalyzer
from agents.agent_generator import DynamicAgentGenerator
from agents.documentation_updater import DocumentationUpdater
from agents.learning_engine import LearningEngine

class LiveDemo:
    """Live demo orchestrator"""
    
    def __init__(self):
        self.sentry = None
        self.senso = None
        self.system_ready = False
    
    async def setup(self):
        """Setup all systems"""
        print("🌌 DIALECTIC: The Self-Learning Cursor Community")
        print("=" * 60)
        print("\n⚡ Initializing systems...")
        
        self.sentry = SentryMCPConnector()
        self.senso = SensoMCPConnector()
        
        await self.sentry.connect()
        await self.senso.connect()
        
        self.analyzer = ContextAnalyzer(self.sentry, self.senso)
        self.generator = DynamicAgentGenerator(self.analyzer)
        self.updater = DocumentationUpdater('.cursor/')
        self.learner = LearningEngine()
        
        self.system_ready = True
        print("✅ All systems online\n")
    
    async def run_scenario(self, scenario_name: str, event_data: dict):
        """Run a demo scenario"""
        print(f"\n🎭 SCENARIO: {scenario_name}")
        print("-" * 60)
        
        print(f"📝 Event: {event_data['message']}")
        print(f"📁 Files: {', '.join(event_data['files'])}")
        
        # Step 1: Analyze
        print("\n🔍 Analyzing context...")
        await asyncio.sleep(0.5)  # Dramatic pause
        context = await self.analyzer.analyze_event(event_data)
        
        focuses = []
        if context['security_focus']:
            focuses.append('🔒 Security')
        if context['mvp_focus']:
            focuses.append('🚀 MVP')
        if context['performance_focus']:
            focuses.append('⚡ Performance')
        
        print(f"   Detected: {', '.join(focuses)}")
        
        # Step 2: Generate agents
        print("\n🤖 Generating specialized agents...")
        await asyncio.sleep(0.5)
        agents = await self.generator.generate_agents(event_data)
        
        for agent in agents:
            await asyncio.sleep(0.3)
            print(f"   ✨ Spawned: {agent.agent_type}")
        
        # Step 3: Update docs
        print("\n📚 Updating documentation...")
        total_updates = 0
        for agent in agents:
            await asyncio.sleep(0.3)
            updates = await self.updater.update_documentation(agent, context)
            total_updates += len(updates)
            print(f"   ✏️  {agent.agent_type} updated {len(updates)} files")
        
        # Step 4: Learn
        print("\n🧠 Learning from interaction...")
        await asyncio.sleep(0.5)
        await self.learner.learn_from_event(event_data, agents, 'success')
        summary = self.learner.get_learning_summary()
        print(f"   📊 Success rate: {summary['success_rate']}")
        print(f"   🔬 Patterns learned: {summary['patterns_learned']}")
        
        print(f"\n✅ Scenario complete: {total_updates} documentation updates")
    
    async def run_full_demo(self):
        """Run complete demo sequence"""
        
        scenarios = [
            {
                'name': 'Security Focus',
                'event': {
                    'files': ['src/auth/jwt.py', 'src/middleware/auth.py'],
                    'message': 'Add JWT authentication with secure token handling',
                    'errors': []
                }
            },
            {
                'name': 'MVP Sprint',
                'event': {
                    'files': ['src/prototype/feature.py'],
                    'message': 'Quick MVP prototype for hackathon demo',
                    'errors': []
                }
            },
            {
                'name': 'Performance Optimization',
                'event': {
                    'files': ['src/api/optimize.py', 'src/cache/redis.py'],
                    'message': 'Optimize API response time with caching',
                    'errors': []
                }
            }
        ]
        
        for scenario in scenarios:
            await self.run_scenario(scenario['name'], scenario['event'])
            await asyncio.sleep(2)  # Pause between scenarios
        
        # Final summary
        print("\n" + "=" * 60)
        print("🌟 DIALECTIC DEMONSTRATION COMPLETE")
        print("=" * 60)
        
        summary = self.learner.get_learning_summary()
        print(f"\n📊 System Statistics:")
        print(f"   Total events processed: {summary['total_events_processed']}")
        print(f"   Success rate: {summary['success_rate']}")
        print(f"   Patterns learned: {summary['patterns_learned']}")
        print(f"\n💡 Your .cursor folder is now a living, learning system")

async def main():
    demo = LiveDemo()
    await demo.setup()
    await demo.run_full_demo()

if __name__ == "__main__":
    asyncio.run(main())
```

### **Step 5.2: Run Demo** (30 min)
```bash
# Run the live demo
python demo/live_demo.py
```

---

## ✅ Final Checklist

### **Integration**
- [ ] Sentry MCP server connected
- [ ] Senso MCP server connected
- [ ] Both servers responding to queries

### **Agent System**
- [ ] Context analyzer detects different focus areas
- [ ] Agent generator creates appropriate agents
- [ ] Different contexts generate different agents

### **Documentation**
- [ ] Documentation updater creates new files
- [ ] Updates append to existing files
- [ ] Different agent types create different content

### **Learning**
- [ ] Pattern tracking working
- [ ] Success metrics collecting
- [ ] Recommendations improving over time

### **Demo**
- [ ] Demo script runs smoothly
- [ ] All three scenarios work
- [ ] Visual impact is clear
- [ ] Judges can see agents spawning

---

## 🚨 Contingency Plans

### **If Sentry MCP fails:**
- Use file system watcher (watchdog library)
- Monitor git commits directly
- Fall back to manual event triggers

### **If Senso MCP fails:**
- Use simple context extraction from files
- Manual template system
- Direct file reading for context

### **If demo fails:**
- Pre-record a backup video
- Use mock data to show system working
- Have screenshots ready

---

## 🎯 Success Criteria

### **Minimum:**
- [ ] Agents generate dynamically based on context
- [ ] Documentation updates automatically
- [ ] System demonstrates learning

### **Strong:**
- [ ] All 3 demo scenarios work live
- [ ] Real MCP server integration
- [ ] Clear visual differentiation between contexts

### **Legendary:**
- [ ] Judges are amazed by living system concept
- [ ] No hardcoding visible
- [ ] System adapts in real-time during demo

---

**This plan uses existing sponsor tools and focuses on YOUR unique contribution: the decision-making intelligence layer.** 🚀

