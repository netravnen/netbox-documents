from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from netbox_documents.template_content import _make_extension


class DocumentPanelRenderTest(TestCase):
    """Tests for the documents panel visibility in _render_panel()."""

    def setUp(self):
        # Any saved model instance works as the detail page object.
        self.obj = ContentType.objects.get_for_model(ContentType)
        self.model_label = f'{self.obj.app_label}.{self.obj.model}'
        extension_class = _make_extension('contenttypes.contenttype')
        self.extension = extension_class({'object': self.obj})

    def _render(self):
        with patch.object(self.extension, 'render', return_value='PANEL'), \
                patch.object(self.extension, '_get_return_url', return_value='/'):
            return self.extension._render_panel()

    def test_panel_shown_when_mapping_empty(self):
        """Should render the panel with the default empty mapping."""
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': {}}}):
            self.assertEqual(self._render(), 'PANEL')

    def test_panel_shown_when_no_plugin_config(self):
        """Should render the panel when the plugin has no configuration."""
        with self.settings(PLUGINS_CONFIG={}):
            self.assertEqual(self._render(), 'PANEL')

    def test_panel_shown_when_model_has_types(self):
        """Should render the panel when the model maps to some types."""
        mapping = {self.model_label: ['diagram']}
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            self.assertEqual(self._render(), 'PANEL')

    def test_panel_hidden_when_model_has_no_types(self):
        """Should hide the panel when the model maps to an empty list."""
        mapping = {self.model_label: []}
        with self.settings(PLUGINS_CONFIG={'netbox_documents': {'allowed_doc_types': mapping}}):
            self.assertEqual(self._render(), '')
