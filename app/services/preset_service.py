from app.models import Workout


class PresetService:
    PRESETS = {
        "push-day": {
            "name": "Push Day",
            "description": "Chest, shoulders, and triceps focused workout.",
            "items": [
                {"workout_name": "Bench Press", "sets": 4, "reps": 8, "notes": "Focus on controlled reps and proper bar path."},
                {"workout_name": "Push Up", "sets": 3, "reps": 15, "notes": "Bodyweight finisher."},
                {"workout_name": "Tricep Pushdowns", "sets": 3, "reps": 12, "notes": "Full lockout on each rep."},
                {"workout_name": "Bicep Curls", "sets": 3, "reps": 10, "notes": "Optional arm finisher."},
            ],
        },
        "pull-day": {
            "name": "Pull Day",
            "description": "Back and biceps focused workout.",
            "items": [
                {"workout_name": "Pull Ups", "sets": 4, "reps": 8, "notes": "Use assistance if needed."},
                {"workout_name": "Lat Pullovers", "sets": 3, "reps": 12, "notes": "Stretch and squeeze the lats."},
                {"workout_name": "Deadlifts", "sets": 4, "reps": 5, "notes": "Keep a neutral spine throughout."},
                {"workout_name": "Bicep Curls", "sets": 3, "reps": 12, "notes": "Slow eccentric for more control."},
            ],
        },
        "leg-day": {
            "name": "Leg Day",
            "description": "Lower body workout focused on quads, glutes, and hamstrings.",
            "items": [
                {"workout_name": "Squat", "sets": 4, "reps": 8, "notes": "Main compound lift."},
                {"workout_name": "Bulgarian Split Squats", "sets": 3, "reps": 10, "notes": "Each leg."},
                {"workout_name": "Lunges", "sets": 3, "reps": 12, "notes": "Drive through the front heel."},
                {"workout_name": "Hamstring Curls", "sets": 3, "reps": 12, "notes": "Pause at the squeeze."},
                {"workout_name": "Pistol Squats", "sets": 2, "reps": 6, "notes": "Advanced movement, use support if needed."},
            ],
        },
    }

    def get_all_presets(self):
        presets = []
        for slug, preset in self.PRESETS.items():
            presets.append(
                {
                    "slug": slug,
                    "name": preset["name"],
                    "description": preset["description"],
                    "exercise_count": len(preset["items"]),
                    "items": preset["items"],
                }
            )
        return presets

    def get_preset(self, slug: str):
        preset = self.PRESETS.get(slug)
        if not preset:
            return None

        return {
            "slug": slug,
            "name": preset["name"],
            "description": preset["description"],
            "exercise_count": len(preset["items"]),
            "items": preset["items"],
        }