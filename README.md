# Grocery Store App

## 1. Introduction
**Grocery Store App** is a web-based application to buy groceries online.  
Title of my App is: **Nature’s Nourish**.

## 2. Overview
I have undertaken this project with the goal of developing a web-based inventory management system for the grocery store.  

The primary objective of this project is to create a **user-friendly platform** that enables people to buy products from the grocery store online.

This project focuses on developing a web application using **Flask** where:
- Users can buy products from the grocery store online.
- Admins can manage products and categories on the web application.

## 3. Technologies Used
- **Flask Framework**: Backend application development.
- **Flask-Security**: For secure login system.
- **Bcrypt**: For password hashing.
- **SQLite Database**: For data storage and retrieval.
- **Bootstrap**: For styling.
- **Jinja2**: For creating monthly reports.
- **Flask-SQLAlchemy**: For database integration.
- **Flask-RESTful**: For designing and implementing RESTful API endpoints.
- **Vue.js (CLI)**: Frontend application development.
- **Redis**: For caching.
- **Redis and Celery**: For batch jobs.
- **MailHog**: For sending emails.
- **WeasyPrint**: For generating PDFs.

## 4. Data Models
- **User**: Stores user information.
- **Roles**: Stores roles information.
- **Category**: Stores category details (name, description, etc.).
- **Product**: Stores product details (name, price, etc.).
- **Cart**: Stores user cart details (products added and quantity).
- **Order**: Stores order information (total, address, name, etc.).
- **Order_Details**: Stores detailed order information (products, quantity, price).
- **CreateReq**: Stores manager's request to admin to create a category.
- **DeleteReq**: Stores manager's request to admin to delete a category.
- **EditReq**: Stores manager's request to admin to edit a category.
- **LoginReq**: Stores manager's signup request.

## 5. System Architecture
The system follows a **client-server architecture**:  
The **client-side** is built using **Vue.js**, and the **server-side** is built using **Flask** to handle API requests and interaction with the database.

## 6. Functionality
- I have implemented a **role-based access system**. The app has three roles: **Admin**, **Store Manager**, and **User**.

### User Features:
- Users can visit products, search products, visit products by category, add products into the cart, and buy the product.

### Manager Features:
- Managers can perform **CRUD operations** on products.
- Managers can see all the orders made by the user.
- Managers can delete orders.
- Managers can request the admin to create, update, and delete categories.
- Managers can download the list of products in **CSV format**.  
  *(Implemented as an **Asynchronous Task** using **Celery Workers** to handle the CSV generation in the background without blocking the application.)*

### Admin Features:
- Admin can approve a manager's request for signup as a manager.
- Admin can create, update, and delete categories with or without the manager’s request.

### Additional Features:
- The app can send daily reminders to the user via email.
- The app can send monthly reports to the users in HTML format via email.
- The app is using **Redis for caching** to improve the performance of the app.
- I have added styling to make my app look good.
- YAML file for API documentation for CRUD operations on categories.
- **Asynchronous CSV Export**:  
  Managers can download the complete list of products in CSV format, handled asynchronously through **Celery workers**, ensuring smooth performance and non-blocking operations during file generation.
