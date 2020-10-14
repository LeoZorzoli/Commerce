from django import forms
from .models import Category

class AuctionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    starting_bid = forms.IntegerField(label='Initial Bid', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category", widget=forms.Select(attrs={'class': 'form-control'}))

