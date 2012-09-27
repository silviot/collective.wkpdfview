import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from urllib import urlopen

from collective.wkpdfview.testing import\
    COLLECTIVE_WKPDFVIEW_FUNCTIONAL


class TestExample(unittest.TestCase):

    layer = COLLECTIVE_WKPDFVIEW_FUNCTIONAL

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.wkpdfview'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_download_homepage_as_pdf(self):
        portal = self.layer['portal']
        path = '/'.join(portal.getPhysicalPath())
        host, port = self.layer['zserver_info']
        url = "http://%(host)s:%(port)i%(path)s/@@wkpdf" % locals()
        result = urlopen(url)
        pdf_data = result.read()
        # PDFs have magic byte %PDF
        self.assertEqual('%PDF', pdf_data[:4])