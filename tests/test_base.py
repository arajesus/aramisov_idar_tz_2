import allure
import time

from locators.locators import navigate_locator, fast_preview_profile_locator, profile_navigate_locator, \
    hero_base, news_page, cybersports_page


class TestPc:

    @allure.title("Тест 1: Панель навигации")
    @allure.description("Проверка отображения элементов главной навигации, проверка отображения выбранной страницы, проверка переходов")
    def test_main_navigation(self, page_helper):
        nav_test_data = [("Форум", "Dota 2 Форум"),
                         ("Новости", "Новости"),
                         ("Киберспорт", "Расписание матчей по Dota 2"),
                         ("База знаний", "Герои"),
                         ("Стримы", "Стримы Dota 2"),
                         ("Видео", "Видео Dota 2"),
                         ("Мемы", "Мемы Dota 2"),
                         ]

        page_helper.open_main_page()

        with allure.step("Проверка на наличие нужных элементов навигации на странице"):
            elements = page_helper.get_elements_path(locator=navigate_locator['nav_items'])
            assert len(elements) == len(nav_test_data)

            for i in elements:
                assert page_helper.get_text_element(element=i) in [item[0] for item in nav_test_data]

        with allure.step("Проверка переходов по навигации, ожидается появление нужных элементов"):
            for i in nav_test_data:
                page_helper.click_nav_item(i[0])
                # Проверка выбранной страницы
                assert page_helper.get_text(locator=navigate_locator['selected_tab']) == i[0]
                # Проверка переходов
                assert page_helper.get_text(locator=navigate_locator['h1_global_page']) == i[1]
                # Проверка наличия остальный после перехода
                assert len(page_helper.get_elements_path(locator=navigate_locator['nav_items'])) == len(nav_test_data) - 1

    @allure.feature("Тест 2: Авторизация")
    @allure.title("Проверка негативной и позитивной авторизации")
    def test_authentication_check(self, page_helper, test_data):

        person_random = test_data.get_fake_person()
        person_positiv = test_data.get_admin()

        page_helper.open_main_page()

        # TODO Происходит блокировка по ip при частом использовании, раскоментировать при прогоне
        # with allure.step("Негатив - Вход с фейк данными, проверка появления ошибки"):
        #     pass
        #     page_helper.auth_person(person_random)
        #     assert page_helper.element_is_visible_bool(locator="//div[@class='noty_message']"), "Authentication error - Ошибка не появилась с рандом данными"
        #     time.sleep(10)
        #
        #     assert not page_helper.element_is_visible_bool(locator="//div[@class='noty_message']"), "Authentication error - Ошибка не пропала спустя время"

        with allure.step("Позитив - Вход с норм данными, проверка отсутствия ошибки"):
            page_helper.auth_person(person_positiv, clean=True)

            assert not page_helper.element_is_visible_bool(locator="//div[@class='noty_message']"), "Authentication error - Ошибка появилась с валидными данными"

        with allure.step("Проверка авторизации, проверка валидности профиля"):
            page_helper.move_to_element_and_click(locator=fast_preview_profile_locator["prifile_icon"])

            assert page_helper.element_is_visible_bool(locator=fast_preview_profile_locator["prifile_name_fast_preview"]), "Логин в быстром просмотре не отображается"
            assert page_helper.get_text(locator=fast_preview_profile_locator["prifile_name_fast_preview"]) == person_positiv["username"]

    @allure.feature("Тест 3 : Навигация профиль")
    @allure.title("Проверка перехода в профиль после авторизации, проверка навигации по разделам профиля")
    def test_profile_main_page(self, page_helper, test_data):
        profile_nav = ["Стена", "Активность", "Нарушения", "Информация", "Оценки"]

        person_positiv = test_data.get_admin()
        page_helper.open_main_page()

        with allure.step("Авторизация и переход на главную страницу профиля"):
            page_helper.auth_person(person_positiv, clean=False)
            page_helper.move_to_element_and_click(locator=fast_preview_profile_locator["prifile_icon"])
            time.sleep(2)
            page_helper.move_to_element_and_click(locator=fast_preview_profile_locator["prifile_name_fast_preview"])

            assert page_helper.get_text(locator=profile_navigate_locator["profile_name_main"]) == person_positiv["username"], "Логин не отображается на главной странице профиля"

        with allure.step("Проверка на наличие нужных элементов навигации на странице"):
            assert len(page_helper.get_elements_path(locator=navigate_locator['nav_items'])) == 6, "Не отображается главная навигация по сайту"

            elements = page_helper.get_elements_path(locator=profile_navigate_locator['nav_items'])
            assert len(elements) == len(profile_nav)

            for i in elements:
                assert page_helper.get_text_element(element=i) in profile_nav

    @allure.feature("Тест 4 : Выход из профиля")
    @allure.title("Проверка выхода из профиля")
    def test_sing_out_profile(self, page_helper, test_data):

        person_positiv = test_data.get_admin()
        page_helper.open_main_page()

        with allure.step("Авторизация и переход на главную страницу профиля"):
            page_helper.auth_person(person_positiv, clean=False)
            page_helper.move_to_element_and_click(locator=fast_preview_profile_locator["prifile_icon"])
            assert page_helper.element_is_visible_bool(locator=fast_preview_profile_locator["prifile_name_fast_preview"]), "Логин в быстром просмотре не отображается"

        with allure.step("Выход из профиля"):
            page_helper.move_to_element_and_click(locator=fast_preview_profile_locator["sing_out"])
            page_helper.move_to_element_and_click(locator=fast_preview_profile_locator["submit_sing_out"])

            time.sleep(5)
            assert not page_helper.element_is_visible_bool(locator=fast_preview_profile_locator["prifile_icon"]), "Выход не выполнился"
            assert len(page_helper.get_elements_path(locator=navigate_locator['nav_items'])) == 7, "Проверка навигации"

    @allure.feature("Тест 5 : Проверка страницы 'База знаний'")
    @allure.title("Проверка отображения всех классов персонажей и проверка поиска")
    def test_hero_base_page(self, page_helper):
        hero_type_all = ["Сила", "Ловкость", "Интеллект", "Универсальный"]

        page_helper.open_main_page()

        with allure.step("Переход на страницу с персонажами и проверка отображения всех классов персонажей"):
            page_helper.click_nav_item("База знаний")
            elements = page_helper.get_elements_path(locator=hero_base['hero_type_title_all'])

            assert len(elements) == 4, "Отображаются не все классы героев"

            for i in elements:
                assert page_helper.get_text_element(element=i) in hero_type_all

        with allure.step("Проверка поиска героев"):
            hero_name = "Pudge"
            page_helper.set_value(locator=hero_base['search_input'], value=hero_name, clean=False)

            assert page_helper.element_is_visible_bool(locator=hero_base['hero_in_search'].format(hero_name)), "Нужный герой не отображается на странице"
            assert not page_helper.element_is_visible_bool(locator=hero_base['hero_in_search'].format("Axe")), "На странице левый герой"

    @allure.feature("Тест 6 : Проверка страницы 'Новости'")
    @allure.title("Отображения страницы 'Новости', проверка на наличие всех разделов новостей")
    def test_news_page(self, page_helper):
        news_all_tab = ["Все", "Обновления", "Патчи", "Интервью", "Статьи", "Разное", "Железо"]

        page_helper.open_main_page()

        with allure.step("Переход на страницу с новостями и проверка отображения всех категорий"):
            page_helper.click_nav_item("Новости")
            elements = page_helper.get_elements_path(locator=news_page['news_title_all'])

            assert len(elements) == 7, "Отображаются не все категории"
            assert page_helper.element_is_visible_bool(locator=news_page['comments_block'])

            for i in elements:
                assert page_helper.get_text_element(element=i) in news_all_tab

    @allure.title("Тест 7: Проверка страницы 'Киберспорт'")
    @allure.description("Отображения страницы 'Киберспорт', проверка на наличие всех разделов")
    def test_cybersports_page(self, page_helper):
        nav_cybersports_test_data = [("Матчи", "Расписание матчей по Dota 2"),
                                     ("Турниры", "Турниры по Dota 2"),
                                     ("DPC", "Dota Pro Circuit 2022-23"),
                                     ("Команды", "Профессиональные команды по Dota 2"),
                                     ("Игроки", "Профессиональные игроки по Dota 2"),
                                     ("Трансферы", "Трансферы по Dota 2"),
                                     ("Карты", "Карты по Dota 2"),
                                     ("Студии", "Студии освещения по Dota 2"),
                                     ("Сборки", "Сборки игроков в профессиональных матчах"),
                                     ("Прогнозы", "Прогнозы")
                                     ]

        page_helper.open_main_page()

        with allure.step("Переход на страницу Киберспорт"):
            page_helper.click_nav_item("Киберспорт")
            elements = page_helper.get_elements_path(locator=cybersports_page['cybersports_title_all'])

            assert len(elements) == 10, "Отображаются не все категории страницы Кибирспорт"
            assert page_helper.element_is_visible_bool(locator=cybersports_page['comments_block'])

            for i in elements:
                assert page_helper.get_text_element(element=i) in [item[0] for item in nav_cybersports_test_data]

        with allure.step("Проверка переходов по внутренней навигации, ожидается появление нужных элементов"):
            for i in nav_cybersports_test_data:
                page_helper.click_nav_item_cybersports(i[0])

                # Проверка переходов
                assert page_helper.get_text(locator=cybersports_page['h1_global_page']) == i[1]

                # Проверка наличия остальный после перехода
                assert len(elements) == 10, "Отображаются не все категории страницы Кибирспорт"

                assert page_helper.element_is_visible_bool(locator=cybersports_page['comments_block'])
