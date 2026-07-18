from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("analysis", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="analysis",
            name="matching_score",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="analysis",
            name="interview_questions",
            field=models.JSONField(default=list),
        ),
    ]
