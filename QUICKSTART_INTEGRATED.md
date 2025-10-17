# 🚀 Quick Start: Integrated Dialectic System

**Last Updated**: 2025-10-17  
**Status**: READY TO DEMO

---

## 🎯 What This Does

This runs the **complete integrated system** showing:
- **Aria's backend**: Agent generation, documentation updates, learning
- **Shrey's frontend**: Real-time dashboard, beautiful visualization
- **StackAI**: Workflow orchestration with real API
- **Redpanda**: Event streaming
- **WebSocket**: Real-time backend ↔ frontend communication

---

## 🏃 Quick Start (30 seconds)

### Option 1: Run Integration Example

```bash
cd /Users/ariahan/Documents/hackathons/projects/Dialectic

# Terminal 1: Start the integrated backend
python demo/INTEGRATION_EXAMPLE.py

# Terminal 2: Open the dashboard
open frontend/dashboard.html
```

**What happens:**
1. Backend starts on `ws://localhost:8000/ws`
2. Dashboard connects automatically
3. Click demo buttons → See real agents spawn
4. Watch documentation update in real-time
5. See stats increment live

### Option 2: Run Full Auto-Sequence Demo

```bash
# Run all scenarios automatically
python demo/INTEGRATION_EXAMPLE.py sequence
```

This runs 3 scenarios back-to-back without needing the frontend.

---

## 📋 Step-by-Step Setup

### 1. **Check Dependencies**

```bash
# Make sure you're in the venv
source venv/bin/activate

# Check requirements
pip list | grep -E "websockets|litellm|sentry-sdk"
```

If missing:
```bash
pip install websockets
```

### 2. **Test WebSocket Bridge**

```bash
# Test the bridge standalone
python demo/websocket_bridge.py
```

Expected output:
```
🌐 WebSocket server ready at ws://localhost:8000/ws
   Connect from: ws://localhost:8000/ws
   Open dashboard.html to test
```

Press Ctrl+C to stop, then move to integrated demo.

### 3. **Run Integrated Demo**

```bash
# Start the full system
python demo/INTEGRATION_EXAMPLE.py
```

Expected output:
```
🌌 DIALECTIC: Integrated System
==================================================================

⚡ Initializing all components...
   ✅ Sentry SDK initialized
   ✅ Redpanda streaming ready
   ✅ Message handlers registered
   ✅ WebSocket bridge started
   ✅ Demo triggers registered

🎉 All systems online!
📊 Dashboard: http://localhost:8080/dashboard.html
🌐 WebSocket: ws://localhost:8000/ws

⏸️  Demo server running...
   Open dashboard.html and click demo buttons
   Press Ctrl+C to stop
```

### 4. **Open Dashboard**

```bash
# In another terminal
open frontend/dashboard.html
```

Or manually:
1. Open browser
2. Navigate to `frontend/dashboard.html`
3. Should see "🟢 Connected" in top right

### 5. **Click Demo Buttons**

Click any demo button:
- **Security Focus Demo**
- **MVP Focus Demo**
- **Performance Focus Demo**

Watch:
- Agents appear in real-time
- Documentation updates stream in
- Stats increment
- Console shows full flow

---

## 🔍 What's Happening Behind the Scenes

### When You Click "Security Focus Demo":

```
Frontend Button Click
    ↓
WebSocket sends: {action: 'trigger_demo', scenario: 'security'}
    ↓
Backend receives trigger
    ↓
Context Analyzer analyzes security event
    ↓
AI Agent Generator spawns security_specialist agent
    ↓
WebSocket broadcasts: {type: 'agent_generated', agent: {...}}
    ↓
Frontend dashboard adds agent card
    ↓
StackAI Client creates workflow
    ↓
StackAI API executes workflow
    ↓
WebSocket broadcasts: {type: 'workflow_executed', ...}
    ↓
Documentation Updater writes to .cursor/ folder
    ↓
WebSocket broadcasts: {type: 'documentation_updated', ...}
    ↓
Frontend shows update in feed
    ↓
Redpanda streams all events
    ↓
Learning Engine processes pattern
    ↓
WebSocket broadcasts: {type: 'learning_event', ...}
    ↓
Frontend increments stats
```

### All 3 Systems Working Together:
1. **Aria's Backend** (Python) - Intelligence layer
2. **Shrey's Infrastructure** (StackAI + Redpanda) - Orchestration
3. **Shrey's Frontend** (HTML/JS) - Visualization

---

## 🧪 Testing Each Component

### Test 1: WebSocket Communication
```bash
# Terminal 1
python demo/websocket_bridge.py

# Terminal 2
# Open browser console at dashboard.html
# Check for "Connected to Dialectic backend"
```

