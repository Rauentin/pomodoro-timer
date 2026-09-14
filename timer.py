# pomodoro timer logic
class PomodoroTimer:
    def __init__(self, work_minutes=25, break_minutes=5):
        self.work_time = work_minutes * 60   # seconds
        self.break_time = break_minutes * 60  # seconds
        self.time_left = self.work_time
        self.is_work = True
        self.running = False

    def tick(self):
        """Decrease timer by 1 second. Returns 'work' or 'break' when a period ends."""
        if self.running and self.time_left > 0:
            self.time_left -= 1
            if self.time_left == 0:
                return self.switch_period()
        return None

    def switch_period(self):
        """Switch between work and break. Returns the new period name."""
        self.is_work = not self.is_work
        if self.is_work:
            self.time_left = self.work_time
            return "work"
        else:
            self.time_left = self.break_time
            return "break"

    def toggle_pause(self):
        """Pause or resume the countdown. Returns True if now running."""
        self.running = not self.running
        return self.running

    def reset(self):
        self.running = False
        self.is_work = True
        self.time_left = self.work_time

    def get_time_display(self):
        """Return time as MM:SS string"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes:02d}:{seconds:02d}"
