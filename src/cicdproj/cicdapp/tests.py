from cicdapp.models import Entry
from django.test import TestCase
from django.urls import reverse
from factories.factories import EntryFactory


class TestIndexView(TestCase):
    """
    Test case for index view
    """

    def setUp(self) -> None:
        """
        Set up method that is run before every individual test. Here it prepares test user and tasks,
        logs in a user, and sets up a standard response object for use in the tests.
        """
        super().setUp()
        self.response = self.client.get(reverse("index"))

    def test_should_return_status_code_200_when_request_by_name(self):
        """
        Test whether the view returns a HTTP 200 OK status code when a request is made.
        """
        self.assertEqual(self.response.status_code, 200)

    def test_should_check_that_view_use_correct_template(self):
        """
        Test whether the view uses the correct template.
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "cicdapp/index.html")


class TestEntryListView(TestCase):
    """
    Test case for the entries list view.
    """

    template = "cicdapp/entrys_list.html"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("entries")

    def setUp(self) -> None:
        """
        Set up method that is run before every individual test. Here it prepares test user and tasks,
        logs in a user, and sets up a standard response object for use in the tests.
        """
        super().setUp()
        self.test_entry1 = EntryFactory.create()
        self.test_entry2 = EntryFactory.create()
        self.response = self.client.get(self.url)

    def tearDown(self):
        """
        Clean up method after each test case.
        """
        Entry.objects.all().delete()
        super().tearDown()

    def test_should_return_status_code_200_when_request_by_name(self):
        """
        Test whether the view returns a HTTP 200 OK status code when a request is made.
        """
        self.assertEqual(self.response.status_code, 200)

    def test_should_check_that_view_use_correct_template(self):
        """
        Test whether the view uses the correct template.
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, TestEntryListView.template)

    def test_should_return_correct_objects_when_request_is_sent(self):
        """
        Test whether the correct objects are returned when a request is sent to the view.
        """
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, TestEntryListView.template)
        self.assertEqual(
            list(self.response.context["object_list"]),
            [self.test_entry2, self.test_entry1],
        )

    def test_should_make_pagination_if_there_is_more_then_ten_element(self):
        """
        Test whether the view paginates the results when there are more than ten items.
        """
        for _ in range(11):
            EntryFactory.create()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        print(response)
        self.assertContains(response, 'href="?page=2"')
        self.assertEqual(len(response.context["object_list"]), 10)

    def test_elements_should_be_sorted_by_id_from_newest(self):
        """
        Test whether the returned tasks are sorted by id from newest.
        """
        self.assertEqual(
            list(self.response.context["object_list"])[0], self.test_entry2
        )


class TestEntryCreateView(TestCase):
    """
    Test case for the entry create view.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("entry-create")
        cls.data = {
            "text": "test entry text",
        }

    def tearDown(self) -> None:
        Entry.objects.all().delete()
        super().tearDown()

    def test_should_return_form_on_get_with_right_template_and_200_status_code(self):
        """
        Test whether the view returns form object, entry_form.html template and a HTTP 200 OK status code when a GET
        request is made.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cicdapp/entry_form.html")
        self.assertIn("form", response.context)

    def test_should_create_task_object(self):
        """
        Test whether a new entry object is created after a POST request is made.
        """
        response = self.client.post(self.url, data=self.data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Entry.objects.filter(text=self.data["text"]).count(), 1)

    def test_should_redirect_to_proper_url_after_success(self):
        """
        Test whether the view redirects to the correct URL after a successful task creation.
        """
        response = self.client.post(self.url, data=self.data, follow=True)

        self.assertRedirects(
            response,
            reverse("entries"),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class TestEntryDetailView(TestCase):
    """
    Test case for the entry detail view.
    """

    def setUp(self):
        super().setUpClass()
        self.test_entry = EntryFactory.create()
        self.url = reverse("entry", kwargs={"pk": self.test_entry.id})
        self.response = self.client.get(self.url)

    def tearDown(self) -> None:
        Entry.objects.all().delete()
        super().tearDown()

    def test_should_return_object_on_get_with_right_template_and_200_status_code(self):
        """
        Test whether the view returns entry object, correct template and a HTTP 200 OK status code
        """

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "cicdapp/entry_detail.html")
        self.assertIn("object", self.response.context)
        self.assertEqual(self.response.context["object"], self.test_entry)
