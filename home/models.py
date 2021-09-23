from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core import blocks as wagtail_blocks
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey

from home import blocks

## Pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class HomePage(Page):

    lead_text = models.CharField(
        max_length=140, blank=True, help_text="Banner title here"
    )
    button = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        help_text="Select an optional page link to",
        on_delete=models.SET_NULL,
    )
    button_text = models.CharField(
        max_length=50,
        default="Read more",
        blank=False,
        help_text="Button text",
    )
    banner_background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        help_text="The banner background image",
        on_delete=models.SET_NULL,
    )

    banner = MultiFieldPanel([
        FieldPanel("lead_text"),
        PageChooserPanel("button"),
        FieldPanel("button_text"),
        ImageChooserPanel("banner_background_image"),
    ], heading='Banner Info', classname='collapsible')

    body = StreamField(
        [
            ("title", wagtail_blocks.CharBlock(classname="Full title")),
            ("cards", blocks.CardsBlock()),
            ("ImageAndTextBlock", blocks.ImageAndTextBlock()),
            ("cta", blocks.CallToActionBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        banner,
        StreamFieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        all_posts = ArticlePage.objects.all().order_by('-first_published_at')

        paginator = Paginator(all_posts, 5)

        page = request.GET.get("page")

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["articles"] = posts
        return context


class ArticlePage(Page):
    parent_page_types = ["home.HomePage"]

    intro = models.CharField(
        max_length=140, blank=True, help_text="News introduction"
    )

    author = SnippetChooserBlock(
        target_model="snippets.Author",
        template="snippets/author_block.html",
    )

    body = StreamField(
        [
            ("title", blocks.TitleBlock()),
            ("cards", blocks.CardsBlock()),
            ("ImageAndTextBlock", blocks.ImageAndTextBlock()),
            ("cta", blocks.CallToActionBlock()),
            (
                "richtext",
                wagtail_blocks.RichTextBlock(
                    template="streams/simple_richtext_block.html",
                    features=[
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "link",
                        "code",
                        "blockquote",
                    ],
                ),
            ),
            (
                "large_image",
                ImageChooserBlock(
                    help_text="This image will be cropped to 1200px by 775px",
                    template="streams/large_image_block.html",
                ),
            ),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("intro"),
            InlinePanel('author', label='Author'),
        ], heading='Article info'),
        StreamFieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Article page"
        verbose_name_plural = "Article pages"
    
    @property
    def authors(self):
        return self.author.select_related('author').all()


class AuthorItem(Orderable):
    page = ParentalKey('home.ArticlePage', related_name='author')
    show_boolean = models.BooleanField("Show Author Bio",
                                       default=False)
    author = models.ForeignKey('snippets.Author',
                               null=True,
                               blank=False,
                               on_delete=models.CASCADE,
                               related_name='+')

    panels = [SnippetChooserPanel('author')]
