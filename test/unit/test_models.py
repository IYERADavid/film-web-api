from storage.database_tables import User, Video

def test_new_user():
    new_user = User(
        first_name="f_name", last_name="l_name",
        middle_name="m_name", email="test@gmail.com",
        password="password"
    )
    assert new_user.user_id == None
    assert new_user.first_name == "f_name"
    assert new_user.last_name == "l_name"
    assert new_user.middle_name == "m_name"
    assert new_user.email == "test@gmail.com"
    assert new_user.password == "password"
    assert new_user.profile_picture == None
    assert new_user.creation_time == None
    assert new_user.serializable_json() == {
        'user_id': new_user.user_id,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'middle_name': new_user.middle_name,
        'email': new_user.email,
        'profile_picture': new_user.profile_picture
    }

def test_new_video():
    new_video = Video(
        video_name="V_name",video_description="some testing descrpt",
        video_photo="photo_test.png",video_filename="movie_test.mp4",
        video_year=1900,video_genre="action",video_language="English"
    )
    assert new_video.video_id == None
    assert new_video.video_name == "V_name"
    assert new_video.video_description == "some testing descrpt"
    assert new_video.video_photo == "photo_test.png"
    assert new_video.video_filename == "movie_test.mp4"
    assert new_video.video_year == 1900
    assert new_video.video_genre == "action"
    assert new_video.video_language == "English"
    assert new_video.video_time_saved == None
    assert new_video.serializable_json() == {
        'video_id': new_video.video_id,
        'video_photo': new_video.video_photo,
        'video_filename': new_video.video_filename,
        'video_name': new_video.video_name,
        'video_description': new_video.video_description,
        'active': new_video.active,
        'video_year': new_video.video_year,
        'video_genre': new_video.video_genre,
        'video_language': new_video.video_language
    }
