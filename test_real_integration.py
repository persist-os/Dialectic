#!/usr/bin/env python3
"""
Real Integration Test for Dialectic
Tests integration with actual StackAI API and Redpanda Connect
"""
import asyncio
import sys
import os
import logging
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streams.redpanda_client import RedpandaClient
from streams.message_handler import MessageHandler, MessageType
from orchestration.stackai_client import StackAIClient
from orchestration.workflow_manager import WorkflowManager, AgentContext

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_real_stackai_integration():
    """Test real StackAI API integration"""
    logger.info("🤖 Testing real StackAI API integration...")
    
    try:
        # Initialize StackAI client with real API
        stackai_client = StackAIClient()
        
        # Test direct API call
        test_payload = {
            "user_id": "dialectic_test_user",
            "in-0": "What are you capable of? Analyze this code change: ['auth.py', 'security.py'] with focus on security."
        }
        
        logger.info("📡 Making direct StackAI API call...")
        response = await stackai_client._call_stackai_api(test_payload)
        logger.info(f"✅ StackAI API Response: {response}")
        
        # Test workflow creation and execution
        test_agents = [
            {"id": "test_security", "type": "security_specialist", "name": "Security Expert"},
            {"id": "test_doc", "type": "documentation_agent", "name": "Documentation Agent"}
        ]
        
        logger.info("🔧 Creating workflow with real StackAI...")
        workflow_id = await stackai_client.create_agent_workflow(test_agents, "real_test_workflow")
        logger.info(f"✅ Workflow created: {workflow_id}")
        
        # Execute workflow with real API
        logger.info("⚙️ Executing workflow with real StackAI API...")
        execution_id = await stackai_client.execute_workflow(workflow_id, {
            "code_changes": ["auth.py", "security.py", "middleware.py"],
            "focus_area": "security",
            "file_context": {"auth.py": "authentication logic"}
        })
        logger.info(f"✅ Workflow executed: {execution_id}")
        
        # Check execution status
        await asyncio.sleep(2)  # Wait for execution
        status = await stackai_client.get_execution_status(execution_id)
        logger.info(f"✅ Execution status: {status}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ StackAI integration test failed: {e}")
        return False

async def test_real_redpanda_integration():
    """Test real Redpanda Connect integration"""
    logger.info("📡 Testing real Redpanda Connect integration...")
    
    try:
        # Initialize Redpanda client
        redpanda_client = RedpandaClient()
        
        # Setup streams
        logger.info("🔧 Setting up Redpanda streams...")
        success = await redpanda_client.setup_streams()
        if not success:
            logger.warning("⚠️ Redpanda setup failed, continuing with mock mode")
        
        # Test message streaming
        logger.info("📨 Testing agent message streaming...")
        await redpanda_client.stream_agent_message(
            agent_id="test_security_agent",
            message="Testing real Redpanda integration",
            message_type="test"
        )
        
        # Test documentation update streaming
        logger.info("📝 Testing documentation update streaming...")
        await redpanda_client.stream_documentation_update({
            "file": "security_patterns.md",
            "action": "created",
            "content": "Security patterns for authentication",
            "agent_id": "test_security_agent"
        })
        
        # Test learning event streaming
        logger.info("🧠 Testing learning event streaming...")
        await redpanda_client.stream_learning_event({
            "event_type": "pattern_recognized",
            "pattern": "security_focus",
            "confidence": 0.92,
            "context": {"files_changed": ["auth.py", "security.py"]}
        })
        
        # Health check
        health = await redpanda_client.health_check()
        logger.info(f"✅ Redpanda health check: {health}")
        
        # Cleanup
        await redpanda_client.stop()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Redpanda integration test failed: {e}")
        return False

async def test_end_to_end_integration():
    """Test complete end-to-end integration"""
    logger.info("🌌 Testing end-to-end integration...")
    
    try:
        # Initialize all components
        redpanda_client = RedpandaClient()
        message_handler = MessageHandler()
        stackai_client = StackAIClient()
        workflow_manager = WorkflowManager(stackai_client, message_handler)
        
        # Setup Redpanda
        await redpanda_client.setup_streams()
        
        # Create test context
        context = AgentContext(
            code_changes=["auth.py", "security.py", "middleware.py"],
            file_context={
                "auth.py": "authentication and authorization logic",
                "security.py": "security utilities and helpers",
                "middleware.py": "request processing middleware"
            },
            focus_area="security",
            urgency="high",
            metadata={"test_run": True, "real_integration": True}
        )
        
        # Coordinate agents (this will use real StackAI API)
        logger.info("🤖 Coordinating agents with real StackAI...")
        result = await workflow_manager.coordinate_agents(context)
        
        if result.success:
            logger.info(f"✅ Agent coordination successful!")
            logger.info(f"   - Workflow ID: {result.workflow_id}")
            logger.info(f"   - Execution ID: {result.execution_id}")
            logger.info(f"   - Agents generated: {len(result.agents_generated)}")
            logger.info(f"   - Documentation updates: {len(result.documentation_updates)}")
            logger.info(f"   - Learning events: {len(result.learning_events)}")
            
            # Stream results through Redpanda
            logger.info("📡 Streaming results through Redpanda...")
            for agent in result.agents_generated:
                await redpanda_client.stream_agent_message(
                    agent_id=agent["id"],
                    message=f"Agent {agent['name']} generated for {context.focus_area} focus",
                    message_type="agent_generated",
                    metadata={"agent": agent, "context": context.__dict__}
                )
            
            for update in result.documentation_updates:
                await redpanda_client.stream_documentation_update(update)
            
            for event in result.learning_events:
                await redpanda_client.stream_learning_event(event)
            
            logger.info("✅ End-to-end integration successful!")
            return True
        else:
            logger.error(f"❌ Agent coordination failed: {result.error_message}")
            return False
        
    except Exception as e:
        logger.error(f"❌ End-to-end integration test failed: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            await redpanda_client.stop()
        except:
            pass

async def main():
    """Main test function"""
    print("=" * 70)
    print("🌌 DIALECTIC - REAL INTEGRATION TEST")
    print("   Testing with actual StackAI API and Redpanda Connect")
    print("=" * 70)
    
    results = {}
    
    # Test 1: StackAI API
    print("\n🤖 Testing StackAI API Integration...")
    results["stackai"] = await test_real_stackai_integration()
    
    # Test 2: Redpanda Connect
    print("\n📡 Testing Redpanda Connect Integration...")
    results["redpanda"] = await test_real_redpanda_integration()
    
    # Test 3: End-to-end
    print("\n🌌 Testing End-to-End Integration...")
    results["end_to_end"] = await test_end_to_end_integration()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 INTEGRATION TEST RESULTS")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name.upper()}: {status}")
    
    if all_passed:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("🚀 Dialectic is ready for Phase 1 checkpoint!")
        print("\nNext steps:")
        print("1. Open frontend/dashboard.html in browser")
        print("2. Test demo scenarios with real StackAI integration")
        print("3. Verify Redpanda streaming is working")
        print("4. Prepare for demo presentation")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("🔧 Check logs above for specific issues")
        print("💡 Consider using fallback modes for demo")
    
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
