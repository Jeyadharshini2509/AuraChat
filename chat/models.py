from django.contrib.auth.models import User
from django.db import models


class ChatThread(models.Model):
    """One conversation. A user can have many of these (the sidebar list)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=255, default="New chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class Message(models.Model):
    """One message inside a thread - either from the user or the assistant."""

    ROLE_CHOICES = [
        ("user", "user"),
        ("assistant", "assistant"),
    ]

    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:40]}"
