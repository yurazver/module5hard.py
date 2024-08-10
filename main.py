import hashlib
import time

class User:
    def __init__(self, nickname: str, password: str, age: int):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    def hash_password(self, password: str):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

class Video:
    def __init__(self, title: str, duration: int, adult_mode: bool = False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname: str, password: str):
        hashed_password = int(hashlib.sha256(password.encode()).hexdigest(), 16)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                return
        print("Неверные данные для входа")

    def register(self, nickname: str, password: str, age: int):
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user

    def log_out(self):
        self.current_user = None

    def add(self, *videos):
        for video in videos:
            if not any(existing_video.title.lower() == video.title.lower() for existing_video in self.videos):
                self.videos.append(video)

    def get_videos(self, search_keyword: str):
        return [video.title for video in self.videos if search_keyword.lower() in video.title.lower()]

    def watch_video(self, title: str):
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return
        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return
                print(f"Начало просмотра {video.title}")
                while video.time_now < video.duration:
                    print(f"Время просмотра: {video.time_now}")
                    time.sleep(1) 
                    video.time_now += 1
                print("Конец видео")
                video.time_now = 0
                return
        print("Видео не найдено")


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))  # ['Лучший язык программирования 2024 года']
print(ur.get_videos('ПРОГ'))     # ['Лучший язык программирования 2024 года']

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')  # "Войдите в аккаунт, чтобы смотреть видео"
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')  # "Вам нет 18 лет, пожалуйста покиньте страницу"
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')  # Начало просмотра, идет вывод секунд

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user.nickname)  # 'vasya_pupkin'

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')  # "Видео не найдено"
