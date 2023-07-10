from rest_framework import serializers
from .models import Movie
from django.utils import timezone
from rest_framework.validators import UniqueValidator
from rest_framework.validators import ValidationError

PREFIX= "Movie-"

class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        min_length=len(PREFIX)+2,
        max_length=len(PREFIX)+100,
        validators=[UniqueValidator(queryset=Movie.objects.all())],
        error_messages={
            'required': 'The title field is required.',
            'min_length': 'The movie title must be at least 2 characters long.',
            'max_length': 'The movie title must be at most 100 characters long.',
            'unique': 'A movie with this title already exists.'
        }
    )
    release_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'The release_date field is required.',
            'invalid_date': 'Enter a valid date.',
            'future_date': 'The release date cannot be in the future.',
            'past_date': 'The release date should be within the last 30 years.'
        }
    )
    genre = serializers.ChoiceField(
        choices=["Action", "Drama", "Comedy", "Thriller", "Sci-Fi"],
        required=True,
        error_messages={
            'required': 'The genre field is required.',
            'invalid_choice': 'Invalid genre. Choose one of: Action, Drama, Comedy, Thriller, Sci-Fi.'
        }
    )
    duration_minutes = serializers.IntegerField(
        required=True,
        min_value=1,
        max_value=600,
        error_messages={
            'required': 'The duration_minutes field is required.',
            'min_value': 'The duration must be at least 1 minute.',
            'max_value': 'The duration cannot exceed 600 minutes (10 hours).',
            'invalid': 'Enter a valid integer.'
        }
    )
    rating = serializers.DecimalField(
        required=False,
        max_digits=3,
        decimal_places=1,
        min_value=0.0,
        max_value=10.0,
        error_messages={
            'max_digits': 'There should be only 3 digits in total.The rating cannot exceed 10.0.',
            'max_decimal_places': 'Ensure that there are not more than 1 decimal place.',
            'min_value': 'The rating must be at least 0.0.',
            'max_value': 'The rating cannot exceed 10.0.',
            'invalid': 'Enter a valid decimal number.'
        }
    )

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):

        if value > timezone.now().date():
            raise ValidationError(self.fields['release_date'].error_messages['future_date'])
        if value.year < timezone.now().year - 30:
            raise ValidationError(self.fields['release_date'].error_messages['past_date'])
        return value

    def validate_title(self, value):

        if not value.startswith(PREFIX):
            raise ValidationError('The title should start with "Movie-".')
        text_after_prefix = value[len(PREFIX):]
        if len(text_after_prefix) < 2 or len(text_after_prefix) > 100:
            raise serializers.ValidationError(
                'The length of the title (excluding "Movie-" prefix) must be between 2 and 100 characters.'
            )
        existing_titles = Movie.objects.filter(title=value)
        if self.instance:
            existing_titles = existing_titles.exclude(pk=self.instance.pk)
        if existing_titles.exists():
            raise serializers.ValidationError(self.fields['title'].error_messages['unique'])
        return value
