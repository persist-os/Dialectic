"""
Quick test script for Sentry MCP connection
Run this to verify everything is set up correctly
"""

import asyncio
from connectors.sentry_connector import SentryMCPConnector, SentryEventSimulator


async def test_sentry_setup():
    """Test Sentry connector setup"""
    
    print("🌌 DIALECTIC - Sentry Integration Test")
    print("=" * 60)
    
    # Step 1: Test connector initialization
    print("\n1️⃣ Testing Sentry Connector Initialization...")
    
    # TODO: Replace with your actual Sentry organization slug
    # You can find this in Sentry → Settings → Organization Settings
    ORGANIZATION_SLUG = "persistos"  # ⚠️ REPLACE THIS
    PROJECT_SLUG = "dialectic"
    
    connector = SentryMCPConnector(
        organization_slug=ORGANIZATION_SLUG,
        project_slug=PROJECT_SLUG
    )
    
    connected = await connector.connect()
    
    if connected:
        print("   ✅ Connector initialized successfully")
    else:
        print("   ⚠️  Connector initialized but needs configuration")
        print("   📝 Update ORGANIZATION_SLUG in this file")
    
    # Step 2: Test event simulator
    print("\n2️⃣ Testing Event Simulator (for demo purposes)...")
    simulator = SentryEventSimulator()
    
    event_types = ["security", "performance", "error", "mvp"]
    
    for event_type in event_types:
        event = simulator.generate_mock_event(event_type)
        print(f"\n   🎭 {event_type.upper()} Event:")
        print(f"      Message: {event['message']}")
        print(f"      Files: {', '.join(event['files'][:2])}")
        print(f"      Level: {event['level']}")
    
    # Step 3: Instructions for next steps
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("=" * 60)
    print("\n1. Get your Sentry organization slug:")
    print("   → Go to Sentry → Settings → Organization Settings")
    print("   → Copy the 'Organization Slug' value")
    print("   → Update ORGANIZATION_SLUG in this test file")
    
    print("\n2. Create a Sentry project called 'dialectic':")
    print("   → In Sentry dashboard, click 'Projects'")
    print("   → Click 'Create Project'")
    print("   → Select 'Python' platform")
    print("   → Name it 'dialectic'")
    
    print("\n3. Authenticate Sentry MCP in Cursor:")
    print("   → Restart Cursor to load the new MCP config")
    print("   → You should be prompted to authenticate with Sentry")
    print("   → Grant access to your organization")
    
    print("\n4. Test with real Sentry data:")
    print("   → Once authenticated, we can fetch real issues")
    print("   → For now, we'll use the simulator for demos")
    
    print("\n✅ Sentry connector is ready for Phase 1!")
    print("   Next: Build the Context Analyzer (agents/context_analyzer.py)")
    

if __name__ == "__main__":
    asyncio.run(test_sentry_setup())

