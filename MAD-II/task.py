from datetime import datetime, timedelta
import flask_excel as excel
from celery import shared_task
from app import Product, celery, Cart, User, Order,Order_Details
from celery.schedules import crontab
from mail_service import send_message, send_html_email
from flask import render_template
from weasyprint import HTML
import os

@celery.task()
def pdf_generator(message,name):
    html = HTML(string = message)
    filename = name +".pdf"
    print("Finished")
    current_dir = os.path.dirname(os.path.realpath(__file__))
    report_dir = os.path.join(current_dir, 'Report')
    pdf_path = os.path.join(report_dir, filename)
    file_path = os.path.join(report_dir, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
    html.write_pdf(pdf_path)

@celery.task()
def report(user):
    current_date = datetime.now()
    last_day = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day = (last_day - timedelta(days=1)).replace(day=1)
    user_obj = User.query.filter_by(user_id = user).first()
    orders = Order.query.filter(Order.user_id == user and (Order.order_date >= first_day, Order.order_date < last_day)).all()
    grand_total = 0
    for i in orders:
        grand_total = grand_total + i.total 
    message = render_template('pdf-report.html', user_obj = user_obj, orders = orders, grand_total = grand_total)
    pdf_generator(message, user_obj.email)
    return message

@celery.task()
def download_csv_file():
    products = Product.query.with_entities(Product.name, Product.price
    , Product.quantity, Product.unit, Product.expiry_date, Product.description ).all()
    
    csv_output = excel.make_response_from_query_sets(products, ["name", "price"
        , "quantity", "unit", "expiry_date", "description"], "csv")
    file_name="Products.csv"

    with open (file_name, "wb") as f:
        f.write(csv_output.data) 

    return file_name

@celery.task()
def daily_remainder():
    current_date = datetime.now()
    today = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    subject = "Daily Remainder"
    content_body =  "Daily Reminder To Buy your Groceries ! Have A Good Day!"
    # list = Cart.query.with_entities(Cart.user_id).distinct().all()
    orders = Order.query.with_entities(Order.user_id).filter(Order.order_date > today).all()
    orders = [o.user_id for o in orders]
    users = User.query.filter(~User.user_id.in_(orders)).all()
    for i in users:
        # user_ = User.query.filter_by(user_id = i.user_id).first()
        user_email_id = i.email
        send_html_email(user_email_id, subject, content_body)
    return "Schedule Task For Sending Email Is Completed"

@celery.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1', hour=2),
        daily_remainder.s()
    )

@celery.task()
def html_rep():
    email_subject = "HTML Report Email"
    users = User.query.all()
    for i in users:
        id = i.user_id
        to_address = i.email
        html_report = report(id)
        send_html_email(to_address, email_subject, html_report,f"report/{i.email}.pdf")
    return "Schedule Task For Sending Email with HTML Is Completed"

@celery.on_after_configure.connect
def send_email_with_html(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1', hour='13'),
        html_rep.s()
    )





# def html_report():
#     current_date = datetime.now()
#     last_day = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     first_day = (last_day - timedelta(days=1)).replace(day=1)
#     users = User.query.all()
#     for user in users:
#         user_obj = User.query.filter_by(user_id = user).first()
#         orders = Order.query.filter(Order.user_id == user,Order.order_date >= first_day,Order.order_date < last_day).all()
#         message = render_template('pdf-report.html', user_obj = user_obj, order = orders)


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#         # sender.add_periodic_task(10.0, daily_remainder.s('hello'), name='add every 10')
#         sender.add_periodic_task(
#             crontab(hour=18, minute=46, day_of_week=7),
#             daily_remainder.s("Hello"),
#             )
        

#             # crontab(hour=22, minute=54, day_of_week=6),
# # 


# @celery.task()
# def daily_remainder():
#     subject = "Daily Remainder"
#     content_body = "Check out Your Items in Cart."
#     rows = Cart.query.with_entities(Cart.user_id).all()
#     for row in rows:
#         user_email = User.query.filter_by(user_id = row.user_id).with_entities(User.email).first()
#         send_message(user_email, subject, content_body)
#     return "OK"


# @celery.on_after_configure.connect
# def send_email(sender, **kwargs):
#     sender.add_periodic_task(
#         crontab(minute='*/1', hour='9', day_of_week=1),
#         daily_remainder.s(),
#     )