"""
INTEGRATION EXAMPLE
Shows how to connect Aria's backend to Shrey's frontend

This demonstrates the key integration points between:
- Aria's agent system (context_analyzer, agent_generator, etc.)
- Shrey's infrastructure (StackAI, Redpanda, dashboard)
- The WebSocket bridge connecting them

Copy these patterns into live_demo.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# ARIA'S COMPONENTS
from agents.context_analyzer import ContextAnalyzer
from agents.dynamic_agent_generator import AIAgentGenerator
from agents.documentation_updater import DocumentationUpdater
from agents.learning_engine import LearningEngine
from config.sentry_config import initialize_sentry, capture_agent_event

# SHREY'S COMPONENTS
from orchestration.stackai_client import StackAIClient
from streams.redpanda_client import RedpandaClient
from streams.message_handler import MessageHandler, MessageType

# INTEGRATION BRIDGE
from demo.websocket_bridge import WebSocketBridge


class IntegratedDialecticDemo:
    """
    Fully integrated demo showing Aria + Shrey's work together
    
    This connects:
    - Backend agent system → WebSocket → Frontend dashboard
    - StackAI workflows
    - Redpanda streaming
    - Real-time visualization
    """
    
    def __init__(self):
        # ARIA'S COMPONENTS
        self.analyzer = ContextAnalyzer()
        self.generator = AIAgentGenerator()
        self.updater = DocumentationUpdater('.cursor/')
        self.learner = LearningEngine()
        
        # SHREY'S COMPONENTS
        self.stackai = StackAIClient()
        self.redpanda = RedpandaClient()
        self.message_handler = MessageHandler()
        
        # INTEGRATION BRIDGE
        self.ws_bridge = WebSocketBridge()
        
        # Stats
        self.demo_stats = {
            'events_processed': 0,
            'agents_spawned': 0,
            'files_updated': 0,
            'workflows_executed': 0
        }
    
    async def setup(self):
        """Initialize all systems"""
        print("🌌 DIALECTIC: Integrated System")
        print("=" * 70)
        print("\n⚡ Initializing all components...")
        
        # Initialize Sentry
        initialize_sentry(environment="demo")
        print("   ✅ Sentry SDK initialized")
        
        # Setup Redpanda streaming
        await self.redpanda.setup_streams()
        print("   ✅ Redpanda streaming ready")
        
        # Register message handlers
        self._setup_message_handlers()
        print("   ✅ Message handlers registered")
        
        # Start WebSocket bridge
        await self.ws_bridge.start()
        print("   ✅ WebSocket bridge started")
        
        # Register demo triggers
        self._register_demo_triggers()
        print("   ✅ Demo triggers registered")
        
        print("\n🎉 All systems online!")
        print(f"📊 Dashboard: http://localhost:8080/dashboard.html")
        print(f"🌐 WebSocket: {self.ws_bridge.get_stats()['server_address']}\n")
    
    def _setup_message_handlers(self):
        """Setup Redpanda message handlers"""
        
        async def handle_agent_message(message):
            """Handle agent communication messages"""
            print(f"💬 Agent message: {message.content}")
        
        async def handle_doc_update(message):
            """Handle documentation updates"""
            print(f"📝 Documentation updated: {message.content.get('file')}")
        
        self.message_handler.register_handler(
            MessageType.COMMUNICATION,
            handle_agent_message
        )
        self.message_handler.register_handler(
            MessageType.DOCUMENTATION_UPDATE,
            handle_doc_update
        )
    
    def _register_demo_triggers(self):
        """Register handlers for frontend demo buttons"""
        
        async def trigger_security(scenario):
            event = {
                'files': ['src/auth/jwt.py', 'src/middleware/auth.py'],
                'message': 'Add JWT authentication with secure token handling',
                'errors': []
            }
            await self.run_scenario('Security Focus', event)
        
        async def trigger_mvp(scenario):
            event = {
                'files': ['src/prototype/feature.py'],
                'message': 'Quick MVP prototype for hackathon demo',
                'errors': []
            }
            await self.run_scenario('MVP Sprint', event)
        
        async def trigger_performance(scenario):
            event = {
                'files': ['src/api/optimize.py', 'src/cache/redis.py'],
                'message': 'Optimize API response time with caching',
                'errors': []
            }
            await self.run_scenario('Performance Optimization', event)
        
        # Register with WebSocket bridge
        self.ws_bridge.register_demo_trigger('security', trigger_security)
        self.ws_bridge.register_demo_trigger('mvp', trigger_mvp)
        self.ws_bridge.register_demo_trigger('performance', trigger_performance)
    
    async def run_scenario(self, scenario_name: str, event_data: dict):
        """
        Run a complete integrated scenario
        
        This is the INTEGRATION CORE - shows how everything connects
        """
        
        print(f"\n🎭 SCENARIO: {scenario_name}")
        print("-" * 70)
        
        # STEP 1: ANALYZE CONTEXT (Aria's code)
        print("\n🔍 Analyzing context...")
        context = await self.analyzer.analyze_event(event_data)
        summary = self.analyzer.get_context_summary(context)
        print(f"   📊 {summary}")
        
        # STEP 2: GENERATE AGENTS (Aria's code)
        print("\n🤖 Generating specialized agents...")
        agents, llm_data = await self.generator.generate_agents(context)
        print(f"   ✨ Generated {len(agents)} agents")
        
        # STEP 3: BROADCAST TO FRONTEND (Integration point)
        for agent in agents:
            # Send to WebSocket → Dashboard
            await self.ws_bridge.broadcast_agent_generated({
                'id': agent.agent_id,
                'type': agent.agent_type,
                'name': agent.agent_type.replace('_', ' ').title(),
                'description': agent.context_reason,
                'capabilities': agent.tags,
                'generated_at': asyncio.get_event_loop().time()
            })
            
            # Stream to Redpanda
            await self.redpanda.stream_agent_message(
                agent_id=agent.agent_id,
                message=f"Agent {agent.agent_type} generated",
                message_type="agent_generation",
                metadata={'context_reason': agent.context_reason}
            )
            
            print(f"      • {agent.agent_type} ({agent.confidence:.0%})")
        
        # STEP 4: CREATE STACKAI WORKFLOW (Shrey's code)
        print("\n🔄 Creating StackAI workflow...")
        stackai_agents = [
            {
                'id': agent.agent_id,
                'type': agent.agent_type,
                'name': agent.agent_type
            }
            for agent in agents
        ]
        
        workflow_id = await self.stackai.create_agent_workflow(stackai_agents)
        print(f"   📋 Workflow created: {workflow_id}")
        
        # STEP 5: EXECUTE WORKFLOW
        print("\n▶️  Executing workflow...")
        execution_id = await self.stackai.execute_workflow(
            workflow_id,
            {
                'code_changes': event_data['files'],
                'focus_area': 'security' if context['security_focus'] else 'general'
            }
        )
        print(f"   🎯 Execution ID: {execution_id}")
        
        # Broadcast workflow execution
        await self.ws_bridge.broadcast_workflow_executed({
            'workflow_id': workflow_id,
            'execution_id': execution_id,
            'agent_count': len(agents)
        })
        
        self.demo_stats['workflows_executed'] += 1
        
        # STEP 6: UPDATE DOCUMENTATION (Aria's code)
        print("\n📚 Updating documentation...")
        for agent in agents:
            updates, content_data = await self.updater.update_documentation(agent, context)
            
            for update in updates:
                # Broadcast to frontend
                await self.ws_bridge.broadcast_documentation_updated({
                    'action': update['type'].title(),
                    'file': update['file'],
                    'content': f"Updated by {agent.agent_type}",
                    'type': agent.focus_area,
                    'size': update['size']
                })
                
                # Stream to Redpanda
                await self.redpanda.stream_documentation_update({
                    'file': update['file'],
                    'agent': agent.agent_type,
                    'action': update['type']
                })
            
            print(f"      ✏️  {agent.agent_type}: {len(updates)} files")
            self.demo_stats['files_updated'] += len(updates)
            
            # Capture in Sentry
            capture_agent_event(
                agent_type=agent.agent_type,
                event_data=event_data,
                success=True
            )
        
        # STEP 7: LEARN FROM EVENT (Aria's code)
        print("\n🧠 Learning from interaction...")
        await self.learner.learn_from_event(event_data, agents, 'success', [])
        summary = self.learner.get_learning_summary()
        
        # Broadcast learning event
        await self.ws_bridge.broadcast_learning_event({
            'event_type': 'pattern_recognized',
            'pattern': scenario_name,
            'success_rate': summary['success_rate'],
            'patterns_learned': summary['patterns_learned']
        })
        
        # Stream to Redpanda
        await self.redpanda.stream_learning_event({
            'event_type': 'scenario_complete',
            'scenario': scenario_name,
            'agents_spawned': len(agents)
        })
        
        print(f"   📊 Success rate: {summary['success_rate']}")
        print(f"   🔬 Patterns learned: {summary['patterns_learned']}")
        
        # Update stats
        self.demo_stats['events_processed'] += 1
        self.demo_stats['agents_spawned'] += len(agents)
        
        print(f"\n✅ Scenario complete!")
    
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
            await asyncio.sleep(2)
        
        # Final summary
        await self._show_final_summary()
    
    async def _show_final_summary(self):
        """Show final demo summary"""
        print("\n" + "=" * 70)
        print("🎊 INTEGRATED DEMO COMPLETE")
        print("=" * 70)
        
        print(f"\n📊 System Statistics:")
        print(f"   Events processed: {self.demo_stats['events_processed']}")
        print(f"   Agents spawned: {self.demo_stats['agents_spawned']}")
        print(f"   Files updated: {self.demo_stats['files_updated']}")
        print(f"   Workflows executed: {self.demo_stats['workflows_executed']}")
        
        print(f"\n🌐 Integration Status:")
        ws_stats = self.ws_bridge.get_stats()
        print(f"   WebSocket clients: {ws_stats['connected_clients']}")
        print(f"   Redpanda status: {self.redpanda.is_running}")
        print(f"   StackAI workflows: {len(self.stackai.list_workflows())}")
        
        redpanda_health = await self.redpanda.health_check()
        print(f"   Redpanda topics: {', '.join(redpanda_health['topics'])}")
        
        print(f"\n💡 Integration Points Working:")
        print(f"   ✅ Backend → WebSocket → Frontend")
        print(f"   ✅ StackAI workflow orchestration")
        print(f"   ✅ Redpanda event streaming")
        print(f"   ✅ Real-time dashboard updates")
        print(f"   ✅ Sentry error tracking")
        
        print(f"\n🎯 This demonstrates:")
        print(f"   • Aria's agent intelligence")
        print(f"   • Shrey's infrastructure")
        print(f"   • Seamless integration")
        print(f"   • Full sponsor utilization")
    
    async def run_forever(self):
        """Keep server running for interactive demo"""
        print("\n⏸️  Demo server running...")
        print("   Open dashboard.html and click demo buttons")
        print("   Press Ctrl+C to stop\n")
        
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup all systems"""
        await self.ws_bridge.stop()
        await self.redpanda.stop()
        print("✅ All systems stopped")


async def main():
    """Main entry point"""
    import sys
    
    demo = IntegratedDialecticDemo()
    await demo.setup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "sequence":
        # Run predefined sequence
        await demo.run_full_demo()
    else:
        # Run forever and wait for frontend triggers
        await demo.run_forever()


if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(main())

