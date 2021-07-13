FROM python:3

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY /policy_engine.py .

COPY . .

CMD [ "python", "/test_scripts/unit_tests.py" ]
