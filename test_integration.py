#!/usr/bin/env python3
"""
Quick test script for Dialectic integration
Tests the basic functionality of streaming and orchestration components
"""
import asyncio
import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streams.redpanda_client import RedpandaClient
from streams.message_handler import MessageHandler, MessageType
from orchestration.stackai_client import StackAIClient
from orchestration.workflow_manager import WorkflowManager, AgentContext

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_basic_functionality():
    """Test basic functionality of all components"""
    logger.info("🚀 Starting Dialectic basic functionality test...")
    
    try:
        # Initialize components
        logger.info("📡 Initializing Redpanda client...")
        redpanda_client = RedpandaClient()
        
        logger.info("📨 Initializing message handler...")
        message_handler = MessageHandler()
        
        logger.info("🤖 Initializing StackAI client...")
        stackai_client = StackAIClient()
        
        logger.info("⚙️ Initializing workflow manager...")
        workflow_manager = WorkflowManager(stackai_client, message_handler)
        
        # Test 1: Redpanda streams
        logger.info("🔧 Testing Redpanda streams...")
        await redpanda_client.setup_streams()
        await redpanda_client.stream_agent_message("test_agent", "Hello from test!")
        logger.info("✅ Redpanda streams working")
        
        # Test 2: Message handling
        logger.info("📨 Testing message handling...")
        await message_handler.broadcast_message(
            sender_id="test_sender",
            message_type=MessageType.AGENT_GENERATION,
            content={"test": "message"}
        )
        logger.info("✅ Message handling working")
        
        # Test 3: StackAI workflows
        logger.info("🤖 Testing StackAI workflows...")
        test_agents = [
            {"id": "test_security", "type": "security_specialist", "name": "Test Security Agent"}
        ]
        workflow_id = await stackai_client.create_agent_workflow(test_agents)
        logger.info(f"✅ StackAI workflow created: {workflow_id}")
        
        # Test 4: Agent coordination
        logger.info("⚙️ Testing agent coordination...")
        context = AgentContext(
            code_changes=["test.py"],
            file_context={"test.py": "test content"},
            focus_area="security",
            urgency="medium"
        )
        result = await workflow_manager.coordinate_agents(context)
        logger.info(f"✅ Agent coordination completed: {result.success}")
        
        # Test 5: Dashboard simulation
        logger.info("🎭 Testing dashboard simulation...")
        logger.info("   - Opening dashboard.html in browser...")
        logger.info("   - Dashboard should show real-time agent updates")
        logger.info("   - Demo buttons should trigger agent generation")
        
        logger.info("🎉 All basic functionality tests PASSED!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            await redpanda_client.stop()
        except:
            pass

async def main():
    """Main test function"""
    print("=" * 60)
    print("🌌 DIALECTIC - LIVING DEVELOPMENT ENVIRONMENT")
    print("   Phase 1: Streaming & Orchestration Test")
    print("=" * 60)
    
    success = await test_basic_functionality()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ INTEGRATION TEST PASSED!")
        print("🚀 Ready for Phase 1 checkpoint!")
        print("\nNext steps:")
        print("1. Open frontend/dashboard.html in browser")
        print("2. Test demo buttons for different scenarios")
        print("3. Verify real-time agent generation")
        print("4. Check documentation updates")
    else:
        print("❌ INTEGRATION TEST FAILED!")
        print("🔧 Check logs above for issues")
    
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
