from django.test import TestCase
from louslist.models import Course, Section, Meeting, User, Profile
import louslist.views

class FeaturesTests(TestCase):
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

    # search for a course
    def test_search(self):
        response = self.client.get('/search/general?q=cs')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_general_results.html')

    # search for an instructor
    def test_search(self):
        response = self.client.get('/search/general?q=bloomfield')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_general_results.html')

    # updating profile
    def test_updating_profile(self):
        user = self.user1
        self.client.force_login(self.user1)
        user.username = 'keivon'
        self.assertEquals(user.username, 'keivon')

    # updating password
    def test_updating_password(self):
        user = self.user1
        user.set_password('happy')
        user.save()
        self.assertEquals(user.check_password('happy'), True)

    # search for a user
    def test_search_user(self):
        self.client.force_login(self.user1)
        response = self.client.get('/search/users/results?q=emil')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_users_results.html')

    # saving a course
    def test_save_course(self):
        profile = Profile.objects.get(user=self.user1)
        profile.year = '3rd'
        profile.major = 'CS'
        self.client.force_login(self.user1)
        self.client.post('/section/save',{'section_to_save': '13512'})
        self.assertTrue(profile.saved_sections.filter(course_number=13512).exists())

    # unsaving a course
    def test_unsave_course(self):
        profile = Profile.objects.get(user = self.user1)
        profile.year = '3rd'
        profile.major = 'CS'
        self.client.force_login(self.user1)
        self.client.post('/section/save',{'section_to_save': '13512'})
        self.client.post('/section/unsave',{'section_to_unsave': '13512'})
        self.assertFalse(profile.saved_sections.filter(course_number=13512).exists())

    # adding a friend
    def test_add_friend(self):
        profile = Profile.objects.get(user = self.user1)
        profile.year = '3rd'
        profile.major = 'CS'
        user2 = User.objects.create_user(username='eei9wnp', password='test')
        self.client.force_login(self.user1)
        self.client.post('/profile/save',{'username': 'eei9wnp'})
        self.assertTrue(profile.friends.filter(user__username='eei9wnp').exists())

    # unadding a friend
    def test_unadd_friend(self):
        profile = Profile.objects.get(user = self.user1)
        profile.year = '3rd'
        profile.major = 'CS'
        user2 = User.objects.create_user(username='eei9wnp', password='test')
        self.client.force_login(self.user1)
        self.client.post('/profile/save',{'username': 'eei9wnp'})
        self.client.post('/profile/unsave',{'username': 'eei9wnp'})
        self.assertFalse(profile.friends.filter(user__username='eei9wnp').exists())
