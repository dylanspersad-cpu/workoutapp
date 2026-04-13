import typer
from sqlmodel import select

from app.database import get_cli_session, create_db_and_tables, drop_all
from app.models import User, Workout, Routine, RoutineWorkout
from app.utilities.security import encrypt_password

cli = typer.Typer()


@cli.command()
def initialize():
    with get_cli_session() as db:
        drop_all()
        create_db_and_tables()

        # Create required assessment user
        bob = User(
            username="bob",
            email="bob@mail.com",
            password=encrypt_password("bobpass"),
            role="regular_user"
        )
        db.add(bob)
        db.commit()
        db.refresh(bob)

        # Seed workouts
        workouts = [
            Workout(
                name="Pull Ups",
                category="Strength",
                target_muscle="Lats + Upper Back + Biceps + Rear Delts",
                equipment="Pull up bar",
                difficulty="Intermediate",
                instructions="Pull your body upward until your chin clears the bar, then lower with control.",
                duration_minutes=0,
                image_filename="pullups.png",
                youtube_url="https://www.youtube.com/watch?v=eGo4IYlbE5g",
            ),
            Workout(
                name="Bench Press",
                category="Strength",
                target_muscle="Chest + Front Delts + Triceps",
                equipment="Bench press",
                difficulty="Beginner",
                instructions="Lower the bar to your chest with control, then press it back up.",
                duration_minutes=0,
                image_filename="bench_press.png",
                youtube_url="https://www.youtube.com/watch?v=4Y2ZdHCOXok",
            ),
            Workout(
                name="Bicep Curls",
                category="Strength",
                target_muscle="Biceps + Forearms",
                equipment="Dumbbell (recommended)",
                difficulty="Beginner",
                instructions="Curl the weight upward by bending the elbow, then lower slowly.",
                duration_minutes=0,
                image_filename="bicep_curl.jpg",
                youtube_url="https://www.youtube.com/watch?v=XE_pHwbst04",
            ),
            Workout(
                name="Tricep Pushdowns",
                category="Strength",
                target_muscle="Triceps",
                equipment="Cable machine",
                difficulty="Beginner",
                instructions="Push the cable handle down until your arms are straight, then return slowly.",
                duration_minutes=0,
                image_filename="tricep_pushdown.jpg",
                youtube_url="https://www.youtube.com/watch?v=_w-HpW70nSQ",
            ),
            Workout(
                name="Bulgarian Split Squats",
                category="Strength",
                target_muscle="Quads + Glutes + Hamstrings",
                equipment="Bodyweight/Dumbbells",
                difficulty="Intermediate",
                instructions="Place one foot behind you on a bench, lower into a split squat, then rise.",
                duration_minutes=0,
                image_filename="bulgarian_split_squats.jpg",
                youtube_url="https://www.youtube.com/watch?v=VPhhE6bBzZE",
            ),
            Workout(
                name="Hamstring Curls",
                category="Strength",
                target_muscle="Hamstrings",
                equipment="Hamstring curl machine",
                difficulty="Beginner",
                instructions="Curl the pad toward your glutes, then lower with control.",
                duration_minutes=0,
                image_filename="hamstring_curls.jpg",
                youtube_url="https://www.youtube.com/watch?v=XMI4HDLZMf0",
            ),
            Workout(
                name="Lat Pullovers",
                category="Strength",
                target_muscle="Lats + Chest + Serratus Anterior",
                equipment="Cable machine",
                difficulty="Beginner",
                instructions="Pull the handle down in an arc while keeping arms mostly straight.",
                duration_minutes=0,
                image_filename="lat_pullover.jpg",
                youtube_url="https://www.youtube.com/watch?v=2aWk3hF2tVg"
            ),
            Workout(
                name="Pistol Squats",
                category="Strength",
                target_muscle="Quads + Glutes + Core + Hamstrings",
                equipment="Bodyweight/Dumbbells",
                difficulty="Advanced",
                instructions="Lower into a single-leg squat while extending the other leg forward, then stand up.",
                duration_minutes=0,
                image_filename="pistol_squats.jpg",
                youtube_url="https://www.youtube.com/watch?v=vq5-vdgJc0I"
            ),
            Workout(
                name="Cable Crunch",
                category="Core",
                target_muscle="Abs + Hip Flexors",
                equipment="Cable machine",
                difficulty="Beginner",
                instructions="Crunch downward against the cable resistance while keeping hips stable.",
                duration_minutes=0,
                image_filename="cable_crunch.jpg",
                youtube_url="https://www.youtube.com/watch?v=0KEP6A1deBE"
            ),
            Workout(
                name="Deadlifts",
                category="Strength",
                target_muscle="Glutes + Hamstrings + Lower Back + Core + Traps",
                equipment="Barbell",
                difficulty="Intermediate",
                instructions="Lift the bar from the floor by driving through your legs and extending your hips.",
                duration_minutes=0,
                image_filename="deadlift.png",
                youtube_url="https://www.youtube.com/watch?v=XxWcirHIwVo",
            ),
            Workout(
                name="Burpees",
                category="Strength/Cardio",
                target_muscle="Chest + Shoulders + Triceps + Quads + Glutes + Core",
                equipment="None",
                difficulty="Intermediate",
                instructions="Drop into a squat, kick back into plank, perform the movement, then jump upward.",
                duration_minutes=4,
                image_filename="burpees.png",
                youtube_url="https://www.youtube.com/watch?v=qLBImHhCXSw",
            ),
            Workout(
                name="Jumping Jacks",
                category="Cardio",
                target_muscle="Full Body + Shoulders + Calves",
                equipment="None",
                difficulty="Beginner",
                instructions="Jump feet apart while raising arms overhead, then return.",
                duration_minutes=4,
                image_filename="jumping_jacks.png",
                youtube_url="https://www.youtube.com/watch?v=c4DAnQ6DtF8",
            ),
            Workout(
                name="Lunges",
                category="Strength",
                target_muscle="Quads + Glutes + Hamstrings + Calves",
                equipment="Bodyweight",
                difficulty="Intermediate",
                instructions="Step forward, lower until both knees bend, then return.",
                duration_minutes=0,
                image_filename="lunges.jpg",
                youtube_url="https://www.youtube.com/watch?v=ASdqJoDPMHA",
            ),
            Workout(
                name="Mountain Climbers",
                category="Cardio",
                target_muscle="Core + Shoulders + Hip Flexors",
                equipment="None",
                difficulty="Intermediate",
                instructions="From plank position, drive knees toward chest one at a time quickly.",
                duration_minutes=4,
                image_filename="mountain_climber.jpg",
                youtube_url="https://www.youtube.com/watch?v=cnyTQDSE884",
            ),
            Workout(
                name="Plank",
                category="Core",
                target_muscle="Abs + Obliques + Lower Back + Shoulders",
                equipment="Bodyweight",
                difficulty="Beginner",
                instructions="Hold a forearm plank with a straight back and tight core.",
                duration_minutes=0,
                image_filename="plank.png",
                youtube_url="https://www.youtube.com/watch?v=A2b2EmIg0dA",
            ),
            Workout(
                name="Push Up",
                category="Strength",
                target_muscle="Chest + Triceps + Front Delts + Core",
                equipment="Bodyweight",
                difficulty="Beginner",
                instructions="Start in a plank position, lower your body, then push back up.",
                duration_minutes=0,
                image_filename="pushups.png",
                youtube_url="https://www.youtube.com/watch?v=i9sTjhN4Z3M",
            ),
            Workout(
                name="Squat",
                category="Strength",
                target_muscle="Quads + Glutes + Hamstrings + Core",
                equipment="Bodyweight",
                difficulty="Beginner",
                instructions="Stand with feet shoulder-width apart, lower hips, then stand back up.",
                duration_minutes=0,
                image_filename="squat.png",
                youtube_url="https://www.youtube.com/watch?v=gcNh17Ckjgg",
            ),
            Workout(
                name="Shrugs",
                category="Strength",
                target_muscle="Traps + Upper Back",
                equipment="Dumbbells",
                difficulty="Beginner",
                instructions="Stand with dumbbells at your sides and lift them up toward your shoulders.",
                duration_minutes=0,
                image_filename="shrugs.jpg",
                youtube_url="https://www.youtube.com/watch?v=5j2t9sXoQh8",
            )
        ]

        for workout in workouts:
            db.add(workout)
        db.commit()

                # Preset routines for Bob
        push_day = Routine(
            user_id=bob.id,
            name="Push Day",
            description="Chest, shoulders, and triceps focused workout.",
        )
        pull_day = Routine(
            user_id=bob.id,
            name="Pull Day",
            description="Back and biceps focused workout.",
        )
        leg_day = Routine(
            user_id=bob.id,
            name="Leg Day",
            description="Lower body workout focused on quads, glutes, and hamstrings.",
        )

        db.add(push_day)
        db.add(pull_day)
        db.add(leg_day)
        db.commit()
        db.refresh(push_day)
        db.refresh(pull_day)
        db.refresh(leg_day)

        # Get workouts by name
        bench_press = db.exec(select(Workout).where(Workout.name == "Bench Press")).one()
        push_up = db.exec(select(Workout).where(Workout.name == "Push Up")).one()
        tricep_pushdowns = db.exec(select(Workout).where(Workout.name == "Tricep Pushdowns")).one()
        bicep_curls = db.exec(select(Workout).where(Workout.name == "Bicep Curls")).one()

        pull_ups = db.exec(select(Workout).where(Workout.name == "Pull Ups")).one()
        lat_pullovers = db.exec(select(Workout).where(Workout.name == "Lat Pullovers")).one()
        deadlifts = db.exec(select(Workout).where(Workout.name == "Deadlifts")).one()

        squat = db.exec(select(Workout).where(Workout.name == "Squat")).one()
        bulgarian_split_squats = db.exec(select(Workout).where(Workout.name == "Bulgarian Split Squats")).one()
        lunges = db.exec(select(Workout).where(Workout.name == "Lunges")).one()
        hamstring_curls = db.exec(select(Workout).where(Workout.name == "Hamstring Curls")).one()
        pistol_squats = db.exec(select(Workout).where(Workout.name == "Pistol Squats")).one()

        preset_items = [
            # Push Day
            RoutineWorkout(
                routine_id=push_day.id,
                workout_id=bench_press.id,
                order_index=1,
                sets=4,
                reps=8,
                notes="Focus on controlled reps and proper bar path.",
            ),
            RoutineWorkout(
                routine_id=push_day.id,
                workout_id=push_up.id,
                order_index=2,
                sets=3,
                reps=15,
                notes="Bodyweight finisher.",
            ),
            RoutineWorkout(
                routine_id=push_day.id,
                workout_id=tricep_pushdowns.id,
                order_index=3,
                sets=3,
                reps=12,
                notes="Full lockout on each rep.",
            ),
            RoutineWorkout(
                routine_id=push_day.id,
                workout_id=bicep_curls.id,
                order_index=4,
                sets=3,
                reps=10,
                notes="Optional arm finisher.",
            ),

            # Pull Day
            RoutineWorkout(
                routine_id=pull_day.id,
                workout_id=pull_ups.id,
                order_index=1,
                sets=4,
                reps=8,
                notes="Use assistance if needed.",
            ),
            RoutineWorkout(
                routine_id=pull_day.id,
                workout_id=lat_pullovers.id,
                order_index=2,
                sets=3,
                reps=12,
                notes="Stretch and squeeze the lats.",
            ),
            RoutineWorkout(
                routine_id=pull_day.id,
                workout_id=deadlifts.id,
                order_index=3,
                sets=4,
                reps=5,
                notes="Keep a neutral spine throughout.",
            ),
            RoutineWorkout(
                routine_id=pull_day.id,
                workout_id=bicep_curls.id,
                order_index=4,
                sets=3,
                reps=12,
                notes="Slow eccentric for more control.",
            ),

            # Leg Day
            RoutineWorkout(
                routine_id=leg_day.id,
                workout_id=squat.id,
                order_index=1,
                sets=4,
                reps=8,
                notes="Main compound lift.",
            ),
            RoutineWorkout(
                routine_id=leg_day.id,
                workout_id=bulgarian_split_squats.id,
                order_index=2,
                sets=3,
                reps=10,
                notes="Each leg.",
            ),
            RoutineWorkout(
                routine_id=leg_day.id,
                workout_id=lunges.id,
                order_index=3,
                sets=3,
                reps=12,
                notes="Drive through the front heel.",
            ),
            RoutineWorkout(
                routine_id=leg_day.id,
                workout_id=hamstring_curls.id,
                order_index=4,
                sets=3,
                reps=12,
                notes="Pause at the squeeze.",
            ),
            RoutineWorkout(
                routine_id=leg_day.id,
                workout_id=pistol_squats.id,
                order_index=5,
                sets=2,
                reps=6,
                notes="Advanced movement, use support if needed.",
            ),
        ]

        for item in preset_items:
            db.add(item)
        db.commit()

        # Optional starter routine for bob
        starter_routine = Routine(
            user_id=bob.id,
            name="Bob Starter Routine",
            description="A simple starter routine for testing.",
        )
        db.add(starter_routine)
        db.commit()
        db.refresh(starter_routine)

        push_up = db.exec(select(Workout).where(Workout.name == "Push Up")).one()
        squat = db.exec(select(Workout).where(Workout.name == "Squat")).one()
        plank = db.exec(select(Workout).where(Workout.name == "Plank")).one()

        routine_items = [
            RoutineWorkout(
                routine_id=starter_routine.id,
                workout_id=push_up.id,
                order_index=1,
                sets=3,
                reps=12,
                duration_seconds=None,
                notes="Keep elbows tucked.",
            ),
            RoutineWorkout(
                routine_id=starter_routine.id,
                workout_id=squat.id,
                order_index=2,
                sets=3,
                reps=15,
                duration_seconds=None,
                notes="Keep chest up.",
            ),
            RoutineWorkout(
                routine_id=starter_routine.id,
                workout_id=plank.id,
                order_index=3,
                sets=2,
                reps=None,
                duration_seconds=45,
                notes="Tighten core.",
            ),
        ]

        for item in routine_items:
            db.add(item)
        db.commit()

        print("Database initialized successfully.")


