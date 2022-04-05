from django import forms

class search_form(forms.Form):
    search = forms.CharField(label="Search",required=False,widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

class add_form(forms.Form):
    title = forms.CharField(label="Title",required=True,widget=forms.TextInput(attrs={'placeholder':'Enter Title'}))
    body = forms.CharField(label="Markdown content",required=False,widget=forms.Textarea(attrs={'placeholder':'Enter markdown content'}))

class edit_form(forms.Form):
    title = forms.CharField(label="Title",required=False, disabled=False,widget=forms.HiddenInput())
    body = forms.CharField(label="Markdown content",widget=forms.Textarea())