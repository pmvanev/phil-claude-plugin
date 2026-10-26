from routing import route_for


def test_known_paths_map_to_their_action():
    assert route_for("/api/export") == "export"
    assert route_for("/api/count/") == "count"


def test_any_other_path_asks_who_the_user_is():
    assert route_for("/api/anything") == "whoami"
