from django.db import models
from .customer import Customer  # Import the Customer model if it's in the same directory

class UserActivity(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    input_text = models.TextField()
    search_res = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.timestamp}'
    
    @staticmethod
    def save_text(user, input_text, search_res):
        UserActivity.objects.create(user=user, input_text=input_text,search_res = search_res)

    
    @staticmethod
    def get_text_by_customer(customer_id):
        return UserActivity.objects.filter(user=customer_id).order_by('-timestamp')
