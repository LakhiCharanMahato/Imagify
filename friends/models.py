from django.contrib import admin

# Register your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class FriendList(models.Model):
    # user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    # related_name="user")
    # friends=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
    # related_name="friends")
    user1=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    related_name='user')
    user2=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    related_name='friend')
    is_active=models.BooleanField(blank=True,null=False,default=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user1.username

    def send_friend_request(user1,user2):
        entry1=FriendList(user1=user1,user2=user2)
        entry1.save()
    
    def accept_friend_request(user1,user2):
        entry1=FriendList.objects.filter(user1=user1).filter(user2=user2)[0]
        entry1.is_active=False
        entry1.save()
        entry2=FriendList(user1=user2,user2=user1,is_active=False)
        entry2.save()

    def delete_friend_request(user1,user2):
        entry1=FriendList.objects.filter(user1=user1).filter(user2=user2)[0]
        entry1.delete()

    def unfriend_someone(user1,user2):
        entry1=FriendList.objects.filter(user1=user1)\
            .filter(user2=user2)\
            .filter(is_active=False)[0]
        entry1.delete()
        entry2=FriendList.objects.filter(user1=user2)\
            .filter(user2=user1)\
            .filter(is_active=False)[0]
        entry2.delete()     

# def add_friend(self,account):
# """
# Add a new friend
# """
# if not account in self.friends.all():
# self.friends.add(account)

# def remove_friend(self,account):
# """
# Remove a friend
# """
# if account in self.friends.all():
# self.friends.remove(account)

# def unfriend(self,removee):
# """
# Initiate the action of unfriending someone.
# """
# remover_friends_list=self #person terminating the friendship

# #Remove friend from remover friend list
# remover_friends_list.remove_friend(removee)

# #Remove friend from removee friend list
# friends_list=FriendList.objects.get(user=removee)
# friends_list.remove_friend(self.user)

# def is_mutual_friend(self,friend):
# """
# Is this a friend?
# """
# if friend in self.friends.all():
# return True
# return False

# def accept(self):
# """
# Accept a friend request
# Update both SENDER and RECEIVER friend lists
# """
# receiver_friend_list=FriendList.objects.get(user=self.receiver)
# if receiver_friend_list:
# receiver_friend_list.add_friend(self.sender)
# sender_friend_list=FriendList.objects.get(user=self.sender)
# if sender_friend_list:
# sender_friend_list.add_friend(self.receiver)
# self.is_active=False
# self.save()

# def decline(self):
# """
# Decline a friend request.
# It is declined by setting the 'is_active' field to False
# """
# self.is_active=False
# self.save()

# def cancel(self):
# """
# Cancel a friend request
# It is "cancelled" by setting the "is_active" field to False. 
# This is only different with respect to "declining" through the notification
# that is generated
# """
# self.is_active=False
# self.save()





# class FriendRequest(models.Model):
# """
# A friend request consists of two main parts:
# 1. SENDER:
# - Person sending/initiating the friend request
# 2. RECEIVER:
# - Person receiving the friend request
# """
# sender=models.ForeignKey(settings.AUTH_USER_MODEL,
# on_delete=models.CASCADE, related_name="sender")
# receiver=models.ForeignKey(settings.AUTH_USER_MODEL,
# on_delete=models.CASCADE, related_name="receiver")
# is_active=models.BooleanField(blank=True,null=False,default=True)
# timestamp=models.DateTimeField(auto_now_add=True)

# def __str__(self):
# return self.sender.username

# def accept(self):
# """
# Accept a friend request
# Update both SENDER and RECEIVER friend lists
# """
# receiver_friend_list=FriendList.objects.get(user=self.receiver)
# if receiver_friend_list:
# receiver_friend_list.add_friend(self.sender)
# sender_friend_list=FriendList.objects.get(user=self.sender)
# if sender_friend_list:
# sender_friend_list.add_friend(self.receiver)
# self.is_active=False
# self.save()

# def decline(self):
# """
# Decline a friend request.
# It is declined by setting the 'is_active' field to False
# """
# self.is_active=False
# self.save()

# def cancel(self):
# """
# Cancel a friend request
# It is "cancelled" by setting the "is_active" field to False. 
# This is only different with respect to "declining" through the notification
# that is generated
# """
# self.is_active=False
# self.save()
