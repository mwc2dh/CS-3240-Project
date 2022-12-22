from django.test import TestCase
from louslist.models import Course, Section, Meeting, User, Profile
from louslist.views import SearchUsersResultsView
from django.urls import reverse 

class URLsTests(TestCase):
    def setUp(self):
        Course.objects.create(subject='WGS', 
                              catalog_number='7500', 
                              description='Topics in Gender and Sexuality Studies')
        Section.objects.create(course=Course.objects.get(subject='WGS'), 
                               instructor_name='Tiffany King',
                               instructor_email='tjk9b@virginia.edu',
                               course_number=13512, 
                               semester_code=1228, 
                               course_section='001', 
                               units='3', 
                               component='SEM', 
                               class_capacity=20, 
                               wait_list=0, 
                               wait_cap=199,
                               enrollment_total=13,
                               enrollment_available=7,
                               topic='Approaches to Gender & Sexuality Studies')
        Meeting.objects.create(section=Section.objects.get(instructor_name='Tiffany King'),
                               days='Mo',
                               start_time='15.30.00.000000-05:00',
                               end_time='18.00.00.000000-05:00',
                               facility_description='New Cabell Hall 415')
        self.user1 = User.objects.create_user(username='micah', password='test')

    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_users_home_url(self):
        response = self.client.get(reverse('users-home'))
        self.assertEqual(response.status_code, 200)

    def test_search_users_home_view_url(self):
        response = self.client.get(reverse('search_users_home_view'))
        self.assertEqual(response.status_code, 200)

    def test_users_register_url(self):
        response = self.client.get(reverse('users-register'))
        self.assertEqual(response.status_code, 200)

    def test_users_profile_url(self):
        self.client.force_login(self.user1)
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_password_change_url(self):
        self.client.force_login(self.user1)
        response = self.client.get('/password-change/')
        self.assertEqual(response.status_code, 200)

    def test_saved_courses_url(self):
        self.client.force_login(self.user1)
        response = self.client.get('/section/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_dept_page_url(self):
        response = reverse('dept_page', kwargs={'dept': 'ANTH'})
        self.assertEqual(response, '/departments/ANTH')

    def test_course_page_url(self):
        response = reverse('course_page', kwargs={'dept': 'CS', 'catalog_number': '1110'})
        self.assertEqual(response, '/departments/CS/1110')

    def test_view_friend_url(self):
        response = reverse('profile_detail_view', kwargs={'username': 'keivon'})
        self.assertEqual(response, '/profile/keivon')

    def test_add_friend_url(self):
        self.client.force_login(self.user1)
        response = self.client.get('/friends/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friendslist.html')