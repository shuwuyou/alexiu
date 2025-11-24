"""Utility class for constructing conversation messages."""

from typing import List, Dict, Optional, Literal

# OpenAI message roles
Role = Literal["system", "user", "assistant", "tool"]


class MessageBuilder:
    """Utility class for constructing conversation messages using OpenAI's role format."""
    
    def __init__(self):
        """Initialize an empty message builder."""
        self.messages: List[Dict[str, str]] = []
    
    def add_system_message(self, content: str) -> 'MessageBuilder':
        """Add a system message to the conversation.
        
        Args:
            content: System message content
            
        Returns:
            self for method chaining
        """
        self.messages.append({"role": "system", "content": content})
        return self
    
    def add_user_message(self, content: str) -> 'MessageBuilder':
        """Add a user message to the conversation.
        
        Args:
            content: User message content
            
        Returns:
            self for method chaining
        """
        self.messages.append({"role": "user", "content": content})
        return self
    
    def add_assistant_message(self, content: str) -> 'MessageBuilder':
        """Add an assistant message to the conversation.
        
        Args:
            content: Assistant message content
            
        Returns:
            self for method chaining
        """
        self.messages.append({"role": "assistant", "content": content})
        return self
    
    def add_message(self, role: Role, content: str) -> 'MessageBuilder':
        """Add a message with specified role.
        
        Args:
            role: Message role - must be one of OpenAI's roles: "system", "user", "assistant", "tool"
            content: Message content
            
        Returns:
            self for method chaining
            
        Raises:
            ValueError: If role is not a valid OpenAI role
        """
        valid_roles = {"system", "user", "assistant", "tool"}
        if role not in valid_roles:
            raise ValueError(f"Invalid role '{role}'. Must be one of: {valid_roles}")
        self.messages.append({"role": role, "content": content})
        return self
    
    def build(self) -> List[Dict[str, str]]:
        """Build and return the message list.
        
        Returns:
            List of message dictionaries ready for OpenAI API
        """
        return self.messages.copy()
    
    def clear(self) -> 'MessageBuilder':
        """Clear all messages.
        
        Returns:
            self for method chaining
        """
        self.messages = []
        return self
    
    def __len__(self) -> int:
        """Return the number of messages."""
        return len(self.messages)
    
    def __repr__(self) -> str:
        return f"MessageBuilder(messages={len(self.messages)})"

