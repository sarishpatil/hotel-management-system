# Hotel Management System

A Python CLI application designed to manage room bookings, track dynamic room availability, and calculate billing using MySQL for persistent data storage.

## Features
* **Dynamic Room Tracking:** Synchronizes room availability automatically by checking active database entries against total capacity.
* **Full Database Integration:** Uses MySQL for persistent booking records, search queries, dynamic billing calculations, and deletions.
* **Secure Environment Credentials:** Reads database authentication parameters securely from system environment variables.
* **Robust Input Validation:** Includes error handling for menu selections, invalid strings, and negative numerical inputs to prevent runtime crashes.

## Tech Stack
* **Language:** Python 3
* **Database:** MySQL
* **Libraries:** `mysql-connector-python`, `os`, `random`

## Database Schema
The application automatically creates the `hotel` database and initializes the `bookings` table on startup:

| Field | Type | Description |
| :--- | :--- | :--- |
| `booking_id` | INT (Primary Key) | Unique 5-digit booking identifier |
| `customer_name` | VARCHAR(100) | Full name of the guest |
| `room_type` | VARCHAR(50) | Selected room category (Single, Double, Suite) |
| `nights` | INT | Duration of stay |
| `total_cost` | FLOAT | Computed total cost based on room rate |
| `booking_date` | TIMESTAMP | Auto-generated booking timestamp |

## Getting Started

### Prerequisites
* Python 3.x installed
* MySQL Server running locally

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/sarishpatil/hotel-management-system.git](https://github.com/sarishpatil/hotel-management-system.git)
