from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Auction(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_who_make_the_auction')
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    img_url = models.CharField(max_length=200)
    comments = models.ManyToManyField('Comment', related_name='comments_in_the_auction')
    bids = models.ManyToManyField('Bid', related_name='bids_in_the_auction')

    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_who_make_the_bid')
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name='auction_for_the_bid')
    bid = models.IntegerField()
    dateBid = datetime.datetime.now()

    def __str__(self):
        return '%s %s' % (self.user , self.bid)

class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_who_make_the_comment')
    comment = models.TextField()
    dateComment = datetime.datetime.now()

    def __str__(self):
        return '%s %s' % (self.user, self.dateComment)
