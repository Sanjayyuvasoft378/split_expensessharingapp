from django import forms
from expenses.models import Group, Expense, Refund
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from betterforms.widgets import DatePickerInput

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'users_can_edit']

class UserModelChoiceField(forms.ModelChoiceField):
    # Normally, we would simply use the proxy model from expenses.models
    # See expenses.models.Group for more details
    def label_from_instance(self, user):
        return user.get_full_name()

class ExpenseForm(forms.ModelForm):
    user = UserModelChoiceField(label=_("From"),queryset=User.objects.all(), empty_label=_("Select a person"))

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = DatePickerInput()

        if users:
            self.fields['user'].queryset = users

    class Meta:
        model = Expense
        exclude = ['group']

