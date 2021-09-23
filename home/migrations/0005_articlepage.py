# Generated by Django 3.2.7 on 2021-09-21 02:45

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('home', '0004_alter_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.StreamField([('title', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(help_text='Text to display', required=True))])), ('cards', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Bold title text for this card.', max_length=100)), ('text', wagtail.core.blocks.TextBlock(help_text='Optional text for this card.', max_length=255, required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image will be auto. cropped to 570x770')), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(max_length=25)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))], help_text='Enter a link'))])))])), ('ImageAndTextBlock', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image will be auto. cropped to 786x552')), ('image_alignment', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Image to the left'), ('right', 'Image to the right')], help_text='Image on the left with text on the right. Or image on the right with text on the left.')), ('title', wagtail.core.blocks.CharBlock(help_text='Max length of 60 characters', max_length=60)), ('text', wagtail.core.blocks.CharBlock(help_text='Max length of 120 characters', max_length=140, required=False)), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(max_length=25)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))]))])), ('cta', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Max length of 200 characters', max_length=200)), ('link', wagtail.core.blocks.StructBlock([('link_text', wagtail.core.blocks.CharBlock(max_length=25)), ('internal_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_link', wagtail.core.blocks.URLBlock(required=False))]))])), ('richtext', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'link', 'code', 'blockquote'], template='streams/simple_richtext_block.html')), ('large_image', wagtail.images.blocks.ImageChooserBlock(help_text='This image will be cropped to 1200px by 775px', template='streams/large_image_block.html'))], blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Article page',
                'verbose_name_plural': 'Article pages',
            },
            bases=('wagtailcore.page',),
        ),
    ]