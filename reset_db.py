import os
import shutil

# PATH SETUP
base_dir = os.getcwd()
db_path = os.path.join(base_dir, 'db.sqlite3')
migration_dir = os.path.join(base_dir, 'store', 'migrations')

print("-" * 30)
print("🛑 STARTING FACTORY RESET...")
print("-" * 30)

# 1. DELETE OLD DATABASE
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("🗑️  Deleted old 'db.sqlite3' file.")
    except Exception as e:
        print(f"⚠️  Error deleting DB: {e}")
else:
    print("ℹ️  No database found (Clean slate).")

# 2. DELETE OLD MIGRATIONS (Clean History)
if os.path.exists(migration_dir):
    for filename in os.listdir(migration_dir):
        # Delete everything except __init__.py and folders
        file_path = os.path.join(migration_dir, filename)
        if filename != "__init__.py" and filename.endswith(".py"):
            try:
                os.remove(file_path)
                print(f"🗑️  Deleted migration file: {filename}")
            except Exception as e:
                print(f"⚠️  Error deleting {filename}: {e}")

# 3. CREATE NEW DATABASE (Auto-Run Commands)
print("-" * 30)
print("⚙️  BUILDING NEW DATABASE...")
print("-" * 30)

# Run Makemigrations
exit_code1 = os.system("python manage.py makemigrations")
if exit_code1 == 0:
    print("✅ Migrations created successfully.")
else:
    print("❌ Error creating migrations.")

# Run Migrate
exit_code2 = os.system("python manage.py migrate")
if exit_code2 == 0:
    print("✅ Tables created successfully.")
else:
    print("❌ Error building tables.")

print("-" * 30)
print("🚀 RESET COMPLETE! Database is Brand New.")
print("-" * 30)