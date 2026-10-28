from file_organizer import organize_files
from analyzer import analyze_folder
from analytics import create_dataframe, show_analysis
from visualizer import create_bar_chart


print("==============================")
print("          FILEFLOW")
print(" Intelligent File Organizer")
print("==============================")


folder = input("\nEnter the folder path to organize: ")

organize_files(folder)


print("\n📊 FILE ANALYSIS")
print("==============================")

total_files, categories = analyze_folder(folder)

print(f"Total Files: {total_files}")

for category, count in categories.items():
    print(f"{category}: {count}")


# Create Pandas DataFrame
df = create_dataframe(categories)

# Show Pandas analysis
show_analysis(df)

# Create file category chart
create_bar_chart(df)