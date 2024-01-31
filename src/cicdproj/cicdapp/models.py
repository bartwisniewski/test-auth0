from django.db import models


class Entry(models.Model):
    """
    This model represents text entry.
    """

    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.updated_at}: {self.text}"

    def __repr__(self) -> str:
        return f"<Entry id={self.id}, updated: {self.updated_at}, {self.text}>"
