from django import forms

from posts.models import Link

class LinkAddForm(forms.ModelForm):

	class Meta:
			model = Link
			fields = (
				'title',
				'url',
				'description',
				'tags',
				'owner_authored',				
			)

	def __init__(self, *args, **kwargs):
		super(LinkAddForm, self).__init__(*args, **kwargs)
		self.fields['owner_authored'].label = "Are you the author of this resource?"

	def clean_slug(self):
		slug = self.cleaned_data.get('slug').strip().lower()
		if not slug:
			raise forms.ValidationError("You must set a slug")
		if " " in slug:
			raise forms.ValidationError("You can't have spaces in your slug")

		return slug


