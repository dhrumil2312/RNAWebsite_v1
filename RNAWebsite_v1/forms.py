from django import forms


class BothTextData_Form(forms.Form):
    sequence = forms.CharField(max_length=5000)
    structure = forms.CharField(max_length=5000)
    emailId = forms.CharField(max_length=1000)

class CTForm(forms.Form):
    ct_file = forms.FileField()
    ct_emailId= forms.CharField(max_length=1000)


class ENTRNA_BatchMode(forms.Form):
    file = forms.FileField()
    emailId = forms.CharField(max_length=1000)

class QLRNA_text(forms.Form):
    structure = forms.CharField(max_length=5000)
    emailId = forms.CharField(max_length=100)

class QLRNA_file(forms.Form):
    structureFile = forms.FileField()
    emailId= forms.CharField(max_length=100)

class QLRNA_BatchMode(forms.Form):
    structureBatchMode = forms.FileField()
    emailId = forms.CharField(max_length=100)