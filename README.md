# YAML File Editor & Viewer

=======
This project is a web-based application designed for dynamically loading and editing YAML files. It allows users to upload YAML files, view their contents as a form, and modify the values interactively. It also supports displaying non-YAML files as plain text.

---

## Features

- **Dynamic Form Generation**: Converts YAML files into editable forms based on their structure.
- **File Type Detection**: Differentiates between YAML files and other file types (JSON, plain text).
- **Interactive Form Editing**: Supports inputs for strings, integers, lists, and nested dictionaries.
- **Live Preview**: Displays the raw file content for non-YAML files.
- **Error Handling**: Displays appropriate error messages for unsupported files or parsing errors.

---

## Project Structure

```plaintext
.
├── backend
│   └── src
│       ├── app
│       │   ├── data
│       │   │   └── app.db
│       │   ├── file_servcice_container
│       │   │   ├── container_monitor.py
│       │   │   └── Dockerfile
│       │   ├── __init__.py
│       │   ├── routes
│       │   │   ├── auth_routes.py
│       │   │   ├── container_proxy.py
│       │   │   ├── docker_routes.py
│       │   │   ├── dynamic_router.py
│       │   │   ├── fileupload_routes.py
│       │   │   ├── loadfile_routes.py
│       │   │   └── __pycache__
│       │   ├── services
│       │   │   ├── bind_filesystem.py
│       │   │   ├── database.py
│       │   │   ├── docker_service.py
│       │   │   ├── loadfile_service.py
│       │   │   ├── __pycache__
│       │   │   ├── server.py
│       │   │   ├── user.py
│       │   │   └── yaml_service.py
│       │   └── utils
│       │       ├── db_setup.py
│       │       ├── docker_manager.py
│       │       ├── file_handler.py
│       │       ├── __pycache__
│       │       └── request_router.py
│       ├── __pycache__
│       ├── requirements.txt
│       ├── run.py
│       └── src
│           └── data
│               └── app.db
├── frontend
│   └── python-project
│       ├── angular.json
│       ├── package.json
│       ├── package-lock.json
│       ├── public
│       │   └── favicon.ico
│       ├── README.md
│       ├── server.py
│       ├── server.ts
│       ├── src
│       │   ├── app
│       │   │   ├── app.component.css
│       │   │   ├── app.component.html
│       │   │   ├── app.component.html.bk
│       │   │   ├── app.component.spec.ts
│       │   │   ├── app.component.ts
│       │   │   ├── app.config.server.ts
│       │   │   ├── app.config.ts
│       │   │   ├── app.routes.ts
│       │   │   ├── code-editor
│       │   │   │   ├── code-editor.component.css
│       │   │   │   ├── code-editor.component.html
│       │   │   │   ├── code-editor.component.spec.ts
│       │   │   │   └── code-editor.component.ts
│       │   │   ├── components
│       │   │   │   ├── code-form
│       │   │   │   │   ├── code-form.component.css
│       │   │   │   │   ├── code-form.component.html
│       │   │   │   │   ├── code-form.component.spec.ts
│       │   │   │   │   └── code-form.component.ts
│       │   │   │   ├── feature1
│       │   │   │   │   ├── feature1.component.css
│       │   │   │   │   ├── feature1.component.html
│       │   │   │   │   ├── feature1.component.spec.ts
│       │   │   │   │   └── feature1.component.ts
│       │   │   │   ├── feature2
│       │   │   │   │   ├── feature2.component.css
│       │   │   │   │   ├── feature2.component.html
│       │   │   │   │   ├── feature2.component.spec.ts
│       │   │   │   │   └── feature2.component.ts
│       │   │   │   ├── file-content
│       │   │   │   │   ├── file-content.component.css
│       │   │   │   │   ├── file-content.component.html
│       │   │   │   │   ├── file-content.component.spec.ts
│       │   │   │   │   └── file-content.component.ts
│       │   │   │   ├── file-environment
│       │   │   │   │   ├── file-environment.component.css
│       │   │   │   │   ├── file-environment.component.html
│       │   │   │   │   ├── file-environment.component.spec.ts
│       │   │   │   │   └── file-environment.component.ts
│       │   │   │   ├── home
│       │   │   │   │   ├── home.component.css
│       │   │   │   │   ├── home.component.html
│       │   │   │   │   ├── home.component.spec.ts
│       │   │   │   │   └── home.component.ts
│       │   │   │   ├── login
│       │   │   │   │   ├── login.component.css
│       │   │   │   │   ├── login.component.html
│       │   │   │   │   ├── login.component.spec.ts
│       │   │   │   │   └── login.component.ts
│       │   │   │   └── register
│       │   │   │       ├── register.component.css
│       │   │   │       ├── register.component.html
│       │   │   │       ├── register.component.spec.ts
│       │   │   │       └── register.component.ts
│       │   │   └── services
│       │   │       ├── auth.guard.ts
│       │   │       ├── auth.service.ts
│       │   │       ├── file-upload.service.spec.ts
│       │   │       ├── file-upload.service.ts
│       │   │       ├── folder.service.spec.ts
│       │   │       └── folder.service.ts
│       │   ├── index.html
│       │   ├── main.server.ts
│       │   ├── main.ts
│       │   └── styles.css
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       └── tsconfig.spec.json
├── README.md
└── setup.sh

30 directories, 90 files
```

---

## Installation

### Prerequisites

- **Node.js**: Required for running the Angular frontend.
- **Python 3.9+**: Required for running the Flask backend.
- **Docker**: Optional for containerized deployment.

---

### Backend Setup

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```
3. Install the required dependencies (from inside /backend/src):
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask backend (from inside /backend/src):
   ```bash
   gunicorn -w 5 -b 0.0.0.0:8000 run:app
   ```
   The backend should now be running on `http://localhost:8000`.

---

### Frontend Setup

1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Angular development server:
   ```bash
   ng serve
   ```
   The frontend should now be running on `http://localhost:4200`.

---

## Usage

1. **Select a File**: Use the file browser to select a YAML or JSON file.
2. **Edit YAML**: If the file is a valid YAML, it will be converted into a form for editing. Modify values and interact with nested structures.
3. **View Plain Content**: For non-YAML files, the raw content will be displayed in a `pre` block.
4. **Submit Changes**: Edited YAML files can be converted back and sent to the backend for further processing.

---

## API Endpoints

### GET `/api/file-content`

Fetches the content of the specified file.

- **Parameters**: `path` (file path)
- **Response**: 
  - For YAML files: Returns the parsed YAML as a JSON array.
  - For other files: Returns the raw file content.

---

## Known Issues

- YAML files with invalid syntax may cause parsing errors.
- Dynamic form rendering may not fully support deeply nested structures.
- Styling for the generated forms can be improved.
