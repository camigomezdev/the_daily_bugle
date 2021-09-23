from django import forms

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList


class TitleBlock(blocks.StructBlock):
    text = blocks.CharBlock(
        required=True,
        help_text="Text to display",
    )

    class Meta:
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on the page"


class LinkValue(blocks.StructValue):
    """Additional logic for our links."""

    def url(self) -> str:
        internal_page = self.get("internal_page")
        external_link = self.get("external_link")
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        return ""


class Link(blocks.StructBlock):
    link_text = blocks.CharBlock(max_length=25)
    internal_page = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(required=False)

    class Meta:
        value_class = LinkValue

    def clean(self, value):
        internal_page = value.get("internal_page")
        external_link = value.get("external_link")

        errors = {}
        if not internal_page and not external_link:
            errors["internal_page"] = ErrorList(
                ["Please select at least one of this options"]
            )
            errors["external_link"] = ErrorList(
                ["Please select at least one of this options"]
            )

        if internal_page and external_link:
            errors["internal_page"] = ErrorList(["Both can't be exist"])
            errors["external_link"] = ErrorList(["Both can't be exist"])

        if errors:
            raise ValidationError("Validation error in your link", params=errors)

        return super().clean(value)


class Card(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=100,
        help_text="Bold title text for this card.",
    )
    text = blocks.TextBlock(
        max_length=255, help_text="Optional text for this card.", required=False
    )
    image = ImageChooserBlock(help_text="Image will be auto. cropped to 570x770")
    link = Link(help_text="Enter a link")


class CardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(Card())

    class Meta:
        template = "streams/cards_block.html"
        icon = "image"
        label = "Standar Cards"


class RadioSelectBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)


class ImageAndTextBlock(blocks.StructBlock):
    image = ImageChooserBlock(help_text="Image will be auto. cropped to 786x552")
    image_alignment = RadioSelectBlock(
        choices=(
            ("left", "Image to the left"),
            ("right", "Image to the right"),
        ),
        default="left",
        help_text="Image on the left with text on the right. Or image on the right with text on the left.",
    )
    title = blocks.CharBlock(max_length=60, help_text="Max length of 60 characters")
    text = blocks.CharBlock(
        max_length=140, required=False, help_text="Max length of 120 characters"
    )

    link = Link()

    class Meta:
        template = "streams/image_and_text_block.html"
        icon = "image"
        label = "Image & Text"


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200, help_text="Max length of 200 characters")
    link = Link()

    class Meta:
        template = "streams/call_to_action_block.html"
        icon = "plus"
        label = "Call to Action"


class PrincingTableBlock(TableBlock):
    class Meta:
        template = "streams/pricing_table_block.html"
        label = "Pricing Table"
        icon = "table"
        help_text = "Some text"


class RichTextWithTitle(blocks.StructBlock):

    title = blocks.CharBlock(max_length=50)
    context = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "link", "code", "blockquote"]
    )

    class Meta:
        template = "streams/simple_richtext_block.html"
        label = "RichText"
        icon = "table"
        help_text = "Some text"
