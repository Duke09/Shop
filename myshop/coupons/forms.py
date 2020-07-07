from django import forms

class CouponApllyForm(forms.Form):
    code = forms.CharField()