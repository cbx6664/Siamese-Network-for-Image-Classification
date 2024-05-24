import os

count = 0
for root, dirs, files in os.walk(r"train_set/old_d0"):
    for file in files:
        if file == 'Thumbs.db':
            count+=1
            os.remove(os.path.join(root, file))

print(f"Removed {count} Thumbs.db files")