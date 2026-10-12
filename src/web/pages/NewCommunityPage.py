from playwright.sync_api import Page, expect

from src.web.components.Header import Header


class NewCommunityPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)

        self.form = page.get_by_test_id('community-create-form')
        self.name_input = page.get_by_test_id('community-name-input')
        self.slug_input = page.get_by_test_id('community-slug-input')
        self.description_input = page.get_by_test_id('community-description-input')

        self.cover_section = page.get_by_test_id('community-cover-upload')
        self.cover_preview = page.get_by_test_id('community-cover-preview')
        self.cover_upload_button = page.get_by_test_id('community-cover-upload-btn')
        self.cover_upload_status = page.get_by_test_id('community-cover-upload-status')
        self.cover_manual_url_toggle = self.cover_section.get_by_text('Вставити URL вручну', exact=True)

        self.unlisted_checkbox = page.get_by_test_id('community-unlisted-input')
        self.create_button = page.get_by_test_id('community-create-submit')

    def is_loaded(self):
        expect(self.header.title).to_have_text('Створити спільноту')
        self.header.is_loaded()

        for element in [
            self.form,
            self.name_input,
            self.slug_input,
            self.description_input,
            self.cover_section,
            self.cover_preview,
            self.cover_upload_button,
            self.cover_upload_status,
            self.cover_manual_url_toggle,
            self.unlisted_checkbox,
            self.create_button,
        ]:
            expect(element).to_be_visible()

    def create_community(self, name: str, slug: str, description: str):
        self.name_input.fill(name)
        self.slug_input.fill(slug)
        self.description_input.fill(description)
        self.unlisted_checkbox.click()
        self.create_button.click()
