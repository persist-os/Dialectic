#!/usr/bin/env python3
"""
Dialectic Phase 1 Checkpoint Demo
Demonstrates the completed streaming and orchestration system
"""
import asyncio
import sys
import os
import logging
import webbrowser
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streams.redpanda_client import RedpandaClient
from streams.message_handler import MessageHandler, MessageType
from orchestration.stackai_client import StackAIClient
from orchestration.workflow_manager import WorkflowManager, AgentContext

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DialecticDemo:
    """Main demo class for Phase 1 checkpoint"""
    
    def __init__(self):
        self.redpanda_client = RedpandaClient()
        self.message_handler = MessageHandler()
        self.stackai_client = StackAIClient()
        self.workflow_manager = WorkflowManager(self.stackai_client, self.message_handler)
        self.demo_scenarios = [
            {
                "name": "Security Focus",
                "code_changes": ["auth.py", "security.py", "middleware.py"],
                "focus_area": "security",
                "urgency": "high",
                "description": "Authentication and security vulnerabilities"
            },
            {
                "name": "MVP Focus", 
                "code_changes": ["prototype.py", "features.py", "user_interface.py"],
                "focus_area": "mvp",
                "urgency": "medium",
                "description": "Minimum viable product development"
            },
            {
                "name": "Performance Focus",
                "code_changes": ["optimization.py", "cache.py", "database.py"],
                "focus_area": "performance", 
                "urgency": "medium",
                "description": "Performance optimization and scaling"
            }
        ]
    
    async def setup_demo(self):
        """Setup the demo environment"""
        logger.info("🚀 Setting up Dialectic demo environment...")
        
        # Setup Redpanda streams
        logger.info("📡 Setting up Redpanda Connect streams...")
        await self.redpanda_client.setup_streams()
        
        logger.info("✅ Demo environment ready!")
        return True
    
    async def run_demo_scenario(self, scenario):
        """Run a complete demo scenario"""
        logger.info(f"\n🎭 Running scenario: {scenario['name']}")
        logger.info(f"   Focus: {scenario['focus_area']}")
        logger.info(f"   Files: {', '.join(scenario['code_changes'])}")
        logger.info(f"   Description: {scenario['description']}")
        
        # Create context
        context = AgentContext(
            code_changes=scenario['code_changes'],
            file_context={f: f"{f} content" for f in scenario['code_changes']},
            focus_area=scenario['focus_area'],
            urgency=scenario['urgency'],
            metadata={"demo_scenario": scenario['name']}
        )
        
        # Step 1: Detect code changes (simulated)
        logger.info("🔍 Step 1: Detecting code changes...")
        await asyncio.sleep(0.5)
        logger.info(f"   ✅ Detected changes in: {', '.join(scenario['code_changes'])}")
        
        # Step 2: Generate agents dynamically
        logger.info("🤖 Step 2: Generating agents dynamically...")
        result = await self.workflow_manager.coordinate_agents(context)
        
        if result.success:
            logger.info(f"   ✅ Generated {len(result.agents_generated)} agents:")
            for agent in result.agents_generated:
                logger.info(f"      - {agent['name']} ({agent['type']})")
        else:
            logger.error(f"   ❌ Agent generation failed: {result.error_message}")
            return False
        
        # Step 3: Stream agent communication
        logger.info("📡 Step 3: Streaming agent communication...")
        for agent in result.agents_generated:
            await self.redpanda_client.stream_agent_message(
                agent_id=agent["id"],
                message=f"Analyzing {scenario['focus_area']} focus for {', '.join(scenario['code_changes'])}",
                message_type="agent_analysis",
                metadata={"scenario": scenario['name'], "agent": agent}
            )
            await asyncio.sleep(0.2)
        
        # Step 4: Update documentation
        logger.info("📝 Step 4: Updating documentation...")
        for update in result.documentation_updates:
            await self.redpanda_client.stream_documentation_update(update)
            logger.info(f"   ✅ Updated: {update['file']}")
            await asyncio.sleep(0.2)
        
        # Step 5: Learning events
        logger.info("🧠 Step 5: Recording learning events...")
        for event in result.learning_events:
            await self.redpanda_client.stream_learning_event(event)
            logger.info(f"   ✅ Event: {event['event_type']}")
            await asyncio.sleep(0.2)
        
        logger.info(f"✅ Scenario '{scenario['name']}' completed successfully!")
        return True
    
    async def run_all_scenarios(self):
        """Run all demo scenarios"""
        logger.info("\n" + "="*60)
        logger.info("🌌 DIALECTIC PHASE 1 CHECKPOINT DEMO")
        logger.info("="*60)
        
        success_count = 0
        total_scenarios = len(self.demo_scenarios)
        
        for i, scenario in enumerate(self.demo_scenarios, 1):
            logger.info(f"\n📋 Scenario {i}/{total_scenarios}")
            success = await self.run_demo_scenario(scenario)
            if success:
                success_count += 1
            
            # Brief pause between scenarios
            if i < total_scenarios:
                logger.info("⏸️  Pausing before next scenario...")
                await asyncio.sleep(1)
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("📊 DEMO SUMMARY")
        logger.info("="*60)
        logger.info(f"✅ Successful scenarios: {success_count}/{total_scenarios}")
        logger.info(f"📡 Redpanda Connect: {'✅ Working' if self.redpanda_client.is_running else '❌ Not running'}")
        logger.info(f"🤖 StackAI Integration: {'✅ Connected' if success_count > 0 else '⚠️ Using fallback'}")
        
        if success_count == total_scenarios:
            logger.info("\n🎉 ALL SCENARIOS COMPLETED SUCCESSFULLY!")
            logger.info("🚀 Phase 1 checkpoint achieved!")
        else:
            logger.info(f"\n⚠️ {total_scenarios - success_count} scenarios had issues")
            logger.info("💡 Check logs above for details")
        
        return success_count == total_scenarios
    
    async def cleanup(self):
        """Cleanup demo resources"""
        try:
            await self.redpanda_client.stop()
            logger.info("🧹 Demo cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

async def main():
    """Main demo function"""
    demo = DialecticDemo()
    
    try:
        # Setup
        await demo.setup_demo()
        
        # Run scenarios
        success = await demo.run_all_scenarios()
        
        # Show next steps
        print("\n" + "="*60)
        print("🎯 NEXT STEPS FOR PHASE 1")
        print("="*60)
        print("1. 📱 Open dashboard: frontend/dashboard.html")
        print("2. 🎮 Test demo buttons for interactive scenarios")
        print("3. 📊 Monitor real-time agent generation")
        print("4. 📝 Verify documentation updates")
        print("5. 🧠 Check learning event patterns")
        
        if success:
            print("\n✅ PHASE 1 CHECKPOINT COMPLETED!")
            print("🚀 Ready for Phase 2: Enhancement")
        else:
            print("\n⚠️ Phase 1 needs attention")
            print("🔧 Review logs and fix issues before Phase 2")
        
        print("="*60)
        
        return success
        
    finally:
        await demo.cleanup()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
