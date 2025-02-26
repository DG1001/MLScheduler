# Find a Slot with MeiLuft

## Description
Find a Slot with MeiLuft is a web application designed to help users find the best time slots for meetings through voting. The application allows an admin to create polls with multiple date and time options, and participants can vote on their availability using options like Yes, No, or Maybe.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage
- Access the application in your web browser at `http://localhost:8080`.
- Create a new poll and share the generated links with participants.
- Admins can manage polls and add time slots, while users can vote on available options.

## Project Structure
- **app.py**: Main application file that sets up the Flask web server and handles routes for creating and managing polls.
- **templates/admin_poll.html**: Admin interface for adding time slots and viewing results.
- **templates/index.html**: Landing page for creating new polls.
- **templates/user_poll.html**: User interface for voting on time slots.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **README.md**: Provides project documentation.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License.
