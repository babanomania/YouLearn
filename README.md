# YouLearn

A YouTube based learning bot, that can summarize a youtube videos (based on captions) and then answer questions on the video based on the data it has learnt

| Summarizing Mode    | QA Mode |
| -------- | ------- |
| ![init mode](images/init.png)  | ![qa mode](images/qa.png)    |

# How to run

* Prepare a venv
```bash
python -m venv venv
source venv/bin/activate
```

* Install the dependencies
```bash
pip3 import -r requirements.txt
```

* Execute it as below
```bash
export OPENAI_API_KEY=...
chainlit run app.py
```
