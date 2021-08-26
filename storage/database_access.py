from passlib.hash import sha256_crypt
from storage.database_tables import db, User, Video

class Userdatabaseclients:

    @staticmethod
    def check_if_email_exists(email):
        user = User.query.filter_by(email=email).scalar() is not None
        return user

    @staticmethod
    def add_new_user(first_name, last_name, middle_name, email, password):
        hashed_password = sha256_crypt.encrypt(password)
        new_user = User(
            first_name=first_name, last_name=last_name,middle_name=middle_name,
            email=email, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.serializable_json()

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).one()
        if sha256_crypt.verify(password, user.password):
            return user.serializable_json()
        return None

    @staticmethod
    def change_password(email, password):
        user = User.query.filter_by(email=email).one()
        hashed_password = sha256_crypt.encrypt(password)
        user.password = hashed_password
        db.session.commit()
        return user.serializable_json()

    @staticmethod
    def get_user(user_id):
        user = User.query.filter_by(user_id=user_id).one()
        return user.serializable_json()
    
    @staticmethod
    def uploaded_videos():
        all_videos_info = Video.query.order_by(Video.video_id.desc())
        needed_videos = all_videos_info.limit(60)
        videos = []
        for video in needed_videos:
            videos.append(video.serializable_json())
        return videos
    
    @staticmethod
    def videos_with_name(name):
        all_videos_info = Video.query.filter_by(
            video_name=name).order_by(Video.video_id.desc())
        videos = []
        for video in all_videos_info:
            videos.append(video.serializable_json())
        return videos

    @staticmethod
    def videos_with_genre(genre):
        all_videos_info = Video.query.filter_by(
            video_genre=genre).order_by(Video.video_id.desc())
        videos = []
        for video in all_videos_info:
            videos.append(video.serializable_json())
        return videos

    @staticmethod
    def videos_with_year(year):
        year = int(year)
        all_videos_info = Video.query.filter_by(
            video_year=year).order_by(Video.video_id.desc())
        videos = []
        for video in all_videos_info:
            videos.append(video.serializable_json())
        return videos

    @staticmethod
    def videos_with_language(language):
        all_videos_info = Video.query.filter_by(
            video_language=language).order_by(Video.video_id.desc())
        videos = []
        for video in all_videos_info:
            videos.append(video.serializable_json())
        return videos
