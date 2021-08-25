from storage.database_tables import User

def test_new_user():
    new_user = User(
        first_name="f_name", last_name="l_name",
        middle_name="m_name", email="test@gmail.com",
        password="password")
    assert new_user.user_id == None
    assert new_user.first_name == "f_name"
    assert new_user.last_name == "l_name"
    assert new_user.middle_name == "m_name"
    assert new_user.email == "test@gmail.com"
    assert new_user.password == "password"
    assert new_user.creation_time == None
    assert new_user.serializable_json() == {
        'user_id': new_user.user_id,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'middle_name': new_user.middle_name,
        'email': new_user.email}
