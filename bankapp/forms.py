from django import forms
from .models import accounts


# Add Account Form
class addaccountsform(forms.ModelForm):

    class Meta:
        model = accounts

        fields = [
            'acc_number',
            'name',
            'password',
            'amount',
            'address',
            'mobile_no'
        ]

        widgets = {
            'acc_number': forms.TextInput(
                attrs={'placeholder': 'Enter Account Number'}
            ),
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter Customer Name'}
            ),
            'password': forms.PasswordInput(
                render_value=False
            ),
            'amount': forms.NumberInput(
                attrs={'min': '0', 'step': '0.01'}
            ),
            'address': forms.TextInput(
                attrs={'placeholder': 'Enter Address'}
            ),
            'mobile_no': forms.TextInput(
                attrs={'placeholder': 'Enter Mobile Number'}
            ),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if amount < 0:
            raise forms.ValidationError(
                "Initial balance cannot be negative."
            )

        return amount


# Balance Form
class balanceform(forms.Form):

    acc_number = forms.CharField(
        max_length=40,
        label="Account Number"
    )

    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label="Password"
    )


# Withdrawal Form
class withdrawform(forms.Form):

    acc_number = forms.CharField(
        max_length=40,
        label="Account Number"
    )

    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label="Password"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        label="Withdrawal Amount"
    )


# Deposit Form
class depositeform(forms.Form):

    acc_number = forms.CharField(
        max_length=40,
        label="Account Number"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        label="Deposit Amount"
    )


# Transfer Form
class transferform(forms.Form):

    from_acc_number = forms.CharField(
        max_length=40,
        label="Sender Account Number"
    )

    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label="Sender Password"
    )

    to_acc_number = forms.CharField(
        max_length=40,
        label="Receiver Account Number"
    )

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        label="Transfer Amount"
    )

    def clean(self):
        cleaned_data = super().clean()

        from_acc = cleaned_data.get('from_acc_number')
        to_acc = cleaned_data.get('to_acc_number')

        if from_acc and to_acc and from_acc == to_acc:
            raise forms.ValidationError(
                "Sender and receiver accounts must be different."
            )

        return cleaned_data


# Close Account Form
class closeform(forms.Form):

    acc_number = forms.CharField(
        max_length=40,
        label="Account Number"
    )

    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(),
        label="Account Password"
    )