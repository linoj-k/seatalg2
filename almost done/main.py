import numpy as np
import os


class Classroom:
    def __init__(self, name, seats, rows, subjects):
        self.name = name
        self.seats = seats
        self.rows = rows
        self.subjects = subjects
        self.cols = (seats + rows - 1) // rows
        self.seating_arrangement = np.full((rows, self.cols), '', dtype=object)


def assign_students_round_robin(subjects, classrooms):
    # Create output directory if it doesn't exist
    output_dir = 'seating_arrangements'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #keep a single subject_indices accross all classrooms
    global_subject_indices = {sub: 0 for sub in subjects}

    unplaced_students = {subject: [] for subject in subjects}
    html_content = []

    # Start the HTML document
    html_content.append("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Classroom Seating Arrangements</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .classroom {
                margin-bottom: 30px;
                page-break-inside: avoid;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 20px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .class-title {
                background-color: white;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid black;
                border-bottom: none;
            }
            th {
                background-color: #f2f2f2;
                text-align: center;
                font-weight: bold;
                padding: 10px;
                border: 2px solid black;
            }
            td {
                padding: 10px;
                border: 2px solid black;
                text-align: center;
                vertical-align: top;
            }
            .student {
                margin: 5px 0;
            }
            .student:nth-child(even) {
                color: #0000aa;
            }
            .student:nth-child(odd) {
                color: #8b4513;
            }
            .unplaced {
                margin-top: 30px;
            }
            h2 {
                color: #333;
            }
            @media print {
                body {
                    background-color: white;
                }
                table {
                    box-shadow: none;
                }
                .classroom {
                    page-break-inside: avoid;
                }
            }
        </style>
    </head>
    <body>
    <h1>Classroom Seating Arrangements</h1>
    """)

    # Process each classroom
    for classroom in classrooms:
        available_subjects = [sub for sub in classroom.subjects if sub in subjects]
        #subject_indices = {sub: 0 for sub in available_subjects}

        col_index = 0
        # Fill the seating arrangement
        while col_index < classroom.cols:
            for subject in available_subjects:
                if col_index >= classroom.cols:
                    break

                students = subjects[subject]
                start_index = global_subject_indices[subject]

                row_index = 0
                while row_index < classroom.rows and start_index < len(students):
                    classroom.seating_arrangement[row_index, col_index] = students[start_index]
                    start_index += 1
                    row_index += 1

                global_subject_indices[subject] = start_index
                col_index += 1

        # Create HTML for this classroom
        html_content.append(f'<div class="classroom">')
        html_content.append(f'<div class="class-title">{classroom.name}</div>')
        html_content.append('<table>')

        # Column headers
        html_content.append('<tr>')
        for col in range(classroom.cols):
            html_content.append(f'<th>column {col + 1}</th>')
        html_content.append('</tr>')

        # Rows with student IDs
        for row in range(classroom.rows):
            html_content.append('<tr>')
            for col in range(classroom.cols):
                student_id = classroom.seating_arrangement[row, col]
                if student_id:
                    html_content.append(f'<td><div class="student">{student_id}</div></td>')
                else:
                    html_content.append('<td></td>')
            html_content.append('</tr>')

        html_content.append('</table>')
        html_content.append('</div>')


    # Track unplaced students - THIS SECTION MOVED HERE
    for subject in subjects:
        if subject in global_subject_indices:
            remaining = subjects[subject][global_subject_indices[subject]:]
            if remaining:
                unplaced_students[subject].extend(remaining)



    # Add unplaced students to HTML if any
    if any(students for students in unplaced_students.values()):
        html_content.append('<div class="unplaced">')
        html_content.append('<h2>Unplaced Students</h2>')

        for subject, students in unplaced_students.items():
            if students:
                html_content.append(f'<h3>{subject}</h3>')
                html_content.append('<ul>')
                for student in students:
                    html_content.append(f'<li>{student}</li>')
                html_content.append('</ul>')

        html_content.append('</div>')

    # Close HTML document
    html_content.append('</body></html>')

    # Write combined HTML file
    output_file = os.path.join(output_dir, 'seating_arrangements.html')
    with open(output_file, 'w') as f:
        f.write('\n'.join(html_content))

    print(f"HTML file has been created successfully in the '{output_dir}' folder!")
    print(f"Open 'seating_arrangements.html' to view all classroom seating arrangements.")

    return output_file