### Test 2: Agent Generation
```bash
# Run just agent generation
python agents/dynamic_agent_generator.py
```

### Test 3: StackAI Integration
```bash
# Test StackAI client
python orchestration/stackai_client.py
```

### Test 4: Redpanda Streaming
```bash
# Test Redpanda client
python streams/redpanda_client.py
```

### Test 5: Full Integration
```bash
# Run complete integrated demo
python demo/INTEGRATION_EXAMPLE.py
```

---

## 📁 Check the Results

### Documentation Files Created
```bash
# Check .cursor folder
ls -la .cursor/rules/
ls -la .cursor/commands/
cat .cursor/rules/security_rules.md
```

### Learning Data
```bash
# Check learning patterns
cat .cursor/learning/patterns.json
cat .cursor/learning/success_metrics.json
```

### Redpanda Logs
```bash
# Check Redpanda status
cat redpanda_config.yaml
```

---

## 🎬 Demo Script for Judges

### 30-Second Pitch
```
"Watch as our system detects code changes, spawns specialized AI agents 
dynamically, updates documentation automatically, and learns from patterns - 
all in real-time with StackAI orchestration and Redpanda streaming."
```

### Live Demo Flow (3 minutes)

1. **Show Dashboard** (10 seconds)
   - "This is our real-time agent dashboard"
   - Point out stats at zero

2. **Trigger Security Demo** (30 seconds)
   - Click "Security Focus Demo"
   - "Watch agents spawn in real-time"
   - Point to security specialist card appearing
   - "See documentation updating live"
   - Point to update feed

3. **Trigger MVP Demo** (30 seconds)
   - Click "MVP Focus Demo"
   - "Different context, different agents"
   - Show MVP strategist spawning
   - "All automatic, no hardcoding"

4. **Show Learning** (30 seconds)
   - Point to learning events counter
   - "System learns patterns over time"
   - Open `.cursor/learning/patterns.json`

5. **Show Integration** (30 seconds)
   - "StackAI orchestrating workflows"
   - "Redpanda streaming events"
   - "Sentry tracking everything"
   - Show integration status in console

6. **Show Real Files** (30 seconds)
   - Open `.cursor/rules/security_rules.md`
   - "Real documentation, automatically generated"
   - "Based on actual code context"

---

## 🚨 Troubleshooting

### Problem: Dashboard shows "🔴 Disconnected"
**Solution:**
```bash
# Make sure backend is running
python demo/INTEGRATION_EXAMPLE.py

# Check if WebSocket port is open
lsof -i :8000
```

### Problem: No agents appearing
**Solution:**
```bash
# Check console for errors
# Make sure all imports work
python -c "from demo.INTEGRATION_EXAMPLE import *"
```

### Problem: StackAI API errors
**Solution:**
```bash
# Check API key in orchestration/stackai_client.py
# Fallback mode will activate automatically
```

### Problem: Redpanda not starting
**Solution:**
```bash
# Check if rpk is installed
rpk --version

# System will fallback to mock mode if not available
# Mock mode still demonstrates the concept
```

---

## 🎯 Success Criteria

You know it's working when:
- ✅ Dashboard shows "🟢 Connected"
- ✅ Clicking buttons spawns agents in real-time
- ✅ Documentation updates appear in feed
- ✅ Stats increment (agents, updates, workflows, learning)
- ✅ Files created in `.cursor/` folder
- ✅ Console shows full flow
- ✅ No errors in console

---

## 💡 Key Files Reference

### Aria's Backend
- `agents/context_analyzer.py` - Analyzes events
- `agents/dynamic_agent_generator.py` - Spawns agents
- `agents/documentation_updater.py` - Updates files
- `agents/learning_engine.py` - Learns patterns

### Shrey's Infrastructure
- `orchestration/stackai_client.py` - StackAI integration
- `streams/redpanda_client.py` - Redpanda streaming
- `streams/message_handler.py` - Message routing

### Shrey's Frontend
- `frontend/dashboard.html` - Dashboard UI
- `frontend/demo_interface.js` - Real-time updates

### Integration Bridge
- `demo/websocket_bridge.py` - WebSocket server
- `demo/INTEGRATION_EXAMPLE.py` - Full integration

---

## 🚀 Ready to Demo!

```bash
# One command to rule them all
python demo/INTEGRATION_EXAMPLE.py

# Then open dashboard
open frontend/dashboard.html

# Click buttons and watch the magic happen! ✨
```

**Time to set up**: 30 seconds  
**Time to wow judges**: 3 minutes  
**Integration status**: 100% READY 🎉

