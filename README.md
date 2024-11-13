![item added](https://github.com/user-attachments/assets/563771ea-554b-48b1-9dbc-9bd2d5b90c36)# Restaurant Booking System (Little Lemon)

A Django-based restaurant management system that allows users to browse the menu, place orders, make bookings, and manage their profile. It includes an admin interface for managing menu items, a 'Dish of the Day' feature, and the ability to assign roles (Manager, Delivery Crew). This project also integrates user authentication using Djoser for registration, login, and role-based access.
![Home](https://github.com/user-attachments/assets/c5075f73-31f1-41dc-b0c1-364c60167b22)
![about](https://github.com/user-attachments/assets/a52398f1-64c8-45de-b6a6-83c03fdc3879)
![Menu](https://github.com/user-attachments/assets/8814e267-3961-4699-8558-2ddce5ff4a0d)


## Features

- **User Authentication:**
  - User registration and login via Django's built-in authentication system.
  - Redirect to the home page after login and to the login page after logout.
  - Role-based access control for managers and admins (e.g., access to the manager dashboard, user management).
  - Ability to manage user profiles.

- **Manager Dashboard:**
  - Access is restricted to users.
  - Users with 'manager' roles or superusers can access Manager Dashboard.
  - Redirect unauthorized users to the home page.
  - Displays the manager dashboard template (`manager_dashboard.html`) for authorized users.
![Manager_DB](https://github.com/user-attachments/assets/0e732d3d-6d74-4fcb-909e-146ccf68ed47)

- **User Registration:**
  - User registration through Django's `UserCreationForm`.
  - Automatically logs in the user after registration and redirects to the home page.
  - Displays success or error messages based on registration form validation.
![register](https://github.com/user-attachments/assets/c64f2501-8e3e-4a28-8079-ee944db290e8)

- **User List Management:**
  - Admin and managers can view, edit, or delete users from the `user_list.html` template.
  - Users can be edited (username and email) and deleted if the current user has the required permissions.
![all users](https://github.com/user-attachments/assets/fc1b1f17-dc25-4e54-84ad-ad501f74a9b9)

- **Login and Logout:**
  - Handles user login via a form that authenticates credentials using Django's `authenticate` function.
  - On successful login, the user is redirected to the `next` URL or home page.
  - Logout functionality that redirects the user to the home page.
![login](https://github.com/user-attachments/assets/c1340c70-2c14-4dd0-8125-a8d2f276b4c8)

- **User Edit and Delete:**
  - Admin and managers can edit user details (username and email).
  - Admin and managers can delete users, with the change reflected immediately after deletion.
  ![Edit users](https://github.com/user-attachments/assets/bfc3ab90-db49-4c5e-a20a-c1694965aad4)

- **Permissions and Access Control:**
  - **`@superuser_or_multiple_groups_required(['manager', 'Admin'])`**: Ensures the user has the required permissions to access specific views (e.g., user list, edit, delete).
  - **`@login_required`**: Ensures a user is logged in before accessing restricted views (e.g., user management).

- **Registration Success Page:**
  - Displays a registration success page with the new user's username and ID.

- **Whole Menu:**
  - Displays the entire menu to all users (authenticated and anonymous).
  - For authenticated users, retrieves the user's cart and shows items in the cart.
  - For anonymous users, use a session-based cart to track items.
  - Categories are displayed based on distinct menu categories.
  - Provides a flag (`is_manager_or_superuser`) to check if the user is a manager or superuser, enabling conditional access to specific menu management features.
![Menu](https://github.com/user-attachments/assets/8da7e8e9-7fd2-4be1-a06d-6127e9309d6e)
![Menu-cart](https://github.com/user-attachments/assets/aa470b24-7c79-4a76-9613-2799ed7cacfd)

- **Single Menu Item View:**
  - Allows users to view detailed information for a single menu item.
  - Displays the menu item based on the provided primary key (`pk`).
![single item](https://github.com/user-attachments/assets/3e09deed-4bde-45ba-b305-fb9dee27065b)

- **Add Menu Item:**
  - Accessible only to managers, admins, and superusers (via `@superuser_or_multiple_groups_required`).
  - Allows managers to add new menu items to the menu.
  - Handles image uploads for menu items.
  - After successful addition, the newly added menu item is displayed on the page.
![item added](https://github.com/user-attachments/assets/cab21677-2fdc-45de-8611-bff7f62ebaf1)

- **Delete Menu Item:**
  - Accessible only to managers, admins, and superusers (via `@superuser_or_multiple_groups_required`).
  - Allows managers to delete a menu item from the menu.
  - Redirects to the menu page after deletion.
 ![manger-menu](https://github.com/user-attachments/assets/c228c59d-cbf0-4860-8e05-98b86f7b6f55)

    
## Booking Features

- **Book Table:**
  - Allows users to book a table by submitting a booking form.
  - After successful form submission, the user is redirected to a booking confirmation page (`booking_success.html`).
![table booked](https://github.com/user-attachments/assets/4c5cb821-52ad-414f-80a0-228fdb6ed7ae)

- **Manage Bookings:**
  - Accessible only by managers (via `@superuser_or_multiple_groups_required`).
  - Displays all bookings in the `manage_bookings.html` template.
  - Allows managers to view the list of all bookings.
![manager bookings](https://github.com/user-attachments/assets/41118718-6635-4a2c-9d96-03898ead9da1)

- **Edit Booking:**
  - Accessible only by managers (via `@superuser_or_multiple_groups_required`).
  - Allows managers to edit the details of a booking (e.g., update booking status).
  - After editing, a success message is shown and the manager is redirected to the manage bookings page.
![booking update](https://github.com/user-attachments/assets/4cdcf1d6-d431-413e-a6ac-01a0faa05e8e)

- **Delete Booking:**
  - Accessible only by managers (via `@superuser_or_multiple_groups_required`).
  - Allows managers to delete a booking.
  - After deletion, a success message is shown and the manager is redirected to the manage bookings page.

- **Mark Booking as Done:**
  - Accessible only by managers (via `@superuser_or_multiple_groups_required`).
  - Allows managers to mark a booking as "done" (if not already marked).
  - After marking, a success message is shown and the manager is redirected to the manage bookings page.

## Dish of the Day Features

- **Dish of the Day:**
  - Allows managers to view all menu items marked as the "Dish of the Day."
  - Managers can remove an item from the Dish of the Day list by submitting a POST request.
  - After removing, the list refreshes to reflect the changes.
![dish-D](https://github.com/user-attachments/assets/81d987f9-08d7-4deb-916f-fdfbd8636587)

- **Toggle Dish of the Day:**
  - Allows managers to toggle the "Dish of the Day" status for a menu item.
  - Clicking this option sets the `dish_of_the_day` flag for the item to either `True` or `False`.
  - After toggling, the user is redirected to the menu page to reflect the changes.
 ![manger-menu](https://github.com/user-attachments/assets/02fdd2a9-7f41-45f7-bbd8-bc60aff0eb28)

    
## Cart Features

- **Add to Cart:**
  - Allows authenticated users to add items to their cart.
  - For anonymous users, cart is handled via session-based storage.
  - Users can specify the quantity of the item being added to the cart.
  - If the item already exists in the cart, the quantity is updated.
![cart](https://github.com/user-attachments/assets/1d634dca-0b23-4c2f-aec2-6ced731049c8)

- **Remove from Cart:**
  - Allows users to remove an item from the cart.
  - Both authenticated and anonymous users can remove items from their respective carts.
![order placed](https://github.com/user-attachments/assets/8c8acdec-613a-408f-8db9-51dc5e0aebd1)

- **Cart Detail:**
  - Displays the contents of the user's cart.
  - For authenticated users, the cart is associated with their user account.
  - For anonymous users, the cart is managed using session-based storage.

- **Update Cart Quantity:**
  - Allows users to update the quantity of an item in their cart (either increment or decrement).
  - If the quantity is set to zero, the item is removed from the cart.

## Group Management Features

- **Manage Groups:**
  - Allows managers or admins to view all groups in the system.
  - Accessible only to users with `manager` or `admin` roles.
![group](https://github.com/user-attachments/assets/2ec59cbf-f849-44fd-a289-df2e98465b98)

- **Add Group:**
  - Allows managers or admins to create new user groups.
  - Groups can be assigned permissions during creation.
  - Accessible only to users with `manager` or `admin` roles.
![new group1](https://github.com/user-attachments/assets/56987e76-a27c-4619-8ede-142bd2fcb008)

- **Group Details:**
  - Displays details of a specific group, including the users not in the group and all available permissions.
  - Managers or admins can add or remove users from groups, as well as assign or remove permissions for a group.
  - Accessible only to users with `manager` or `admin` roles.
![group-manager](https://github.com/user-attachments/assets/31cb720c-ec54-4c83-9f3a-34789c24109c)

- **Remove User from Group:**
  - Allows managers or admins to remove a user from a specific group.
  - Accessible only to users with `manager` or `admin` roles.
![group manger1](https://github.com/user-attachments/assets/19089625-33b0-484b-baf3-f4d7730903f6)

- **Remove Permission from Group:**
  - Allows managers or admins to remove permission from a specific group.
  - Accessible only to users with `manager` or `admin` roles.
 
    
## Delivery Crew Features

- **Delivery Crew Dashboard:**
  - Managers can see all unassigned orders (orders without a delivery crew assigned and status is `False`).
  - Delivery crew members can only see orders assigned to them.
  - Accessible to users with `manager`, `admin`, or `delivery crew` roles.
![Deliver DB](https://github.com/user-attachments/assets/829f1604-9687-4d5d-80b5-7fca7ad4ce77)

- **Update Order Status:**
  - Delivery crew members can update the status of orders assigned to them.
  - Once the order is marked as delivered, its status is updated to `True`.
  - Prevents updates if the order has already been delivered.
  - Accessible to users with `manager`, `admin`, or `delivery crew` roles.
![Update ordr](https://github.com/user-attachments/assets/3af413ec-1c16-4386-888d-6e545212862e)

- **Assign Delivery Crew:**
  - Allows managers to assign a delivery crew member to a pending order.
  - Ensures that the order is not already completed or assigned to another crew member.
  - Accessible to users with `manager` or `admin` roles.
![orders-mang](https://github.com/user-attachments/assets/d02cd3a6-0f31-404b-bb44-6678adc90335)

- **Delivery Crew List:**
  - Displays a list of all members of the `Delivery Crew` group.
  - Shows the total number of assigned orders, completed orders, and pending orders for each delivery crew member.
  - Allows managers or admins to view the availability of delivery crew members.
  - Accessible to users with `manager` or `admin` roles.
![deliver Drive crew](https://github.com/user-attachments/assets/36411db7-41c9-44b6-a1ed-676612ee0b7c)

- **Remove Delivery Crew:**
  - Allows managers to remove a user from the `Delivery Crew` group.
  - Ensures the user is a member of the `Delivery Crew` group before removal.
  - Accessible to users with `manager` or `admin` roles.
 
    
## Orders

- **Place Order:**
  - Allows logged-in users to place an order with the items in their cart.
  - Ensures that the cart is not empty before placing the order.
  - Calculates the total cost of the cart items and creates a new `Order` with the total cost, date, and status set to `False` (pending).
  - After placing the order, cart items are deleted to clear the cart.
  - Accessible only by authenticated users.
![order placed](https://github.com/user-attachments/assets/51607f43-6707-4df5-9825-73097f1df313)

- **Order Confirmation:**
  - Displays the details of the placed order including the items and total cost.
  - Accessible by users after placing an order.
  - Accessible only by authenticated users.
![Screen Shot 2024-11-12 at 6 24 45 PM](https://github.com/user-attachments/assets/a94334e4-93e1-425d-adb6-f916795c3768)

- **Order History:**
  - Displays all past orders for the logged-in user, ordered by the most recent.
  - Accessible only by authenticated users.
![orders history](https://github.com/user-attachments/assets/54e086b1-2e4e-45ac-8f71-42f7f1109f17)

- **Order Detail:**
  - Allows managers, admins, and delivery crew to view the details of an order.
  - Displays order details and allows for delivery crew assignment if the order has not been delivered yet.
  - Accessible to users with `manager`, `admin`, or `delivery crew` roles.
![detail order](https://github.com/user-attachments/assets/6ef2671c-2fb2-44f2-a01d-076b3bad6bf9)

- **Orders List:**
  - Displays a list of all orders in the system.
  - Shows all orders regardless of their status, along with the delivery crew assignment.
  - Accessible to users with `manager` or `admin` roles.
![orders history](https://github.com/user-attachments/assets/4dadf99e-cd37-498b-8ecc-159f8c564113)


## Manager Dashboard

- **Manager Dashboard:**
  - Provides managers with a dedicated dashboard to manage the system.
  - Accessible only by superusers or users in the `manager` group.
  - Displays manager-specific content and actions.
![Screen Shot 2024-11-12 at 7 06 01 PM](https://github.com/user-attachments/assets/922c1bc0-85b8-4770-8f94-5a577ce78e0c)

- **Regular View:**
  - Redirects regular users to the home page, ensuring they don't have access to manager-specific content.
  ![Home](https://github.com/user-attachments/assets/63db8e6a-d12e-49d2-b638-a41aac77e769)

- **Home Clear Manager:**
  - Clears the manager view session flag when accessing the home page from the manager dashboard, ensuring that the manager session is properly reset.
  - Redirects to the home page after clearing the session flag.
![manager](https://github.com/user-attachments/assets/5e9f13c0-8686-46f6-a434-e3c22000bebb)

## Installation

### Prerequisites

- Python 3.12.5
- Django 5.1.2
- SQLite (default database)
- Djoser for authentication
- Bootstrap for layout

### Setup

1. Clone the repository:

   git clone https://github.com/vamshiachavelli/littlelemon.git
   cd restaurant-booking-system
   
2. Install the required dependencies:

   pip install -r requirements.txt
   Set up the database and run migrations:

3. Set up the database and run migrations:

    python manage.py migrate

4. Start the Django development server:

    python manage.py runserver

5. Access the project in your browser at http://127.0.0.1:8000.

