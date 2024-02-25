
# Главная навигация сайта
navigate_locator = {
    'nav_items': "//nav//li[@class='navigation__item ']/a",
    'nav_item_by_name': "//nav//li[@class='navigation__item ']/a[text()='{}']",
    'h1_global_page': "//h1[text()]",
    'selected_tab': "//nav//li[@class='navigation__item navigation__list--active']/a"
    }

# Навигация в профиле
profile_navigate_locator = {
    'nav_items': "//a[@role='tab']/span",
    'nav_item_by_name': "//a[@role='tab']/span[text()='{}']",
    'profile_name_main': "//h3[@class='forum-profile__head-title title-global forum-profile__head--backwrapped ']/span"
    }

# Быстрый просмотр профиля
fast_preview_profile_locator = {
    'prifile_icon': "//a[@class='header__link header__link--user header__link--user--active']",
    'prifile_name_fast_preview': "//p[@class='header__subitem-text--name']",
    'sing_out': "//i[@class='fas fa-sign-out-alt']",
    'submit_sing_out': "//button[@id='logout-yes-btn']"
}

# Авторизация
auth_locator = {
    'login_input_form': "//input[@id='login_credential_form']",
    'password_input_form': "//input[@id='login_password_form']",
    'login_input': "//input[@id='login_credential']",
    'password_input': "//input[@id='login_password']",
    'submit_button_form': "//form//button[@class='authorization__btn mb32']"
}

# Страница База героев
hero_base = {
    "search_input": "//input[@name='name']",
    "role_box": "//select[@name='role']",
    "attack_type_box": "//select[@name='attack_type']",
    "hero_type_title_all": "//h3[@class='subtitle-global base-hero__subtitle']",
    "hero_in_search": '//a[@data-tooltipe="{}"]'
}

# Страница Новости
news_page = {
    "search_news_input": '//input[@class="js-news-search"]',
    "news_title_all": '//div[@class="global-content__btn-block global-content__btn-block--nowrap"]/a',
    "comments_block": "//div[@class='component-block__title subtitle-global']",
}

# Страница Киберспорт
cybersports_page = {
    'nav_item_by_name': "//div[@class='global-content__btn-block-top']/a[normalize-space()='{}']",
    'h1_global_page': "//h1[text()]",
    "cybersports_title_all": "//div[@class='global-content__btn-block-top']/a",
    "comments_block": "//div[@class='component-block__title subtitle-global']",
}
