from src.utils.data import fake
from src.web.application import Application


def test_create_new_community(logged_app: Application):
    community_name = f'{fake.street_name()} community'
    community_slug = fake.slug()
    community_description = fake.sentence()

    logged_app.me_page.open()
    logged_app.me_page.expect_loaded()
    logged_app.me_page.open_new_community()
    logged_app.new_community_page.expect_loaded()

    logged_app.new_community_page.create_community(community_name, community_slug, community_description)

    logged_app.community_page.check_community_info(community_name, community_slug, community_description)
