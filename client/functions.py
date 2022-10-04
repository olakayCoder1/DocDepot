from email.message import EmailMessage
import ssl
import smtplib
import os
import environ
from django.conf import settings


env = environ.Env()
environ.Env.read_env()


def send_reset_mail(receiver,token,uidb64):
    sender_email = "olakaycoder1@gmail.com"
    receiver_email = receiver

    # the app password generated from gmail
    print()
    password = 'evctrejhhdkghsmy' 
    subject = "Paasword reset"
    body = f"""
            we receive a request to reset your password\n
            You can ignore if you don't make the request. Click the link below the to set new password.\n
            http://127.0.0.1:8000/api/v1/auth/setpassword/{token}/{uidb64}/
        """

    em = EmailMessage()
    em["From"] = receiver_email
    em["To"] = sender_email
    em["subject"] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as connection:
            connection.login(sender_email, password)
            connection.sendmail(sender_email, receiver_email, em.as_string())
    except:
        pass
    return True





def update_file_url(instance ,name):

    # get instance file url 
    instance_file_url = instance.file 
    #  change the file name to the new name in the url
    old_file_name = str(instance_file_url).split('/')[-1] 
    old_path = str(instance_file_url).split('/')

    u = old_file_name.split('.')
    u[0] = name
    new_name_file = '.'.join(u)

    old_path[-1] = new_name_file
    renamed_str_path = '/'.join(old_path)

    renamed_path = r'%s'%renamed_str_path
    instance.file = renamed_path
    instance.save()
    return True



def rename(instance , new_name):
    # rename the file path to use os.path.sep
    new_instance = f'{os.path.sep}'.join(str(instance.file).split('/'))
    # append a path sep to the start of the new_instance
    current_path =   str(os.path.sep) + new_instance
    # getting the full path to the newly updated old path
    old_path = str(settings.MEDIA_ROOT) +  current_path 
    # Now let create a path to for the new name 
    # first let split the path using the path sep
    old_path_separated_list = old_path.split(os.path.sep)
    editing_new_name = old_path.split(os.path.sep)[-1]
    rename_old_file_name_list =  editing_new_name.split('.') 
    # Now change change the file name to the new name 
    rename_old_file_name_list[0] =  new_name
    old_name_renamed_to = '.'.join(rename_old_file_name_list)
    # print(old_name_renamed_to) 
    # create the full path for the new name 
    old_path_separated_list[-1] = old_name_renamed_to
    new_path_of_file = str(os.path.sep).join(old_path_separated_list)
    # make both new and old a raw string 
    old = r'%s'% old_path
    new = r'%s'% new_path_of_file   
    #  use os rename function to change the name of the file 
    os.rename(old,new)
    #  Now let cal the function below to update the file url in the database 
    update_file_url(instance , new_name)
    return True 