@cli.command()
def get_all_users():
    with get_cli_session() as db:
        users = db.exec(select(User)).all()
        if not users:
            print("No users found")
            return
        for user in users:
            print(user)


@cli.command()
def get_all_workouts():
    with get_cli_session() as db:
        workouts = db.exec(select(Workout)).all()
        if not workouts:
            print("No workouts found")
            return
        for workout in workouts:
            print(workout)


@cli.command()
def get_user_routines(username: str):
    with get_cli_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User not found")
            return

        routines = db.exec(select(Routine).where(Routine.user_id == user.id)).all()
        if not routines:
            print("No routines found for user")
            return

        for routine in routines:
            print(routine)


@cli.command()
def add_routine(username: str, name: str, description: str = ""):
    with get_cli_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User not found")
            return

        routine = Routine(user_id=user.id, name=name, description=description)
        db.add(routine)
        db.commit()
        db.refresh(routine)
        print(f"Routine created: {routine}")


@cli.command()
def add_workout_to_routine(username: str, routine_id: int, workout_id: int, sets: int = 3, reps: int = 10):
    with get_cli_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User not found")
            return

        routine = db.exec(
            select(Routine).where(Routine.id == routine_id, Routine.user_id == user.id)
        ).one_or_none()
        if not routine:
            print("Routine not found for user")
            return

        workout = db.get(Workout, workout_id)
        if not workout:
            print("Workout not found")
            return

        existing_items = db.exec(
            select(RoutineWorkout).where(RoutineWorkout.routine_id == routine.id)
        ).all()
        next_order = len(existing_items) + 1

        item = RoutineWorkout(
            routine_id=routine.id,
            workout_id=workout.id,
            order_index=next_order,
            sets=sets,
            reps=reps,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        print(f"Workout added to routine: {item}")


if __name__ == "__main__":
    cli()