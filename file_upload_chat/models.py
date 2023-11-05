from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_size(value):
    # 5 MB limit
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size must be no more than 5 MB.')
    
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    pdfName = models.CharField(max_length=120)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf']), validate_file_size]
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    userId = models.CharField(max_length=200)

    def __str__(self):
        return self.pdfName
    
class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    chatId = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=[('system', 'System'), ('user', 'User')])