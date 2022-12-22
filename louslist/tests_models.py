from django.test import TestCase
from louslist.models import Course, Section, Meeting, User, Profile

class ModelsTests(TestCase):
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
        self.user1 = User.objects.create_user(username='micah')

    def test_course_model(self):
        wgs7500 = Course.objects.get(subject='WGS')
        self.assertEqual(wgs7500.subject, 'WGS')
        self.assertEqual(wgs7500.catalog_number, '7500')
    
    def test_section_model(self):
        wgs7500_001 = Section.objects.get(instructor_name='Tiffany King')
        self.assertEqual(wgs7500_001.course_section, '001')

    def test_meeting_model(self):
        wgs7500 = Meeting.objects.get(days='Mo')
        self.assertEqual(wgs7500.start_time, '15.30.00.000000-05:00')
        self.assertEqual(wgs7500.end_time, '18.00.00.000000-05:00')
        self.assertEqual(wgs7500.facility_description, 'New Cabell Hall 415')
    
    def test_user_model(self):
        self.assertEqual(self.user1.username, 'micah')
    
    def test_profile_model(self):
        profile = Profile.objects.get(user=self.user1)
        profile.year = '3rd'
        profile.major = 'CS'
        self.assertEqual(profile.user.username, 'micah')
        self.assertEqual(profile.year, '3rd')
        self.assertEqual(profile.major, 'CS')

    def tearDown(self):
        self.user1.delete()
