from main import assign_students_round_robin, Classroom
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


class StudentRegistrationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Registration System")
        self.root.geometry("800x600")

        # Main data storage
        self.branch = {}
        self.subjects = {}
        self.classrooms = []

        # Class variables that were causing "defined outside __init__" errors
        self.branch_entries = []
        self.subject_entries = []
        self.classroom_entries = []
        self.branch_entries_frame = None
        self.branch_submit_btn = None
        self.subject_entries_frame = None
        self.subject_submit_btn = None
        self.subject_notebook = None
        self.dynamic_frame = None
        self.classroom_entries_frame = None
        self.classroom_submit_btn = None
        self.classroom_notebook = None
        self.results_frame = None
        self.results_text = None

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.branch_tab = ttk.Frame(self.notebook)
        self.subjects_tab = ttk.Frame(self.notebook)
        self.classroom_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.branch_tab, text="Branches")
        self.notebook.add(self.subjects_tab, text="Subjects")
        self.notebook.add(self.classroom_tab, text="Classrooms")
        self.notebook.add(self.results_tab, text="Results")

        # Variable initialization
        self.num_branch_var = tk.StringVar()
        self.subjects_count_var = tk.StringVar()
        self.no_of_classes_var = tk.StringVar()

        # Initialize each tab
        self.setup_branch_tab()
        self.setup_subjects_tab()
        self.setup_classroom_tab()
        self.setup_results_tab()

    def setup_branch_tab(self):
        frame = ttk.LabelFrame(self.branch_tab, text="Add Branches")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Number of branches
        ttk.Label(frame, text="Number of branches:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.num_branch_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Set", command=self.create_branch_entries).grid(row=0, column=2, padx=5, pady=5)

        # Container for dynamic branch entries
        self.branch_entries_frame = ttk.Frame(frame)
        self.branch_entries_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Submit button
        self.branch_submit_btn = ttk.Button(frame, text="Submit Branches", command=self.submit_branches)
        self.branch_submit_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.branch_submit_btn.grid_remove()  # Hide initially

    def create_branch_entries(self):
        # Clear any existing entries
        for widget in self.branch_entries_frame.winfo_children():
            widget.destroy()

        try:
            num_branches = int(self.num_branch_var.get())
            if num_branches <= 0:
                messagebox.showerror("Invalid Input", "Number of branches must be positive.")
                return

            self.branch_entries = []

            # Create headers
            ttk.Label(self.branch_entries_frame, text="Department Name").grid(row=0, column=0, padx=5, pady=5)
            ttk.Label(self.branch_entries_frame, text="Year").grid(row=0, column=1, padx=5, pady=5)
            ttk.Label(self.branch_entries_frame, text="Number of Students").grid(row=0, column=2, padx=5, pady=5)

            # Create entry fields for each branch
            for i in range(num_branches):
                branch_entry = {
                    "name": tk.StringVar(),
                    "year": tk.StringVar(),
                    "students": tk.StringVar()
                }

                ttk.Entry(self.branch_entries_frame, textvariable=branch_entry["name"]).grid(row=i + 1, column=0,
                                                                                             padx=5, pady=5)
                ttk.Entry(self.branch_entries_frame, textvariable=branch_entry["year"]).grid(row=i + 1, column=1,
                                                                                             padx=5, pady=5)
                ttk.Entry(self.branch_entries_frame, textvariable=branch_entry["students"]).grid(row=i + 1, column=2,
                                                                                                 padx=5, pady=5)

                self.branch_entries.append(branch_entry)

            # Show the submit button
            self.branch_submit_btn.grid()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def submit_branches(self):
        # Process branch entries
        self.branch = {}
        for i, entry in enumerate(self.branch_entries):
            try:
                branch_name = entry["name"].get()
                year = int(entry["year"].get())
                no_of_students = int(entry["students"].get())

                # Map department codes according to original code
                dep = ""
                if branch_name == "CS":
                    dep = "CS"
                elif branch_name == "EC":
                    dep = "EC"
                elif branch_name == "CE":
                    dep = "CE"
                elif branch_name == "ME":
                    dep = "ME"
                elif branch_name == "EE":
                    dep = "EE"
                else:
                    messagebox.showerror("Invalid Department", f"Invalid department: {branch_name}")
                    return

                # Generate student IDs
                self.branch[branch_name] = [f"MBC{year}{dep}{g + 1:02d}" for g in range(no_of_students)]

            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter valid numbers for branch {i + 1}")
                return

        # Update the results tab with branch information
        self.update_results()

        # Move to the next tab
        self.notebook.select(1)  # Select the Subject tab
        messagebox.showinfo("Success", "Branches added successfully!")

    def setup_subjects_tab(self):
        frame = ttk.LabelFrame(self.subjects_tab, text="Add Subjects")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Number of subjects
        ttk.Label(frame, text="Number of subjects:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.subjects_count_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Set", command=self.create_subject_entries).grid(row=0, column=2, padx=5, pady=5)

        # Container for dynamic subject entries
        self.subject_entries_frame = ttk.Frame(frame)
        self.subject_entries_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Submit button
        self.subject_submit_btn = ttk.Button(frame, text="Submit Subjects", command=self.submit_subjects)
        self.subject_submit_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.subject_submit_btn.grid_remove()  # Hide initially

    def create_subject_entries(self):
        # Clear any existing entries
        for widget in self.subject_entries_frame.winfo_children():
            widget.destroy()

        try:
            subjects_count = int(self.subjects_count_var.get())
            if subjects_count <= 0:
                messagebox.showerror("Invalid Input", "Number of subjects must be positive.")
                return

            self.subject_entries = []

            # Create a notebook for each subject
            self.subject_notebook = ttk.Notebook(self.subject_entries_frame)
            self.subject_notebook.pack(fill='both', expand=True)

            for i in range(subjects_count):
                subject_frame = ttk.Frame(self.subject_notebook)
                self.subject_notebook.add(subject_frame, text=f"Subject {i + 1}")

                subject_entry = {
                    "name": tk.StringVar(),
                    "selection_type": tk.IntVar(value=1),
                    "branch_selection": tk.StringVar(),
                    "range_start": tk.StringVar(),
                    "range_end": tk.StringVar(),
                    "dynamic_selections": [],
                    "dynamic_frame": None  # Store the frame reference here
                }

                # Subject name
                ttk.Label(subject_frame, text="Subject Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                ttk.Entry(subject_frame, textvariable=subject_entry["name"]).grid(row=0, column=1, padx=5, pady=5,
                                                                                  columnspan=2)

                # Selection type
                ttk.Label(subject_frame, text="Selection Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

                # Using lambda with default arguments to avoid closure issues
                ttk.Radiobutton(subject_frame, text="Whole Branch", variable=subject_entry["selection_type"], value=1,
                                command=lambda s=subject_frame, e=subject_entry: self.toggle_selection_type(s, e,
                                                                                                            1)).grid(
                    row=1, column=1, padx=5, pady=5)
                ttk.Radiobutton(subject_frame, text="Dynamic Selection", variable=subject_entry["selection_type"],
                                value=2,
                                command=lambda s=subject_frame, e=subject_entry: self.toggle_selection_type(s, e,
                                                                                                            2)).grid(
                    row=1, column=2, padx=5, pady=5)

                # Branch selection (for whole branch)
                ttk.Label(subject_frame, text="Branch:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                branch_dropdown = ttk.Combobox(subject_frame, textvariable=subject_entry["branch_selection"])
                branch_dropdown.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
                branch_dropdown['values'] = list(self.branch.keys())

                # Dynamic selection controls
                dynamic_frame = ttk.LabelFrame(subject_frame, text="Dynamic Selection")
                dynamic_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
                dynamic_frame.grid_remove()  # Hide initially

                subject_entry["dynamic_frame"] = dynamic_frame  # Store the reference

                ttk.Label(dynamic_frame, text="Branch:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                dynamic_branch = ttk.Combobox(dynamic_frame, textvariable=subject_entry["branch_selection"])
                dynamic_branch.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
                dynamic_branch['values'] = list(self.branch.keys())

                ttk.Label(dynamic_frame, text="Range Start:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                ttk.Entry(dynamic_frame, textvariable=subject_entry["range_start"]).grid(row=1, column=1, padx=5,
                                                                                         pady=5)

                ttk.Label(dynamic_frame, text="Range End:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                ttk.Entry(dynamic_frame, textvariable=subject_entry["range_end"]).grid(row=2, column=1, padx=5, pady=5)

                # Add dynamic selection button
                ttk.Button(dynamic_frame, text="Add Selection",
                           command=lambda e=subject_entry: self.add_dynamic_selection(e)).grid(row=3, column=0,
                                                                                               columnspan=3, padx=5,
                                                                                               pady=5)

                # Add to entries
                self.subject_entries.append(subject_entry)

            # Show the submit button
            self.subject_submit_btn.grid()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def toggle_selection_type(self, subject_frame, subject_entry, selection_type):
        # Use the stored reference instead of trying to find the widget
        dynamic_frame = subject_entry["dynamic_frame"]

        if selection_type == 1:  # Whole Branch
            dynamic_frame.grid_remove()
        else:  # Dynamic Selection
            dynamic_frame.grid()

    def add_dynamic_selection(self, subject_entry):
        try:
            branch_name = subject_entry["branch_selection"].get()
            range_start = int(subject_entry["range_start"].get())
            range_end = int(subject_entry["range_end"].get())

            if branch_name not in self.branch:
                messagebox.showerror("Invalid Branch", f"Branch {branch_name} does not exist.")
                return

            # Validate range
            if range_start < 1 or range_end > len(self.branch[branch_name]) or range_start > range_end:
                messagebox.showerror("Invalid Range", "Please enter a valid range.")
                return

            # Add selection to the entry
            subject_entry["dynamic_selections"].append((branch_name, range_start, range_end))
            messagebox.showinfo("Success", f"Added students {range_start}-{range_end} from {branch_name}")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for range.")

    def submit_subjects(self):
        # Process subject entries
        self.subjects = {}
        for subject_entry in self.subject_entries:
            subject_name = subject_entry["name"].get()
            selection_type = subject_entry["selection_type"].get()

            if selection_type == 1:  # Whole Branch
                branch_name = subject_entry["branch_selection"].get()
                if branch_name in self.branch:
                    self.subjects[subject_name] = self.branch[branch_name].copy()
                else:
                    messagebox.showerror("Invalid Branch", f"Branch {branch_name} does not exist.")
                    return
            else:  # Dynamic Selection
                student_list = []
                for branch_name, range_start, range_end in subject_entry["dynamic_selections"]:
                    if branch_name in self.branch:
                        student_list.extend(self.branch[branch_name][range_start - 1:range_end])

                self.subjects[subject_name] = student_list

        # Update the results tab with subject information
        self.update_results()

        # Move to the next tab
        self.notebook.select(2)  # Select the Classroom tab
        messagebox.showinfo("Success", "Subjects added successfully!")

    def setup_classroom_tab(self):
        frame = ttk.LabelFrame(self.classroom_tab, text="Add Classrooms")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Number of classrooms
        ttk.Label(frame, text="Number of classrooms:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame, textvariable=self.no_of_classes_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Set", command=self.create_classroom_entries).grid(row=0, column=2, padx=5, pady=5)

        # Container for dynamic classroom entries
        self.classroom_entries_frame = ttk.Frame(frame)
        self.classroom_entries_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Submit button
        self.classroom_submit_btn = ttk.Button(frame, text="Submit Classrooms", command=self.submit_classrooms)
        self.classroom_submit_btn.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.classroom_submit_btn.grid_remove()  # Hide initially

    def create_classroom_entries(self):
        # Clear any existing entries
        for widget in self.classroom_entries_frame.winfo_children():
            widget.destroy()

        try:
            no_of_classes = int(self.no_of_classes_var.get())
            if no_of_classes <= 0:
                messagebox.showerror("Invalid Input", "Number of classrooms must be positive.")
                return

            self.classroom_entries = []

            # Create a notebook for each classroom
            self.classroom_notebook = ttk.Notebook(self.classroom_entries_frame)
            self.classroom_notebook.pack(fill='both', expand=True)

            for i in range(no_of_classes):
                classroom_frame = ttk.Frame(self.classroom_notebook)
                self.classroom_notebook.add(classroom_frame, text=f"Classroom {i + 1}")

                classroom_entry = {
                    "name": tk.StringVar(),
                    "seats": tk.StringVar(),
                    "rows": tk.StringVar(),
                    "subject_count": tk.StringVar(),
                    "subjects": [],
                    "subject_frame": None
                }

                # Classroom details
                ttk.Label(classroom_frame, text="Classroom Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                ttk.Entry(classroom_frame, textvariable=classroom_entry["name"]).grid(row=0, column=1, padx=5, pady=5,
                                                                                      columnspan=2)

                ttk.Label(classroom_frame, text="Number of Seats:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                ttk.Entry(classroom_frame, textvariable=classroom_entry["seats"]).grid(row=1, column=1, padx=5, pady=5,
                                                                                       columnspan=2)

                ttk.Label(classroom_frame, text="Number of Rows:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                ttk.Entry(classroom_frame, textvariable=classroom_entry["rows"]).grid(row=2, column=1, padx=5, pady=5,
                                                                                      columnspan=2)

                # Subjects allowed
                ttk.Label(classroom_frame, text="Number of Subjects:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
                ttk.Entry(classroom_frame, textvariable=classroom_entry["subject_count"]).grid(row=3, column=1, padx=5,
                                                                                               pady=5)

                # Use lambda with default argument to avoid closure issues
                ttk.Button(classroom_frame, text="Set",
                           command=lambda c_entry=classroom_entry: self.create_subject_dropdowns(c_entry)).grid(row=3,
                                                                                                                column=2,
                                                                                                                padx=5,
                                                                                                                pady=5)

                # Container for subject dropdowns
                subject_frame = ttk.Frame(classroom_frame)
                subject_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
                classroom_entry["subject_frame"] = subject_frame

                self.classroom_entries.append(classroom_entry)

            # Show the submit button
            self.classroom_submit_btn.grid()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def create_subject_dropdowns(self, classroom_entry):
        # Clear any existing dropdowns
        subject_frame = classroom_entry["subject_frame"]
        for widget in subject_frame.winfo_children():
            widget.destroy()

        try:
            subject_count = int(classroom_entry["subject_count"].get())
            if subject_count <= 0:
                messagebox.showerror("Invalid Input", "Number of subjects must be positive.")
                return

            classroom_entry["subjects"] = []
            subject_list = list(self.subjects.keys())

            for i in range(subject_count):
                subject_var = tk.StringVar()
                ttk.Label(subject_frame, text=f"Subject {i + 1}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
                subject_dropdown = ttk.Combobox(subject_frame, textvariable=subject_var)
                subject_dropdown.grid(row=i, column=1, padx=5, pady=5)
                subject_dropdown['values'] = subject_list

                classroom_entry["subjects"].append(subject_var)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def submit_classrooms(self):
        # Process classroom entries
        self.classrooms = []


        for classroom_entry in self.classroom_entries:
            try:
                name = classroom_entry["name"].get()
                seats = int(classroom_entry["seats"].get())
                rows = int(classroom_entry["rows"].get())

                subjects_list = [var.get() for var in classroom_entry["subjects"]]

                classroom = Classroom(name, seats, rows, subjects_list)
                self.classrooms.append(classroom)

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for classroom details.")
                return

        # Update the results tab with classroom information
        self.update_results()

        try:
            output_file = assign_students_round_robin(self.subjects, self.classrooms)
            messagebox.showinfo("Success", f"Seating arrangement created: {output_file}")
            import webbrowser
            webbrowser.open(output_file)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


        # Move to the results tab
        self.notebook.select(3)  # Select the Results tab
        messagebox.showinfo("Success", "Classrooms added successfully!")

    def setup_results_tab(self):
        self.results_frame = ttk.Frame(self.results_tab)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a scrollable text widget for results
        self.results_text = tk.Text(self.results_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(self.results_frame, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)

        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_results(self):
        # Clear current results
        self.results_text.delete(1.0, tk.END)

        # Display branch information
        self.results_text.insert(tk.END, "=== BRANCH INFORMATION ===\n\n")
        for name, items in self.branch.items():
            self.results_text.insert(tk.END, f"Branch name: {name}\n")
            self.results_text.insert(tk.END, f"Students: {items}\n\n")

        # Display subject information
        self.results_text.insert(tk.END, "=== SUBJECT INFORMATION ===\n\n")
        for name, items in self.subjects.items():
            self.results_text.insert(tk.END, f"Subject: {name}\n")
            self.results_text.insert(tk.END, f"Students: {items}\n\n")

        # Display classroom information
        self.results_text.insert(tk.END, "=== CLASSROOM INFORMATION ===\n\n")
        for classroom in self.classrooms:
            self.results_text.insert(tk.END, f"Classroom name: {classroom.name}\n")
            self.results_text.insert(tk.END, f"Subjects: {classroom.subjects}\n")
            self.results_text.insert(tk.END, f"Rows: {classroom.rows}\n")
            self.results_text.insert(tk.END, f"Columns: {classroom.cols}\n\n")



# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRegistrationGUI(root)
    root.mainloop()