# 🌌 Dialectic: Quick Reference

## The One-Liner
**"Autonomous community of AI agents that continuously learns from your codebase and maintains your `.cursor` folder without human intervention."**

## Who Owns What

| Person | Domain | Files | Key Responsibility |
|--------|--------|-------|-------------------|
| **Aria** | Dynamic Agent System | `mcp_server/`, `agents/`, `tests/` | Agent generation, event analysis, learning |
| **Shrey** | Infrastructure & Communication | `streams/`, `orchestration/`, `frontend/` | MCP server, Redpanda, StackAI, dashboard |

## Timeline Checkpoints

```
9:00  ┌─ Setup & Scaffold (0.5h)
9:30  ├─ Phase 1 MVP (2h) ──────────────┐
11:30 ├─ Integration Test #1 (0.5h)      │
12:00 ├─ Lunch (0.5h)                    │
12:30 ├─ Phase 2 Enhancement (1.5h) ────┤
14:00 ├─ Integration Test #2 (0.5h)      │
14:30 ├─ Phase 3 Polish (1h)             │
15:30 └─ Demo Prep & Submission (0.5h) ──┘
16:00
```

## Tech Stack

- **Sentry MCP Server**: Event detection and learning engine
- **Redpanda**: Real-time A2A communication streams  
- **StackAI**: Agent orchestration and workflow management
- **OpenAI GPT-4**: Dynamic agent generation
- **OpenAI GPT-3.5**: Documentation editing
- **Python FastAPI**: MCP server and API endpoints
- **React**: Real-time dashboard

## File Structure

```
dialectic/
├── mcp_server/           # Aria: Event detection & agent generation
├── agents/               # Aria: Dynamic agent creation
├── streams/              # Shrey: Redpanda integration
├── orchestration/        # Shrey: StackAI workflows
├── frontend/             # Shrey: Real-time dashboard
└── tests/                # Aria: Integration tests
```

## Key Interfaces

```python
# MCP Server Interface
@server.tool("detect_code_change")
async def detect_code_change(commit_data):
    return {"context": context, "needs_agents": True}

# Agent Generation Interface  
async def create_contextual_agents(context):
    return [SecurityAgent(), MVPAgent(), PerformanceAgent()]

# Redpanda Streaming Interface
async def stream_agent_message(agent_id, message):
    await client.produce(topic, {"agent_id": agent_id, "message": message})
```

## Push Order (Avoid Conflicts)

1. **Aria pushes first**: MCP server and agent generation
2. **Shrey pulls and integrates**: Redpanda streams and StackAI
3. **Aria pulls and tests**: Integration tests
4. **Shrey pushes dashboard**: Frontend updates
5. **Both test together**: Full system integration

## Common Issues + Fixes

| Problem | Solution |
|---------|----------|
| MCP server not detecting events | Use mock event handlers |
| Redpanda connection fails | Implement WebSocket fallback |
| StackAI workflow errors | Use simple agent coordination |
| Agent generation fails | Use predefined templates |
| Dashboard not updating | Check WebSocket connection |
| Documentation not updating | Verify file permissions |

## Demo Commands

```bash
# Start MCP server
python -m mcp_server.dialectic_mcp

# Test agent generation
python -m agents.agent_generator --test-context=security

# Run demo scenario
python -m demo.run_scenario --name=security_focus

# Open dashboard
open frontend/dashboard.html

# Full integration test
python -m tests.test_full_system --demo-mode
```

## The Pitch (60 seconds)

*"Every developer has a `.cursor` folder, but maintaining it manually is impossible. Dialectic is an autonomous community of AI agents that continuously learns from your codebase and maintains your development environment without human intervention. Watch as agents dynamically emerge based on your codebase needs - security agents for auth code, performance agents for optimization, documentation agents for new features. The system learns from every commit, every error, every debugging session, making your development environment a living, self-improving ecosystem. This isn't just documentation - it's the future of development environments."*

## If Things Break

| Component | Fallback |
|-----------|----------|
| MCP Server | Mock event handlers |
| Redpanda | WebSocket communication |
| StackAI | Simple agent coordination |
| Agent Generation | Predefined templates |
| Dashboard | Console output |
| Documentation | Manual updates |

## Pre-Submission Checklist

- [ ] All components integrated and working
- [ ] Demo scenarios tested and recorded  
- [ ] Pitch rehearsed and timed
- [ ] Devpost submission completed
- [ ] Code repository updated
- [ ] Sponsor integration documented
- [ ] At least 3 sponsors used meaningfully

## Winning Factors

1. **Dynamic Agent Generation**: No hardcoded roles, agents emerge based on context
2. **Event-Driven Learning**: System learns from real development events
3. **Zero Maintenance**: Documentation updates automatically
4. **Cost-Effective**: Uses cheaper models for low-risk tasks
5. **Living Environment**: Development environment as a living organism

## Communication

**How to Unblock:**
- **Aria blocked**: Check agent generation logic, use mock data
- **Shrey blocked**: Check Redpanda connection, use WebSocket fallback
- **Integration issues**: Run integration tests, check interfaces
- **Demo issues**: Use backup recording, simplify scenarios

## Mantras

**Aria**: "Dynamic agents, zero hardcoding, living system"
**Shrey**: "Real-time streams, seamless integration, bulletproof infrastructure"

---

**Ready to build the future of development environments!** 🚀