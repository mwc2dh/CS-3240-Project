from .models import *


class CourseJsonParser:
    def __init__(self, json_object) -> None:
        self.json_object = json_object

    def get_course(self):
        subject = self.json_object.get("subject")
        catalog_number=self.json_object.get("catalog_number")
        description=self.json_object.get("description")
        if not Course.objects.filter(subject=subject, catalog_number=catalog_number, description=description):
            Course.objects.create(subject=subject, catalog_number=catalog_number, description=description)
            print("Created course", subject, catalog_number, description)
        return Course.objects.get(subject=subject, catalog_number=catalog_number, description=description)

    def get_section(self):
        
        course = self.get_course()
        
        section = Section(course = course,
                            course_number=self.json_object.get("course_number"),
                            semester_code=self.json_object.get("semester_code"),
                            course_section=self.json_object.get("course_section"),
                            units=self.json_object.get("units"),
                            component=self.json_object.get("component"),
                            class_capacity=self.json_object.get("class_capacity"),
                            wait_list=self.json_object.get("wait_list"),
                            wait_cap=self.json_object.get("wait_cap"),
                            enrollment_total=self.json_object.get("enrollment_total"),
                            enrollment_available=self.json_object.get("enrollment_available"),
                            topic=self.json_object.get("topic", "N/A"),
                            instructor_name=self.json_object.get("instructor", {}).get("name"),
                            instructor_email=self.json_object.get("instructor", {}).get("email"))

        if not Section.objects.filter(course_number = section.course_number).exists():
            section.save()
        
        return Section.objects.get(course_number = section.course_number)


    def get_meetings(self):
        section = self.get_section()
        
        if Meeting.objects.filter(section=section).exists():
            return Meeting.objects.filter(section=section)

        meetings = []

        for meeting in self.json_object.get("meetings", []):
            start_time = meeting.get("start_time")
            end_time = meeting.get("end_time")
            if not start_time or not end_time:
                new_meeting = Meeting(section=section, days=meeting.get("days"), start_time="", end_time="", facility_description=meeting.get("facility_description"))
            else:
                start_ampm = "AM" if int(start_time[0:2]) < 12 else "PM"
                end_ampm = "AM" if int(end_time[0:2]) < 12 else "PM"
                start_hour = start_time[0:2] if int(start_time[0:2]) < 13 else str(int(start_time[0:2])-12)
                end_hour = end_time[0:2] if int(end_time[0:2]) < 13 else str(int(end_time[0:2])-12)
                start_time_str = start_hour + ":" + start_time[3:5] + start_ampm
                end_time_str = end_hour + ":" + end_time[3:5] + end_ampm 
                new_meeting = Meeting(section=section,
                                        days = meeting.get("days"),
                                        start_time = start_time_str,
                                        end_time = end_time_str,
                                        facility_description = meeting.get("facility_description"))
            meetings.append(new_meeting)
        
        for meeting in meetings:
            meeting.save()

        return meetings
    
    def load_all(self):
        self.get_meetings()
        # load the sections into course model