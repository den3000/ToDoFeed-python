# Нано бэкенд для ToDoFeed-aurora

Этот "бэкенд", с вашего позволения, написан для работы вот этого примера https://github.com/den3000/ToDoFeed-aurora по мотивам туториала от amvera https://docs.amvera.ru/books/amvera/page/bystryi-start

Соответственно, следуйте инстукциям от amvera, чтобы развернуть это приложение, в итоге вы получите url вида `https://app-name-user-name.amvera.io`, и этот url вам надо будет сохранить в файл с именем `api.endpoint`

Единственное, в том туториале на момент написания использовался `Flask 2.2.2`, который не будет работать с последней версией `Werkzeug`, надо тоже использовать версию `2.2.2`, но это всё уже прописано в [requirements.txt](https://github.com/den3000/ToDoFeed-python/blob/master/requirements.txt), просто имейте это ввиду.