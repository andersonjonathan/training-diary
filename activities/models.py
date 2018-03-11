from django.db import models


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

    class Meta:
        unique_together = (('serial_number', 'timestamp'),)

    def __str__(self):
        return "{} {}".format(self.pk, self.start_time)


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

    def __str__(self):
        return "{} {} {}".format(self.activity_id, self.lap_nr, self.start_time)


class DataPoint(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="data")
    altitude = models.FloatField(help_text="m", blank=True, null=True)
    distance = models.FloatField(help_text="m", blank=True, null=True)
    heart_rate = models.IntegerField(help_text="bpm", blank=True, null=True)
    position_lat = models.FloatField(help_text="deg", blank=True, null=True)
    position_long = models.FloatField(help_text="deg", blank=True, null=True)
    speed = models.FloatField(help_text="min/km", blank=True, null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return "{} {}".format(self.activity_id, self.timestamp)
