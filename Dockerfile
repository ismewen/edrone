FROM python:3.8.3
RUN mkdir /code
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple
COPY . /code
CMD pip install ./dutils
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
