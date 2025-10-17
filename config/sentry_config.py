"""
Sentry Configuration
Initializes Sentry SDK for error tracking and monitoring
"""

import sentry_sdk
import os


# Sentry DSN from your project
SENTRY_DSN = "https://0d779500cadc770af5c1e9eec71138ef@o4510206067605504.ingest.us.sentry.io/4510206088249344"

# Your Sentry organization and project
SENTRY_ORG_SLUG = "persistos"  # Update if different
SENTRY_PROJECT_SLUG = "dialectic"  # Update to "dialectic" once you create that project


def initialize_sentry(
    dsn: str = SENTRY_DSN,
    environment: str = "development",
    enable_tracing: bool = True
):
    """
    Initialize Sentry SDK for error monitoring
    
    Args:
        dsn: Sentry DSN for the project
        environment: Environment name (development, production, demo)
        enable_tracing: Enable performance tracing
    """
    
    sentry_sdk.init(
        dsn=dsn,
        
        # Add request headers and user IP data
        send_default_pii=True,
        
        # Set environment
        environment=environment,
        
        # Enable performance tracing
        traces_sample_rate=1.0 if enable_tracing else 0.0,
        
        # Enable profiling
        profiles_sample_rate=1.0,
        
        # Release tracking
        release=f"dialectic@1.0.0-hackathon",
        
        # Additional context
        attach_stacktrace=True,
        
        # Custom tags
        default_integrations=True,
    )
    
    # Set custom tags for Dialectic
    sentry_sdk.set_tag("project", "dialectic")
    sentry_sdk.set_tag("sponsor", "sentry")
    sentry_sdk.set_tag("hackathon", "true")
    
    print(f"✅ Sentry SDK initialized (env: {environment})")


def capture_agent_event(agent_type: str, event_data: dict, success: bool = True):
    """
    Capture custom event for agent generation
    
    Args:
        agent_type: Type of agent generated
        event_data: Event data that triggered agent
        success: Whether agent generation was successful
    """
    
    with sentry_sdk.push_scope() as scope:
        # Add custom context
        scope.set_context("agent", {
            "type": agent_type,
            "files": event_data.get("files", []),
            "message": event_data.get("message", ""),
            "success": success
        })
        
        scope.set_tag("agent_type", agent_type)
        scope.set_tag("success", str(success))
        
        # Send as breadcrumb or message
        sentry_sdk.add_breadcrumb(
            category="agent.generated",
            message=f"Generated {agent_type} agent",
            level="info"
        )


def capture_documentation_update(files_updated: list, agent_type: str):
    """
    Capture documentation update event
    
    Args:
        files_updated: List of files that were updated
        agent_type: Type of agent that made the update
    """
    
    with sentry_sdk.push_scope() as scope:
        scope.set_context("documentation", {
            "files_updated": files_updated,
            "agent_type": agent_type,
            "count": len(files_updated)
        })
        
        sentry_sdk.add_breadcrumb(
            category="documentation.updated",
            message=f"{agent_type} updated {len(files_updated)} files",
            level="info"
        )


def capture_learning_event(pattern_key: str, success_rate: float):
    """
    Capture learning system event
    
    Args:
        pattern_key: Pattern that was learned
        success_rate: Current success rate
    """
    
    with sentry_sdk.push_scope() as scope:
        scope.set_context("learning", {
            "pattern": pattern_key,
            "success_rate": success_rate
        })
        
        sentry_sdk.add_breadcrumb(
            category="learning.pattern",
            message=f"Learned pattern: {pattern_key}",
            level="info"
        )


if __name__ == "__main__":
    # Test Sentry integration
    print("🧪 Testing Sentry SDK Integration\n")
    
    initialize_sentry(environment="test")
    
    print("📤 Sending test error to Sentry...")
    
    try:
        # Intentional error for testing
        division_by_zero = 1 / 0
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print("✅ Test error sent to Sentry!")
        print("   Check your Sentry dashboard: https://sentry.io/issues/")
    
    # Test custom events
    print("\n📤 Sending custom agent event...")
    capture_agent_event(
        agent_type="security_specialist",
        event_data={
            "files": ["auth.py"],
            "message": "Test security event"
        },
        success=True
    )
    print("✅ Custom event sent!")
    
    print("\n🎉 Sentry integration test complete!")
    print("   Go to: https://sentry.io/organizations/ariahan/issues/")

