# alx_travel_app_0x01
Django Travel App project with models Listing, Booking, Review, serializers, seeding command, etc.

## Background Task Management with Celery and RabbitMQ

### Steps Implemented
- Duplicated project to `alx_travel_app_0x03`
- Installed Celery and configured RabbitMQ
- Added Celery setup in `settings.py` and created `celery.py`
- Implemented async email task in `listings/tasks.py`
- Triggered email sending on booking creation using `delay()`
- Tested Celery worker and confirmed async execution
