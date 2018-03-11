from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def format_speed(speed):
    return "{}:{:02.0f}".format(int(speed), (speed-int(speed))*60)


def format_time(time):
    return "{}:{:02.0f}".format(int(time/60), time - int(time/60)*60)


class Activity(models.Model):
    avg_heart_rate = models.FloatField(help_text="bmp", blank=True, null=True)
    avg_heart_rate_clock = models.FloatField(help_text="bmp", blank=True, null=True)
    avg_speed = models.FloatField(help_text="min/km", blank=True, null=True)
    max_heart_rate = models.IntegerField(help_text="bmp", blank=True, null=True)
    max_heart_rate_clock = models.IntegerField(help_text="bmp", blank=True, null=True)
    max_speed = models.FloatField(help_text="min/km", blank=True, null=True)
    num_laps = models.IntegerField()
    serial_number = models.CharField(max_length=255)
    sport = models.CharField(max_length=255)
    start_position_lat = models.FloatField(help_text="deg", blank=True, null=True)
    start_position_long = models.FloatField(help_text="deg", blank=True, null=True)
    start_time = models.DateTimeField()
    timestamp = models.DateTimeField()
    total_ascent = models.IntegerField(help_text="m", blank=True, null=True)
    total_calories = models.IntegerField(help_text="kcal", blank=True, null=True)
    total_descent = models.IntegerField(help_text="m", blank=True, null=True)
    total_distance = models.FloatField(help_text="m", blank=True, null=True)
    total_elapsed_time = models.FloatField(help_text="s")
    total_timer_time = models.FloatField(help_text="s")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('serial_number', 'timestamp', 'user'),)
        ordering = ("-start_time",)

    def __str__(self):
        return "{} {}".format(self.pk, self.start_time)

    def formatted_distance(self):
        km = self.total_distance/1000
        return "{0:.2f} km".format(km) if km else "No GPS"

    def formatted_avg_speed(self):
        return format_speed(self.avg_speed)

    def formatted_max_speed(self):
        return format_speed(self.max_speed)

    def formatted_total_time(self):
        return format_time(self.total_timer_time)

    def get_absolute_url(self):
        return reverse('activity', args=[str(self.id)])


class Lap(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="laps")
    lap_nr = models.IntegerField()
    avg_heart_rate = models.FloatField(help_text="bmp", blank=True, null=True)
    avg_heart_rate_clock = models.IntegerField(help_text="bmp", blank=True, null=True)
    avg_speed = models.FloatField(help_text="min/km", blank=True, null=True)
    end_position_lat = models.FloatField(help_text="deg", blank=True, null=True)
    end_position_long = models.FloatField(help_text="deg", blank=True, null=True)
    end_time = models.DateTimeField()
    lap_trigger = models.CharField(max_length=255)
    max_heart_rate = models.IntegerField(help_text="bmp", blank=True, null=True)
    max_heart_rate_clock = models.IntegerField(help_text="bmp", blank=True, null=True)
    max_speed = models.FloatField(help_text="min/km", blank=True, null=True)
    start_position_lat = models.FloatField(help_text="deg", blank=True, null=True)
    start_position_long = models.FloatField(help_text="deg", blank=True, null=True)
    start_time = models.DateTimeField()
    timestamp = models.DateTimeField()
    total_ascent = models.IntegerField(help_text="m", blank=True, null=True)
    total_calories = models.IntegerField(help_text="kcal", blank=True, null=True)
    total_descent = models.IntegerField(help_text="m", blank=True, null=True)
    total_distance = models.FloatField(help_text="m", blank=True, null=True)
    total_elapsed_time = models.FloatField(help_text="s", blank=True, null=True)
    total_timer_time = models.FloatField(help_text="s", blank=True, null=True)

    class Meta:
        ordering = ("activity", "lap_nr",)

    def __str__(self):
        return "{} {} {}".format(self.activity_id, self.lap_nr, self.start_time)

    def formatted_distance(self):
        km = self.total_distance/1000
        return "{0:.2f} km".format(km) if km else "No GPS"

    def formatted_avg_speed(self):
        return format_speed(self.avg_speed)

    def formatted_max_speed(self):
        return format_speed(self.max_speed)

    def formatted_total_time(self):
        return format_time(self.total_timer_time)

    def lap_time_start(self):
        activity_start = self.start_time - self.activity.start_time
        return format_time(activity_start.seconds)


class DataPoint(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="data")
    altitude = models.FloatField(help_text="m", blank=True, null=True)
    distance = models.FloatField(help_text="m", blank=True, null=True)
    heart_rate = models.IntegerField(help_text="bpm", blank=True, null=True)
    position_lat = models.FloatField(help_text="deg", blank=True, null=True)
    position_long = models.FloatField(help_text="deg", blank=True, null=True)
    speed = models.FloatField(help_text="min/km", blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ("timestamp",)

    def __str__(self):
        return "{} {}".format(self.activity_id, self.timestamp)
