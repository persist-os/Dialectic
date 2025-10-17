"""
Sentry MCP Connector
Connects to Sentry's hosted MCP server to get issue and error data

Note: This is SEPARATE from the Sentry SDK (sentry_config.py)
- SDK = Send errors TO Sentry
- MCP = Read issues FROM Sentry
"""

import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SentryIssue:
    """Represents a Sentry issue"""
    id: str
    title: str
    culprit: str
    level: str
    status: str
    count: int
    user_count: int
    first_seen: str
    last_seen: str


class SentryMCPConnector:
    """
    Connects to Sentry's hosted MCP server
    Uses Sentry's MCP tools to get issue data
    """
    
    def __init__(self, organization_slug: str = None, project_slug: str = None):
        """
        Initialize Sentry connector
        
        Args:
            organization_slug: Your Sentry organization slug
            project_slug: Your Sentry project slug (e.g., 'dialectic')
        """
        self.organization_slug = organization_slug
        self.project_slug = project_slug
        self.connected = False
    
    async def connect(self) -> bool:
        """
        Verify connection to Sentry MCP server
        Note: Actual MCP connection is handled by Cursor's MCP client
        This method verifies configuration is correct
        """
        if not self.organization_slug:
            print("⚠️  No organization slug provided - will need to set this")
            return False
        
        self.connected = True
        print(f"✅ Sentry MCP connector initialized for org: {self.organization_slug}")
        return True
    
    async def get_recent_issues(self, limit: int = 10, status: str = "unresolved") -> List[SentryIssue]:
        """
        Get recent issues from Sentry
        
        Args:
            limit: Number of issues to return
            status: Filter by status (unresolved, resolved, all)
        
        Returns:
            List of SentryIssue objects
        """
        if not self.connected:
            raise RuntimeError("Not connected. Call connect() first")
        
        print(f"📥 Fetching {limit} {status} issues from Sentry...")
        
        # Note: In production, this would use MCP client to call:
        # await mcp_client.call_tool("list_issues", {
        #     "organization": self.organization_slug,
        #     "project": self.project_slug,
        #     "limit": limit,
        #     "status": status
        # })
        
        # For now, return structure that we'll populate with real data
        return []
    
    async def search_errors_in_file(self, file_path: str) -> List[Dict]:
        """
        Search for errors in a specific file
        
        Args:
            file_path: Path to the file to search for errors
        
        Returns:
            List of errors found in that file
        """
        if not self.connected:
            raise RuntimeError("Not connected. Call connect() first")
        
        print(f"🔍 Searching for errors in: {file_path}")
        
        # Note: In production, this would use MCP client to call:
        # await mcp_client.call_tool("search_errors", {
        #     "file_path": file_path
        # })
        
        return []
    
    async def get_issue_details(self, issue_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific issue
        
        Args:
            issue_id: The Sentry issue ID
        
        Returns:
            Detailed issue information
        """
        if not self.connected:
            raise RuntimeError("Not connected. Call connect() first")
        
        print(f"📋 Getting details for issue: {issue_id}")
        
        # Note: In production, this would use MCP client to call:
        # await mcp_client.call_tool("get_issue_details", {
        #     "issue_id": issue_id
        # })
        
        return None
    
    async def create_project(self, project_name: str, team_slug: str) -> Dict:
        """
        Create a new Sentry project
        
        Args:
            project_name: Name for the new project
            team_slug: Team to create project under
        
        Returns:
            Created project information
        """
        if not self.connected:
            raise RuntimeError("Not connected. Call connect() first")
        
        print(f"🆕 Creating project: {project_name}")
        
        # Note: In production, this would use MCP client to call:
        # await mcp_client.call_tool("create_project", {
        #     "organization": self.organization_slug,
        #     "name": project_name,
        #     "team": team_slug,
        #     "platform": "python"
        # })
        
        return {}
    
    async def invoke_seer(self, issue_id: str) -> Dict:
        """
        Invoke Sentry's Seer AI for automated issue analysis
        
        Args:
            issue_id: The issue to analyze
        
        Returns:
            Seer analysis results
        """
        if not self.connected:
            raise RuntimeError("Not connected. Call connect() first")
        
        print(f"🤖 Invoking Seer for issue: {issue_id}")
        
        # Note: In production, this would use MCP client
        
        return {}


# Simulated event generator for demo purposes
class SentryEventSimulator:
    """
    Simulates Sentry events for demo/testing
    Use this when you need to demo without real Sentry data
    """
    
    @staticmethod
    def generate_mock_event(event_type: str = "security") -> Dict:
        """
        Generate a mock Sentry event for testing
        
        Args:
            event_type: Type of event (security, performance, error)
        
        Returns:
            Mock event data
        """
        
        mock_events = {
            "security": {
                "files": ["src/auth/jwt.py", "src/middleware/auth.py"],
                "message": "Add JWT authentication with secure token handling",
                "errors": [],
                "issue_id": "DIALECTIC-001",
                "level": "warning"
            },
            "performance": {
                "files": ["src/api/optimize.py", "src/cache/redis.py"],
                "message": "Optimize API response time with caching",
                "errors": [],
                "issue_id": "DIALECTIC-002",
                "level": "info"
            },
            "error": {
                "files": ["src/api/handler.py"],
                "message": "Fix TypeError in user handler",
                "errors": [{"type": "TypeError", "count": 5}],
                "issue_id": "DIALECTIC-003",
                "level": "error"
            },
            "mvp": {
                "files": ["src/prototype/feature.py"],
                "message": "Quick MVP prototype for hackathon demo",
                "errors": [],
                "issue_id": "DIALECTIC-004",
                "level": "info"
            }
        }
        
        return mock_events.get(event_type, mock_events["security"])


if __name__ == "__main__":
    # Quick test
    async def test():
        print("🧪 Testing Sentry MCP Connector\n")
        
        # Test with mock organization
        connector = SentryMCPConnector(
            organization_slug="your-org-slug",
            project_slug="dialectic"
        )
        
        await connector.connect()
        
        # Test simulator
        print("\n🎭 Testing Event Simulator:")
        simulator = SentryEventSimulator()
        
        for event_type in ["security", "performance", "error", "mvp"]:
            event = simulator.generate_mock_event(event_type)
            print(f"  {event_type}: {event['message']}")
    
    asyncio.run(test())

