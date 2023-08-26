
---

# API Service for CRUD

This project implements an API service for CRUD operations on a store's inventory of cuboid boxes. Each box has dimensions (length, breadth, and height) and is associated with a creator (store employee) upon creation. The project includes APIs for adding, updating, listing, and deleting boxes, along with various permissions and filters.

## Project Overview

The project consists of the following key components:

1. **Models**: The minimal required models for the store inventory, including user authentication, are set up.

2. **API Endpoints**: The project implements the following API endpoints:

   - **Add Box**: Add a new box with dimensions. Staff users can add boxes.
   - **Update Box**: Update dimensions of a box by its ID. Any staff user can update a box, except creator and creation date.
   - **List All Boxes**: List all available boxes. Provides data like length, width, height, area, volume, creator (for staff), and last updated (for staff).
   - **List My Boxes**: List boxes created by the requesting staff user. Provides the same data as the list all API.
   - **Delete Box**: Delete a box by its ID. Only the creator of the box can delete it.

3. **Permissions and Filters**: Different permissions and filters are applied to each API to ensure proper access control and filtering.

4. **Constraints**: Various conditions are checked on each add/update/delete operation to ensure that average area, average volume, and total box limits are not exceeded.

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment (recommended).
4. Install the required dependencies using `pip install -r requirements.txt`.
5. Set up your database (if not already done).
6. Run migrations using `python manage.py migrate`.
7. Start the development server using `python manage.py runserver`.

## API Endpoints

### Add Box

- **URL**: `/boxes/`
- **Method**: POST
- **Permissions**: User must be logged in and staff.
- **Request Body**:
  ```json
  {
    "length": 10,
    "breadth": 8,
    "height": 5
  }
  ```
- **Response**: The newly added box details.

### Update Box

- **URL**: `/boxes/<int:pk>/`
- **Method**: PUT
- **Permissions**: Any staff user.
- **Request Body**:
  ```json
  {
    "length": 12,
    "breadth": 9,
    "height": 6
  }
  ```
- **Response**: The updated box details.

### List All Boxes

- **URL**: `/boxes/`
- **Method**: GET
- **Permissions**: Any user.
- **Response**: List of all available boxes with relevant details.

### List My Boxes

- **URL**: `/my-boxes/`
- **Method**: GET
- **Permissions**: Staff users only.
- **Response**: List of boxes created by the requesting staff user.

### Delete Box

- **URL**: `/boxdel/<int:pk>/`
- **Method**: DELETE
- **Permissions**: Creator of the box only.
- **Response**: Success message upon successful deletion.

## Filters

You can apply filters to the list APIs using query parameters. Available filters include `length_more_than`, `length_less_than`, `breadth_more_than`, `breadth_less_than`, `height_more_than`, `height_less_than`, `area_more_than`, `area_less_than`, `volume_more_than`, `volume_less_than`, `created_by_username`, `created_before`, and `created_after`.

## Constraints

- Average area of all added boxes should not exceed A1.
- Average volume of all boxes added by a user should not exceed V1.
- Total boxes added in a week should not exceed L1.
- Total boxes added in a week by a user should not exceed L2.

## Configuration

- A1: 100
- V1: 1000
- L1: 100
- L2: 50

## Contributing

Feel free to contribute by creating issues or pull requests. Your contributions are valuable.

<!-- ## License

This project is licensed under the [MIT License](LICENSE). -->

---
