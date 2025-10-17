"""
Dialectic Live Demo
Complete demonstration of the self-learning Cursor community

This orchestrates the entire system to show agents spawning dynamically,
updating documentation, and learning from interactions.
"""

import asyncio
import time
import sys
import os
from datetime import datetime
from typing import Dict, List
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import our components
from config.sentry_config import initialize_sentry, capture_agent_event
from connectors.sentry_connector import SentryMCPConnector, SentryEventSimulator
from agents.context_analyzer import ContextAnalyzer
from agents.agent_generator import DynamicAgentGenerator
from agents.documentation_updater import DocumentationUpdater
from agents.learning_engine import LearningEngine


class DialecticDemo:
    """
    Live demo orchestrator for Dialectic
    
    This demonstrates the complete system:
    1. Event detection (Sentry)
    2. Context analysis
    3. Dynamic agent generation
    4. Documentation updates
    5. Learning from interactions
    """
    
    def __init__(self):
        """Initialize the demo system"""
        self.sentry_connector = None
        self.analyzer = None
        self.generator = None
        self.updater = None
        self.learner = None
        self.system_ready = False
        
        # Demo statistics
        self.demo_stats = {
            'events_processed': 0,
            'agents_spawned': 0,
            'files_updated': 0,
            'patterns_learned': 0
        }
    
    async def setup(self):
        """Setup all systems for the demo"""
        
        print("🌌 DIALECTIC: The Self-Learning Cursor Community")
        print("=" * 70)
        print("\n⚡ Initializing systems...")
        
        # Initialize Sentry SDK
        initialize_sentry(environment="demo")
        print("   ✅ Sentry SDK initialized")
        
        # Setup MCP connector
        self.sentry_connector = SentryMCPConnector(
            organization_slug="persistos",
            project_slug="dialectic"
        )
        await self.sentry_connector.connect()
        print("   ✅ Sentry MCP connector ready")
        
        # Setup our intelligence layer
        self.analyzer = ContextAnalyzer()
        self.generator = DynamicAgentGenerator()
        self.updater = DocumentationUpdater('.cursor/')
        self.learner = LearningEngine()
        
        print("   ✅ Context analyzer ready")
        print("   ✅ Agent generator ready")
        print("   ✅ Documentation updater ready")
        print("   ✅ Learning engine ready")
        
        self.system_ready = True
        print("\n🎉 All systems online and ready for demo!")
    
    async def run_scenario(self, scenario_name: str, event_data: Dict):
        """
        Run a complete demo scenario
        
        Args:
            scenario_name: Name of the scenario
            event_data: Event data to process
        """
        
        if not self.system_ready:
            raise RuntimeError("System not ready. Call setup() first.")
        
        print(f"\n🎭 SCENARIO: {scenario_name}")
        print("-" * 70)
        
        print(f"📝 Event: {event_data['message']}")
        print(f"📁 Files: {', '.join(event_data['files'])}")
        
        # Step 1: Analyze context
        print("\n🔍 Step 1: Analyzing context...")
        await asyncio.sleep(0.8)  # Dramatic pause
        
        context = await self.analyzer.analyze_event(event_data)
        summary = self.analyzer.get_context_summary(context)
        print(f"   📊 Analysis: {summary}")
        
        # Step 2: Generate agents dynamically
        print("\n🤖 Step 2: Generating specialized agents...")
        await asyncio.sleep(0.8)
        
        agents = await self.generator.generate_agents(context)
        agent_summary = self.generator.get_agent_summary(agents)
        print(f"   ✨ Agents: {agent_summary}")
        
        for agent in agents:
            await asyncio.sleep(0.4)
            print(f"      • {agent.agent_type}: {agent.context_reason}")
        
        # Step 3: Update documentation
        print("\n📚 Step 3: Updating documentation...")
        total_updates = 0
        
        for agent in agents:
            await asyncio.sleep(0.4)
            updates = await self.updater.update_documentation(agent, context)
            total_updates += len(updates)
            print(f"      ✏️  {agent.agent_type}: {len(updates)} files updated")
            
            # Capture agent event in Sentry
            capture_agent_event(
                agent_type=agent.agent_type,
                event_data=event_data,
                success=True
            )
        
        # Step 4: Learn from interaction
        print("\n🧠 Step 4: Learning from interaction...")
        await asyncio.sleep(0.8)
        
        await self.learner.learn_from_event(event_data, agents, 'success', [])
        learning_summary = self.learner.get_learning_summary()
        
        print(f"   📈 Success rate: {learning_summary['success_rate']}")
        print(f"   🔬 Patterns learned: {learning_summary['patterns_learned']}")
        
        # Update demo stats
        self.demo_stats['events_processed'] += 1
        self.demo_stats['agents_spawned'] += len(agents)
        self.demo_stats['files_updated'] += total_updates
        self.demo_stats['patterns_learned'] = learning_summary['patterns_learned']
        
        print(f"\n✅ Scenario complete: {total_updates} documentation updates")
        
        return {
            'agents_spawned': len(agents),
            'files_updated': total_updates,
            'context_summary': summary
        }
    
    async def run_full_demo(self):
        """Run the complete demo sequence"""
        
        if not self.system_ready:
            await self.setup()
        
        print("\n" + "=" * 70)
        print("🌟 DIALECTIC LIVE DEMONSTRATION")
        print("=" * 70)
        
        # Demo scenarios
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
            },
            {
                'name': 'Error Resolution',
                'event': {
                    'files': ['src/api/handler.py'],
                    'message': 'Fix TypeError in user handler',
                    'errors': [{'type': 'TypeError', 'count': 5}]
                }
            },
            {
                'name': 'Frontend Development',
                'event': {
                    'files': ['src/components/Button.tsx', 'src/styles/button.css'],
                    'message': 'Add new button component with responsive design',
                    'errors': []
                }
            }
        ]
        
        # Run each scenario
        scenario_results = []
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎬 Scenario {i}/{len(scenarios)}")
            result = await self.run_scenario(scenario['name'], scenario['event'])
            scenario_results.append(result)
            
            # Pause between scenarios
            if i < len(scenarios):
                print("\n⏸️  Pausing between scenarios...")
                await asyncio.sleep(2)
        
        # Final summary
        await self._show_final_summary(scenario_results)
    
    async def _show_final_summary(self, scenario_results: List[Dict]):
        """Show final demo summary"""
        
        print("\n" + "=" * 70)
        print("🎊 DIALECTIC DEMONSTRATION COMPLETE")
        print("=" * 70)
        
        # Demo statistics
        print(f"\n📊 Demo Statistics:")
        print(f"   Events processed: {self.demo_stats['events_processed']}")
        print(f"   Agents spawned: {self.demo_stats['agents_spawned']}")
        print(f"   Files updated: {self.demo_stats['files_updated']}")
        print(f"   Patterns learned: {self.demo_stats['patterns_learned']}")
        
        # Learning summary
        learning_summary = self.learner.get_learning_summary()
        print(f"\n🧠 Learning Summary:")
        print(f"   Success rate: {learning_summary['success_rate']}")
        print(f"   Total patterns: {learning_summary['patterns_learned']}")
        
        print(f"\n🏆 Most Effective Agents:")
        for agent in learning_summary['most_effective_agents'][:3]:
            print(f"   • {agent['agent_type']}: {agent['successful_updates']} updates")
        
        # Documentation summary
        doc_summary = self.updater.get_update_summary()
        print(f"\n📚 Documentation Summary:")
        print(f"   Total updates: {doc_summary['total_updates']}")
        print(f"   Files created: {doc_summary['files_created']}")
        print(f"   Files updated: {doc_summary['files_updated']}")
        
        # Key insights
        print(f"\n💡 Key Insights:")
        print(f"   ✅ Agents spawn dynamically based on context")
        print(f"   ✅ No hardcoded agent definitions")
        print(f"   ✅ System learns and improves over time")
        print(f"   ✅ Documentation updates automatically")
        print(f"   ✅ Sentry integration for monitoring")
        
        print(f"\n🎯 What Makes This Special:")
        print(f"   🌟 Living development environment")
        print(f"   🌟 Context-driven agent generation")
        print(f"   🌟 Self-improving documentation system")
        print(f"   🌟 Sponsor-first architecture")
        
        print(f"\n📁 Check .cursor/ folder for generated documentation!")
        print(f"📁 Check .cursor/learning/ for learning data!")
        print(f"📊 Check Sentry dashboard for captured events!")
        
        print(f"\n🚀 Dialectic: Where your development environment comes alive!")


# Quick demo runner
async def run_quick_demo():
    """Run a quick demo with 3 scenarios"""
    
    demo = DialecticDemo()
    
    # Quick scenarios
    quick_scenarios = [
        {
            'name': 'Security Event',
            'event': {
                'files': ['src/auth/jwt.py'],
                'message': 'Add JWT authentication',
                'errors': []
            }
        },
        {
            'name': 'MVP Event',
            'event': {
                'files': ['src/prototype/feature.py'],
                'message': 'Quick MVP prototype',
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
        }
    ]
    
    await demo.setup()
    
    for scenario in quick_scenarios:
        await demo.run_scenario(scenario['name'], scenario['event'])
        await asyncio.sleep(1)
    
    # Show summary
    learning_summary = demo.learner.get_learning_summary()
    print(f"\n✅ Quick demo complete!")
    print(f"   Success rate: {learning_summary['success_rate']}")
    print(f"   Patterns learned: {learning_summary['patterns_learned']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        print("🚀 Running quick demo...")
        asyncio.run(run_quick_demo())
    else:
        print("🎬 Running full demo...")
        demo = DialecticDemo()
        asyncio.run(demo.run_full_demo())
