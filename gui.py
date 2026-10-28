
import tkinter as tk
from tkinter import filedialog, messagebox

from file_manager import FileManager
from analytics import create_dataframe, check_missing_values
from visualizer import create_bar_chart
from seaborn_visualizer import create_seaborn_chart
from plotly_visualizer import create_plotly_chart
from numpy_analyzer import analyze_with_numpy
from functional_analysis import functional_analysis


def start_gui():
    window = tk.Tk()
    window.title("FileFlow - Intelligent File Organizer")
    window.geometry("750x800")
    window.minsize(550, 450)

    selected_folder = ""
    current_categories = {}

    # ---------- Scrollable Window ----------

    outer_frame = tk.Frame(window)
    outer_frame.pack(fill="both", expand=True)

    page_canvas = tk.Canvas(
        outer_frame,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        outer_frame,
        orient="vertical",
        command=page_canvas.yview
    )

    page_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    page_canvas.pack(side="left", fill="both", expand=True)

    content_frame = tk.Frame(page_canvas)

    canvas_window = page_canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw"
    )

    def update_scroll_region(event=None):
        page_canvas.configure(
            scrollregion=page_canvas.bbox("all")
        )

    def resize_content(event):
        page_canvas.itemconfigure(
            canvas_window,
            width=event.width
        )
        update_scroll_region()

    content_frame.bind("<Configure>", update_scroll_region)
    page_canvas.bind("<Configure>", resize_content)

    # ---------- Touchpad and Mouse Wheel ----------

    def scroll_with_wheel(event):
        delta = getattr(event, "delta", 0)

        if delta:
            if abs(delta) >= 120:
                units = int(-delta / 120)
            else:
                # Small events from precision touchpads
                units = -1 if delta > 0 else 1

            page_canvas.yview_scroll(units, "units")

        return "break"

    def scroll_up(event):
        page_canvas.yview_scroll(-1, "units")
        return "break"

    def scroll_down(event):
        page_canvas.yview_scroll(1, "units")
        return "break"

    # Custom binding tag to catch scrolling before widget handlers.
    def add_scroll_tag(widget):
        tags = list(widget.bindtags())

        if "FileFlowScroll" not in tags:
            tags.insert(0, "FileFlowScroll")
            widget.bindtags(tuple(tags))

        for child in widget.winfo_children():
            add_scroll_tag(child)

    window.bind_class(
        "FileFlowScroll",
        "<MouseWheel>",
        scroll_with_wheel
    )
    window.bind_class(
        "FileFlowScroll",
        "<Button-4>",
        scroll_up
    )
    window.bind_class(
        "FileFlowScroll",
        "<Button-5>",
        scroll_down
    )

    # Keep global wheel bindings as a fallback.
    window.bind_all("<MouseWheel>", scroll_with_wheel, add="+")
    window.bind_all("<Button-4>", scroll_up, add="+")
    window.bind_all("<Button-5>", scroll_down, add="+")

    # Keyboard scrolling
    window.bind_all(
        "<Up>",
        lambda event: (
            page_canvas.yview_scroll(-1, "units"),
            "break"
        )[1],
        add="+"
    )
    window.bind_all(
        "<Down>",
        lambda event: (
            page_canvas.yview_scroll(1, "units"),
            "break"
        )[1],
        add="+"
    )
    window.bind_all(
        "<Prior>",
        lambda event: (
            page_canvas.yview_scroll(-1, "pages"),
            "break"
        )[1],
        add="+"
    )
    window.bind_all(
        "<Next>",
        lambda event: (
            page_canvas.yview_scroll(1, "pages"),
            "break"
        )[1],
        add="+"
    )

    # ---------- Folder Selection ----------

    def select_folder():
        nonlocal selected_folder

        folder = filedialog.askdirectory()

        if folder:
            selected_folder = folder
            folder_label.config(
                text=f"Selected Folder:\n{folder}"
            )

    # ---------- Organize Files ----------

    def organize():
        nonlocal current_categories

        if not selected_folder:
            messagebox.showwarning(
                "No Folder",
                "Please select a folder first."
            )
            return

        try:
            manager = FileManager(selected_folder)
            manager.organize()

            total_files, categories = manager.analyze()
            current_categories = categories

            total_label.config(text=f"Total Files\n{total_files}")
            images_label.config(
                text=f"Images\n{categories.get('Images', 0)}"
            )
            documents_label.config(
                text=f"Documents\n{categories.get('Documents', 0)}"
            )
            videos_label.config(
                text=f"Videos\n{categories.get('Videos', 0)}"
            )
            music_label.config(
                text=f"Music\n{categories.get('Music', 0)}"
            )
            code_label.config(
                text=f"Code\n{categories.get('Code', 0)}"
            )

            create_bar_chart(create_dataframe(categories))

            messagebox.showinfo(
                "FileFlow",
                "Files organized and analyzed successfully!"
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Something went wrong:\n\n{error}"
            )

    # ---------- Detailed Analysis ----------

    def view_analysis():
        if not current_categories:
            messagebox.showwarning(
                "No Analysis",
                "Please organize files first."
            )
            return

        result_window = tk.Toplevel(window)
        result_window.title("FileFlow - Detailed Analysis")
        result_window.geometry("450x450")

        tk.Label(
            result_window,
            text="DETAILED FILE ANALYSIS",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            result_window,
            text=f"Total Files: {sum(current_categories.values())}",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        for category, count in current_categories.items():
            tk.Label(
                result_window,
                text=f"{category}: {count} files",
                font=("Arial", 12)
            ).pack(pady=5)

        tk.Button(
            result_window,
            text="Close",
            width=15,
            command=result_window.destroy
        ).pack(pady=20)

    # ---------- NumPy Analysis ----------

    def show_numpy_analysis():
        if not current_categories:
            messagebox.showwarning(
                "No Analysis",
                "Please organize files first."
            )
            return

        results = analyze_with_numpy(current_categories)

        result_window = tk.Toplevel(window)
        result_window.title("FileFlow - NumPy Analysis")
        result_window.geometry("500x400")

        tk.Label(
            result_window,
            text="NUMPY FILE ANALYSIS",
            font=("Arial", 18, "bold")
        ).pack(pady=25)

        tk.Label(
            result_window,
            text=f"Total Files: {results['Total Files']}",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        tk.Label(
            result_window,
            text=(
                "Average Files per Category: "
                f"{results['Average Files per Category']:.2f}"
            ),
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Label(
            result_window,
            text=(
                "Maximum Files in a Category: "
                f"{results['Maximum Files in a Category']}"
            ),
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Label(
            result_window,
            text=(
                "Minimum Files in a Category: "
                f"{results['Minimum Files in a Category']}"
            ),
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(
            result_window,
            text="Close",
            width=15,
            command=result_window.destroy
        ).pack(pady=20)

    # ---------- Pandas Missing Values ----------

    def show_missing_values():
        if not current_categories:
            messagebox.showwarning(
                "No Analysis",
                "Please organize files first."
            )
            return

        df = create_dataframe(current_categories)
        missing_values = check_missing_values(df)

        result_window = tk.Toplevel(window)
        result_window.title("FileFlow - Missing Values")
        result_window.geometry("500x400")

        tk.Label(
            result_window,
            text="PANDAS MISSING VALUES",
            font=("Arial", 18, "bold")
        ).pack(pady=25)

        for column, count in missing_values.items():
            tk.Label(
                result_window,
                text=f"{column}: {count} missing values",
                font=("Arial", 12)
            ).pack(pady=10)

        total_missing = missing_values.sum()

        if total_missing == 0:
            status = "DataFrame is clean - No missing values!"
        else:
            status = f"Total Missing Values: {total_missing}"

        tk.Label(
            result_window,
            text=status,
            font=("Arial", 12, "bold")
        ).pack(pady=20)

        tk.Button(
            result_window,
            text="Close",
            width=15,
            command=result_window.destroy
        ).pack(pady=15)

    # ---------- Matplotlib Chart ----------

    def show_matplotlib_chart():
        if not current_categories:
            messagebox.showwarning(
                "No Analysis",
                "Please organize files first."
            )
            return

        create_bar_chart(create_dataframe(current_categories))

    # ---------- Seaborn Chart ----------

    def show_seaborn_chart():
        if not current_categories:
            messagebox.showwarning(
                "No Analysis",
                "Please organize files first."
            )
            return

        create_seaborn_chart(create_dataframe(current_categories))

    # ---------- Plotly Chart ----------

    def show_plotly_chart():
        if not current_categories:
            messagebox.showwarning(
                "No Analysis",
                "Please organize files first."
            )
            return

        create_plotly_chart(create_dataframe(current_categories))

    # ---------- Functional Programming ----------

    def show_functional_analysis():
        if not current_categories:
            messagebox.showwarning(
                "No Analysis",
                "Please organize files first."
            )
            return

        results = functional_analysis(current_categories)

        result_window = tk.Toplevel(window)
        result_window.title("FileFlow - Functional Analysis")
        result_window.geometry("550x500")

        tk.Label(
            result_window,
            text="FUNCTIONAL PROGRAMMING ANALYSIS",
            font=("Arial", 17, "bold")
        ).pack(pady=20)

        tk.Label(
            result_window,
            text=f"Total Files: {results['Total Files']}",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        highest = results["Highest Category"]

        tk.Label(
            result_window,
            text=f"Highest Category: {highest[0]} ({highest[1]} files)",
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Label(
            result_window,
            text=f"Doubled Counts: {results['Doubled Counts']}",
            font=("Arial", 11)
        ).pack(pady=10)

        tk.Label(
            result_window,
            text=f"Non-Zero Counts: {results['Non Zero Counts']}",
            font=("Arial", 11)
        ).pack(pady=10)

        tk.Label(
            result_window,
            text="Concepts: lambda, map(), filter(), reduce()",
            font=("Arial", 11)
        ).pack(pady=15)

        tk.Button(
            result_window,
            text="Close",
            width=15,
            command=result_window.destroy
        ).pack(pady=20)

    # ---------- About ----------

    def show_about():
        messagebox.showinfo(
            "About FileFlow",
            "FILEFLOW\n\n"
            "Intelligent File Organizer\n\n"
            "Features:\n"
            "• Automatic File Organization\n"
            "• Pandas and NumPy Analysis\n"
            "• Missing Value Detection\n"
            "• Matplotlib, Seaborn and Plotly\n"
            "• Functional Programming\n"
            "• Tkinter GUI\n\n"
            "Python Mini Project"
        )

    # ---------- Exit ----------

    def exit_application():
        if messagebox.askyesno(
            "Exit FileFlow",
            "Are you sure you want to exit?"
        ):
            window.destroy()

    # ---------- Menu Bar ----------

    menu_bar = tk.Menu(window)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(
        label="Browse Folder",
        command=select_folder
    )
    file_menu.add_command(
        label="Organize Files",
        command=organize
    )
    file_menu.add_separator()
    file_menu.add_command(
        label="Exit",
        command=exit_application
    )
    menu_bar.add_cascade(label="File", menu=file_menu)

    analysis_menu = tk.Menu(menu_bar, tearoff=0)
    analysis_menu.add_command(
        label="View Analysis",
        command=view_analysis
    )
    analysis_menu.add_command(
        label="NumPy Analysis",
        command=show_numpy_analysis
    )
    analysis_menu.add_command(
        label="Missing Values",
        command=show_missing_values
    )
    analysis_menu.add_command(
        label="Matplotlib Chart",
        command=show_matplotlib_chart
    )
    analysis_menu.add_command(
        label="Seaborn Chart",
        command=show_seaborn_chart
    )
    analysis_menu.add_command(
        label="Plotly Chart",
        command=show_plotly_chart
    )
    analysis_menu.add_command(
        label="Functional Analysis",
        command=show_functional_analysis
    )
    menu_bar.add_cascade(label="Analysis", menu=analysis_menu)

    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(
        label="About FileFlow",
        command=show_about
    )
    menu_bar.add_cascade(label="Help", menu=help_menu)

    window.config(menu=menu_bar)

    # ---------- Header ----------

    header_canvas = tk.Canvas(
        content_frame,
        width=700,
        height=130,
        highlightthickness=0
    )
    header_canvas.pack(pady=(20, 10))

    header_canvas.create_rectangle(
        10, 10, 690, 120,
        outline="black",
        width=2
    )

    header_canvas.create_text(
        350, 50,
        text="FILEFLOW",
        font=("Arial", 28, "bold")
    )

    header_canvas.create_text(
        350, 90,
        text="Intelligent File Organizer",
        font=("Arial", 14)
    )

    # ---------- Selected Folder ----------

    folder_label = tk.Label(
        content_frame,
        text="No folder selected",
        font=("Arial", 11),
        wraplength=650
    )
    folder_label.pack(pady=10)

    # ---------- Statistics ----------

    stats_frame = tk.Frame(content_frame)
    stats_frame.pack(pady=15)

    total_label = tk.Label(
        stats_frame,
        text="Total Files\n0",
        font=("Arial", 13, "bold"),
        width=15,
        height=3,
        relief="ridge"
    )
    total_label.grid(row=0, column=0, padx=5)

    images_label = tk.Label(
        stats_frame,
        text="Images\n0",
        font=("Arial", 13, "bold"),
        width=15,
        height=3,
        relief="ridge"
    )
    images_label.grid(row=0, column=1, padx=5)

    documents_label = tk.Label(
        stats_frame,
        text="Documents\n0",
        font=("Arial", 13, "bold"),
        width=15,
        height=3,
        relief="ridge"
    )
    documents_label.grid(row=0, column=2, padx=5)

    second_frame = tk.Frame(content_frame)
    second_frame.pack(pady=10)

    videos_label = tk.Label(
        second_frame,
        text="Videos\n0",
        font=("Arial", 12, "bold"),
        width=15,
        height=3,
        relief="ridge"
    )
    videos_label.grid(row=0, column=0, padx=5)

    music_label = tk.Label(
        second_frame,
        text="Music\n0",
        font=("Arial", 12, "bold"),
        width=15,
        height=3,
        relief="ridge"
    )
    music_label.grid(row=0, column=1, padx=5)

    code_label = tk.Label(
        second_frame,
        text="Code\n0",
        font=("Arial", 12, "bold"),
        width=15,
        height=3,
        relief="ridge"
    )
    code_label.grid(row=0, column=2, padx=5)

    # ---------- All Buttons ----------

    button_specs = [
        ("Browse Folder", select_folder),
        ("Organize Files", organize),
        ("View Analysis", view_analysis),
        ("NumPy Analysis", show_numpy_analysis),
        ("Missing Values", show_missing_values),
        ("Matplotlib Chart", show_matplotlib_chart),
        ("Seaborn Chart", show_seaborn_chart),
        ("Plotly Chart", show_plotly_chart),
        ("Functional Analysis", show_functional_analysis),
        ("About FileFlow", show_about),
        ("Exit", exit_application),
    ]

    buttons = []

    for label, command in button_specs:
        button = tk.Button(
            content_frame,
            text=label,
            font=("Arial", 11, "bold"),
            width=25,
            command=command
        )
        button.pack(pady=5)
        buttons.append(button)

    # ---------- Button Hover ----------

    def mouse_enter(event):
        event.widget.config(relief="sunken")

    def mouse_leave(event):
        event.widget.config(relief="raised")

    for button in buttons:
        button.bind("<Enter>", mouse_enter)
        button.bind("<Leave>", mouse_leave)

    # Apply custom scroll binding to every widget.
    add_scroll_tag(window)

    # ---------- Keyboard Shortcuts ----------

    window.bind(
        "<Control-o>",
        lambda event: select_folder()
    )
    window.bind(
        "<Control-r>",
        lambda event: organize()
    )
    window.bind(
        "<Control-q>",
        lambda event: exit_application()
    )

    window.mainloop()


if __name__ == "__main__":
    start_gui()