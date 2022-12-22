from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# class Instructor(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     def __str__(self):
#         return str(self.name)


class Course(models.Model):
    subject = models.CharField(max_length=4)
    catalog_number = models.CharField(max_length=4, default="")
    description = models.TextField(default="")
    def __str__(self):
        return self.subject + " " + self.catalog_number + " " + self.description


class Section(models.Model):
    #instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    instructor_name = models.CharField(max_length=50, default="")
    instructor_email = models.EmailField(default="a@gmail.com")
    course_number = models.IntegerField()
    semester_code = models.IntegerField()
    course_section = models.CharField(max_length=5)
    #subject = models.CharField(max_length=4)
    #catalog_number = models.CharField(max_length=4)
    #description = models.TextField()
    units = models.CharField(max_length=20)
    component = models.CharField(max_length=10)
    class_capacity = models.IntegerField()
    wait_list = models.IntegerField()
    wait_cap = models.IntegerField()
    enrollment_total = models.IntegerField()
    enrollment_available = models.IntegerField()
    topic = models.CharField(max_length=50)
    def __str__(self):
        return str(self.course) + str(self.course_number)
    def get_meetings(self):
        return Meeting.objects.filter(section=self)

    def conflicts(self, other_section):
        # returns true or false depending on if there's a time conflict
        this_meetings = self.get_meetings()
        m2s = other_section.get_meetings()

        for m1 in this_meetings:
            for m2 in m2s:
                if Meeting.conflicts(m1, m2):
                    return True

        return False
    

class Meeting(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    days = models.CharField(max_length=50) 
    start_time = models.CharField(max_length=50) 
    end_time = models.CharField(max_length=50)
    facility_description = models.CharField(max_length=50)
    def __str__(self):
        #"08.30.00.000000-05:00"
        #start_time = datetime.strptime(self.start_time, "%H.%M.%S.%f-%z")
        start_time = self.start_time
        end_time = self.end_time
        return str(self.days) + " " + start_time[:-2].lstrip("0") + "-" + end_time.lstrip("0")

    @staticmethod
    def conflicts(m1, m2):
        self_start = datetime.strptime(m1.start_time, "%I:%M%p")
        self_end = datetime.strptime(m1.end_time, "%I:%M%p")
        other_start = datetime.strptime(m2.start_time, "%I:%M%p")
        other_end = datetime.strptime(m2.end_time, "%I:%M%p")
        #(StartA <= EndB) and (EndA >= StartB) = conflict
        time_conflict = (self_start <= other_end) and (self_end >= other_start)

        m1_days = set([m1.days[i:i+2] for i in range(0, len(m1.days), 2)])
        m2_days = set([m2.days[i:i+2] for i in range(0, len(m2.days), 2)])

        intersect = m1_days.intersection(m2_days)
        if len(intersect) > 0 and time_conflict:
            return True
        else:
            return False
        

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=50)
    year = models.CharField(max_length=10)
    bio = models.TextField()
    saved_sections = models.ManyToManyField(Section, blank=True)
    friends = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " (" + self.user.username + ")"

    def get_comments(self):
        return Comment.objects.filter(profile=self).order_by("-comment_date")
    

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name="comment_profile_set")
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, related_name="comment_commenter_set")
    text = models.TextField(default="")
    comment_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.profile) + " " + self.text
    
