from app.models.colony_counter import simple_colony_count

def test_simple_colony_count_logic():
    image_name = "sample.jpg"
    count = simple_colony_count(image_name)
    assert isinstance(count, int)
    assert 10 <= count <= 100
