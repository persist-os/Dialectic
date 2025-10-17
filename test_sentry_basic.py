"""
Simple Sentry Integration Test
Tests both SDK (sending) and MCP (reading) without complex imports
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import sentry_sdk
    SENTRY_AVAILABLE = True
except ImportError:
    print("⚠️  sentry-sdk not installed. Run: pip install sentry-sdk")
    SENTRY_AVAILABLE = False

# Import our modules
try:
    from config.sentry_config import initialize_sentry, SENTRY_ORG_SLUG, SENTRY_PROJECT_SLUG
    from connectors.sentry_connector import SentryMCPConnector, SentryEventSimulator
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Import error: {e}")
    MODULES_AVAILABLE = False


async def test_sentry_basic():
    """Basic Sentry test without complex dependencies"""
    
    print("🌌 DIALECTIC - Basic Sentry Test")
    print("=" * 50)
    
    if not SENTRY_AVAILABLE:
        print("\n❌ Sentry SDK not available")
        print("   Run: pip install sentry-sdk")
        return
    
    if not MODULES_AVAILABLE:
        print("\n❌ Custom modules not available")
        print("   Check file paths and imports")
        return
    
    # Test 1: Initialize Sentry
    print("\n1️⃣ Testing Sentry SDK initialization...")
    try:
        initialize_sentry(environment="test")
        print("   ✅ Sentry SDK initialized")
    except Exception as e:
        print(f"   ❌ Sentry SDK failed: {e}")
        return
    
    # Test 2: Send test error
    print("\n2️⃣ Testing error capture...")
    try:
        # Intentional error
        test_value = 1 / 0
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)
        print("   ✅ Test error sent to Sentry")
    
    # Test 3: Test MCP connector
    print("\n3️⃣ Testing MCP connector...")
    try:
        connector = SentryMCPConnector(
            organization_slug=SENTRY_ORG_SLUG,
            project_slug=SENTRY_PROJECT_SLUG
        )
        
        connected = await connector.connect()
        
        if connected:
            print("   ✅ MCP connector initialized")
        else:
            print("   ⚠️  MCP connector needs configuration")
    except Exception as e:
        print(f"   ❌ MCP connector failed: {e}")
    
    # Test 4: Test event simulator
    print("\n4️⃣ Testing event simulator...")
    try:
        simulator = SentryEventSimulator()
        event = simulator.generate_mock_event("security")
        print(f"   ✅ Event simulator working")
        print(f"      Sample event: {event['message']}")
    except Exception as e:
        print(f"   ❌ Event simulator failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ BASIC SENTRY TEST COMPLETE")
    print("=" * 50)
    
    print(f"\n📊 Organization: {SENTRY_ORG_SLUG}")
    print(f"📊 Project: {SENTRY_PROJECT_SLUG}")
    print(f"📊 Dashboard: https://sentry.io/organizations/{SENTRY_ORG_SLUG}/issues/")
    
    print("\n🎯 Next Steps:")
    print("   1. Check Sentry dashboard for the test error")
    print("   2. Restart Cursor to authenticate Sentry MCP")
    print("   3. Build Context Analyzer")


if __name__ == "__main__":
    asyncio.run(test_sentry_basic())

