"""
Pydantic Models for Dialectic
Type definitions only - no business logic
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AgentSpec(BaseModel):
    """Specification for a dynamically generated agent"""
    
    agent_id: str = Field(description="Unique identifier for this agent instance")
    agent_type: str = Field(description="Type/role of the agent (e.g., 'security_specialist')")
    focus_area: str = Field(description="Primary focus area (e.g., 'security', 'performance')")
    
    documentation_targets: List[str] = Field(
        description="List of documentation files this agent should update"
    )
    priority: int = Field(
        description="Priority level (1=highest, 3=lowest)",
        ge=1,
        le=3
    )
    confidence: float = Field(
        description="Confidence score that this agent is needed (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    created_at: str = Field(description="ISO timestamp when agent was created")
    context_reason: str = Field(description="Human-readable reason why this agent was spawned")
    estimated_duration: str = Field(description="Estimated time to complete (e.g., '15-30 min')")
    
    tags: List[str] = Field(description="Searchable tags for this agent type")
    dependencies: List[str] = Field(
        default_factory=list,
        description="Other agent types this agent depends on"
    )


class ContextAnalysis(BaseModel):
    """Analysis of a code change event"""
    
    security_focus: bool = Field(description="Whether this event involves security concerns")
    mvp_focus: bool = Field(description="Whether this is MVP/prototype work")
    performance_focus: bool = Field(description="Whether this involves performance optimization")
    documentation_focus: bool = Field(description="Whether documentation files were changed")
    error_focus: bool = Field(description="Whether errors are present")
    
    files_changed: List[str] = Field(description="List of files that were modified")
    commit_message: str = Field(description="Commit or event message")
    error_count: int = Field(description="Number of errors detected")
    
    file_types: dict = Field(description="Breakdown of file types changed")
    complexity_score: int = Field(description="Estimated complexity of the change")
    
    confidence: dict = Field(description="Confidence scores for each focus area")


class DocumentationUpdate(BaseModel):
    """Record of a documentation update"""
    
    file: str = Field(description="Path to file that was updated")
    type: str = Field(description="'created' or 'updated'")
    timestamp: str = Field(description="When the update occurred")
    agent: str = Field(description="Agent type that made the update")
    size: int = Field(description="Size of content added in bytes")


class LearningPattern(BaseModel):
    """A learned pattern from events"""
    
    pattern_key: str = Field(description="Unique key identifying this pattern")
    occurrence_count: int = Field(description="Number of times this pattern was seen")
    agents_spawned: List[str] = Field(description="Agent types typically spawned for this pattern")
    success_rate: float = Field(description="Success rate for this pattern (0.0-1.0)")
    last_seen: str = Field(description="ISO timestamp when last seen")

