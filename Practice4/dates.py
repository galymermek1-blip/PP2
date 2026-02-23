from datetime import datetime, timedelta

# 1. Subtract five days from current date
current = datetime.now()
five_days_ago = current - timedelta(days=5)
print("Current date:", current.strftime("%Y-%m-%d"))
print("Five days ago:", five_days_ago.strftime("%Y-%m-%d"))
print()

# 2. Print yesterday, today, tomorrow
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:", today.strftime("%Y-%m-%d"))
print("Tomorrow:", tomorrow.strftime("%Y-%m-%d"))
print()

# 3. Drop microseconds from datetime
now = datetime.now()
print("With microseconds:", now)
print("Without microseconds:", now.replace(microsecond=0))
print()

# 4. Calculate two date difference in seconds
date1 = datetime(2024, 2, 20, 10, 0, 0)
date2 = datetime(2024, 2, 25, 15, 30, 0)

difference = date2 - date1
print("Date1:", date1)
print("Date2:", date2)
print("Difference in seconds:", difference.total_seconds())