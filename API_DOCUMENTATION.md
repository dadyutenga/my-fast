# API Endpoints Documentation

This document provides a detailed overview of all API endpoints available in the FastAPI backend project.

## Authentication Endpoints

- **POST /api/auth/register**
  - **Description**: Register a new user with email and password.
  - **Request Body**: `{ "email": "string", "password": "string", "role": "string" }`
  - **Response**: `{ "access_token": "string", "refresh_token": "string", "token_type": "bearer" }`
  - **Status Codes**: 200 OK, 400 Bad Request (Email already registered)

- **POST /api/auth/token**
  - **Description**: Login to obtain access and refresh tokens.
  - **Request Body**: Form data with `username` (email) and `password`.
  - **Response**: `{ "access_token": "string", "refresh_token": "string", "token_type": "bearer" }`
  - **Status Codes**: 200 OK, 401 Unauthorized (Incorrect credentials)

- **POST /api/auth/refresh**
  - **Description**: Refresh access token using refresh token.
  - **Request Body**: `{ "refresh_token": "string" }`
  - **Response**: `{ "access_token": "string", "refresh_token": "string", "token_type": "bearer" }`
  - **Status Codes**: 200 OK, 401 Unauthorized (Invalid refresh token)

- **POST /api/auth/validate**
  - **Description**: Validate a given token.
  - **Request Body**: `{ "token": "string" }`
  - **Response**: `{ "valid": true, "email": "string", "role": "string" }`
  - **Status Codes**: 200 OK, 401 Unauthorized (Invalid token)

- **POST /api/auth/logout**
  - **Description**: Logout by invalidating the current token.
  - **Headers**: `Authorization: Bearer <token>`
  - **Response**: `{ "message": "Successfully logged out" }`
  - **Status Codes**: 200 OK, 401 Unauthorized (Invalid token)

## User Endpoints

- **GET /api/user/me**
  - **Description**: Get current user's profile information.
  - **Headers**: `Authorization: Bearer <token>`
  - **Response**: User object with id, email, role, and timestamps.
  - **Status Codes**: 200 OK, 401 Unauthorized

