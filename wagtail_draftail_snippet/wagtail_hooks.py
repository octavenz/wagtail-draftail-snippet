from django.urls import include, path
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext

from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from wagtail import __version__

from . import urls
from .richtext import (
    ContentstateSnippetLinkConversionRule,
    ContentstateSnippetEmbedConversionRule,
    SnippetLinkHandler,
    SnippetEmbedHandler,
)

WAGTAIL_MAJOR_VERSION = int(__version__.split(".", 1)[0])

if WAGTAIL_MAJOR_VERSION >= 3:
    from wagtail import hooks
else:
    from wagtail.core import hooks


@hooks.register("register_rich_text_features")
def register_snippet_link_feature(features):
    feature_name = "snippet-link"
    type_ = "SNIPPET"

    features.register_link_type(SnippetLinkHandler)

    # wagtailadmin/js/chooser-modal.js is needed for window.ChooserModalOnloadHandlerFactory
    js_include = [
        "wagtailadmin/js/chooser-modal.js",
        "wagtailsnippets/js/snippet-chooser-modal.js",  # not present in wagtail >=v4
        "wagtail_draftail_snippet/js/wagtail-draftail-snippet.js",
    ]

    # In WT3 and earlier, SNIPPET_CHOOSER_MODAL_ONLOAD_HANDLERS exists. In later versions, we need to define it.
    if WAGTAIL_MAJOR_VERSION >= 4:
        js_include.append("wagtail_draftail_snippet/js/snippet-model-chooser-modal.js")
    else:
        js_include.append("wagtail_draftail_snippet/js/snippet-model-chooser.js")

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {
                "type": type_,
                "icon": "snippet",
                "description": gettext("Snippet Link"),
                "chooserUrls": {
                    "snippetLinkModelChooser": reverse("wagtaildraftailsnippet:choose-snippet-link-model"),
                },
            },
            js=js_include,
        ),
    )

    features.register_converter_rule(
        "contentstate", feature_name, ContentstateSnippetLinkConversionRule
    )


@hooks.register("register_rich_text_features")
def register_snippet_embed_feature(features):
    feature_name = "snippet-embed"
    type_ = "SNIPPET-EMBED"

    # Defines a handler for converting db saved content,
    # e.g. <embed app-name="xyz" content-type-name="abcd" embedtype="snippet" id="2"/>
    # into frontend HTML
    features.register_embed_type(SnippetEmbedHandler)

    # todo prob need to add this...
    # # define how to convert between editorhtml's representation of embeds and
    # # the database representation
    # features.register_converter_rule(
    #     "editorhtml", "embed", EditorHTMLEmbedConversionRule
    # )

    js_include = [
        "wagtailadmin/js/chooser-modal.js",  # is needed for window.ChooserModalOnloadHandlerFactory
        # "wagtailsnippets/js/snippet-chooser-modal.js", # doesn't exist in Wagtail 5.2
        "wagtail_draftail_snippet/js/snippet-model-chooser-modal.js", # onload handlers
        "wagtail_draftail_snippet/js/wagtail-draftail-snippet.js", # draftail choosers, Interfaces with Wagtail's ModalWorkflow
    ]

    # In WT3 and earlier, SNIPPET_CHOOSER_MODAL_ONLOAD_HANDLERS exists. In later versions, we need to define it.
    if WAGTAIL_MAJOR_VERSION >= 4:
        js_include.append("wagtail_draftail_snippet/js/snippet-chooser-modal.js")

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {
                "type": type_,
                "icon": "code",
                "description": gettext("Snippet Embed"),
                "chooserUrls": {
                    "snippetEmbedModelChooser": reverse("wagtaildraftailsnippet:choose-snippet-embed-model")
                },
            },
            js=js_include,
        ),
    )

    # Define how to convert between contentstate's representation of embeds and
    # the database representation
    features.register_converter_rule(
        "contentstate", feature_name, ContentstateSnippetEmbedConversionRule
    )


@hooks.register("insert_editor_js")
def editor_js():

    html = f"""
            <script>
                window.chooserUrls.snippetChooser = '{reverse('wagtaildraftailsnippet:choose_generic')}';
            </script>
            """

    return format_html(html)


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [path("snippets/", include(urls, namespace="wagtaildraftailsnippet"))]
