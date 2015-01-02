from django import forms

from posts.models import Post

class PostAddForm(forms.ModelForm):

	class Meta:
			model = Post
			fields = (
				'title',
				'url',
				'description',
				'tags',
				'skill_level',
				'owner_authored',				
			)

	def __init__(self, *args, **kwargs):
		super(PostAddForm, self).__init__(*args, **kwargs)
		self.fields['owner_authored'].label = "Are you the author of this resource?"
		self.fields['tags'].label = "Tags/Topics (separate by commas):"

	def clean_slug(self):
		slug = self.cleaned_data.get('slug').strip().lower()
		if not slug:
			raise forms.ValidationError("You must set a slug")
		if " " in slug:
			raise forms.ValidationError("You can't have spaces in your slug")

		return slug


