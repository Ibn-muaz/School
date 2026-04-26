from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0003_remove_feestructure_total_fee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feestructure',
            old_name='tuition_fee',
            new_name='tuition_fee_per_unit',
        ),
    ]