- **PUT /api/user/me**
  - **Description**: Update current user's profile.
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "email": "string", "password": "string", "role": "string" }` (all optional)
  - **Response**: Updated user object.
  - **Status Codes**: 200 OK, 400 Bad Request (Email in use), 401 Unauthorized

## Admin Endpoints

- **GET /api/admin/users**
  - **Description**: Get a list of all users (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of user objects.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

## OTP Endpoints

- **POST /api/otp/send-email-otp**
  - **Description**: Send OTP to an email address.
  - **Request Body**: `{ "email": "string" }`
  - **Response**: `{ "message": "OTP sent to email" }`
  - **Status Codes**: 200 OK

- **POST /api/otp/send-sms-otp**
  - **Description**: Send OTP to a phone number.
  - **Request Body**: `{ "phone": "string" }`
  - **Response**: `{ "message": "OTP sent to SMS" }`
  - **Status Codes**: 200 OK

- **POST /api/otp/verify-otp**
  - **Description**: Verify OTP for email or phone.
  - **Request Body**: `{ "email_or_phone": "string", "otp": "string" }`
  - **Response**: `{ "message": "OTP verified" }`
  - **Status Codes**: 200 OK, 400 Bad Request (Invalid or expired OTP)

## Password Reset Endpoints

- **POST /api/password-reset/request**
  - **Description**: Request a password reset code via email.
  - **Request Body**: `{ "email": "string" }`
  - **Response**: `{ "message": "Password reset code sent to email" }`
  - **Status Codes**: 200 OK, 404 Not Found (Email not found)

- **POST /api/password-reset/confirm**
  - **Description**: Confirm password reset with code and new password.
  - **Request Body**: `{ "email": "string", "code": "string", "new_password": "string" }`
  - **Response**: `{ "message": "Password reset successful" }`
  - **Status Codes**: 200 OK, 400 Bad Request (Invalid or expired code), 404 Not Found

## Metrics Endpoints

- **GET /api/metrics/health**
  - **Description**: Check API health status.
  - **Response**: `{ "status": "healthy" }`
  - **Status Codes**: 200 OK

- **GET /api/metrics/metrics**
  - **Description**: Get API usage metrics (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Response**: Metrics data object.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

## Inventory Management Endpoints

- **POST /api/item/items**
  - **Description**: Create a new inventory item (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "name": "string", "description": "string", "quantity": int, "price": float }`
  - **Response**: Created item object.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **POST /api/item/items/bulk**
  - **Description**: Create multiple inventory items (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: List of item objects.
  - **Response**: List of created item objects.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/item/items**
  - **Description**: Get a list of inventory items.
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of item objects.
  - **Status Codes**: 200 OK

- **GET /api/item/items/{item_id}**
  - **Description**: Get a specific inventory item.
  - **Path Param**: `item_id` (int)
  - **Response**: Item object.
  - **Status Codes**: 200 OK, 404 Not Found

- **PUT /api/item/items/{item_id}**
  - **Description**: Update an inventory item (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Path Param**: `item_id` (int)
  - **Request Body**: `{ "name": "string", "description": "string", "quantity": int, "price": float }` (all optional)
  - **Response**: Updated item object.
  - **Status Codes**: 200 OK, 404 Not Found, 403 Forbidden, 401 Unauthorized

- **DELETE /api/item/items/{item_id}**
  - **Description**: Delete an inventory item (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Path Param**: `item_id` (int)
  - **Response**: Deleted item object.
  - **Status Codes**: 200 OK, 404 Not Found, 403 Forbidden, 401 Unauthorized

## Media Endpoints

- **POST /api/media/media**
  - **Description**: Upload a media file (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: Multipart form with file.
  - **Response**: Media object.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/media/media/{media_id}**
  - **Description**: Get a specific media item.
  - **Path Param**: `media_id` (int)
  - **Response**: Media object.
  - **Status Codes**: 200 OK, 404 Not Found

## Receipt Endpoints

- **POST /api/receipt/receipts**
  - **Description**: Create a new receipt (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "order_id": int, "items": array, "total": float }`
  - **Response**: Created receipt object.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/receipt/receipts/{receipt_id}**
  - **Description**: Get a specific receipt.
  - **Path Param**: `receipt_id` (int)
  - **Response**: Receipt object.
  - **Status Codes**: 200 OK, 404 Not Found

- **GET /api/receipt/receipts**
  - **Description**: Get a list of receipts.
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of receipt objects.
  - **Status Codes**: 200 OK

## Payment Endpoints

- **POST /api/payments**
  - **Description**: Create a new payment record and initiate payment with the selected gateway.
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "order_id": "string", "amount": float, "currency": "string", "method": "enum (selcom, paypal, stripe, mpesa)", "buyer_email": "string (optional)", "buyer_name": "string (optional)", "buyer_phone": "string (optional)" }`
  - **Response**: Payment object.
  - **Status Codes**: 200 OK, 400 Bad Request, 401 Unauthorized, 500 Internal Server Error

- **GET /api/payments**
  - **Description**: Get a list of payments for the current user.
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of payment objects.
  - **Status Codes**: 200 OK, 401 Unauthorized

- **GET /api/payments/{payment_id}**
  - **Description**: Get details of a specific payment.
  - **Headers**: `Authorization: Bearer <token>`
  - **Path Param**: `payment_id` (int)
  - **Response**: Payment object.
  - **Status Codes**: 200 OK, 404 Not Found, 401 Unauthorized

- **PUT /api/payments/{payment_id}**
  - **Description**: Update the status of a payment (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Path Param**: `payment_id` (int)
  - **Request Body**: `{ "status": "enum (pending, completed, failed, refunded) (optional)", "transaction_id": "string (optional)" }`
  - **Response**: Updated payment object.
  - **Status Codes**: 200 OK, 404 Not Found, 403 Forbidden, 401 Unauthorized

## User Activity Endpoints

- **POST /api/user-activity/activities**
  - **Description**: Log a user activity (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "user_id": int, "action": "string", "details": "string" }`
  - **Response**: Activity object.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/user-activity/activities**
  - **Description**: Get all user activities (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of activity objects.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/user-activity/my-activities**
  - **Description**: Get current user's activities.
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of activity objects.
  - **Status Codes**: 200 OK, 401 Unauthorized

## Notification Endpoints

- **POST /api/notification/notifications**
  - **Description**: Create a notification (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "user_id": int, "title": "string", "message": "string" }`
  - **Response**: Notification object.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/notification/notifications**
  - **Description**: Get all notifications (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of notification objects.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/notification/my-notifications**
  - **Description**: Get current user's notifications.
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of notification objects.
  - **Status Codes**: 200 OK, 401 Unauthorized

- **PUT /api/notification/notifications/{notification_id}**
  - **Description**: Update notification status (mark as read).
  - **Headers**: `Authorization: Bearer <token>`
  - **Path Param**: `notification_id` (int)
  - **Request Body**: `{ "is_read": boolean }`
  - **Response**: Updated notification object.
  - **Status Codes**: 200 OK, 404 Not Found, 401 Unauthorized

## Audit Log Endpoints

- **POST /api/audit-log/audit-logs**
  - **Description**: Log an audit event (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "user_id": int, "entity_type": "string", "entity_id": int, "action": "string", "details": "string" }`
  - **Response**: Audit log object.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/audit-log/audit-logs**
  - **Description**: Get all audit logs (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of audit log objects.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

- **GET /api/audit-log/audit-logs/entity/{entity_type}/{entity_id}**
  - **Description**: Get audit logs for a specific entity (admin only).
  - **Headers**: `Authorization: Bearer <token>`
  - **Path Params**: `entity_type` (string), `entity_id` (int)
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of audit log objects.
  - **Status Codes**: 200 OK, 403 Forbidden, 401 Unauthorized

## Chat Message Endpoints

- **POST /api/chat-message/messages**
  - **Description**: Send a chat message.
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "receiver_id": int, "content": "string" }`
  - **Response**: Message object.
  - **Status Codes**: 200 OK, 401 Unauthorized

- **GET /api/chat-message/messages/sent**
  - **Description**: Get sent messages.
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of message objects.
  - **Status Codes**: 200 OK, 401 Unauthorized

- **GET /api/chat-message/messages/received**
  - **Description**: Get received messages.
  - **Headers**: `Authorization: Bearer <token>`
  - **Query Params**: `skip` (int, default 0), `limit` (int, default 100)
  - **Response**: List of message objects.
  - **Status Codes**: 200 OK, 401 Unauthorized

- **PUT /api/chat-message/messages/{message_id}**
  - **Description**: Update message status (mark as read).
  - **Headers**: `Authorization: Bearer <token>`
  - **Path Param**: `message_id` (int)
  - **Request Body**: `{ "is_read": boolean }`
  - **Response**: Updated message object.
  - **Status Codes**: 200 OK, 404 Not Found, 401 Unauthorized
